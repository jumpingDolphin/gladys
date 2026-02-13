#!/usr/bin/env node
/**
 * Manage Telegram groups via special "Gladys Groups" contact
 * Usage:
 *   node manage-groups.js list
 *   node manage-groups.js add --name "Patates" --id "-5285631663"
 *   node manage-groups.js get --name "Patates"
 */

const api = require('./google-contacts-api');

const GROUPS_CONTACT_NAME = 'Gladys Groups';

async function getOrCreateGroupsContact() {
  let contact = await api.findContactByName(GROUPS_CONTACT_NAME);
  
  if (!contact) {
    console.log(`Creating "${GROUPS_CONTACT_NAME}" contact...`);
    contact = await api.createContact({
      names: [{ givenName: 'Gladys', familyName: 'Groups' }],
      biographies: [{
        value: JSON.stringify({ groups: {} }),
        contentType: 'TEXT_PLAIN'
      }]
    });
  }
  
  return contact;
}

async function getGroups() {
  const contact = await getOrCreateGroupsContact();
  const fullContact = await api.getContact(contact.resourceName);
  const bio = fullContact.biographies?.[0]?.value;
  
  if (!bio) return {};
  
  try {
    const data = JSON.parse(bio);
    return data.groups || {};
  } catch (e) {
    console.error('Failed to parse groups data:', e.message);
    console.error('Bio content:', bio);
    return {};
  }
}

async function saveGroups(groups) {
  const contact = await getOrCreateGroupsContact();
  const fullContact = await api.getContact(contact.resourceName);
  const data = { groups };
  
  await api.updateContact(
    fullContact.resourceName,
    {
      etag: fullContact.etag,
      biographies: [{
        value: JSON.stringify(data, null, 2),
        contentType: 'TEXT_PLAIN'
      }]
    },
    ['biographies']
  );
}

async function listGroups() {
  const groups = await getGroups();
  const entries = Object.entries(groups);
  
  if (entries.length === 0) {
    console.log('No groups registered.');
    return;
  }
  
  console.log(`Registered groups (${entries.length}):\n`);
  entries.forEach(([key, group]) => {
    console.log(`- ${group.name} (${key})`);
    console.log(`  ID: ${group.id}\n`);
  });
}

async function addGroup(name, id) {
  const groups = await getGroups();
  const key = name.toLowerCase().replace(/\s+/g, '-');
  
  groups[key] = { id, name };
  await saveGroups(groups);
  
  console.log(`✅ Group "${name}" added (ID: ${id})`);
}

async function getGroup(name) {
  const groups = await getGroups();
  const key = name.toLowerCase().replace(/\s+/g, '-');
  const group = groups[key];
  
  if (!group) {
    console.log(`Group not found: ${name}`);
    return;
  }
  
  console.log(`Name: ${group.name}`);
  console.log(`ID: ${group.id}`);
}

async function main() {
  const command = process.argv[2];
  
  if (command === 'list') {
    await listGroups();
  } else if (command === 'add') {
    const args = process.argv.slice(3);
    const name = args[args.indexOf('--name') + 1];
    const id = args[args.indexOf('--id') + 1];
    
    if (!name || !id) {
      console.error('Usage: node manage-groups.js add --name "Group Name" --id "-123456789"');
      process.exit(1);
    }
    
    await addGroup(name, id);
  } else if (command === 'get') {
    const args = process.argv.slice(3);
    const name = args[args.indexOf('--name') + 1];
    
    if (!name) {
      console.error('Usage: node manage-groups.js get --name "Group Name"');
      process.exit(1);
    }
    
    await getGroup(name);
  } else {
    console.log('Usage:');
    console.log('  node manage-groups.js list');
    console.log('  node manage-groups.js add --name "Group Name" --id "-123456789"');
    console.log('  node manage-groups.js get --name "Group Name"');
    process.exit(1);
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
