# Setup guide

SimC Local Runner can run on a personal computer with Docker Desktop or on a
trusted homelab server with Docker Engine. The personal-computer setup keeps its
data in Docker-managed volumes. The homelab setup can instead keep profiles and
reports in normal host folders for direct backup access.

## Personal computer

### Before you start

Install and start [Docker Desktop](https://www.docker.com/products/docker-desktop/).
On Windows, make sure Docker Desktop is using Linux containers.

The web interface has native `linux/amd64` and `linux/arm64` images. The
official SimulationCraft image is currently `linux/amd64`, so Intel and AMD
computers provide the best performance. Apple silicon can use Docker's AMD64
emulation, but simulations may be slower.

### Download and start

1. Open the [latest release](https://github.com/Bromeego/SimC-Local-Runner/releases/latest).
2. Download **Source code (zip)** and extract it to a permanent folder.
3. Start the runner:

   - Windows: double-click `start.cmd`.
   - macOS: open Terminal in the extracted folder and run `sh start.sh`.
   - Linux desktop: run `sh start.sh`.

4. Open <http://localhost:8088> if it does not open automatically.

The launcher checks that Docker is running, downloads the newest web image, and
starts the app. Docker creates persistent volumes for profiles and reports. A
normal stop, restart, update, or `docker compose down` keeps those volumes.

### Stop and update

Stop the runner without deleting saved data:

```sh
docker compose down
```

Run the launcher again whenever you want to start or update the app. To update
manually, run:

```sh
docker compose pull simc-web
docker compose up -d
```

Do not add `--volumes` to `docker compose down` unless you intentionally want
to delete every saved profile and report.

## Homelab with host folders

The default Docker-managed volumes are also suitable for a homelab. Use this
mode when you prefer profiles and reports under a known host path such as
`/srv/simc-web`.

1. Clone the repository into the permanent deployment directory:

   ```sh
   sudo mkdir -p /srv/simc-web
   sudo chown "$USER":"$USER" /srv/simc-web
   git clone https://github.com/Bromeego/SimC-Local-Runner.git /srv/simc-web
   cd /srv/simc-web
   mkdir -p input output
   ```

2. Create `.env` from the example and set these homelab values:

   ```sh
   cp .env.example .env
   ```

   ```dotenv
   COMPOSE_FILE=compose.yaml:compose.bind.yaml
   SIMC_WEB_ROOT=/srv/simc-web
   ```

3. Start the runner:

   ```sh
   docker compose pull simc-web
   docker compose up -d
   ```

4. Open `http://SERVER-IP:8088` from another device on the trusted network.

The bind-folder override replaces the two Docker-managed data volumes. The app
discovers the resolved Docker mounts automatically and gives the same storage
to each temporary SimulationCraft container.

For a different port, timezone, resource limit, or retention count, copy the
corresponding value from [`.env.example`](../.env.example) into `.env` and edit
it. Keep the deployment on a trusted network. If remote access is required, put
it behind a reverse proxy with TLS and authentication.

## Troubleshooting

### Docker is unavailable

Confirm Docker Desktop or Docker Engine is running:

```sh
docker info
docker compose version
```

### The page does not open

Check the container and recent logs:

```sh
docker compose ps
docker compose logs --tail=100 simc-web
```

The default address is <http://localhost:8088>. A homelab is reached through
the server's hostname or LAN IP instead of `localhost`.

### A simulation cannot access its input or output

The web container must have `/data/input`, `/data/output`, and
`/var/run/docker.sock` mounted. Recreate the deployment from the supplied
Compose files rather than starting the image directly without those mounts.
