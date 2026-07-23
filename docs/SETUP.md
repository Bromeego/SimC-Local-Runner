# Set up SimC Local Runner

Choose the path that matches where the runner will live.

| Setup | Best for | Storage |
| --- | --- | --- |
| [Personal computer](#personal-computer) | Windows, macOS, or Linux desktop | Docker-managed volumes |
| [Homelab with host folders](#homelab-with-host-folders) | A trusted always-on Linux server | `input/` and `output/` on the host |

> [!IMPORTANT]
> Both setups mount the Docker socket and are intended for a trusted private
> network. The runner does not include authentication.

## Personal computer

### Before you start

Install and start [Docker Desktop](https://www.docker.com/products/docker-desktop/)
or Docker Engine with Compose. On Windows, configure Docker Desktop to use
Linux containers.

The SimC Local Runner web image supports `linux/amd64` and `linux/arm64`. The
official SimulationCraft image is currently `linux/amd64`, so Intel and AMD
computers deliver native performance. Apple silicon uses Docker's AMD64
emulation and may run simulations more slowly.

### Download and launch

1. Open the [latest release](https://github.com/Bromeego/SimC-Local-Runner/releases/latest).
2. Download **Source code (zip)** and extract it to a permanent folder.
3. Start the runner:

   | Platform | Action |
   | --- | --- |
   | Windows | Double-click `start.cmd` |
   | macOS | Open Terminal in the folder and run `sh start.sh` |
   | Linux desktop | Run `sh start.sh` |

4. Open <http://localhost:8088> if it does not open automatically.

The launcher confirms Docker is available, downloads the newest web image, and
starts the app. Docker creates persistent volumes for profiles and reports. A
normal stop, restart, update, or `docker compose down` keeps those volumes.

### Stop

Stop the runner without deleting saved data:

```bash
docker compose down
```

> [!CAUTION]
> Do not add `--volumes` unless you intentionally want to delete every saved
> profile and report in the managed volumes.

### Update

Run the launcher again, or update manually:

```bash
docker compose pull simc-web
docker compose up -d
```

The web image updates immediately. The configured SimulationCraft engine is
checked according to `SIMC_PULL_POLICY` when the next simulation begins.

## Homelab with host folders

The default managed volumes also work on a homelab. Use this optional mode when
you need profiles and reports in a known host path for direct backup access.
The example below uses `/srv/simc-web`.

### 1. Prepare the deployment folder

```bash
sudo mkdir -p /srv/simc-web
sudo chown "$USER":"$USER" /srv/simc-web
git clone https://github.com/Bromeego/SimC-Local-Runner.git /srv/simc-web
cd /srv/simc-web
mkdir -p input output
```

### 2. Enable bind-folder storage

Copy the environment example:

```bash
cp .env.example .env
```

Add or uncomment:

```dotenv
COMPOSE_FILE=compose.yaml:compose.bind.yaml
SIMC_WEB_ROOT=/srv/simc-web
```

`SIMC_WEB_ROOT` must be an absolute path containing the `input/` and `output/`
folders.

### 3. Start the runner

```bash
docker compose pull simc-web
docker compose up -d
```

### 4. Open it on the private network

Visit `http://SERVER-IP:8088` from another trusted device.

The bind override replaces the two managed data volumes. The app discovers the
resolved mounts and gives the same storage to every temporary SimulationCraft
container.

> [!TIP]
> To change the port, timezone, resource limits, or retention count, copy the
> corresponding setting from [`.env.example`](../.env.example) into `.env`.

## Build from source

To run the web app from the current checkout instead of the published image:

```bash
docker compose -f compose.yaml -f compose.build.yaml up -d --build
```

For source builds with bind-folder storage:

```bash
SIMC_WEB_ROOT=/srv/simc-web docker compose \
  -f compose.yaml \
  -f compose.bind.yaml \
  -f compose.build.yaml \
  up -d --build
```

## Troubleshooting

### Docker is unavailable

Confirm that Docker Desktop or Docker Engine is running:

```bash
docker info
docker compose version
```

If either command fails, resolve Docker access before starting the runner.

### The page does not open

Check the container state and recent logs:

```bash
docker compose ps
docker compose logs --tail=100 simc-web
```

The desktop address is <http://localhost:8088>. On a homelab, use the server's
hostname or LAN IP rather than `localhost`.

If another service already uses port `8088`, set a different host port in
`.env`:

```dotenv
SIMC_WEB_PORT=8090
```

Then recreate the service with `docker compose up -d`.

### A simulation cannot access its input or output

The web container needs all three mounts:

- `/data/input`
- `/data/output`
- `/var/run/docker.sock`

Recreate the deployment from the supplied Compose files instead of starting the
image directly without its mounts.

In bind-folder mode, also confirm that:

- `SIMC_WEB_ROOT` is an absolute path;
- `input/` and `output/` exist beneath it; and
- the Docker daemon can read and write both folders.

### The SimulationCraft image will not pull

Pull the engine directly to see the registry or platform error:

```bash
docker pull simulationcraftorg/simc:latest
```

If the host must run offline, pull the image in advance and set:

```dotenv
SIMC_PULL_POLICY=never
```

### The runner is slow on Apple silicon

The web interface runs natively on ARM64, but the current official
SimulationCraft image runs through AMD64 emulation. Lowering iterations can
shorten a test run; use an x86-64 host when native simulation performance is
important.

## Next steps

- Review all optional settings in [`.env.example`](../.env.example).
- Read the [storage and privacy notes](../README.md#storage-and-privacy).
- Keep the deployment inside the boundary described in
  [`SECURITY.md`](../SECURITY.md).
