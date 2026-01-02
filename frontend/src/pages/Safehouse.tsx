import { useNavigate } from 'react-router-dom'
import Card from '../components/Card'
import Button from '../components/Button'

const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api"

function Safehouse() {
  const navigate = useNavigate()

  const handleJoinSafehouse = async () => {
    const res = await fetch(`${API_BASE}/server/info`)
    if (!res.ok) throw new Error("Failed to fetch server info")
    const data = await res.json()

    alert('Launching Project Zomboid and joining server...')
    window.location.href = data.steam_url;
  }

  const handleGrantAccess = () => {
    navigate('/whitelister')
  }

  return (
    <div className="page-container">
      <Card title="Safehouse">
        <div className="button-group">
          <Button variant="primary" onClick={handleJoinSafehouse}>
            Join Safehouse
          </Button>
          <Button variant="secondary" onClick={handleGrantAccess}>
            Grant Access
          </Button>
        </div>
      </Card>
    </div>
  )
}

export default Safehouse

