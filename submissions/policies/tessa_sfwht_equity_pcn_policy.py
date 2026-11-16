"""
submissions/policies/tessa_sfwht_equity_pcn_policy.py
=====================================================
32-PCN Federation Policy (`batch_32pcn = True`) Combining `Tessa` Bipartite
Gray-Code / Scaled Fast Walsh-Hadamard (`sfwht`) Continuous Angle Compression
(`arXiv:2611.18440v1` Sec. 2.1) with an Exact Un-Compressed Binary Clinical
Safety Channel (`Core20` Interpreter + `HYP007` Frail `80+` Ceiling + `CQWM` Washout).

Demonstrates the constructive clinical rule for Era I/II hardware-native data loading:
  - Lossy `sfwht` threshold compression (`|alpha_j| < tau_rad -> 0`, cancelling ~35%+
    of 2-qubit CNOT gates in pairs) is safe on *continuous* pathway affinity weights,
  - PROVIDED discrete clinical safety invariants (`CLEAN_VERIFIED`, `Core20` interpreter,
    `HYP007 <= 150/90`, `CYP3A4` >=96h / >=48h washout holds) remain in an exact
    un-compressed channel.
"""

from __future__ import annotations

import math
from typing import Any, Mapping, Sequence


def _safe_menu(obs: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    """Exact un-compressed binary clinical safety channel (`0` Goodhart tolerance)."""
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


def _sfwht_compress_superpixel_16(values_16: Sequence[float], tau_rad: float = 0.03) -> list[float]:
    """
    Applies exact 4-address (`2^4 = 16`-slot) Tessa `sfwht` + Gray-code compression
    (`Eq. 2` of Bultrini, `arXiv:2611.18440v1`) to a 16-slot continuous affinity block.
    """
    vmin = min(values_16)
    vmax = max(values_16)
    span = max(1e-9, vmax - vmin)
    thetas = [math.pi * (float(v) - vmin) / span for v in values_16]

    grays = [j ^ (j >> 1) for j in range(16)]
    alphas = []
    for j in range(16):
        gj = grays[j]
        acc = 0.0
        for i in range(16):
            x = i & gj
            par = (x & 1) ^ ((x >> 1) & 1) ^ ((x >> 2) & 1) ^ ((x >> 3) & 1)
            acc += (-1.0 if par else 1.0) * thetas[i]
        ang = acc / 16.0
        alphas.append(0.0 if abs(ang) < tau_rad else ang)

    rec_vals: list[float] = []
    for i in range(16):
        acc_th = 0.0
        for j in range(16):
            x = i & grays[j]
            par = (x & 1) ^ ((x >> 1) & 1) ^ ((x >> 2) & 1) ^ ((x >> 3) & 1)
            acc_th += (-1.0 if par else 1.0) * alphas[j]
        th_clamped = min(math.pi, max(0.0, acc_th))
        rec_vals.append(vmin + span * (th_clamped / math.pi))
    return rec_vals


def _pathway_affinity(obs: Mapping[str, Any], k_dim: int, best_safe_yield: float) -> float:
    eq_debias = (1.12 / 0.96) if obs["is_core20_deprived"] else 1.04
    debiased_yield = best_safe_yield * eq_debias
    dw = float(obs["demand_weights"][k_dim])
    imd_norm = float(obs["imd_2025_score"]) / 45.0
    pmdi_norm = float(obs["propellant_pmdi_share_pct"]) / 100.0
    frail_norm = float(obs["frail_80plus_hyp_share"]) * 4.0

    bonus = 0.0
    if k_dim in (0, 2):
        bonus = 0.022 * frail_norm
    elif k_dim == 1:
        bonus = 0.020 * imd_norm
    elif k_dim == 3:
        bonus = 0.022 * pmdi_norm
    elif k_dim == 4:
        bonus = 0.032 * imd_norm
    elif k_dim == 5:
        bonus = 0.032 * pmdi_norm
    return debiased_yield * (0.93 + 0.07 * dw) + bonus


def propose(observations: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    best_by_pcn_k: dict[tuple[str, int], dict[str, Any]] = {}
    obs_by_code: dict[str, Mapping[str, Any]] = {}
    ordered_keys: list[tuple[str, int]] = []
    raw_flat: list[float] = []

    for obs in observations:
        code = str(obs["pcn_ods_code"])
        obs_by_code[code] = obs
        safe = _safe_menu(obs)
        for k_dim in range(6):
            cand_k = [c for c in safe if int(c["pathway_k"]) == k_dim]
            top_c = dict(max(cand_k, key=lambda x: float(x["observable_proxy_yield"])))
            best_by_pcn_k[(code, k_dim)] = top_c
            ordered_keys.append((code, k_dim))
            raw_flat.append(_pathway_affinity(obs, k_dim, float(top_c["observable_proxy_yield"])))

    # Encode all 32 x 6 = 192 continuous pathway affinities across 12 degree-4 Tessa super-pixels
    comp_flat: list[float] = []
    for start in range(0, len(raw_flat), 16):
        chunk = raw_flat[start : start + 16]
        if len(chunk) == 16:
            comp_flat.extend(_sfwht_compress_superpixel_16(chunk, tau_rad=0.03))
        else:
            comp_flat.extend(chunk)

    score_by_pcn_k = {k_pair: comp_flat[idx] for idx, k_pair in enumerate(ordered_keys)}

    unassigned = set(obs_by_code.keys())
    assignments: dict[str, dict[str, Any]] = {}
    counts = [0] * 6
    covered_peak = [0.0] * 6

    for _round in range(5):
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

    for code in sorted(unassigned):
        weakest_k = min(range(6), key=lambda k: (covered_peak[k], counts[k]))
        chosen = best_by_pcn_k[(code, weakest_k)]
        assignments[code] = chosen
        counts[weakest_k] += 1
        covered_peak[weakest_k] = max(covered_peak[weakest_k], float(chosen["observable_proxy_yield"]))

    return assignments


propose.batch_32pcn = True  # type: ignore[attr-defined]
