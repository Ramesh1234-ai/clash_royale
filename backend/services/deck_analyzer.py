"""
Deck Analysis Service
Implements rule-based deck analysis logic
"""
from typing import Dict, List, Tuple
from flask import current_app
from models import Card


class DeckAnalyzer:
    """Analyzes Clash Royale decks and provides insights"""
    
    def __init__(self):
        """Initialize the deck analyzer with thresholds from config"""
        self.thresholds = current_app.config.get('ANALYSIS_THRESHOLDS', {
            'high_elixir': 4.5,
            'low_elixir': 3.0,
            'min_air_defense': 2,
            'min_splash': 2,
            'min_win_conditions': 1,
            'max_win_conditions': 3,
        })
    
    def analyze_deck(self, cards: List[Card]) -> Dict:
        """
        Analyze a deck and return comprehensive analysis
        
        Args:
            cards: List of Card objects (should be 8 cards)
            
        Returns:
            Dict: Complete analysis with metrics, strengths, weaknesses, and suggestions
        """
        if len(cards) != 8:
            raise ValueError(f"Deck must contain exactly 8 cards, got {len(cards)}")
        
        # Calculate metrics
        metrics = self._calculate_metrics(cards)
        
        # Analyze strengths
        strengths = self._analyze_strengths(cards, metrics)
        
        # Analyze weaknesses
        weaknesses = self._analyze_weaknesses(cards, metrics)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(cards, metrics, weaknesses)
        
        # Calculate overall rating
        overall_rating = self._calculate_overall_rating(strengths, weaknesses)
        
        return {
            'metrics': metrics,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'suggestions': suggestions,
            'overall_rating': overall_rating
        }
    
    def _calculate_metrics(self, cards: List[Card]) -> Dict:
        """Calculate deck metrics"""
        total_elixir = sum(card.elixir_cost for card in cards)
        avg_elixir = round(total_elixir / len(cards), 2)
        
        air_targeting_count = sum(1 for card in cards if card.is_air_targeting)
        splash_damage_count = sum(1 for card in cards if card.is_splash_damage)
        win_condition_count = sum(1 for card in cards if card.is_win_condition)
        tank_count = sum(1 for card in cards if card.is_tank)
        
        spell_counts = self._count_spells(cards)
        
        return {
            'avg_elixir': avg_elixir,
            'air_targeting_count': air_targeting_count,
            'splash_damage_count': splash_damage_count,
            'win_condition_count': win_condition_count,
            'light_spell_count': spell_counts['light'],
            'heavy_spell_count': spell_counts['heavy'],
            'tank_count': tank_count,
            'total_spells': spell_counts['total']
        }
    
    def _count_spells(self, cards: List[Card]) -> Dict:
        """Count spell types in deck"""
        light_spells = sum(1 for card in cards if card.spell_type == 'light')
        heavy_spells = sum(1 for card in cards if card.spell_type == 'heavy')
        
        return {
            'light': light_spells,
            'heavy': heavy_spells,
            'total': light_spells + heavy_spells
        }
    
    def _analyze_strengths(self, cards: List[Card], metrics: Dict) -> List[Dict]:
        """Identify deck strengths"""
        strengths = []
        
        # Fast cycle deck
        if metrics['avg_elixir'] < self.thresholds['low_elixir']:
            strengths.append({
                'category': 'Cycle Speed',
                'title': 'Fast Cycle Deck',
                'description': f"With an average elixir cost of {metrics['avg_elixir']}, this deck cycles extremely fast, allowing you to quickly return to key cards and apply constant pressure."
            })
        
        # Good elixir balance
        if self.thresholds['low_elixir'] <= metrics['avg_elixir'] <= self.thresholds['high_elixir']:
            strengths.append({
                'category': 'Balance',
                'title': 'Well-Balanced Elixir',
                'description': f"Average elixir of {metrics['avg_elixir']} provides a good balance between defense and offense without being too heavy or too light."
            })
        
        # Strong air defense
        if metrics['air_targeting_count'] >= self.thresholds['min_air_defense'] + 1:
            strengths.append({
                'category': 'Air Defense',
                'title': 'Excellent Air Defense',
                'description': f"With {metrics['air_targeting_count']} air-targeting cards, this deck is well-equipped to handle aerial threats like Balloon, Lava Hound, and flying troops."
            })
        
        # Good splash damage
        if metrics['splash_damage_count'] >= self.thresholds['min_splash']:
            strengths.append({
                'category': 'Area Damage',
                'title': 'Strong Splash Damage',
                'description': f"Having {metrics['splash_damage_count']} splash damage cards makes this deck effective against swarm troops like Skeleton Army, Minion Horde, and Goblin Gang."
            })
        
        # Multiple win conditions
        if metrics['win_condition_count'] >= 2:
            strengths.append({
                'category': 'Win Conditions',
                'title': 'Multiple Win Conditions',
                'description': f"This deck has {metrics['win_condition_count']} win conditions, making it unpredictable and harder for opponents to defend against."
            })
        
        # Good spell balance
        if metrics['light_spell_count'] >= 1 and metrics['heavy_spell_count'] >= 1:
            strengths.append({
                'category': 'Spells',
                'title': 'Balanced Spell Suite',
                'description': f"Having both light ({metrics['light_spell_count']}) and heavy ({metrics['heavy_spell_count']}) spells provides versatility in dealing with various threats and supporting pushes."
            })
        
        # Tank synergy
        if metrics['tank_count'] >= 2:
            strengths.append({
                'category': 'Tank Support',
                'title': 'Strong Tank Presence',
                'description': f"With {metrics['tank_count']} tanks, this deck can create powerful pushes by protecting support troops and applying sustained pressure."
            })
        
        return strengths
    
    def _analyze_weaknesses(self, cards: List[Card], metrics: Dict) -> List[Dict]:
        """Identify deck weaknesses"""
        weaknesses = []
        
        # Heavy deck
        if metrics['avg_elixir'] > self.thresholds['high_elixir']:
            weaknesses.append({
                'category': 'Cycle Speed',
                'title': 'Heavy Deck - Slow Cycle',
                'description': f"Average elixir of {metrics['avg_elixir']} makes this deck slow to cycle. You may struggle against faster decks and have difficulty defending when low on elixir.",
                'severity': 'high'
            })
        
        # Weak air defense
        if metrics['air_targeting_count'] < self.thresholds['min_air_defense']:
            weaknesses.append({
                'category': 'Air Defense',
                'title': 'Vulnerable to Air Attacks',
                'description': f"Only {metrics['air_targeting_count']} air-targeting card(s) in this deck. You'll struggle against air-heavy decks with Balloon, Lava Hound, or mass flying troops.",
                'severity': 'high'
            })
        
        # Weak against swarms
        if metrics['splash_damage_count'] < self.thresholds['min_splash']:
            weaknesses.append({
                'category': 'Area Damage',
                'title': 'Weak Against Swarm Decks',
                'description': f"With only {metrics['splash_damage_count']} splash damage card(s), you may struggle to defend against swarm troops like Skeleton Army, Goblin Gang, and Minion Horde.",
                'severity': 'high'
            })
        
        # No big spell
        if metrics['heavy_spell_count'] == 0:
            weaknesses.append({
                'category': 'Spells',
                'title': 'No Heavy Spell',
                'description': "Without a heavy spell (Fireball, Rocket, Lightning, Poison), you'll have difficulty dealing with buildings like X-Bow, Mortar, or Tesla, and may struggle to finish low-HP towers.",
                'severity': 'medium'
            })
        
        # No small spell
        if metrics['light_spell_count'] == 0:
            weaknesses.append({
                'category': 'Spells',
                'title': 'No Light Spell',
                'description': "Without a light spell (Zap, Log, Arrows, Snowball), you may struggle to counter swarm troops quickly and reset charging units like Prince or Inferno Dragon.",
                'severity': 'medium'
            })
        
        # No win condition
        if metrics['win_condition_count'] < self.thresholds['min_win_conditions']:
            weaknesses.append({
                'category': 'Win Conditions',
                'title': 'No Clear Win Condition',
                'description': "This deck lacks a clear win condition. Without a reliable tower-targeting card, you may struggle to deal consistent tower damage.",
                'severity': 'high'
            })
        
        # Too many win conditions
        if metrics['win_condition_count'] > self.thresholds['max_win_conditions']:
            weaknesses.append({
                'category': 'Win Conditions',
                'title': 'Too Many Win Conditions',
                'description': f"Having {metrics['win_condition_count']} win conditions might make the deck unfocused. Consider replacing one with a support or defensive card.",
                'severity': 'low'
            })
        
        # Too spell-heavy
        if metrics['total_spells'] >= 4:
            weaknesses.append({
                'category': 'Spells',
                'title': 'Too Spell-Heavy',
                'description': f"With {metrics['total_spells']} spells, you may lack troops for defense and counter-pushes. Consider replacing one spell with a versatile troop.",
                'severity': 'medium'
            })
        
        return weaknesses
    
    def _generate_suggestions(self, cards: List[Card], metrics: Dict, weaknesses: List[Dict]) -> List[Dict]:
        """Generate card replacement suggestions based on weaknesses"""
        suggestions = []
        card_names = [card.name for card in cards]
        
        # Suggest air defense if weak
        if metrics['air_targeting_count'] < self.thresholds['min_air_defense']:
            air_defense_suggestions = ['Musketeer', 'Mega Minion', 'Archers', 'Electro Wizard', 'Baby Dragon', 'Tesla', 'Inferno Tower']
            available_suggestions = [card for card in air_defense_suggestions if card not in card_names]
            
            if available_suggestions:
                suggestions.append({
                    'type': 'Add Air Defense',
                    'reason': 'Deck is vulnerable to air attacks',
                    'consider_adding': available_suggestions[:3],
                    'consider_removing': self._suggest_removals(cards, exclude_types=['air_targeting'])
                })
        
        # Suggest splash if weak
        if metrics['splash_damage_count'] < self.thresholds['min_splash']:
            splash_suggestions = ['Valkyrie', 'Baby Dragon', 'Wizard', 'Bomber', 'Arrows', 'Fireball', 'Log']
            available_suggestions = [card for card in splash_suggestions if card not in card_names]
            
            if available_suggestions:
                suggestions.append({
                    'type': 'Add Splash Damage',
                    'reason': 'Deck struggles against swarm troops',
                    'consider_adding': available_suggestions[:3],
                    'consider_removing': self._suggest_removals(cards, exclude_types=['splash'])
                })
        
        # Suggest big spell if missing
        if metrics['heavy_spell_count'] == 0:
            heavy_spell_suggestions = ['Fireball', 'Rocket', 'Lightning', 'Poison']
            available_suggestions = [card for card in heavy_spell_suggestions if card not in card_names]
            
            if available_suggestions:
                suggestions.append({
                    'type': 'Add Heavy Spell',
                    'reason': 'Need spell to deal with buildings and finish towers',
                    'consider_adding': available_suggestions[:3],
                    'consider_removing': self._suggest_removals(cards, prefer_type='spell')
                })
        
        # Suggest small spell if missing
        if metrics['light_spell_count'] == 0:
            light_spell_suggestions = ['Zap', 'Log', 'Arrows', 'Snowball']
            available_suggestions = [card for card in light_spell_suggestions if card not in card_names]
            
            if available_suggestions:
                suggestions.append({
                    'type': 'Add Light Spell',
                    'reason': 'Need quick response to swarm troops and charging units',
                    'consider_adding': available_suggestions[:3],
                    'consider_removing': self._suggest_removals(cards, prefer_type='spell')
                })
        
        # Suggest win condition if missing
        if metrics['win_condition_count'] < self.thresholds['min_win_conditions']:
            win_con_suggestions = ['Hog Rider', 'Giant', 'Royal Giant', 'Balloon', 'Miner', 'Graveyard']
            available_suggestions = [card for card in win_con_suggestions if card not in card_names]
            
            if available_suggestions:
                suggestions.append({
                    'type': 'Add Win Condition',
                    'reason': 'Deck needs a reliable way to deal tower damage',
                    'consider_adding': available_suggestions[:3],
                    'consider_removing': self._suggest_removals(cards, exclude_types=['win_condition'])
                })
        
        # Suggest reducing elixir if too heavy
        if metrics['avg_elixir'] > self.thresholds['high_elixir']:
            heavy_cards = sorted([card for card in cards], key=lambda c: c.elixir_cost, reverse=True)
            suggestions.append({
                'type': 'Reduce Elixir Cost',
                'reason': 'Deck cycles too slowly',
                'consider_replacing': heavy_cards[0].name if heavy_cards else None,
                'with_cheaper_alternatives': ['Knight', 'Skeletons', 'Ice Spirit', 'Ice Golem']
            })
        
        return suggestions
    
    def _suggest_removals(self, cards: List[Card], exclude_types: List[str] = None, prefer_type: str = None) -> List[str]:
        """Suggest cards that could be removed"""
        exclude_types = exclude_types or []
        candidates = []
        
        for card in cards:
            # Skip cards with important roles
            if 'air_targeting' in exclude_types and card.is_air_targeting:
                continue
            if 'splash' in exclude_types and card.is_splash_damage:
                continue
            if 'win_condition' in exclude_types and card.is_win_condition:
                continue
            
            # Prefer removing spells if specified
            if prefer_type == 'spell' and card.is_spell:
                candidates.insert(0, card.name)
            else:
                candidates.append(card.name)
        
        return candidates[:2]
    
    def _calculate_overall_rating(self, strengths: List[Dict], weaknesses: List[Dict]) -> str:
        """Calculate overall deck rating"""
        strength_score = len(strengths)
        weakness_score = sum(
            3 if w.get('severity') == 'high' else 2 if w.get('severity') == 'medium' else 1
            for w in weaknesses
        )
        
        net_score = strength_score - (weakness_score / 2)
        
        if net_score >= 4:
            return 'excellent'
        elif net_score >= 2:
            return 'good'
        elif net_score >= 0:
            return 'average'
        else:
            return 'poor'


# Singleton instance
_analyzer = None


def get_analyzer() -> DeckAnalyzer:
    """Get or create the analyzer singleton"""
    global _analyzer
    if _analyzer is None:
        _analyzer = DeckAnalyzer()
    return _analyzer