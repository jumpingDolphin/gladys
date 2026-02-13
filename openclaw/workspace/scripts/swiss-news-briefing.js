#!/usr/bin/env node
/**
 * Swiss News Briefing - Echo der Zeit + RTS Top News
 * Runs daily at 8:30 AM CET
 * Fetches yesterday's Echo der Zeit (since it airs in the evening)
 * and today's top RTS news articles
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
    
    // Get yesterday's date (since Echo der Zeit airs in the evening)
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const yesterdayStr = yesterday.toISOString().split('T')[0]; // YYYY-MM-DD
    
    console.log(`Looking for Echo der Zeit from ${yesterdayStr}\n`);
    
    // Fetch Echo der Zeit RSS (fetches multiple episodes for parsing)
    const edzXML = await fetchURL('https://www.srf.ch/feed/podcast/sd/28549e81-c453-4671-92ad-cb28796d06a8.xml');
    
    // Parse all items (we need to check multiple in case latest is a placeholder)
    const allItems = [];
    const itemMatches = edzXML.match(/<item>[\s\S]*?<\/item>/g) || [];
    
    for (const item of itemMatches.slice(0, 5)) { // Check first 5 episodes
      const title = (item.match(/<itunes:title>(.*?)<\/itunes:title>/) || 
                    item.match(/<title>(.*?)<\/title>/))?.[1] || '';
      const link = item.match(/<link>(.*?)<\/link>/)?.[1] || '';
      const summaryMatch = item.match(/<itunes:summary><!\[CDATA\[([\s\S]*?)\]\]><\/itunes:summary>/);
      const description = summaryMatch ? summaryMatch[1] : 
                         (item.match(/<description><!\[CDATA\[([\s\S]*?)\]\]><\/description>/) || 
                          item.match(/<description>(.*?)<\/description>/))?.[1] || '';
      const guid = item.match(/<guid[^>]*>(.*?)<\/guid>/)?.[1] || '';
      const pubDate = item.match(/<pubDate>(.*?)<\/pubDate>/)?.[1] || '';
      
      allItems.push({ title, link, description, guid, pubDate });
    }
    
    if (allItems.length === 0) {
      throw new Error('No Echo der Zeit episodes found');
    }
    
    // Find the first episode with actual content (segments)
    let edzEpisode = null;
    let segments = [];
    
    for (const episode of allItems) {
      // Try to parse segments from description
      const alleThemenMatch = episode.description.match(/Alle Themen:\s*([\s\S]+)$/);
      
      if (alleThemenMatch) {
        const themenText = alleThemenMatch[1];
        const lines = themenText.split(/\r?\n/);
        const tempSegments = [];
        
        for (const line of lines) {
          const match = line.match(/\((\d{2}:\d{2})\)\s*(.+)/);
          if (match) {
            const [, timestamp, title] = match;
            if (!title.includes('Intro') && !title.includes('Nachrichtenübersicht')) {
              tempSegments.push({ timestamp, title: title.trim() });
            }
          }
        }
        
        // If we found segments, use this episode
        if (tempSegments.length > 0) {
          edzEpisode = episode;
          segments = tempSegments;
          break;
        }
      }
    }
    
    if (!edzEpisode || segments.length === 0) {
      throw new Error('No Echo der Zeit episodes with segments found');
    }
    
    console.log(`🇩🇪 Echo der Zeit: ${edzEpisode.title}`);
    console.log(`   Published: ${edzEpisode.pubDate}`);
    
    console.log(`  Found ${segments.length} segments`);
    segments.slice(0, 5).forEach(s => console.log(`   - ${s.timestamp}: ${s.title}`));
    
    // Fetch RTS top news articles from RSS
    console.log('\n🇫🇷 Fetching RTS news...');
    const rtsXML = await fetchURL('https://www.rts.ch/info/?format=rss/news');
    
    // Parse RSS feed
    const articles = [];
    const rtsItemMatches = rtsXML.match(/<item>[\s\S]*?<\/item>/g) || [];
    
    for (const item of rtsItemMatches.slice(0, 5)) {
      const titleMatch = item.match(/<title>(.*?)<\/title>/);
      const linkMatch = item.match(/<link>(.*?)<\/link>/);
      const categoryMatch = item.match(/<category>(.*?)<\/category>/);
      
      if (titleMatch && linkMatch) {
        const title = titleMatch[1].replace(/<!\[CDATA\[|\]\]>/g, '').trim();
        const link = linkMatch[1];
        const category = categoryMatch ? categoryMatch[1] : null;
        
        articles.push({ title, link, category });
      }
    }
    
    console.log(`  Found ${articles.length} articles`);
    articles.forEach(a => console.log(`   - [${a.category || 'Info'}] ${a.title}`));
    
    // Build Echo der Zeit link from guid
    const edzLink = `https://www.srf.ch/audio/echo-der-zeit?id=${edzEpisode.guid}`;
    
    // Build Telegram message (use <link> to suppress preview)
    let message = `📰 *Swiss News Briefing*\n\n`;
    message += `🇩🇪 *Echo der Zeit*\n`;
    
    segments.slice(0, 6).forEach((seg, i) => {
      message += `• \\[${seg.timestamp}\\] ${seg.title.replace(/[_*[\]()~`>#+=|{}.!-]/g, '\\$&')}\n`;
    });
    
    message += `\n<${edzLink}>\n\n`;
    message += `🇫🇷 *RTS Info*\n`;
    
    articles.slice(0, 5).forEach(article => {
      const category = article.category ? `[${article.category}] ` : '';
      message += `• ${category}${article.title.replace(/[_*[\]()~`>#+=|{}.!-]/g, '\\$&')}\n`;
      message += `  <${article.link}>\n`;
    });
    
    // Send via OpenClaw message tool (would need to be called from the agent)
    console.log('\n📤 Message prepared:\n');
    console.log(message);
    
    // Output JSON for the agent to consume
    const output = {
      edzEpisode,
      segments: segments.slice(0, 6),
      rtsArticles: articles.slice(0, 5)
    };
    
    console.log('\n' + JSON.stringify(output, null, 2));
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

main();
