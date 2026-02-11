import React, { useState } from 'react';
import './AnalysisSection.css';

function AnalysisSection({ analysis }) {
  const [activeTab, setActiveTab] = useState('strengths');

  const getSeverityColor = (severity) => {
    const colors = {
      high: '#ef4444',
      medium: '#f59e0b',
      low: '#10b981'
    };
    return colors[severity] || '#6b7280';
  };

  return (
    <div className="analysis-container">
      {/* Tabs */}
      <div className="analysis-tabs">
        <button
          className={`tab ${activeTab === 'strengths' ? 'active' : ''}`}
          onClick={() => setActiveTab('strengths')}
        >
          <span className="tab-icon">✓</span>
          Strengths ({analysis.strengths?.length || 0})
        </button>
        <button
          className={`tab ${activeTab === 'weaknesses' ? 'active' : ''}`}
          onClick={() => setActiveTab('weaknesses')}
        >
          <span className="tab-icon">⚠</span>
          Weaknesses ({analysis.weaknesses?.length || 0})
        </button>
        <button
          className={`tab ${activeTab === 'suggestions' ? 'active' : ''}`}
          onClick={() => setActiveTab('suggestions')}
        >
          <span className="tab-icon">💡</span>
          Suggestions ({analysis.suggestions?.length || 0})
        </button>
      </div>

      {/* Content */}
      <div className="analysis-content">
        {/* Strengths Tab */}
        {activeTab === 'strengths' && (
          <div className="tab-content">
            {analysis.strengths && analysis.strengths.length > 0 ? (
              <div className="items-list">
                {analysis.strengths.map((strength, index) => (
                  <div key={index} className="analysis-item strength-item">
                    <div className="item-header">
                      <span className="item-icon strength-icon">✓</span>
                      <div className="item-title-group">
                        <h3 className="item-title">{strength.title}</h3>
                        <span className="item-category">{strength.category}</span>
                      </div>
                    </div>
                    <p className="item-description">{strength.description}</p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="empty-state">
                <p>No significant strengths identified</p>
              </div>
            )}
          </div>
        )}

        {/* Weaknesses Tab */}
        {activeTab === 'weaknesses' && (
          <div className="tab-content">
            {analysis.weaknesses && analysis.weaknesses.length > 0 ? (
              <div className="items-list">
                {analysis.weaknesses.map((weakness, index) => (
                  <div key={index} className="analysis-item weakness-item">
                    <div className="item-header">
                      <span className="item-icon weakness-icon">⚠</span>
                      <div className="item-title-group">
                        <h3 className="item-title">{weakness.title}</h3>
                        <div className="item-meta">
                          <span className="item-category">{weakness.category}</span>
                          {weakness.severity && (
                            <span 
                              className="severity-badge"
                              style={{ backgroundColor: getSeverityColor(weakness.severity) }}
                            >
                              {weakness.severity}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                    <p className="item-description">{weakness.description}</p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="empty-state">
                <p>No weaknesses identified - excellent deck!</p>
              </div>
            )}
          </div>
        )}

        {/* Suggestions Tab */}
        {activeTab === 'suggestions' && (
          <div className="tab-content">
            {analysis.suggestions && analysis.suggestions.length > 0 ? (
              <div className="items-list">
                {analysis.suggestions.map((suggestion, index) => (
                  <div key={index} className="analysis-item suggestion-item">
                    <div className="item-header">
                      <span className="item-icon suggestion-icon">💡</span>
                      <h3 className="item-title">{suggestion.type}</h3>
                    </div>
                    <p className="item-description">{suggestion.reason}</p>
                    
                    <div className="suggestion-details">
                      {suggestion.consider_adding && (
                        <div className="suggestion-section">
                          <h4>Consider Adding:</h4>
                          <div className="card-suggestions">
                            {suggestion.consider_adding.map((card, idx) => (
                              <span key={idx} className="suggested-card add">
                                + {card}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                      
                      {suggestion.consider_removing && (
                        <div className="suggestion-section">
                          <h4>Consider Removing:</h4>
                          <div className="card-suggestions">
                            {suggestion.consider_removing.map((card, idx) => (
                              <span key={idx} className="suggested-card remove">
                                - {card}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                      
                      {suggestion.consider_replacing && (
                        <div className="suggestion-section">
                          <h4>Consider Replacing:</h4>
                          <span className="suggested-card remove">
                            {suggestion.consider_replacing}
                          </span>
                        </div>
                      )}
                      
                      {suggestion.with_cheaper_alternatives && (
                        <div className="suggestion-section">
                          <h4>With Cheaper Alternatives:</h4>
                          <div className="card-suggestions">
                            {suggestion.with_cheaper_alternatives.map((card, idx) => (
                              <span key={idx} className="suggested-card add">
                                {card}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="empty-state">
                <p>No suggestions needed - your deck looks great!</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default AnalysisSection;