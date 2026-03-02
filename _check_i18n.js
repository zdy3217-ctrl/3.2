const fs = require('fs');
const src = fs.readFileSync('src/lib/i18n.ts', 'utf8');

// Extract keys from zh and en blocks
const keyRe = /"([^"]+)":\s*"/g;

// Split by "en:" to get zh and en sections
const zhSection = src.substring(src.indexOf('zh: {'), src.indexOf('en: {'));
const enSection = src.substring(src.indexOf('en: {'));

function extractKeys(section) {
  const keys = [];
  let m;
  const re = /"([^"]+)":\s*"/g;
  while ((m = re.exec(section)) !== null) {
    keys.push(m[1]);
  }
  return keys;
}

const zhKeys = extractKeys(zhSection);
const enKeys = extractKeys(enSection);

console.log('zh keys count:', zhKeys.length);
console.log('en keys count:', enKeys.length);

const zhSet = new Set(zhKeys);
const enSet = new Set(enKeys);

const missingInEn = zhKeys.filter(k => !enSet.has(k));
const missingInZh = enKeys.filter(k => !zhSet.has(k));

if (missingInEn.length) {
  console.log('\nMissing in EN (zh has, en missing):');
  missingInEn.forEach(k => console.log('  -', k));
}
if (missingInZh.length) {
  console.log('\nMissing in ZH (en has, zh missing):');
  missingInZh.forEach(k => console.log('  -', k));
}
if (!missingInEn.length && !missingInZh.length) {
  console.log('\nAll keys match perfectly!');
}

// Check for duplicate keys
function findDupes(keys, label) {
  const seen = new Set();
  const dupes = [];
  keys.forEach(k => {
    if (seen.has(k)) dupes.push(k);
    seen.add(k);
  });
  if (dupes.length) console.log('\nDuplicate keys in ' + label + ':', dupes);
}
findDupes(zhKeys, 'zh');
findDupes(enKeys, 'en');
