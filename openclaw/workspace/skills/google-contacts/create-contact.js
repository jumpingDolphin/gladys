#!/usr/bin/env node
/**
 * Create a new contact
 * Usage: node create-contact.js --name "Agnes" --email "agnes.alvesdesouza@gmail.com" --telegram-id "2072813705"
 */

const api = require('./google-contacts-api');

const args = process.argv.slice(2);
const getName = () => {
  const idx = args.indexOf('--name');
  return idx >= 0 ? args[idx + 1] : null;
};
const getEmail = () => {
  const idx = args.indexOf('--email');
  return idx >= 0 ? args[idx + 1] : null;
};
const getTelegramId = () => {
  const idx = args.indexOf('--telegram-id');
  return idx >= 0 ? args[idx + 1] : null;
};

const name = getName();
const email = getEmail();
const telegramId = getTelegramId();

if (!name) {
  console.error('Error: --name required');
  process.exit(1);
}

async function main() {
  const nameParts = name.split(' ');
  const givenName = nameParts[0];
  const familyName = nameParts.slice(1).join(' ') || undefined;

  const contactData = {
    names: [{ givenName, familyName }]
  };

  if (email) {
    contactData.emailAddresses = [{ value: email }];
  }

  if (telegramId) {
    contactData.userDefined = [{ key: 'Telegram ID', value: telegramId }];
  }

  console.log(`Creating contact: ${name}`);
  if (email) console.log(`  Email: ${email}`);
  if (telegramId) console.log(`  Telegram ID: ${telegramId}`);

  await api.createContact(contactData);

  console.log('✅ Contact created successfully');
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
