<p align="center">
  <img src="app/static/favicon.svg" alt="" width="72" height="72">
</p>

<h1 align="center">SimC Local Runner</h1>

<p align="center">
  Profile in. Official SimulationCraft report out.<br>
  A private, Docker-first runner for your browser.
</p>

<p align="center">
  <a href="https://github.com/Bromeego/SimC-Local-Runner/actions/workflows/ci.yml"><img src="https://github.com/Bromeego/SimC-Local-Runner/actions/workflows/ci.yml/badge.svg" alt="CI status"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-c75b2a.svg" alt="MIT License"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="docs/SETUP.md">Setup guide</a> ·
  <a href="#configuration">Configuration</a> ·
  <a href="#troubleshooting">Troubleshooting</a> ·
  <a href="CONTRIBUTING.md">Contributing</a>
</p>

---

SimC Local Runner turns a `.simc` or `.txt` profile into an official
[SimulationCraft](https://www.simulationcraft.org/) HTML report. Upload or
paste a profile, tune the encounter, and keep the result in a local report
archive—without an account, database, external API key, or subscription.

> [!IMPORTANT]
> This app is designed for a trusted personal computer or private homelab. It
> mounts the Docker socket and does not include authentication. Do not expose it
> directly to the public internet.

## Preview

<p align="center">
  <img src="docs/screenshots/simc-web-dark.png" alt="SimC Local Runner in dark theme" width="49%">
  <img src="docs/screenshots/simc-web-light.png" alt="SimC Local Runner in light theme" width="49%">
</p>

## What it does

| Run | Preserve | Operate |
| --- | --- | --- |
| Upload, drop, or paste a profile | Save inputs and HTML reports | Start with one Compose command |
| Choose Patchwerk, HecticAddCleave, or DungeonSlice | Record image digest, SimC version, settings, and run time | Update the SimC engine automatically |
| Set iterations, targets, and fight time | Retain a bounded report history | Limit uploads, concurrency, resources, and run time |
| Use the official SimulationCraft container | Delete reports and matching inputs together | Serve a responsive light and dark interface |

The project stays intentionally small. It is a polished local path from profile
to report, not a replacement for Raidbots or a full optimization suite.

## Quick start

### 1. Download

Open the [latest release](https://github.com/Bromeego/SimC-Local-Runner/releases/latest),
download **Source code (zip)**, and extract it to a permanent folder.

### 2. Launch

| Platform | Start the runner |
| --- | --- |
| Windows | Double-click `start.cmd` |
| macOS | Open Terminal in the folder and run `sh start.sh` |
| Linux | Run `sh start.sh` |

The launcher checks Docker, pulls the current web image, and starts the app. No
`.env` file or storage path is required.

### 3. Open

Visit <http://localhost:8088>.

For a manual start:

```bash
docker compose pull simc-web
docker compose up -d
```

> [!TIP]
> The [setup guide](docs/SETUP.md) covers Docker Desktop, homelab bind folders,
> platform notes, updates, and more detailed troubleshooting.

## How a run works

1. The runner accepts an uploaded or pasted profile.
2. Your form settings replace matching `fight_style`, `iterations`,
   `desired_targets`, and `max_time` values in that profile.
3. A temporary container runs the configured official SimulationCraft image.
4. The input, HTML report, and reproducibility metadata are saved locally.

If both an upload and pasted text are present, the uploaded file wins.
DungeonSlice manages its own target flow and timing, so the runner does not add
`desired_targets` or `max_time` for that fight style.

The header badge describes the SimC nightly used by the latest completed run.
Open it to see the matching WoW build, hotfix, upstream commit, image source,
and container digest.

## Requirements

- Docker Desktop on Windows or macOS, or Docker Engine with Compose on Linux
- Linux container support and permission to access the Docker socket
- An x86-64 computer for native SimulationCraft performance

The web image supports `linux/amd64` and `linux/arm64`. The official
SimulationCraft image is currently x86-64; Apple silicon can run it through
Docker emulation, but simulations may be slower.

## Configuration

The defaults work without a `.env` file. Copy [`.env.example`](.env.example)
to `.env` only when you want to override them.

| Variable | Default | Purpose |
| --- | --- | --- |
| `SIMC_WEB_PORT` | `8088` | Host port for the web app |
| `SIMC_WEB_IMAGE` | `ghcr.io/bromeego/simc-local-runner:latest` | Web interface image used by Compose |
| `TZ` | `UTC` | Container timezone as an IANA name |
| `SIMC_IMAGE` | `simulationcraftorg/simc:latest` | SimulationCraft image used for runs |
| `SIMC_PULL_POLICY` | `always` | Engine image policy: `always`, `missing`, or `never` |
| `SIMC_CPUS` | unset | Optional CPU limit for each simulation |
| `SIMC_MEMORY` | unset | Optional memory limit such as `4g` |
| `SIMC_TIMEOUT_SECONDS` | `1800` | Maximum run time before a simulation is stopped |
| `MAX_UPLOAD_MB` | `2` | Maximum request and profile size |
| `MAX_CONCURRENT_SIMS` | `1` | Simulation jobs accepted at once |
| `REPORT_RETENTION_COUNT` | `100` | Successful reports retained |
| `WEB_THREADS` | `4` | Threads serving pages and long-running requests |

### Engine update policy

With the default `always` policy, Docker checks `SIMC_IMAGE` before every run
and reuses unchanged image layers. This keeps the nightly current across game
patches and model updates.

- `always` checks the registry before every run.
- `missing` pulls only when the image is not already cached.
- `never` uses an offline or locally built image without pulling.

## Storage and privacy

The default deployment stores profiles and reports in Docker-managed volumes.
The optional homelab mode stores them in `input/` and `output/` beneath
`SIMC_WEB_ROOT`; see [Homelab with host folders](docs/SETUP.md#homelab-with-host-folders).

Every successful report gets a matching `.json` metadata file. It records the
resolved image digest when available, the SimC version, selected settings, UTC
creation time, and wall-clock run duration.

Profiles and reports may contain character information. Back them up and share
them with the same care as any other personal data. When a report is deleted in
the interface, its matching saved input is deleted too. Retention cleanup
removes the oldest report/input pair after a successful run.

## Everyday commands

View logs:

```bash
docker compose logs -f simc-web
```

Stop the app without deleting saved data:

```bash
docker compose down
```

Update and restart:

```bash
docker compose pull simc-web
docker compose up -d
```

> [!CAUTION]
> Do not add `--volumes` to `docker compose down` unless you intend to delete
> every profile and report stored in the managed volumes.

## Build from this checkout

The default Compose file pulls the published image. Add the build override to
run the source in your current checkout:

```bash
docker compose -f compose.yaml -f compose.build.yaml up -d --build
```

Remove the override to return to the published image. Release tags such as
`v0.3.0` also publish matching container tags; set `SIMC_WEB_IMAGE` if you want
to pin one.

## Project map

```text
.
├── app/                     # Flask app, templates, static assets, container
├── docs/
│   ├── screenshots/         # README previews
│   └── SETUP.md             # Desktop and homelab setup
├── examples/demo.simc       # Anonymous smoke-test profile
├── tests/                   # Unit, browser, and engine checks
├── compose.yaml             # Published-image deployment
├── compose.bind.yaml        # Optional host-folder storage
├── compose.build.yaml       # Local source-build override
├── start.cmd                # Windows launcher
└── start.sh                 # macOS and Linux launcher
```

See [`DESIGN.md`](DESIGN.md) for the interface design system and agent
guardrails.

## Troubleshooting

### Docker socket permission error

Confirm Docker is running and `/var/run/docker.sock` is mounted as shown in
`compose.yaml`. On Linux, the account running Compose must be allowed to use
Docker.

### The page does not open

Check the service and its recent logs:

```bash
docker compose ps
docker compose logs --tail=100 simc-web
```

The desktop address is <http://localhost:8088>. For a homelab, use the server's
hostname or LAN IP.

### A simulation starts but no report appears

Check the logs for a Docker storage error. The web container must have
`/data/input`, `/data/output`, and `/var/run/docker.sock` mounted. In bind-folder
mode, `SIMC_WEB_ROOT` must exist and be writable.

### The SimulationCraft image cannot be pulled

Pull it directly to reveal the underlying Docker error:

```bash
docker pull simulationcraftorg/simc:latest
```

More fixes are collected in the [setup guide](docs/SETUP.md#troubleshooting).

## Development

Install the application dependencies and run the test suite:

```bash
.venv/bin/python -m pip install -r app/requirements.txt
.venv/bin/python -m unittest discover -s tests -v
```

Validate Compose and build the web image:

```bash
docker compose config --quiet
docker compose -f compose.yaml -f compose.build.yaml config --quiet
SIMC_WEB_ROOT=/tmp/simc-web docker compose \
  -f compose.yaml -f compose.bind.yaml config --quiet
docker build -t simc-web:test app
```

Run an end-to-end check against the real engine:

```bash
sh tests/smoke-test.sh
```

GitHub Actions runs unit, Compose, and image-build checks on every pull request.
A scheduled workflow runs the anonymous demo profile against the latest
official SimulationCraft image each week.

## Contributing and security

Focused issues and pull requests are welcome. Read
[`CONTRIBUTING.md`](CONTRIBUTING.md) before making a change, especially the
rules for removing character and host information from profiles, reports,
screenshots, and logs.

Report vulnerabilities privately as described in [`SECURITY.md`](SECURITY.md).

## Upstream projects and trademarks

This project runs the official
[`simulationcraft/simc`](https://github.com/simulationcraft/simc) engine through
its [`simulationcraftorg/simc`](https://hub.docker.com/r/simulationcraftorg/simc)
container image. SimulationCraft's contributors deserve the credit for the
simulator and its maintained class models.

SimC Local Runner is an independent community project. It is not affiliated
with or endorsed by SimulationCraft, Raidbots, or Blizzard Entertainment.
World of Warcraft and Blizzard Entertainment are trademarks or registered
trademarks of Blizzard Entertainment, Inc.

## License

SimC Local Runner is available under the [MIT License](LICENSE). SimulationCraft
and other upstream components retain their own licenses.
