# Feedback: design robinhood

Companion to `design_report_design_robinhood_20260727_220944.md`. One evolving
file per question — on re-assessment, mark items RESOLVED (with date) rather
than duplicating them, and append new IDs for anything newly found.

Status legend: **OPEN** (gap, not yet addressed) · **RESOLVED** (fixed in a
later attempt) · **AFFIRMED** (discussed and confirmed as the right call, no
action needed).

## Assessment: 2026-07-28

### Requirements
- [req-01] OPEN: no cancel/modify-order functional requirement stated.
- [req-02] OPEN: auth/KYC not explicitly named as out-of-scope.
- [req-03] OPEN: "transfer money" ambiguity never resolved — is it ACH deposit/withdraw (multi-day, can bounce) or internal account-to-account transfer? Changes whether settlement needs async/pending-state handling.
- [req-04] OPEN: no scale/traffic numbers stated at requirements time.
- [req-05] OPEN: NFRs stated as a flat system-wide list rather than scoped per flow — e.g. "highly consistent" applied uniformly instead of distinguishing order/transfer writes (CP) from ticker/portfolio reads (AP).
- [req-06] OPEN: no durability NFR named separately from consistency (financial data must never be lost).

### Capacity Estimation
- [cap-01] N/A: this step didn't exist yet when this design was assessed (added 2026-07-28). Apply fresh on re-assessment — traffic (users, read:write ratio, avg/peak QPS) and throughput (payload sizes, bandwidth, storage growth).

### APIs
- [api-01] OPEN: no idempotency key on `POST /order/create` or `POST /transfer` — a client retry can double-submit. Fix: client-generated key (UUID), not backend-derived from field hashing (a hash can't distinguish "retry" from "intentional duplicate order").
- [api-02] OPEN: `price` on order create should be marked optional (`price?`), required only when `pricing_type=limit`.
- [api-03] OPEN: callback endpoints (`/callbacks/marketmaker`, `/callbacks/exchangeservice`) have no auth/signature verification. Add an HMAC signature in a request header (verified against raw body) plus a timestamp to block replay.
- [api-04] OPEN: `rpc accountService` request has no explicit buy/sell (`side`) field — "add stock position" can't tell direction.

### Workflows
- [wf-01] OPEN: order-create workflow has no durable persist-as-PENDING step before dispatching to `marketMakerService` — a crash mid-dispatch loses all record the order was attempted.
- [wf-02] OPEN: `orderCache` is never written by the order-create workflow, but `POST /status/order` reads from it — the status API depends on a cache the create-workflow never populates.
- [wf-03] OPEN: `POST /status/order` has no fallback to durable storage on a cache miss (relevant once filled orders are evicted from cache — see opt discussion below).
- [wf-04] OPEN: transfer workflow (`transferService -> SQS -> settlementService`) has no pending/settled state or ledger step — thin for what's likely ACH-style money movement (ties to req-03).
- [wf-05] AFFIRMED: keeping the market-maker/exchange failure & rollback path out of the happy-path workflow diagram, and covering it in Edge Cases instead, is the right time allocation for a 45-min session.

### Architecture
- [arch-01] OPEN: no orders table anywhere in the schema — `orderCache` is described as a cache with an eviction policy, but nothing durable backs it once entries are evicted (same root cause as wf-01/wf-02).
- [arch-02] OPEN: no ledger/transfer table backing `transferService`/`settlementService` (same root cause as wf-04).
- [arch-03] OPEN: `marketMakerService` and `exchangeService` are typed/drawn identically to owned internal services, despite being external counterparty integrations. Retype as "Other" (matching SQS) and/or rename to `*Gateway` to signal "adapter to a system I don't control."
- [arch-04] AFFIRMED: keeping both raw `lot[]` and a rolled-up `avg_cost/shares/amount` in the positions table is a good, intentional denormalization (lots for tax-lot accounting, rollup for fast reads) — just needs a one-line note that the rollup updates transactionally with each lot insert.

### Optimizations
- [opt-01] OPEN: distributed lock on account/fund access undermines "highly available" — a lock-service outage or an unreleased lock after a crash takes down all account operations. Replace with an optimistic/conditional update (`UPDATE ... WHERE balance >= amount`) — same consistency guarantee, no lock dependency, fails closed instead of blocking.
- [opt-02] OPEN: sharding strategy names no shard key. Use `account_id` for accounts/positions (matches access pattern), `ticker`/hash-of-ticker for market data — worth stating explicitly given the design's own meme-stock hot-partition callout.
- [opt-03] OPEN: no read replicas mentioned for Postgres despite read-heavy portfolio/performance endpoints — pair with the read:write ratio now captured in Capacity Estimation to justify.
- [opt-04] OPEN: horizontal-scaling justification ("traffic tends to be persistent") is asserted rather than grounded in actual peak-multiplier data — tie to Capacity Estimation numbers.
- [opt-05] OPEN: CAP framing not stated explicitly for the (now-recommended) read-replica topology — say directly: writes (balance/orders) are CP, reads (ticker/portfolio) are AP, since partition behavior differs per data path.

### Edge Cases
- [edge-01] OPEN: "Large Scale Failures" section is completely empty — no entries for a sustained 3rd-party outage (exchange/market-maker down for an extended period, not just a transient 5xx), AZ/DC-level failure, or deployment failure, despite depending on external market-maker/exchange integrations.
- [edge-02] OPEN: overdraft-prevention edge case is described as check-then-act ("always check if order exists if executed whether balance fall below requirement"), which reintroduces the TOCTOU race that opt-01's atomic-update fix is meant to close. Rewrite to point at the atomic conditional update directly rather than a separate check step.
- [edge-03] OPEN: cache-miss mitigation ("loosen eviction policy") treats a miss-*rate* problem, not a miss-*storm*/thundering-herd problem. Add request coalescing/single-flight (or a short-TTL repopulation lock) so concurrent misses on the same hot key don't all hit the DB at once.
- [edge-04] OPEN: double-submission on client retry of `POST /order/create` isn't named as its own edge case, even though it's the concrete scenario the missing idempotency key (api-01) would cause.
- [edge-05] OPEN: "orders expired need to be removed from cache via eviction" has no prevention/mitigation detail — unclear if eviction is TTL-driven (matching the order's `expiration_type`), passive-on-read, or an active background sweep.
