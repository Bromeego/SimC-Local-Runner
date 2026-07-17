# Contributing to simc-web

Thanks for helping make local SimulationCraft runs easier to use.

## Before opening a change

- Search existing issues first.
- Keep the app focused: a small Docker-first runner rather than a replacement
  for full gear-optimization services.
- Open an issue before making a large interface or architecture change.
- Never include exported character profiles, generated reports, credentials,
  host paths, or other personal data in a commit.

## Local setup

1. Install Python 3.12 or newer.
2. Install the application dependencies:

   ```sh
   python -m pip install -r app/requirements.txt
   ```

3. Run the tests:

   ```sh
   python -m unittest discover -s tests -v
   ```

4. Validate the Compose configuration:

   ```sh
   SIMC_WEB_ROOT=/tmp/simc-web docker compose config --quiet
   ```

5. Build the web image:

   ```sh
   docker build -t simc-web:test app
   ```

For an end-to-end check against the official SimulationCraft image, run
`tests/smoke-test.sh` on a Linux Docker host.

## Pull requests

- Keep pull requests small and explain the user-facing reason for the change.
- Add or update tests when behavior changes.
- Update `README.md` and `CHANGELOG.md` for visible features or configuration.
- Include screenshots for meaningful interface changes, in both themes when
  the change affects them.
- Confirm that all automated checks pass.

## Reporting security problems

Please do not open a public issue for a vulnerability. Follow
[`SECURITY.md`](SECURITY.md) instead.
