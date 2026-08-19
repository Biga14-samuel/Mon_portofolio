export function stripEmojis(input) {
  if (!input && input !== 0) return '';
  const str = String(input);
  // Regex to remove most emoji characters and pictographs
  return str.replace(/([\u2700-\u27BF]|[\uE000-\uF8FF]|[\uD83C-\uDBFF\uDC00-\uDFFF]|[\u2011-\u26FF]|[\uFE00-\uFE0F])/g, '').trim();
}
