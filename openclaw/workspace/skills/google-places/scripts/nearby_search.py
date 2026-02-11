#!/usr/bin/env python3
"""Search for nearby places by type with OAuth.

Usage:
    python3 nearby_search.py PLACE_TYPE --lat LAT --lng LNG [--radius METERS]
    
Examples:
    # Find restaurants within 1km
    python3 nearby_search.py restaurant --lat 46.5197 --lng 6.6323 --radius 1000
    
    # Find cafes nearby
    python3 nearby_search.py cafe --lat 46.5197 --lng 6.6323
    
    # Find gyms, open now
    python3 nearby_search.py gym --lat 46.5197 --lng 6.6323 --open-now
    
Common types: restaurant, cafe, bar, gym, pharmacy, hospital, park, museum, 
              shopping_mall, grocery_or_supermarket, gas_station, atm, bank
"""
import argparse
import json
from google_auth import get_credentials
import requests

BASE_URL = 'https://places.googleapis.com/v1/places:searchNearby'

def nearby_search(place_type, lat, lng, radius=1000, open_now=False, max_results=10):
    """Search for nearby places by type using OAuth."""
    creds = get_credentials()
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {creds.token}',
        'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.location,places.rating,places.userRatingCount,places.priceLevel,places.types,places.currentOpeningHours,places.id'
    }
    
    body = {
        'includedTypes': [place_type],
        'maxResultCount': max_results,
        'locationRestriction': {
            'circle': {
                'center': {'latitude': lat, 'longitude': lng},
                'radius': radius
            }
        }
    }
    
    if open_now:
        body['openNow'] = True
    
    try:
        response = requests.post(BASE_URL, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        return data.get('places', [])
    
    except Exception as e:
        print(f"Error searching nearby places: {e}")
        if hasattr(e, 'response'):
            print(f"Response: {e.response.text}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Search nearby places by type')
    parser.add_argument('place_type', help='Place type (e.g., restaurant, cafe, gym)')
    parser.add_argument('--lat', type=float, required=True, help='Latitude')
    parser.add_argument('--lng', type=float, required=True, help='Longitude')
    parser.add_argument('--radius', type=int, default=1000, help='Search radius in meters (default: 1000)')
    parser.add_argument('--open-now', action='store_true', help='Only show open places')
    parser.add_argument('--max-results', type=int, default=10, help='Maximum results (1-20)')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    args = parser.parse_args()
    
    places = nearby_search(
        args.place_type,
        args.lat,
        args.lng,
        radius=args.radius,
        open_now=args.open_now,
        max_results=args.max_results
    )
    
    if places is None:
        exit(1)
    
    if not places:
        print(f"No {args.place_type} places found nearby.")
        exit(0)
    
    if args.format == 'json':
        print(json.dumps(places, indent=2))
    else:
        print(f"Found {len(places)} {args.place_type} places within {args.radius}m:\n")
        for i, place in enumerate(places, 1):
            name = place.get('displayName', {}).get('text', 'Unnamed')
            address = place.get('formattedAddress', 'N/A')
            rating = place.get('rating', 'N/A')
            rating_count = place.get('userRatingCount', 0)
            
            print(f"{i}. {name}")
            print(f"   Address: {address}")
            print(f"   Rating: {rating} ({rating_count} reviews)")
            print(f"   ID: {place.get('id', 'N/A')}\n")

if __name__ == '__main__':
    main()
