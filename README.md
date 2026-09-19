# Entrotter Scenarios

Open, versioned inputs and schemas for reproducible agent stress tests. MIT.
The easiest place to contribute is a new scenario and its evidence.

| Input | Type | Status |
| --- | --- | --- |
| `fixtures/liquidity-shock.json` | Invented price path | Offline runnable |
| `fixtures/recovery-trap.json` | Invented recovery path | Offline runnable; candidate can underperform |
| `fixtures/depeg-stress.json` | Invented depeg-shaped path | Offline runnable; not historical USDC data |
| `evm/local-branch-revert.json` | Local native transfers and REVERT bytecode | Requires Anvil integration validation |
| `evm/ethereum-state-fork.json` | Archived-block execution template | Requires archive RPC and real execution validation |

Every fixture has a provenance kind, description, baseline and candidate
policy, costs and an explicit observation sequence. Money is serialized as
decimal strings, not binary floats. Strategies never receive future prices.

Schemas describe the wire format. The engine enforces additional semantic
constraints such as target allowlists, positive prices, integer wei, limits and
mode-specific fields. Neither schema validity nor a content hash proves the
economic model correct.

To validate (requires the sibling engine and development-only jsonschema):

```bash
PYTHONPATH=../engine/src python3 -m unittest discover -s tests -v
```

A historical contribution must include a permitted source, chain ID, pinned
block number and hash, affected contract addresses, source timestamps, archive
requirements, assumptions and a runnable acceptance test. Do not label a
synthetic or retrospectively informed policy as a historical backtest.

Do not change fixture inputs to improve displayed scores. Add train/test splits
and untouched holdout scenarios before comparing tuned agents. PRs that show
failure cases are as valuable as favorable demonstrations.
