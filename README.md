# Entrotter Scenarios

Open, versioned inputs and schemas for reproducible agent stress tests. MIT.
The easiest place to contribute is a new scenario and its evidence.

| Input | Type | Status |
| --- | --- | --- |
| `fixtures/liquidity-shock.json` | Invented price path | Offline runnable |
| `fixtures/recovery-trap.json` | Invented recovery path | Offline runnable; candidate can underperform |
| `fixtures/depeg-stress.json` | Invented depeg-shaped path | Offline runnable; not historical USDC data |
| `evm/local-branch-revert.json` | Local native transfers and REVERT bytecode | Verified with Anvil v1.8.3 |
| `evm/ethereum-state-fork.json` | Archived-block execution template | Native fork executed; use the pinned Uniswap case below for token evidence |

See the [recovery-trap walkthrough](docs/recovery-trap.md) for a field-by-field
explanation of the synthetic recovery fixture.

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

## Verified pinned Uniswap intervention

`evm/ethereum-uniswap-slippage.json` starts two isolated forks at Ethereum block
19,000,000, hash `0xcf384012b91b081230cdf17a3f7dd370d8e67056058af6b272b3d54aa2714fac`.
Both actors start with an overridden 10 ETH and wrap 1 ETH into WETH. Both approve
exactly 1 WETH to the legacy Uniswap v3 SwapRouter. The baseline swaps with no
output floor; the candidate demands an intentionally impossible 1,000,000 USDC.
This is a controlled intervention, not a recovered historical decision.

The baseline produced 2,556.134769 USDC; the candidate reverted, retained 1 WETH,
and paid gas. No asset valuation, future price path or portfolio profit is claimed.
The `tracked_tokens` optional v0.1 extension pins decimals and records raw balances.
Use the engine commit linked in the workspace release evidence; older engines
reject unknown fields. All original v0.1 examples remain unchanged.

From the six-checkout workspace, with Foundry v1.8.3 on PATH:

```bash
# Set an archive-capable URL privately; never commit provider credentials.
export ENTROTTER_RPC_URL=https://eth.drpc.org
PYTHONPATH=engine/src python3 entrotter/scripts/check_historical.py
```

This public endpoint served the archived state during verification; availability
and limits may change. PublicNode returned the header but pruned state and failed
explicitly. No substitute fixture was used. On macOS Python installations missing
a certificate chain, use the trusted system bundle via
`SSL_CERT_FILE=/etc/ssl/cert.pem`; never disable TLS verification.

Contract references: [Uniswap deployments](https://developers.uniswap.org/docs/protocols/v3/deployments/v3-ethereum-deployments)
and [Circle USDC addresses](https://developers.circle.com/stablecoins/usdc-contract-addresses).
Source, full receipts, two-run equality and measured runtime are stored in the
[workspace evidence](https://github.com/entrotter/entrotter/tree/main/evidence).
This one case is not a three-scenario benchmark or an untouched holdout.
