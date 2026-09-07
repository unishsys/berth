# Contributing to Berth

Thanks for your interest in Berth. This document explains how to get help,
report problems, and contribute to this repository.

## About this repository

Berth is proprietary, commercial software, and its application source is
not public. This repository is the **public distribution**: the Helm
chart, documentation, helper scripts, release binaries, and container
image live here.

That means the most valuable contributions are not application code. They
are:

- **Bug reports** for the product, the chart, or the docs.
- **Feature ideas and feedback** that shape the roadmap.
- **Improvements to what lives in this repo**: the Helm chart under
  `charts/berth`, the docs under `docs`, and the scripts under `scripts`.

## Getting help

- **Questions and troubleshooting:** open a
  [Q&A Discussion](https://github.com/unishsys/berth/discussions/categories/q-a).
- **Feature ideas:** open an
  [Ideas Discussion](https://github.com/unishsys/berth/discussions/categories/ideas)
  so others can weigh in and upvote.
- **Documentation:** start at https://berth.agrohi.com.

Please do not use issues for support questions. Issues are for confirmed
bugs and tracked work.

## Reporting a bug

1. Search [existing issues](https://github.com/unishsys/berth/issues) and
   Discussions first.
2. Open a new issue using the **Bug report** template.
3. Include your Berth version, how you deployed it, your Kubernetes
   distribution and version, and the AI provider in use.
4. Redact cluster names, tokens, and anything sensitive from logs and
   screenshots.

For security vulnerabilities, do not open a public issue. Follow
[SECURITY.md](SECURITY.md).

## Proposing changes to the chart, docs, or scripts

1. Open an issue or Discussion first for anything more than a small fix,
   so we can agree on the approach before you invest time.
2. Fork the repository and create a branch from `master`.
3. Make your change, keeping it focused and scoped to one concern.
4. For chart changes, run `helm lint charts/berth` and, where practical,
   `helm template charts/berth` to confirm it renders. Bump the chart
   version in `charts/berth/Chart.yaml` when the chart's behavior changes.
5. For docs, match the existing style: no emoji, no em-dashes, and use
   `berth.agrohi.com` for links.
6. Open a pull request against `master` using the PR template and link
   the related issue.

## Contribution terms

Berth is licensed under the [EULA](LICENSE). By submitting a contribution
to this repository, you confirm that you have the right to submit it and
that you grant Unish Systems permission to use, modify, and distribute it
as part of Berth under the project's license.

## Code of conduct

Participation in this project is governed by our
[Code of Conduct](CODE_OF_CONDUCT.md). By taking part, you agree to uphold
it.
