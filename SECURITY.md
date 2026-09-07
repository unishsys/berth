# Security Policy

Berth runs inside your infrastructure and talks to your Kubernetes
clusters, so we take security seriously. Thank you for helping keep Berth
and its users safe.

## Reporting a vulnerability

Please do not report security vulnerabilities through public GitHub
issues, Discussions, or pull requests.

Instead, report privately through GitHub Security Advisories:

1. Go to https://github.com/unishsys/berth/security/advisories/new
2. Describe the issue, the affected version, and how to reproduce it.

We will acknowledge your report within 3 business days and keep you
updated as we investigate. Once a fix is available, we will coordinate a
disclosure timeline with you and credit you unless you prefer to remain
anonymous.

## What to include

- The Berth version affected (chart, image tag, or binary version).
- How Berth was deployed and configured, including the AI provider.
- A clear description of the impact and steps to reproduce.
- Any proof of concept, logs, or screenshots. Redact secrets and tokens.

## Scope

In scope:

- The Berth backend, API, and dashboard.
- The Helm chart and default deployment configuration.
- The licensing and authentication mechanisms.
- Handling of cluster credentials and AI provider keys.

Out of scope:

- Vulnerabilities in third-party dependencies that are already public and
  have an upstream fix. Please open a normal issue to bump the dependency.
- Issues that require a compromised cluster or host, or physical access.
- Findings from automated scanners without a demonstrated impact.

## Supported versions

Security fixes are applied to the latest released version. We recommend
staying current with the most recent release. Older versions are not
patched.
