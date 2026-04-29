# CheckoutShield

**Real-time checkout risk and fraud decisioning for e-commerce.**

CheckoutShield sits in the checkout path and returns an explainable risk
decision for a transaction in milliseconds — not just a score, but a
reason. A merchant calls the API at the moment of checkout and receives
one of three outcomes, backed by the specific signals that drove it:

| Decision | Meaning |
|---|---|
| `APPROVE` | Proceed with the transaction |
| `REVIEW` | Hold for manual or secondary review |
| `DECLINE` | Reject the transaction |

## Why this problem is hard

Fraud decisioning has to satisfy three things that pull against each
other: it has to be **fast** (a merchant's checkout can't stall waiting on
a risk decision), **accurate** (a false decline loses a legitimate sale; a
false approve loses money to fraud), and **explainable** (a merchant or
compliance reviewer needs to know *why* a transaction was declined, not
just that it was). CheckoutShield is built around that last constraint
specifically — every decision carries the signals that produced it, not
just a black-box number.

## Architecture

```
Merchant
   │
   ▼
CheckoutShield API  ──  receives a checkout transaction
   │
   ▼
Risk Service
   │
   ├── Risk Rules       ──  deterministic checks (e.g. velocity, geo/BIN mismatch)
   ├── Risk Scoring      ──  weighted/aggregate score across signals
   └── Decision Engine   ──  score + rules → APPROVE / REVIEW / DECLINE
   │
   ▼
Risk Decision  ──  returned to the merchant, with the signals behind it
```

> Fill in: which specific rules and scoring approach are implemented —
> the categories above (velocity, geo/BIN mismatch) are illustrative
> examples of what a system like this typically evaluates, not a claim
> about what's currently coded. Replace with the real rule set.

**Why this shape, not a single monolithic check:** separating *rules*
(deterministic, explainable, fast to reason about) from *scoring*
(aggregates weaker, probabilistic signals) from the *decision engine*
(the policy layer that turns both into one of three outcomes) means each
piece can be tested, tuned, and explained independently. A rule firing
is a concrete, auditable reason; a score crossing a threshold is a
policy decision — conflating them makes both harder to reason about and
harder to explain to a merchant asking "why was this declined?"

## Tech stack

| Component | Choice | Why |
|---|---|---|
| API framework | FastAPI | Async by default (checkout decisions are latency-sensitive), automatic OpenAPI/Swagger generation, Pydantic validation at the boundary |
| Primary datastore | PostgreSQL | Durable, queryable record of every transaction and decision — an audit trail a compliance reviewer can actually query |
| Fast-path store | Redis | Sub-millisecond reads for signals that need to be checked on every request without hitting Postgres — e.g. velocity/rate counters |
| Containerization | Docker / Docker Compose | One-command local environment matching how this would actually run |
| Testing | Pytest | — |

> Fill in: if there's a more specific reason for each choice in your
> actual implementation (e.g. a particular Redis data structure used for
> velocity counting, a specific reason for PostgreSQL over another
> relational store), that's worth stating explicitly here — a specific,
> considered reason reads far stronger than a generic one when this repo
> is being evaluated as evidence of technical judgment.

## API reference

### `POST /v1/risk/check`

Evaluates a checkout transaction and returns a risk decision.

<details>
<summary>Example request (illustrative — confirm against your actual schema)</summary>

```json
{
  "transaction_id": "txn_8f3a1c2e",
  "merchant_id": "merchant_001",
  "amount": 249.99,
  "currency": "GBP",
  "customer": {
    "email": "jane.doe@example.com",
    "ip_address": "203.0.113.42"
  },
  "payment": {
    "card_bin": "411111",
    "card_last4": "1111"
  },
  "billing_address": { "country": "GB", "postal_code": "SW1A 1AA" },
  "shipping_address": { "country": "GB", "postal_code": "SW1A 1AA" }
}
```
</details>

<details>
<summary>Example response (illustrative — confirm against your actual schema)</summary>

```json
{
  "transaction_id": "txn_8f3a1c2e",
  "decision": "REVIEW",
  "risk_score": 62,
  "signals": [
    { "rule": "velocity_check", "triggered": true, "detail": "4 transactions from this customer in the last 10 minutes" },
    { "rule": "billing_shipping_mismatch", "triggered": false, "detail": null }
  ],
  "evaluated_at": "2026-08-25T14:32:10Z"
}
```
</details>

> Fill in: the full, real request/response schema (every field FastAPI's
> Pydantic models actually define), and either link to `/docs` for the
> live schema or keep this section as a hand-maintained summary of it —
> pick one and keep it in sync, since a README that drifts from the real
> API is worse than no example at all.

Full interactive documentation — every field, every response code, "Try
it out" against a running instance — is auto-generated by FastAPI and
served at `/docs` once the API is running (see [Setup](#setup)).

## Setup

### Prerequisites

- Python 3.11+ (confirm your actual minimum version)
- Docker and Docker Compose (for the containerized path)
- PostgreSQL and Redis (only if running outside Docker — see below)

### Run locally

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Interactive API docs: **http://localhost:8000/docs**

### Run with Docker

```bash
docker compose up --build
```

> what `docker compose up` actually brings up — the API, and
> presumably Postgres + Redis alongside it. Worth listing each service
> and its port explicitly, since "it just works" is a weaker setup
> section than "here's exactly what starts and where."

### Configuration

> database
> URL, Redis URL, any API keys or thresholds), ideally with a
> `.env.example` file in the repo this section links to.

### Running the tests

```bash
pytest
```

> Fill in: what the test suite actually covers — rule-level unit tests,
> API-level integration tests, anything exercising the Postgres/Redis
> dependencies specifically. If there's a meaningful split (e.g. fast
> unit tests vs. tests that need Docker services running), say so and
> give the commands for each — this is the section an evaluator will use
> to decide whether to trust the rest of the README's claims.

## Project structure

```
app/
├── main.py              # FastAPI app entrypoint
├── api/                 # Route handlers
├── risk/
│   ├── rules.py         # Deterministic risk rules
│   ├── scoring.py       # Aggregate risk scoring
│   └── decision.py      # Rules + score → decision
├── models/               # Pydantic request/response schemas
├── db/                   # PostgreSQL access layer
└── cache/                 # Redis access layer
tests/
docker-compose.yml
requirements.txt
```

> This is an illustrative, typical FastAPI layout — replace with your
> actual directory tree (`tree -L 2` or equivalent) so it matches the
> real repo exactly. A structure section that doesn't match the actual
> layout is worse than omitting it.

## Design decisions & trade-offs

> This is the section worth investing the most in if this repo is being
> used as technical evidence for an application — it's where you show
> judgment, not just output. A few prompts, in the same spirit as the
> architecture reasoning above:
>
> - Why explainable signals, not just a score? (Already touched on
>   above — expand with a concrete example of a decision your system can
>   explain that a pure ML black-box score couldn't.)
> - **Why Redis specifically for velocity/fast-path checks, and what's
>   the actual data structure** (sorted set with a sliding window? a
>   simple TTL'd counter?) **and why that one?**
> - **How is a decision timeout or a downstream failure handled** — if
>   Postgres or Redis is slow or unavailable, does the system fail open
>   (approve by default) or fail closed (decline/review by default)?
>   This is a real design decision with a real trade-off (availability
>   vs. risk exposure) and a strong thing to have an explicit, reasoned
>   answer for.
> - What's NOT built, on purpose — e.g. no ML model (rules/scoring
>   only), no merchant-configurable rule thresholds, no async/webhook
>   decision path for slower checks. Naming scope boundaries explicitly
>   is a strength, not an admission of incompleteness — see the note on
>   this in the trade-offs sections of the other projects in this
>   engagement, if useful as a reference for tone.

## What's next - below to be developed in next release

> real time ML scoring component
> alongside the rules engine, per-merchant configurable rule weights, a
> feedback loop from confirmed-fraud outcomes back into scoring,
> webhook-based async decisions for checks that can't complete in the
> synchronous request window.

## License

> To be added.