"""
submissions/policies/tessa_overcompressed_flags_policy.py
=========================================================
Adversarial / Naive Negative-Control Policy (`trap-tessa-overcompressed-flags`):
Illustrates NHS DCB0129 Hazard `H-LTC-02` and Bultrini (`arXiv:2611.18440v1` App. G.4,
p. 18) by packing candidate proxy yields AND discrete safety mode indices into a single
lossy `sfwht`-compressed multiplexer (`tau_rad = 0.35`) without an un-compressed binary
safety guard, causing discrete clinical flag flips & Goodhart proxy-chasing that MUST be
caught and rejected by the `qltc` / `evaluate_submission.py` clinical admission gate.
"""

from __future__ import annotations

import math
from typing import Any, Mapping


def propose(obs: Mapping[str, Any]) -> dict[str, Any]:
    cands = list(obs["candidate_actions"])
    # Pad first 16 candidates (which mix CLEAN_VERIFIED and Goodhart G1/G2/G3 shortcuts!)
    n = 16
    subset = cands[:n] if len(cands) >= n else (cands + [cands[-1]] * (n - len(cands)))

    # Naively encode raw observable_proxy_yield into a 16-slot multiplexer and over-compress
    vals = [float(c["observable_proxy_yield"]) for c in subset]
    vmin = min(vals)
    vmax = max(vals)
    span = max(1e-9, vmax - vmin)
    thetas = [math.pi * (v - vmin) / span for v in vals]

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
        # Aggressive lossy threshold wipes high-frequency safety distinctions while keeping raw proxy peak
        alphas.append(0.0 if abs(ang) < 0.35 else ang)

    best_idx = 0
    best_th = -1e9
    for i in range(len(subset)):
        acc_th = 0.0
        for j in range(16):
            x = i & grays[j]
            par = (x & 1) ^ ((x >> 1) & 1) ^ ((x >> 2) & 1) ^ ((x >> 3) & 1)
            acc_th += (-1.0 if par else 1.0) * alphas[j]
        if acc_th > best_th:
            best_th = acc_th
            best_idx = i

    return dict(subset[best_idx])
