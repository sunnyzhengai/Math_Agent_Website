import axios, { AxiosError, AxiosInstance, AxiosRequestConfig } from 'axios'
import {
  NextItemResponse,
  GradeResponse,
  ProgressResponse,
  UserSession,
} from '@/types/api'

/**
 * API Client for Math Agent Backend
 * 
 * Provides type-safe methods for all FastAPI endpoints with:
 * - Automatic JWT token injection
 * - Error handling
 * - Request/response interceptors
 * - Retry logic
 */

class ApiClient {
  private client: AxiosInstance
  private retryCount = 0
  private maxRetries = 3

  constructor() {
    const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Request interceptor: add JWT token
    this.client.interceptors.request.use((config) => {
      const token = this.getToken()
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    // Response interceptor: handle errors
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        // Retry on network errors (but not 4xx/5xx)
        if (!error.response && this.retryCount < this.maxRetries) {
          this.retryCount++
          return this.client.request(error.config!)
        }

        // Reset retry counter
        this.retryCount = 0

        // Handle 401 Unauthorized
        if (error.response?.status === 401) {
          this.clearToken()
          // Redirect to login (if in browser)
          if (typeof window !== 'undefined') {
            window.location.href = '/auth/login'
          }
        }

        return Promise.reject(error)
      }
    )
  }

  /**
   * Token Management
   */
  private getToken(): string | null {
    if (typeof window === 'undefined') return null
    return localStorage.getItem('authToken')
  }

  private clearToken(): void {
    if (typeof window === 'undefined') return
    localStorage.removeItem('authToken')
  }

  setToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('authToken', token)
    }
  }

  /**
   * Health & Auth
   */

  async healthz(): Promise<{ status: string; timestamp: string }> {
    const res = await this.client.get('/healthz')
    return res.data
  }

  async verifySession(accessToken: string): Promise<UserSession> {
    const res = await this.client.post('/api/auth/session', {
      access_token: accessToken,
    })
    return res.data
  }

  /**
   * Skills
   */

  async listSkills(domain: string = 'Quadratics') {
    const res = await this.client.get('/api/skills', {
      params: { domain },
    })
    return res.data.skills
  }

  /**
   * Learning - Core Endpoints
   */

  async getNextItem(
    userId: string,
    domain: string = 'Quadratics',
    seed?: number
  ): Promise<NextItemResponse> {
    const res = await this.client.post('/api/next-item', {
      user_id: userId,
      domain,
      seed,
    })
    return res.data
  }

  async gradeResponse(
    userId: string,
    itemId: string,
    selectedChoiceId: string,
    timeMs: number = 0,
    confidence: number = 0.5
  ): Promise<GradeResponse> {
    const res = await this.client.post('/api/grade', {
      user_id: userId,
      item_id: itemId,
      selected_choice_id: selectedChoiceId,
      time_ms: timeMs,
      confidence,
    })
    return res.data
  }

  /**
   * Progress & Dashboard
   */

  async getProgress(
    userId: string,
    domain: string = 'Quadratics'
  ): Promise<ProgressResponse> {
    const res = await this.client.get('/api/progress', {
      params: {
        user_id: userId,
        domain,
      },
    })
    return res.data
  }

  /**
   * Error Handling
   */

  getErrorMessage(error: unknown): string {
    if (axios.isAxiosError(error)) {
      // API returned error response
      if (error.response?.data?.message) {
        return error.response.data.message
      }
      if (error.response?.data?.detail) {
        return error.response.data.detail
      }
      // Network error
      if (error.message === 'Network Error') {
        return 'Network error. Please check your connection.'
      }
      return error.message
    }
    return 'An unknown error occurred'
  }
}

// Create singleton instance
export const apiClient = new ApiClient()

/**
 * Convenience exports for direct method usage
 * 
 * Usage:
 *   const item = await api.nextItem(userId)
 *   const result = await api.grade(userId, itemId, choiceId)
 *   const progress = await api.progress(userId)
 */
export const api = {
  // Health & Auth
  healthz: () => apiClient.healthz(),
  verifySession: (token: string) => apiClient.verifySession(token),
  setToken: (token: string) => apiClient.setToken(token),

  // Skills
  listSkills: (domain?: string) => apiClient.listSkills(domain),

  // Learning
  nextItem: (
    userId: string,
    domain?: string,
    seed?: number
  ) => apiClient.getNextItem(userId, domain, seed),

  grade: (
    userId: string,
    itemId: string,
    choiceId: string,
    timeMs?: number,
    confidence?: number
  ) => apiClient.gradeResponse(userId, itemId, choiceId, timeMs, confidence),

  // Progress
  progress: (userId: string, domain?: string) =>
    apiClient.getProgress(userId, domain),

  // Error handling
  getErrorMessage: (error: unknown) => apiClient.getErrorMessage(error),
}

export default apiClient
