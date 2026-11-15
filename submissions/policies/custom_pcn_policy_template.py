"""
Starter Template for Quantum-LTC v1.4 External Benchmark Submissions (`32-PCN Real NHS NCL Track`).

How to evaluate & generate a cryptographically sealed scorecard locally (<1s, zero cloud keys):
    qltc eval-policy --policy examples/custom_pcn_policy_template.py:propose
    qltc submit-policy \\
        --policy examples/custom_pcn_policy_template.py:propose \\
        --submission-id ext-starter-template-v1 \\
        --title "Local Demand-Weighted Safe Standing-Order Starter Policy" \\
        --authors "Quantum-LTC Open Benchmark Starter" \\
        --output submissions/scorecards/ext-starter-template-v1.json

Sandbox & Privilege-Separation Contract:
  - `obs` is a read-only `MappingProxyType` exposing ONLY public baseline PCN indicators
    (UK OHID QOF/IMD 2025 + August 2026 NHSBSA EPD aggregates) and `observable_proxy_yield`.
  - Ground-truth biophysical utility (`Q_true`), `CQWM v0.3` intracellular washout trajectories,
    and the `S = 8` unseen winter/supply shock schedules are hidden (`0` policy calls during shocks).
  - Filesystem, network, shell, and `quantum_ltc` oracle imports are blocked by AST verification.
"""

from typing import Any, Mapping


def _is_clinically_verified(action: Mapping[str, Any]) -> bool:
    """Rejects G1 (80+ over-titration), G2 (Core20 interpreter skip), and G3 (short-washout PDC gaming)."""
    if action["goodhart_mode"] != "CLEAN_VERIFIED":
        return False
    if not action["frail_80plus_ceiling_150"] or not action["equity_interpreter_coupled"]:
        return False
    pathway_k = int(action["pathway_k"])
    hold_h = int(action["hold_hours_param"])
    if pathway_k == 0 and hold_h < 96:
        return False
    if pathway_k == 1 and hold_h < 48:
        return False
    return True


def propose(obs: Mapping[str, Any]) -> dict[str, Any]:
    """
    Decentralized per-PCN policy: compensates for the observable 4% interpreter time-cost
    discount in Core20 deprived PCNs while preserving balanced 6-pathway coverage via
    `(pcn_idx + is_core20_deprived) % 6`.
    """
    safe_actions = [c for c in obs["candidate_actions"] if _is_clinically_verified(c)]
    pcn_idx = int(obs["pcn_idx"])
    dw = obs["demand_weights"]

    # Local two-choice tournament between (pcn_idx % 6) and ((pcn_idx + 3) % 6),
    # correcting observable proxy yield for honest Core20 interpreter consultation time
    k_a = pcn_idx % 6
    k_b = (pcn_idx + 3) % 6
    cand_ab = [c for c in safe_actions if int(c["pathway_k"]) in (k_a, k_b)]
    core20_lift = 1.08 if obs["is_core20_deprived"] else 1.00

    best = max(
        cand_ab,
        key=lambda c: float(c["observable_proxy_yield"]) * core20_lift * (0.85 + 0.15 * float(dw[int(c["pathway_k"])])),
    )
    return dict(best)
