# Changelog

All notable changes to this project will be documented in this file. The format
is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Drag-and-drop `.simc` and `.txt` profile uploads.
- Responsive light and dark interface.
- Patchwerk, HecticAddCleave, and DungeonSlice controls.
- Saved report list with deletion and automatic retention.
- Per-run timeout, concurrency, upload, CPU, and memory limits.
- Health check and threaded Gunicorn server.
- Reproducibility metadata beside each report, including the configured image,
  resolved digest, SimulationCraft version, settings, and run duration.
- Automated unit, Compose, container-build, and SimulationCraft smoke checks.
- Docker image publishing workflow for GitHub Container Registry.

### Security

- Escaped process error output before rendering it in the browser.
- Unique per-run filenames and container names.
- Documented the Docker socket trust boundary.

### Fixed

- Reset the transient simulation progress state when returning to the runner
  with the browser Back button.
