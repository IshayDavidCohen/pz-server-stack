import ipaddress
from fastapi import Request
from app.core.Config import settings


def is_lan_client(request: Request) -> bool:
    client_ip = request.client.host if request.client else ""
    try:
        ip = ipaddress.ip_address(client_ip)
    except Exception:
        return False

    cidrs = [c.strip() for c in settings.LAN_CIDRS.split(",") if c.strip()]
    for c in cidrs:
        try:
            if ip in ipaddress.ip_network(c, strict=False):
                return True
        except Exception:
            continue
    return False


def build_steam_join_url(host: str, port: int, password: str | None) -> str:
    # PZ supports these JVM args for auto-connect:
    # -Dargs.server.connect="IP:PORT"
    # -Dargs.server.password="PASSWORD"
    args = [f'-Dargs.server.connect="{host}:{port}"']
    if password:
        args.append(f'-Dargs.server.password="{password}"')
    joined = " ".join(args)

    # Steam protocol run:
    # steam://run/108600//<args>
    # We'll URL-encode via simple replacement; safe enough for these args.
    from urllib.parse import quote
    return f"steam://run/108600//{quote(joined)}"
