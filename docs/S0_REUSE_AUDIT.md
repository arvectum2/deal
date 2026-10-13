# S0 — Reuse and rights audit

**Checked:** 2026-10-13 against locally available repos on Mac mini.

## Technical provenance
- Data Platform: arvectum2/data-platform commit \`daa0719da31f989afcf49283ffa295cfb5f2ccac\`, package \`arvectum-data\` 0.6.0; Python >=3.11; SDK \`arvectum_data.connectors\` exports \`DiscoveryPage\`, \`DiscoveredResource\`, \`ManualURLConnector\` and \`ConnectorHealth\`. Network-bound discovery validates public HTTP(S) targets; never bypass that policy.
- Discount Parser: arvectum2/discount-parser at commit 34217cb, local \`main\` when audited; \`pyproject.toml\` currently pins a different Data Platform commit. The old app includes offer normalization, source SDK, dedup, publication ledger, scheduler, web and Telegram. This is a **candidate inventory**, not a reuse grant.

## Ownership and license gate
- The repositories contain MIT LICENSE files. This is an initial technical observation and does **not** establish the client's contractual rights under the original Kwork engagement.
- No Discount Parser source files have been copied into DealForge at S0.
- **BLOCKED / requires user-supplied contract**: verify Kwork contract, agreement for transfer of exclusive rights, deliverables, third-party licensing terms and any confidentiality provisions before sharing/refactoring code across products.
- After rights verification, extract only necessary code behind documented interfaces, preserve copyright/license notices and run regression tests in both projects.

## Accepted integration
- DealForge's \`DataPlatformDiscovery\` wraps supported \`ManualURLConnector\` and exposes only a local \`SourceCandidate\`, not unverified pricing.
- Tests use a fake connector for determinism plus an actual installed Data Platform connector health test; no public websites are contacted in CI.
- Need later: S1 document processing adapter; S2 price identity adapter; per-connector provenance and stale validation.

## Deliberate non-goals at S0
No PDF parsing, no sourcing outreach, no customer accounts, no verified savings, no automatic negotiation, no production DB. Those are gated S1–S4.
