"""
Player Routes
Handles player data retrieval and deck analysis
"""
from flask import Blueprint, request, jsonify
from services.player_service import PlayerService
from services.clash_royale import ClashRoyaleAPIError

player_bp = Blueprint('player', __name__, url_prefix='/api/players')


@player_bp.route('/<player_tag>', methods=['GET'])
def get_player(player_tag):
    """
    Get player information
    
    Args:
        player_tag: Player tag (with or without #)
    
    Query params:
        refresh: Force refresh from API (true/false)
    
    Returns:
        200: Player data
        400: Invalid request
        404: Player not found
        500: Server error
    """
    try:
        force_refresh = request.args.get('refresh', 'false').lower() == 'true'
        player_data = PlayerService.get_or_create_player(player_tag, force_refresh=force_refresh)
        
        return jsonify({
            'success': True,
            'data': player_data
        }), 200
        
    except ClashRoyaleAPIError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404 if 'not found' in str(e).lower() else 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch player: {str(e)}'
        }), 500


@player_bp.route('/<player_tag>/analyze', methods=['GET'])
def analyze_player_deck(player_tag):
    """
    Analyze player's current deck
    
    Args:
        player_tag: Player tag (with or without #)
    
    Returns:
        200: Analysis results
        400: Invalid request
        404: Player or deck not found
        500: Server error
    """
    try:
        # First ensure player data is fetched
        try:
            PlayerService.get_or_create_player(player_tag, force_refresh=True)
        except ClashRoyaleAPIError as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 404 if 'not found' in str(e).lower() else 400
        
        # Analyze deck
        analysis_data = PlayerService.analyze_player_deck(player_tag)
        
        return jsonify({
            'success': True,
            'data': analysis_data
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to analyze deck: {str(e)}'
        }), 500


@player_bp.route('', methods=['GET'])
def list_players():
    """
    Get list of all players with pagination
    
    Query params:
        limit: Number of players per page (default: 20)
        offset: Offset for pagination (default: 0)
    
    Returns:
        200: List of players
        400: Invalid parameters
    """
    try:
        limit = int(request.args.get('limit', 20))
        offset = int(request.args.get('offset', 0))
        
        if limit < 1 or limit > 100:
            return jsonify({
                'success': False,
                'error': 'Limit must be between 1 and 100'
            }), 400
        
        if offset < 0:
            return jsonify({
                'success': False,
                'error': 'Offset must be non-negative'
            }), 400
        
        result = PlayerService.get_all_players(limit=limit, offset=offset)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except ValueError:
        return jsonify({
            'success': False,
            'error': 'Invalid limit or offset parameter'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch players: {str(e)}'
        }), 500


@player_bp.route('/search', methods=['GET'])
def search_players():
    """
    Search players by tag or name
    
    Query params:
        q: Search query (player tag or name)
    
    Returns:
        200: Search results
        400: Missing query parameter
    """
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Search query is required'
        }), 400
    
    try:
        # Try to fetch as player tag
        if query.startswith('#') or len(query) <= 15:
            try:
                player_data = PlayerService.get_or_create_player(query)
                return jsonify({
                    'success': True,
                    'data': {
                        'players': [player_data],
                        'total': 1
                    }
                }), 200
            except ClashRoyaleAPIError:
                pass
        
        # Search in database by name
        from models import Player
        players = Player.query.filter(Player.name.ilike(f'%{query}%')).limit(10).all()
        
        return jsonify({
            'success': True,
            'data': {
                'players': [p.to_dict() for p in players],
                'total': len(players)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Search failed: {str(e)}'
        }), 500