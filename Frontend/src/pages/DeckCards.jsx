import React from 'react';
import './DeckCards.css';

function DeckCards({ cards, avgElixir }) {
  // Sort cards by position
  const sortedCards = [...cards].sort((a, b) => a.position - b.position);

  const getElixirColor = (cost) => {
    if (cost <= 2) return 'elixir-low';
    if (cost <= 4) return 'elixir-medium';
    return 'elixir-high';
  };

  const getRarityColor = (rarity) => {
    const colors = {
      common: '#A8A8A8',
      rare: '#FF8C00',
      epic: '#9B59B6',
      legendary: '#FFD700',
      champion: '#FF69B4'
    };
    return colors[rarity] || '#A8A8A8';
  };

  return (
    <div className="deck-cards-container">
      <div className="deck-summary">
        <div className="avg-elixir">
          <span className="elixir-label">Average Elixir:</span>
          <span className={`elixir-value ${getElixirColor(avgElixir)}`}>
            {avgElixir}
          </span>
        </div>
      </div>

      <div className="cards-grid">
        {sortedCards.map((deckCard, index) => {
          const card = deckCard.card;
          return (
            <div key={index} className="card-item">
              <div className="card-image-wrapper">
                {card.icon_url ? (
                  <img 
                    src={card.icon_url} 
                    alt={card.name}
                    className="card-image"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'flex';
                    }}
                  />
                ) : null}
                <div 
                  className="card-placeholder"
                  style={{ display: card.icon_url ? 'none' : 'flex' }}
                >
                  <span className="card-initial">{card.name.charAt(0)}</span>
                </div>
                
                <div className="card-level">Lv {deckCard.card_level}</div>
                <div 
                  className="card-rarity-badge"
                  style={{ backgroundColor: getRarityColor(card.rarity) }}
                >
                  {card.rarity}
                </div>
              </div>

              <div className="card-info">
                <h3 className="card-name">{card.name}</h3>
                <div className="card-stats">
                  <span className={`card-elixir ${getElixirColor(card.elixir_cost)}`}>
                    ⚡ {card.elixir_cost}
                  </span>
                  <span className="card-type">{card.card_type}</span>
                </div>
                
                <div className="card-attributes">
                  {card.is_win_condition && (
                    <span className="attribute win-condition" title="Win Condition">🎯</span>
                  )}
                  {card.is_air_targeting && (
                    <span className="attribute air-targeting" title="Air Targeting">✈️</span>
                  )}
                  {card.is_splash_damage && (
                    <span className="attribute splash-damage" title="Splash Damage">💥</span>
                  )}
                  {card.is_tank && (
                    <span className="attribute tank" title="Tank">🛡️</span>
                  )}
                  {card.is_spell && (
                    <span className="attribute spell" title="Spell">✨</span>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default DeckCards;