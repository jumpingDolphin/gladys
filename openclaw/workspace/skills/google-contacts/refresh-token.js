#!/usr/bin/env node
/**
 * Refresh Google OAuth2 token
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const querystring = require('querystring');

const TOKEN_PATH = path.join(process.env.HOME, 'gladys', 'openclaw', 'workspace', 'google_token.json');

function refreshToken(refreshToken, clientId, clientSecret) {
  return new Promise((resolve, reject) => {
    const postData = querystring.stringify({
      refresh_token: refreshToken,
      client_id: clientId,
      client_secret: clientSecret,
      grant_type: 'refresh_token'
    });

    const options = {
      hostname: 'oauth2.googleapis.com',
      port: 443,
      path: '/token',
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode === 200) {
          resolve(JSON.parse(data));
        } else {
          reject(new Error(`Token refresh failed: ${data}`));
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

async function main() {
  const tokenData = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
  
  console.log('Refreshing token...');
  const response = await refreshToken(
    tokenData.refresh_token,
    tokenData.client_id,
    tokenData.client_secret
  );

  // Calculate expiry time
  const expiryDate = new Date(Date.now() + (response.expires_in * 1000));
  
  // Update token file
  tokenData.token = response.access_token;
  tokenData.access_token = response.access_token;
  tokenData.expiry = expiryDate.toISOString();
  
  fs.writeFileSync(TOKEN_PATH, JSON.stringify(tokenData, null, 2));
  
  console.log('✅ Token refreshed successfully');
  console.log(`New expiry: ${expiryDate.toISOString()}`);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
