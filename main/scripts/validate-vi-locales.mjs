import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(scriptDir, '..');

const files = [
  path.join(rootDir, 'manager-web', 'src', 'i18n', 'vi.js'),
  path.join(rootDir, 'manager-mobile', 'src', 'i18n', 'vi.ts'),
];

const allowedKeys = new Set([
  'language.zhCN',
  'language.zhTW',
]);

const forbiddenPattern = /[\p{Script=Han}、。？！；：]/u;
const keyValuePattern = /^\s*'([^']+)':\s*'((?:\\.|[^'\\])*)',?\s*$/;

const issues = [];

for (const file of files) {
  const content = fs.readFileSync(file, 'utf8');
  const lines = content.split(/\r?\n/);

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    const match = line.match(keyValuePattern);
    if (!match) {
      continue;
    }

    const key = match[1];
    const value = match[2];

    if (allowedKeys.has(key)) {
      continue;
    }

    if (forbiddenPattern.test(value)) {
      issues.push({ file, line: index + 1, key, value });
    }
  }
}

if (issues.length > 0) {
  console.error('Found forbidden Han characters or Chinese punctuation in Vietnamese locale files:');
  for (const issue of issues) {
    console.error(`- ${path.relative(rootDir, issue.file)}:${issue.line} ${issue.key} -> ${issue.value}`);
  }
  process.exitCode = 1;
} else {
  console.log('Vietnamese locale validation passed.');
}
