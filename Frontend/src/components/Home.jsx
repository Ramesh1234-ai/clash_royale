import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { playerAPI } from '../services/api';
import './Home.css';

function Home() {
  const [playerTag, setPlayerTag] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!playerTag.trim()) {
      setError('Please enter a player tag');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Normalize tag (remove # if present, add it back)
      let normalizedTag = playerTag.trim().toUpperCase();
      if (normalizedTag.startsWith('#')) {
        normalizedTag = normalizedTag.substring(1);
      }

      // Fetch player data first to validate
      await playerAPI.getPlayer(normalizedTag, true);

      // Navigate to dashboard
      navigate(`/dashboard/${normalizedTag}`);
    } catch (err) {
      setError(err.message || 'Failed to fetch player data. Please check the player tag and try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (tag) => {
    setPlayerTag(tag);
  };

  return (
    <div className="home-container">
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            Clash Royale<br />
            <span className="highlight">Deck Analyzer</span>
          </h1>
          <p className="hero-subtitle">
            Get instant analysis of your deck's strengths, weaknesses, and strategic improvements
          </p>

          <form onSubmit={handleSubmit} className="search-form">
            <div className="input-group">
              <span className="input-prefix">#</span>
              <input
                type="text"
                value={playerTag}
                onChange={(e) => setPlayerTag(e.target.value)}
                placeholder="Enter your player tag (e.g., 2PP)"
                className="player-tag-input"
                disabled={loading}
              />
            </div>
            <button 
              type="submit" 
              className="analyze-button"
              disabled={loading}
            >
              
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Analyzing...
                </>
              ) : (
                'Analyze Deck'
              )}
            </button>
          </form>

          {error && (
            <div className="error-message">
              <svg className="error-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {error}
            </div>
          )}

          <div className="example-tags">
            <span className="example-label">Try example:</span>
            <button 
              onClick={() => handleExampleClick('2PP')}
              className="example-tag"
            >
              #2PP
            </button>
            <button 
              onClick={() => handleExampleClick('8YC9VY8C')}
              className="example-tag"
            >
              #8YC9VY8C
            </button>
          </div>
        </div>
      </div>

      <div className="features-section">
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3>Instant Analysis</h3>
            <p>Get real-time deck analysis with detailed metrics and insights</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <h3>Strategic Insights</h3>
            <p>Identify strengths, weaknesses, and optimal card replacements</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Visual Charts</h3>
            <p>Interactive charts showing elixir distribution and card types</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">💡</div>
            <h3>Smart Suggestions</h3>
            <p>AI-powered recommendations to improve your deck composition</p>
          </div>
        </div>
      </div>

      <div className="how-it-works">
        <h2>How It Works</h2>
        <div className="steps-grid">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Enter Player Tag</h3>
            <p>Input your Clash Royale player tag</p>
          </div>
          <div className="step">
            <div className="step-number">2</div>
            <h3>Fetch Data</h3>
            <p>We retrieve your current deck from the game</p>
          </div>
          <div className="step">
            <div className="step-number">3</div>
            <h3>Analyze Deck</h3>
            <p>Our algorithm analyzes your deck composition</p>
          </div>
          <div className="step">
            <div className="step-number">4</div>
            <h3>Get Results</h3>
            <p>Receive detailed insights and recommendations</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;