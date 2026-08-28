function normalizeTag(category = '') {
  return category
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();
}

const TAG_RULES = [
  { tone: 'tag-cyber', keywords: ['cyber', 'securite', 'soc', 'detection', 'threat', 'incident'] },
  { tone: 'tag-network', keywords: ['reseau', 'fibre'] },
  { tone: 'tag-system', keywords: ['systeme', 'systemes', 'maintenance', 'virtualisation', 'cloud'] },
  { tone: 'tag-web', keywords: ['web', 'programmation', 'scripting', 'dev'] },
  { tone: 'tag-data', keywords: ['base', 'donnee', 'db'] },
  { tone: 'tag-method', keywords: ['methodologie', 'gestion', 'conception'] },
  { tone: 'tag-design', keywords: ['infographie', 'design'] },
  { tone: 'tag-learning', keywords: ['diplome', 'certification', 'formation'] },
];

export function tagTone(category = '') {
  const value = normalizeTag(category);
  if (!value) return 'neutral';

  const match = TAG_RULES.find((rule) =>
    rule.keywords.some((kw) => value.includes(kw))
  );

  return match ? match.tone : 'neutral';
}
