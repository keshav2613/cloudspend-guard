export interface CPUHistoryPoint {
  timestamp: string
  average_cpu_percent: number
}

export interface RecommendationMetrics {
  average_cpu_percent?: number
  period_days?: number
}

export interface Recommendation {
  resource_id: string
  resource_name: string | null
  resource_type: string
  finding_type: string
  cpu_history?: CPUHistoryPoint[]
  severity: string
  metrics?: RecommendationMetrics
  message: string
  recommendation: string
  estimated_monthly_cost_usd?: number
  potential_monthly_savings_usd?: number
}

export interface RecommendationsResponse {
  count: number
  recommendations: Recommendation[]
}