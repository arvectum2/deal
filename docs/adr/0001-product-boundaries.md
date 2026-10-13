# ADR 0001 — Independent DealForge product, shared Data Platform (accepted)

**Date:** 2026-10-13

## Decision
- Own the DealForge business domain in \`arvectum2/deal\`: buyer intents, supplier RFQs, comparable offers, Deal Rooms, fees and realized savings.
- Consume \`arvectum-data\` as a **commit-pinned external dependency**, initially daa0719da31f989afcf49283ffa295cfb5f2ccac. A version bump requires adapter contract tests.
- Reuse Discount Parser code selectively only after confirming contractual IP rights and dependencies; treat it as a separate product, not a runtime dependency.
- Keep one modular monolith until commercial validation; no premature microservice decomposition.
- No outbound messages or commitment on behalf of users without explicit, recorded buyer approval.
- Preserve evidence, timestamp and comparability; no speculative savings badges.

## Why
A permanent Git branch in a commissioned application couples unrelated release and client commitments; copying the Data Platform would undo the ongoing architecture refactor.

## Review points
S1: source document extraction DTOs; S2: price verification; S3: supplier communication and approval.
