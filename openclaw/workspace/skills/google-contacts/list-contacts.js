#!/usr/bin/env node
/**
 * List all contacts with Telegram IDs
 */

const api = require('./google-contacts-api');

async function main() {
  const contacts = await api.listContacts();
  
  const withTelegram = contacts.filter(c => 
    c.userDefined && c.userDefined.some(u => u.key === 'Telegram ID')
  );

  if (withTelegram.length === 0) {
    console.log('No contacts with Telegram IDs found.');
    return;
  }

  console.log(`Found ${withTelegram.length} contact(s) with Telegram IDs:\n`);

  withTelegram.forEach(c => {
    const name = c.names?.[0]?.displayName || 'Unknown';
    const email = c.emailAddresses?.[0]?.value || 'No email';
    const telegramId = c.userDefined.find(u => u.key === 'Telegram ID')?.value;
    
    console.log(`- ${name}`);
    console.log(`  Email: ${email}`);
    console.log(`  Telegram ID: ${telegramId}\n`);
  });
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
