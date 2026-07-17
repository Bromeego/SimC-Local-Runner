# Changelog

All notable changes to this project will be documented in this file. The format
is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-07-17

### Added

- Show the SimulationCraft nightly used by the latest completed report in an
  accessible header badge, with WoW build, hotfix, source commit, image digest,
  and update-policy details.

### Fixed

- Read current large SimulationCraft reports and labeled nightly build output
  so the source commit is included in the badge.

## [0.1.1] - 2026-07-17

### Changed

- Check for the newest configured SimulationCraft image before every run by
  default, while retaining configurable cached and offline pull policies.

## [0.1.0] - 2026-07-17

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
- A compact SimulationCraft favicon matching the web interface.

### Changed

- The default Compose deployment now pulls the published GHCR image, with a
  separate override available for local builds.

### Fixed

- Reset the transient simulation progress state when returning to the runner
  with the browser Back button.

### Security

- Escaped process error output before rendering it in the browser.
- Unique per-run filenames and container names.
- Documented the Docker socket trust boundary.

[Unreleased]: https://github.com/Bromeego/SimC-Local-Runner/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/Bromeego/SimC-Local-Runner/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/Bromeego/SimC-Local-Runner/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/Bromeego/SimC-Local-Runner/releases/tag/v0.1.0
