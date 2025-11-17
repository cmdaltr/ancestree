import axios from 'axios'
import { useAuthStore } from '../stores/authStore'

const api = axios.create({
  baseURL: '/api',
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', new URLSearchParams(data), {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }),
  me: () => api.get('/auth/me'),
}

// Family Members API
export const familyAPI = {
  getAll: () => api.get('/family-members'),
  getOne: (id) => api.get(`/family-members/${id}`),
  create: (data) => api.post('/family-members', data),
  update: (id, data) => api.put(`/family-members/${id}`, data),
  delete: (id) => api.delete(`/family-members/${id}`),
  getChildren: (id) => api.get(`/family-members/${id}/children`),
  getAncestors: (id, generations = 3) => api.get(`/family-members/${id}/ancestors?generations=${generations}`),
}

// Documents API
export const documentsAPI = {
  getAll: (familyMemberId = null) => {
    const params = familyMemberId ? `?family_member_id=${familyMemberId}` : ''
    return api.get(`/documents${params}`)
  },
  getOne: (id) => api.get(`/documents/${id}`),
  upload: (formData) => api.post('/documents', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  delete: (id) => api.delete(`/documents/${id}`),
}

// Search API
export const searchAPI = {
  genealogy: (query) => api.post('/search/genealogy', query),
  history: () => api.get('/search/history'),
  sources: () => api.get('/search/sources'),
}

export default api
