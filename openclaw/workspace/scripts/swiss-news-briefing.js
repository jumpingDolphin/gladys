#!/usr/bin/env node
/**
 * Swiss News Briefing - Echo der Zeit + RTS Le 12h30
 * Runs daily at 8:30 AM CET
 * Sends formatted briefing to Telegram
 */

const https = require('https');
const { execSync } = require('child_process');

// Fetch URL content
function fetchURL(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

// Parse RSS XML (simple extraction)
function parseRSS(xml) {
  const items = [];
  const itemMatches = xml.match(/<item>[\s\S]*?<\/item>/g) || [];
  
  for (const item of itemMatches.slice(0, 1)) { // Only first item
    const title = (item.match(/<itunes:title>(.*?)<\/itunes:title>/) || 
                  item.match(/<title>(.*?)<\/title>/))?.[1] || '';
    const link = item.match(/<link>(.*?)<\/link>/)?.[1] || '';
    const summaryMatch = item.match(/<itunes:summary><!\[CDATA\[([\s\S]*?)\]\]><\/itunes:summary>/);
    const description = summaryMatch ? summaryMatch[1] : 
                       (item.match(/<description><!\[CDATA\[([\s\S]*?)\]\]><\/description>/) || 
                        item.match(/<description>(.*?)<\/description>/))?.[1] || '';
    const guid = item.match(/<guid[^>]*>(.*?)<\/guid>/)?.[1] || '';
    
    items.push({ title, link, description, guid });
  }
  
  return items;
}

// Extract segments from Echo der Zeit episode page
async function getEchoDerZeitSegments(url) {
  const html = await fetchURL(url);
  
  // Extract "Alle Themen" section
  const alleThemenMatch = html.match(/Alle Themen:[\s\S]*?<\/div>/);
  if (!alleThemenMatch) return [];
  
  const themen = alleThemenMatch[0];
  const segments = [];
  
  // Match lines like "(01:28) Topic title"
  const matches = themen.matchAll(/\((\d{2}:\d{2})\)\s*([^<\n]+)/g);
  
  for (const match of matches) {
    const [, timestamp, title] = match;
    if (title.trim() && !title.includes('Intro')) {
      segments.push({ timestamp, title: title.trim() });
    }
  }
  
  return segments;
}

// Main function
async function main() {
  try {
    console.log('📰 Fetching Swiss news briefing...\n');
    
    // Fetch Echo der Zeit
    const edzXML = await fetchURL('https://www.srf.ch/feed/podcast/sd/28549e81-c453-4671-92ad-cb28796d06a8.xml');
    const edzEpisodes = parseRSS(edzXML);
    
    if (edzEpisodes.length === 0) {
      throw new Error('No Echo der Zeit episodes found');
    }
    
    const edzEpisode = edzEpisodes[0];
    console.log(`🇩🇪 Echo der Zeit: ${edzEpisode.title}`);
    
    // Parse segments from description (they're in the RSS description!)
    const segments = [];
    const alleThemenMatch = edzEpisode.description.match(/Alle Themen:\s*([\s\S]+)$/);
    
    if (alleThemenMatch) {
      const themenText = alleThemenMatch[1];
      const lines = themenText.split(/\r?\n/);
      
      for (const line of lines) {
        const match = line.match(/\((\d{2}:\d{2})\)\s*(.+)/);
        if (match) {
          const [, timestamp, title] = match;
          if (!title.includes('Intro') && !title.includes('Nachrichtenübersicht')) {
            segments.push({ timestamp, title: title.trim() });
          }
        }
      }
    }
    
    console.log(`  Found ${segments.length} segments`);
    segments.slice(0, 5).forEach(s => console.log(`   - ${s.timestamp}: ${s.title}`));
    
    // Fetch Le 12h30
    const l12XML = await fetchURL('https://www.rts.ch/la-1ere/programmes/le-12h30/podcast/?flux=rss/podcast');
    const l12Episodes = parseRSS(l12XML);
    
    if (l12Episodes.length === 0) {
      throw new Error('No Le 12h30 episodes found');
    }
    
    const l12Episode = l12Episodes[0];
    console.log(`\n🇫🇷 Le 12h30: ${l12Episode.title}`);
    console.log(`   ${l12Episode.link}`);
    
    // Build Echo der Zeit link from guid
    const edzLink = `https://www.srf.ch/audio/echo-der-zeit?id=${edzEpisode.guid}`;
    
    // Build Telegram message
    let message = `📰 *Swiss News Briefing*\n\n`;
    message += `🇩🇪 *Echo der Zeit*\n`;
    
    segments.slice(0, 6).forEach((seg, i) => {
      message += `${i + 1}\\. \\[${seg.timestamp}\\] ${seg.title.replace(/[_*[\]()~`>#+=|{}.!-]/g, '\\$&')}\n`;
    });
    
    message += `\n🔗 [Zur Sendung](${edzLink})\n\n`;
    message += `🇫🇷 *Le 12h30*\n`;
    message += `${l12Episode.title.replace(/[_*[\]()~`>#+=|{}.!-]/g, '\\$&')}\n`;
    message += `🔗 [Écouter](${l12Episode.link})`;
    
    // Send via OpenClaw message tool (would need to be called from the agent)
    console.log('\n📤 Message prepared:\n');
    console.log(message);
    
    // Output JSON for the agent to consume
    const output = {
      edzEpisode,
      segments: segments.slice(0, 6),
      l12Episode
    };
    
    console.log('\n' + JSON.stringify(output, null, 2));
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

main();
