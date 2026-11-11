# Quantum-LTC — Open Research & Interactive Results Portal

Live GitHub Pages site: **https://arunnadarasa.github.io/quantum-ltc/**

Interactive 8-Layer Knowledge Graph Explorer: **https://arunnadarasa.github.io/quantum-ltc/knowledge-graph.html**

**Author:** Arun Nadarasa (Innovation Fellow, Mid and South Essex NHS Foundation Trust; International Social Prescribing Pharmacy Association [ISPPA], London, UK)

---

## Included Open-Access Artifacts

- **Compiled Samskrift Monograph (`downloads/Quantum_LTC_Roadmap.pdf`, 10 pp., 29 verified references):**
  - Four-Era Clinical Quantum Optimisation & Simulation Roadmap grounded in the **NHS North Central London ICB Locally Commissioned Service (LCS) for Proactive, Personalised Care — Long Term Conditions (Version 6, 2026–2027)** across 9 Long Term Conditions (CVD, AF, Hypertension Outcome #23, T2D, T1D, CKD, NAFLD/MASLD, COPD, and Adult/CYP Asthma).
  - Strictly decouples sparse PCN scheduling—where exact classical **HiGHS MILP** solves operational instances in `< 25 ms`—from Era III–IV open-system $\mathcal{O}(4^{n_{\text{spin}}})$ multi-organ Lindbladians ($n_{\text{spin}} \ge 16 \implies > 1.92\text{ TB}$ Krylov RAM) and catalytic $\text{Zn}^{2+}$ metalloenzyme active spaces (`PDB 1O86` human `ACE`–Lisinopril, `CAS(36e,26o)` = `52` logical qubits).
- **Interactive Modules (`index.html`, `knowledge-graph.html`):**
  - Real-time **Four-Era Logical-Qubit Roadmap Simulator** (`0` to `160+` logical qubits, `[[8,3,2]]` post-selection yield vs active surface-code + $T$-factory overhead).
  - **Ontology-Grounded Heterogeneous Knowledge Graph Explorer (`57` nodes, `114` directed triples, W3C JSON-LD):** Resolves all 9 NCL LTCs to authoritative **EMBL-EBI OLS4 Human Disease Ontology (`DOID`)** IRIs (`https://www.ebi.ac.uk/ols4/api-docs`), linked to `SNOMED:315594003`, UniProtKB, crystal `PDB 1O86` & `1N9V`, Kashefi Primitives Atlas v0.4, 9 platform receipts, and 6 open NHS DCB0129 hazards.
- **SHA-256-Sealed Provenance Receipts (`receipts/`) & Publication Figures (`figures/`):**
  - `nexus_helios_ltc_receipt.json` (`0e3216dd...`) — Quantinuum Nexus `Helios-1E-lite` (`6,144` cloud emulator shots, `0` physical QPU shots)
  - `haiqu_jij_ltc_receipt.json` (`7212c3d9...`) — Haiqu SDK (`223 -> 26` HUBO LR-QAOA, EME, SU(2), OBP) + JijModeling/OpenJij + HiGHS MILP
  - `biophysical_qprotsim_ltc_receipt.json` (`6ba83347...`) — HQS `struqture-py`/`qoqo`, `QProtSim` (`1N9V`), BioHub, Neurosnap (`1O86`), AlphaGenome Atlas, Arc Institute, Paperclip
  - `modal_roadmap_rhyme_qml_receipt.json` (`cb1fec7c...`) — Modal Cloud, Rhyme (`rhyme-beta`), `QLTCMLM`, $2 \times 2$ Barren Plateau
  - `governance_primitives_jev_receipt.json` (`bd60742f...`) — Text2WetLab (`6/6 PASS`), Medicus FHIR R4 + `ML-DSA-65`, DisCoPy, Moth Blur, Kashefi Primitives Atlas v0.4, TypeSafe Jev 1.14
  - `quantum_ltc_knowledge_graph.json` & `.jsonld` (`c08d35c2...`) — Sealed 57-node / 114-triple property graph & W3C JSON-LD

## External Cloud Links

- **Samskrift Cloud Live Paper View:** https://samskrift.com/view/00aac676-979d-4bcd-b94f-c680a79d1a6f/ed0f2129-55d6-4699-81ae-0bcc2b01b0c3
- **Hugging Face Interactive Space (Live Mirror):** https://huggingface.co/spaces/socialprescribing/quantum-ltc (`https://socialprescribing-quantum-ltc.static.hf.space/index.html`)
- **Hugging Face Model Hub (`QLTCMLM`):** https://huggingface.co/socialprescribing/quantum-ltc-qltcmlm

## Statutory NHS DCB0129 Demarcation

All cohorts, schedules, and FHIR R4 bundles are 100% synthetic (`phi_present = False`, `0` physical QPU shots, `0` wet-lab human specimens). All 6 clinical safety hazards (`H-LTC-01` to `H-LTC-06`) remain **OPEN** under mandatory GP, Clinical Pharmacist, and Tier 2/3 Specialist Nurse human sign-off.

## Acknowledgments

This work was supported in part by complimentary access to Google Antigravity and Gemini 4 Argon to accelerate scientific workflows.
