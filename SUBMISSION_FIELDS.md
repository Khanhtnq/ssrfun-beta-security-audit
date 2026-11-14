# Superteam Earn Submission Fields: SSR.FUN Beta Audit ($50 USDC Zero-KYC)

**Platform:** Superteam Earn  
**Bounty:** SSR.FUN Beta Security & Architecture Audit  
**Reward:** $50 USDC (Zero-KYC Instant Payout)  
**Applicant Name:** Trần Ngọc Quốc Khánh (`Khanhtnq`)  
**Applicant Solana Wallet:** `6mghraUR9NV2fA187VXoLN2rVS3WLA91UhqLfjtvDdmf`  
**GitHub Identity:** `Khanhtnq <218711032+Khanhtnq@users.noreply.github.com>`  
**Report Artifact:** `SSRFUN_AUDIT_REPORT.md`

---

### Form Field 1: Audit Scope & Target Assets Verified
- **Target URLs:** `https://ssr.fun`, `https://ssr.fun/beta`, `https://ssr.fun/leaderboard`
- **Extracted Client Bundles:**
  - `beta-CH5hkIN6.js` (2,441 B)
  - `leaderboard-lvjdhEed.js` (3,447 B)
  - `core-DNPvxTZ8.js` (6,084 B, Kasada KPSDK anti-bot layer)
  - `modulepreload-polyfill-Dezn_h7o.js` (698 B)
- **Live Mainnet API:** `https://ssr.fun/api/mainnet/campaign-leaderboard`
- **Core Anchor Program ID:** `8hTW7fHwn8t8hcgTVeyAhHMiCTHGUP3783NWUTBBFwH9`
- **ProgramData Binary Account:** `2YF7aofgPbNj96pJJh1uzLtCk4H2fUq1FVLxFf9TAwow` (1,772,165 bytes ELF)

---

### Form Field 2: Key On-Chain & SPL Token-2022 Technical Findings
1. **Token-2022 TransferFeeConfig Parameterization:**
   - Program: `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`
   - Extension: `TransferFeeConfig` with `transferFeeBasisPoints = 15` (0.15% fee).
   - Authority: `5Wd7CVo1ysQ4DdivX4MmXT7UWzbMku6KSjW2S4mwZY75`.
   - Fee Collection Mechanism: Invokes `HarvestWithheldTokensToMint` -> `WithdrawWithheldTokensFromMint` -> `TransferChecked`.
2. **Ceiling Division Micro-Transfer Trap:**
   - Invariant: `Fee = (Amount * 15 + 9999) / 10000`.
   - Transfers $\le 666$ raw units incur an integer ceiling fee of 1 unit, creating a 100% tax on 1-unit transfers.
   - Off-chain float calculation causes 1-lamport discrepancies that trigger on-chain slippage reverts (`ZeroAmountAfterFeesOrRounding`).
3. **Anchor Account Discriminators & PDAs:**
   - `ProtocolConfig`: `cf5bfa1c98b3d7d1` (`5dhEfqb5wLy5yxZwYwZCXNsW2ALYoEbeYBfuR8B3ud88`)
   - `Reserve`: `2bf2ccca1af73b7f` (72 instances, e.g. Reserve 93 `FFPxPj1BaAPD8WuYpvnpReyUCYJZqA2pQxXH94yW7MVb`)
   - `TradeTax`: `cfd849462c1ce954`
   - `ManagerFeeRecipients`: `6b591e426c26219c`
   - `FeeSettlement`: `c1c6d31d0b62c3e5`
4. **Leaderboard Concurrency & Spoofing Flaws:**
   - Unsynchronized 60-second polling without `AbortController` causes race conditions under high network jitter.
   - Slicing only last 4 characters (`…${e.slice(-4)}`) enables trivial vanity lookalike impersonation on the public trader leaderboard.

---

### Form Field 3: Solana Payout Wallet Address
```
6mghraUR9NV2fA187VXoLN2rVS3WLA91UhqLfjtvDdmf
```
*(Zero-KYC Solana SPL USDC address)*
