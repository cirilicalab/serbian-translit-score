#!/usr/bin/env node

const pravopis = require('pravopis');
const fs = require('fs');

const filepath = process.argv[2];
if (!filepath) {
    console.error('Usage: node cyr.js <latin-file>');
    process.exit(1);
}

const latinText = fs.readFileSync(filepath, 'utf-8');
const cyrillicText = pravopis.toCyrillic(latinText);
console.log(cyrillicText);
