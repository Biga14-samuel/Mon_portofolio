function normalizeTag(category = '') {
  return category
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();
}

export function tagTone(category = '') {
  const value = normalizeTag(category);

  if (
    value.includes('cyber') ||
    value.includes('securite') ||
    value.includes('soc') ||
    value.includes('detection') ||
    value.includes('threat') ||
    value.includes('incident')
  ) return 'tag-cyber';
  if (value.includes('reseau') || value.includes('fibre')) return 'tag-network';
  if (value.includes('systeme') || value.includes('systemes') || value.includes('maintenance') || value.includes('virtualisation') || value.includes('cloud')) return 'tag-system';
  if (value.includes('web') || value.includes('programmation') || value.includes('scripting') || value.includes('dev')) return 'tag-web';
  if (value.includes('base') || value.includes('donnee') || value === 'db') return 'tag-data';
  if (value.includes('methodologie') || value.includes('gestion') || value.includes('conception')) return 'tag-method';
  if (value.includes('infographie') || value.includes('design')) return 'tag-design';
  if (value.includes('diplome') || value.includes('certification') || value.includes('formation')) return 'tag-learning';

  return 'neutral';
}
