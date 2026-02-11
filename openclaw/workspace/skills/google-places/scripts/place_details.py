#!/usr/bin/env python3
"""Get detailed information about a specific place with OAuth.

Usage:
    python3 place_details.py PLACE_ID
    python3 place_details.py PLACE_ID --format json
"""
import argparse
import json
from google_auth import get_credentials
import requests

def get_place_details(place_id):
    """Get detailed information about a place using OAuth."""
    creds = get_credentials()
    
    url = f'https://places.googleapis.com/v1/places/{place_id}'
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {creds.token}',
        'X-Goog-FieldMask': 'displayName,formattedAddress,location,rating,userRatingCount,priceLevel,types,currentOpeningHours,websiteUri,internationalPhoneNumber,businessStatus,googleMapsUri'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    except Exception as e:
        print(f"Error getting place details: {e}")
        if hasattr(e, 'response'):
            print(f"Response: {e.response.text}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Get place details from Google Places API')
    parser.add_argument('place_id', help='Place ID')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    args = parser.parse_args()
    
    place = get_place_details(args.place_id)
    
    if not place:
        exit(1)
    
    if args.format == 'json':
        print(json.dumps(place, indent=2))
    else:
        name = place.get('displayName', {}).get('text', 'Unnamed')
        address = place.get('formattedAddress', 'N/A')
        rating = place.get('rating', 'N/A')
        rating_count = place.get('userRatingCount', 0)
        price_level = place.get('priceLevel', 'N/A')
        phone = place.get('internationalPhoneNumber', 'N/A')
        website = place.get('websiteUri', 'N/A')
        maps_uri = place.get('googleMapsUri', 'N/A')
        status = place.get('businessStatus', 'N/A')
        types = ', '.join(place.get('types', []))
        
        # Opening hours
        opening = place.get('currentOpeningHours', {})
        open_now = opening.get('openNow', 'Unknown')
        weekday_text = opening.get('weekdayDescriptions', [])
        
        print(f"Name: {name}")
        print(f"Address: {address}")
        print(f"Rating: {rating} ({rating_count} reviews)")
        print(f"Price Level: {price_level}")
        print(f"Phone: {phone}")
        print(f"Website: {website}")
        print(f"Google Maps: {maps_uri}")
        print(f"Status: {status}")
        print(f"Open Now: {open_now}")
        print(f"Types: {types}")
        
        if weekday_text:
            print("\nOpening Hours:")
            for day in weekday_text:
                print(f"  {day}")

if __name__ == '__main__':
    main()
