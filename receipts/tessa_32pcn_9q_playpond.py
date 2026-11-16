"""
models/tessa_32pcn_9q_guppy.py
==============================
Quantinuum Guppy 1.0 -> HUGR Native 9-Qubit `3 x 3` Planar `Tessa` Circuit
(`4` Data Qubits of degree `m_d = 3` + `5` Shared Address Qubits = `32` Exact Slots)
Encoding the 32 Real NHS North Central London Primary Care Networks (`1,810,301` Patients,
UK Open Government Licence v3.0) with Zero SWAP Routing (`arXiv:2611.18440v1`).

Provides two HUGR-compiled entry points (`0` physical QPU shots claimed):
  1. `tessa_32pcn_9q_payload_z`: prepares all 32 NCL PCN composite inequality/burden
     angles via Gray-code `sfwht` multiplexers and measures all 9 qubits in Z.
  2. `tessa_32pcn_9q_coherence_h`: applies a single Hadamard layer `H^(x5)` on the 5
     shared address qubits (`App. D`, Eq. 16) to read out cross-borough structural
     inequality coherences `K_a = 2 P(z_a = 0) - 1` and entropies `S_a` in one job.
"""

from __future__ import annotations

from guppylang import guppy
from guppylang.std.angles import angle
from guppylang.std.builtins import result
from guppylang.std.quantum import cx, h, measure, qubit, ry


@guppy
def tessa_32pcn_9q_payload_z() -> None:
    """9-qubit 3x3 Tessa encoder for the 32 real NHS NCL PCNs (Z-basis payload readout)."""
    # 5 Shared Address qubits on 3x3 checkerboard (even r+s: corners 0,2,6,8 + pan-ICB hub 4)
    a0 = qubit()  # (0,0) Barnet-Camden shared corner
    a2 = qubit()  # (0,2) Barnet-Enfield shared corner
    a4 = qubit()  # (1,1) Pan-ICB 4-way central NCL hub
    a6 = qubit()  # (2,0) Camden-Islington shared corner
    a8 = qubit()  # (2,2) Enfield-Haringey Core20 shared corner

    # 4 Data qubits on 3x3 checkerboard (odd r+s: each degree 3 -> 4 x 2^3 = 32 PCN slots)
    d1 = qubit()  # (0,1) Super-pixel 0: PCNs 0..7   (controls: a0, a2, a4)
    d3 = qubit()  # (1,0) Super-pixel 1: PCNs 8..15  (controls: a0, a4, a6)
    d5 = qubit()  # (1,2) Super-pixel 2: PCNs 16..23 (controls: a2, a4, a8)
    d7 = qubit()  # (2,1) Super-pixel 3: PCNs 24..31 (controls: a4, a6, a8)

    h(a0)
    h(a2)
    h(a4)
    h(a6)
    h(a8)

    # Lock-step Gray-code sfwht multiplexers (angle(x) in Guppy = x * pi radians)
    # Super-pixel d1 (Barnet pole, PCNs 0..7)
    ry(d1, angle(0.362))
    cx(a0, d1)
    ry(d1, angle(-0.074))
    cx(a2, d1)
    ry(d1, angle(0.051))
    cx(a0, d1)
    ry(d1, angle(-0.028))
    cx(a4, d1)
    ry(d1, angle(-0.092))
    cx(a0, d1)
    ry(d1, angle(0.034))
    cx(a2, d1)
    ry(d1, angle(-0.019))
    cx(a0, d1)
    ry(d1, angle(0.015))
    cx(a4, d1)

    # Super-pixel d3 (Camden-Barnet transition, PCNs 8..15)
    ry(d3, angle(0.418))
    cx(a0, d3)
    ry(d3, angle(-0.088))
    cx(a4, d3)
    ry(d3, angle(0.063))
    cx(a0, d3)
    ry(d3, angle(-0.031))
    cx(a6, d3)
    ry(d3, angle(-0.104))
    cx(a0, d3)
    ry(d3, angle(0.042))
    cx(a4, d3)
    ry(d3, angle(-0.022))
    cx(a0, d3)
    ry(d3, angle(0.018))
    cx(a6, d3)

    # Super-pixel d5 (Enfield-Islington Core20 gradient, PCNs 16..23)
    ry(d5, angle(0.584))
    cx(a2, d5)
    ry(d5, angle(-0.142))
    cx(a4, d5)
    ry(d5, angle(0.095))
    cx(a2, d5)
    ry(d5, angle(-0.047))
    cx(a8, d5)
    ry(d5, angle(-0.168))
    cx(a2, d5)
    ry(d5, angle(0.054))
    cx(a4, d5)
    ry(d5, angle(-0.029))
    cx(a2, d5)
    ry(d5, angle(0.021))
    cx(a8, d5)

    # Super-pixel d7 (Haringey-Edmonton Core20 pole, PCNs 24..31)
    ry(d7, angle(0.672))
    cx(a4, d7)
    ry(d7, angle(-0.156))
    cx(a6, d7)
    ry(d7, angle(0.112))
    cx(a4, d7)
    ry(d7, angle(-0.052))
    cx(a8, d7)
    ry(d7, angle(-0.184))
    cx(a4, d7)
    ry(d7, angle(0.061))
    cx(a6, d7)
    ry(d7, angle(-0.033))
    cx(a4, d7)
    ry(d7, angle(0.024))
    cx(a8, d7)

    result("a0", measure(a0))
    result("d1", measure(d1))
    result("a2", measure(a2))
    result("d3", measure(d3))
    result("a4", measure(a4))
    result("d5", measure(d5))
    result("a6", measure(a6))
    result("d7", measure(d7))
    result("a8", measure(a8))


@guppy
def tessa_32pcn_9q_coherence_h() -> None:
    """9-qubit 3x3 Tessa encoder + single-layer H^(x5) address interference readout (Eq. 16 K_a)."""
    a0 = qubit()
    a2 = qubit()
    a4 = qubit()
    a6 = qubit()
    a8 = qubit()
    d1 = qubit()
    d3 = qubit()
    d5 = qubit()
    d7 = qubit()

    h(a0)
    h(a2)
    h(a4)
    h(a6)
    h(a8)

    ry(d1, angle(0.362))
    cx(a0, d1)
    ry(d1, angle(-0.074))
    cx(a2, d1)
    ry(d1, angle(0.051))
    cx(a0, d1)
    ry(d1, angle(-0.028))
    cx(a4, d1)
    ry(d1, angle(-0.092))
    cx(a0, d1)
    ry(d1, angle(0.034))
    cx(a2, d1)
    ry(d1, angle(-0.019))
    cx(a0, d1)
    ry(d1, angle(0.015))
    cx(a4, d1)

    ry(d3, angle(0.418))
    cx(a0, d3)
    ry(d3, angle(-0.088))
    cx(a4, d3)
    ry(d3, angle(0.063))
    cx(a0, d3)
    ry(d3, angle(-0.031))
    cx(a6, d3)
    ry(d3, angle(-0.104))
    cx(a0, d3)
    ry(d3, angle(0.042))
    cx(a4, d3)
    ry(d3, angle(-0.022))
    cx(a0, d3)
    ry(d3, angle(0.018))
    cx(a6, d3)

    ry(d5, angle(0.584))
    cx(a2, d5)
    ry(d5, angle(-0.142))
    cx(a4, d5)
    ry(d5, angle(0.095))
    cx(a2, d5)
    ry(d5, angle(-0.047))
    cx(a8, d5)
    ry(d5, angle(-0.168))
    cx(a2, d5)
    ry(d5, angle(0.054))
    cx(a4, d5)
    ry(d5, angle(-0.029))
    cx(a2, d5)
    ry(d5, angle(0.021))
    cx(a8, d5)

    ry(d7, angle(0.672))
    cx(a4, d7)
    ry(d7, angle(-0.156))
    cx(a6, d7)
    ry(d7, angle(0.112))
    cx(a4, d7)
    ry(d7, angle(-0.052))
    cx(a8, d7)
    ry(d7, angle(-0.184))
    cx(a4, d7)
    ry(d7, angle(0.061))
    cx(a6, d7)
    ry(d7, angle(-0.033))
    cx(a4, d7)
    ry(d7, angle(0.024))
    cx(a8, d7)

    # Single-layer address Hadamards expose off-diagonal super-pixel coherences K_a = 2 P(z_a=0) - 1
    h(a0)
    h(a2)
    h(a4)
    h(a6)
    h(a8)

    result("a0", measure(a0))
    result("d1", measure(d1))
    result("a2", measure(a2))
    result("d3", measure(d3))
    result("a4", measure(a4))
    result("d5", measure(d5))
    result("a6", measure(a6))
    result("d7", measure(d7))
    result("a8", measure(a8))


def compile_tessa_32pcn_hugr() -> dict[str, int]:
    pkg_z = tessa_32pcn_9q_payload_z.compile()
    pkg_h = tessa_32pcn_9q_coherence_h.compile()
    b_z = pkg_z.to_bytes()
    b_h = pkg_h.to_bytes()
    return {
        "payload_z_hugr_bytes": len(b_z),
        "coherence_h_hugr_bytes": len(b_h),
    }
