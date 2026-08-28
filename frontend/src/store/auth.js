import { reactive } from 'vue';

const STORAGE_SESSION_KEY = 'portfolio_admin_session';

export const authState = reactive({
  token: typeof sessionStorage !== 'undefined' ? sessionStorage.getItem(STORAGE_SESSION_KEY) || '' : '',
});

export function setToken(token) {
  authState.token = token;
  if (typeof sessionStorage !== 'undefined') {
    sessionStorage.setItem(STORAGE_SESSION_KEY, token);
  }
}

export function clearToken() {
  authState.token = '';
  if (typeof sessionStorage !== 'undefined') {
    sessionStorage.removeItem(STORAGE_SESSION_KEY);
  }
}

export function isAuthenticated() {
  return Boolean(authState.token);
}
