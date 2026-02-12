"""
Main Flask Application
Clash Royale Deck Analyzer Backend
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import get_config
from models import db
import os


def create_app(config_name=None):
    """
    Application factory pattern
    
    Args:
        config_name: Configuration name (development, production, testing)
        
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    jwt = JWTManager(app)
    
    # Create database tables on startup
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f'Warning: Failed to create database tables: {e}')
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.players import player_bp
    from routes.cards import cards_bp
    from routes.roast import roast_bp
    from services.roast_service import generate_roast    
    app.register_blueprint(auth_bp)
    app.register_blueprint(player_bp)
    app.register_blueprint(cards_bp)
    app.register_blueprint(roast_bp)
    
    # Root route
    @app.route('/')
    def index():
        """Root endpoint"""
        return jsonify({
            'message': 'Clash Royale Deck Analyzer API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'players': '/api/players',
                'cards': '/api/cards',
                'roast': '/api/roast'
            }
        })
@app.route('/debug/ip')
def get_ip():
    ip = requests.get('https://api.ipify.org').text
    return {"server_ip": ip}
    # Health check
    @app.route('/health')
    def health():
        """Health check endpoint"""
        try:
            # Check database connection
            db.session.execute('SELECT 1')
            db_status = 'healthy'
        except Exception as e:
            db_status = f'unhealthy: {str(e)}'
        
        return jsonify({
            'status': 'healthy' if db_status == 'healthy' else 'unhealthy',
            'database': db_status
        })


    @app.route('/debug/cr_test', methods=['GET'])
    def debug_cr_test():
        """Development-only endpoint to validate the configured Clash Royale API key.

        Returns a masked indicator of whether a key is configured and attempts
        a test request to the Clash Royale API for a given player (query param
        `player`, defaults to #2GYQ8L9PR).
        """
        # Only allow in development to avoid exposing key diagnostics in prod
        if app.config.get('ENVIRONMENT', 'development') != 'development':
            return jsonify({'success': False, 'error': 'Disabled outside development environment'}), 403

        try:
            from services.clash_royale import get_api_service, ClashRoyaleAPIError

            api = get_api_service()
            key = app.config.get('CLASH_ROYALE_API_KEY', '')
            masked = (f"{key[:4]}...{key[-4:]}" if len(key) > 8 else ('set' if key else 'not set'))

            player_tag = request.args.get('player', '#2GYQ8L9PR')

            try:
                api.get_player(player_tag)
                return jsonify({'success': True, 'message': 'API key validated (200)', 'masked_key': masked}), 200
            except ClashRoyaleAPIError as e:
                return jsonify({'success': False, 'error': str(e), 'masked_key': masked}), 400
        except Exception as e:
            return jsonify({'success': False, 'error': f'Unexpected error: {str(e)}'}), 500
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({
            'success': False,
            'error': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Handle expired tokens"""
        return jsonify({
            'success': False,
            'error': 'Token has expired'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Handle invalid tokens"""
        return jsonify({
            'success': False,
            'error': 'Invalid token'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """Handle missing tokens"""
        return jsonify({
            'success': False,
            'error': 'Authorization token is missing'
        }), 401
    
    # CLI commands
    @app.cli.command()
    def init_db():
        """Initialize the database"""
        with app.app_context():
            db.create_all()
            print("Database initialized successfully!")
    
    @app.cli.command()
    def seed_cards():
        """Seed the database with card data"""
        with app.app_context():
            from services.clash_royale import get_api_service
            from models import Card
            
            try:
                api_service = get_api_service()
                api_cards = api_service.get_cards()
                
                for api_card in api_cards:
                    parsed_card = api_service.parse_card_data(api_card)
                    
                    # Check if card exists
                    card = Card.query.filter_by(card_id=parsed_card['card_id']).first()
                    
                    if not card:
                        card = Card(
                            card_id=parsed_card['card_id'],
                            name=parsed_card['name'],
                            max_level=parsed_card['max_level'],
                            icon_url=parsed_card['icon_url'],
                            elixir_cost=parsed_card.get('elixir_cost', 0),
                            rarity='common',
                            card_type='troop'
                        )
                        db.session.add(card)
                
                db.session.commit()
                print(f"Successfully seeded {len(api_cards)} cards!")
                
            except Exception as e:
                db.session.rollback()
                print(f"Error seeding cards: {str(e)}")
    
    return app

if __name__ == '__main__':
    # Get environment
    env = os.getenv('FLASK_ENV', 'development')
    app = create_app(env)
    
    # Run application
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )