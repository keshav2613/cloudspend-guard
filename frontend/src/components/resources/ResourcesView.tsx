import {
  HardDrive,
  Lock,
  Server,
} from 'lucide-react'

import type {
  DashboardResourcesData,
} from '../../types/dashboard'

interface ResourcesViewProps {
  resources: DashboardResourcesData
}

function ResourcesView({
  resources,
}: ResourcesViewProps) {
  const totalResources =
    resources.ec2.length +
    resources.ebs.length

  return (
    <section className="resources-view">
      <div className="resources-header">
        <div>
          <p className="eyebrow">
            AWS INFRASTRUCTURE
          </p>

          <h3>Cloud resources</h3>

          <p className="resources-description">
            Discovered resources in your
            connected AWS environment.
          </p>
        </div>

        <div className="resource-total">
          <span>TOTAL RESOURCES</span>
          <strong>{totalResources}</strong>
        </div>
      </div>

      <section className="panel resource-section">
        <div className="resource-section-heading">
          <div>
            <div className="resource-heading-icon">
              <Server size={18} />
            </div>

            <div>
              <h4>EC2 Instances</h4>

              <p>
                Compute resources
              </p>
            </div>
          </div>

          <span className="resource-count">
            {resources.ec2.length}
          </span>
        </div>

        {resources.ec2.length === 0 ? (
          <div className="resource-empty">
            No EC2 instances discovered.
          </div>
        ) : (
          <div className="resource-table-wrapper">
            <table className="resource-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Instance ID</th>
                  <th>Type</th>
                  <th>State</th>
                  <th>Availability Zone</th>
                  <th>Private IP</th>
                </tr>
              </thead>

              <tbody>
                {resources.ec2.map(
                  (instance) => (
                    <tr
                      key={
                        instance.instance_id
                      }
                    >
                      <td>
                        <strong>
                          {instance.name ||
                            'Unnamed'}
                        </strong>
                      </td>

                      <td className="resource-id">
                        {instance.instance_id}
                      </td>

                      <td>
                        {instance.instance_type}
                      </td>

                      <td>
                        <span
                          className={`resource-state ${
                            instance.state ===
                            'running'
                              ? 'running'
                              : ''
                          }`}
                        >
                          <span />
                          {instance.state}
                        </span>
                      </td>

                      <td>
                        {
                          instance.availability_zone
                        }
                      </td>

                      <td>
                        {instance.private_ip ||
                          '—'}
                      </td>
                    </tr>
                  ),
                )}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="panel resource-section">
        <div className="resource-section-heading">
          <div>
            <div className="resource-heading-icon">
              <HardDrive size={18} />
            </div>

            <div>
              <h4>EBS Volumes</h4>

              <p>
                Block storage resources
              </p>
            </div>
          </div>

          <span className="resource-count">
            {resources.ebs.length}
          </span>
        </div>

        {resources.ebs.length === 0 ? (
          <div className="resource-empty">
            No EBS volumes discovered.
          </div>
        ) : (
          <div className="resource-table-wrapper">
            <table className="resource-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Volume ID</th>
                  <th>Type</th>
                  <th>Size</th>
                  <th>State</th>
                  <th>Encrypted</th>
                  <th>Availability Zone</th>
                </tr>
              </thead>

              <tbody>
                {resources.ebs.map(
                  (volume) => (
                    <tr
                      key={volume.volume_id}
                    >
                      <td>
                        <strong>
                          {volume.name ||
                            'Unnamed'}
                        </strong>
                      </td>

                      <td className="resource-id">
                        {volume.volume_id}
                      </td>

                      <td>
                        {volume.volume_type}
                      </td>

                      <td>
                        {volume.size_gb} GB
                      </td>

                      <td>
                        <span className="resource-state">
                          <span />
                          {volume.state}
                        </span>
                      </td>

                      <td>
                        <div className="encryption-status">
                          {volume.encrypted && (
                            <Lock size={12} />
                          )}

                          {volume.encrypted
                            ? 'Encrypted'
                            : 'Not encrypted'}
                        </div>
                      </td>

                      <td>
                        {
                          volume.availability_zone
                        }
                      </td>
                    </tr>
                  ),
                )}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </section>
  )
}

export default ResourcesView