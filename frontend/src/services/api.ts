import type {
  DashboardResourcesData,
  DashboardSummary,
} from '../types/dashboard'
import type { Recommendation } from '../types/recommendations'

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'

export interface DashboardResponse {
  summary: DashboardSummary
  resources: DashboardResourcesData
  recommendations: Recommendation[]
}

export async function getDashboard(
  forceRefresh = false,
): Promise<DashboardResponse> {
  const query = forceRefresh
    ? '?refresh=true'
    : ''

  const response = await fetch(
    `${API_BASE_URL}/dashboard${query}`,
  )

  if (!response.ok) {
    throw new Error(
      `Unable to load dashboard (${response.status})`,
    )
  }

  return response.json()
}