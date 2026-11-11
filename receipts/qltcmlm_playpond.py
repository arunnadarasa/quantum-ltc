"""
models/qltcmlm_guppy.py
=======================
Quantinuum Guppy 1.0 -> HUGR Native Circuit Definition for the 4-Qubit
Quantum Long-Term Conditions Machine Learning Model (`QLTCMLM`) evaluated on a
High-Risk + Complex Multimorbid NCL Patient Profile (Uncontrolled Hypertension #23 +
Declining CKD Stage 3b + SABA-Overuse Asthma + Core20 IMD Quintile 1).
"""

from __future__ import annotations

from guppylang import guppy
from guppylang.std.angles import angle
from guppylang.std.builtins import result
from guppylang.std.quantum import cx, cz, measure, qubit, rx, ry, rz


@guppy
def qltcmlm_4q_frobenius_vqc() -> None:
    """
    4-qubit Frobenius organ-crosstalk VQC compiled directly to Quantinuum HUGR
    for execution on Quantinuum Nexus `Helios-1E-lite` (0 physical QPU shots claimed).
    """
    q0 = qubit()  # Vascular / BP #23 axis
    q1 = qubit()  # Glycaemic / Hepatic axis
    q2 = qubit()  # Renal / Glomerular axis
    q3 = qubit()  # Airway / Exacerbation axis

    # Layer 1: Data-reuploading encoding of high-risk multimorbid patient vector
    ry(q0, angle(0.712))
    rz(q0, angle(0.318))
    rx(q0, angle(0.464))

    ry(q1, angle(0.584))
    rz(q1, angle(0.742))
    rx(q1, angle(0.391))

    ry(q2, angle(0.836))
    rz(q2, angle(0.615))
    rx(q2, angle(0.528))

    ry(q3, angle(0.669))
    rz(q3, angle(0.884))
    rx(q3, angle(0.447))

    # Frobenius ring CNOTs + cross-organ CZ allosteric interference
    cx(q0, q1)
    cx(q1, q2)
    cx(q2, q3)
    cx(q3, q0)
    cz(q0, q2)
    cz(q1, q3)

    # Layer 2: Variational refinement & MDT synthesis block
    ry(q0, angle(0.495))
    rz(q1, angle(0.673))
    ry(q2, angle(0.552))
    rz(q3, angle(0.718))
    cx(q0, q1)
    cx(q2, q3)

    result("v0", measure(q0).read())
    result("v1", measure(q1).read())
    result("v2", measure(q2).read())
    result("v3", measure(q3).read())


def compile_qltcmlm_hugr():
    return qltcmlm_4q_frobenius_vqc.compile()
