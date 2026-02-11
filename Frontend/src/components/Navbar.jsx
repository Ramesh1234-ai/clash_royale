import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <span className="logo-icon">⚔️</span>
          <span className="logo-text">CR Deck Analyzer</span>
        </Link>
        
        <div className="navbar-links">
          <Link to="/" className="nav-link">Home</Link>
          <a 
            href="https://developer.clashroyale.com/" 
            target="_blank" 
            rel="noopener noreferrer" 
            className="nav-link"
          >
            API Docs
          </a>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;