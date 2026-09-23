const API_URL = (() => {
  const envUrl = import.meta.env.VITE_API_URL?.trim();
  if (envUrl) return envUrl.replace(/\/$/, '');
  const devUrl = 'http://' + 'localhost' + ':8000';
  return import.meta.env.DEV ? devUrl : window.location.origin;
})();

export function resolveAssetUrl(path) {
  const value = path?.trim();
  if (!value || /^(?:https?:|data:|blob:)/i.test(value)) return value || '';
  return `${API_URL}${value.startsWith('/') ? value : `/${value}`}`;
}

function authHeaders(token) {
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function request(path, options = {}) {
  const headers = new Headers(options.headers || {});
  if (!headers.has('Content-Type') && options.body && !(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }

  const timeoutMs = options.timeout || 4000;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  const signal = options.signal || controller.signal;

  try {
    const response = await fetch(`${API_URL}${path}`, {
      ...options,
      headers,
      signal,
    });
    clearTimeout(timer);

    let data = null;
    const contentType = response.headers.get('content-type') || '';
    if (contentType.includes('application/json')) {
      data = await response.json();
    }

    if (!response.ok) {
      const message = data?.detail || 'Une erreur est survenue.';
      const error = new Error(Array.isArray(message) ? message.map((entry) => entry.msg).join(' ') : message);
      error.status = response.status;
      throw error;
    }

    return data;
  } catch (err) {
    clearTimeout(timer);
    throw err;
  }
}

export function getItems(type = '') {
  const query = type ? `?type=${encodeURIComponent(type)}` : '';
  return request(`/api/items${query}`);
}

export function login(username, password) {
  return request('/api/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  });
}

export function createItem(item, token) {
  return request('/api/items', {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify(item),
  });
}

export function updateItem(id, item, token) {
  return request(`/api/items/${id}`, {
    method: 'PUT',
    headers: authHeaders(token),
    body: JSON.stringify(item),
  });
}

export function deleteItem(id, token) {
  return request(`/api/items/${id}`, {
    method: 'DELETE',
    headers: authHeaders(token),
  });
}

export function getTags(type = '') {
  const query = type ? `?type=${encodeURIComponent(type)}` : '';
  return request(`/api/tags${query}`);
}

export function createTag(tag, token) {
  return request('/api/tags', {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify(tag),
  });
}

export function deleteTag(id, token) {
  return request(`/api/tags/${id}`, {
    method: 'DELETE',
    headers: authHeaders(token),
  });
}

export function getTestimonials(token = null) {
  const options = {};
  if (token) {
    options.headers = authHeaders(token);
  }
  return request('/api/testimonials', options);
}

export function getVeille(limit = 8) {
  return request(`/api/veille?limit=${encodeURIComponent(limit)}`);
}

export function createTestimonial(testimonial) {
  return request('/api/testimonials', {
    method: 'POST',
    body: JSON.stringify(testimonial),
  });
}

export function updateTestimonial(id, is_visible, token) {
  return request(`/api/testimonials/${id}`, {
    method: 'PUT',
    headers: authHeaders(token),
    body: JSON.stringify({ is_visible }),
  });
}

export function deleteTestimonial(id, token) {
  return request(`/api/testimonials/${id}`, {
    method: 'DELETE',
    headers: authHeaders(token),
  });
}

export async function sendContactMessage(email, subject, message) {
  const WEB3FORMS_KEY = 'b8b2578f-5ef6-4fe5-a2f5-485c99ae5985';

  const cleanSubject = (subject || '').trim() || 'Prise de contact';
  const cleanEmail = (email || '').trim();
  const cleanMessage = (message || '').trim();
  const now = new Date().toLocaleString('fr-FR', {
    dateStyle: 'full',
    timeStyle: 'medium',
    timeZone: 'Africa/Douala',
  });

  try {
    const formData = new FormData();
    formData.append('access_key', WEB3FORMS_KEY);
    formData.append('from_name', 'Portfolio Raoul BIGA');
    formData.append('subject', `[Portfolio Contact] ${cleanSubject} — (${cleanEmail})`);
    formData.append('replyto', cleanEmail);
    formData.append('Expediteur', cleanEmail);
    formData.append('Objet', cleanSubject);
    formData.append('Message', cleanMessage);
    formData.append('Date_Envoi', now);
    formData.append('Provenance', 'https://raoulbiga-phi.vercel.app');
    formData.append('botcheck', '');

    const response = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    if (response.ok && data.success) {
      return data;
    }
    throw new Error(data.message || "Échec Web3Forms");
  } catch (web3Error) {
    // Fallback automatique vers l'API backend si besoin
    return request('/api/contact', {
      method: 'POST',
      body: JSON.stringify({ email: cleanEmail, subject: cleanSubject, message: cleanMessage }),
    });
  }
}

export function uploadImage(file, token) {
  return uploadFile(file, token);
}


export function uploadFile(file, token) {
  const formData = new FormData();
  formData.append('file', file);

  return request('/api/upload', {
    method: 'POST',
    headers: authHeaders(token),
    body: formData,
  });
}
