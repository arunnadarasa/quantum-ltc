---
license: cc-by-4.0
task_categories:
  - other
tags:
  - quantum-chemistry
  - fault-tolerant-quantum-computing
  - cytochrome-p450
  - fcidump
  - qmmm
  - pharmacology
  - nhs-dcb0129
pretty_name: OpenCYP-FTQC v1.0 — Human Cytochrome P450 QM/MM Active-Space Hamiltonians & Clinical DDI Benchmark
size_categories:
  - n<1K
---

# OpenCYP-FTQC v1.0
**Open-Science Crystallographic `QM/MM` Active-Space `FCIDUMP` Hamiltonians (`CYP3A4`, `CYP2D6`, `CYP2C9` vs Closed-Shell `ACE` `Zn²⁺`) & Multi-Isoform `ChEMBL_37` Clinical DDI Benchmark**

**Author:** Arun Nadarasa (*Mid and South Essex NHS Foundation Trust & International Social Prescribing Pharmacy Association (ISPPA), London, UK*)  
**Interactive Portal & 3D Viewer:** https://arunnadarasa.github.io/quantum-ltc/#structures  
**Scope:** Strictly **non-commercial open scientific research** (`0` physical QPU shots, `0` human wet-lab specimens, `phi_present = False`, `6/6` NHS DCB0129 & DCB0160 hazards `OPEN`).

---

## Why OpenCYP-FTQC Exists
Fault-tolerant quantum computing (`FTQC`) chemistry benchmarks overwhelmingly target industrial nitrogenase (`FeMoco`), leaving **human polypharmacy drug metabolism** without standardized, ready-to-load second-quantized Hamiltonians. `OpenCYP-FTQC v1.0` provides **8 spin-pure, protein-electrostatic-embedded (`PySCF 2.15 qmmm.mm_charge`, `def2-SVP`) `FCIDUMP` Hamiltonians** across the three human P450 isoforms responsible for >75% of small-molecule drug clearance (`CYP3A4`, `CYP2D6`, `CYP2C9`) alongside a closed-shell `3d¹⁰` `Zn²⁺` negative control (`ACE` `PDB 1O86`, where classical `RCCSD(T)` matches `Exact FCI` to `0.00566 mHa`).

## 8 Verified `QM/MM` `FCIDUMP` Hamiltonians

| File (`fcidump/`) | Active Space | `2S` (`ms2`) | `E_core` (Ha) | Size | SHA-256 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `CYP3A4_5TE8_08J_RC_QMMM_CAS9e9o_def2SVP.fcidump.gz` | `(9e, 9o)` | `1` | `-1867.3733` | `14.0 KB` | `f0a4199bd1c57954…` |
| `CYP3A4_5TE8_08J_TS_HAT_QMMM_CAS9e9o_def2SVP.fcidump.gz` | `(9e, 9o)` | `1` | `-1870.1631` | `13.9 KB` | `d0d065aa296a3cbe…` |
| `CYP3A4_3NXU_RIT_TypeII_QMMM_CAS9e9o_def2SVP.fcidump.gz` | `(9e, 9o)` | `1` | `-1801.3002` | `13.9 KB` | `9c59075f5f2c9970…` |
| `CYP2D6_4WNU_QDN_RC_QMMM_CAS9e9o_def2SVP.fcidump.gz` | `(9e, 9o)` | `1` | `-1871.3706` | `13.8 KB` | `9e4e3caf4c3f0f67…` |
| `CYP2D6_4WNU_QDN_TS_HAT_QMMM_CAS9e9o_def2SVP.fcidump.gz` | `(9e, 9o)` | `1` | `-1871.1266` | `13.8 KB` | `3187f2222bb16239…` |
| `CYP2C9_1R9O_FLP_RC_QMMM_CAS9e9o_def2SVP.fcidump.gz` | `(9e, 9o)` | `1` | `-1868.0985` | `13.9 KB` | `57c09d5f28a0822f…` |
| `CYP2C9_1R9O_FLP_TS_HAT_QMMM_CAS9e9o_def2SVP.fcidump.gz` | `(9e, 9o)` | `1` | `-1870.7926` | `13.7 KB` | `b37203e84a1b658c…` |
| `ACE_1O86_LPR_Zn2_QMMM_CAS12e10o_def2SVP.fcidump.gz` | `(12e, 10o)` | `0` | `-2012.4348` | `20.2 KB` | `5b1fdcede7e4d65f…` |

## 5-Line Python Quickstart (`PySCF` / `OpenFermion` / `Block2`)
```python
import gzip, shutil
from pyscf import fci
from pyscf.tools import fcidump

with gzip.open("fcidump/CYP3A4_5TE8_08J_TS_HAT_QMMM_CAS9e9o_def2SVP.fcidump.gz", "rb") as fin, open("ts.fcidump", "wb") as fout:
    shutil.copyfileobj(fin, fout)

ctx = fcidump.read("ts.fcidump")
e_fci, _ = fci.direct_spin1.kernel(ctx["H1"], ctx["H2"], ctx["NORB"], (5, 4), ecore=ctx["ECORE"])
print(f"Exact CAS(9e,9o) QM/MM Energy: {e_fci:.6f} Ha")
```

## Mandatory Upstream Non-Commercial & Open-Data Attributions
- **Google Antigravity for Scientific Workflows:** Supported in part by complimentary access to Google Antigravity and Gemini 4 Argon for non-commercial scientific research.
- **RCSB Protein Data Bank (`PDB 5TE8`, `3NXU`, `4WNU`, `1R9O`, `1O86`):** CC0 1.0 Public Domain (https://www.rcsb.org/pages/usage-policy).
- **EMBL-EBI ChEMBL (`ChEMBL_37`: `CHEMBL340`, `CHEMBL289`, `CHEMBL3397`):** CC BY-SA 3.0 (https://chembl.gitbook.io/chembl-interface-documentation/about).
- **AlphaGenome 2 (`v2.dna_client` & Atlas AVI):** Subject to the AlphaGenome Non-Commercial Terms (https://deepmind.google.com/science/alphagenome/terms).
