import {
  DollarSign,
  PiggyBank,
  TrendingDown,
} from 'lucide-react'

import type {
  Recommendation,
} from '../../types/recommendations'

interface CostsViewProps {
  findings: Recommendation[]
  loading: boolean
}

function CostsView({
  findings,
  loading,
}: CostsViewProps) {
  const pricedFindings = findings.filter(
    (finding) =>
      typeof finding
        .estimated_monthly_cost_usd ===
      'number',
  )

  const identifiedCost =
    pricedFindings.reduce(
      (total, finding) =>
        total +
        (finding
          .estimated_monthly_cost_usd ??
          0),
      0,
    )

  const potentialSavings =
    findings.reduce(
      (total, finding) =>
        total +
        (finding
          .potential_monthly_savings_usd ??
          0),
      0,
    )

  return (
    <section className="costs-view">
      <div className="resources-header">
        <div>
          <p className="eyebrow">
            COST INTELLIGENCE
          </p>

          <h3>
            Cost optimization
          </h3>

          <p className="resources-description">
            Cost estimates derived from
            supported AWS pricing data and
            optimization findings.
          </p>
        </div>
      </div>

      <div className="cost-metric-grid">
        <article className="cost-metric-card">
          <div className="cost-icon">
            <DollarSign size={18} />
          </div>

          <div>
            <span>
              IDENTIFIED MONTHLY COST
            </span>

            <strong>
              {loading
                ? '—'
                : `$${identifiedCost.toFixed(
                    2,
                  )}`}
            </strong>

            <p>
              Priced optimization findings
            </p>
          </div>
        </article>

        <article className="cost-metric-card">
          <div className="cost-icon">
            <TrendingDown size={18} />
          </div>

          <div>
            <span>
              POTENTIAL SAVINGS
            </span>

            <strong>
              {loading
                ? '—'
                : `$${potentialSavings.toFixed(
                    2,
                  )}`}
            </strong>

            <p>
              Estimated monthly opportunity
            </p>
          </div>
        </article>

        <article className="cost-metric-card">
          <div className="cost-icon">
            <PiggyBank size={18} />
          </div>

          <div>
            <span>
              PRICED FINDINGS
            </span>

            <strong>
              {loading
                ? '—'
                : pricedFindings.length}
            </strong>

            <p>
              Resources with cost estimates
            </p>
          </div>
        </article>
      </div>

      <section className="panel">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">
              COST BREAKDOWN
            </p>

            <h3>
              Optimization opportunities
            </h3>
          </div>
        </div>

        {loading ? (
          <div className="resource-empty">
            Calculating cost data...
          </div>
        ) : pricedFindings.length === 0 ? (
          <div className="resource-empty">
            No priced optimization
            findings are currently
            available.
          </div>
        ) : (
          <div className="resource-table-wrapper">
            <table className="resource-table">
              <thead>
                <tr>
                  <th>Resource</th>
                  <th>Type</th>
                  <th>Finding</th>
                  <th>
                    Est. Monthly Cost
                  </th>
                  <th>
                    Potential Savings
                  </th>
                </tr>
              </thead>

              <tbody>
                {pricedFindings.map(
                  (finding) => (
                    <tr
                      key={`${finding.finding_type}-${finding.resource_id}`}
                    >
                      <td>
                        <strong>
                          {finding.resource_name ||
                            finding.resource_id}
                        </strong>
                      </td>

                      <td>
                        {finding.resource_type}
                      </td>

                      <td>
                        {finding.finding_type
                          .replaceAll(
                            '_',
                            ' ',
                          )
                          .toLowerCase()}
                      </td>

                      <td>
                        $
                        {finding
                          .estimated_monthly_cost_usd!
                          .toFixed(2)}
                      </td>

                      <td className="savings-value">
                        $
                        {(
                          finding
                            .potential_monthly_savings_usd ??
                          0
                        ).toFixed(2)}
                      </td>
                    </tr>
                  ),
                )}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <div className="cost-note">
        <strong>
          Pricing coverage
        </strong>

        <p>
          CloudSpend Guard currently
          estimates costs only for
          supported resources where AWS
          pricing integration is
          available. These values do not
          represent the account's total
          AWS bill.
        </p>
      </div>
    </section>
  )
}

export default CostsView