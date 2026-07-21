const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');

async function request(path, options = {}) {
  const headers = new Headers(options.headers || {});
  if (!headers.has('Content-Type') && options.body) {
    headers.set('Content-Type', 'application/json');
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });

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
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(item),
  });
}

export function updateItem(id, item, token) {
  return request(`/api/items/${id}`, {
    method: 'PUT',
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(item),
  });
}

export function deleteItem(id, token) {
  return request(`/api/items/${id}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  });
}
