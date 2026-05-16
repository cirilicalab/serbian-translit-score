#!/usr/bin/env php
<?php

// Učitaj Composer-ov autoloader za korišćenje biblioteke
require_once '/vendor/autoload.php';

use Turanjanin\SerbianTransliterator\Transliterator;

if ($argc !== 2) {
    fprintf(STDERR, "Greška: Navedite putanju do jednog latiniknog fajla.\n");
    fprintf(STDERR, "Korišćenje: php preslovi.php <putanja do fajla>\n");
    exit(1);
}

$filePath = $argv[1];

if (!file_exists($filePath)) {
    fprintf(STDERR, "Greška: Fajl '%s' ne postoji.\n", $filePath);
    exit(1);
}

$latinText = file_get_contents($filePath);

if ($latinText === false) {
    fprintf(STDERR, "Greška: Fajl '%s' nije moguće pročitati.\n", $filePath);
    exit(1);
}

$cyrillicText = Transliterator::toCyrillic($latinText);

echo $cyrillicText;
