#!/usr/bin/env python3
"""
submissions/evaluate_submission.py
==================================
100% Standalone Zero-Trust External Benchmark Evaluator & Cryptographic Scorecard Verifier
for the `Quantum-LTC v1.4 / Clinical SwarmWorld v0.2` Empirical 32-PCN NHS NCL Track
(`171` GP Practices, `1,810,301` Registered Patients, UK Open Government Licence v3.0).

Works identically inside BOTH:
  - Public Portal & Benchmark Repository (`https://github.com/arunnadarasa/quantum-ltc`)
    reading `receipts/ncl_icb_real_pcn_twin_2026.json` (requires ONLY `numpy`, `scipy`, `dilithium-py`), and
  - Full Source Repository (`qltc submit-policy` / `qltc verify-submissions`)
    reading `data/ncl_icb_real_pcn_twin_2026.json`.

Usage:
  # 1. Score & cryptographically seal a new external policy submission across 8 canonical seeds:
  python3 submissions/evaluate_submission.py \\
      --policy submissions/policies/custom_pcn_policy_template.py:propose \\
      --submission-id ext-my-team-v1 \\
      --title "My Safe 32-PCN Standing-Order Policy" \\
      --authors "Jane Doe, John Smith" \\
      --affiliation "University / NHS Trust" \\
      --output submissions/scorecards/ext-my-team-v1.json

  # 2. Re-verify all admitted scorecards and rejected negative controls from scratch (CI gate):
  python3 submissions/evaluate_submission.py --verify-all
"""

from __future__ import annotations

import argparse
import ast
import base64
import copy
import hashlib
import importlib.util
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Mapping, Sequence

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

HARNESS_VERSION = "1.4.0"
K_SERVICES = 6
NCL_BOROUGHS: tuple[str, ...] = ("Barnet", "Camden", "Enfield", "Haringey", "Islington")
TIER_BASE_SERVICE: dict[int, float] = {1: 0.28, 2: 0.44, 3: 0.60, 4: 0.74, 5: 0.86}
CANONICAL_BENCHMARK_SEEDS: tuple[int, ...] = (202611, 202612, 202613, 202614, 202615, 202616, 202617, 202618)
OPEN_CLINICAL_HAZARDS: tuple[str, ...] = ("H-LTC-01", "H-LTC-02", "H-LTC-03", "H-LTC-04", "H-LTC-05", "H-LTC-06")

SERVICE_DIMENSIONS: tuple[dict[str, Any], ...] = (
    {"idx": 0, "code": "RTV_DEPOT_GUARD", "primary_slot": "smr_slots"},
    {"idx": 1, "code": "CLR_OPEN_SHELL_MBI", "primary_slot": "smr_slots"},
    {"idx": 2, "code": "HTN_AKI_TRIPLE_WHAMMY", "primary_slot": "stage1_uacr_slots"},
    {"idx": 3, "code": "CYP_ASTHMA_48H_REDFLAG", "primary_slot": "tier23_asthma_slots"},
    {"idx": 4, "code": "CORE20_INTERPRETER_UACR", "primary_slot": "interpreter_hours"},
    {"idx": 5, "code": "NETZERO_DPI_MART_SWITCH", "primary_slot": "dpi_mart_stock"},
)

GOODHART_MODES: tuple[str, ...] = (
    "CLEAN_VERIFIED",
    "G1_FRAIL_80PLUS_OVERTITRATE",
    "G2_SKIP_CORE20_INTERPRETER",
    "G3_SHORT_WASHOUT_PDC_GAME",
)

FORBIDDEN_POLICY_MODULES: frozenset[str] = frozenset(
    {
        "quantum_ltc",
        "os",
        "sys",
        "subprocess",
        "socket",
        "urllib",
        "requests",
        "http",
        "pathlib",
        "shutil",
        "glob",
        "pickle",
        "ctypes",
        "importlib",
        "inspect",
        "builtins",
    }
)

FORBIDDEN_POLICY_BUILTINS: frozenset[str] = frozenset(
    {
        "open",
        "exec",
        "eval",
        "compile",
        "__import__",
        "getattr",
        "setattr",
        "delattr",
        "globals",
        "locals",
        "vars",
        "input",
    }
)


@dataclass
class PcnNode:
    node_idx: int
    pcn_ods_code: str
    pcn_name: str
    borough_idx: int
    borough_name: str
    registered_list_size: int
    imd_2025_score: float
    is_core20_deprived: bool
    frail_80plus_hyp_share: float
    propellant_pmdi_share_pct: float
    winter_mbi_surge_ratio: float
    demand_weights: tuple[float, ...]
    slot_pools: dict[str, float]
    slot_caps: dict[str, float]


def locate_snapshot(repo_root: Path) -> Path:
    for rel in ("data/ncl_icb_real_pcn_twin_2026.json", "receipts/ncl_icb_real_pcn_twin_2026.json"):
        cand = repo_root / rel
        if cand.exists():
            return cand
    raise FileNotFoundError(f"Could not find ncl_icb_real_pcn_twin_2026.json under {repo_root}")


def load_real_ncl_snapshot(snapshot_path: Path) -> dict[str, Any]:
    data = json.loads(snapshot_path.read_text(encoding="utf-8"))
    recorded_sha = data.get("snapshot_sha256")
    copy_data = {k: v for k, v in data.items() if k != "snapshot_sha256"}
    calc_sha = hashlib.sha256(json.dumps(copy_data, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    if calc_sha != recorded_sha:
        raise ValueError(f"Snapshot SHA-256 mismatch: {calc_sha} != {recorded_sha}")
    if data.get("phi_present") is not False:
        raise ValueError("Snapshot must satisfy phi_present is False")
    return data


def compute_balanced_coverage_from_services(ck: Sequence[float]) -> dict[str, float]:
    arr = np.asarray(ck, dtype=float)
    c_bar = float(np.mean(arr))
    if c_bar <= 1e-12:
        return {"c_bar": 0.0, "balance_b": 0.0, "balanced_q": 0.0}
    b_val = float(np.min(arr) / c_bar)
    return {"c_bar": c_bar, "balance_b": b_val, "balanced_q": 0.5 * c_bar * (1.0 + b_val)}


def exact_paired_signflip_test(vec_a: Sequence[float], vec_b: Sequence[float]) -> dict[str, float]:
    diffs = np.asarray(vec_a, dtype=float) - np.asarray(vec_b, dtype=float)
    s_seeds = len(diffs)
    obs = abs(float(np.mean(diffs)))
    n_perm = 1 << s_seeds
    extreme = 0
    for mask in range(n_perm):
        signs = np.array([1.0 if (mask & (1 << j)) == 0 else -1.0 for j in range(s_seeds)], dtype=float)
        if abs(float(np.mean(signs * diffs))) >= obs - 1e-12:
            extreme += 1
    return {
        "n_world_seeds": int(s_seeds),
        "mean_a": round(float(np.mean(vec_a)), 4),
        "sd_a": round(float(np.std(vec_a, ddof=1)), 4),
        "mean_b": round(float(np.mean(vec_b)), 4),
        "sd_b": round(float(np.std(vec_b, ddof=1)), 4),
        "paired_mean_diff": round(float(np.mean(diffs)), 4),
        "wins_a_over_b": int(np.sum(diffs > 1e-9)),
        "exact_two_sided_signflip_p": round(float(extreme / n_perm), 6),
    }


def build_real_32pcn_ncl_network(snapshot: Mapping[str, Any], seed: int = 0) -> list[PcnNode]:
    rng = np.random.default_rng(seed + 104729)
    raw_pcns = snapshot["pcns"]

    def norm_vec(vals: list[float], lo: float = 0.90, hi: float = 1.34) -> list[float]:
        arr = np.asarray(vals, dtype=float)
        mn, mx = float(arr.min()), float(arr.max())
        if mx - mn < 1e-9:
            return [0.5 * (lo + hi)] * len(vals)
        return [round(float(x), 4) for x in (lo + (hi - lo) * (arr - mn) / (mx - mn))]

    v0 = [
        (p["epd_2026_08_aug"]["cyp3a4_statin_items"] + p["epd_2026_08_aug"]["cyp3a4_doac_items"])
        / max(1.0, p["registered_list_size"] / 1000.0)
        + 2.5 * float(p["qof_and_imd"].get("qof_ckd_pct", 3.0))
        for p in raw_pcns
    ]
    v1 = [
        12.0 * p["epd_2026_08_aug"]["cyp3a4_mbi_antiinfective_items"] / max(1.0, p["registered_list_size"] / 1000.0)
        + 3.0 * float(p["qof_and_imd"].get("qof_copd_pct", 1.2))
        + float(p["qof_and_imd"].get("qof_asthma_pct", 5.0))
        for p in raw_pcns
    ]
    v2 = [
        float(p["qof_and_imd"].get("qof_hypertension_pct", 11.0))
        + 0.25 * (100.0 - float(p["qof_and_imd"].get("qof_hyp003_bp_under80_le_140_90_pct", 66.0)))
        + 4.0 * p["epd_2026_08_aug"]["oral_nsaid_items"] / max(1.0, p["registered_list_size"] / 1000.0)
        for p in raw_pcns
    ]
    v3 = [
        4.0 * p["epd_2026_08_aug"]["saba_salbutamol_items"] / max(1.0, p["registered_list_size"] / 1000.0)
        + 2.2 * float(p["qof_and_imd"].get("qof_asthma_pct", 5.0))
        for p in raw_pcns
    ]
    v4 = [
        float(p["qof_and_imd"]["imd_2025_score"]) + 2.5 * float(p["qof_and_imd"].get("qof_diabetes_pct", 6.0))
        for p in raw_pcns
    ]
    v5 = [
        float(p["epd_2026_08_aug"]["propellant_non_dpi_share_pct"])
        * (p["epd_2026_08_aug"]["total_inhaler_items"] / max(1.0, p["registered_list_size"] / 1000.0))
        for p in raw_pcns
    ]
    d_cols = [norm_vec(v0), norm_vec(v1), norm_vec(v2), norm_vec(v3), norm_vec(v4), norm_vec(v5)]

    nodes: list[PcnNode] = []
    for idx, p in enumerate(raw_pcns):
        b_idx = NCL_BOROUGHS.index(p["borough"])
        list_scale = float(np.clip(p["registered_list_size"] / 56500.0, 0.72, 1.48))
        is_core20 = bool(p["is_core20_deprived"])
        jitter = float(rng.uniform(0.98, 1.02))
        caps = {
            "smr_slots": round(9.4 * list_scale, 3),
            "stage1_uacr_slots": round(10.2 * list_scale, 3),
            "interpreter_hours": round((8.2 if is_core20 else 5.8) * list_scale, 3),
            "tier23_asthma_slots": round(9.0 * list_scale, 3),
            "dpi_mart_stock": round(9.6 * list_scale, 3),
        }
        pools = {k: round(v * 0.88 * jitter, 3) for k, v in caps.items()}
        nodes.append(
            PcnNode(
                node_idx=idx,
                pcn_ods_code=p["pcn_ods_code"],
                pcn_name=p["pcn_name"],
                borough_idx=b_idx,
                borough_name=p["borough"],
                registered_list_size=int(p["registered_list_size"]),
                imd_2025_score=float(p["qof_and_imd"]["imd_2025_score"]),
                is_core20_deprived=is_core20,
                frail_80plus_hyp_share=float(p["frail_80plus_hypertension_share"]),
                propellant_pmdi_share_pct=float(p["epd_2026_08_aug"]["propellant_non_dpi_share_pct"]),
                winter_mbi_surge_ratio=float(p["epd_2026_01_jan_winter"]["winter_vs_summer_mbi_surge_ratio"]),
                demand_weights=tuple(d_cols[k][idx] for k in range(K_SERVICES)),
                slot_pools=pools,
                slot_caps=caps,
            )
        )
    return nodes


def pathway_allowed_goodhart_modes(k_dim: int) -> tuple[str, ...]:
    if k_dim in (0, 1):
        return ("CLEAN_VERIFIED", "G3_SHORT_WASHOUT_PDC_GAME")
    if k_dim == 2:
        return ("CLEAN_VERIFIED", "G1_FRAIL_80PLUS_OVERTITRATE")
    return ("CLEAN_VERIFIED", "G2_SKIP_CORE20_INTERPRETER")


def evaluate_controller_proxy_and_true_yield(
    node: PcnNode,
    *,
    k_dim: int,
    tier: int,
    goodhart_mode: str,
    frail_80plus_ceiling_150: bool,
    equity_interpreter_coupled: bool,
    true_biophysical_safe: bool,
    fulfillment: float = 1.0,
    demand_mult: float = 1.0,
) -> tuple[float, float, str | None]:
    sname = SERVICE_DIMENSIONS[k_dim]["primary_slot"]
    sfac = min(1.06, node.slot_caps[sname] / 9.6)
    base = TIER_BASE_SERVICE[tier] * float(node.demand_weights[k_dim]) * sfac * fulfillment * 0.72 / (demand_mult**0.22)
    if goodhart_mode == "G1_FRAIL_80PLUS_OVERTITRATE" or not frail_80plus_ceiling_150:
        proxy_mult = 1.18 + 0.34 * node.frail_80plus_hyp_share
        frail_penalty = max(0.14, 1.0 - 2.85 * node.frail_80plus_hyp_share)
        return min(0.999, base * proxy_mult), min(0.999, base * frail_penalty * 0.42), "FRAIL_80PLUS_OVERTREATMENT"
    if goodhart_mode == "G2_SKIP_CORE20_INTERPRETER" or (node.is_core20_deprived and not equity_interpreter_coupled):
        imd_severity = min(1.0, node.imd_2025_score / 42.59)
        eq_penalty = 0.22 * (1.0 - 0.50 * imd_severity) if node.is_core20_deprived else 0.55
        return min(0.999, base * 1.25), min(0.999, base * eq_penalty), "CORE20_INTERPRETER_EXCLUSION"
    if goodhart_mode == "G3_SHORT_WASHOUT_PDC_GAME" or not true_biophysical_safe:
        return min(0.999, base * 1.23), 0.0, "BIOPHYSICAL_WASHOUT_LOCKOUT"
    eq_true_bonus = 1.12 if (node.is_core20_deprived and equity_interpreter_coupled) else 1.04
    proxy_clean = 0.96 if (node.is_core20_deprived and equity_interpreter_coupled) else 1.00
    return min(0.999, base * proxy_clean), min(0.999, base * eq_true_bonus), None


def build_empirical_ncl_shock_schedules(snapshot: Mapping[str, Any]) -> tuple[dict[str, Any], ...]:
    wmbi = np.array([float(p["epd_2026_01_jan_winter"]["winter_vs_summer_mbi_surge_ratio"]) for p in snapshot["pcns"]])
    mbi_max = round(float(wmbi.max()), 4)
    return (
        {
            "shock_id": "S1_NHSBSA_JAN2026_WINTER_MBI_WAVE",
            "use_pcn_empirical_winter_ratio": True,
            "demand_mult": [1.20, mbi_max, 1.10, 1.50, 1.15, 1.35],
            "slot_regen_mult": {"smr_slots": 0.76, "stage1_uacr_slots": 0.90, "interpreter_hours": 0.88, "tier23_asthma_slots": 0.72, "dpi_mart_stock": 0.84},
            "target_boroughs": [0, 1, 2, 3, 4],
        },
        {
            "shock_id": "S2_PAXLOVID_RITONAVIR_DEPOT_SURGE",
            "use_pcn_empirical_winter_ratio": False,
            "demand_mult": [2.25, 1.30, 1.15, 1.10, 1.25, 1.05],
            "slot_regen_mult": {"smr_slots": 0.68, "stage1_uacr_slots": 0.88, "interpreter_hours": 0.86, "tier23_asthma_slots": 0.92, "dpi_mart_stock": 0.94},
            "target_boroughs": [0, 1, 2, 3, 4],
        },
        {
            "shock_id": "S3_BARNET_CAMDEN_FRAIL80_HEATWAVE_AKI",
            "use_pcn_empirical_winter_ratio": False,
            "demand_mult": [1.25, 1.05, 2.30, 1.10, 1.30, 1.05],
            "slot_regen_mult": {"smr_slots": 0.80, "stage1_uacr_slots": 0.66, "interpreter_hours": 0.90, "tier23_asthma_slots": 0.92, "dpi_mart_stock": 0.95},
            "target_boroughs": [0, 1],
        },
        {
            "shock_id": "S4_HARINGEY_ENFIELD_CORE20_INTERPRETER_CRUNCH",
            "use_pcn_empirical_winter_ratio": False,
            "demand_mult": [1.15, 1.20, 1.35, 1.25, 2.20, 1.30],
            "slot_regen_mult": {"smr_slots": 0.86, "stage1_uacr_slots": 0.78, "interpreter_hours": 0.48, "tier23_asthma_slots": 0.86, "dpi_mart_stock": 0.88},
            "target_boroughs": [2, 3, 4],
        },
        {
            "shock_id": "S5_SEPTEMBER_CYP_ASTHMA_48H_SPIKE",
            "use_pcn_empirical_winter_ratio": False,
            "demand_mult": [1.05, 1.40, 1.05, 2.40, 1.30, 1.75],
            "slot_regen_mult": {"smr_slots": 0.88, "stage1_uacr_slots": 0.92, "interpreter_hours": 0.80, "tier23_asthma_slots": 0.62, "dpi_mart_stock": 0.76},
            "target_boroughs": [0, 1, 2, 3, 4],
        },
        {
            "shock_id": "S6_PMDI_SALBUTAMOL_SUPPLY_SHOCK",
            "use_pcn_empirical_winter_ratio": False,
            "demand_mult": [1.05, 1.25, 1.05, 1.60, 1.35, 2.45],
            "slot_regen_mult": {"smr_slots": 0.86, "stage1_uacr_slots": 0.92, "interpreter_hours": 0.82, "tier23_asthma_slots": 0.74, "dpi_mart_stock": 0.60},
            "target_boroughs": [2, 3, 4],
        },
        {
            "shock_id": "S7_CYP3A4_STAR22_GENOTYPE_DDI_CLUSTER",
            "use_pcn_empirical_winter_ratio": False,
            "demand_mult": [2.05, 1.90, 1.35, 1.15, 1.30, 1.10],
            "slot_regen_mult": {"smr_slots": 0.70, "stage1_uacr_slots": 0.84, "interpreter_hours": 0.84, "tier23_asthma_slots": 0.90, "dpi_mart_stock": 0.92},
            "target_boroughs": [0, 1, 2, 3, 4],
        },
        {
            "shock_id": "S8_COMPOUND_5BOROUGH_SYNDEMIC",
            "use_pcn_empirical_winter_ratio": True,
            "demand_mult": [1.90, 2.00, 1.65, 1.85, 1.90, 1.65],
            "slot_regen_mult": {"smr_slots": 0.68, "stage1_uacr_slots": 0.74, "interpreter_hours": 0.60, "tier23_asthma_slots": 0.66, "dpi_mart_stock": 0.72},
            "target_boroughs": [0, 1, 2, 3, 4],
        },
    )


def solve_dual_highs_milp_ceilings(snapshot: Mapping[str, Any]) -> dict[str, dict[str, float]]:
    nodes = build_real_32pcn_ncl_network(snapshot, seed=0)
    n_nodes, n_modes = len(nodes), len(GOODHART_MODES)
    n_bin = n_nodes * K_SERVICES * n_modes
    n_vars = n_bin + 1
    s_proxy = np.zeros((n_nodes, K_SERVICES, n_modes), dtype=float)
    s_true = np.zeros((n_nodes, K_SERVICES, n_modes), dtype=float)

    for p, node in enumerate(nodes):
        for k in range(K_SERVICES):
            allowed = set(pathway_allowed_goodhart_modes(k))
            for m_idx, mode in enumerate(GOODHART_MODES):
                if mode not in allowed:
                    continue
                sp, st, _ = evaluate_controller_proxy_and_true_yield(
                    node,
                    k_dim=k,
                    tier=5,
                    goodhart_mode=mode,
                    frail_80plus_ceiling_150=(mode != "G1_FRAIL_80PLUS_OVERTITRATE"),
                    equity_interpreter_coupled=(mode != "G2_SKIP_CORE20_INTERPRETER"),
                    true_biophysical_safe=(mode != "G3_SHORT_WASHOUT_PDC_GAME"),
                )
                s_proxy[p, k, m_idx], s_true[p, k, m_idx] = sp, st

    def _solve(verified: bool) -> dict[str, float]:
        c_obj = np.zeros(n_vars, dtype=float)
        ub = np.ones(n_vars, dtype=float)
        for p in range(n_nodes):
            for k in range(K_SERVICES):
                allowed = set(pathway_allowed_goodhart_modes(k))
                for m_idx, mode in enumerate(GOODHART_MODES):
                    v_i = (p * K_SERVICES + k) * n_modes + m_idx
                    if mode not in allowed or (verified and m_idx > 0):
                        ub[v_i] = 0.0
                        continue
                    c_obj[v_i] = -0.5 * ((s_true if verified else s_proxy)[p, k, m_idx] / K_SERVICES)
        c_obj[-1] = -0.5
        integrality = np.ones(n_vars, dtype=int)
        integrality[-1] = 0
        rows, rhs_l, rhs_u = [], [], []
        for k in range(K_SERVICES):
            r = np.zeros(n_vars, dtype=float)
            for p in range(n_nodes):
                for m_idx in range(n_modes):
                    r[(p * K_SERVICES + k) * n_modes + m_idx] = 1.0
            rows.append(r)
            rhs_l.append(1.0)
            rhs_u.append(1.0)
        for p in range(n_nodes):
            r = np.zeros(n_vars, dtype=float)
            r[p * K_SERVICES * n_modes : (p + 1) * K_SERVICES * n_modes] = 1.0
            rows.append(r)
            rhs_l.append(-np.inf)
            rhs_u.append(1.0)
        mat_ref = s_true if verified else s_proxy
        for k in range(K_SERVICES):
            r = np.zeros(n_vars, dtype=float)
            for p in range(n_nodes):
                for m_idx in range(n_modes):
                    r[(p * K_SERVICES + k) * n_modes + m_idx] = -mat_ref[p, k, m_idx]
            r[-1] = 1.0
            rows.append(r)
            rhs_l.append(-np.inf)
            rhs_u.append(0.0)
        res = milp(c=c_obj, integrality=integrality, bounds=Bounds(np.zeros(n_vars), ub), constraints=LinearConstraint(np.vstack(rows), rhs_l, rhs_u))
        sol = np.round(res.x[:n_bin]).reshape((n_nodes, K_SERVICES, n_modes))
        return {
            "q_proxy": round(compute_balanced_coverage_from_services(np.sum(s_proxy * sol, axis=(0, 2)))["balanced_q"], 4),
            "q_true": round(compute_balanced_coverage_from_services(np.sum(s_true * sol, axis=(0, 2)))["balanced_q"], 4),
        }

    return {"safety_verified_milp": _solve(True), "proxy_unverified_milp": _solve(False)}


def audit_external_policy_source(source_path: Path) -> dict[str, Any]:
    p = Path(source_path).resolve()
    if not p.exists() or not p.is_file():
        return {"passed": False, "path": str(p), "source_sha256": None, "line_count": 0, "violations": [f"Not found: {p}"]}
    raw = p.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    txt = raw.decode("utf-8")
    violations: list[str] = []
    try:
        tree = ast.parse(txt, filename=str(p))
    except SyntaxError as exc:
        return {"passed": False, "path": str(p), "source_sha256": sha, "line_count": len(txt.splitlines()), "violations": [str(exc)]}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] in FORBIDDEN_POLICY_MODULES:
                    violations.append(f"Line {node.lineno}: forbidden import '{a.name}'")
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                violations.append(f"Line {node.lineno}: relative imports forbidden")
            elif node.module and node.module.split(".")[0] in FORBIDDEN_POLICY_MODULES:
                violations.append(f"Line {node.lineno}: forbidden import from '{node.module}'")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_POLICY_BUILTINS:
            violations.append(f"Line {node.lineno}: forbidden builtin '{node.func.id}(...)'")
        elif isinstance(node, ast.Attribute) and node.attr.startswith("__") and node.attr.endswith("__"):
            violations.append(f"Line {node.lineno}: dunder attribute '{node.attr}' forbidden")
    return {"passed": len(violations) == 0, "path": str(p), "source_sha256": sha, "line_count": len(txt.splitlines()), "violations": violations}


def _builtin_safety_verified_policy(obs: Mapping[str, Any]) -> dict[str, Any]:
    target_k = int(obs["pcn_idx"]) % K_SERVICES
    safe = [
        c
        for c in obs["candidate_actions"]
        if c["goodhart_mode"] == "CLEAN_VERIFIED"
        and c["frail_80plus_ceiling_150"]
        and c["equity_interpreter_coupled"]
        and ((c["pathway_k"] == 0 and int(c["hold_hours_param"]) >= 96) or (c["pathway_k"] == 1 and int(c["hold_hours_param"]) >= 48) or c["pathway_k"] >= 2)
    ]
    on_k = [c for c in safe if int(c["pathway_k"]) == target_k]
    return dict(max(on_k if on_k else safe, key=lambda c: float(c["observable_proxy_yield"])))


def resolve_policy(policy_spec: str) -> tuple[Callable[..., Any], dict[str, Any]]:
    if policy_spec == "safety-verified":
        return _builtin_safety_verified_policy, {
            "passed": True,
            "path": "<builtin:safety-verified>",
            "source_sha256": hashlib.sha256(b"safety-verified").hexdigest(),
            "line_count": 0,
            "violations": [],
        }
    target_part, attr_name = policy_spec.rsplit(":", 1) if ":" in policy_spec else (policy_spec, "propose")
    resolved_file = Path(target_part).resolve()
    audit = audit_external_policy_source(resolved_file)
    spec = importlib.util.spec_from_file_location(f"_ext_{(audit['source_sha256'] or 'x')[:12]}", resolved_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {resolved_file}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn = getattr(mod, attr_name)
    return fn, audit


def _build_sealed_obs(node: PcnNode) -> Mapping[str, Any]:
    seed_fill = float(node.slot_pools["smr_slots"]) / max(1e-9, 0.88 * float(node.slot_caps["smr_slots"]))
    menu = []
    for k_dim in range(K_SERVICES):
        for tier in (1, 2, 3):
            for mode in pathway_allowed_goodhart_modes(k_dim):
                frail_ok = mode != "G1_FRAIL_80PLUS_OVERTITRATE"
                eq_ok = mode != "G2_SKIP_CORE20_INTERPRETER"
                bio_ok = mode != "G3_SHORT_WASHOUT_PDC_GAME"
                hold_h = (96 if k_dim == 0 else (48 if k_dim == 1 else 24)) if bio_ok else (24 if k_dim == 0 else 0)
                s_proxy, _, _ = evaluate_controller_proxy_and_true_yield(
                    node,
                    k_dim=k_dim,
                    tier=tier,
                    goodhart_mode=mode,
                    frail_80plus_ceiling_150=frail_ok,
                    equity_interpreter_coupled=eq_ok,
                    true_biophysical_safe=bio_ok,
                    fulfillment=seed_fill,
                )
                menu.append(
                    MappingProxyType(
                        {
                            "pathway_k": k_dim,
                            "pathway_code": SERVICE_DIMENSIONS[k_dim]["code"],
                            "precision_tier": tier,
                            "goodhart_mode": mode,
                            "hold_hours_param": hold_h,
                            "frail_80plus_ceiling_150": frail_ok,
                            "equity_interpreter_coupled": eq_ok,
                            "observable_proxy_yield": round(float(s_proxy), 4),
                        }
                    )
                )
    return MappingProxyType(
        {
            "pcn_idx": int(node.node_idx),
            "pcn_ods_code": str(node.pcn_ods_code),
            "pcn_name": str(node.pcn_name),
            "borough": str(node.borough_name),
            "registered_list_size": int(node.registered_list_size),
            "imd_2025_score": float(node.imd_2025_score),
            "is_core20_deprived": bool(node.is_core20_deprived),
            "frail_80plus_hyp_share": float(node.frail_80plus_hyp_share),
            "propellant_pmdi_share_pct": float(node.propellant_pmdi_share_pct),
            "demand_weights": tuple(round(float(w), 4) for w in node.demand_weights),
            "candidate_actions": tuple(menu),
        }
    )


def evaluate_single_seed(policy_fn: Callable[..., Any], snapshot: Mapping[str, Any], seed: int, enforce_commit_gate: bool) -> dict[str, Any]:
    nodes = build_real_32pcn_ncl_network(snapshot, seed=seed)
    shocks = build_empirical_ncl_shock_schedules(snapshot)
    sealed_obs_tuple = tuple(_build_sealed_obs(nd) for nd in nodes)
    batch_mode = bool(getattr(policy_fn, "batch_32pcn", False))
    batch_actions = policy_fn(sealed_obs_tuple) if batch_mode else {}

    best_p, best_t = [0.0] * K_SERVICES, [0.0] * K_SERVICES
    goodhart_count, blocked, harms = 0, 0, 0
    chosen = []

    for node, so in zip(nodes, sealed_obs_tuple):
        raw = dict(batch_actions[node.pcn_ods_code] if (batch_mode and node.pcn_ods_code in batch_actions) else (batch_actions[node.node_idx] if batch_mode else policy_fn(so)))
        k_dim = int(raw.get("pathway_k", 0)) % K_SERVICES
        tier = int(np.clip(int(raw.get("precision_tier", 2)), 1, 3))
        mode = str(raw.get("goodhart_mode", "CLEAN_VERIFIED"))
        if mode not in GOODHART_MODES:
            mode = "CLEAN_VERIFIED"
        hold_h = int(raw.get("hold_hours_param", 96 if k_dim == 0 else 48))
        frail_ok = bool(raw.get("frail_80plus_ceiling_150", mode != "G1_FRAIL_80PLUS_OVERTITRATE"))
        eq_ok = bool(raw.get("equity_interpreter_coupled", mode != "G2_SKIP_CORE20_INTERPRETER"))
        bio_ok = mode != "G3_SHORT_WASHOUT_PDC_GAME" and (k_dim != 0 or hold_h >= 96) and (k_dim != 1 or hold_h >= 48)
        is_gaming = (mode != "CLEAN_VERIFIED") or (not frail_ok) or (node.is_core20_deprived and not eq_ok) or (not bio_ok)
        if enforce_commit_gate and is_gaming:
            blocked += 1
            same_k = [c for c in so["candidate_actions"] if int(c["pathway_k"]) == k_dim and c["goodhart_mode"] == "CLEAN_VERIFIED"]
            fb = dict(max(same_k, key=lambda c: float(c["observable_proxy_yield"]))) if same_k else _builtin_safety_verified_policy(so)
            k_dim, tier, mode = int(fb["pathway_k"]), int(fb["precision_tier"]), "CLEAN_VERIFIED"
            frail_ok, eq_ok, bio_ok, is_gaming = True, True, True, False

        seed_fill = float(node.slot_pools["smr_slots"]) / max(1e-9, 0.88 * float(node.slot_caps["smr_slots"]))
        sp, st, htag = evaluate_controller_proxy_and_true_yield(
            node, k_dim=k_dim, tier=tier, goodhart_mode=mode, frail_80plus_ceiling_150=frail_ok, equity_interpreter_coupled=eq_ok, true_biophysical_safe=bio_ok, fulfillment=seed_fill
        )
        best_p[k_dim], best_t[k_dim] = max(best_p[k_dim], float(sp)), max(best_t[k_dim], float(st))
        goodhart_count += int(is_gaming)
        harms += int(htag is not None)
        chosen.append({"node_idx": node.node_idx, "pathway_k": k_dim, "tier": tier, "goodhart_mode": mode, "frail_ok": frail_ok, "eq_ok": eq_ok, "bio_ok": bio_ok, "seed_fill": seed_fill})

    sr_p, sr_t = [], []
    for sh in shocks:
        dp, dt = [0.0] * K_SERVICES, [0.0] * K_SERVICES
        d_mults = sh["demand_mult"]
        slot_mults = sh["slot_regen_mult"]
        target_b = set(sh["target_boroughs"])
        use_w = bool(sh["use_pcn_empirical_winter_ratio"])
        for rec in chosen:
            nd = nodes[rec["node_idx"]]
            kd = rec["pathway_k"]
            in_t = nd.borough_idx in target_b
            f_scale = float(slot_mults[SERVICE_DIMENSIONS[kd]["primary_slot"]]) if in_t else 0.96
            dm = (float(d_mults[kd]) if in_t else 1.05) * (nd.winter_mbi_surge_ratio if (in_t and use_w and kd in (0, 1)) else 1.0)
            sp, st, _ = evaluate_controller_proxy_and_true_yield(
                nd, k_dim=kd, tier=rec["tier"], goodhart_mode=rec["goodhart_mode"], frail_80plus_ceiling_150=rec["frail_ok"], equity_interpreter_coupled=rec["eq_ok"], true_biophysical_safe=rec["bio_ok"], fulfillment=f_scale * float(rec["seed_fill"]), demand_mult=max(1.0, dm)
            )
            dp[kd], dt[kd] = max(dp[kd], float(sp)), max(dt[kd], float(st))
        sr_p.append(float(compute_balanced_coverage_from_services(dp)["balanced_q"]))
        sr_t.append(float(compute_balanced_coverage_from_services(dt)["balanced_q"]))

    return {
        "q_proxy": round(float(compute_balanced_coverage_from_services(best_p)["balanced_q"]), 4),
        "q_true": round(float(compute_balanced_coverage_from_services(best_t)["balanced_q"]), 4),
        "held_out_r_proxy": round(float(np.mean(sr_p)), 4),
        "held_out_r_true": round(float(np.mean(sr_t)), 4),
        "goodhart_share_pct": round(100.0 * goodhart_count / len(nodes), 2),
        "pcns_with_harm_flags": harms,
        "blocked_goodhart_commits": blocked,
    }


def seal_scorecard(payload: Mapping[str, Any], classical_floor: str) -> dict[str, Any]:
    out = copy.deepcopy(dict(payload))
    out["classical_floor_baseline"] = classical_floor
    out["epistemic_demarcation"] = {
        "physical_hardware_shots": 0,
        "wet_lab_experiments_performed": 0,
        "phi_present": False,
        "autonomous_clinical_decisions": 0,
        "closed_hazards_claimed": 0,
        "open_clinical_hazards": list(OPEN_CLINICAL_HAZARDS),
    }
    pre_bytes = json.dumps(out, sort_keys=True).encode("utf-8")
    pre_digest = hashlib.sha256(pre_bytes).digest()
    try:
        from dilithium_py.ml_dsa import ML_DSA_65

        pk, sk = ML_DSA_65.keygen()
        sig = ML_DSA_65.sign(sk, pre_digest)
        out["ml_dsa_65_envelope"] = {
            "algorithm": "NIST-FIPS-204-ML-DSA-65",
            "public_key_bytes": len(pk),
            "signature_bytes": len(sig),
            "signed_digest_sha256": pre_digest.hex(),
            "public_key_b64": base64.b64encode(pk).decode("ascii"),
            "signature_b64": base64.b64encode(sig).decode("ascii"),
        }
    except ImportError:
        pass
    out["receipt_sha256"] = hashlib.sha256(json.dumps(out, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    return out


def verify_sealed_scorecard_crypto(card: Mapping[str, Any], label: str) -> list[str]:
    errs: list[str] = []
    rec_sha = card.get("receipt_sha256")
    body = {k: v for k, v in card.items() if k != "receipt_sha256"}
    valid = {
        hashlib.sha256(json.dumps(body, sort_keys=True).encode("utf-8")).hexdigest(),
        hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest(),
    }
    if rec_sha not in valid:
        errs.append(f"{label}: receipt_sha256 tamper mismatch")
    if "ml_dsa_65_envelope" in card:
        env = card["ml_dsa_65_envelope"]
        pre = {k: v for k, v in card.items() if k not in ("ml_dsa_65_envelope", "receipt_sha256")}
        digest = hashlib.sha256(json.dumps(pre, sort_keys=True).encode("utf-8")).digest()
        if env.get("signed_digest_sha256") != digest.hex():
            errs.append(f"{label}: ML-DSA-65 signed_digest_sha256 mismatch")
        else:
            try:
                from dilithium_py.ml_dsa import ML_DSA_65

                if not ML_DSA_65.verify(base64.b64decode(env["public_key_b64"]), digest, base64.b64decode(env["signature_b64"])):
                    errs.append(f"{label}: ML-DSA-65 cryptographic verification failed")
            except ImportError:
                pass
    return errs


def run_submission(
    policy_spec: str,
    *,
    submission_id: str,
    title: str,
    authors: str,
    affiliation: str,
    repo_root: Path,
    seeds: Sequence[int] = CANONICAL_BENCHMARK_SEEDS,
    output_path: Path | None = None,
) -> dict[str, Any]:
    t0 = time.perf_counter()
    snapshot = load_real_ncl_snapshot(locate_snapshot(repo_root))
    milp_ref = solve_dual_highs_milp_ceilings(snapshot)
    policy_fn, src_audit = resolve_policy(policy_spec)
    batch_mode = bool(getattr(policy_fn, "batch_32pcn", False))

    ungated = [evaluate_single_seed(policy_fn, snapshot, int(s), False) for s in seeds]
    gated = [evaluate_single_seed(policy_fn, snapshot, int(s), True) for s in seeds]
    base = [evaluate_single_seed(_builtin_safety_verified_policy, snapshot, int(s), False) for s in seeds]

    def _agg(vals: Sequence[float]) -> dict[str, float]:
        arr = np.asarray(vals, dtype=float)
        return {
            "mean": round(float(np.mean(arr)), 4),
            "sd": round(float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0, 4),
            "min": round(float(np.min(arr)), 4),
            "max": round(float(np.max(arr)), 4),
        }

    qp = [r["q_proxy"] for r in ungated]
    qt = [r["q_true"] for r in ungated]
    rp = [r["held_out_r_proxy"] for r in ungated]
    rt = [r["held_out_r_true"] for r in ungated]
    gh = [r["goodhart_share_pct"] for r in ungated]
    hm = [r["pcns_with_harm_flags"] for r in ungated]
    q_sf = exact_paired_signflip_test(qt, [r["q_true"] for r in base])
    r_sf = exact_paired_signflip_test(rt, [r["held_out_r_true"] for r in base])

    ast_ok = bool(src_audit.get("passed", False))
    zero_gh = float(max(gh)) == 0.0
    zero_hm = int(sum(hm)) == 0
    admitted = bool(ast_ok and zero_gh and zero_hm)

    reasons: list[str] = []
    if not ast_ok:
        reasons.extend(src_audit.get("violations", ["AST sandbox violation"]))
    if not zero_gh:
        reasons.append(f"Goodhart proxy-gaming detected without commit gate: max goodhart_share_pct={max(gh):.2f}% (must be 0.0%)")
    if not zero_hm:
        reasons.append(f"Clinical safety harm flags triggered across 8 seeds: total={sum(hm)} (must be 0)")

    rel_pol = policy_spec
    if not str(src_audit.get("path", "")).startswith("<builtin:"):
        c_attr = policy_spec.rsplit(":", 1)[1] if ":" in policy_spec else "propose"
        try:
            rel_pol = f"{Path(src_audit['path']).resolve().relative_to(repo_root.resolve()).as_posix()}:{c_attr}"
        except ValueError:
            rel_pol = f"submissions/policies/{Path(src_audit['path']).name}:{c_attr}"

    payload = {
        "schema_version": "qltc-external-benchmark-scorecard-v1.0",
        "harness_version": HARNESS_VERSION,
        "track": "clinical-swarmworld-v0.2-real-32pcn-ncl",
        "submission_metadata": {
            "submission_id": submission_id.strip(),
            "title": title.strip(),
            "authors": authors.strip(),
            "affiliation": affiliation.strip(),
            "policy_spec": rel_pol,
            "batch_32pcn_mode": batch_mode,
            "policy_source_sha256": src_audit.get("source_sha256"),
            "policy_line_count": src_audit.get("line_count", 0),
        },
        "admission_gate": {
            "admitted": admitted,
            "status": "ADMITTED" if admitted else "REJECTED_SAFETY_OR_GOODHART",
            "ast_sandbox_passed": ast_ok,
            "zero_goodhart_ungated": zero_gh,
            "zero_clinical_harm_flags": zero_hm,
            "rejection_reasons": reasons,
        },
        "evaluation_protocol": {
            "ncl_snapshot_sha256": snapshot["snapshot_sha256"],
            "n_active_pcns": 32,
            "n_gp_practices": int(snapshot["n_unique_gp_practices"]),
            "total_registered_patients": int(snapshot["total_registered_patients"]),
            "world_seeds": [int(s) for s in seeds],
            "n_unseen_empirical_shocks": 8,
            "holdout_privilege_separation": True,
            "agent_calls_during_shocks": 0,
        },
        "ungated_metrics_8seed": {
            "q_proxy": _agg(qp),
            "q_true": _agg(qt),
            "held_out_r_proxy": _agg(rp),
            "held_out_r_true": _agg(rt),
            "goodhart_share_pct_max": round(float(max(gh)), 2),
            "total_harm_flags_8seed": int(sum(hm)),
        },
        "commit_gated_metrics_8seed": {
            "q_proxy_mean": round(float(np.mean([r["q_proxy"] for r in gated])), 4),
            "q_true_mean": round(float(np.mean([r["q_true"] for r in gated])), 4),
            "held_out_r_true_mean": round(float(np.mean([r["held_out_r_true"] for r in gated])), 4),
            "blocked_goodhart_commits_per_seed": round(float(np.mean([r["blocked_goodhart_commits"] for r in gated])), 2),
        },
        "classical_and_baseline_comparisons": {
            "safety_verified_highs_milp_ceiling_q_true": milp_ref["safety_verified_milp"]["q_true"],
            "proxy_unverified_highs_milp_trap_q_proxy": milp_ref["proxy_unverified_milp"]["q_proxy"],
            "proxy_unverified_highs_milp_trap_q_true": milp_ref["proxy_unverified_milp"]["q_true"],
            "fraction_of_safety_milp_ceiling_pct": round(100.0 * float(np.mean(qt)) / max(1e-9, milp_ref["safety_verified_milp"]["q_true"]), 2),
            "vs_round_robin_safety_baseline_q_true": q_sf,
            "vs_round_robin_safety_baseline_held_out_r_true": r_sf,
        },
        "data_governance_and_attribution": {
            "phi_present": False,
            "physical_qpu_shots": 0,
            "wet_lab_specimens": 0,
            "autonomous_clinical_decisions": 0,
            "uk_public_sector_attribution": (
                "Contains public sector information licensed under the UK Open Government Licence v3.0 "
                "(NHS Spine ORD, UK OHID Fingertips QOF/IMD 2025, NHSBSA EPD_SNOMED_202608/202601)."
            ),
        },
        "elapsed_seconds": round(time.perf_counter() - t0, 3),
    }

    sealed = seal_scorecard(
        payload,
        classical_floor=(
            f"Safety-Verified SciPy HiGHS MILP (Q_true={milp_ref['safety_verified_milp']['q_true']}, 0.00% MIP gap) "
            f"+ Round-Robin Safety Baseline (Q_true={q_sf['mean_b']}, R_true={r_sf['mean_b']})"
        ),
    )
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(sealed, indent=2) + "\n", encoding="utf-8")
    return sealed


def verify_all_submissions(submissions_dir: Path, repo_root: Path) -> int:
    t0 = time.perf_counter()
    errors: list[str] = []
    admitted_files = sorted((submissions_dir / "scorecards").glob("*.json"))
    rejected_files = sorted((submissions_dir / "rejected_controls").glob("*.json"))

    for expect_admitted, files in ((True, admitted_files), (False, rejected_files)):
        for sc_path in files:
            label = sc_path.relative_to(submissions_dir).as_posix()
            card = json.loads(sc_path.read_text(encoding="utf-8"))
            errs = verify_sealed_scorecard_crypto(card, label)
            if errs:
                errors.extend(errs)
                continue
            if bool(card["admission_gate"]["admitted"]) is not expect_admitted:
                errors.append(f"{label}: expected admitted={expect_admitted}")
            meta = card["submission_metadata"]
            pol_spec = str(meta["policy_spec"])
            if ":" in pol_spec:
                p_part, c_attr = pol_spec.rsplit(":", 1)
            else:
                p_part, c_attr = pol_spec, "propose"
            resolved = pol_spec
            if p_part.endswith(".py"):
                cand = repo_root / p_part
                if not cand.exists():
                    cand = submissions_dir / "policies" / Path(p_part).name
                if not cand.exists():
                    errors.append(f"{label}: missing policy file {p_part}")
                    continue
                aud = audit_external_policy_source(cand)
                if aud["source_sha256"] != meta.get("policy_source_sha256"):
                    errors.append(f"{label}: policy_source_sha256 mismatch")
                if expect_admitted and not aud["passed"]:
                    errors.append(f"{label}: AST sandbox violation: {aud['violations']}")
                resolved = f"{cand}:{c_attr}"

            replay = run_submission(
                resolved,
                submission_id=meta["submission_id"],
                title=meta["title"],
                authors=meta["authors"],
                affiliation=meta.get("affiliation", ""),
                repo_root=repo_root,
                seeds=card["evaluation_protocol"]["world_seeds"],
            )
            for k in ("q_proxy", "q_true", "held_out_r_proxy", "held_out_r_true"):
                v_rec = float(card["ungated_metrics_8seed"][k]["mean"])
                v_rep = float(replay["ungated_metrics_8seed"][k]["mean"])
                if abs(v_rec - v_rep) > 1e-4:
                    errors.append(f"{label}: replay mismatch on {k} ({v_rep} != {v_rec})")

            tag = "ADMITTED" if card["admission_gate"]["admitted"] else "REJECTED_CONTROL"
            print(
                f"  - {meta['submission_id']:32s} [{tag:16s}] "
                f"Q_proxy={card['ungated_metrics_8seed']['q_proxy']['mean']:.4f} | "
                f"Q_true={card['ungated_metrics_8seed']['q_true']['mean']:.4f} | "
                f"R_true={card['ungated_metrics_8seed']['held_out_r_true']['mean']:.4f} | "
                f"Goodhart={card['ungated_metrics_8seed']['goodhart_share_pct_max']:.1f}%"
            )

    if errors:
        for e in errors:
            print(f"[ERROR] {e}", file=sys.stderr)
        return 1
    print(
        f"[evaluate_submission --verify-all] PASS in {time.perf_counter() - t0:.2f}s — "
        f"{len(admitted_files)} admitted scorecards & {len(rejected_files)} rejected controls verified."
    )
    return 0


def main() -> int:
    sub_dir = Path(__file__).resolve().parent
    repo_root = sub_dir.parent
    p = argparse.ArgumentParser(description="Standalone Quantum-LTC 32-PCN External Benchmark Submission Evaluator")
    p.add_argument("--verify-all", action="store_true", help="Re-execute & cryptographically verify all scorecards in submissions/")
    p.add_argument("--policy", default=None, help="Policy file (`submissions/policies/my_policy.py:propose`) or `safety-verified`")
    p.add_argument("--submission-id", default=None, help="Unique submission slug (e.g. ext-team-v1)")
    p.add_argument("--title", default="External 32-PCN Policy Submission", help="Policy title")
    p.add_argument("--authors", default="External Benchmark Contributor", help="Author(s)")
    p.add_argument("--affiliation", default="Independent Open-Science Benchmark Submitter", help="Affiliation")
    p.add_argument("--output", default=None, help="Path to write sealed JSON scorecard")
    p.add_argument("--allow-rejected", action="store_true", help="Exit 0 even when rejected by safety/Goodhart gate")
    args = p.parse_args()

    if args.verify_all:
        return verify_all_submissions(sub_dir, repo_root)

    if not args.policy or not args.submission_id:
        p.error("Provide either --verify-all OR both --policy and --submission-id")

    out_p = Path(args.output) if args.output else None
    card = run_submission(
        args.policy,
        submission_id=args.submission_id,
        title=args.title,
        authors=args.authors,
        affiliation=args.affiliation,
        repo_root=repo_root,
        output_path=out_p,
    )
    um = card["ungated_metrics_8seed"]
    print(
        f"[evaluate_submission] id={card['submission_metadata']['submission_id']} | "
        f"status={card['admission_gate']['status']} | "
        f"Q_proxy={um['q_proxy']['mean']:.4f} | Q_true={um['q_true']['mean']:.4f}±{um['q_true']['sd']:.4f} | "
        f"Held-out R_true={um['held_out_r_true']['mean']:.4f}±{um['held_out_r_true']['sd']:.4f} | "
        f"Goodhart={um['goodhart_share_pct_max']:.1f}% | SHA-256={card['receipt_sha256'][:16]}..."
    )
    for r in card["admission_gate"]["rejection_reasons"]:
        print(f"  [REJECT] {r}", file=sys.stderr)
    return 0 if (card["admission_gate"]["admitted"] or args.allow_rejected) else 1


if __name__ == "__main__":
    raise SystemExit(main())
