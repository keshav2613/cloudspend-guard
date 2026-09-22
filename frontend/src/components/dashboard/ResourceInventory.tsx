import {
  HardDrive,
  Server,
} from 'lucide-react'

interface ResourceInventoryProps {
  ec2Count: number
  ebsCount: number
  loading: boolean
}

function ResourceInventory({
  ec2Count,
  ebsCount,
  loading,
}: ResourceInventoryProps) {
  return (
    <section className="panel inventory-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">
            INFRASTRUCTURE
          </p>

          <h3>
            Resource inventory
          </h3>
        </div>
      </div>

      <div className="inventory-list">
        <div className="inventory-row">
          <div className="inventory-icon">
            <Server size={20} />
          </div>

          <div>
            <strong>
              EC2 Instances
            </strong>

            <span>
              Compute
            </span>
          </div>

          <strong className="inventory-count">
            {loading
              ? '—'
              : ec2Count}
          </strong>
        </div>

        <div className="inventory-row">
          <div className="inventory-icon">
            <HardDrive size={20} />
          </div>

          <div>
            <strong>
              EBS Volumes
            </strong>

            <span>
              Storage
            </span>
          </div>

          <strong className="inventory-count">
            {loading
              ? '—'
              : ebsCount}
          </strong>
        </div>
      </div>

      <div className="coverage">
        <div>
          <span>
            Analysis scope
          </span>

          <strong>
            {loading
              ? '—'
              : `${ec2Count + ebsCount} resources`}
          </strong>
        </div>

        <div className="coverage-bar">
          <div />
        </div>

        <p>
          {loading
            ? 'Analyzing discovered resources'
            : 'EC2 and EBS resources included in analysis'}
        </p>
      </div>
    </section>
  )
}

export default ResourceInventory