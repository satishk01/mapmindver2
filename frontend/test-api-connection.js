#!/usr/bin/env node
/**
 * Simple script to test API connection to the backend
 * Usage: node test-api-connection.js
 */

import https from 'https';
import http from 'http';
import fs from 'fs';

// Read configuration
const config = JSON.parse(fs.readFileSync('./config.json', 'utf8'));

const apiUrl = config.production.apiUrl;
const url = new URL(apiUrl);

console.log(`🔍 Testing connection to: ${apiUrl}`);

const client = url.protocol === 'https:' ? https : http;

const options = {
  hostname: url.hostname,
  port: url.port || (url.protocol === 'https:' ? 443 : 80),
  path: '/flows/',
  method: 'GET',
  timeout: 5000
};

const req = client.request(options, (res) => {
  console.log(`✅ Connection successful!`);
  console.log(`   Status: ${res.statusCode}`);
  console.log(`   Headers:`, res.headers);
  
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    try {
      const response = JSON.parse(data);
      console.log(`   Response:`, response);
      
      if (response.status === 'healthy') {
        console.log('🎉 Backend is healthy and ready!');
      }
    } catch (e) {
      console.log(`   Raw response: ${data}`);
    }
  });
});

req.on('error', (error) => {
  console.error(`❌ Connection failed: ${error.message}`);
  console.log('');
  console.log('🔧 Troubleshooting steps:');
  console.log('   1. Verify the IP address is correct');
  console.log('   2. Check if the backend is running on EC2');
  console.log('   3. Ensure port 8000 is accessible');
  console.log('   4. Check EC2 security groups allow inbound traffic on port 8000');
});

req.on('timeout', () => {
  console.error('❌ Connection timeout');
  req.destroy();
});

req.end();