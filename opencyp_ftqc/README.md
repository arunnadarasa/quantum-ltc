---
license: cc-by-4.0
task_categories:
  - other
tags:
  - quantum-chemistry
  - fault-tolerant-quantum-computing
  - tensor-hypercontraction
  - orbital-entanglement
  - cytochrome-p450
  - fcidump
  - qmmm
  - pharmacology
  - nhs-dcb0129
pretty_name: OpenCYP-FTQC v1.2 — 15 Human Cytochrome P450 QM/MM Active-Space FCIDUMP Hamiltonians (up to CAS 13e,13o / 2.94M Dets), Orbital Entanglement, Empirical THC & Clinical DDI Benchmark
size_categories:
  - n<1K
---

# OpenCYP-FTQC v1.2
**Open-Science Crystallographic `QM/MM` Active-Space `FCIDUMP` Hamiltonians (`15` `.fcidump.gz` files up to `CAS(13e,13o)` / `2,944,656` Slater determinants across `CYP3A4`, `CYP2D6`, `CYP2C9` vs Closed-Shell `ACE` `Zn²⁺`), Exact Orbital Entanglement & Fiedler DMRG Bond Dimensions (`χ = 963`), Empirical `THC` / `SO(M)` `Δ-THC` Factors (`opencyp_ftqc_v1_1_thc_factors.npz`), & External Human Washout / `openFDA FAERS` Benchmark**

**Author:** Arun Nadarasa (*Mid and South Essex NHS Foundation Trust & International Social Prescribing Pharmacy Association (ISPPA), London, UK*)  
**Interactive Portal & 3D Viewer:** https://arunnadarasa.github.io/quantum-ltc/#structures  
**Scope:** Strictly **non-commercial open scientific research** (`0` physical QPU shots, `0` human wet-lab specimens, `phi_present = False`, `6/6` NHS DCB0129 & DCB0160 hazards `OPEN`).

---

## Why OpenCYP-FTQC Exists
Fault-tolerant quantum computing (`FTQC`) chemistry benchmarks overwhelmingly target industrial nitrogenase (`FeMoco`), leaving **human polypharmacy drug metabolism** without standardized, ready-to-load second-quantized Hamiltonians. `OpenCYP-FTQC v1.2` provides **15 spin-pure, protein-electrostatic-embedded (`PySCF 2.15 qmmm.mm_charge`, `def2-SVP`) `FCIDUMP` Hamiltonians** across the three human P450 isoforms responsible for >75% of small-molecule drug clearance (`CYP3A4`, `CYP2D6`, `CYP2C9` spanning all 6 FTQC-routed NCL ICB Long Term Conditions: `CVD`, `AF`, `CKD`, `NAFLD/MASLD`, `COPD`, `Adult Asthma`), alongside:
- **Expanded `v1.2` `CAS(13e, 13o)` (`2,944,656` Slater determinants)** midazolam C–H abstraction (`RC` and `TS_HAT`) on `CYP3A4` `PDB 5TE8` (`opencyp_ftqc_v1_2_manifest.json`), plus `CAS(11e, 11o)` (`213,444` determinants) in `v1.1`;
- **Exact orbital entanglement (`s_p^(1)`, `I_{pq}`), spectral Fiedler 1D DMRG bond dimensions (`χ`), and `SelectedCI` determinant walls:** closed-shell `ACE 1O86` (`S=0`) exhibits near-zero total single-orbital entropy (`∑ s_p^(1) = 0.0832 nats`, `0%` pairs with `I_{pq} > 0.01`, `SelectedCI` `< 1.6 mHa` in `100` dets, Fiedler `χ(10^-6) = 63`), whereas matched-`S=0` `COPD CLR-MIC 1TQN` reaches `5.0650 nats` (**`60.85×` higher**, `χ(10^-6) = 378`) and `CYP3A4 5TE8` `CAS(13e,13o)` reaches **`6.8953 nats` (`82.84×` `ACE 1O86`)** and **Fiedler `χ(10^-6) = 963` (`15.29×` `ACE 1O86`)**;
- **Matched-spin (`S = 0`) singlet demarcation** contrasting open-shell `COPD` clarithromycin nitroso-alkane metabolic-intermediate complex (`CYP3A4` `PDB 1TQN`, `|RCCSD(T) - FCI| = 7.15 mHa`, `T1 = 0.124`) against closed-shell `3d¹⁰` `Zn²⁺` `ACE + Lisinopril` (`PDB 1O86`, `|RCCSD(T) - FCI| = 0.00566 mHa`, `T1 = 0.0038` — **`1,263×` singlet error separation**);
- **Empirical unit-leaf Tensor Hypercontraction (`THC`) and `SO(M)`-aligned difference-Hamiltonian `Δ-THC` factors** (`opencyp_ftqc_v1_1_thc_factors.npz`, reproducing exact spin-pure `FCI` to `< 1.0 mHa` across all 6 FTQC LTCs with empirical frozen-core `λ_THC < λ_DF` crossover at `M = 26`);
- **Sealed `CQWM v0.1`, `CQWM v0.2`, & External Human Washout / `openFDA FAERS` receipts (`receipts/`)** validating zero-refit `CQWM Δ-THC` (`GMFE = 1.434`, `6/7` active visits in 2-fold) on the human 5-day ritonavir + midazolam washout trial (`PMID: 38393578`), disproportionality across `21,054,159` `openFDA FAERS` reports (`6.57×` active-comparator `ROR` for `Clarithromycin + Simvastatin` vs `Azithromycin + Simvastatin`, `p < 10^-23`), and live 6-qubit `Guppy 1.0 → HUGR` Quantum Comb runs on Quantinuum Nexus `Helios-1E-lite` (`6,144` cloud-emulator shots, `0` physical QPU shots).

## 15 Verified `QM/MM` `FCIDUMP` Hamiltonians (`v1.0` + `v1.1` + `v1.2`)

| File (`fcidump/`) | Release | Active Space | `2S` (`ms2`) | `E_core` (Ha) | Size | SHA-256 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `CYP3A4_5TE8_08J_RC_QMMM_CAS9e9o_def2SVP.fcidump.gz` | `v1.0` | `(9e, 9o)` | `1` | `-1867.3733` | `14.0 KB` | `f0a4199bd1c57954…` |
| `CYP3A4_5TE8_08J_TS_HAT_QMMM_CAS9e9o_def2SVP.fcidump.gz` | `v1.0` | `(9e, 9o)` | `1` | `-1870.1631` | `13.9 KB` | `d0d065aa296a3cbe…` |
| `CYP3A4_3NXU_RIT_TypeII_QMMM_CAS9e9o_def2SVP.fcidump.gz` | `v1.0` | `(9e, 9o)` | `1` | `-1801.3002` | `13.9 KB` | `9c59075f5f2c9970…` |
| `CYP2D6_4WNU_QDN_RC_QMMM_CAS9e9o_def2SVP.fcidump.gz` | `v1.0` | `(9e, 9o)` | `1` | `-1871.3706` | `13.8 KB` | `9e4e3caf4c3f0f67…` |
| `CYP2D6_4WNU_QDN_TS_HAT_QMMM_CAS9e9o_def2SVP.fcidump.gz` | `v1.0` | `(9e, 9o)` | `1` | `-1871.1266` | `13.8 KB` | `3187f2222bb16239…` |
| `CYP2C9_1R9O_FLP_RC_QMMM_CAS9e9o_def2SVP.fcidump.gz` | `v1.0` | `(9e, 9o)` | `1` | `-1868.0985` | `13.9 KB` | `57c09d5f28a0822f…` |
| `CYP2C9_1R9O_FLP_TS_HAT_QMMM_CAS9e9o_def2SVP.fcidump.gz` | `v1.0` | `(9e, 9o)` | `1` | `-1870.7926` | `13.7 KB` | `b37203e84a1b658c…` |
| `ACE_1O86_LPR_Zn2_QMMM_CAS12e10o_def2SVP.fcidump.gz` | `v1.0` | `(12e, 10o)` | `0` | `-2012.4348` | `20.2 KB` | `5b1fdcede7e4d65f…` |
| `CYP3A4_1TQN_Resting_OH2_QMMM_CAS9e9o_def2SVP.fcidump.gz` | `v1.1` | `(9e, 9o)` | `1` | `-1821.7548` | `14.3 KB` | `6a2e70ab1382d860…` |
| `CYP3A4_1TQN_CLR_MIC_QMMM_CAS10e10o_def2SVP.fcidump.gz` | `v1.1` | `(10e, 10o)` | `0` | `-1915.0472` | `20.7 KB` | `86768eda7d40fb7f…` |
| `CYP3A4_1TQN_ITR_TypeII_QMMM_CAS9e9o_def2SVP.fcidump.gz` | `v1.1` | `(9e, 9o)` | `1` | `-1998.2221` | `14.4 KB` | `ba87598bf957c8b3…` |
| `CYP3A4_5TE8_08J_RC_QMMM_CAS11e11o_def2SVP.fcidump.gz` | `v1.1` | `(11e, 11o)` | `1` | `-1863.9312` | `29.7 KB` | `545c26a0be57ab85…` |
| `CYP3A4_5TE8_08J_TS_HAT_QMMM_CAS11e11o_def2SVP.fcidump.gz` | `v1.1` | `(11e, 11o)` | `1` | `-1864.1737` | `29.6 KB` | `1d089cf4e288e629…` |
| `CYP3A4_5TE8_08J_RC_QMMM_CAS13e13o_def2SVP.fcidump.gz` | `v1.2` | `(13e, 13o)` | `1` | `-1856.4909` | `55.0 KB` | `d4b0f8ae33c63d76…` |
| `CYP3A4_5TE8_08J_TS_HAT_QMMM_CAS13e13o_def2SVP.fcidump.gz` | `v1.2` | `(13e, 13o)` | `1` | `-1854.3292` | `54.6 KB` | `0f5fc7d8666dcbf3…` |

## 5-Line Python Quickstart (`PySCF` / `OpenFermion` / `Block2`)
```python
import gzip, shutil
from pyscf import fci
from pyscf.tools import fcidump

with gzip.open("fcidump/CYP3A4_5TE8_08J_TS_HAT_QMMM_CAS13e13o_def2SVP.fcidump.gz", "rb") as fin, open("ts13.fcidump", "wb") as fout:
    shutil.copyfileobj(fin, fout)

ctx = fcidump.read("ts13.fcidump")
solver = fci.addons.fix_spin_(fci.direct_spin1.FCI(), ss=0.75)
e_fci, _ = solver.kernel(ctx["H1"], ctx["H2"], ctx["NORB"], (7, 6), ecore=ctx["ECORE"])
print(f"Exact Spin-Pure CAS(13e,13o) QM/MM Energy (2,944,656 dets): {e_fci:.6f} Ha")
```

## Mandatory Upstream Non-Commercial & Open-Data Attributions
- **Google Antigravity for Scientific Workflows:** Supported in part by complimentary access to Google Antigravity and Gemini 4 Argon for non-commercial scientific research.
- **RCSB Protein Data Bank (`PDB 1TQN`, `5TE8`, `3NXU`, `4WNU`, `1R9O`, `1O86`):** CC0 1.0 Public Domain (https://www.rcsb.org/pages/usage-policy).
- **EMBL-EBI ChEMBL (`ChEMBL_37`: `CHEMBL340`, `CHEMBL289`, `CHEMBL3397`):** CC BY-SA 3.0 (https://chembl.gitbook.io/chembl-interface-documentation/about).
- **NCBI PubMed E-utilities & openFDA FAERS (`21,054,159` reports):** Retrieved via official rate-limited APIs for non-commercial research only (*Do not rely on openFDA to make decisions regarding medical care. Always speak to your health provider about the risks and benefits of FDA-regulated products.*).
- **AlphaGenome 2 (`v2.dna_client` & Atlas AVI):** Subject to the AlphaGenome Non-Commercial Terms (https://deepmind.google.com/science/alphagenome/terms).
