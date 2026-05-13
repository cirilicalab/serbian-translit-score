// cyrlatconv.cjs
global.NodeList = class NodeList {};

const CyrLatConverter = require('cyrlatconverter');
const { readFileSync } = require('fs');

const inputFile = process.argv[2];
if (!inputFile) {
    console.error('Употреба: node cyrlatconv.cjs <улазна-датотека>');
    process.exit(1);
}

const text = readFileSync(inputFile, 'utf-8');
const converter = new CyrLatConverter();
converter.init();
process.stdout.write(converter.getL2C(text));
