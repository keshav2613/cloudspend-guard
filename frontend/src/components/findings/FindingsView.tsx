import {
  AlertTriangle,
  CheckCircle2,
} from 'lucide-react'

import FindingCard from './FindingCard'

import type {
  Recommendation,
} from '../../types/recommendations'

interface FindingsViewProps {
  findings: Recommendation[]
  loading: boolean
}

function FindingsView({
  findings,
  loading,
}: FindingsViewProps) {
  const ec2Findings = findings.filter(
    (finding) =>
      finding.finding_type ===
      'LOW_EC2_CPU_UTILIZATION',
  )

  const ebsFindings = findings.filter(
    (finding) =>
      finding.finding_type ===
      'UNATTACHED_EBS_VOLUME',
  )

  return (
    <section className="findings-view">
      <div className="resources-header">
        <div>
          <p className="eyebrow">
            OPTIMIZATION ENGINE
          </p>

          <h3>
            Optimization findings
          </h3>

          <p className="resources-description">
            AWS resources that may have
            opportunities for cost or
            utilization improvements.
          </p>
        </div>

        <div className="resource-total">
          <span>ACTIVE FINDINGS</span>

          <strong>
            {loading
              ? '—'
              : findings.length}
          </strong>
        </div>
      </div>

      {!loading &&
        findings.length > 0 && (
          <div className="finding-summary-grid">
            <div className="finding-summary-card">
              <div className="finding-summary-icon">
                <AlertTriangle
                  size={18}
                />
              </div>

              <div>
                <span>
                  LOW UTILIZATION EC2
                </span>

                <strong>
                  {ec2Findings.length}
                </strong>
              </div>
            </div>

            <div className="finding-summary-card">
              <div className="finding-summary-icon">
                <AlertTriangle
                  size={18}
                />
              </div>

              <div>
                <span>
                  UNATTACHED EBS
                </span>

                <strong>
                  {ebsFindings.length}
                </strong>
              </div>
            </div>
          </div>
        )}

      <section className="panel">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">
              RECOMMENDATIONS
            </p>

            <h3>
              Resources requiring review
            </h3>
          </div>

          {!loading && (
            <span className="finding-total">
              {findings.length}{' '}
              finding
              {findings.length === 1
                ? ''
                : 's'}
            </span>
          )}
        </div>

        {loading && (
          <div className="finding-state">
            <p>
              Analyzing AWS resources...
            </p>
          </div>
        )}

        {!loading &&
          findings.length === 0 && (
            <div className="finding-state">
              <CheckCircle2
                size={28}
              />

              <div>
                <strong>
                  No optimization
                  findings
                </strong>

                <p>
                  No current resource
                  waste was detected by
                  the configured rules.
                </p>
              </div>
            </div>
          )}

        {!loading &&
          findings.map((finding) => (
            <FindingCard
              key={`${finding.finding_type}-${finding.resource_id}`}
              finding={finding}
            />
          ))}
      </section>
    </section>
  )
}

export default FindingsView