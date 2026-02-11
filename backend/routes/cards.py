"""
Cards Routes
Handles card data retrieval and management
"""
from flask import Blueprint, request, jsonify
from models import db, Card
from services.clash_royale import get_api_service, ClashRoyaleAPIError

cards_bp = Blueprint('cards', __name__, url_prefix='/api/cards')


@cards_bp.route('', methods=['GET'])
def get_all_cards():
    """
    Get all cards from database
    
    Query params:
        type: Filter by card type (troop, spell, building)
        rarity: Filter by rarity (common, rare, epic, legendary)
    
    Returns:
        200: List of cards
        500: Server error
    """
    try:
        query = Card.query
        
        # Apply filters
        card_type = request.args.get('type')
        if card_type:
            query = query.filter_by(card_type=card_type)
        
        rarity = request.args.get('rarity')
        if rarity:
            query = query.filter_by(rarity=rarity)
        
        # Order by elixir cost and name
        cards = query.order_by(Card.elixir_cost, Card.name).all()
        
        return jsonify({
            'success': True,
            'data': {
                'cards': [card.to_dict() for card in cards],
                'total': len(cards)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch cards: {str(e)}'
        }), 500


@cards_bp.route('/<int:card_id>', methods=['GET'])
def get_card(card_id):
    """
    Get specific card by ID
    
    Args:
        card_id: Card database ID
    
    Returns:
        200: Card data
        404: Card not found
    """
    card = Card.query.get(card_id)
    
    if not card:
        return jsonify({
            'success': False,
            'error': 'Card not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': card.to_dict()
    }), 200


@cards_bp.route('/sync', methods=['POST'])
def sync_cards():
    """
    Sync cards from Clash Royale API to database
    This should be run initially to populate the card database
    
    Returns:
        200: Sync successful
        500: Sync failed
    """
    try:
        api_service = get_api_service()
        api_cards = api_service.get_cards()
        
        synced_count = 0
        updated_count = 0
        
        for api_card in api_cards:
            parsed_card = api_service.parse_card_data(api_card)
            
            # Check if card exists
            card = Card.query.filter_by(card_id=parsed_card['card_id']).first()
            
            if card:
                # Update existing card
                card.name = parsed_card['name']
                card.max_level = parsed_card['max_level']
                card.icon_url = parsed_card['icon_url']
                card.elixir_cost = parsed_card.get('elixir_cost', card.elixir_cost)
                updated_count += 1
            else:
                # Create new card (with default analysis attributes)
                card = Card(
                    card_id=parsed_card['card_id'],
                    name=parsed_card['name'],
                    max_level=parsed_card['max_level'],
                    icon_url=parsed_card['icon_url'],
                    elixir_cost=parsed_card.get('elixir_cost', 0),
                    rarity='common',  # Default, should be updated in schema
                    card_type='troop'  # Default, should be updated in schema
                )
                db.session.add(card)
                synced_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Cards synced successfully',
            'data': {
                'synced': synced_count,
                'updated': updated_count,
                'total': synced_count + updated_count
            }
        }), 200
        
    except ClashRoyaleAPIError as e:
        return jsonify({
            'success': False,
            'error': f'API error: {str(e)}'
        }), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Sync failed: {str(e)}'
        }), 500


@cards_bp.route('/statistics', methods=['GET'])
def get_card_statistics():
    """
    Get card usage statistics
    
    Returns:
        200: Card statistics
        500: Server error
    """
    try:
        from sqlalchemy import func
        from models import DeckCard
        
        # Get most used cards
        most_used = db.session.query(
            Card,
            func.count(DeckCard.id).label('usage_count')
        ).join(
            DeckCard, Card.id == DeckCard.card_id
        ).group_by(
            Card.id
        ).order_by(
            func.count(DeckCard.id).desc()
        ).limit(20).all()
        
        # Format results
        statistics = []
        for card, usage_count in most_used:
            card_dict = card.to_dict()
            card_dict['usage_count'] = usage_count
            statistics.append(card_dict)
        
        return jsonify({
            'success': True,
            'data': {
                'most_used_cards': statistics
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch statistics: {str(e)}'
        }), 500