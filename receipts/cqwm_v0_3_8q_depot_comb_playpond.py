"""
models/cqwm_v0_3_8q_depot_comb_guppy.py
=======================================
Quantinuum Guppy 1.0 -> HUGR Native Circuit Definitions for the Clinical Quantum
World Model (`CQWM v0.3`) 8-Qubit Multi-Slot Depot Quantum Comb (`Kashefi Atlas A01c`).

Register layout (8 qubits, Hilbert dimension d = 256, Liouvillian d^2 = 65,536):
  - s0: Cardiovascular / Outcome #23 Vascular BP axis
  - s1: Hepatic CYP3A4 victim-drug toxicity axis (Midazolam / Simvastatin / Rivaroxaban)
  - s2: Renal eGFR / OAT3-Pgp / Hyperkalaemia axis
  - s3: Pulmonary / Viral acute flare axis (Paxlovid / Clarithromycin trigger)
  - m0: Tier-1 Bath Memory — Hepatic CYP3A4 covalent heme-adduct pool (t_1/2 = 55.2 h)
  - m1: Tier-2 Bath Memory — Intracellular hepatocyte/enterocyte lipophilic depot
        (Keemink et al. 2015, PMID: 25989229, Kp,uu = 1.4; feeds `m0` via CRy(m1->m0)!)
  - m2: Tier-3 Bath Memory — Renal-tubular / OAT3-Pgp efflux stress memory
  - p0: Active Syndrome Post-Selection (`ASPS`) & SPAM Parity Witness Ancilla
        (`mid_p0 == 0` mid-comb bath-wire transport check + `p0 ^ s0 ^ s1 ^ s2 ^ s3 == 0`
         end-of-comb 4-organ GF(2) readout syndrome invariant)

Four paired 8-qubit circuits are compiled to Quantinuum HUGR for live execution on
Quantinuum Nexus `Helios-1E-lite` (`QSystemErrorModel("alpha")`; 0 physical QPU shots):
  1. `cqwm_8q_full_depot_comb`: Full 3-bath Non-Markovian Comb (`m0, m1, m2` coherent across
     all k = 1..5 clinical slots) under naive +48h washout restart `pi_B`.
  2. `cqwm_8q_partial_depot_reset_comb`: Operational Causal-Break Tomography on `m1` ONLY
     (`project_z(m1) + reset(m1)` after Slot 1 while `m0, m2` remain coherent), isolating the
     exact causal contribution of the intracellular hepatocyte depot vs covalent enzyme memory.
  3. `cqwm_8q_full_markovian_reset_comb`: Full Memoryless Markovian Causal-Break Twin
     (`project_z + reset` on `m0, m1, m2` after Slots 1, 2, 3, 4), defining the operational
     multi-time Process-Tensor Non-Markovianity Witness.
  4. `cqwm_8q_depot_aware_safe_hold_comb`: Persistent 3-bath Non-Markovian physics (`zero resets`
     on `m0, m1, m2`) under depot-aware Pharmacist SMR extended Day-10 hold `do(pi_C*)`.
"""

from __future__ import annotations

from guppylang import guppy
from guppylang.std.angles import angle
from guppylang.std.builtins import result
from guppylang.std.quantum import cx, cz, measure, project_z, qubit, reset, ry, rz


@guppy
def cqwm_8q_full_depot_comb() -> None:
    """
    Arm 1: 8-Qubit Full 2-Tier Depot Non-Markovian Quantum Comb (`pi_B` +48h Restart).
    All three physiological bath wires (`m0` covalent CYP3A4 pool, `m1` intracellular
    hepatocyte depot, `m2` renal-tubular stress) persist coherently across Slots 1..5.
    """
    s0 = qubit()
    s1 = qubit()
    s2 = qubit()
    s3 = qubit()
    m0 = qubit()
    m1 = qubit()
    m2 = qubit()
    p0 = qubit()

    # Slot 1 (Days 1-5 Boosting): Viral/airway flare + loading of covalent heme bath `m0`,
    # intracellular lipophilic hepatocyte depot `m1` (Kp,uu = 1.4), and tubular bath `m2`
    ry(s3, angle(0.52))
    ry(s0, angle(0.16))
    ry(s2, angle(0.18))
    ry(m0, angle(0.78))
    ry(m1, angle(0.88))
    ry(m2, angle(0.58))
    cz(s3, m0)
    cz(m1, m0)
    cz(s2, m2)
    cx(s3, s0)

    # Slot 2 (Day 6, +24h Washout): Plasma drug < LLOQ; de-novo enzyme synthesis relaxes `m0`
    # (`ry(-0.52)`), while persistent intracellular depot `m1` applies CRy(m1 -> m0, +0.56)!
    ry(m0, angle(-0.52))
    ry(m0, angle(0.28))
    cx(m1, m0)
    ry(m0, angle(-0.28))
    cx(m1, m0)
    ry(m1, angle(-0.14))

    # Mid-comb phase-preserving ASPS / SPAM transport witness on `p0` (ideal `mid_p0 == 0`)
    cx(m0, p0)
    cx(m1, p0)
    cx(m1, p0)
    cx(m0, p0)
    result("mid_p0", project_z(p0).read())
    reset(p0)

    # Slot 3 (Day 7, +48h Probe / Naive Restart `pi_B`): Re-inactivated `m0` drives hepatic
    # victim-drug surge `s1` -> cardiorenal cascade `s2`
    ry(s1, angle(0.10))
    cx(m0, s1)
    cx(s1, s2)
    cz(m2, s2)

    # Slot 4 (Day 9, +96h Offset): Intracellular depot clears and PXR-primed synthesis recovers `m0`
    ry(m1, angle(-0.52))
    ry(m0, angle(-0.26))
    ry(m2, angle(-0.20))
    cx(m0, s0)
    cz(s1, s2)

    # Slot 5 (Day 14 Continuity + End-of-Comb 4-Organ GF(2) ASPS Parity Extraction on `p0`)
    ry(s3, angle(-0.44))
    ry(s0, angle(-0.10))
    rz(s1, angle(0.16))
    cx(s0, p0)
    cx(s1, p0)
    cx(s2, p0)
    cx(s3, p0)

    result("s0", measure(s0).read())
    result("s1", measure(s1).read())
    result("s2", measure(s2).read())
    result("s3", measure(s3).read())
    result("m0", measure(m0).read())
    result("m1", measure(m1).read())
    result("m2", measure(m2).read())
    result("p0", measure(p0).read())


@guppy
def cqwm_8q_partial_depot_reset_comb() -> None:
    """
    Arm 2: 8-Qubit Partial Causal-Break Comb (`do(reset m1)` Depot-Ablated Twin).
    Identical 1Q/2Q unitary gates to Arm 1, except intracellular hepatocyte depot `m1`
    undergoes mid-circuit `project_z(m1) + reset(m1)` after Slot 1 while covalent hepatic
    `CYP3A4` pool `m0` remains coherent — isolating the exact causal effect of the depot (`m1`).
    """
    s0 = qubit()
    s1 = qubit()
    s2 = qubit()
    s3 = qubit()
    m0 = qubit()
    m1 = qubit()
    m2 = qubit()
    p0 = qubit()

    # Slot 1 (Days 1-5): Identical unitary block
    ry(s3, angle(0.52))
    ry(s0, angle(0.16))
    ry(s2, angle(0.18))
    ry(m0, angle(0.78))
    ry(m1, angle(0.88))
    ry(m2, angle(0.58))
    cz(s3, m0)
    cz(m1, m0)
    cz(s2, m2)
    cx(s3, s0)

    # Causal break on intracellular depot `m1` ONLY (plasma-only MBI assumption `CQWM v0.1`)
    result("s1_dep_m1", project_z(m1).read())
    reset(m1)

    # Slot 2 (Day 6, +24h Washout): Identical unitary block (`CRy(m1->m0)` acts as identity!)
    ry(m0, angle(-0.52))
    ry(m0, angle(0.28))
    cx(m1, m0)
    ry(m0, angle(-0.28))
    cx(m1, m0)
    ry(m1, angle(-0.14))

    result("s2_dep_m1", project_z(m1).read())
    reset(m1)

    # Mid-comb ASPS transport witness on `p0`
    cx(m0, p0)
    cx(m1, p0)
    cx(m1, p0)
    cx(m0, p0)
    result("mid_p0", project_z(p0).read())
    reset(p0)

    # Slot 3 (Day 7, +48h Probe / Naive Restart `pi_B`): Identical unitary block
    ry(s1, angle(0.10))
    cx(m0, s1)
    cx(s1, s2)
    cz(m2, s2)

    # Slot 4 (Day 9, +96h Offset): Identical unitary block
    ry(m1, angle(-0.52))
    ry(m0, angle(-0.26))
    ry(m2, angle(-0.20))
    cx(m0, s0)
    cz(s1, s2)

    # Slot 5 (Day 14 Continuity + End-of-Comb ASPS Parity Extraction on `p0`)
    ry(s3, angle(-0.44))
    ry(s0, angle(-0.10))
    rz(s1, angle(0.16))
    cx(s0, p0)
    cx(s1, p0)
    cx(s2, p0)
    cx(s3, p0)

    result("s0", measure(s0).read())
    result("s1", measure(s1).read())
    result("s2", measure(s2).read())
    result("s3", measure(s3).read())
    result("m0", measure(m0).read())
    result("m1", measure(m1).read())
    result("m2", measure(m2).read())
    result("p0", measure(p0).read())


@guppy
def cqwm_8q_full_markovian_reset_comb() -> None:
    """
    Arm 3: 8-Qubit Full Memoryless Markovian Causal-Break Twin (`do(reset m0, m1, m2)`).
    Identical 1Q/2Q unitary gates to Arm 1, interrupted after Slots 1, 2, 3, and 4 by
    mid-circuit `project_z + reset` across all three bath-memory qubits `m0, m1, m2`.
    """
    s0 = qubit()
    s1 = qubit()
    s2 = qubit()
    s3 = qubit()
    m0 = qubit()
    m1 = qubit()
    m2 = qubit()
    p0 = qubit()

    # Slot 1 (Days 1-5): Identical unitary block
    ry(s3, angle(0.52))
    ry(s0, angle(0.16))
    ry(s2, angle(0.18))
    ry(m0, angle(0.78))
    ry(m1, angle(0.88))
    ry(m2, angle(0.58))
    cz(s3, m0)
    cz(m1, m0)
    cz(s2, m2)
    cx(s3, s0)

    # Full Markovian bath erasure after Slot 1
    result("k1_m0", project_z(m0).read())
    reset(m0)
    result("k1_m1", project_z(m1).read())
    reset(m1)
    result("k1_m2", project_z(m2).read())
    reset(m2)

    # Slot 2 (Day 6): Identical unitary block
    ry(m0, angle(-0.52))
    ry(m0, angle(0.28))
    cx(m1, m0)
    ry(m0, angle(-0.28))
    cx(m1, m0)
    ry(m1, angle(-0.14))

    # Full Markovian bath erasure after Slot 2
    result("k2_m0", project_z(m0).read())
    reset(m0)
    result("k2_m1", project_z(m1).read())
    reset(m1)
    result("k2_m2", project_z(m2).read())
    reset(m2)

    # Mid-comb ASPS transport witness on `p0`
    cx(m0, p0)
    cx(m1, p0)
    cx(m1, p0)
    cx(m0, p0)
    result("mid_p0", project_z(p0).read())
    reset(p0)

    # Slot 3 (Day 7): Identical unitary block
    ry(s1, angle(0.10))
    cx(m0, s1)
    cx(s1, s2)
    cz(m2, s2)

    # Full Markovian bath erasure after Slot 3
    result("k3_m0", project_z(m0).read())
    reset(m0)
    result("k3_m1", project_z(m1).read())
    reset(m1)
    result("k3_m2", project_z(m2).read())
    reset(m2)

    # Slot 4 (Day 9): Identical unitary block
    ry(m1, angle(-0.52))
    ry(m0, angle(-0.26))
    ry(m2, angle(-0.20))
    cx(m0, s0)
    cz(s1, s2)

    # Full Markovian bath erasure after Slot 4
    result("k4_m0", project_z(m0).read())
    reset(m0)
    result("k4_m1", project_z(m1).read())
    reset(m1)
    result("k4_m2", project_z(m2).read())
    reset(m2)

    # Slot 5 (Day 14 Continuity + End-of-Comb ASPS Parity Extraction on `p0`)
    ry(s3, angle(-0.44))
    ry(s0, angle(-0.10))
    rz(s1, angle(0.16))
    cx(s0, p0)
    cx(s1, p0)
    cx(s2, p0)
    cx(s3, p0)

    result("s0", measure(s0).read())
    result("s1", measure(s1).read())
    result("s2", measure(s2).read())
    result("s3", measure(s3).read())
    result("m0", measure(m0).read())
    result("m1", measure(m1).read())
    result("m2", measure(m2).read())
    result("p0", measure(p0).read())


@guppy
def cqwm_8q_depot_aware_safe_hold_comb() -> None:
    """
    Arm 4: 8-Qubit Persistent-Bath Counterfactual Depot-Aware Safe Policy `do(pi_C*)` Comb.
    Preserves 100% of Non-Markovian bath physics (`zero mid-circuit resets` on `m0, m1, m2`),
    while applying CQWM v0.3's extended Day-10 Pharmacist SMR hold until BOTH intracellular
    hepatocyte depot (`m1`) and covalent hepatic CYP3A4 pool (`m0`) have cleared.
    """
    s0 = qubit()
    s1 = qubit()
    s2 = qubit()
    s3 = qubit()
    m0 = qubit()
    m1 = qubit()
    m2 = qubit()
    p0 = qubit()

    # Slot 1 (Days 1-5): Identical acute flare + boosting exposure
    ry(s3, angle(0.52))
    ry(s0, angle(0.16))
    ry(s2, angle(0.18))
    ry(m0, angle(0.78))
    ry(m1, angle(0.88))
    ry(m2, angle(0.58))
    cz(s3, m0)
    cz(m1, m0)
    cz(s2, m2)
    cx(s3, s0)

    # Slot 2 (Days 6-7): Pharmacist SMR Hold initiated — flare/depot phase-lock uncomputed as `m1` desorbs
    cz(m1, m0)
    cz(s3, m0)
    ry(m1, angle(-0.82))
    ry(m0, angle(-0.44))
    ry(m2, angle(-0.48))

    # Mid-comb ASPS transport witness on `p0`
    cx(m0, p0)
    cx(m1, p0)
    cx(m1, p0)
    cx(m0, p0)
    result("mid_p0", project_z(p0).read())
    reset(p0)

    # Slot 3 (Days 8-10): Extended hold completes PXR-primed `m0` + `m1` recovery prior to step-in
    ry(m1, angle(-0.06))
    ry(m0, angle(-0.30))
    ry(s1, angle(0.04))
    cx(m0, s1)
    cx(s1, s2)
    cz(m2, s2)

    # Slot 4 (Days 11-12): Safe low-dose victim re-initiation into recovered enzyme pool
    ry(s1, angle(0.04))
    ry(m2, angle(-0.10))
    cx(m0, s0)
    cz(s1, s2)

    # Slot 5 (Day 14 Continuity + End-of-Comb ASPS Parity Extraction on `p0`)
    ry(s3, angle(-0.44))
    ry(s0, angle(-0.10))
    rz(s1, angle(0.16))
    cx(s0, p0)
    cx(s1, p0)
    cx(s2, p0)
    cx(s3, p0)

    result("s0", measure(s0).read())
    result("s1", measure(s1).read())
    result("s2", measure(s2).read())
    result("s3", measure(s3).read())
    result("m0", measure(m0).read())
    result("m1", measure(m1).read())
    result("m2", measure(m2).read())
    result("p0", measure(p0).read())


def compile_cqwm_v0_3_8q_hugrs():
    return (
        cqwm_8q_full_depot_comb.compile(),
        cqwm_8q_partial_depot_reset_comb.compile(),
        cqwm_8q_full_markovian_reset_comb.compile(),
        cqwm_8q_depot_aware_safe_hold_comb.compile(),
    )
