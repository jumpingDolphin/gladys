#!/usr/bin/env node
const api = require('./google-contacts-api');

const searchTerm = process.argv[2];

if (!searchTerm) {
  console.error('Usage: node search-contact.js <name or email>');
  process.exit(1);
}

async function main() {
  const contacts = await api.listContacts();
  
  const matches = contacts.filter(c => {
    const name = c.names?.[0]?.displayName || '';
    const email = c.emailAddresses?.[0]?.value || '';
    const search = searchTerm.toLowerCase();
    
    return name.toLowerCase().includes(search) || 
           email.toLowerCase().includes(search);
  });

  if (matches.length === 0) {
    console.log(`No contacts found matching: ${searchTerm}`);
    return;
  }

  console.log(`Found ${matches.length} contact(s):\n`);
  matches.forEach(c => {
    const name = c.names?.[0]?.displayName || 'No name';
    const email = c.emailAddresses?.[0]?.value || 'No email';
    console.log(`- ${name}`);
    console.log(`  Email: ${email}`);
    console.log(`  Resource: ${c.resourceName}\n`);
  });
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
