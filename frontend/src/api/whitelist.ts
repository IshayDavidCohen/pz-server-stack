export interface WhitelistRequest {
  username: string
  note: string
}

export interface WhitelistResponse {
  ok: boolean
  message: string
  request_id: string
}

export async function requestWhitelist(
  username: string,
  note: string
): Promise<WhitelistResponse> {
  const response = await fetch('http://localhost:8000/whitelist/request', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username,
      note,
    }),
  })

  if (!response.ok) {
    let errorMessage = `Request failed with status ${response.status}`
    try {
      const errorData = await response.json()
      errorMessage = errorData.message || errorData.detail || errorMessage
    } catch {
      // If response is not JSON, use default error message
    }
    throw new Error(errorMessage)
  }

  const data: WhitelistResponse = await response.json()

  if (!data.ok) {
    throw new Error(data.message || 'Request failed')
  }

  return data
}

