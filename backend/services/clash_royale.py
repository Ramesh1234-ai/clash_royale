"""
Clash Royale API Service
Handles all interactions with the Clash Royale official API
"""
import requests
from typing import Dict, List, Optional
from flask import current_app


class ClashRoyaleAPIError(Exception):
    """Custom exception for Clash Royale API errors"""
    pass


class ClashRoyaleAPIService:
    """Service for interacting with Clash Royale API"""
    
    def __init__(self, api_key: str = None, base_url: str = None, timeout: int = 10):
        """
        Initialize the API service
        
        Args:
            api_key: Clash Royale API key
            base_url: Base URL for the API
            timeout: Request timeout in seconds
        """
        self.api_key = api_key or current_app.config.get('CLASH_ROYALE_API_KEY')
        self.base_url = base_url or current_app.config.get('CLASH_ROYALE_API_BASE_URL')
        self.timeout = timeout or current_app.config.get('CLASH_ROYALE_API_TIMEOUT', 10)
        
        if not self.api_key:
            raise ValueError("Clash Royale API key is required")
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        }
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """
        Make a request to the Clash Royale API
        
        Args:
            endpoint: API endpoint (e.g., '/players/%23ABC123')
            params: Query parameters
            
        Returns:
            Dict: API response data
            
        Raises:
            ClashRoyaleAPIError: If API request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=self.timeout
            )
            
            # Check for API errors
            if response.status_code == 404:
                raise ClashRoyaleAPIError("Player not found")
            elif response.status_code == 403:
                raise ClashRoyaleAPIError("Invalid API key or access forbidden")
            elif response.status_code == 429:
                raise ClashRoyaleAPIError("API rate limit exceeded")
            elif response.status_code >= 500:
                raise ClashRoyaleAPIError("Clash Royale API server error")
            elif response.status_code != 200:
                raise ClashRoyaleAPIError(f"API request failed with status {response.status_code}")
            
            return response.json()
            
        except requests.exceptions.Timeout:
            raise ClashRoyaleAPIError("API request timed out")
        except requests.exceptions.ConnectionError:
            raise ClashRoyaleAPIError("Failed to connect to Clash Royale API")
        except requests.exceptions.RequestException as e:
            raise ClashRoyaleAPIError(f"API request failed: {str(e)}")
    
    @staticmethod
    def format_player_tag(tag: str) -> str:
        """
        Format player tag to be URL-safe
        
        Args:
            tag: Player tag (with or without #)
            
        Returns:
            str: URL-encoded player tag
        """
        # Remove # if present, add it back with URL encoding
        tag = tag.strip().upper()
        if tag.startswith('#'):
            tag = tag[1:]
        return f'%23{tag}'
    
    def get_player(self, player_tag: str) -> Dict:
        """
        Get player information
        
        Args:
            player_tag: Player tag (with or without #)
            
        Returns:
            Dict: Player data
            
        Raises:
            ClashRoyaleAPIError: If request fails
        """
        formatted_tag = self.format_player_tag(player_tag)
        endpoint = f'/players/{formatted_tag}'
        return self._make_request(endpoint)
    
    def get_player_battles(self, player_tag: str) -> List[Dict]:
        """
        Get player's recent battles
        
        Args:
            player_tag: Player tag (with or without #)
            
        Returns:
            List[Dict]: List of recent battles
            
        Raises:
            ClashRoyaleAPIError: If request fails
        """
        formatted_tag = self.format_player_tag(player_tag)
        endpoint = f'/players/{formatted_tag}/battlelog'
        return self._make_request(endpoint)
    
    def get_cards(self) -> List[Dict]:
        """
        Get all available cards
        
        Returns:
            List[Dict]: List of all cards
            
        Raises:
            ClashRoyaleAPIError: If request fails
        """
        endpoint = '/cards'
        response = self._make_request(endpoint)
        return response.get('items', [])
    
    def extract_current_deck(self, player_data: Dict) -> List[Dict]:
        """
        Extract current deck from player data
        
        Args:
            player_data: Player data from API
            
        Returns:
            List[Dict]: List of cards in current deck
        """
        return player_data.get('currentDeck', [])
    
    def parse_player_data(self, api_response: Dict) -> Dict:
        """
        Parse player data from API response into a clean format
        
        Args:
            api_response: Raw API response
            
        Returns:
            Dict: Parsed player data
        """
        arena = api_response.get('arena', {})
        clan = api_response.get('clan', {})
        
        # Extract current favorite card
        favorite_card = api_response.get('currentFavouriteCard', {})
        current_favourite_card = None
        if favorite_card:
            current_favourite_card = {
                'name': favorite_card.get('name', ''),
                'card_id': favorite_card.get('id'),
                'rarity': favorite_card.get('rarity', '').lower(),
                'elixirCost': favorite_card.get('elixirCost', 0),
                'maxLevel': favorite_card.get('maxLevel', 14),
                'iconUrls': {
                    'medium': favorite_card.get('iconUrls', {}).get('medium', '')
                }
            }
        
        return {
            'player_tag': api_response.get('tag', ''),
            'name': api_response.get('name', ''),
            'trophies': api_response.get('trophies', 0),
            'best_trophies': api_response.get('bestTrophies', 0),
            'wins': api_response.get('wins', 0),
            'losses': api_response.get('losses', 0),
            'battle_count': api_response.get('battleCount', 0),
            'three_crown_wins': api_response.get('threeCrownWins', 0),
            'arena_id': arena.get('id'),
            'arena_name': arena.get('name'),
            'clan_name': clan.get('name'),
            'clan_tag': clan.get('tag'),
            'exp_level': api_response.get('expLevel', 1),
            'current_deck': self.extract_current_deck(api_response),
            'current_favourite_card': current_favourite_card,
        }
    
    def parse_card_data(self, card_api_data: Dict) -> Dict:
        """
        Parse card data from API response
        
        Args:
            card_api_data: Raw card data from API
            
        Returns:
            Dict: Parsed card data
        """
        # Map card type from API names to standardized names
        card_type_map = {
            'Troop': 'troop',
            'Spell': 'spell',
            'Building': 'building',
        }
        
        # Map rarity from API names to standardized names
        rarity_map = {
            'Common': 'common',
            'Rare': 'rare',
            'Epic': 'epic',
            'Legendary': 'legendary',
            'Champion': 'champion',
        }
        
        # Get card type from API (type field)
        card_type_api = card_api_data.get('type', 'Troop')
        card_type = card_type_map.get(card_type_api, 'troop')
        
        # Get rarity from API
        rarity_api = card_api_data.get('rarity', 'Common')
        rarity = rarity_map.get(rarity_api, 'common')
        
        return {
            'card_id': card_api_data.get('id'),
            'name': card_api_data.get('name'),
            'max_level': card_api_data.get('maxLevel', 14),
            'icon_url': card_api_data.get('iconUrls', {}).get('medium', ''),
            'elixir_cost': card_api_data.get('elixirCost', 0),
            'rarity': rarity,
            'card_type': card_type,
        }


# Singleton instance
_api_service = None


def get_api_service() -> ClashRoyaleAPIService:
    """Get or create the API service singleton"""
    global _api_service
    if _api_service is None:
        _api_service = ClashRoyaleAPIService()
    return _api_service