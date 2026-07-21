import { reactive } from 'vue';

const TOKEN_KEY = 'cercle_admin_token';

export const authState = reactive({
  token: sessionStorage.getItem(TOKEN_KEY) || '',
});

export function setToken(token) {
  authState.token = token;
  sessionStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  authState.token = '';
  sessionStorage.removeItem(TOKEN_KEY);
}

export function isAuthenticated() {
  return Boolean(authState.token);
}
