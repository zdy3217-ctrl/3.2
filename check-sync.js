const fs = require('fs');

const files = fs.readdirSync('src/components').filter(f => f.endsWith('.tsx')).map(f => f.replace('.tsx',''));
const nonPanel = ['ErrorBoundary','ErrorToast','LanguageSwitcher','MobileNav','LoginPage','Onboarding','Providers','PwaInstallPrompt','Sidebar','Skeleton','ShortcutHelp','TemplateBar','Toast'];
const panelFiles = files.filter(f => !nonPanel.includes(f));

const page = fs.readFileSync('src/app/page.tsx','utf8');

// Extract lazy imports
const lazyRe = /const (\w+) = lazyPanel\("(\w+)"\)/g;
let m; const lazyImports = {};
while((m = lazyRe.exec(page)) !== null) { lazyImports[m[1]] = m[2]; }

// Extract tabContentMap keys - fix regex to match actual format
const mapKeys = [];
const mapSection = page.substring(page.indexOf('const tabContentMap'), page.indexOf('function renderTabContent'));
// Match keys like: "quickstart": () => or  quickstart: () =>
const mapRe = /["']?([\w-]+)["']?\s*:\s*\(\)\s*=>/g;
while((m = mapRe.exec(mapSection)) !== null) { mapKeys.push(m[1]); }

// Extract tabs array ids
const tabIds = [];
const tabSection = page.substring(page.indexOf('const tabs:'), page.indexOf('export default function Home'));
const tabRe = /id:\s*"([\w-]+)"/g;
while((m = tabRe.exec(tabSection)) !== null) { tabIds.push(m[1]); }

// Extract Tab type values
const typesContent = fs.readFileSync('src/types/index.ts','utf8');
const typeIds = [];
const typeRe = /"([\w-]+)"/g;
const typeLine = typesContent.substring(typesContent.indexOf('export type Tab'), typesContent.indexOf(';', typesContent.indexOf('export type Tab')));
while((m = typeRe.exec(typeLine)) !== null) { typeIds.push(m[1]); }

const lazyValues = new Set(Object.values(lazyImports));
const missingImport = panelFiles.filter(f => !lazyValues.has(f));
console.log('=== Component files without lazy import ===');
console.log(missingImport.length ? missingImport.join('\n') : 'NONE');

const fileSet = new Set(files);
const badImport = Object.entries(lazyImports).filter(([k,v]) => !fileSet.has(v));
console.log('\n=== Lazy imports pointing to missing files ===');
console.log(badImport.length ? badImport.map(([k,v])=>k+' -> '+v).join('\n') : 'NONE');

const mapSet = new Set(mapKeys);
const tabSet = new Set(tabIds);
const typeSet = new Set(typeIds);

const tabNotInMap = tabIds.filter(id => !mapSet.has(id));
console.log('\n=== In tabs[] but NOT in tabContentMap ===');
console.log(tabNotInMap.length ? tabNotInMap.join('\n') : 'NONE');

const mapNotInTab = mapKeys.filter(id => !tabSet.has(id));
console.log('\n=== In tabContentMap but NOT in tabs[] ===');
console.log(mapNotInTab.length ? mapNotInTab.join('\n') : 'NONE');

const tabNotInType = tabIds.filter(id => !typeSet.has(id));
console.log('\n=== In tabs[] but NOT in Tab type ===');
console.log(tabNotInType.length ? tabNotInType.join('\n') : 'NONE');

const typeNotInTab = typeIds.filter(id => !tabSet.has(id));
console.log('\n=== In Tab type but NOT in tabs[] ===');
console.log(typeNotInTab.length ? typeNotInTab.join('\n') : 'NONE');

const typeNotInMap = typeIds.filter(id => !mapSet.has(id));
console.log('\n=== In Tab type but NOT in tabContentMap ===');
console.log(typeNotInMap.length ? typeNotInMap.join('\n') : 'NONE');

console.log('\n=== STATS ===');
console.log('Panel files:', panelFiles.length);
console.log('Lazy imports:', Object.keys(lazyImports).length);
console.log('tabs[] entries:', tabIds.length);
console.log('tabContentMap entries:', mapKeys.length);
console.log('Tab type entries:', typeIds.length);
