# SSR.FUN Solana Protocol & Token-2022 Security Audit

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Chain: Solana Mainnet](https://img.shields.io/badge/Solana-Mainnet--Beta-9945FF.svg)](SSRFUN_AUDIT_REPORT.md)
[![Live Showcase](https://img.shields.io/badge/GitHub_Pages-Audit_Showcase-0ea5e9.svg)](https://khanhtnq.github.io/ssrfun-beta-security-audit/)

Independent reverse-engineering, on-chain account verification, and security invariant audit of the **SSR.FUN** (`ssr_protocol`) Solana Anchor smart contract and **SPL Token-2022 `TransferFeeConfig`** integration, accompanied by reproducible Python verification utilities.

Full technical report: **[`SSRFUN_AUDIT_REPORT.md`](SSRFUN_AUDIT_REPORT.md)**

---

## Audited On-Chain Scope

- **Anchor Program ID:** `8hTW7fHwn8t8hcgTVeyAhHMiCTHGUP3783NWUTBBFwH9`
- **Upgradeable ProgramData Account:** `2YF7aofgPbNj96pJJh1uzLtCk4H2fUq1FVLxFf9TAwow` (`1,772,165` bytes ELF binary)
- **Token Standard:** SPL Token-2022 (`TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`) with `TransferFeeConfig` (`15` bps / `0.15%`)
- **Resolved On-Chain Account Discriminators (`674` Mainnet Accounts):**
  - `ProtocolConfig` (`cf5bfa1c98b3d7d1`)
  - `Reserve` (`2bf2ccca1af73b7f`)
  - `ReserveAsset` (`22f692fa870f4022`)
  - `TradeTax` (`cfd849462c1ce954`)
  - `ManagerFeeRecipients` (`6b591e426c26219c`)
  - `FeeSettlement` (`c1c6d31d0b62c3e5`)

---

## Summary of Key Security Findings

1. **SPL Token-2022 Ceiling-Division Micro-Transfer Fee Trap & Off-Chain Float Drift:**
   - On-chain `TransferFeeConfig` computes $\text{Fee} = \lfloor (\text{Amount} \times 15 + 9,999) / 10,000 \rfloor$, confiscating `100%` of `1`-unit micro-transfers and causing `1`-unit off-chain JS float floor mismatches (`ZeroAmountAfterFeesOrRounding` / `SlippageMinOutputNotMet`).
2. **Unaborted Async Polling Race Condition (`leaderboard-lvjdhEed.js`):**
   - `setInterval(..., 60_000)` dispatches `fetch('/api/mainnet/campaign-leaderboard', { cache: 'no-store' })` without an `AbortController`, allowing delayed responses to overwrite newer UI state.
3. **30x Redundant API Polling Cadence:**
   - Client polls every `60s` against a backend dataset that refreshes every `30m` (`29/30` redundant requests).
4. **Trailing-4 Base58 Vanity Address Spoofing (`e.slice(-4)`):**
   - Truncating trader addresses to only 4 trailing Base58 characters ($58^4 \approx 1.13 \times 10^7$ trials, `< 2s` on consumer GPUs) enables leaderboard lookalike spoofing; remediated via `${e.slice(0, 4)}…${e.slice(-4)}`.

---

## Reproducible Verification Utilities

- `analyze_elf.py` / `check_discriminators.py`: Extracts Anchor 8-byte SHA-256 account & instruction discriminators from the `ssr_protocol` ELF binary.
- `check_fee_math.py` / `parse_tax_tx.py`: Reproduces SPL Token-2022 `HarvestWithheldTokensToMint` + `WithdrawWithheldTokensFromMint` ceiling fee arithmetic against mainnet transaction receipts.
- `query_solana_accounts.py`: Queries on-chain `ProtocolConfig`, `Reserve`, and `FeeSettlement` state layouts.

---

## License

Released under the [MIT License](LICENSE).
