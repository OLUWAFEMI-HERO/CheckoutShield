# CheckoutShield

Real-time checkout risk and fraud decisioning platform for e-commerce.

CheckoutShield provides an API that allows merchants to submit checkout
transactions and receive an explainable risk decision:

- APPROVE
- REVIEW
- DECLINE

## Architecture

```text
Merchant
   |
   v
CheckoutShield API
   |
   v
Risk Service
   |
   +-- Risk Rules
   |
   +-- Risk Scoring
   |
   +-- Decision Engine
   |
   v
Risk Decision
```
## Technology
Python
FastAPI
PostgreSQL
Redis
Docker
Pytest
Run locally
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --reload

## Swagger:

http://localhost:8000/docs

## Run with Docker
docker compose up --build


##  Tests
pytest
Example
POST /v1/risk/check

## 
The service evaluates transaction signals and returns an explainable risk score
and decision.

---


