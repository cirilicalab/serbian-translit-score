const fs = require('fs');
// Comprehensive browser environment mock
global.window = { 
    location: { href: 'http://localhost' },
    contentScriptInjected: false,
    addEventListener: () => {},
    MutationObserver: class MutationObserver {
        constructor() {}
        observe() {}
        disconnect() {}
    }
};

global.location = global.window.location;

// Mock document with sufficient properties
global.document = { 
    body: { childNodes: [], appendChild: () => {} }, 
    head: { childNodes: [] },
    documentElement: { childNodes: [] },
    addEventListener: () => {},
    createElement: () => ({ 
        childNodes: [], 
        setAttribute: () => {},
        getAttribute: () => null,
        appendChild: () => {}
    }),
    querySelector: () => null,
    querySelectorAll: () => [],
    getElementById: () => null,
    getElementsByTagName: () => [],
    nodeType: 9,
    nodeName: '#document',
    childNodes: [],
    hidden: false
};

// Mock chrome API with proper nested structure
global.chrome = { 
    storage: { 
        local: { 
            get: () => {},
            set: () => {}
        } 
    }, 
    runtime: { 
        sendMessage: () => {},
        onMessage: {
            addListener: () => {},
            removeListener: () => {}
        }
    } 
};

global.Node = { 
    TEXT_NODE: 3, 
    ELEMENT_NODE: 1,
    DOCUMENT_NODE: 9,
    DOCUMENT_FRAGMENT_NODE: 11
};

// Mock MutationObserver
global.MutationObserver = class MutationObserver {
    constructor(callback) {
        this.callback = callback;
    }
    observe(target, options) {
        // No-op
    }
    disconnect() {
        // No-op
    }
    takeRecords() {
        return [];
    }
};

// Mock all the processing functions before loading content.js
global.processText = () => {};
global.processTextNode = () => {};
global.processAttribute = () => {};

// Make them non-configurable
Object.defineProperty(global, 'processText', { value: () => {}, writable: false, configurable: false });
Object.defineProperty(global, 'processTextNode', { value: () => {}, writable: false, configurable: false });
Object.defineProperty(global, 'processAttribute', { value: () => {}, writable: false, configurable: false });

// Silence console
console.log = () => {};
console.warn = () => {};
console.error = () => {};


// Parse command line arguments
// Usage: node script.js <input_text> [path_to_content.js]
// If path_to_content.js is omitted, use default path
const inputFile = process.argv[2];
const contentPath = process.argv[3] || '/tmp/cirilizator/content.js';

if (!inputFile) {
    console.error('Error: Please provide input file path as first argument');
    console.error('Usage: node script.js "input_file.txt" [path/to/content.js]');
    process.exit(1);
}

try {
    inputText = fs.readFileSync(inputFile, 'utf8');
} catch (err) {
    console.error(`Error reading file ${inputFile}:`, err.message);
    process.exit(1);
}

// Read the content.js file from disk
let jsCode;
try {
    jsCode = fs.readFileSync(contentPath, 'utf8');
} catch (err) {
    console.error(`Error reading file ${contentPath}:`, err.message);
    process.exit(1);
}

eval(jsCode);

// 4. Ручно извршавање конверзије
let result;
if (typeof textToCyrillic === 'function') {
    result = textToCyrillic(inputText);
} else if (typeof window.textToCyrillic === 'function') {
    result = window.textToCyrillic(inputText);
} else {
    console.error('Error: textToCyrillic function not found');
    process.exit(1);
}

process.stdout.write(result);
process.exit(0);
