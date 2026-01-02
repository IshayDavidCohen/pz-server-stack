import socket
import struct
from dataclasses import dataclass
from typing import Optional, Tuple

SERVER_DATA_AUTH = 3
SERVER_DATA_AUTH_RESPONSE = 2
SERVER_DATA_EXEC_COMMAND = 2
SERVER_DATA_RESPONSE_VALUE = 0

@dataclass
class RconResult:
    ok: bool
    data: str
    error: Optional[str] = None


class SourceRconClient:
    def __init__(self, host: str, port: int, password: str, timeout: float = 3.0):
        self.host = host
        self.port = port
        self.password = password
        self.timeout = timeout
        self._sock: Optional[socket.socket] = None
        self._request_id = 10

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def connect(self) -> None:
        self._sock = socket.create_connection((self.host, self.port), timeout=self.timeout)

    def close(self) -> None:
        if self._sock:
            try:
                self._sock.close()
            finally:
                self._sock = None

    def _send_packet(self, request_id: int, packet_type: int, body: str)-> None:
        if not self._sock:
            raise RuntimeError("RCON socket is not connected")

        payload = struct.pack("<ii", request_id, packet_type) + body.encode("utf-8") + b"\x00\x00"
        packet = struct.pack("<i", len(payload)) + payload
        self._sock.sendall(packet)

    def _recv_packet(self) -> Tuple[int, int, str]:
        if not self._sock:
            raise RuntimeError("Not connected")

        raw_len = self._sock.recv(4)
        if len(raw_len) < 4:
            raise ConnectionError("RCON: failed to read length")
        (length,) = struct.unpack("<i", raw_len)

        data = b""
        while len(data) < length:
            chunk = self._sock.recv(length - len(data))
            if not chunk:
                break
            data += chunk

        req_id, ptype = struct.unpack("<ii", data[:8])
        body = data[8:-2].decode("utf-8", errors="replace")
        return req_id, ptype, body

    def auth(self) -> RconResult:
        rid = self._next_id()
        self._send_packet(rid, SERVER_DATA_AUTH, self.password)

        # Some servers respond with an empty RESPONSE_VALUE and then AUTH_RESPONSE
        try:
            _ = self._recv_packet()
            req_id, ptype, body = self._recv_packet()
        except Exception as e:
            return RconResult(False, "", f"auth recv failed: {e}")

        if req_id == -1:
            return RconResult(False, "", "auth failed (bad password or unsupported RCON)")
        return RconResult(True, body)

    def exec(self, cmd: str) -> RconResult:
        rid = self._next_id()
        self._send_packet(rid, SERVER_DATA_EXEC_COMMAND, cmd)

        # Responses can come in multiple packets; gather until we stop receiving
        out = []
        try:
            while True:
                req_id, ptype, body = self._recv_packet()
                if req_id != rid:
                    # ignore unrelated packets
                    continue
                out.append(body)
                # heuristic: if body empty, break; otherwise socket timeout will stop us
                if body == "":
                    break
        except socket.timeout:
            pass
        except Exception as e:
            return RconResult(False, "", f"exec failed: {e}")

        return RconResult(True, "".join(out).strip())