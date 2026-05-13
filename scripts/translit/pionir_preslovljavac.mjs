#!/usr/bin/env node

import { readFileSync } from 'fs';
import preslovi from '/usr/local/lib/node_modules/@pionir/preslovljivac/main.js';

// Узимамо име фајла из командне линије
const filePath = process.argv[2];

if (!filePath) {
    console.error('Грешка: Нисте навели фајл. Користите: node preslovi.js <латинични фајл>');
    process.exit(1);
}

try {
    // Читамо садржај фајла
    const latinText = readFileSync(filePath, 'utf8');

    // Позивамо функцију за пресловљавање. Трећи параметар 'a' присилно претвара у ћирилицу.
    // На тај начин се увек врши пресловљавање, без обзира на аутоматску детекцију.
    const cyrillicText = preslovi(latinText, '', 'a');

    // Штампамо резултат на стандардни излаз
    console.log(cyrillicText);
} catch (error) {
    console.error(`Грешка при читању фајла: ${error.message}`);
}
