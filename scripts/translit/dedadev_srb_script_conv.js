#!/usr/bin/env node

const { latinToCyrilic } = require('serbian-script-converter');
const fs = require('fs');

const filePath = process.argv[2];
if (!filePath) {
    console.error(`
Грешка: Нисте навели фајл.
Коришћење: node konvertuj.js <латинични фајл>
`);
    process.exit(1);
}

try {
    const latinText = fs.readFileSync(filePath, 'utf8');
    const cyrillicText = latinToCyrilic(latinText);
    console.log(cyrillicText);
} catch (error) {
    console.error(`Грешка при читању фајла: ${error.message}`);
    process.exit(1);
}
