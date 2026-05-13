const SerbianTransliteration = require('@exvorn/serbian-transliteration');
const { readFileSync } = require('fs');

const inputFile = process.argv[2];
if (!inputFile) {
    // Ништа не штампамо осим грешке на stderr (не на stdout)
    console.error('Употреба: node exvorn_srb_translit.cjs <улазна-датотека>');
    process.exit(1);
}

const text = readFileSync(inputFile, 'utf-8');
const converted = SerbianTransliteration.toCyrillic(text);

// Само излаз, без ичега додатног
process.stdout.write(converted);
