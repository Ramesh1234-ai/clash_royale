# TuxHuz

A full-stack application for analyzing Clash Royale decks and tracking player statistics.

## Project Overview

TuxHuz is a web application that provides players with insights into their Clash Royale decks and gameplay statistics. It integrates with the Clash Royale API to fetch player data and offers comprehensive deck analysis tools.

## Features

- **Player Authentication**: Secure user authentication system
- **Deck Analysis**: Analyze card combinations and deck performance
- **Player Statistics**: Track player progress and game metrics
- **Card Database**: Browse and analyze Clash Royale cards
- **Dashboard**: Visualize player data with interactive charts

## Technology Stack

### Backend
- **Python** with Flask web framework
- **SQLite** (via Flask-SQLAlchemy) for data persistence
- **Clash Royale API** integration
- **CORS** enabled for frontend communication

### Frontend
- **React** (via Vite)
- **JavaScript ES6+**
- **CSS3** for styling
- **Responsive design** for desktop and mobile

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8+
- Node.js 14+
- npm or yarn

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- macOS/Linux:
```bash
source venv/bin/activate
```

4. Install requirements:
```bash
pip install -r requirements.txt
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd Frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Start the Backend Server

1. From the backend directory (with virtual environment activated):
```bash
python app.py
```

The backend will run on `http://localhost:5000` by default.

### Start the Frontend Development Server

1. From the frontend directory:
```bash
npm run dev
```

The frontend will typically run on `http://localhost:5173` (Vite default).

## Project Structure

```
TuxHuz/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── models.py              # Database models
│   ├── init_db.py             # Database initialization
│   ├── requirements.txt        # Python dependencies
│   ├── routes/                # API endpoints
│   │   ├── auth.py           # Authentication routes
│   │   ├── cards.py          # Cards routes
│   │   └── players.py        # Players routes
│   └── services/              # Business logic
│       ├── clash_royale.py    # Clash Royale API integration
│       ├── deck_analyzer.py   # Deck analysis logic
│       └── player_service.py  # Player data service
│
└── Frontend/
    ├── package.json           # Node dependencies
    ├── vite.config.js         # Vite configuration
    ├── index.html             # HTML entry point
    └── src/
        ├── main.jsx           # React entry point
        ├── App.jsx            # Main App component
        ├── components/        # Reusable components
        │   ├── Home.jsx
        │   └── Navbar.jsx
        ├── pages/             # Page components
        │   └── DeckCards.jsx
        ├── services/          # Frontend services
        │   ├── api.js         # API client
        │   ├── Dashboard.jsx
        │   └── ChartsSection.jsx
        └── assets/            # Static assets
```

## API Endpoints

The backend provides the following API endpoints:

- **Authentication**: `/api/auth/*` - User login and registration
- **Players**: `/api/players/*` - Player statistics and data
- **Cards**: `/api/cards/*` - Card information and analysis
- **Deck Analysis**: `/api/analyze/*` - Deck analysis endpoints

## Configuration

Modify `backend/config.py` to adjust:
- Database settings
- API keys and endpoints
- Flask configuration options

## Development

### Running Tests
```bash
# Backend tests (if available)
python -m pytest

# Frontend tests (if available)
npm run test
```

### Building for Production

**Frontend Build:**
```bash
cd Frontend
npm run build
```

The build output will be in the `dist/` directory.

## Troubleshooting

### Port Already in Use
If port 5000 or 5173 is already in use, you can specify a different port:
```bash
# Backend
python app.py --port 5001

# Frontend
npm run dev -- --port 5174
```

### CORS Issues
Ensure the backend is configured to accept requests from your frontend URL. Check `config.py` for CORS settings.

## Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit your changes (`git commit -m 'Add amazing feature'`)
3. Push to the branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request
## Support

For issues or questions, please open an issue on the project repository.
---

**Last Updated:** February 2026
# clash_royale
