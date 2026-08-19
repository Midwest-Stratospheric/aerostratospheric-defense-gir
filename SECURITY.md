# Security Policy

## Supported versions

This repository publishes **open-tier public data and automation scripts**. There is no traditional “product version” with security patches. Scripts and workflows on the `main` branch are the current surface.

## Reporting a vulnerability

If you discover a security issue in the automation (e.g. unsafe handling of untrusted remote content, accidental secret exposure, or a way to inject data into committed artifacts), please:

1. **Do not** open a public issue with exploit details.
2. Email **launchcontrol@midwestsds.com** with a clear description and, if possible, steps to reproduce.
3. Allow reasonable time for review before public disclosure.

We will acknowledge receipt and work to remediate issues that affect the integrity of the public data pipeline or repository credentials.

## Out of scope

- Issues in upstream public feeds (NWS, USGS, NASA, CISA, etc.) — report those to the source operators.
- “Missing classified data” or requests for restricted content — this repo intentionally contains only open-tier material.
- Social-engineering or speculative threat scenarios unrelated to the code/data in this repository.

## Secrets

Optional API keys (e.g. FIRMS) must live in GitHub Actions secrets, never in the tree. Rotate any key that appears in history or logs.
