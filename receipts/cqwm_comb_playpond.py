"""
models/cqwm_quantum_comb_guppy.py
=================================
Quantinuum Guppy 1.0 -> HUGR Native Circuit Definitions for the Clinical Quantum
World Model (`CQWM v0.2`) 6-Qubit Longitudinal Quantum Comb (`Kashefi Atlas A01c`).

Register layout (6 qubits, Hilbert dimension d = 64):
  - s0: Cardiovascular / Outcome #23 BP axis
  - s1: Hepatic CYP3A4 *1/*22 victim-drug toxicity axis (Simvastatin / Finerenone)
  - s2: Renal eGFR / Hyperkalaemia axis
  - s3: Pulmonary COPD / Airway inflammation axis
  - m0: Persistent Hepatic CYP3A4 Covalent Heme-Adduct (MBI) Bath Memory (t_1/2 = 36 h)
  - m1: Persistent Renal-Tubular Inflammatory Bath Memory

Three paired 6-qubit circuits are compiled to HUGR for live execution on
Quantinuum Nexus `Helios-1E-lite` (`QSystemErrorModel("alpha")`; 0 physical QPU shots):
  1. `cqwm_6q_non_markovian_comb`: Persistent bath memory (`m0, m1` never reset) under
     naive Day-5 post-washout restart policy `pi_B` (captures latent enzyme-memory surge).
  2. `cqwm_6q_markovian_reset_twin`: Identical 1Q/2Q unitary gates across all 4 visits,
     interrupted between visits by mid-circuit `project_z` + `reset` on `m0, m1`
     (memoryless Markovian environment assumption; severely underestimates adverse risk).
  3. `cqwm_6q_counterfactual_safe_hold_comb`: Persistent bath memory (`no reset` on `m0, m1`)
     under CQWM's selected safe counterfactual policy `do(pi_C)` (Day-8 resynthesis hold
     + half-dose step-in, restoring safe multi-organ state without erasing bath physics).
"""

from __future__ import annotations

from guppylang import guppy
from guppylang.std.angles import angle
from guppylang.std.builtins import result
from guppylang.std.quantum import cx, cz, measure, project_z, qubit, reset, ry, rz


@guppy
def cqwm_6q_non_markovian_comb() -> None:
    """
    Arm A: 6-Qubit Non-Markovian Quantum Comb (`pi_B` Naive Day-5 Post-Washout Restart).
    Bath-memory qubits `m0` (hepatic CYP3A4 MBI pool) and `m1` (tubular stress) persist
    coherently across all k = 1..4 Year-of-Care interventions.
    """
    s0 = qubit()
    s1 = qubit()
    s2 = qubit()
    s3 = qubit()
    m0 = qubit()
    m1 = qubit()

    # Visit 1 (Day 1-5): Acute COPD flare + Clarithromycin/Ritonavir covalent MBI bath loading
    ry(s3, angle(0.54))
    ry(s0, angle(0.20))
    ry(s2, angle(0.22))
    ry(m0, angle(0.88))
    ry(m1, angle(0.62))
    cz(s3, m0)
    cz(s2, m1)
    cx(s3, s0)

    # Visit 2 (Day 6): Plasma perpetrator washed out, but m0 stays inactivated -> pi_B restart surge
    ry(s1, angle(0.16))
    cx(m0, s1)
    cx(s1, s2)
    cz(m1, s2)

    # Visit 3 (Day 8-10): Partial spontaneous enzyme turnover; residual bath couples into vascular load
    ry(m0, angle(-0.20))
    ry(m1, angle(-0.18))
    cx(m0, s0)
    cz(s1, s2)

    # Visit 4 (Day 14): Airway recovery & House-of-Care continuity readout
    ry(s3, angle(-0.46))
    ry(s0, angle(-0.10))
    rz(s1, angle(0.18))

    result("s0", measure(s0).read())
    result("s1", measure(s1).read())
    result("s2", measure(s2).read())
    result("s3", measure(s3).read())
    result("m0", measure(m0).read())
    result("m1", measure(m1).read())


@guppy
def cqwm_6q_markovian_reset_twin() -> None:
    """
    Arm B: Equal-Unitary-Gate 6-Qubit Memoryless Markovian Twin (`pi_B` with Bath Reset).
    Executes the exact same 1Q and 2Q unitary gates as `cqwm_6q_non_markovian_comb`,
    interrupted between visits by trapped-ion mid-circuit `project_z` + `reset` on `m0, m1`.
    """
    s0 = qubit()
    s1 = qubit()
    s2 = qubit()
    s3 = qubit()
    m0 = qubit()
    m1 = qubit()

    # Visit 1 (Day 1-5): Identical unitary block
    ry(s3, angle(0.54))
    ry(s0, angle(0.20))
    ry(s2, angle(0.22))
    ry(m0, angle(0.88))
    ry(m1, angle(0.62))
    cz(s3, m0)
    cz(s2, m1)
    cx(s3, s0)

    # Markovian memoryless truncation after Visit 1 (erases persistent MBI heme-adduct state)
    result("v1_m0", project_z(m0).read())
    reset(m0)
    result("v1_m1", project_z(m1).read())
    reset(m1)

    # Visit 2 (Day 6): Identical unitary block (falsely misses `cx(m0, s1)` surge!)
    ry(s1, angle(0.16))
    cx(m0, s1)
    cx(s1, s2)
    cz(m1, s2)

    # Markovian memoryless truncation after Visit 2
    result("v2_m0", project_z(m0).read())
    reset(m0)
    result("v2_m1", project_z(m1).read())
    reset(m1)

    # Visit 3 (Day 8-10): Identical unitary block
    ry(m0, angle(-0.20))
    ry(m1, angle(-0.18))
    cx(m0, s0)
    cz(s1, s2)

    # Markovian memoryless truncation after Visit 3
    result("v3_m0", project_z(m0).read())
    reset(m0)
    result("v3_m1", project_z(m1).read())
    reset(m1)

    # Visit 4 (Day 14): Identical final readout block
    ry(s3, angle(-0.46))
    ry(s0, angle(-0.10))
    rz(s1, angle(0.18))

    result("s0", measure(s0).read())
    result("s1", measure(s1).read())
    result("s2", measure(s2).read())
    result("s3", measure(s3).read())
    result("m0", measure(m0).read())
    result("m1", measure(m1).read())


@guppy
def cqwm_6q_counterfactual_safe_hold_comb() -> None:
    """
    Arm C: 6-Qubit Persistent-Bath Counterfactual Safe Policy `do(pi_C)` Comb.
    Keeps full Non-Markovian bath memory (`no reset` on `m0, m1`), while applying CQWM's
    Pharmacist SMR Day-8 de-novo enzyme resynthesis hold + low-dose step-in.
    """
    s0 = qubit()
    s1 = qubit()
    s2 = qubit()
    s3 = qubit()
    m0 = qubit()
    m1 = qubit()

    # Visit 1 (Day 1-5): Identical acute COPD + perpetrator MBI exposure
    ry(s3, angle(0.54))
    ry(s0, angle(0.20))
    ry(s2, angle(0.22))
    ry(m0, angle(0.88))
    ry(m1, angle(0.62))
    cz(s3, m0)
    cz(s2, m1)
    cx(s3, s0)

    # Visit 2 (Day 6-8): Counterfactual `do(pi_C)` Pharmacist SMR Hold during hepatic resynthesis
    ry(m0, angle(-0.80))
    ry(m1, angle(-0.54))
    ry(s1, angle(0.04))
    cx(m0, s1)
    cx(s1, s2)
    cz(m1, s2)

    # Visit 3 (Day 9-11): Completed de-novo CYP3A4 recovery + safe half-dose step-in
    ry(m0, angle(-0.08))
    ry(m1, angle(-0.08))
    ry(s1, angle(0.08))
    cx(m0, s0)
    cz(s1, s2)

    # Visit 4 (Day 14): Airway + cardiorenal stabilization & continuity readout
    ry(s3, angle(-0.46))
    ry(s0, angle(-0.10))
    rz(s1, angle(0.18))

    result("s0", measure(s0).read())
    result("s1", measure(s1).read())
    result("s2", measure(s2).read())
    result("s3", measure(s3).read())
    result("m0", measure(m0).read())
    result("m1", measure(m1).read())


def compile_cqwm_comb_hugrs():
    return (
        cqwm_6q_non_markovian_comb.compile(),
        cqwm_6q_markovian_reset_twin.compile(),
        cqwm_6q_counterfactual_safe_hold_comb.compile(),
    )
