"""
Database Models for Clash Royale Deck Analyzer
Uses SQLAlchemy ORM for MySQL database interaction
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import json

db = SQLAlchemy()


class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'


class Card(db.Model):
    """Card model for Clash Royale cards"""
    __tablename__ = 'cards'
    
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, unique=True, nullable=False, index=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    max_level = db.Column(db.Integer, nullable=False)
    icon_url = db.Column(db.String(255))
    elixir_cost = db.Column(db.Integer, nullable=False, index=True)
    rarity = db.Column(db.Enum('common', 'rare', 'epic', 'legendary', 'champion'), nullable=False)
    card_type = db.Column(db.Enum('troop', 'spell', 'building'), nullable=False)
    
    # Analysis attributes
    is_win_condition = db.Column(db.Boolean, default=False)
    is_air_targeting = db.Column(db.Boolean, default=False)
    is_splash_damage = db.Column(db.Boolean, default=False)
    is_tank = db.Column(db.Boolean, default=False)
    is_spell = db.Column(db.Boolean, default=False)
    spell_type = db.Column(db.Enum('light', 'heavy', 'none'), default='none')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    deck_cards = db.relationship('DeckCard', back_populates='card', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert card to dictionary"""
        return {
            'id': self.id,
            'card_id': self.card_id,
            'name': self.name,
            'max_level': self.max_level,
            'icon_url': self.icon_url,
            'elixir_cost': self.elixir_cost,
            'rarity': self.rarity,
            'card_type': self.card_type,
            'is_win_condition': self.is_win_condition,
            'is_air_targeting': self.is_air_targeting,
            'is_splash_damage': self.is_splash_damage,
            'is_tank': self.is_tank,
            'is_spell': self.is_spell,
            'spell_type': self.spell_type
        }
    
    def __repr__(self):
        return f'<Card {self.name} ({self.elixir_cost} elixir)>'


class Player(db.Model):
    """Player model for Clash Royale players"""
    __tablename__ = 'players'
    
    id = db.Column(db.Integer, primary_key=True)
    player_tag = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    trophies = db.Column(db.Integer, default=0, index=True)
    best_trophies = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    battle_count = db.Column(db.Integer, default=0)
    three_crown_wins = db.Column(db.Integer, default=0)
    arena_id = db.Column(db.Integer)
    arena_name = db.Column(db.String(50))
    clan_name = db.Column(db.String(100))
    clan_tag = db.Column(db.String(20))
    exp_level = db.Column(db.Integer, default=1)
    
    last_fetched = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    decks = db.relationship('Deck', back_populates='player', cascade='all, delete-orphan')
    
    def to_dict(self, include_deck=True):
        """Convert player to dictionary"""
        player_dict = {
            'id': self.id,
            'player_tag': self.player_tag,
            'name': self.name,
            'trophies': self.trophies,
            'best_trophies': self.best_trophies,
            'wins': self.wins,
            'losses': self.losses,
            'battle_count': self.battle_count,
            'three_crown_wins': self.three_crown_wins,
            'arena_id': self.arena_id,
            'arena_name': self.arena_name,
            'clan_name': self.clan_name,
            'clan_tag': self.clan_tag,
            'exp_level': self.exp_level,
            'last_fetched': self.last_fetched.isoformat() if self.last_fetched else None
        }
        
        # Include current deck if requested
        if include_deck:
            current_deck = Deck.query.filter_by(player_id=self.id, is_current_deck=True).first()
            if current_deck:
                deck_cards = DeckCard.query.filter_by(deck_id=current_deck.id).order_by(DeckCard.position).all()
                player_dict['currentDeck'] = [
                    {
                        'name': dc.card.name,
                        'card_id': dc.card.card_id,
                        'level': dc.card_level,
                        'elixirCost': dc.card.elixir_cost,
                        'iconUrls': {
                            'medium': dc.card.icon_url,
                        },
                        'id': dc.card.id,
                        'rarity': dc.card.rarity,
                        'card_type': dc.card.card_type
                    }
                    for dc in deck_cards
                ]
            else:
                player_dict['currentDeck'] = []
            
            # Also include all cards as a fallback
            all_cards = Card.query.all()
            player_dict['cards'] = [
                {
                    'name': card.name,
                    'card_id': card.card_id,
                    'elixirCost': card.elixir_cost,
                    'iconUrls': {
                        'medium': card.icon_url,
                    },
                    'id': card.id,
                    'rarity': card.rarity,
                    'card_type': card.card_type,
                    'maxLevel': card.max_level
                }
                for card in all_cards
            ]
        
        return player_dict
    
    def __repr__(self):
        return f'<Player {self.name} ({self.player_tag})>'


class Deck(db.Model):
    """Deck model for player decks"""
    __tablename__ = 'decks'
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id', ondelete='CASCADE'), nullable=False, index=True)
    deck_hash = db.Column(db.String(64), unique=True, nullable=False, index=True)
    avg_elixir = db.Column(db.Numeric(3, 2), nullable=False, index=True)
    is_current_deck = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    player = db.relationship('Player', back_populates='decks')
    deck_cards = db.relationship('DeckCard', back_populates='deck', cascade='all, delete-orphan')
    analyses = db.relationship('DeckAnalysis', back_populates='deck', cascade='all, delete-orphan')
    
    @staticmethod
    def generate_hash(card_ids):
        """Generate unique hash for a deck based on sorted card IDs"""
        sorted_ids = sorted(card_ids)
        hash_string = '-'.join(map(str, sorted_ids))
        return hashlib.sha256(hash_string.encode()).hexdigest()
    
    def to_dict(self, include_cards=True, include_analysis=False):
        """Convert deck to dictionary"""
        result = {
            'id': self.id,
            'player_id': self.player_id,
            'deck_hash': self.deck_hash,
            'avg_elixir': float(self.avg_elixir),
            'is_current_deck': self.is_current_deck,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_cards:
            result['cards'] = [dc.to_dict() for dc in self.deck_cards]
        
        if include_analysis and self.analyses:
            # Get the latest analysis
            latest_analysis = sorted(self.analyses, key=lambda x: x.created_at, reverse=True)[0]
            result['analysis'] = latest_analysis.to_dict()
        
        return result
    
    def __repr__(self):
        return f'<Deck {self.id} (avg: {self.avg_elixir})>'


class DeckCard(db.Model):
    """DeckCard model for many-to-many relationship between decks and cards"""
    __tablename__ = 'deck_cards'
    
    id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id', ondelete='CASCADE'), nullable=False, index=True)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id', ondelete='CASCADE'), nullable=False, index=True)
    card_level = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    deck = db.relationship('Deck', back_populates='deck_cards')
    card = db.relationship('Card', back_populates='deck_cards')
    
    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('deck_id', 'card_id', name='unique_deck_card'),
    )
    
    def to_dict(self):
        """Convert deck card to dictionary"""
        return {
            'id': self.id,
            'card': self.card.to_dict() if self.card else None,
            'card_level': self.card_level,
            'position': self.position
        }
    
    def __repr__(self):
        return f'<DeckCard {self.card.name if self.card else "Unknown"} L{self.card_level}>'


class DeckAnalysis(db.Model):
    """DeckAnalysis model for storing analysis results"""
    __tablename__ = 'deck_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Metrics
    avg_elixir = db.Column(db.Numeric(3, 2), nullable=False)
    air_targeting_count = db.Column(db.Integer, default=0)
    splash_damage_count = db.Column(db.Integer, default=0)
    win_condition_count = db.Column(db.Integer, default=0)
    light_spell_count = db.Column(db.Integer, default=0)
    heavy_spell_count = db.Column(db.Integer, default=0)
    tank_count = db.Column(db.Integer, default=0)
    
    # Analysis results (stored as JSON)
    strengths = db.Column(db.JSON)
    weaknesses = db.Column(db.JSON)
    suggestions = db.Column(db.JSON)
    overall_rating = db.Column(db.Enum('excellent', 'good', 'average', 'poor'), default='average')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    deck = db.relationship('Deck', back_populates='analyses')
    
    def to_dict(self):
        """Convert analysis to dictionary"""
        return {
            'id': self.id,
            'deck_id': self.deck_id,
            'metrics': {
                'avg_elixir': float(self.avg_elixir),
                'air_targeting_count': self.air_targeting_count,
                'splash_damage_count': self.splash_damage_count,
                'win_condition_count': self.win_condition_count,
                'light_spell_count': self.light_spell_count,
                'heavy_spell_count': self.heavy_spell_count,
                'tank_count': self.tank_count
            },
            'strengths': self.strengths,
            'weaknesses': self.weaknesses,
            'suggestions': self.suggestions,
            'overall_rating': self.overall_rating,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<DeckAnalysis {self.id} ({self.overall_rating})>'