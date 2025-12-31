import time
from typing import Tuple, List, Union

from app.core.Rcon import SourceRconClient
from app.core.Config import settings

class StatusService:
    def __init__(self):
        self._cache_until = 0.0
        self._cache = (False, False, 0, [], None)  # Stands for: (online, rcon_ok, count, players, raw)

    @staticmethod
    def _parse_players(raw: str) -> List[str]:
        # After reading a bit online it made me understand it's gonna be a best-effort parse.
        # Different builds of the game print slightly different outputs.
        # If parsing fails, we just return [] but still include 'raw'.

        players = []
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue

            # Ignore headers, keep names that look sort of like usernames
            if "players" in line.lower() and "connected" in line.lower():
                continue

            # sometimes an output might contain " - name"
            # disgusting.. ik..
            if line.startswith("- "):
                players.append(line[2:].strip())
            else:
                # A fallback
                if len(line) <= 32 and " " not in line:
                    players.append(line)
        return players

    def get_status(self) -> Tuple[bool, bool, int, List[str], Union[str, None]]:
        now = time.time()
        if now < self._cache_until:
            return self._cache

        online = False
        rcon_ok = False
        player_count = 0
        players: List[str] = []
        raw: str | None = None

        try:
            c = SourceRconClient(
                host=settings.PZ_RCON_HOST,
                port=settings.PZ_RCON_PORT,
                password=settings.PZ_RCON_PASSWORD,
                timeout=2.0,
            )
            c.connect()
            auth_res = c.auth()
            if auth_res.ok:
                rcon_ok = True
                online = True
                res = c.exec("players")
                raw = res.data
                if res.ok and raw:
                    players = self._parse_players(raw)
                    player_count = len(players) if players else 0
            c.close()
        except Exception:
            online = False
            rcon_ok = False

        self._cache = (online, rcon_ok, player_count, players, raw)
        self._cache_until = now + max(1, settings.PZ_STATUS_TTL_SECONDS)
        return self._cache