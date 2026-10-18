# Changelog

Notable changes to SimC Local Runner are recorded here.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Dates use
`YYYY-MM-DD`.

## [Unreleased]

### Changed

- Refresh the project documentation and add a project-specific `DESIGN.md` for
  consistent interface work.

## [0.3.1] - 2026-10-19

### Changed

- Run Gunicorn 26.2.0, which keeps a container from shutting down when a child
  process exits while Gunicorn is PID 1.
- Count `docker.io/simulationcraftorg/simc:latest` as the nightly image and
  record the digest for the configured repository.
- Add the app version to static asset URLs so browsers download interface updates.

### Fixed

- Accept uploaded profiles whose names contain characters outside ASCII.
- Keep an uploaded profile ahead of pasted text, including when the file is empty.
- Allow a profile at the advertised upload limit to be submitted with the rest
  of the form.
- Remove saved inputs and partial reports when a simulation fails or times out,
  and stop its container if the web process is shutting down.
- Keep the report list available if a report disappears while the page loads.
- Decode SimulationCraft output as UTF-8 instead of failing on bytes the
  container locale cannot represent.
- Match the browser theme color to the selected light or dark theme.
- Accept pasted profiles up to the configured upload limit. Flask's default
  form-memory cap had rejected anything larger than 500 KB.

## [0.3.0] - 2026-07-17

### Added

- Windows and macOS/Linux launchers.
- A desktop-focused setup guide.
- An optional bind-folder Compose overlay for homelab deployments.

### Changed

- Store data in persistent Docker-managed volumes by default, with no required
  `.env` file or absolute host path.
- Discover the web container's Docker mounts automatically so SimulationCraft
  jobs can share either managed volumes or homelab bind folders.

## [0.2.0] - 2026-07-17

### Added

- An accessible header badge showing the SimulationCraft nightly used by the
  latest completed report, including its WoW build, hotfix, source commit,
  image digest, and update policy.

### Fixed

- Read current large SimulationCraft reports and labeled nightly-build output
  so the source commit appears in the badge.

## [0.1.1] - 2026-07-17

### Changed

- Check for the newest configured SimulationCraft image before every run by
  default, while retaining configurable cached and offline pull policies.

## [0.1.0] - 2026-07-17

### Added

- Drag-and-drop `.simc` and `.txt` profile uploads.
- A responsive light and dark interface.
- Patchwerk, HecticAddCleave, and DungeonSlice controls.
- A saved report list with deletion and automatic retention.
- Per-run timeout, concurrency, upload, CPU, and memory limits.
- A health check and threaded Gunicorn server.
- Reproducibility metadata containing the configured image, resolved digest,
  SimulationCraft version, settings, and run duration.
- Automated unit, Compose, container-build, and SimulationCraft smoke checks.
- Docker image publishing through GitHub Container Registry.
- A compact SimulationCraft favicon matching the web interface.

### Changed

- Pull the published GHCR image in the default Compose deployment, with a
  separate override for local builds.

### Fixed

- Reset transient simulation progress when returning to the runner with the
  browser Back button.

### Security

- Escape process error output before rendering it in the browser.
- Use unique filenames and container names for every run.
- Document the Docker socket trust boundary.

[Unreleased]: https://github.com/Bromeego/SimC-Local-Runner/compare/v0.3.1...HEAD
[0.3.1]: https://github.com/Bromeego/SimC-Local-Runner/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/Bromeego/SimC-Local-Runner/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/Bromeego/SimC-Local-Runner/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/Bromeego/SimC-Local-Runner/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/Bromeego/SimC-Local-Runner/releases/tag/v0.1.0
