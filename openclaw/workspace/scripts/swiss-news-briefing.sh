#!/bin/bash
# Swiss News Briefing - Echo der Zeit + RTS Le 12h30
# Runs daily at 8:30 AM CET

set -e

WORKSPACE="/home/simon/gladys/openclaw/workspace"
TMP_DIR="$WORKSPACE/tmp/briefing"
mkdir -p "$TMP_DIR"

# Fetch Echo der Zeit RSS (German)
echo "Fetching Echo der Zeit..."
curl -s "https://www.srf.ch/feed/podcast/sd/28549e81-c453-4671-92ad-cb28796d06a8.xml" > "$TMP_DIR/echo-der-zeit.xml"

# Fetch Le 12h30 RSS (French)
echo "Fetching Le 12h30..."
curl -s "https://www.rts.ch/la-1ere/programmes/le-12h30/podcast/?flux=rss/podcast" > "$TMP_DIR/le-12h30.xml"

# Parse latest Echo der Zeit episode
EDZ_TITLE=$(grep -m1 "<title>" "$TMP_DIR/echo-der-zeit.xml" | sed -e 's/<[^>]*>//g' -e 's/^[[:space:]]*//' | head -2 | tail -1)
EDZ_URL=$(grep -m1 "<link>" "$TMP_DIR/echo-der-zeit.xml" | sed -e 's/<[^>]*>//g' -e 's/^[[:space:]]*//' | grep "https" | head -1)
EDZ_DESCRIPTION=$(grep -A1 "<description>" "$TMP_DIR/echo-der-zeit.xml" | tail -1 | sed -e 's/<!\[CDATA\[//g' -e 's/\]\]>//g' -e 's/<[^>]*>//g')

# Parse latest Le 12h30 episode  
L12_TITLE=$(grep -m1 "<title>" "$TMP_DIR/le-12h30.xml" | sed -e 's/<[^>]*>//g' -e 's/^[[:space:]]*//' | head -2 | tail -1)
L12_URL=$(grep -m1 "<link>" "$TMP_DIR/le-12h30.xml" | sed -e 's/<[^>]*>//g' -e 's/^[[:space:]]*//' | grep "https" | head -1)

echo "✅ Echo der Zeit: $EDZ_TITLE"
echo "✅ Le 12h30: $L12_TITLE"

# Now we need to parse individual segments from the episode pages
# This would require scraping the HTML pages
# For now, output what we have
echo ""
echo "Echo der Zeit URL: $EDZ_URL"
echo "Le 12h30 URL: $L12_URL"
