import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Card from '../components/Card'
import Input from '../components/Input'
import Button from '../components/Button'
import { requestWhitelist } from '../api/whitelist'
import './Whitelister.css'

function Whitelister() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [discordId, setDiscordId] = useState('')
  const [usernameError, setUsernameError] = useState('')
  const [discordIdError, setDiscordIdError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [successData, setSuccessData] = useState<{ message: string; login_password: string | null } | null>(null)
  const [error, setError] = useState('')

  const validateUsername = (value: string): boolean => {
    if (!value.trim()) {
      setUsernameError('Username is required')
      return false
    }
    if (value.trim().length < 3) {
      setUsernameError('Username must be at least 3 characters')
      return false
    }
    setUsernameError('')
    return true
  }

    const validateDiscordId = (value: string): boolean => {
    const v = value.trim()
    if (!v) {
      setDiscordIdError('Discord User ID is required')
      return false
    }
    // Discord IDs are numbers of lengths commonly 17-20 digits
    if (!/^\d{17,20}$/.test(v)) {
      setDiscordIdError('Discord User ID must be 17–20 digits (numbers only)')
      return false
    }
    setDiscordIdError('')
    return true
  }

  const handleUsernameChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const value = e.target.value
    setUsername(value)
    if (usernameError) validateUsername(value)
  }

  const handleDiscordIdChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const value = e.target.value
    setDiscordId(value)
    if (discordIdError) validateDiscordId(value)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccessData(null)

    const uOk = validateUsername(username)
    const dOk = validateDiscordId(discordId)
    if (!uOk || !dOk) return

    setIsLoading(true)

    try {
      const response = await requestWhitelist(username.trim(), discordId.trim())
      setSuccessData({
        message: response.message,
        login_password: response.login_password,
      })

      // Reset form
      setUsername('')
      setDiscordId('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="page-container">
      <Card>
        <h2 className="whitelister-subtitle">
          Enter your desired username + your Discord User ID so the admin can verify you.
        </h2>
        <form onSubmit={handleSubmit}>
          <Input
            label="Username"
            name="username"
            type="text"
            value={username}
            onChange={handleUsernameChange}
            error={usernameError}
            required
            placeholder="Enter your desired username"
          />
          <Input
            label="Discord User ID"
            name="discordId"
            type="text"
            value={discordId}
            onChange={handleDiscordIdChange}
            error={discordIdError}
            required
            placeholder="e.g., 110635447562782116"
          />
          {error && (
            <div className="error-alert" role="alert" aria-live="polite">
              {error}
            </div>
          )}
            {successData && (
              <div className="success-panel" role="alert" aria-live="polite">
                <h3 className="success-title">Whitelisted</h3>
                <p className="success-message">{successData.message}</p>
                {successData.login_password && (
                  <p className="success-id">Login Password: {successData.login_password}</p>
                )}
              </div>
            )}
          <div className="form-actions">
            <Button type="submit" variant="primary" loading={isLoading} disabled={isLoading}>
              Request Whitelist
            </Button>
            <Button type="button" variant="secondary" onClick={() => navigate('/')}>
              Back to Safehouse
            </Button>
          </div>
        </form>
      </Card>
    </div>
  )
}

export default Whitelister

