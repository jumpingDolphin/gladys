---
name: google-places
description: Search for places (restaurants, cafes, shops, etc.) using Google Places API. Use when the user asks to find nearby places, search for locations, get restaurant recommendations, or find businesses by type or name.
---

# Google Places Search

Find places, businesses, and points of interest using Google Places API (New).

## Setup

Uses OAuth credentials from workspace (same as other Google services):
- `google_credentials.json` - OAuth client config
- `google_token.json` - Access/refresh tokens

Requires requests library:
```bash
pip install requests
```

Scripts automatically refresh tokens when expired.

## Available Operations

### 1. Text Search

Search for places using natural language queries.

```bash
cd google-places/scripts

# Search by query
python3 search_places.py "Italian restaurants in Lausanne"

# Search with location bias
python3 search_places.py "coffee shops" --lat 46.5197 --lng 6.6323 --radius 1000

# Only open places
python3 search_places.py "restaurants" --lat 46.5197 --lng 6.6323 --open-now

# JSON output
python3 search_places.py "museums" --lat 46.5197 --lng 6.6323 --format json
```

**Location coordinates (Swiss cities):**
- Lausanne: `46.5197, 6.6323`
- Geneva: `46.2044, 6.1432`
- Zurich: `47.3769, 8.5417`
- Lucerne: `47.0502, 8.3093`

### 2. Nearby Search (by Type)

Find specific types of places nearby.

```bash
cd google-places/scripts

# Find restaurants within 1km
python3 nearby_search.py restaurant --lat 46.5197 --lng 6.6323 --radius 1000

# Find cafes
python3 nearby_search.py cafe --lat 46.5197 --lng 6.6323

# Find gyms, open now
python3 nearby_search.py gym --lat 46.5197 --lng 6.6323 --open-now
```

**Common place types:**
- `restaurant`, `cafe`, `bar`, `bakery`
- `grocery_or_supermarket`, `pharmacy`, `hospital`
- `gym`, `park`, `museum`, `library`
- `shopping_mall`, `clothing_store`, `bookstore`
- `gas_station`, `parking`, `atm`, `bank`
- `hotel`, `tourist_attraction`

[Full list of types](https://developers.google.com/maps/documentation/places/web-service/place-types)

### 3. Place Details

Get detailed information about a specific place (phone, website, hours, etc.).

```bash
cd google-places/scripts

# Get details by place ID
python3 place_details.py PLACE_ID

# JSON output
python3 place_details.py PLACE_ID --format json
```

**Get place ID** from search results.

## Workflow Patterns

### Find Nearby Restaurant

```bash
cd google-places/scripts

# Search nearby
python3 nearby_search.py restaurant --lat 46.5197 --lng 6.6323 --radius 500 --open-now

# Get details for a specific place
python3 place_details.py PLACE_ID
```

### Search for Specific Place

```bash
cd google-places/scripts

# Text search
python3 search_places.py "La Grappe d'Or Lausanne"

# Get full details
python3 place_details.py PLACE_ID
```

### Find Coffee Shop

```bash
cd google-places/scripts

# Nearby cafes
python3 nearby_search.py cafe --lat 46.5197 --lng 6.6323 --radius 300 --open-now
```

## Common Tasks

### Recommend Restaurants

```bash
cd google-places/scripts

# Find highly rated restaurants
python3 search_places.py "restaurants" --lat 46.5197 --lng 6.6323 --radius 2000

# Filter results manually for rating > 4.0
```

### Find Emergency Services

```bash
cd google-places/scripts

# Find pharmacy
python3 nearby_search.py pharmacy --lat 46.5197 --lng 6.6323 --radius 5000 --open-now

# Find hospital
python3 nearby_search.py hospital --lat 46.5197 --lng 6.6323
```

### Plan Outing

```bash
cd google-places/scripts

# Find museums
python3 nearby_search.py museum --lat 46.2044 --lng 6.1432 --radius 3000

# Get details (hours, website)
python3 place_details.py PLACE_ID
```

## Getting Coordinates

**If user says "near me":**
- Use node location services (if available)
- Ask for city/address and use approximate coordinates
- Default to Lausanne (46.5197, 6.6323) for Simon

**Swiss cities reference:**
```
Lausanne:  46.5197, 6.6323
Geneva:    46.2044, 6.1432
Zurich:    47.3769, 8.5417
Bern:      46.9480, 7.4474
Lucerne:   47.0502, 8.3093
Basel:     47.5596, 7.5886
```

## Output Format

**Text search results include:**
- Name, address
- Rating (0-5) and review count
- Price level (FREE, INEXPENSIVE, MODERATE, EXPENSIVE, VERY_EXPENSIVE)
- Place types
- Place ID (for getting details)

**Place details include:**
- All search info, plus:
- Phone number
- Website
- Google Maps link
- Opening hours (by day)
- Current open/closed status

## API Limits

- Free tier: $200 credit/month
- Text Search: $17 per 1,000 requests
- Nearby Search: $17 per 1,000 requests
- Place Details: $17 per 1,000 requests

Monitor usage in Google Cloud Console.

## Script Dependencies

```bash
pip install requests
```

## Notes

- **Authentication:** Uses OAuth (same as Gmail, Drive, Calendar, etc.)
- **Account:** Gladys's personal Google account (not Simon's)
- **Coordinates:** Latitude/longitude required for location-based searches
- **Radius:** In meters (1000m = 1km)
- **Open now:** Filters to currently open places
- **Place ID:** Permanent identifier for each place (use for details)
