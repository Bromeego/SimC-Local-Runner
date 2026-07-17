# Security policy

## Supported versions

Security fixes are made on the latest release and the default branch. Older
images should be upgraded rather than patched in place.

## Reporting a vulnerability

Use GitHub's **Report a vulnerability** button on the repository's Security
tab to open a private security advisory. Include the affected version, a clear
description, reproduction steps, and the impact you expect.

Please do not include character profiles, reports, credentials, or identifying
host details unless they are essential to the report. Redact them where
possible.

## Deployment boundary

simc-web is designed for trusted home or private networks. It has no built-in
authentication or user isolation and mounts the Docker socket, which grants
highly privileged access to the host. Do not expose it directly to the public
internet. Put remote deployments behind TLS, authentication, and network
access controls.
