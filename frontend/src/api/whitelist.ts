export interface WhitelistRequest {
  username: string
  discord_id: string
}

export interface WhitelistResponse {
  ok: boolean
  message: string
  request_id: string | null
}

const API_BASE = import.meta.env.VITE_API_BASE_URL

export async function requestWhitelist(username: string, discordId: string): Promise<WhitelistResponse> {
  if (!API_BASE) {
    throw new Error('VITE_API_BASE_URL is not set (check frontend .env and restart Vite)')
  }

  const payload: WhitelistRequest = {
    username,
    discord_id: discordId,
  }

  const res = await fetch(`${API_BASE}/whitelist/request`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  // Better error extraction (FastAPI often returns JSON error)
  if (!res.ok) {
    let msg = `Request failed (${res.status})`
    try {
      const data = await res.json()
      msg = data?.detail ?? msg
    } catch {
      const text = await res.text()
      if (text) msg = text
    }
    throw new Error(msg)
  }

  return (await res.json()) as WhitelistResponse
}
