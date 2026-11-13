---
title: Quantum-LTC Roadmap & OpenCYP-FTQC v1.0
emoji: ⚛️
colorFrom: blue
colorTo: green
sdk: static
app_file: index.html
pinned: false
license: cc-by-4.0
short_description: 4-Era Quantum Roadmap, OpenCYP-FTQC v1.0 & 67-Node KG
---

# Quantum-LTC — Open Research, `OpenCYP-FTQC v1.0` & Interactive Results Portal

- **Live GitHub Pages Portal:** **https://arunnadarasa.github.io/quantum-ltc/**
- **Hugging Face Static Space Mirror:** **https://socialprescribing-quantum-ltc.static.hf.space/index.html**
- **Interactive 8-Layer Knowledge Graph Explorer (`QLTC-KG v1.4`, 67 Nodes, 151 Triples):** **https://arunnadarasa.github.io/quantum-ltc/knowledge-graph.html**
- **`OpenCYP-FTQC v1.0` Dataset on Hugging Face Hub:** **https://huggingface.co/datasets/socialprescribing/opencyp-ftqc**

**Author:** Arun Nadarasa (Innovation Fellow, Mid and South Essex NHS Foundation Trust; International Social Prescribing Pharmacy Association [ISPPA], London, UK)

---

## Included Non-Commercial Open-Science Artifacts

- **Compiled Samskrift Monograph (`downloads/Quantum_LTC_Roadmap.pdf`, 18 pp., 49 verified references, SHA-256 `a68671e4871a842b...`):**
  - Four-Era Clinical Quantum Optimisation & Simulation Roadmap grounded in the **NHS North Central London ICB Locally Commissioned Service (LCS) for Proactive, Personalised Care — Long Term Conditions (Version 6, 2026–2027)** across 9 Long Term Conditions (CVD, AF, Hypertension Outcome #23, T2D, T1D, CKD, NAFLD/MASLD, COPD, and Adult/CYP Asthma).
  - Strictly decouples sparse PCN scheduling (`< 25 ms` exact **HiGHS MILP**) and closed-shell $3d^{10}$ $\text{Zn}^{2+}$ `ACE` chemistry (`PDB 1O86`, `|RCCSD(T) - FCI| <= 0.0258 mHa` in **PySCF 2.15** `QM/MM`) from Era III–IV open-shell hepatic **Cytochrome P450 `CYP3A4` (`5TE8`, `3NXU`, `1TQN`), `CYP2D6` (`4WNU`), and `CYP2C9` (`1R9O`) Compound I** polypharmacy catalysis (`+12.83` to `+47.73 mHa` single-reference breakdown, `2.43x–6.02x` Procrustes `Δ-DF` compression, `75–141` logical qubits) and open-system $\mathcal{O}(4^{n_{\text{spin}}})$ Lindbladian memory walls.
- **`OpenCYP-FTQC v1.0` Archive (`opencyp_ftqc/` & Hugging Face Hub):**
  - 8 gzip-compressed `PySCF 2.15` `def2-SVP` protein-electrostatic `QM/MM` `FCIDUMP` files (`3,646–3,900` crystallographic pocket MM point charges) across `CYP3A4` + midazolam/ritonavir (`5TE8`, `3NXU`), `CYP2D6` + quinidine (`4WNU`), `CYP2C9` + flurbiprofen (`1R9O`), and closed-shell `ACE` + lisinopril (`1O86`), linked to `12/12` `ChEMBL_37` genotype-stratified PBPK exposure ratios (`AUCR`).
- **Interactive Modules (`index.html`, `knowledge-graph.html`):**
  - Real-time **Four-Era Logical-Qubit Roadmap Simulator**, **7-Structure 3D WebGL Active-Site Viewer** (`5TE8`, `3NXU`, `4WNU`, `1R9O`, `1TQN`, `1O86`, `1N9V`), and **67-Node / 151-Triple Ontology-Grounded Knowledge Graph Explorer (`QLTC-KG v1.4`, W3C JSON-LD)**.
- **10 SHA-256-Sealed Provenance Receipts (`receipts/`) & 9 Publication Figures (`figures/`):**
  - `nexus_helios_ltc_receipt.json` (`0e3216dd...`) — Quantinuum Nexus `Helios-1E-lite` (`6,144` cloud emulator shots, `0` physical QPU shots)
  - `haiqu_jij_ltc_receipt.json` (`7212c3d9...`) — Haiqu SDK (`223 -> 26` HUBO LR-QAOA, EME, SU(2), OBP) + JijModeling/OpenJij + HiGHS MILP
  - `biophysical_qprotsim_ltc_receipt.json` (`6ba83347...`) — HQS `struqture-py`/`qoqo`, `QProtSim` (`1N9V`), BioHub, Neurosnap (`1O86`), AlphaGenome Atlas, Arc Institute, Paperclip
  - `metalloenzyme_ftqc_ag2_receipt.json` (`1a9541a1...`) — `PySCF 2.15.0` resting `1O86` vs `CYP3A4` `1TQN` + live `alphagenome==2.0.0` (`v2.dna_client`) primary-cell variant scoring
  - `cyp3a4_drug_barrier_chembl_receipt.json` (`164d38af...`) — Co-crystallised `CYP3A4` `5TE8` (midazolam) & `3NXU` (ritonavir) barrier breakdown, Procrustes `Δ-DF` (`197,568 -> 83,632` phys qubits), and `ChEMBL_37` `CYP3A4*22` PBPK
  - `opencyp_ftqc_v1_receipt.json` (`b46e2d83...`) — Multi-isoform protein-electrostatic `QM/MM` `OpenCYP-FTQC v1.0` (`5TE8`, `3NXU`, `4WNU`, `1R9O`, `1O86`), `2.43x–6.02x` `Δ-DF`, and `12/12` `ChEMBL_37` PBPK polypharmacy regimens
  - `modal_roadmap_rhyme_qml_receipt.json` (`cb1fec7c...`) — Modal Cloud, Rhyme (`rhyme-beta`), `QLTCMLM`, $2 \times 2$ Barren Plateau
  - `governance_primitives_jev_receipt.json` (`bd60742f...`) — Text2WetLab (`6/6 PASS`), Medicus FHIR R4 + `ML-DSA-65`, DisCoPy, Moth Blur, Kashefi Primitives Atlas v0.4, TypeSafe Jev 1.14
  - `deep_review_remediation_receipt.json` (`a6b3854e...`) — MCWF/MPDO baselines, post-SWAP `project_z(q2)`, Haiqu/OpenJij/HQS/`QLTCMLM` controls, and Lie algebra $\dim\mathfrak{g}$ audit
  - `quantum_ltc_knowledge_graph.json` & `.jsonld` (`c8f94fe1...`) — Sealed 67-node / 151-triple property graph & W3C JSON-LD

## Statutory NHS DCB0129 & DCB0160 Demarcation & Open-Science Attributions

All cohorts, schedules, PBPK trajectories, and FHIR R4 bundles are 100% synthetic (`phi_present = False`, `0` physical QPU shots, `0` wet-lab human specimens). All 6 clinical safety hazards (`H-LTC-01` to `H-LTC-06`) remain **OPEN** across manufacturer (DCB0129) and deploying NCL ICB / PCN (DCB0160) clinical risk logs under mandatory clinician sign-off.

Released for **non-commercial open scientific research** under [`LICENSE`](LICENSE) (`Apache-2.0` code / `CC BY 4.0` monograph & `OpenCYP-FTQC v1.0`), attributing **RCSB PDB** (`CC0 1.0`, https://www.rcsb.org/pages/usage-policy), **EMBL-EBI ChEMBL (`ChEMBL_37`)** (`CC BY-SA 3.0`, https://chembl.gitbook.io/chembl-interface-documentation/about), **EMBL-EBI OLS4** (`CC0 1.0`, https://www.ebi.ac.uk/ols4/api-docs), **Google DeepMind AlphaGenome** ([Non-Commercial Terms](https://deepmind.google.com/science/alphagenome/terms)), and **Google Antigravity & Gemini 4 Argon**.
