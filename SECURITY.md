# Security policy

> [!WARNING]
> SimC Local Runner mounts the Docker socket and has no built-in authentication
> or user isolation. Treat access to the app as privileged access to the Docker
> host. Do not expose it directly to the public internet.

## Supported versions

Security fixes are made on the latest release and the default branch. Upgrade
older images instead of patching them in place.

| Version | Supported |
| --- | --- |
| Latest release | Yes |
| Default branch | Yes |
| Older releases | No |

## Report a vulnerability

Use **Report a vulnerability** on the repository's **Security** tab to open a
private GitHub security advisory.

Include:

- the affected version or image tag;
- a concise description of the issue;
- the smallest reliable reproduction;
- the expected impact; and
- any mitigation you have already tested.

Do not include character profiles, generated reports, credentials, private
registry details, or identifying host information unless they are essential.
Redact them wherever possible.

Please keep the report private while it is being assessed and addressed.

## Deployment boundary

The intended deployment is one trusted personal computer or a private homelab
network. A simulation starts a temporary container through the host Docker
socket, so the app is not an appropriate security boundary between untrusted
users.

If remote access is required:

- place the app behind a reverse proxy with TLS and authentication;
- restrict access with a VPN, firewall, or private network policy;
- keep Docker, the web image, and the SimulationCraft image current;
- limit who can read stored profiles and reports; and
- back up only the data you intend to retain.

These measures reduce exposure; they do not turn the current app into a
multi-tenant service.
