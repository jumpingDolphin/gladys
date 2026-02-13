#!/usr/bin/env node
/**
 * Lookup contact for allowlist management
 * Usage: node lookup-for-allowlist.js "Michael"
 */

const api = require('./google-contacts-api');

const searchName = process.argv[2];

if (!searchName) {
  console.error('Usage: node lookup-for-allowlist.js "Name"');
  process.exit(1);
}

async function main() {
  const contact = await api.findContactByName(searchName);
  
  if (!contact) {
    console.log(JSON.stringify({ found: false, name: searchName }));
    process.exit(0);
  }

  const fullContact = await api.getContact(contact.resourceName);
  
  const name = fullContact.names?.[0]?.displayName || 'Unknown';
  const email = fullContact.emailAddresses?.[0]?.value || 'No email';
  const telegramId = fullContact.userDefined?.find(u => u.key === 'Telegram ID')?.value;
  
  if (!telegramId) {
    console.log(JSON.stringify({ 
      found: true, 
      name, 
      email, 
      hasTelegramId: false 
    }));
    process.exit(0);
  }

  console.log(JSON.stringify({ 
    found: true, 
    name, 
    email, 
    telegramId,
    hasTelegramId: true
  }));
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
