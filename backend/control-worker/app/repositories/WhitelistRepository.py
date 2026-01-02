import json
from pathlib import Path
from typing import List, Dict

class JsonWhitelistRepository:
    def __init__(self, data_dir: str):
        self._dir = Path(data_dir)
        self._dir.mkdir(parents=True, exist_ok=True)
        self._file = self._dir / "requests.json"

    def load(self) -> List[Dict]:
        if not self._file.exists():
            return []

        txt = self._file.read_text(encoding="utf-8").strip()
        if not txt:
            return []
        return json.loads(txt)

    def save(self, rows: List[Dict]) -> None:
        self._file.write_text(json.dumps(rows, indent=2), encoding="utf-8")
