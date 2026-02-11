#!/usr/bin/env python3
"""Search for places using Google Places API (New) with OAuth.

Usage:
    python3 search_places.py "restaurants in Lausanne"
    python3 search_places.py "cafes near me" --lat 46.5197 --lng 6.6323
    
Examples:
    # Text search
    python3 search_places.py "pizza restaurants in Geneva"
    
    # Nearby search with location
    python3 search_places.py "coffee shop" --lat 46.5197 --lng 6.6323 --radius 1000
    
    # Filter by open now
    python3 search_places.py "restaurants" --lat 46.5197 --lng 6.6323 --open-now
    
    # JSON output
    python3 search_places.py "museums" --lat 46.5197 --lng 6.6323 --format json
"""
import argparse
import json
from google_auth import get_credentials
import requests

BASE_URL = 'https://places.googleapis.com/v1/places:searchText'

def search_places(query, lat=None, lng=None, radius=None, open_now=False, max_results=10):
    """Search for places using Places API (New) with OAuth."""
    creds = get_credentials()
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {creds.token}',
        'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.location,places.rating,places.userRatingCount,places.priceLevel,places.types,places.currentOpeningHours,places.id'
    }
    
    body = {
        'textQuery': query,
        'maxResultCount': max_results
    }
    
    # Add location bias if provided
    if lat and lng:
        body['locationBias'] = {
            'circle': {
                'center': {'latitude': lat, 'longitude': lng},
                'radius': radius if radius else 5000  # default 5km
            }
        }
    
    # Add open now filter
    if open_now:
        body['openNow'] = True
    
    try:
        response = requests.post(BASE_URL, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        return data.get('places', [])
    
    except Exception as e:
        print(f"Error searching places: {e}")
        if hasattr(e, 'response'):
            print(f"Response: {e.response.text}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Search for places using Google Places API')
    parser.add_argument('query', help='Search query (e.g., "restaurants in Lausanne")')
    parser.add_argument('--lat', type=float, help='Latitude for location bias')
    parser.add_argument('--lng', type=float, help='Longitude for location bias')
    parser.add_argument('--radius', type=int, help='Search radius in meters (default: 5000)')
    parser.add_argument('--open-now', action='store_true', help='Only show open places')
    parser.add_argument('--max-results', type=int, default=10, help='Maximum results (1-20)')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    args = parser.parse_args()
    
    places = search_places(
        args.query,
        lat=args.lat,
        lng=args.lng,
        radius=args.radius,
        open_now=args.open_now,
        max_results=args.max_results
    )
    
    if places is None:
        exit(1)
    
    if not places:
        print("No places found.")
        exit(0)
    
    if args.format == 'json':
        print(json.dumps(places, indent=2))
    else:
        for i, place in enumerate(places, 1):
            name = place.get('displayName', {}).get('text', 'Unnamed')
            address = place.get('formattedAddress', 'N/A')
            rating = place.get('rating', 'N/A')
            rating_count = place.get('userRatingCount', 0)
            price_level = place.get('priceLevel', 'N/A')
            types = ', '.join(place.get('types', [])[:3])
            
            print(f"\n{i}. {name}")
            print(f"   Address: {address}")
            print(f"   Rating: {rating} ({rating_count} reviews)")
            print(f"   Price: {price_level}")
            print(f"   Types: {types}")
            print(f"   ID: {place.get('id', 'N/A')}")
        
        print(f"\nTotal: {len(places)} places")

if __name__ == '__main__':
    main()
