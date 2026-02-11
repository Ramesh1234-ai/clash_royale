#!/usr/bin/env python
"""Debug script to see raw API response"""
from app import create_app
from services.clash_royale import get_api_service

app = create_app()
with app.app_context():
    try:
        api_service = get_api_service()
        response = api_service.get_player('#2GQY8L9PR')
        
        print("Full API Response Keys:")
        for key in response.keys():
            print(f"  - {key}")
        
        print("\nLooking for deck-related fields:")
        if 'currentDeck' in response:
            print(f"  currentDeck: {response['currentDeck']}")
        else:
            print("  currentDeck: NOT FOUND")
        
        # Check if there are other variations
        for key in response.keys():
            if 'deck' in key.lower() or 'card' in key.lower():
                print(f"  {key}: {response[key]}")
                
    except Exception as e:
        print(f"Error: {e}")
