#!/usr/bin/env node
/**
 * Google Contacts API helper
 * Uses OAuth2 credentials from google_token.json
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const CREDENTIALS_PATH = path.join(process.env.HOME, 'gladys', 'openclaw', 'workspace', 'google_credentials.json');
const TOKEN_PATH = path.join(process.env.HOME, 'gladys', 'openclaw', 'workspace', 'google_token.json');

function loadToken() {
  if (!fs.existsSync(TOKEN_PATH)) {
    throw new Error(`Token file not found: ${TOKEN_PATH}`);
  }
  return JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
}

function apiRequest(method, path, body = null) {
  return new Promise((resolve, reject) => {
    const token = loadToken();
    const accessToken = token.access_token || token.token;

    const options = {
      hostname: 'people.googleapis.com',
      port: 443,
      path: path,
      method: method,
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            resolve(JSON.parse(data));
          } catch (e) {
            resolve(data);
          }
        } else {
          reject(new Error(`API Error ${res.statusCode}: ${data}`));
        }
      });
    });

    req.on('error', reject);

    if (body) {
      req.write(JSON.stringify(body));
    }

    req.end();
  });
}

async function listContacts() {
  const response = await apiRequest('GET', '/v1/people/me/connections?personFields=names,emailAddresses,userDefined&pageSize=1000');
  return response.connections || [];
}

async function getContact(resourceName) {
  return await apiRequest('GET', `/v1/${resourceName}?personFields=names,emailAddresses,userDefined,biographies`);
}

async function createContact(contactData) {
  return await apiRequest('POST', '/v1/people:createContact', contactData);
}

async function updateContact(resourceName, contactData, updatePersonFields) {
  const fieldMask = updatePersonFields.join(',');
  return await apiRequest('PATCH', `/v1/${resourceName}:updateContact?updatePersonFields=${fieldMask}`, contactData);
}

async function findContactByName(name) {
  const contacts = await listContacts();
  return contacts.find(c => 
    c.names && c.names.some(n => 
      n.displayName && n.displayName.toLowerCase().includes(name.toLowerCase())
    )
  );
}

async function findContactByEmail(email) {
  const contacts = await listContacts();
  return contacts.find(c => 
    c.emailAddresses && c.emailAddresses.some(e => 
      e.value && e.value.toLowerCase() === email.toLowerCase()
    )
  );
}

async function findContactByTelegramId(telegramId) {
  const contacts = await listContacts();
  return contacts.find(c => 
    c.userDefined && c.userDefined.some(u => 
      u.key === 'Telegram ID' && u.value === telegramId
    )
  );
}

module.exports = {
  loadToken,
  apiRequest,
  listContacts,
  getContact,
  createContact,
  updateContact,
  findContactByName,
  findContactByEmail,
  findContactByTelegramId
};
