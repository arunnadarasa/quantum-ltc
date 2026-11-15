"""
Reference External Submission: Core20PLUS5 Deprivation, Propellant pMDI & Frailty-Matched
32-PCN Federation Router (`batch_32pcn = True`).

Grounded in the two empirical North Central London NHS structural poles uncovered in `Clinical SwarmWorld v0.2`:
  1. High-Deprivation Core20 Pole (Haringey/Enfield/Islington; `IMD 2025` up to `42.59`, `pMDI%` up to `81.6%`):
     prioritized for `k=4` (`CORE20_INTERPRETER_UACR`) and `k=5` (`NETZERO_DPI_MART_SWITCH`).
  2. Older Frail Hypertension & Polypharmacy Pole (Barnet/West Camden; high `HYP007` `80+` share):
     prioritized for `k=0` (`RTV_DEPOT_GUARD` >=96h hold) and `k=2` (`HTN_AKI_TRIPLE_WHAMMY` `HYP007 <=150/90`).
"""

from typing import Any, Mapping, Sequence


def _safe_menu(obs: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    out: list[Mapping[str, Any]] = []
    for c in obs["candidate_actions"]:
        k_dim = int(c["pathway_k"])
        hold_h = int(c["hold_hours_param"])
        if (
            c["goodhart_mode"] == "CLEAN_VERIFIED"
            and c["frail_80plus_ceiling_150"]
            and c["equity_interpreter_coupled"]
            and (k_dim != 0 or hold_h >= 96)
            and (k_dim != 1 or hold_h >= 48)
        ):
            out.append(c)
    return out


def _pathway_affinity(obs: Mapping[str, Any], k_dim: int, best_safe_yield: float) -> float:
    """Combines equity-debiased observable yield with Core20/IMD, pMDI%, and 80+ frailty indicators."""
    eq_debias = (1.12 / 0.96) if obs["is_core20_deprived"] else 1.04
    debiased_yield = best_safe_yield * eq_debias
    dw = float(obs["demand_weights"][k_dim])
    imd_norm = float(obs["imd_2025_score"]) / 45.0
    pmdi_norm = float(obs["propellant_pmdi_share_pct"]) / 100.0
    frail_norm = float(obs["frail_80plus_hyp_share"]) * 4.0

    bonus = 0.0
    if k_dim == 0:
        bonus = 0.02 * frail_norm
    elif k_dim == 1:
        bonus = 0.02 * imd_norm
    elif k_dim == 2:
        bonus = 0.02 * frail_norm
    elif k_dim == 3:
        bonus = 0.02 * pmdi_norm
    elif k_dim == 4:
        bonus = 0.03 * imd_norm
    elif k_dim == 5:
        bonus = 0.03 * pmdi_norm
    return debiased_yield * (0.94 + 0.06 * dw) + bonus


def propose(observations: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    """
    Federation-level 32-PCN router (`propose.batch_32pcn = True`):
    Assigns at least 5 PCNs per clinical pathway `k in 0..5` in descending order of safe
    epidemiological affinity so balanced `K = 6` coverage endures unseen winter/supply shocks.
    """
    best_by_pcn_k: dict[tuple[str, int], dict[str, Any]] = {}
    score_by_pcn_k: dict[tuple[str, int], float] = {}
    obs_by_code: dict[str, Mapping[str, Any]] = {}

    for obs in observations:
        code = str(obs["pcn_ods_code"])
        obs_by_code[code] = obs
        safe = _safe_menu(obs)
        for k_dim in range(6):
            cand_k = [c for c in safe if int(c["pathway_k"]) == k_dim]
            top_c = dict(max(cand_k, key=lambda x: float(x["observable_proxy_yield"])))
            best_by_pcn_k[(code, k_dim)] = top_c
            score_by_pcn_k[(code, k_dim)] = _pathway_affinity(
                obs, k_dim, float(top_c["observable_proxy_yield"])
            )

    unassigned = set(obs_by_code.keys())
    assignments: dict[str, dict[str, Any]] = {}
    counts = [0] * 6
    covered_peak = [0.0] * 6

    # Round-robin across the 6 NCL pathways so every pathway secures its top-5 anchor PCNs (30 of 32 PCNs)
    for _round in range(5):
        # Prioritize pathways with lowest current peak yield first
        pathway_order = sorted(range(6), key=lambda k: (covered_peak[k], k))
        for k_dim in pathway_order:
            if not unassigned:
                break
            best_code = max(
                unassigned,
                key=lambda code: (score_by_pcn_k[(code, k_dim)], -int(obs_by_code[code]["pcn_idx"])),
            )
            chosen = best_by_pcn_k[(best_code, k_dim)]
            assignments[best_code] = chosen
            unassigned.remove(best_code)
            counts[k_dim] += 1
            covered_peak[k_dim] = max(covered_peak[k_dim], float(chosen["observable_proxy_yield"]))

    # Assign remaining 2 PCNs to whichever pathway currently has the lowest peak yield
    for code in sorted(unassigned):
        weakest_k = min(range(6), key=lambda k: (covered_peak[k], counts[k]))
        chosen = best_by_pcn_k[(code, weakest_k)]
        assignments[code] = chosen
        counts[weakest_k] += 1
        covered_peak[weakest_k] = max(covered_peak[weakest_k], float(chosen["observable_proxy_yield"]))

    return assignments


propose.batch_32pcn = True
