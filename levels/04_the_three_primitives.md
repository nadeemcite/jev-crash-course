# Level 4 — The Three Primitives

Every question you ask Jev is one of exactly three types. This is the whole
vocabulary — once these three click, you understand the entire API surface.

## 1. `noul` — a yes/no belief

Answers "how likely is this true?" as a single probability between 0 and 1.
There's no separate `confidence` field for `noul` — as one write-up put it,
**"the number *is* the belief."**

Request fragment:
```json
{
  "is_urgent": {
    "type": "noul",
    "instructions": "Does the message convey urgency?"
  }
}
```

Real response (verified against the live API):
```json
{ "is_urgent": { "type": "noul", "noul": 0.98 } }
```

## 2. `choice` — pick one of up to 255 options

Answers "which of these categories fits?" Returns the winning option, a
confidence score, and the **full probability distribution** over every
option you defined — not just the winner.

Request fragment:
```json
{
  "department": {
    "type": "choice",
    "instructions": "Which team should handle this?",
    "criteria": {
      "billing": "Payments, invoicing, refunds",
      "technical": "Bugs, outages, integrations",
      "sales": "Pricing, upgrades, new accounts"
    }
  }
}
```

Real response:
```json
{
  "department": {
    "type": "choice",
    "choice": "billing",
    "confidence": 0.78,
    "probabilities": { "sales": 0.0, "technical": 0.15, "billing": 0.85 }
  }
}
```

Note `confidence` (0.78) and the winning probability (0.85) are related but
not identical — confidence reflects how *separated* the winner is from the
runner-up, not just its raw probability.

## 3. `score` — a position on an ordered scale

Answers "where does this fall on a scale?" `criteria` must be a **list** of
2–10 ordered labels (low → high). Returns a probability-weighted score
(so it can land *between* levels, e.g. `3.9`), a confidence value, a
`legend` mapping each level's index to its label, and the full probability
distribution across levels.

Request fragment:
```json
{
  "frustration": {
    "type": "score",
    "instructions": "How frustrated is the customer, from calm to extremely angry?",
    "criteria": ["calm", "mildly annoyed", "annoyed", "angry", "extremely angry"]
  }
}
```

Real response:
```json
{
  "frustration": {
    "type": "score",
    "score": 3.9,
    "confidence": 0.92,
    "legend": { "0": "calm", "1": "mildly annoyed", "2": "annoyed", "3": "angry", "4": "extremely angry" },
    "probabilities": { "0": 0.0, "1": 0.0, "2": 0.0, "3": 0.09, "4": 0.91 }
  }
}
```

> ⚠️ **Gotcha found while building this course:** `score` criteria must be a
> **list** (`["calm", "annoyed", ...]`), not a dict of `{level: label}`.
> Sending a dict returns a `422` with `"Input should be a valid list"`. Some
> third-party write-ups show dict-shaped examples — trust the shapes above,
> they're verified against the live API.

## Asking multiple questions in one call

All three question types can be mixed in a single request against a single
`state`, and — because Jev evaluates them in parallel rather than one after
another — **adding more questions barely changes response time.** This is
the basis of the "speculative fan-out" pattern in
[Level 8](08_confidence_gating_best_practices.md): ask everything you might
need up front, since it's nearly free.

Next: **[Level 5 — The Real API](05_the_real_api.md)**, where we make an
actual call using the `TYPESAFE_API_KEY` already sitting in your `.env`.
