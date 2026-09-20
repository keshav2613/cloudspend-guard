import {
  Bell,
  RefreshCw,
} from 'lucide-react'

interface HeaderProps {
  loading: boolean
  onRefresh: () => void
}

function Header({
  loading,
  onRefresh,
}: HeaderProps) {
  return (
    <header className="topbar">
      <div>
        <p className="eyebrow">
          CLOUD INTELLIGENCE
        </p>

        <h2>Overview</h2>
      </div>

      <div className="topbar-actions">
        <div className="live-pill">
          <span className="status-dot" />
          Live
        </div>

        <button
          className="icon-button"
          aria-label="Refresh AWS analysis"
          type="button"
          onClick={onRefresh}
          disabled={loading}
        >
          <RefreshCw
            size={18}
            className={
              loading
                ? 'refresh-spinning'
                : ''
            }
          />
        </button>

        <button
          className="icon-button"
          aria-label="Notifications"
          type="button"
        >
          <Bell size={19} />
        </button>

        <div className="avatar">
          KS
        </div>
      </div>
    </header>
  )
}

export default Header