import type { ReactNode } from 'react'

interface MetricCardProps {
  title: string
  value: string | number
  description: string
  icon: ReactNode
  variant?: 'default' | 'warning' | 'savings' | 'health'
}

function MetricCard({
  title,
  value,
  description,
  icon,
  variant = 'default',
}: MetricCardProps) {
  const iconClassName =
    variant === 'warning'
      ? 'metric-icon warning'
      : variant === 'savings'
        ? 'metric-icon savings'
        : 'metric-icon'

  return (
    <article
      className={
        variant === 'health'
          ? 'metric-card health-card'
          : 'metric-card'
      }
    >
      <div className="metric-header">
        <span>{title}</span>

        {variant === 'health' ? (
          <div className="health-indicator">
            ●
          </div>
        ) : (
          <div className={iconClassName}>
            {icon}
          </div>
        )}
      </div>

      <strong className="metric-value">
        {value}
      </strong>

      <p>
        {variant === 'warning' ? (
          <span className="warning-text">
            {description}
          </span>
        ) : (
          description
        )}
      </p>
    </article>
  )
}

export default MetricCard