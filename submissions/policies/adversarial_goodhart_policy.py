"""
Adversarial Negative-Control Submission (`trap-unverified-greedy-proxy`).

Intentionally chases raw observable throughput `observable_proxy_yield` without clinical safety
or equity invariants (selecting G1 80+ over-titration, G2 Core20 interpreter-skipping, and G3
short-washout PDC gaming). Used in CI to verify that `qltc submit-policy` and `verify-submissions`
automatically mark proxy-gaming submissions `REJECTED_SAFETY_OR_GOODHART`.
"""

from typing import Any, Mapping


def propose(obs: Mapping[str, Any]) -> dict[str, Any]:
    """Selects highest raw `observable_proxy_yield` on `(pcn_idx % 6)`, triggering Goodhart rejection."""
    target_k = int(obs["pcn_idx"]) % 6
    on_k = [c for c in obs["candidate_actions"] if int(c["pathway_k"]) == target_k]
    pool = on_k if on_k else obs["candidate_actions"]
    return dict(max(pool, key=lambda c: float(c["observable_proxy_yield"])))
