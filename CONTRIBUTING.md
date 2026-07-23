# Contributing to SimC Local Runner

Thanks for helping make local SimulationCraft runs easier to operate and easier
to trust.

> [!NOTE]
> The project is deliberately narrow: a small, Docker-first runner from profile
> to official HTML report. Changes should strengthen that path rather than turn
> the app into a hosted optimization service.

## Before you begin

- Search existing issues and pull requests.
- Open an issue before a large interface or architecture change.
- Keep changes focused on one user-facing problem.
- Never commit exported character profiles, generated reports, credentials,
  host paths, image digests tied to a private registry, or other personal data.
- Read [`DESIGN.md`](DESIGN.md) before changing the interface.

## Development setup

### 1. Prepare Python

Use Python 3.12 or newer, preferably in a virtual environment:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r app/requirements.txt
```

On Windows PowerShell, activate the environment with
`.venv\Scripts\Activate.ps1`.

### 2. Run the checks

```bash
python -m unittest discover -s tests -v
docker compose config --quiet
docker compose -f compose.yaml -f compose.build.yaml config --quiet
docker build -t simc-web:test app
```

Validate the optional bind-folder deployment separately:

```bash
SIMC_WEB_ROOT=/tmp/simc-web docker compose \
  -f compose.yaml -f compose.bind.yaml config --quiet
```

### 3. Exercise the real engine

On a Linux Docker host, run:

```bash
sh tests/smoke-test.sh
```

This uses the anonymous [`examples/demo.simc`](examples/demo.simc) profile
against the official SimulationCraft image.

## What to test

| Change | Minimum evidence |
| --- | --- |
| Python behavior | Add or update a unit test |
| Browser behavior | Update the JavaScript test where practical |
| Compose or environment settings | Validate every affected Compose combination |
| Interface layout or color | Check narrow and wide screens in both themes |
| User-visible behavior | Update `README.md` and `CHANGELOG.md` |
| Meaningful interface change | Include light and dark screenshots |

## Pull request checklist

- [ ] The pull request explains the user-facing reason for the change.
- [ ] The change stays small enough to review as one unit.
- [ ] Tests cover new or changed behavior.
- [ ] Compose configurations still validate.
- [ ] Documentation and changelog entries are current.
- [ ] Screenshots, logs, profiles, and reports contain no personal information.
- [ ] Both themes and keyboard focus states were checked for UI changes.
- [ ] Automated checks pass.

## Design changes

Preserve the interface's local-workbench character: warm paper in light mode,
charcoal in dark mode, ember-orange for decisive actions, monospace for
technical detail, and restrained motion. Use existing tokens and patterns
before adding new ones.

The complete palette, type hierarchy, component rules, responsive behavior, and
design anti-patterns live in [`DESIGN.md`](DESIGN.md).

## Security reports

Do not open a public issue for a vulnerability. Follow the private reporting
process in [`SECURITY.md`](SECURITY.md).
