import {
  Cloud,
  LayoutDashboard,
  Lightbulb,
  Server,
  Settings,
  WalletCards,
} from 'lucide-react'

export type AppView =
  | 'overview'
  | 'resources'
  | 'findings'
  | 'costs'

interface SidebarProps {
  findingCount: number
  loading: boolean
  activeView: AppView
  onViewChange: (view: AppView) => void
}

function Sidebar({
  findingCount,
  loading,
  activeView,
  onViewChange,
}: SidebarProps) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon">
          <Cloud size={22} />
        </div>

        <div>
          <h1>CloudSpend</h1>
          <span>GUARD</span>
        </div>
      </div>

      <nav className="nav">
        <p className="nav-label">
          WORKSPACE
        </p>

        <button
          className={`nav-item ${
            activeView === 'overview'
              ? 'active'
              : ''
          }`}
          type="button"
          onClick={() =>
            onViewChange('overview')
          }
        >
          <LayoutDashboard size={19} />
          Overview
        </button>

        <button
          className={`nav-item ${
            activeView === 'resources'
              ? 'active'
              : ''
          }`}
          type="button"
          onClick={() =>
            onViewChange('resources')
          }
        >
          <Server size={19} />
          Resources
        </button>

        <button
          className={`nav-item ${
            activeView === 'findings'
              ? 'active'
              : ''
          }`}
          type="button"
          onClick={() =>
            onViewChange('findings')
          }
        >
          <Lightbulb size={19} />
          Findings

          {!loading && findingCount > 0 && (
            <span className="nav-count">
              {findingCount}
            </span>
          )}
        </button>

        <button
          className={`nav-item ${
            activeView === 'costs'
              ? 'active'
              : ''
          }`}
          type="button"
          onClick={() =>
            onViewChange('costs')
          }
        >
          <WalletCards size={19} />
          Costs
        </button>
      </nav>

      <div className="sidebar-bottom">
        <button
          className="nav-item"
          type="button"
        >
          <Settings size={19} />
          Settings
        </button>

        <div className="aws-status">
          <div className="status-header">
            <span className="status-dot" />
            AWS Connected
          </div>

          <p>eu-west-1</p>

          <span>
            On-demand AWS analysis
          </span>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar