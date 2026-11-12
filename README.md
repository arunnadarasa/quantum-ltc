# Quantum-LTC — Open Research & Interactive Results Portal

Live GitHub Pages site: **https://arunnadarasa.github.io/quantum-ltc/**

Interactive 8-Layer Knowledge Graph Explorer: **https://arunnadarasa.github.io/quantum-ltc/knowledge-graph.html**

**Author:** Arun Nadarasa (Innovation Fellow, Mid and South Essex NHS Foundation Trust; International Social Prescribing Pharmacy Association [ISPPA], London, UK)

---

## Included Open-Access Artifacts

- **Compiled Samskrift Monograph (`downloads/Quantum_LTC_Roadmap.pdf`, 15 pp., 42 verified references):**
  - Four-Era Clinical Quantum Optimisation & Simulation Roadmap grounded in the **NHS North Central London ICB Locally Commissioned Service (LCS) for Proactive, Personalised Care — Long Term Conditions (Version 6, 2026–2027)** across 9 Long Term Conditions (CVD, AF, Hypertension Outcome #23, T2D, T1D, CKD, NAFLD/MASLD, COPD, and Adult/CYP Asthma).
  - Strictly decouples sparse PCN scheduling (solved in `< 25 ms` by exact classical **HiGHS MILP**) and closed-shell $3d^{10}$ $\text{Zn}^{2+}$ `ACE` chemistry (`PDB 1O86`, `|RCCSD(T) - FCI| <= 0.0154 mHa` in **PySCF 2.15**) from Era III–IV open-shell hepatic **Cytochrome P450 `CYP3A4` Compound I** polypharmacy catalysis (`PDB 1TQN`, `+47.734 mHa = +29.95 kcal/mol` single-reference spin-gap breakdown, `75–141` ancilla-complete Cholesky DF-QPE logical qubits) and open-system $\mathcal{O}(4^{n_{\text{spin}}})$ Lindbladian memory walls (`1.875 TiB` exact Krylov vs MCWF/MPDOs).
- **Interactive Modules (`index.html`, `knowledge-graph.html`):**
  - Real-time **Four-Era Logical-Qubit Roadmap Simulator** (`0` to `180+` logical qubits, `[[8,3,2]]` post-selection yield vs active surface-code + $T$-factory overhead, strict binary `MiB`/`GiB`/`TiB` scaling).
  - **Ontology-Grounded Heterogeneous Knowledge Graph Explorer (`61` nodes, `126` directed triples, W3C JSON-LD):** Resolves all 9 NCL LTCs to authoritative **EMBL-EBI OLS4 Human Disease Ontology (`DOID`)** IRIs (`https://www.ebi.ac.uk/ols4/api-docs`), linked to `SNOMED:315594003`, UniProtKB, crystal `PDB 1TQN` (`CYP3A4`), `1O86` (`ACE`), & `1N9V` (`Ang II`), live **AlphaGenome 2 (`v2.dna_client`)** primary-cell loci (`CYP3A4*22`, `ACE`, `SLC5A2`, `MUC5B`), Kashefi Primitives Atlas v0.4, platform receipts, and 6 open NHS DCB0129 & DCB0160 hazards.
- **SHA-256-Sealed Provenance Receipts (`receipts/`) & Publication Figures (`figures/`):**
  - `nexus_helios_ltc_receipt.json` (`0e3216dd...`) — Quantinuum Nexus `Helios-1E-lite` (`6,144` cloud emulator shots, `0` physical QPU shots)
  - `haiqu_jij_ltc_receipt.json` (`7212c3d9...`) — Haiqu SDK (`223 -> 26` HUBO LR-QAOA, EME, SU(2), OBP) + JijModeling/OpenJij + HiGHS MILP
  - `biophysical_qprotsim_ltc_receipt.json` (`6ba83347...`) — HQS `struqture-py`/`qoqo`, `QProtSim` (`1N9V`), BioHub, Neurosnap (`1O86`), AlphaGenome Atlas, Arc Institute, Paperclip
  - `metalloenzyme_ftqc_ag2_receipt.json` (`1a9541a1...`) — `PySCF 2.15.0` identical-$H_{\text{CAS}}$ single-reference `1O86` vs open-shell `CYP3A4` `1TQN` (`+47.7 mHa` `RCCSD(T)` spin-gap failure, `75–141L` Cholesky DF-QPE) + live `alphagenome==2.0.0` (`v2.dna_client`) primary-cell variant scoring
  - `modal_roadmap_rhyme_qml_receipt.json` (`cb1fec7c...`) — Modal Cloud, Rhyme (`rhyme-beta`), `QLTCMLM`, $2 \times 2$ Barren Plateau
  - `governance_primitives_jev_receipt.json` (`bd60742f...`) — Text2WetLab (`6/6 PASS`), Medicus FHIR R4 + `ML-DSA-65`, DisCoPy, Moth Blur, Kashefi Primitives Atlas v0.4, TypeSafe Jev 1.14
  - `deep_review_remediation_receipt.json` (`a6b3854e...`) — MCWF/MPDO baselines, post-SWAP `project_z(q2)` & 4-state counts, Haiqu uncompressed/compressed & random bitflip controls, OpenJij raw pre-polish (`160/160` feasible) & $C_{p,q}$ bounds, 4-regime decoupled HQS Lindbladian, ancilla-complete `64L/68L` `PDB 1O86`, 5-seed `QLTCMLM` Reservoir & Cubic Poly-LogReg, and Lie algebra $\dim\mathfrak{g}$ audit
  - `quantum_ltc_knowledge_graph.json` & `.jsonld` (`73ee2005...`) — Sealed 61-node / 126-triple property graph & W3C JSON-LD

## External Cloud Links

- **Samskrift Cloud Live Paper View:** https://samskrift.com/view/00aac676-979d-4bcd-b94f-c680a79d1a6f/ed0f2129-55d6-4699-81ae-0bcc2b01b0c3
- **Hugging Face Interactive Space (Live Mirror):** https://huggingface.co/spaces/socialprescribing/quantum-ltc (`https://socialprescribing-quantum-ltc.static.hf.space/index.html`)
- **Hugging Face Model Hub (`QLTCMLM`):** https://huggingface.co/socialprescribing/quantum-ltc-qltcmlm

## Statutory NHS DCB0129 & DCB0160 Demarcation

All cohorts, schedules, and FHIR R4 bundles are 100% synthetic (`phi_present = False`, `0` physical QPU shots, `0` wet-lab human specimens). All 6 clinical safety hazards (`H-LTC-01` to `H-LTC-06`) remain **OPEN** across manufacturer (DCB0129) and deploying NCL ICB / PCN (DCB0160) clinical risk logs under mandatory GP, Clinical Pharmacist, and Tier 2/3 Specialist Nurse human sign-off.

## Acknowledgments

This work was supported in part by complimentary access to Google Antigravity and Gemini 4 Argon to accelerate scientific workflows.
