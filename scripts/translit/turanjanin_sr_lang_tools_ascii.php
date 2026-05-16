#!/usr/bin/env php
<?php

// Učitaj Composer-ov autoloader za korišćenje biblioteke
require_once '/vendor/autoload.php';

use Turanjanin\SerbianLanguageTools\Text;
use Turanjanin\SerbianLanguageTools\Transformers\ToAsciiLatin;
use Turanjanin\SerbianLanguageTools\Transformers\ToCyrillic;
use Turanjanin\SerbianLanguageTools\Transformers\ToLatin;
use Turanjanin\SerbianLanguageTools\Transformers\DiacriticRestorer;

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

$asciiStr = file_get_contents($filePath);

if ($asciiStr === false) {
    fprintf(STDERR, "Greška: Fajl '%s' nije moguće pročitati.\n", $filePath);
    exit(1);
}

$asciiText = Text::fromString($asciiStr);
$latin = (new DiacriticRestorer)($asciiText);

// !!!exception thrown unless this is executed
(new ToLatin)(Text::fromString(''));

$cyrillic = (new ToCyrillic)($latin); // Пример латиничног текста
echo $cyrillic;

