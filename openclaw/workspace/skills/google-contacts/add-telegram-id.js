#!/usr/bin/env node
/**
 * Add or update Telegram ID for a contact
 * Usage:
 *   node add-telegram-id.js --name "Agnes" --telegram-id "2072813705"
 *   node add-telegram-id.js --email "hi@simonschenker.com" --telegram-id "7273735518"
 */

const api = require('./google-contacts-api');

const args = process.argv.slice(2);
const name = args[args.indexOf('--name') + 1];
const email = args[args.indexOf('--email') + 1];
const telegramId = args[args.indexOf('--telegram-id') + 1];

if (!telegramId) {
  console.error('Error: --telegram-id required');
  process.exit(1);
}

if (!name && !email) {
  console.error('Error: --name or --email required');
  process.exit(1);
}

async function main() {
  let contact;

  if (name) {
    contact = await api.findContactByName(name);
    if (!contact) {
      console.error(`Contact not found: ${name}`);
      process.exit(1);
    }
  } else if (email) {
    contact = await api.findContactByEmail(email);
    if (!contact) {
      console.error(`Contact not found: ${email}`);
      process.exit(1);
    }
  }

  const displayName = contact.names?.[0]?.displayName || 'Unknown';
  console.log(`Found contact: ${displayName}`);

  // Fetch full contact details with etag
  const fullContact = await api.getContact(contact.resourceName);

  // Check if Telegram ID already exists
  const existingUserDefined = fullContact.userDefined || [];
  const telegramField = existingUserDefined.find(u => u.key === 'Telegram ID');

  let updatedUserDefined;
  if (telegramField) {
    // Update existing
    updatedUserDefined = existingUserDefined.map(u => 
      u.key === 'Telegram ID' ? { key: 'Telegram ID', value: telegramId } : u
    );
    console.log(`Updating Telegram ID: ${telegramField.value} → ${telegramId}`);
  } else {
    // Add new
    updatedUserDefined = [...existingUserDefined, { key: 'Telegram ID', value: telegramId }];
    console.log(`Adding Telegram ID: ${telegramId}`);
  }

  // Update contact (include etag)
  await api.updateContact(
    fullContact.resourceName,
    { 
      etag: fullContact.etag,
      userDefined: updatedUserDefined 
    },
    ['userDefined']
  );

  console.log('✅ Telegram ID saved to Google Contacts');
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
