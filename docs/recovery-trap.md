# Recovery-trap fixture walkthrough

[`fixtures/recovery-trap.json`](../fixtures/recovery-trap.json) is a synthetic
scenario: its prices are invented and are not historical observations, a
forecast, or investment advice. It compares a hold policy with a circuit
breaker on the same exogenous sequence; neither policy can see future prices.

## Scenario and provenance

- `schema_version: "0.1.0"` selects the existing scenario contract.
- `id` and `title` identify this fixture as `recovery-trap` / “Synthetic recovery
  trap.”
- `mode: "fixture"` selects the local deterministic simulator rather than an
  EVM run.
- `provenance.kind: "synthetic"` and its description explicitly identify the
  invented recovery path.

## Market assumptions

- `prices` is the invented observation path: 100, 97, 84, 83, 90, 104, 118,
  123, 129. These are observations in order, not claims about a real asset.
- `initial_cash: "0"` and `initial_units: "100"` start both policies with the
  same all-unit position. `symbol: "TEST"` is only a fixture label.
- `fee_bps: 30` means a 0.30% fee on a sale, and `slippage_bps: 20` means the
  simulated sale price is 0.20% below that observation. The engine applies both
  to the candidate's sale; this fixture does not model gas, liquidity, market
  impact, or MEV.

## Policies and qualitative outcome

The baseline is `hold`, so it keeps its 100 units throughout the observations.
The candidate is a `circuit_breaker` with `drawdown_trigger: "0.12"` (12%). The
engine compares the current observed price with the highest price seen so far:
`(peak_price - price) / peak_price`. When the path reaches 84 after a peak of
100, the drawdown is 16%, so the candidate sells before the later recovery in
the fixture. The later observations rise from 83 to 129, but the candidate has
already sold; the hold baseline remains exposed to the full path.

This is a qualitative reading of the fixture and the rule in the sibling
engine's [`fixture.py`](https://github.com/entrotter/engine/blob/main/src/entrotter_engine/fixture.py),
not a reported benchmark result. No performance number is claimed here. The
scenario is useful for inspecting how a simple drawdown trigger can exit before
a recovery, while also seeing that fees and slippage are explicit assumptions.
