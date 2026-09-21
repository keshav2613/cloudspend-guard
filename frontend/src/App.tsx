import { useEffect, useState } from 'react'

import {
  Lightbulb,
  RefreshCw,
  Server,
  TrendingDown,
} from 'lucide-react'

import CostsView from './components/costs/CostsView'
import FindingsView from './components/findings/FindingsView'
import MetricCard from './components/dashboard/MetricCard'
import ResourceInventory from './components/dashboard/ResourceInventory'
import FindingCard from './components/findings/FindingCard'
import Header from './components/layout/Header'
import Sidebar from './components/layout/Sidebar'
import ResourcesView from './components/resources/ResourcesView'

import { getDashboard } from './services/api'

import type {
  AppView,
} from './components/layout/Sidebar'

import type {
  DashboardResourcesData,
  DashboardSummary,
} from './types/dashboard'

import type {
  RecommendationsResponse,
} from './types/recommendations'

import './index.css'


function App() {
  const [activeView, setActiveView] =
    useState<AppView>('overview')

  const [summary, setSummary] =
    useState<DashboardSummary | null>(null)

  const [resources, setResources] =
    useState<DashboardResourcesData>({
      ec2: [],
      ebs: [],
    })

  const [recommendations, setRecommendations] =
    useState<RecommendationsResponse | null>(
      null,
    )

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState<string | null>(null)

  const [lastAnalysis, setLastAnalysis] =
    useState<Date | null>(null)


  async function loadDashboard(
    forceRefresh = false,
  ) {
    try {
      setLoading(true)
      setError(null)

      const dashboardData =
        await getDashboard(forceRefresh)

      setSummary(
        dashboardData.summary,
      )

      setResources(
        dashboardData.resources,
      )

      setRecommendations({
        count:
          dashboardData.recommendations
            .length,
        recommendations:
          dashboardData.recommendations,
      })

      setLastAnalysis(
        new Date(),
      )
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Unable to load dashboard data',
      )
    } finally {
      setLoading(false)
    }
  }


  useEffect(() => {
  let cancelled = false

  async function initialLoad() {
    try {
      const dashboardData =
        await getDashboard()

      if (cancelled) {
        return
      }

      setSummary(
        dashboardData.summary,
      )

      setResources(
        dashboardData.resources,
      )

      setRecommendations({
        count:
          dashboardData.recommendations.length,
        recommendations:
          dashboardData.recommendations,
      })

      setLastAnalysis(
        new Date(),
      )
    } catch (err) {
      if (cancelled) {
        return
      }

      setError(
        err instanceof Error
          ? err.message
          : 'Unable to load dashboard data',
      )
    } finally {
      if (!cancelled) {
        setLoading(false)
      }
    }
  }

  void initialLoad()

  return () => {
    cancelled = true
  }
}, [])


  const resourceCount =
    summary?.resources.total ?? 0

  const ec2Count =
    summary?.resources.ec2 ?? 0

  const ebsCount =
    summary?.resources.ebs ?? 0

  const findingCount =
    summary?.findings.total ?? 0

  const savings =
    summary
      ?.estimated_monthly_savings_usd ??
    0

  const findings =
    recommendations?.recommendations ??
    []


  return (
    <div className="app-shell">
      <Sidebar
        findingCount={findingCount}
        loading={loading}
        activeView={activeView}
        onViewChange={setActiveView}
      />

      <main className="main-content">
        <Header
          loading={loading}
          onRefresh={() =>
            loadDashboard(true)
          }
        />

        <section className="dashboard">
          {error && (
            <div className="api-error">
              <strong>
                Unable to refresh AWS data
              </strong>

              <span>
                {error}
              </span>
            </div>
          )}

          {activeView === 'resources' ? (
  <ResourcesView
    resources={resources}
  />
) : activeView === 'findings' ? (
  <FindingsView
    findings={findings}
    loading={loading}
  />
) : activeView === 'costs' ? (
  <CostsView
    findings={findings}
    loading={loading}
  />
) : (
   
            <>
              <div className="hero">
                <div>
                  <p className="eyebrow">
                    AWS COST OPTIMIZATION
                  </p>

                  <h3>
                    Your cloud, optimized.
                  </h3>

                  <p className="hero-description">
                    Monitor resource
                    efficiency, identify
                    waste and uncover
                    opportunities to reduce
                    your AWS spend.
                  </p>
                </div>

                <div className="last-scan">
                  <span>
                    LAST ANALYSIS
                  </span>

                  <strong>
                    {loading
                      ? 'Analyzing...'
                      : lastAnalysis
                        ? lastAnalysis
                            .toLocaleTimeString(
                              [],
                              {
                                hour:
                                  '2-digit',
                                minute:
                                  '2-digit',
                              },
                            )
                        : 'Not analyzed'}
                  </strong>
                </div>
              </div>

              <div className="metric-grid">
                <MetricCard
                  title="Cloud resources"
                  value={
                    loading
                      ? '—'
                      : resourceCount
                  }
                  description={
                    loading
                      ? 'Loading resources...'
                      : `${ec2Count} EC2 · ${ebsCount} EBS`
                  }
                  icon={
                    <Server
                      size={18}
                    />
                  }
                />

                <MetricCard
                  title="Optimization findings"
                  value={
                    loading
                      ? '—'
                      : findingCount
                  }
                  description={
                    loading
                      ? 'Analyzing resources...'
                      : findingCount ===
                          0
                        ? 'No findings detected'
                        : `${findingCount} require${
                            findingCount ===
                            1
                              ? 's'
                              : ''
                          } attention`
                  }
                  icon={
                    <Lightbulb
                      size={18}
                    />
                  }
                  variant="warning"
                />

                <MetricCard
                  title="Potential savings"
                  value={
                    loading
                      ? '—'
                      : `$${savings.toFixed(
                          2,
                        )}`
                  }
                  description="Estimated monthly savings"
                  icon={
                    <TrendingDown
                      size={18}
                    />
                  }
                  variant="savings"
                />

                <MetricCard
                  title="Cloud efficiency"
                  value={
                    loading
                      ? 'Analyzing'
                      : findingCount >
                          0
                        ? 'Review'
                        : 'Optimized'
                  }
                  description={
                    loading
                      ? 'Scanning cloud resources'
                      : `${findingCount} optimization ${
                          findingCount ===
                          1
                            ? 'opportunity'
                            : 'opportunities'
                        }`
                  }
                  icon={null}
                  variant="health"
                />
              </div>

              <div className="content-grid">
                <section className="panel findings-panel">
                  <div className="panel-heading">
                    <div>
                      <p className="eyebrow">
                        SMART
                        RECOMMENDATIONS
                      </p>

                      <h3>
                        Optimization
                        opportunities
                      </h3>
                    </div>

                    <span className="finding-total">
                      {loading
                        ? 'Analyzing'
                        : `${findings.length} finding${
                            findings.length ===
                            1
                              ? ''
                              : 's'
                          }`}
                    </span>
                  </div>

                  {loading && (
                    <div className="finding-state">
                      <RefreshCw
                        size={20}
                        className="refresh-spinning"
                      />

                      <p>
                        Analyzing AWS
                        resources and
                        CloudWatch
                        metrics...
                      </p>
                    </div>
                  )}

                  {!loading &&
                    !error &&
                    findings.length ===
                      0 && (
                      <div className="finding-state">
                        <div className="success-state-icon">
                          ✓
                        </div>

                        <div>
                          <strong>
                            No optimization
                            findings
                          </strong>

                          <p>
                            No current
                            resource waste
                            was detected by
                            the configured
                            rules.
                          </p>
                        </div>
                      </div>
                    )}

                  {!loading &&
                    findings.map(
                      (finding) => (
                        <FindingCard
                          key={`${finding.finding_type}-${finding.resource_id}`}
                          finding={
                            finding
                          }
                        />
                      ),
                    )}
                </section>

                <ResourceInventory
                  ec2Count={ec2Count}
                  ebsCount={ebsCount}
                  loading={loading}
                />
              </div>
            </>
          )}
        </section>
      </main>
    </div>
  )
}

export default App