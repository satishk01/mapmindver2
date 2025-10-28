#!/usr/bin/env node
/**
 * Script to update the API IP address across all configuration files
 * Usage: node update-ip.js <new-ip-address>
 * Example: node update-ip.js 54.123.45.67
 */

const fs = require('fs');
const path = require('path');

const newIp = process.argv[2];

if (!newIp) {
  console.error('❌ Please provide a new IP address');
  console.log('Usage: node update-ip.js <new-ip-address>');
  console.log('Example: node update-ip.js 54.123.45.67');
  process.exit(1);
}

// Validate IP format (basic validation)
const ipRegex = /^(\d{1,3}\.){3}\d{1,3}$/;
if (!ipRegex.test(newIp)) {
  console.error('❌ Invalid IP address format');
  process.exit(1);
}

const newApiUrl = `http://${newIp}:8000`;

console.log(`🔄 Updating API URL to: ${newApiUrl}`);

// Files to update
const filesToUpdate = [
  {
    path: '.env',
    pattern: /VITE_API_URL=http:\/\/[\d.]+:8000/,
    replacement: `VITE_API_URL=${newApiUrl}`
  },
  {
    path: '.env.production',
    pattern: /VITE_API_URL=http:\/\/[\d.]+:8000/,
    replacement: `VITE_API_URL=${newApiUrl}`
  },
  {
    path: 'config.json',
    isJson: true
  }
];

// Update text files
filesToUpdate.forEach(file => {
  if (file.isJson) {
    // Handle JSON file
    try {
      const configPath = path.join(__dirname, file.path);
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      
      // Update all environment URLs
      Object.keys(config).forEach(env => {
        if (config[env].apiUrl && env !== 'notes') {
          if (env === 'development') {
            // Keep localhost for development
            config[env].apiUrl = 'http://localhost:8000';
          } else {
            config[env].apiUrl = newApiUrl;
          }
        }
      });
      
      fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
      console.log(`✅ Updated ${file.path}`);
    } catch (error) {
      console.error(`❌ Error updating ${file.path}:`, error.message);
    }
  } else {
    // Handle text files
    try {
      const filePath = path.join(__dirname, file.path);
      
      if (fs.existsSync(filePath)) {
        let content = fs.readFileSync(filePath, 'utf8');
        content = content.replace(file.pattern, file.replacement);
        fs.writeFileSync(filePath, content);
        console.log(`✅ Updated ${file.path}`);
      } else {
        console.log(`⚠️  File not found: ${file.path}`);
      }
    } catch (error) {
      console.error(`❌ Error updating ${file.path}:`, error.message);
    }
  }
});

console.log('');
console.log('🎉 IP address update complete!');
console.log('📝 Next steps:');
console.log('   1. Restart the frontend development server: npm run dev');
console.log('   2. Verify the new API URL in the browser console');
console.log('   3. Test flow creation functionality');