# Project Zomboid Build 42 Dedicated Server — `infra/pz`

Minimal, LAN-friendly Docker Compose setup to run a Project Zomboid Build 42 (unstable) dedicated server.

## Summary
This folder contains a lightweight Docker Compose config, environment template, and helper scripts to run a Project Zomboid server for friends or small groups. It favors simplicity and local development / small-host deployment.

## Contents
- `docker-compose.yml` — Compose service for the Project Zomboid container.
- `.env.example` — Template environment variables (copy to `.env` and edit).
- `start.sh` — Start the service (optional pull, optional logs).
- `stop.sh` — Stop the service (keeps containers).
- `down.sh` — Stop and remove containers + network.
- `logs.sh` — Follow service logs.
- `server-files/` — bind-mount for server binaries / install (host).
- `server-data/` — bind-mount for persistent config, saves, logs (host).

## Prerequisites
- Docker Engine
- Docker Compose plugin (so `docker compose ...` works)
- Recommended host: Ubuntu / Linux, but works where Docker Compose plugin is available.

---

# Quickstart

1. Copy the env template and edit:
```bash
# bash
cd infra/pz
cp .env.example .env
# edit `.env` and set required values (PASSWORD, ADMIN_PASSWORD, SERVER_NAME, etc.)
```

2. Start the server (default: follow logs):
```bash
# bash
./start.sh
```

3. Stop (keeps containers):
```bash
# bash
./stop.sh
```

4. Remove containers + network:
```bash
# bash
./down.sh
```

5. View logs:
```bash
# bash
./logs.sh
```

## Important `.env` values
Ensure you set at minimum:
- `SERVER_BRANCH` — e.g. `unstable` (Build 42) or leave empty for stable.
- `SERVER_NAME` — server save name / identifier.
- `PASSWORD` — join password for players.
- `ADMIN_USERNAME` and `ADMIN_PASSWORD` — administrative credentials.

Example minimal `.env` snippet:
```env
# .env (examples)
SERVER_BRANCH=unstable
SERVER_NAME=pzserver
PASSWORD=CHANGE_ME
ADMIN_USERNAME=admin
ADMIN_PASSWORD=CHANGE_ME_ADMIN
```

## Ports
- UDP `16261` — primary game port
- UDP `16262` — secondary game port
- TCP `27015` — RCON (optional; only required if you use remote console)

If you do not need RCON, remove the `27015:27015/tcp` mapping from `docker-compose.yml`.

## RCON
RCON is optional. If enabled, set `RCON_PASSWORD` and optionally restrict access via firewall to LAN only.

## Mods & Maps
Two practical ways to add mods:
- Edit the generated server `.ini` in `server-data/` after first run (recommended and reliable).
- If your image supports it, set `MODS=` and `MAP=` in `.env` (behavior depends on image).

When editing `.ini`, there are **two values** you usually need for a mod:

* **Workshop ID** (a number from the Steam Workshop URL) → goes into `WorkshopItems=`
* **Mod ID** (a string the mod author provides, often shown on the workshop page) → goes into `Mods=`

Both lists are **semicolon `;` separated**.

#### Recommended workflow (reliable)

1. Boot once to generate config:

```bash
./start.sh
```

2. Stop:

```bash
./stop.sh
```

3. Locate and edit your server ini:

```bash
find ./server-data -type f -path "*Server*" -name "*.ini"
```

4) Edit the file that matches your server name (example):
```bash
nano ./server-data/Zomboid/Server/<SERVER_NAME>.ini
```

5) Set these keys:
- `WorkshopItems=` → numeric workshop IDs, `;` separated
- `Mods=` → mod IDs, `;` separated


6. Example: Add / update:

```ini
WorkshopItems=2169435993;2200148440
Mods=modoptions;BetterSorting
```

7. Start again:

```bash
./start.sh
```

#### Map mods (special note)

Map mods often require updating `Map=` too. Typical pattern:

```ini
Map=SomeMapFolder;Muldraugh, KY
```

Keep `Muldraugh, KY` last unless the mod author says otherwise.

#### Troubleshooting mods

* If the server boots but the mod doesn’t load: you probably added the **Workshop ID** to `Mods` (wrong) or the **Mod ID** to `WorkshopItems` (wrong).
* If a mod depends on another mod: include **both** in `WorkshopItems` and **both** Mod IDs in `Mods`.
* After editing the `.ini`, always restart (`./stop.sh` then `./start.sh`).

---

## Backups
Persistent data lives in:
- `server-data/` (saves, config, logs)
- `server-files/` (server install)

Quick backup:
```bash
# bash
tar -czf pz-backup-$(date +%F).tgz server-data server-files
```

## Notes on scripts
- `start.sh` supports environment overrides:
  - `PULL_FIRST=1` — pull image before start
  - `FOLLOW_LOGS=0` — start without following logs
  - `SERVICE_NAME` — override compose service name (default `pz_srv`)
- `stop.sh` stops service but preserves containers and network.
- `down.sh` removes containers and network but leaves bind-mounted data on disk.
- `logs.sh` follows logs for the compose service.

## Firewall & Router
- Allow UDP `16261` and `16262` through your host firewall (UFW example):
```bash
# bash
sudo ufw allow 16261/udp
sudo ufw allow 16262/udp
```
- If exposing RCON keep it LAN-only:

### LAN-only RCON example:
If your LAN is `10.0.0.0/24`, allow RCON **only from LAN** like this:

```bash
sudo ufw allow from 10.0.0.0/24 to any port 27015 proto tcp
```

(Optional) if you want to be explicit about the destination IP (your server’s LAN IP, e.g. `10.0.0.11`):
```bash
sudo ufw allow from 10.0.0.0/24 to 10.0.0.11 port 27015 proto tcp
```

And verify:

```bash
sudo ufw status verbose
```


---

## Troubleshooting
- If configs are not applied, stop the container, inspect `server-data/` for generated `.ini` files, and edit the server-specific `.ini`.
- If ports appear blocked, verify host firewall / router port forwarding.
- Use `docker compose ps` and `docker compose logs` for runtime diagnostics.

### Verify ports are published
```bash
docker compose ps
```

### Follow logs
```bash
./logs.sh
```

### Check if the server is listening
```bash
sudo ss -lunp | egrep '16261|16262'
```

### Check RCON (only if enabled)
```bash
sudo ss -lntp | egrep '27015'
```

---

## Contact / Attribution
This infra is intended for small LAN / friends deployments. Adapt as needed for public hosting, security hardening, or larger scale deployments.

