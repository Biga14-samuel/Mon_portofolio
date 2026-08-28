export function stripEmojis(input) {
  if (!input && input !== 0) return '';
  return Array.from(String(input))
    .filter((char) => {
      const code = char.codePointAt(0);
      if (!code) return false;
      // Supplemental symbols and pictographs, Emojis
      if (code >= 0x1f300 && code <= 0x1faff) return false;
      // Dingbats and misc symbols
      if (code >= 0x2600 && code <= 0x27bf) return false;
      // Variation selectors and zero-width joiner
      if (code >= 0xfe00 && code <= 0xfe0f) return false;
      if (code === 0x200d) return false;
      // Regional indicators / Flags
      if (code >= 0x1f1e0 && code <= 0x1f1ff) return false;
      return true;
    })
    .join('')
    .trim();
}
