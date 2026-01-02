import { useNavigate } from 'react-router-dom'
import Card from '../components/Card'
import Button from '../components/Button'

function Safehouse() {
  const navigate = useNavigate()

  const SERVER_IP = "10.0.0.18";     // for LAN tests; for friends outside use your public IP/DDNS
  const SERVER_PORT = 16261;
  const SERVER_PASSWORD = "5533";

  const handleJoinSafehouse = async () => {

    // Launch game script - this would typically call a backend endpoint
    // or use a protocol handler like steam:// or a custom script
    // For now, we'll show an alert as a placeholder
    const res = await fetch("http://<your-api-host>:8000/server/info");
    const data = await res.json();
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

