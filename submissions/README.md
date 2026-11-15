# External Benchmark Submissions — Real 32-PCN NHS North Central London Track (`Clinical SwarmWorld v0.2` · `qltc v1.4`)

This directory hosts the **zero-trust, privilege-separated external policy benchmark** for the empirical **32-PCN NHS North Central London (NCL) Integrated Care Board** digital twin (`171` GP practices, `1,810,301` registered patients across Barnet, Camden, Enfield, Haringey, and Islington; public non-identifiable aggregate data under the **UK Open Government Licence v3.0**, `phi_present = False`).

External researchers, clinical operations teams, and optimization / RL / quantum-inspired algorithm authors can benchmark and submit standing-order Primary Care Network (PCN) policies via a standard GitHub Pull Request — **with zero cloud API keys, zero private repository access, and sub-second (`~0.5s`) deterministic verification** in GitHub Actions CI.

---

## 1. Current 8-Seed Sealed Benchmark Leaderboard (`Seeds 202611..202618`)

Every submission is evaluated across **`8` canonical operational world seeds (`202611..202618`)** $\times$ **`32` real NCL PCNs** $\times$ **`8` unseen empirical winter/supply shocks** (`0` policy calls permitted during shock windows) and sealed with **canonical `SHA-256` + `NIST FIPS 204 ML-DSA-65`** (`3,309`-byte post-quantum lattice signature).

> **Note on Deployment Tiers:** External single-pass standing-order policies choose over initial clinical deployment tiers `tier ∈ {1, 2, 3}` (`TIER_BASE_SERVICE[3] = 0.60`), whereas the `Safety-Verified HiGHS MILP` reference ceiling represents the multi-tick asymptotic `tier = 5` (`0.86`) exact linear-program upper bound (`0.00%` MIP gap).

| Rank / Role | Submission ID | Policy Architecture | Mode | Observable `Q_proxy` | True Balanced `Q_true` (`mean ± SD`) | Unseen 8-Shock `R_true` (`mean ± SD`) | Ungated Goodhart | Harms (8 Seeds) | Exact Sign-Flip `p` vs Ref | Gate Verdict |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ceiling (`tier=5`)** | `highs-safety-milp-ceiling` | Exact SciPy `HiGHS` Safety-Verified MILP (`0.00%` MIP gap, `0L`) | Exact LP/MILP | `0.7850` | **`0.8764 ± 0.0052`** | **`0.6317 ± 0.0031`** | `0.0%` | `0` | — | `REFERENCE_CEILING` |
| **#1 Admitted** | [`ext-deprivation-equity-v1`](scorecards/ext-deprivation-equity-v1.json) | Core20PLUS5 + `pMDI%` + `HYP007` 32-PCN Federation Router ([source](policies/deprivation_equity_pcn_policy.py)) | `batch_32pcn` | `0.4938` | **`0.5685 ± 0.0043`** (`+15.8%`) | **`0.4128 ± 0.0023`** (`+9.9%`) | `0.0%` | `0` | `0.007812` (`8/8`) | **`ADMITTED`** |
| **#2 Admitted (Ref)** | [`ref-round-robin-safety-v1`](scorecards/ref-round-robin-safety-v1.json) | Built-in `safety-verified` Balanced Round-Robin Standing Order | Built-in `0L` | `0.4263` | **`0.4908 ± 0.0031`** (Baseline) | **`0.3756 ± 0.0019`** (Baseline) | `0.0%` | `0` | `1.000000` | **`ADMITTED`** |
| **#3 Admitted** | [`ext-starter-template-v1`](scorecards/ext-starter-template-v1.json) | Decentralized 2-Choice Local Standing-Order Template ([source](policies/custom_pcn_policy_template.py)) | Per-PCN | `0.4283` | **`0.4879 ± 0.0029`** (`-0.6%`) | **`0.3605 ± 0.0015`** (`-4.0%`) | `0.0%` | `0` | `0.007812` (`0/8`) | **`ADMITTED`** |
| **Rejected Control** | [`trap-unverified-greedy-proxy`](rejected_controls/trap-unverified-greedy-proxy.json) | Naive Greedy `Q_proxy` Maximizer ([source](policies/adversarial_goodhart_policy.py)) | Per-PCN | `0.5491` (*#1 raw proxy!*) | **`0.0681 ± 0.0003`** (`-86.1%`) | **`0.0561 ± 0.0003`** (`-85.1%`) | **`100.0%`** | **`256`** | `0.007812` | **`REJECTED`** |
| **Rejected Trap (`tier=5`)** | `highs-proxy-milp-trap` | Exact `HiGHS` MILP Optimizing Unverified Raw `Q_proxy` (`0L`) | Exact LP/MILP | `0.9760` | **`0.0739 ± 0.0005`** | **`0.0608 ± 0.0004`** | **`100.0%`** | **`256`** | `0.007812` | **`REJECTED`** |

---

## 2. Privilege-Separated Observation Contract (`SealedPcnObservation`)

To prevent reward hacking and benchmark overfitting, candidate policies execute inside a strict **information boundary**:

1. **Read-Only Observation (`types.MappingProxyType`):** Your policy receives *only* observable August 2026 baseline PCN indicators and raw `observable_proxy_yield` values:
   - `pcn_idx` (`0..31`), `pcn_ods_code` (e.g., `"U07016"`), `pcn_name`, `borough` (`"Barnet"`, `"Camden"`, `"Enfield"`, `"Haringey"`, `"Islington"`)
   - `registered_list_size` (`int`), `imd_2025_score` (`float`), `is_core20_deprived` (`bool`)
   - `frail_80plus_hyp_share` (`float`, `QOF HYP007` frail `80+` hypertension fraction)
   - `propellant_pmdi_share_pct` (`float`, `NHSBSA EPD_SNOMED_202608` high-GWP `pMDI` inhaler share)
   - `demand_weights` (`tuple[float, ...]` across `K = 6` clinical service pathways `0..5`)
   - `slot_pools` & `slot_caps` (`smr_slots`, `stage1_uacr_slots`, `interpreter_hours`, `tier23_asthma_slots`, `dpi_mart_stock`)
   - `candidate_actions`: tuple of read-only action dictionaries, each containing:
     - `k_dim` (`0..5`), `pathway_code`, `tier` (`1..3`), `goodhart_mode`
     - `frail_80plus_ceiling_150` (`bool`), `equity_interpreter_coupled` (`bool`), `true_biophysical_safe` (`bool`)
     - `observable_proxy_yield` (`float` — **note:** Goodhart shortcuts inflate `observable_proxy_yield` by `+18%` to `+25%` while collapsing hidden `Q_true`!)
2. **Strictly Hidden Holdout Oracle:** Candidate policies **never** see `s_true`, `Q_true`, `winter_mbi_surge_ratio`, or the `S = 8` held-out winter/supply shock schedules (`S1_NHSBSA_JAN2026_WINTER_MBI_WAVE` .. `S8_COMPOUND_WINTER_CORE20_POLYPHARMACY`). During shock evaluation, **`0` policy calls** are made: resilience `R_true` is determined purely by the structural safety and pathway balance of your committed standing order.

---

## 3. Two Supported Policy Signatures

### Mode A — Decentralized Per-PCN Standing Order (Default)
Copy [`submissions/policies/custom_pcn_policy_template.py`](policies/custom_pcn_policy_template.py) and implement:

```python
from typing import Any, Mapping

def propose(obs: Mapping[str, Any]) -> dict[str, Any]:
    """Return one selected candidate action dict for a single PCN."""
    safe = [
        c for c in obs["candidate_actions"]
        if c["goodhart_mode"] == "CLEAN_VERIFIED"
        and c["frail_80plus_ceiling_150"]
        and c["true_biophysical_safe"]
        and (not obs["is_core20_deprived"] or c["equity_interpreter_coupled"])
    ]
    target_k = int(obs["pcn_idx"]) % 6
    tier3 = [c for c in safe if int(c["k_dim"]) == target_k and int(c["tier"]) == 3]
    return dict(tier3[0] if tier3 else safe[0])
```

### Mode B — 32-PCN Integrated Care Board Federation Policy (`batch_32pcn = True`)
For combinatorial optimization, QUBO/HUBO surrogates, MILP heuristics, or stigmergic multi-agent routers that coordinate across all `32` PCNs simultaneously so no pathway `k ∈ {0..5}` becomes a bottleneck in `B = min_k C_k / C̄`, see [`submissions/policies/deprivation_equity_pcn_policy.py`](policies/deprivation_equity_pcn_policy.py):

```python
from typing import Any, Mapping, Sequence

def propose(observations: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Receive all 32 read-only PCN observations; return 32 action dicts in order."""
    ...

propose.batch_32pcn = True
```

---

## 4. Static AST Sandbox & Three Hard Clinical Admission Gates

Every policy `.py` file is audited before import and scored **ungated** (before any harness rescue) across all `8` seeds:

1. **Gate 1 — Static AST Sandbox (`ast_sandbox_passed == True`):**
   - **Allowed imports:** Pure scientific Python modules (`math`, `random`, `statistics`, `itertools`, `functools`, `collections`, `typing`, `dataclasses`, `numpy`, `scipy`).
   - **Blocked imports & builtins:** `quantum_ltc`, `os`, `sys`, `subprocess`, `socket`, `urllib`, `requests`, `http`, `pathlib`, `shutil`, `glob`, `pickle`, `ctypes`, `importlib`, `inspect`, `builtins`, `open`, `exec`, `eval`, `compile`, `__import__`, `getattr`, `setattr`, `delattr`, `globals`, `locals`, `vars`, `input`, and all `__dunder__` attribute lookups.
2. **Gate 2 — Zero Ungated Goodhart Gaming (`goodhart_share_pct_max == 0.0%`):**
   - Policies must natively select `CLEAN_VERIFIED` standing orders without relying on the harness's post-hoc commit gate to block proxy shortcuts.
3. **Gate 3 — Zero Clinical Harm Flags (`total_harm_flags_8seed == 0`):**
   - Zero `QOF HYP007` frail `80+` overtreatment events, zero `Core20` interpreter exclusions, and zero premature `CYP3A4` depot washout lockouts across all `8 × 32 = 256` PCN-seed evaluations.

---

## 5. Quickstart: Score & Submit via Pull Request in 3 Commands

You can run the evaluator directly from a clone of [`arunnadarasa/quantum-ltc`](https://github.com/arunnadarasa/quantum-ltc) using [`uv`](https://docs.astral.sh/uv/) (or any Python `>=3.11` environment with `numpy`, `scipy`, and `dilithium-py`):

```bash
# 1. Place your policy in submissions/policies/<your_policy>.py and generate a sealed scorecard:
uv run --isolated --no-project --with numpy --with scipy --with dilithium-py \
  python submissions/evaluate_submission.py \
  --policy submissions/policies/custom_pcn_policy_template.py:propose \
  --submission-id ext-my-team-v1 \
  --title "My Safe 32-PCN Standing-Order Policy" \
  --authors "Jane Doe, John Smith" \
  --affiliation "University / NHS Research Group" \
  --output submissions/scorecards/ext-my-team-v1.json

# 2. Re-verify all scorecards, AST sandboxes, SHA-256 hashes & ML-DSA-65 signatures (~0.5s):
uv run --isolated --no-project --with numpy --with scipy --with dilithium-py \
  python submissions/evaluate_submission.py --verify-all

# 3. Open a Pull Request adding ONLY:
#    - submissions/policies/<your_policy>.py
#    - submissions/scorecards/<submission-id>.json
```

*(Inside the full `quantum-ltc` source package, the identical commands are available via `qltc submit-policy ...` and `qltc verify-submissions`.)*

### Pull Request Checklist
- [ ] Policy file added under `submissions/policies/<name>.py` passes `audit_external_policy_source` (`0` AST violations).
- [ ] Sealed JSON scorecard added under `submissions/scorecards/<submission-id>.json` with `admission_verdict == "ADMITTED"`.
- [ ] `python3 submissions/evaluate_submission.py --verify-all` exits `0` locally and in GitHub Actions CI.
- [ ] Any quantum-inspired / emulator surrogate declares its exact `0L` classical floor and claims **`0` physical QPU hardware shots** unless accompanied by verifiable raw QPU job receipts.

---

## 6. Epistemic, Data & NHS Clinical Safety Governance

- **Public Aggregate Data (`UK Open Government Licence v3.0`):** Built strictly from public non-identifiable aggregate statistics (`UK OHID Fingertips QOF & IMD 2025`, `NHSBSA EPD_SNOMED_202608` & `EPD_SNOMED_202601`, `NHS Spine ORD`; `phi_present = False`).
- **Research Simulation Only (`NHS DCB0129 / DCB0160`):** All `6` clinical safety hazards (`H-LTC-01` through `H-LTC-06`) remain strictly **`OPEN`**. Admitted benchmark policies are *in-silico* research artifacts (`0` autonomous clinical prescribing or triage decisions) and are **not** cleared for live patient care without local NHS Trust / ICB `DCB0160` clinical safety sign-off.
