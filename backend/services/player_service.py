"""
Player Service
Handles player-related database operations
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from flask import current_app
from models import db, Player, Deck, DeckCard, Card, DeckAnalysis
from services.clash_royale import get_api_service, ClashRoyaleAPIError
from services.deck_analyzer import get_analyzer


class PlayerService:
    """Service for managing players and their decks"""
    
    @staticmethod
    def get_or_create_player(player_tag: str, force_refresh: bool = False) -> Dict:
        """
        Get player from database or fetch from API if not cached or refresh needed
        
        Args:
            player_tag: Player tag (with or without #)
            force_refresh: Force refresh from API even if cached
            
        Returns:
            Dict: Player data with current deck
            
        Raises:
            ClashRoyaleAPIError: If API request fails
        """
        # Normalize player tag
        if not player_tag.startswith('#'):
            player_tag = f'#{player_tag}'
        
        player = Player.query.filter_by(player_tag=player_tag).first()
        cache_duration = current_app.config.get('PLAYER_CACHE_DURATION', 300)
        
        # Check if we need to fetch from API
        should_fetch = (
            force_refresh or
            player is None or
            (datetime.utcnow() - player.last_fetched).total_seconds() > cache_duration
        )
        
        extra_api_fields = {}
        
        if should_fetch:
            # Fetch from API
            api_service = get_api_service()
            api_data = api_service.get_player(player_tag)
            player_data = api_service.parse_player_data(api_data)
            
            # Store extra fields from API
            extra_api_fields = {
                'current_favourite_card': player_data.get('current_favourite_card')
            }
            
            # Update or create player
            if player is None:
                player = Player()
            
            # Update player fields
            player.player_tag = player_data['player_tag']
            player.name = player_data['name']
            player.trophies = player_data['trophies']
            player.best_trophies = player_data['best_trophies']
            player.wins = player_data['wins']
            player.losses = player_data['losses']
            player.battle_count = player_data['battle_count']
            player.three_crown_wins = player_data['three_crown_wins']
            player.arena_id = player_data['arena_id']
            player.arena_name = player_data['arena_name']
            player.clan_name = player_data['clan_name']
            player.clan_tag = player_data['clan_tag']
            player.exp_level = player_data['exp_level']
            player.last_fetched = datetime.utcnow()
            
            db.session.add(player)
            db.session.commit()
            
            # Process deck
            if player_data.get('current_deck'):
                PlayerService._process_player_deck(player, player_data['current_deck'])
        
        # Get player dict
        player_dict = player.to_dict()
        
        # Add extra API fields if available
        if extra_api_fields.get('current_favourite_card'):
            player_dict['currentFavouriteCard'] = extra_api_fields['current_favourite_card']
        
        return player_dict
    
    @staticmethod
    def _process_player_deck(player: Player, deck_data: List[Dict]) -> Deck:
        """
        Process and save player's current deck
        
        Args:
            player: Player object
            deck_data: List of card data from API
            
        Returns:
            Deck: Created or existing deck object
        """
        # First, ensure all cards exist in database by syncing if needed
        from services.clash_royale import get_api_service
        
        api_service = get_api_service()
        api_cards = api_service.get_cards()
        
        # Map card IDs from API to database, creating cards if needed
        card_map = {}  # Maps API card_id to database Card object
        total_elixir = 0
        
        for card_data in deck_data:
            api_card_id = card_data.get('id')
            card = Card.query.filter_by(card_id=api_card_id).first()
            
            # If card doesn't exist, try to create it from API data
            if not card:
                # Find the card data from the full API cards list
                api_card_data = next((c for c in api_cards if c.get('id') == api_card_id), None)
                if api_card_data:
                    parsed_card = api_service.parse_card_data(api_card_data)
                    # Ensure rarity is lowercase for database
                    rarity = parsed_card.get('rarity', 'common').lower()
                    card = Card(
                        card_id=parsed_card['card_id'],
                        name=parsed_card['name'],
                        card_type=parsed_card['card_type'],
                        rarity=rarity,
                        elixir_cost=parsed_card['elixir_cost'],
                        max_level=parsed_card.get('max_level', 14),
                        icon_url=parsed_card.get('icon_url', '')
                    )
                    db.session.add(card)
                    db.session.flush()  # Get the card ID
            
            if card:
                card_map[len(card_map)] = card
                total_elixir += card.elixir_cost
        
        # Generate deck hash from card IDs
        card_ids = [card.id for card in card_map.values()]
        deck_hash = Deck.generate_hash(card_ids)
        avg_elixir = round(total_elixir / len(card_ids), 2) if card_ids else 0
        
        # Check if deck already exists
        deck = Deck.query.filter_by(deck_hash=deck_hash).first()
        
        if deck is None:
            # Mark old decks as not current
            Deck.query.filter_by(player_id=player.id, is_current_deck=True).update({'is_current_deck': False})
            
            # Create new deck
            deck = Deck(
                player_id=player.id,
                deck_hash=deck_hash,
                avg_elixir=avg_elixir,
                is_current_deck=True
            )
            db.session.add(deck)
            db.session.flush()  # Get deck ID
            
            # Add deck cards
            for position, card_data in enumerate(deck_data):
                card_id = card_data.get('id')
                card = Card.query.filter_by(card_id=card_id).first()
                
                if card:
                    deck_card = DeckCard(
                        deck_id=deck.id,
                        card_id=card.id,
                        card_level=card_data.get('level', 1),
                        position=position
                    )
                    db.session.add(deck_card)
            
            db.session.commit()
        else:
            # Update existing deck as current for this player
            Deck.query.filter_by(player_id=player.id, is_current_deck=True).update({'is_current_deck': False})
            deck.is_current_deck = True
            db.session.commit()
        
        return deck
    
    @staticmethod
    def analyze_player_deck(player_tag: str) -> Dict:
        """
        Analyze player's current deck
        
        Args:
            player_tag: Player tag (with or without #)
            
        Returns:
            Dict: Complete analysis results
            
        Raises:
            ValueError: If player not found or no deck available
        """
        # Normalize player tag
        if not player_tag.startswith('#'):
            player_tag = f'#{player_tag}'
        
        player = Player.query.filter_by(player_tag=player_tag).first()
        
        if not player:
            raise ValueError(f"Player {player_tag} not found")
        
        # Get current deck
        deck = Deck.query.filter_by(player_id=player.id, is_current_deck=True).first()
        
        if not deck:
            raise ValueError(f"No current deck found for player {player_tag}")
        
        # Check if analysis already exists
        existing_analysis = DeckAnalysis.query.filter_by(deck_id=deck.id).order_by(DeckAnalysis.created_at.desc()).first()
        
        if existing_analysis:
            # Return existing analysis if it's recent (within 1 hour)
            if (datetime.utcnow() - existing_analysis.created_at).total_seconds() < 3600:
                return {
                    'player': player.to_dict(),
                    'deck': deck.to_dict(include_cards=True),
                    'analysis': existing_analysis.to_dict()
                }
        
        # Get deck cards
        deck_cards = DeckCard.query.filter_by(deck_id=deck.id).all()
        cards = [dc.card for dc in deck_cards]
        
        # Analyze deck
        analyzer = get_analyzer()
        analysis_result = analyzer.analyze_deck(cards)
        
        # Save analysis
        deck_analysis = DeckAnalysis(
            deck_id=deck.id,
            avg_elixir=analysis_result['metrics']['avg_elixir'],
            air_targeting_count=analysis_result['metrics']['air_targeting_count'],
            splash_damage_count=analysis_result['metrics']['splash_damage_count'],
            win_condition_count=analysis_result['metrics']['win_condition_count'],
            light_spell_count=analysis_result['metrics']['light_spell_count'],
            heavy_spell_count=analysis_result['metrics']['heavy_spell_count'],
            tank_count=analysis_result['metrics']['tank_count'],
            strengths=analysis_result['strengths'],
            weaknesses=analysis_result['weaknesses'],
            suggestions=analysis_result['suggestions'],
            overall_rating=analysis_result['overall_rating']
        )
        db.session.add(deck_analysis)
        db.session.commit()
        
        return {
            'player': player.to_dict(),
            'deck': deck.to_dict(include_cards=True),
            'analysis': deck_analysis.to_dict()
        }
    
    @staticmethod
    def get_all_players(limit: int = 20, offset: int = 0) -> Dict:
        """
        Get all players with pagination
        
        Args:
            limit: Number of players per page
            offset: Offset for pagination
            
        Returns:
            Dict: Players with pagination info
        """
        query = Player.query.order_by(Player.trophies.desc())
        total = query.count()
        players = query.limit(limit).offset(offset).all()
        
        return {
            'players': [p.to_dict() for p in players],
            'total': total,
            'limit': limit,
            'offset': offset
        }