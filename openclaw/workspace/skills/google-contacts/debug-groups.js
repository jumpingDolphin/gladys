#!/usr/bin/env node
const api = require('./google-contacts-api');

async function main() {
  const contact = await api.findContactByName('Gladys Groups');
  
  if (!contact) {
    console.log('Gladys Groups contact not found');
    return;
  }
  
  console.log('Resource:', contact.resourceName);
  
  const fullContact = await api.getContact(contact.resourceName);
  console.log('\nFull contact:');
  console.log(JSON.stringify(fullContact, null, 2));
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
