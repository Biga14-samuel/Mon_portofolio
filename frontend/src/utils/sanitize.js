const EMOJI_RANGES = [
  [0x1f300, 0x1faff], // Supplemental symbols and pictographs, Emojis
  [0x2600, 0x27bf],   // Dingbats and misc symbols
  [0xfe00, 0xfe0f],   // Variation selectors
  [0x1f1e0, 0x1f1ff], // Regional indicators / Flags
];

function isEmojiCode(code) {
  if (!code) return false;
  if (code === 0x200d) return true;
  return EMOJI_RANGES.some(([min, max]) => code >= min && code <= max);
}

export function stripEmojis(input) {
  if (!input && input !== 0) return '';
  return Array.from(String(input))
    .filter((char) => !isEmojiCode(char.codePointAt(0)))
    .join('')
    .trim();
}

