import { useNavigate } from 'react-router-dom'
import Card from '../components/Card'
import Button from '../components/Button'

function Safehouse() {
  const navigate = useNavigate()

  const handleJoinSafehouse = () => {
    // Launch game script - this would typically call a backend endpoint
    // or use a protocol handler like steam:// or a custom script
    // For now, we'll show an alert as a placeholder
    alert('Launching Project Zomboid and joining server...')
    // In a real implementation, this might be:
    // window.location.href = 'steam://run/108600//-connect=server-ip'
    // or fetch('/api/launch-game', { method: 'POST' })
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

