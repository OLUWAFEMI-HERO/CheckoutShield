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