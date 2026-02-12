/**
 * API Service
 * Handles all communication with the backend API
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

/**
 * Generic fetch wrapper with error handling
 */
async function fetchAPI(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const defaultHeaders = {
    'Content-Type': 'application/json',
  };
  
  // Add JWT token if available
  const token = localStorage.getItem('access_token');
  if (token) {
    defaultHeaders['Authorization'] = `Bearer ${token}`;
  }
  
  const config = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };
  
  try {
    const response = await fetch(url, config);
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || `HTTP error! status: ${response.status}`);
    }
    
    return data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

/**
 * Player API endpoints
 */
export const playerAPI = {
  /**
   * Get player information
   * @param {string} playerTag - Player tag (with or without #)
   * @param {boolean} refresh - Force refresh from API
   */
  getPlayer: async (playerTag, refresh = false) => {
    const tag = playerTag.startsWith('#') ? playerTag.substring(1) : playerTag;
    const queryParam = refresh ? '?refresh=true' : '';
    return fetchAPI(`/players/${tag}${queryParam}`);
  },
  
  /**
   * Analyze player's deck
   * @param {string} playerTag - Player tag (with or without #)
   */
  analyzeDeck: async (playerTag) => {
    const tag = playerTag.startsWith('#') ? playerTag.substring(1) : playerTag;
    return fetchAPI(`/players/${tag}/analyze`);
  },
  
  /**
   * Get list of players
   * @param {number} limit - Number of players per page
   * @param {number} offset - Offset for pagination
   */
  listPlayers: async (limit = 20, offset = 0) => {
    return fetchAPI(`/players?limit=${limit}&offset=${offset}`);
  },
  
  /**
   * Search players
   * @param {string} query - Search query (player tag or name)
   */
  searchPlayers: async (query) => {
    return fetchAPI(`/players/search?q=${encodeURIComponent(query)}`);
  },
};

/**
 * Cards API endpoints
 */
export const cardsAPI = {
  /**
   * Get all cards
   * @param {string} type - Filter by card type (troop, spell, building)
   * @param {string} rarity - Filter by rarity
   */
  getAllCards: async (type = null, rarity = null) => {
    let queryParams = [];
    if (type) queryParams.push(`type=${type}`);
    if (rarity) queryParams.push(`rarity=${rarity}`);
    const queryString = queryParams.length > 0 ? `?${queryParams.join('&')}` : '';
    return fetchAPI(`/cards${queryString}`);
  },
  
  /**
   * Get specific card
   * @param {number} cardId - Card database ID
   */
  getCard: async (cardId) => {
    return fetchAPI(`/cards/${cardId}`);
  },
  
  /**
   * Get card usage statistics
   */
  getStatistics: async () => {
    return fetchAPI('/cards/statistics');
  },
  
  /**
   * Sync cards from API
   */
  syncCards: async () => {
    return fetchAPI('/cards/sync', { method: 'POST' });
  },
};

/**
 * Roast API endpoints
 */
export const roastAPI = {
  /**
   * Generate roast for a player
   * @param {string} playerTag - Player tag (with or without #)
   * @param {string} intensity - Roast intensity: 'fun', 'savage', or 'nuclear'
   */
  generateRoast: async (playerTag, intensity = 'fun') => {
    const tag = playerTag.startsWith('#') ? playerTag.substring(1) : playerTag;
    return fetchAPI(`/roast/${tag}?intensity=${intensity}`);
  },
};

/**
 * Auth API endpoints
 */
export const authAPI = {
  /**
   * Register new user
   * @param {string} username
   * @param {string} email
   * @param {string} password
   */
  register: async (username, email, password) => {
    return fetchAPI('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password }),
    });
  },
  
  /**
   * Login user
   * @param {string} username
   * @param {string} password
   */
  login: async (username, password) => {
    const response = await fetchAPI('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    
    // Store tokens
    if (response.access_token) {
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('refresh_token', response.refresh_token);
    }
    
    return response;
  },
  
  /**
   * Logout user
   */
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
  
  /**
   * Get current user
   */
  getCurrentUser: async () => {
    return fetchAPI('/auth/me');
  },
  
  /**
   * Refresh access token
   */
  refreshToken: async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }
    
    const response = await fetchAPI('/auth/refresh', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${refreshToken}`,
      },
    });
    
    if (response.access_token) {
      localStorage.setItem('access_token', response.access_token);
    }
    
    return response;
  },
};

/**
 * Utility function to check if user is authenticated
 */
export const isAuthenticated = () => {
  return !!localStorage.getItem('access_token');
};

export default {
  playerAPI,
  cardsAPI,
  authAPI,
  roastAPI,
  isAuthenticated,
};