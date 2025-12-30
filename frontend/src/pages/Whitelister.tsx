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
  const [note, setNote] = useState('')
  const [usernameError, setUsernameError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [successData, setSuccessData] = useState<{ request_id: string; message: string } | null>(null)
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

  const handleUsernameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setUsername(value)
    if (usernameError) {
      validateUsername(value)
    }
  }

  const handleNoteChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setNote(e.target.value)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccessData(null)

    if (!validateUsername(username)) {
      return
    }

    setIsLoading(true)

    try {
      const response = await requestWhitelist(username.trim(), note.trim())
      setSuccessData({
        request_id: response.request_id,
        message: response.message,
      })
      // Reset form
      setUsername('')
      setNote('')
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
          Enter your desired username so the admin can whitelist you.
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
            label="Note (Optional)"
            name="note"
            value={note}
            onChange={handleNoteChange}
            multiline
            rows={4}
            placeholder="e.g., I'm Alex from uni"
          />
          {error && (
            <div className="error-alert" role="alert" aria-live="polite">
              {error}
            </div>
          )}
          {successData && (
            <div className="success-panel" role="alert" aria-live="polite">
              <h3 className="success-title">Request sent</h3>
              <p className="success-message">{successData.message}</p>
              <p className="success-id">Request ID: {successData.request_id}</p>
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

