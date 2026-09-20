import {
  HardDrive,
  Lightbulb,
  Server,
} from 'lucide-react'


import CPUUtilizationChart from '../charts/CPUUtilizationChart'
import type { Recommendation } from '../../types/recommendations'

interface FindingCardProps {
  finding: Recommendation
}

function FindingCard({
  finding,
}: FindingCardProps) {
  const cpu =
    finding.metrics?.average_cpu_percent

  const period =
    finding.metrics?.period_days

  const isEC2 =
    finding.resource_type === 'EC2'

  const progressWidth =
    typeof cpu === 'number'
      ? Math.max(
          Math.min(cpu, 100),
          1,
        )
      : 0

  const status =
    finding.finding_type ===
    'LOW_EC2_CPU_UTILIZATION'
      ? 'Underutilized'
      : finding.finding_type ===
          'UNATTACHED_EBS_VOLUME'
        ? 'Unattached'
        : 'Review'

  return (
    <div className="finding">
      <div className="finding-top">
        <div className="resource-icon">
          {isEC2 ? (
            <Server size={20} />
          ) : (
            <HardDrive size={20} />
          )}
        </div>

        <div className="finding-title">
          <h4>
            {finding.resource_name ||
              finding.resource_id}
          </h4>

          <p>
            {finding.resource_type}{' '}
            ·{' '}
            {finding.resource_id}
          </p>
        </div>

        <span className="severity">
          {finding.severity.toUpperCase()}
        </span>
      </div>

      <div className="finding-metrics">
        {typeof cpu === 'number' ? (
          <div>
            <span>AVG. CPU</span>

            <strong>
              {cpu.toFixed(2)}%
            </strong>
          </div>
        ) : (
          <div>
            <span>RESOURCE</span>

            <strong>
              {finding.resource_type}
            </strong>
          </div>
        )}

        <div>
          <span>ANALYSIS</span>

          <strong>
            {period
              ? `${period} days`
              : 'Current state'}
          </strong>
        </div>

        <div>
          <span>STATUS</span>

          <strong className="warning-text">
            {status}
          </strong>
        </div>
      </div>

     
      {typeof cpu === 'number' && (
  <div className="utilization">
    <div className="utilization-label">
      <span>
        CPU utilization
      </span>

      <span>
        {cpu.toFixed(2)}%
      </span>
    </div>

    <div className="cpu-scale">
      <div className="progress">
        <div
          className="progress-value"
          style={{
            width: `${progressWidth}%`,
          }}
        />

        <div
          className="threshold-marker"
          style={{
            left: '5%',
          }}
        />
      </div>

      <div className="threshold-label">
        <span>0%</span>

        <span className="threshold-value">
          5% threshold
        </span>

        <span>100%</span>
      </div>
    </div>
  </div>
)}

{isEC2 &&
  finding.cpu_history &&
  finding.cpu_history.length > 0 && (
    <CPUUtilizationChart
      data={finding.cpu_history}
    />
  )}

      <div className="recommendation">
        <Lightbulb size={18} />

        <p>
          {finding.recommendation}
        </p>
      </div>

      {finding
        .potential_monthly_savings_usd !==
        undefined && (
        <div className="finding-savings">
          <span>
            ESTIMATED MONTHLY SAVINGS
          </span>

          <strong>
            $
            {finding
              .potential_monthly_savings_usd
              .toFixed(2)}
          </strong>
        </div>
      )}
    </div>
  )
}

export default FindingCard