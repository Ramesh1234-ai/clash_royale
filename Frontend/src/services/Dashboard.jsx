import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { playerAPI } from './api';
import './dashboard.css';

function Dashboard() {
  const { playerTag } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [player, setPlayer] = useState(null);
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    if (!playerTag) return;

    const fetchData = async () => {
      setLoading(true);
      setError('');

      try {
        // Try to fetch analyzed deck first
        const data = await playerAPI.analyzeDeck(playerTag, true);
        if (data && data.data) {
          console.log('Analysis data:', data.data);
          setPlayer(data.data.player || null);
          setAnalysis(data.data.analysis || null);
        } else {
          console.log('No analysis data returned');
          setError('No analysis data returned');
        }
      } catch (err) {
        // If analyze fails, try to fetch player basic info
        try {
          const p = await playerAPI.getPlayer(playerTag, true);
          console.log('Player data:', p.data);
          setPlayer(p.data || null);
          setAnalysis(null);
        } catch (err2) {
          console.error('Error fetching player:', err2);
          setError(err.message || 'Failed to load player data');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [playerTag]);

  if (loading) return <div className="dashboard-loading">Loading...</div>;
  if (error) return (
    <div className="dashboard-error">
      <p>{error}</p>
      <button onClick={() => navigate('/')}>Back</button>
    </div>
  );

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h2>{player ? player.name : `#${playerTag}`}'s Dashboard</h2>
        <button onClick={() => navigate('/')}>Search another</button>
      </header>

      <section className="player-summary">
        {player ? (
          <>
            <p><strong>Tag:</strong> {player.player_tag}</p>
            <p><strong>Name:</strong> {player.name}</p>
            <p><strong>Trophies:</strong> {player.trophies}</p>
            <p><strong>Best Trophies:</strong> {player.best_trophies}</p>
            <p><strong>Experience Level:</strong> {player.exp_level}</p>
            <p><strong>Wins:</strong> {player.wins}</p>
            <p><strong>Arena Name:</strong> {player.arena_name}</p>
            <p><strong>Losses:</strong> {player.losses}</p>
            <p><strong>3-Crown Wins:</strong> {player.three_crown_wins}</p>
            {player.clan_name && <p><strong>Clan:</strong> {player.clan_name}</p>}
          </>
        ) : (
          <p>No player info available</p>
        )}
      </section>

      <section className="deck-section">
        <h3>Current Deck</h3>
        {player && player.currentDeck && player.currentDeck.length > 0 ? (
          <div className="deck-cards-grid">
            {player.currentDeck.map((card, index) => (
              <div key={index} className={`deck-card rarity-${card.rarity}`}>
                {/* Card Image */}
                <div className="card-image-container">
                  {card.iconUrls && card.iconUrls.medium ? (
                    <img 
                      src={card.iconUrls.medium} 
                      alt={card.name}
                      className="card-image"
                      onError={(e) => {
                        e.target.style.display = 'none';
                      }}
                    />
                  ) : (
                    <div className="card-image-placeholder">No Image</div>
                  )}
                </div>
                
                {/* Card Info */}
                <div className="card-info">
                  <h4>{card.name}</h4>
                  <div className="card-stats">
                    <span className="stat">💎 Lvl: {card.level}</span>
                    <span className="stat">⚡ {card.elixirCost}</span>
                  </div>
                  <div className="card-details">
                    <span className={`rarity-badge ${card.rarity}`}>{card.rarity}</span>
                    {card.starLevel && <span className="star-level">⭐ {card.starLevel}</span>}
                  </div>
                  {card.count !== undefined && (
                    <p className="card-count">Count: {card.count}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="deck-unavailable">
            <p>📌 Deck data not currently available for this player</p>
            <p style={{fontSize: '0.9rem', color: '#666', marginTop: '10px'}}>
              <strong>Why?</strong> The Clash Royale API key needs to be configured with your server's IP address(es) to fetch deck information. 
              <br/><br/>
              <strong>To fix this:</strong>
              <ol style={{marginLeft: '20px', marginTop: '8px'}}>
                <li>Go to <a href="https://developer.clashroyale.com/" target="_blank" rel="noopener noreferrer">developer.clashroyale.com</a></li>
                <li>Click on your API key</li>
                <li>Add your server IP to the "Allowed IPs" list</li>
                <li>Or create a new key without IP restrictions (for testing)</li>
              </ol>
              <strong style={{marginTop: '15px', display: 'block'}}>Alternative:</strong> View the player's card collection below instead
            </p>
          </div>
        )}
      </section>

      {/* Alternative: Card Collection Section */}
      {player && !player.currentDeck && player.cards && player.cards.length > 0 && (
        <section className="card-collection-section">
          <h3>📚 All Cards Collection</h3>
          <p style={{color: 'var(--text-secondary)', marginBottom: '15px'}}>
            Since the current deck isn't available, here's the player's complete card collection:
          </p>
          <div className="deck-cards-grid">
            {player.cards.map((card, index) => (
              <div key={index} className={`deck-card rarity-${card.rarity}`}>
                {/* Card Image */}
                <div className="card-image-container">
                  {card.iconUrls && card.iconUrls.medium ? (
                    <img 
                      src={card.iconUrls.medium} 
                      alt={card.name}
                      className="card-image"
                      onError={(e) => {
                        e.target.style.display = 'none';
                      }}
                    />
                  ) : (
                    <div className="card-image-placeholder">No Image</div>
                  )}
                </div>
                
                {/* Card Info */}
                <div className="card-info">
                  <h4>{card.name}</h4>
                  <div className="card-stats">
                    <span className="stat">💎 Lvl: {card.level}</span>
                    <span className="stat">⚡ {card.elixirCost}</span>
                  </div>
                  <div className="card-details">
                    <span className={`rarity-badge ${card.rarity}`}>{card.rarity}</span>
                    {card.starLevel && <span className="star-level">⭐ {card.starLevel}</span>}
                  </div>
                  {card.count !== undefined && (
                    <p className="card-count">Count: {card.count}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Deck Statistics Section */}
      {player && (player.challengeCardsWon || player.tournamentCardsWon || player.clanCardsCollected) && (
        <section className="deck-stats-section">
          <h3>Card Statistics</h3>
          <div className="stats-grid">
            {player.challengeCardsWon !== undefined && (
              <div className="stat-item">
                <div className="stat-value">🎖️ {player.challengeCardsWon}</div>
                <div className="stat-label">Challenge Cards Won</div>
              </div>
            )}
            {player.tournamentCardsWon !== undefined && (
              <div className="stat-item">
                <div className="stat-value">🏆 {player.tournamentCardsWon}</div>
                <div className="stat-label">Tournament Cards Won</div>
              </div>
            )}
            {player.clanCardsCollected !== undefined && (
              <div className="stat-item">
                <div className="stat-value">👥 {player.clanCardsCollected}</div>
                <div className="stat-label">Clan Cards Collected</div>
              </div>
            )}
          </div>
        </section>
      )}

      {/* Support Cards Section */}
      {player && player.currentDeckSupportCards && player.currentDeckSupportCards.length > 0 && (
        <section className="support-cards-section">
          <h3>Support Cards</h3>
          <div className="support-cards-grid">
            {player.currentDeckSupportCards.map((card, index) => (
              <div key={index} className={`support-card rarity-${card.rarity}`}>
                <div className="card-image-container small">
                  {card.iconUrls && card.iconUrls.medium ? (
                    <img 
                      src={card.iconUrls.medium} 
                      alt={card.name}
                      className="card-image"
                      onError={(e) => {
                        e.target.style.display = 'none';
                      }}
                    />
                  ) : (
                    <div className="card-image-placeholder">No Image</div>
                  )}
                </div>
                <div className="card-info">
                  <h5>{card.name}</h5>
                  <div className="card-stats">
                    <span className="stat">💎 Lvl: {card.level}</span>
                  </div>
                  <span className={`rarity-badge ${card.rarity}`}>{card.rarity}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Favorite Card Section */}
      {player && player.currentFavouriteCard && (
        <section className="favorite-card-section">
          <h3>Favorite Card</h3>
          <div className="favorite-card-container">
            <div className={`favorite-card rarity-${player.currentFavouriteCard.rarity}`}>
              <div className="card-image-container large">
                {player.currentFavouriteCard.iconUrls && player.currentFavouriteCard.iconUrls.medium ? (
                  <img 
                    src={player.currentFavouriteCard.iconUrls.medium} 
                    alt={player.currentFavouriteCard.name}
                    className="card-image"
                    onError={(e) => {
                      e.target.style.display = 'none';
                    }}
                  />
                ) : (
                  <div className="card-image-placeholder">No Image</div>
                )}
              </div>
              <div className="favorite-card-info">
                <h2>{player.currentFavouriteCard.name}</h2>
                <div className="card-details-large">
                  <span className={`rarity-badge ${player.currentFavouriteCard.rarity}`}>
                    {player.currentFavouriteCard.rarity}
                  </span>
                  <span className="elixir-cost">⚡ {player.currentFavouriteCard.elixirCost} Elixir</span>
                </div>
                {player.currentFavouriteCard.maxLevel && (
                  <p><strong>Max Level:</strong> {player.currentFavouriteCard.maxLevel}</p>
                )}
              </div>
            </div>
          </div>
        </section>
      )}

      <section className="analysis-section">
        {analysis ? (
          <>
            <h3>Deck Analysis</h3>
            <p><strong>Overall rating:</strong> {analysis.overall_rating}</p>
            <p><strong>Average Elixir:</strong> {analysis.avg_elixir}</p>
            <div className="analysis-list">
              <div>
                <h4>Strengths</h4>
                <ul>{(analysis.strengths || []).map((s, i) => <li key={i}>{s}</li>)}</ul>
              </div>
              <div>
                <h4>Weaknesses</h4>
                <ul>{(analysis.weaknesses || []).map((w, i) => <li key={i}>{w}</li>)}</ul>
              </div>
              <div>
                <h4>Suggestions</h4>
                <ul>{(analysis.suggestions || []).map((sug, i) => <li key={i}>{sug}</li>)}</ul>
              </div>
            </div>
          </>
        ) : (
          <p>No analysis available for this player yet.</p>
        )}
      </section>
    </div>
  );
}

export default Dashboard;