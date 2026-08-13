# Security policy

## Supported version

Security fixes are applied to the latest FRB Atlas release. The project is research and
educational software; it performs deterministic statistical analysis of a public astronomical
catalog only, accepts no untrusted file uploads, and must not be treated as a source of
real-time astronomical alerts or a substitute for the primary CHIME/FRB Collaboration
publications.

## Reporting a vulnerability

Please use GitHub's private vulnerability-reporting flow for this repository. Do not include
secrets, personal data, or exploit payloads in a public issue.

## Dependency boundary

CI rejects known high-severity vulnerabilities in production web dependencies
(`pnpm audit --prod --audit-level high`). The interactive site accepts no user file uploads,
no authentication, and no server-side persistence of visitor input — every view renders from
the frozen, committed result registry.
