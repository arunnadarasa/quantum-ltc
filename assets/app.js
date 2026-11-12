// Quantum-LTC — Interactive Clinical Quantum Optimisation & Simulation Portal Module
// Matched UX Architecture with Quantum Social Prescribing (https://arunnadarasa.github.io/quantum-social-prescribing/)

const BOOKMARKS = [
  { label: "p.1 · Abstract & NCL LTC Spec", page: 1 },
  { label: "p.3 · 4-Era Roadmap & Baselines", page: 3 },
  { label: "p.5 · Nexus Helios-1E & Haiqu HUBO", page: 5 },
  { label: "p.7 · 4-Regime HQS & PDB 1O86", page: 7 },
  { label: "p.9 · PySCF 1TQN vs 1O86 & AlphaGenome 2", page: 9 },
  { label: "p.11 · Gate 1: PDB 5TE8/3NXU, THC & ChEMBL340", page: 11 },
  { label: "p.12 · 5-Seed Modal QLTCMLM & Barren Plateau", page: 12 },
  { label: "p.14 · Jev 1.14 & DCB0129/0160 Audit", page: 14 },
  { label: "p.15 · 64-Node KG & 47 Verified Refs", page: 15 }
];

// Slider UI values in [0, 1], mapped to centered [-1, 1] via x_c = 2*u - 1
const CLINICAL_PRESETS = [
  {
    name: "Cardiorenal Triple-Whammy Risk",
    u: [0.86, 0.72, 0.84, 0.35, 0.88, 0.82, 0.60, 0.76]
  },
  {
    name: "CYP Asthma 48h + High-GWP SABA",
    u: [0.28, 0.30, 0.24, 0.92, 0.44, 0.85, 0.48, 0.94]
  },
  {
    name: "Hypertension #23 Home Telemonitoring",
    u: [0.84, 0.38, 0.32, 0.20, 0.26, 0.45, 0.25, 0.22]
  },
  {
    name: "MASLD + T2D + Interpreter Equity",
    u: [0.58, 0.88, 0.76, 0.34, 0.62, 0.90, 0.92, 0.58]
  },
  {
    name: "Stable Low-Risk Annual Digital YoC",
    u: [0.22, 0.24, 0.18, 0.16, 0.15, 0.30, 0.18, 0.12]
  }
];

const FEATURE_META = [
  { key: "f0_systolic_bp_excess", label: "Systolic BP Excess (#23)" },
  { key: "f1_glycaemic_hepatic_load", label: "HbA1c / MASLD Load" },
  { key: "f2_renal_uacr_egfr_decline", label: "CKD uACR / eGFR Decline" },
  { key: "f3_airway_saba_exacerbation", label: "Asthma/COPD + SABA Load" },
  { key: "f4_polypharmacy_nsaid_clash", label: "NSAID / Polypharmacy Clash" },
  { key: "f5_imd_core20_deprivation", label: "Core20 IMD Quintile 1" },
  { key: "f6_interpreter_access_barrier", label: "SNOMED Interpreter Need" },
  { key: "f7_winter_admissions_history", label: "Prior Winter / 48h Attack" }
];

const BUNDLE_NAMES = [
  "Bundle 0 · BP #23 ACEi + Home Telemonitoring",
  "Bundle 1 · Cardiorenal SGLT2i + Green PCSP",
  "Bundle 2 · Net-Zero DPI MART + 48h CYP Asthma",
  "Bundle 3 · Complex Tier-3 MDT + Pharmacist SMR + Interpreter"
];

const RISK_NAMES = [
  "Low Risk · Supported Self-Care",
  "Moderate Risk · Annual Year-of-Care",
  "High Risk · Pre-Winter Proactive Recall",
  "High + Complex Risk · Multi-Specialty PCN MDT"
];

const BLOCH_CUES = {
  H: "Stage 2 Info Sharing · Hadamard H — Pre-visit results & agenda preparation opens coherent Year-of-Care superposition (|0⟩+|1⟩)/√2.",
  RX: "Pharmacist SMR · Rx(π/2) — Structured Medication Review resolves ACEi + SGLT2i + NSAID triple-whammy clashes across the meridian.",
  S: "Net-Zero MART · Phase S = Rz(π/2) — Dry-powder MART switch aligns airway inflammation control with NCL Green Plan decarbonisation.",
  Z: "Cardiorenal Sync · Pauli-Z — Dual RAAS/SGLT2 protection inverts destructive glomerular hyperfiltration phase (+1 → −1).",
  ZENO: "Pre-Winter / 48h CYP Check — Proactive MCMR recall locks high-risk retention near |0⟩ (R² = 0.9979 on live Nexus Helios-1E-lite Job 464be33a).",
  COLLAPSE: "Siloed Single-Disease Clinic — Mid-circuit projective collapse degrades MDT coherence from 0.9961 ± 0.0014 to 0.5020 ± 0.0110.",
  RESET: "Reset |0⟩ — Return patient Year-of-Care trajectory to unified House-of-Care baseline (+Z north pole)."
};

const DISCOPY_STEPS = [
  {
    short: "1. η_MDT Cap",
    title: "Layer 1 · Stage 1 Check-and-Test Shared Diagnostic Cap η_MDT : I → C ⊗ R",
    circuit: "Ket(0, 0) >> (H @ Id(1)) >> CX",
    desc: "Single phlebotomy, uACR, FeNO/spirometry, and home BP check-and-test prepares a shared cardiorenal-respiratory entangled diagnostic frame |Φ+⟩."
  },
  {
    short: "2. Ry ⊗ Rz",
    title: "Layer 2 · Parallel Cardiorenal & Airway Optimization (ACEi/SGLT2i ⊗ DPI MART)",
    circuit: "Ry(θ_Cardiorenal) @ Rz(φ_Respiratory)",
    desc: "Evaluates renal/glycaemic protection in tensor product with high-GWP SABA → dry-powder MART transition without prematurely collapsing regimen options."
  },
  {
    short: "3. σ Handoff",
    title: "Layer 3 · Symmetric PCN Multidisciplinary Handoff σ_{C,R}",
    circuit: "SWAP(0, 1)  [Post-SWAP project_z(q2) Algebraic Identity Verified]",
    desc: "Coherent handoff between GP, Clinical Pharmacist SMR, and Tier 2/3 Specialist Nurse preserves off-diagonal pathway correlations."
  },
  {
    short: "4. Stage 3 PCSP",
    title: "Layer 4 · Co-Produced Stage 3 Personalised Care & Support Plan (PCSP)",
    circuit: "Rz†(φ_Respiratory) @ Ry†(θ_Cardiorenal)",
    desc: "Integrates SNOMED 315594003 interpreter support, Core20 IMD equity weighting, and Stage 4 VCSE social prescribing follow-up."
  },
  {
    short: "5. ε_MDT Lock",
    title: "Layer 5 · Unified Year-of-Care Lock ε_MDT on Live Quantinuum Nexus Helios-1E-lite",
    circuit: "CX >> (H @ Id(1)) >> Measure  [P(00) = 0.9961 ± 0.0014 vs 0.5020 ± 0.0110 Siloed]",
    desc: "Equal-unitary-depth verification on live Nexus Helios-1E-lite (Job 5da15d5a, 2,048 shots/branch) locks onto |00⟩ (2,040/2,048 shots) vs 1,028/2,048 under siloed mid-circuit collapse."
  }
];

const BIBTEX_ENTRIES = {
  monograph: `@article{nadarasa2026quantumltc,
  title   = {Quantum-{LTC}: A Four-Era Logical-Qubit Clinical Optimisation and Biophysical Simulation Roadmap for Multimorbid Long Term Conditions in the {NHS}},
  author  = {Nadarasa, Arun},
  year    = {2026},
  month   = nov,
  journal = {Samskrift Clinical Quantum Computing Monograph (Mid and South Essex NHS Foundation Trust \\& ISPPA)},
  pages   = {1--15},
  url     = {https://arunnadarasa.github.io/quantum-ltc/},
  note    = {Grounded in NHS North Central London ICB LTC LCS v6 (9 LTCs); 0 physical QPU shots; 8 SHA-256-sealed receipts across Quantinuum Nexus Helios-1E-lite, Haiqu, OpenJij, HiGHS MILP, HQS, QProtSim, PySCF 2.15 (CYP3A4 PDB 1TQN vs ACE PDB 1O86), AlphaGenome 2, Modal, and TypeSafe Jev 1.14 under NHS DCB0129 \\& DCB0160}
}`,
  qltcmlm: `@misc{nadarasa2026qltcmlm,
  title        = {{QLTCMLM}: 4-Qubit Frobenius Data-Reuploading Multi-Task Variational Quantum Classifier for Multimorbid {NHS} {LTC} Risk Stratification},
  author       = {Nadarasa, Arun},
  year         = {2026},
  howpublished = {Hugging Face Model Hub \\& Interactive Space},
  url          = {https://huggingface.co/socialprescribing/quantum-ltc-qltcmlm},
  note         = {200 trainable params (72 quantum + 128 readout); 5-seed benchmark against untrained quantum reservoir, QKernel, GBDT, RBF-SVM, and Cubic Poly-LogReg}
}`,
  ncl_lcs: `@techreport{ncl_icb_ltc_v6_2026,
  title       = {Locally Commissioned Service Specification: Proactive, Personalised Care --- Long Term Conditions (Version 6, 2026--2027)},
  author      = {{NHS North Central London Integrated Care Board}},
  institution = {NHS North Central London ICB (Barnet, Camden, Enfield, Haringey, and Islington)},
  year        = {2026},
  note        = {Unified Year-of-Care / House-of-Care specification covering CVD, AF, Hypertension Outcome \\#23, T2D, T1D, CKD, NAFLD/MASLD, COPD, and Adult/CYP Asthma}
}`,
  dcb_safety: `@techreport{nhs_dcb0129_0160,
  title       = {{DCB0129} \\& {DCB0160}: Clinical Risk Management Standards in the Manufacture and Deployment of Health {IT} Systems},
  author      = {{NHS England}},
  institution = {NHS England Transformation Directorate},
  year        = {2026},
  url         = {https://digital.nhs.uk/data-and-information/information-standards/information-standards-and-data-collections-including-extractions/publications-and-notifications/standards-and-collections/dcb0129-clinical-risk-management-its-application-in-the-manufacture-of-health-it-systems}
}`
};

let PORTAL_DATA = null;
let QLTC_WEIGHTS = null;
let currentU = [...CLINICAL_PRESETS[0].u];

function showToast(msg) {
  const el = document.getElementById("toast");
  if (!el) return;
  el.textContent = msg;
  el.classList.add("show");
  clearTimeout(showToast._t);
  showToast._t = setTimeout(() => el.classList.remove("show"), 2300);
}

/* ── 1. Sticky Navigation, Scroll-Spy & Mobile Drawer ── */
function initNav() {
  const bar = document.getElementById("scroll-progress");
  const topBtn = document.getElementById("back-to-top");
  const toggle = document.getElementById("menu-toggle");
  const nav = document.getElementById("primary-nav");
  const links = [...document.querySelectorAll("#primary-nav a")];
  const sections = links.map(a => document.querySelector(a.getAttribute("href"))).filter(Boolean);

  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    links.forEach(a => a.addEventListener("click", () => {
      nav.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
    }));
  }

  window.addEventListener("scroll", () => {
    const max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    const pct = Math.min(100, Math.max(0, (window.scrollY / max) * 100));
    if (bar) bar.style.width = pct + "%";
    if (topBtn) topBtn.classList.toggle("visible", window.scrollY > 480);

    let activeIdx = 0;
    sections.forEach((sec, idx) => {
      if (sec.getBoundingClientRect().top <= 130) activeIdx = idx;
    });
    links.forEach((a, idx) => a.classList.toggle("active", idx === activeIdx));
  }, { passive: true });

  if (topBtn) topBtn.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
}

/* ── 2. In-Page PDF.js Reader (13-Page Samskrift Monograph + High-DPI PNG Fallback) ── */
async function initPdfReader() {
  const stream = document.getElementById("reader-canvas-stream");
  const viewportEl = document.getElementById("reader-viewport");
  const pageInput = document.getElementById("reader-page-input");
  const pageCountEl = document.getElementById("reader-page-count");
  const zoomLabel = document.getElementById("reader-zoom-label");
  const bmWrap = document.getElementById("reader-bookmarks");
  const panel = document.getElementById("paper-preview-panel");
  if (!stream || !viewportEl) return;

  const DOC = {
    pdfUrl: "downloads/Quantum_LTC_Roadmap.pdf",
    pagesDir: "pages",
    totalPages: 17,
    altTitle: "Quantum-LTC Four-Era Samskrift Monograph"
  };

  let zoom = 1.0;
  let renderEpoch = 0;

  if (pageInput) pageInput.max = String(DOC.totalPages);
  if (pageCountEl) pageCountEl.textContent = String(DOC.totalPages);

  bmWrap.innerHTML = "";
  BOOKMARKS.forEach((bm, idx) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "bookmark-chip" + (idx === 0 ? " active" : "");
    btn.textContent = bm.label;
    btn.addEventListener("click", () => {
      document.querySelectorAll(".bookmark-chip").forEach(c => c.classList.remove("active"));
      btn.classList.add("active");
      scrollToPage(bm.page);
    });
    bmWrap.appendChild(btn);
  });

  function scrollToPage(p) {
    const clamped = Math.min(DOC.totalPages, Math.max(1, p));
    pageInput.value = String(clamped);
    const slot = stream.querySelector(`[data-page="${clamped}"]`);
    if (slot) slot.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function renderFallbackImages() {
    stream.innerHTML = "";
    const baseW = Math.min(860, viewportEl.clientWidth - 36) * zoom;
    for (let p = 1; p <= DOC.totalPages; p++) {
      const slot = document.createElement("div");
      slot.className = "pdf-page-slot";
      slot.dataset.page = String(p);
      slot.style.width = `${Math.max(300, baseW)}px`;
      const img = document.createElement("img");
      img.className = "pdf-fallback-img";
      img.src = `${DOC.pagesDir}/page_${p}.png`;
      img.alt = `${DOC.altTitle} — Page ${p} of ${DOC.totalPages}`;
      img.loading = p <= 2 ? "eager" : "lazy";
      const badge = document.createElement("span");
      badge.className = "pdf-page-badge";
      badge.textContent = `Page ${p} / ${DOC.totalPages}`;
      slot.appendChild(img);
      slot.appendChild(badge);
      stream.appendChild(slot);
    }
  }

  async function renderPdfJs(epoch) {
    if (!window.pdfjsLib) {
      renderFallbackImages();
      return;
    }
    try {
      window.pdfjsLib.GlobalWorkerOptions.workerSrc =
        "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";
      const pdf = await window.pdfjsLib.getDocument(DOC.pdfUrl).promise;
      if (epoch !== renderEpoch) return;
      stream.innerHTML = "";
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const targetW = Math.max(310, Math.min(860, viewportEl.clientWidth - 36) * zoom);
      for (let p = 1; p <= pdf.numPages; p++) {
        if (epoch !== renderEpoch) return;
        const page = await pdf.getPage(p);
        if (epoch !== renderEpoch) return;
        const vp0 = page.getViewport({ scale: 1 });
        const scale = targetW / vp0.width;
        const vp = page.getViewport({ scale: scale * dpr });
        const slot = document.createElement("div");
        slot.className = "pdf-page-slot";
        slot.dataset.page = String(p);
        const canvas = document.createElement("canvas");
        canvas.width = vp.width;
        canvas.height = vp.height;
        canvas.style.width = `${Math.round(vp.width / dpr)}px`;
        canvas.style.height = `${Math.round(vp.height / dpr)}px`;
        const badge = document.createElement("span");
        badge.className = "pdf-page-badge";
        badge.textContent = `Page ${p} / ${pdf.numPages}`;
        slot.appendChild(canvas);
        slot.appendChild(badge);
        stream.appendChild(slot);
        await page.render({ canvasContext: canvas.getContext("2d"), viewport: vp }).promise;
      }
    } catch (_) {
      if (epoch === renderEpoch) renderFallbackImages();
    }
  }

  renderFallbackImages();
  setTimeout(() => renderPdfJs(++renderEpoch), 300);

  document.getElementById("reader-prev-page")?.addEventListener("click", () => scrollToPage(Number(pageInput.value) - 1));
  document.getElementById("reader-next-page")?.addEventListener("click", () => scrollToPage(Number(pageInput.value) + 1));
  pageInput?.addEventListener("change", () => scrollToPage(Number(pageInput.value)));

  function updateZoom(newZoom) {
    zoom = Math.min(1.75, Math.max(0.65, newZoom));
    zoomLabel.textContent = `${Math.round(zoom * 100)}%`;
    renderEpoch++;
    renderFallbackImages();
  }
  document.getElementById("reader-zoom-in")?.addEventListener("click", () => updateZoom(zoom + 0.15));
  document.getElementById("reader-zoom-out")?.addEventListener("click", () => updateZoom(zoom - 0.15));
  document.getElementById("reader-zoom-fit")?.addEventListener("click", () => updateZoom(1.0));

  document.getElementById("reader-tall-btn")?.addEventListener("click", () => panel.classList.toggle("tall"));
  document.getElementById("reader-collapse-btn")?.addEventListener("click", (e) => {
    const collapsed = panel.classList.toggle("collapsed");
    e.currentTarget.textContent = collapsed ? "▸ Show" : "▾ Hide";
  });
  document.getElementById("reader-fullscreen-btn")?.addEventListener("click", (e) => {
    const fs = panel.classList.toggle("fullscreen");
    e.currentTarget.textContent = fs ? "✕ Exit Fullscreen" : "⛶ Fullscreen";
  });

  viewportEl.addEventListener("scroll", () => {
    const slots = [...stream.querySelectorAll(".pdf-page-slot")];
    const topRef = viewportEl.getBoundingClientRect().top + 120;
    for (const s of slots) {
      const r = s.getBoundingClientRect();
      if (r.bottom >= topRef) {
        pageInput.value = s.dataset.page;
        break;
      }
    }
  }, { passive: true });
}

/* ── 3A. Exact 4-Qubit Complex Statevector QLTCMLM Engine (< 1e-15 Float64 Parity) ── */
function buildQLTCStructure() {
  const p01 = Array.from({ length: 16 }, (_, i) => i ^ (i & 8 ? 4 : 0));
  const p12 = Array.from({ length: 16 }, (_, i) => i ^ (i & 4 ? 2 : 0));
  const p23 = Array.from({ length: 16 }, (_, i) => i ^ (i & 2 ? 1 : 0));
  const p30 = Array.from({ length: 16 }, (_, i) => i ^ (i & 1 ? 8 : 0));
  const czDiag = Float64Array.from({ length: 16 }, (_, idx) =>
    ((idx & 8) && (idx & 2) ? -1.0 : 1.0) * ((idx & 4) && (idx & 1) ? -1.0 : 1.0)
  );
  const zSigns = Array.from({ length: 4 }, (_, q) =>
    Float64Array.from({ length: 16 }, (_, idx) => (((idx >> (3 - q)) & 1) === 0 ? 1.0 : -1.0))
  );
  const pairs = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]];
  const zzSigns = pairs.map(([a, b]) =>
    Float64Array.from({ length: 16 }, (_, idx) => zSigns[a][idx] * zSigns[b][idx])
  );
  const zzzzSign = Float64Array.from({ length: 16 }, (_, idx) =>
    zSigns[0][idx] * zSigns[1][idx] * zSigns[2][idx] * zSigns[3][idx]
  );
  return { p01, p12, p23, p30, czDiag, zSigns, zzSigns, zzzzSign };
}

const QLTC_STRUCT = buildQLTCStructure();

function applyPerm16(re, im, perm) {
  const nRe = new Float64Array(16);
  const nIm = new Float64Array(16);
  for (let i = 0; i < 16; i++) {
    nRe[i] = re[perm[i]];
    nIm[i] = im[perm[i]];
  }
  return [nRe, nIm];
}

function softmax(arr) {
  const m = Math.max(...arr);
  const ex = arr.map(v => Math.exp(v - m));
  const s = ex.reduce((a, b) => a + b, 0);
  return ex.map(v => v / s);
}

export function runQLTCMLM(xCentered, weightsObj) {
  const W = weightsObj.weights;
  let re = new Float64Array(16);
  let im = new Float64Array(16);
  re[0] = 1.0;

  for (let l = 0; l < 3; l++) {
    for (let q = 0; q < 4; q++) {
      const xa = xCentered[q];
      const xb = xCentered[q + 4];
      const angY = W.theta_w[l][q][0] * xa + W.theta_b[l][q][0];
      const angZ = W.theta_w[l][q][1] * xb + W.theta_b[l][q][1];
      const angX = W.theta_w[l][q][2] * (xa * xb) + W.theta_b[l][q][2];
      const step = 1 << (3 - q);

      // RY(angY)
      const cy = Math.cos(0.5 * angY), sy = Math.sin(0.5 * angY);
      const outYRe = new Float64Array(re), outYIm = new Float64Array(im);
      for (let base = 0; base < 16; base += 2 * step) {
        for (let k = 0; k < step; k++) {
          const i0 = base + k, i1 = base + step + k;
          outYRe[i0] = cy * re[i0] - sy * re[i1];
          outYIm[i0] = cy * im[i0] - sy * im[i1];
          outYRe[i1] = sy * re[i0] + cy * re[i1];
          outYIm[i1] = sy * im[i0] + cy * im[i1];
        }
      }
      re = outYRe; im = outYIm;

      // RZ(angZ)
      const cz = Math.cos(0.5 * angZ), sz = Math.sin(0.5 * angZ);
      for (let base = 0; base < 16; base += 2 * step) {
        for (let k = 0; k < step; k++) {
          const i0 = base + k, i1 = base + step + k;
          const r0 = re[i0], m0 = im[i0];
          re[i0] = r0 * cz + m0 * sz;
          im[i0] = m0 * cz - r0 * sz;
          const r1 = re[i1], m1 = im[i1];
          re[i1] = r1 * cz - m1 * sz;
          im[i1] = m1 * cz + r1 * sz;
        }
      }

      // RX(angX)
      const cx = Math.cos(0.5 * angX), sx = Math.sin(0.5 * angX);
      const outXRe = new Float64Array(re), outXIm = new Float64Array(im);
      for (let base = 0; base < 16; base += 2 * step) {
        for (let k = 0; k < step; k++) {
          const i0 = base + k, i1 = base + step + k;
          outXRe[i0] = cx * re[i0] + sx * im[i1];
          outXIm[i0] = cx * im[i0] - sx * re[i1];
          outXRe[i1] = sx * im[i0] + cx * re[i1];
          outXIm[i1] = -sx * re[i0] + cx * im[i1];
        }
      }
      re = outXRe; im = outXIm;
    }

    [re, im] = applyPerm16(re, im, QLTC_STRUCT.p01);
    [re, im] = applyPerm16(re, im, QLTC_STRUCT.p12);
    [re, im] = applyPerm16(re, im, QLTC_STRUCT.p23);
    [re, im] = applyPerm16(re, im, QLTC_STRUCT.p30);
    for (let i = 0; i < 16; i++) {
      re[i] *= QLTC_STRUCT.czDiag[i];
      im[i] *= QLTC_STRUCT.czDiag[i];
    }
  }

  const probs = new Float64Array(16);
  let shannon = 0;
  for (let i = 0; i < 16; i++) {
    const p = re[i] * re[i] + im[i] * im[i];
    probs[i] = p;
    if (p > 1e-12) shannon -= p * Math.log2(p);
  }

  const feats = [];
  for (let q = 0; q < 4; q++) {
    let s = 0;
    for (let i = 0; i < 16; i++) s += probs[i] * QLTC_STRUCT.zSigns[q][i];
    feats.push(s);
  }
  for (let q = 0; q < 4; q++) {
    const step = 1 << (3 - q);
    let acc = 0;
    for (let base = 0; base < 16; base += 2 * step) {
      for (let k = 0; k < step; k++) {
        const i0 = base + k, i1 = base + step + k;
        acc += 2.0 * (re[i0] * re[i1] + im[i0] * im[i1]);
      }
    }
    feats.push(acc);
  }
  for (let pIdx = 0; pIdx < 6; pIdx++) {
    let s = 0;
    for (let i = 0; i < 16; i++) s += probs[i] * QLTC_STRUCT.zzSigns[pIdx][i];
    feats.push(s);
  }
  {
    let s = 0;
    for (let i = 0; i < 16; i++) s += probs[i] * QLTC_STRUCT.zzzzSign[i];
    feats.push(s);
  }
  feats.push(1.0); // bias

  const riskLogits = [0, 1, 2, 3].map(c =>
    feats.reduce((acc, fVal, r) => acc + fVal * W.W_risk[r][c], 0)
  );
  const bundleLogits = [0, 1, 2, 3].map(c =>
    feats.reduce((acc, fVal, r) => acc + fVal * W.W_bundle[r][c], 0)
  );

  return {
    probs,
    shannon,
    riskProbs: softmax(riskLogits),
    bundleProbs: softmax(bundleLogits),
    zzzzParity: feats[14]
  };
}

function initQLTCMLMSimulator() {
  const presetWrap = document.getElementById("qltc-presets");
  const sliderWrap = document.getElementById("qltc-sliders");
  const hilbertWrap = document.getElementById("qltc-hilbert-bars");
  const bundleWrap = document.getElementById("qltc-bundle-bars");
  if (!presetWrap || !sliderWrap || !hilbertWrap || !bundleWrap) return;

  for (let i = 0; i < 16; i++) {
    const col = document.createElement("div");
    col.className = "h-bar-col";
    const fill = document.createElement("div");
    fill.className = "h-bar-fill";
    fill.id = `hbar-${i}`;
    const lbl = document.createElement("span");
    lbl.className = "h-bar-lbl";
    lbl.textContent = i.toString(2).padStart(4, "0");
    col.appendChild(fill);
    col.appendChild(lbl);
    hilbertWrap.appendChild(col);
  }

  BUNDLE_NAMES.forEach((name, idx) => {
    const row = document.createElement("div");
    row.className = "pw-row";
    row.innerHTML = `
      <div class="pw-head">
        <span>${name}</span>
        <strong id="pw-pct-${idx}" style="font-family:var(--font-mono)">0.0%</strong>
      </div>
      <div class="pw-track"><div id="pw-fill-${idx}" class="pw-fill" style="width:0%"></div></div>
    `;
    bundleWrap.appendChild(row);
  });

  FEATURE_META.forEach((f, idx) => {
    const row = document.createElement("div");
    row.className = "f-slider-row";
    row.innerHTML = `
      <label for="f-sl-${idx}">${f.label}</label>
      <input id="f-sl-${idx}" type="range" min="0" max="100" value="${Math.round(currentU[idx] * 100)}" />
      <span id="f-val-${idx}" class="f-slider-val">${currentU[idx].toFixed(2)}</span>
    `;
    sliderWrap.appendChild(row);
    row.querySelector("input").addEventListener("input", (e) => {
      currentU[idx] = Number(e.target.value) / 100;
      document.getElementById(`f-val-${idx}`).textContent = currentU[idx].toFixed(2);
      presetWrap.querySelectorAll(".preset-chip").forEach(c => c.classList.remove("active"));
      renderInference();
    });
  });

  CLINICAL_PRESETS.forEach((pr, idx) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "preset-chip" + (idx === 0 ? " active" : "");
    btn.textContent = pr.name;
    btn.addEventListener("click", () => {
      presetWrap.querySelectorAll(".preset-chip").forEach(c => c.classList.remove("active"));
      btn.classList.add("active");
      currentU = [...pr.u];
      currentU.forEach((v, k) => {
        document.getElementById(`f-sl-${k}`).value = String(Math.round(v * 100));
        document.getElementById(`f-val-${k}`).textContent = v.toFixed(2);
      });
      renderInference();
    });
    presetWrap.appendChild(btn);
  });

  function renderInference() {
    if (!QLTC_WEIGHTS) return;
    const xCentered = currentU.map(u => 2.0 * u - 1.0);
    const res = runQLTCMLM(xCentered, QLTC_WEIGHTS);
    const maxH = Math.max(0.18, ...res.probs);
    for (let i = 0; i < 16; i++) {
      const bar = document.getElementById(`hbar-${i}`);
      if (bar) bar.style.height = `${Math.max(4, Math.round((res.probs[i] / maxH) * 62))}px`;
    }

    let topB = 0;
    res.bundleProbs.forEach((p, idx) => { if (p > res.bundleProbs[topB]) topB = idx; });
    res.bundleProbs.forEach((p, idx) => {
      document.getElementById(`pw-pct-${idx}`).textContent = `${(p * 100).toFixed(1)}%`;
      const fill = document.getElementById(`pw-fill-${idx}`);
      fill.style.width = `${(p * 100).toFixed(1)}%`;
      fill.classList.toggle("top", idx === topB);
    });

    let topR = 0;
    res.riskProbs.forEach((p, idx) => { if (p > res.riskProbs[topR]) topR = idx; });

    document.getElementById("qltc-top-badge").textContent = RISK_NAMES[topR].split("·")[0].trim();
    document.getElementById("qltc-entropy-txt").textContent = `H(ψ) = ${res.shannon.toFixed(2)} bits`;
    document.getElementById("qltc-risk-out").textContent = `${RISK_NAMES[topR]} (${(res.riskProbs[topR] * 100).toFixed(1)}%)`;
    document.getElementById("qltc-parity-out").textContent = `⟨Z₀Z₁Z₂Z₃⟩ = ${res.zzzzParity >= 0 ? "+" : ""}${res.zzzzParity.toFixed(3)}`;

    const safetyBox = document.getElementById("qltc-safety-box");
    const tripleWhammy = currentU[0] >= 0.70 && currentU[2] >= 0.70 && currentU[4] >= 0.72;
    const cyp48h = currentU[3] >= 0.80 && currentU[7] >= 0.80;
    const escalate = tripleWhammy || cyp48h || topR >= 2;
    safetyBox.classList.toggle("escalate", tripleWhammy || cyp48h);
    if (cyp48h) {
      safetyBox.innerHTML = `<strong>⚠ NHS DCB0129 / DCB0160 Urgent Gate (H-LTC-03 · OPEN):</strong> High airway SABA burden (<code>${currentU[3].toFixed(2)}</code>) with acute post-attack flag (<code>${currentU[7].toFixed(2)}</code>). Bypass batch QUBO/VQC scheduling — route directly to <strong>2-working-day Tier 2/3 CYP Asthma Clinician review</strong>.`;
    } else if (tripleWhammy) {
      safetyBox.innerHTML = `<strong>⚠ NHS DCB0129 / DCB0160 Pharmacovigilance Gate (H-LTC-02 · OPEN):</strong> Concurrent BP/CKD burden with nephrotoxic NSAID clash (<code>${currentU[4].toFixed(2)}</code>). Mandatory human <strong>Clinical Pharmacist SMR &amp; baseline eGFR/K⁺ check</strong> before ACEi/ARB + SGLT2i co-initiation.`;
    } else {
      safetyBox.innerHTML = `<strong>✓ Advisory Sandbox Decision-Support Mode (DCB0129 &amp; DCB0160 Human-in-the-Loop):</strong> Classical Cubic Poly-LogReg (<code>66.2% / 87.4%</code>) &amp; RBF-SVM remain primary Era I–II baselines; GP, Pharmacist, and Specialist Nurse retain 100% clinical authority.`;
    }
  }

  renderInference();
}

/* ── 3B. Four-Era Logical-Qubit Roadmap Simulator (Strict Binary MiB/GiB/TiB + MCWF/MPDO) ── */
function initEraSimulator() {
  const slider = document.getElementById("nq-slider");
  if (!slider) return;
  const nqVal = document.getElementById("nq-val");
  const eraPill = document.getElementById("era-pill");
  const organScale = document.getElementById("organ-scale");
  const organSub = document.getElementById("organ-sub");
  const ramScale = document.getElementById("ram-scale");
  const ramSub = document.getElementById("ram-sub");
  const physScale = document.getElementById("phys-scale");
  const physSub = document.getElementById("phys-sub");
  const verdictScale = document.getElementById("verdict-scale");
  const verdictSub = document.getElementById("verdict-sub");

  function formatKrylovBinary(nSpin) {
    if (nSpin <= 2) return "< 1 MiB";
    const bytes = 30 * 16 * Math.pow(4, nSpin);
    const gib = bytes / Math.pow(1024, 3);
    if (gib < 1) return (gib * 1024).toFixed(2) + " MiB";
    if (gib < 1024) return gib.toFixed(2) + " GiB";
    const tib = gib / 1024;
    if (tib < 1024) return tib.toFixed(3) + " TiB";
    return (tib / 1024).toFixed(1) + " PiB";
  }

  function formatMcwfMib(nSpin) {
    const mib = (16 * Math.pow(2, nSpin)) / Math.pow(1024, 2);
    if (mib < 1) return (mib * 1024).toFixed(1) + " KiB/traj";
    if (mib < 1024) return mib.toFixed(2) + " MiB/traj";
    return (mib / 1024).toFixed(2) + " GiB/traj";
  }

  function updateEra() {
    const nL = parseInt(slider.value, 10);
    nqVal.textContent = String(nL);
    if (nL === 0) {
      eraPill.textContent = "Era I · Classical-Exact & NISQ Hardware Readiness (0 Logical)";
      eraPill.className = "pill pill-signal";
      organScale.textContent = "4-Spin Toy / 128-Var QUBO";
      organSub.textContent = "8-var HUBO + NCL PCN Call-Recall";
      ramScale.textContent = "0.12 MiB Krylov";
      ramSub.textContent = "MCWF: 0.25 KiB/traj (36.6 ms exact)";
      physScale.textContent = "4–20 phys / Cloud Emul.";
      physSub.textContent = "6,144 Nexus Helios-1E-lite shots";
      verdictScale.textContent = "Classical HiGHS (<25 ms)";
      verdictScale.style.color = "var(--amber)";
      verdictSub.textContent = "4.3 ms QUBO · 23.0 ms McCormick HUBO";
    } else if (nL <= 24) {
      const blocks = Math.ceil(nL / 3);
      const pAcc = Math.pow(1 - 0.0012, blocks * 8 * Math.max(6, nL)) * 100;
      const nSpin = Math.max(4, Math.floor((nL - 2) / 2));
      eraPill.textContent = "Era II · Error-Detected [[8,3,2]] Color-Code Regime";
      eraPill.className = "pill pill-amber";
      organScale.textContent = `${nSpin} Coupled Spins`;
      organSub.textContent = `[[8,3,2]] iceberg/color code (${blocks} blocks)`;
      ramScale.textContent = formatKrylovBinary(nSpin);
      ramSub.textContent = `MCWF: ${formatMcwfMib(nSpin)} · MPDO χ=64 ≤3 MiB`;
      physScale.textContent = `${blocks * 8 + 8} phys qubits`;
      physSub.textContent = `Post-selection yield ~${pAcc.toFixed(1)}%`;
      verdictScale.textContent = "Classical MCWF / MPDO / MILP";
      verdictScale.style.color = "var(--amber)";
      verdictSub.textContent = "Exponential post-selection limits depth";
    } else if (nL <= 84) {
      const nSpin = Math.floor((nL - 6) / 2);
      const isCyp = nL >= 72;
      const d = isCyp ? 19 : (nL >= 64 ? 17 : (nL >= 50 ? 13 : 11));
      const phys = isCyp ? 90250 : Math.round((Math.ceil(1.5 * nL) + 12) * 2 * d * d);
      eraPill.textContent = "Era III · Active FTQC Simulation Crossover (38–75 Logical)";
      eraPill.className = "pill pill-signal";
      organScale.textContent = isCyp ? `CYP3A4 1TQN CAS(27e,26o) · ${nL}L` : (nL >= 64 ? `ACE 1O86 Control · ${nL}L` : `${nSpin} Organ Spins (${nL}L)`);
      organSub.textContent = isCyp ? "Open-shell Compound I Cholesky DF-QPE" : (nL >= 64 ? "Closed-shell 3d¹⁰ (RCCSD(T) ≤0.015 mHa)" : "Dilated Lindbladian channel");
      ramScale.textContent = isCyp ? "1,574 TiB FCI Wall" : formatKrylovBinary(nSpin);
      ramSub.textContent = isCyp ? "RCCSD(T) fails by +47.7 mHa (29.8×)" : `MCWF: ${formatMcwfMib(nSpin)} (10⁶ shots @ ε=10⁻³)`;
      physScale.textContent = `~${phys.toLocaleString()} phys`;
      physSub.textContent = `Rotated surface code d=${d} + T-factory`;
      verdictScale.textContent = isCyp ? "Open-Shell DF-QPE Advantage" : (nL >= 64 ? "Single-Ref CC Solvable" : (nSpin >= 16 ? "Projected Lindblad Crossover" : "Approaching 1 TiB Wall"));
      verdictScale.style.color = (isCyp || (nSpin >= 16 && nL < 64)) ? "var(--signal)" : "var(--amber)";
      verdictSub.textContent = isCyp ? "Beats FCI >1 TiB & single-ref CC breakdown" : (nL >= 64 ? "Closed-shell Zn²⁺ negative control" : "Beats >1.875 TiB Krylov & volume-law MPDO");
    } else {
      const isDrugCyp = nL >= 136 && nL <= 156;
      const d = 21;
      const phys = isDrugCyp ? 197568 : Math.round((Math.ceil(1.5 * nL) + 24) * 2 * d * d);
      eraPill.textContent = "Era IV · Drug-Bound CYP3A4 & ICS Modular FTQC (100–1,000+ Logical)";
      eraPill.className = "pill pill-signal";
      organScale.textContent = isDrugCyp ? `CYP3A4 + Statin CAS(59e,58o)` : `CYP3A4 42–76o + Quantum B&B`;
      organSub.textContent = `Ancilla-complete Cholesky DF-QPE (${nL}L)`;
      ramScale.textContent = isDrugCyp ? "10²².¹² TiB FCI Wall" : "10¹²–10³³ TiB FCI Wall";
      ramSub.textContent = "10³³ determinants + volume-law entanglement";
      physScale.textContent = `~${phys.toLocaleString()} phys`;
      physSub.textContent = `Modular active QEC d=${d} · 1.7×10¹⁰ T-gates`;
      verdictScale.textContent = "Fault-Tolerant QPE Regime";
      verdictScale.style.color = "var(--signal)";
      verdictSub.textContent = "Strictly advisory R&D under DCB0129/0160";
    }
  }

  slider.addEventListener("input", updateEra);
  updateEra();
}

/* ── 4. Interactive 3D House-of-Care Bloch Sphere & 5-Layer DisCoPy Functor Stepper ── */
function initBlochAndDisCoPy() {
  const wrap = document.getElementById("bloch-canvas-wrap");
  if (!wrap) return;
  const canvas = document.createElement("canvas");
  wrap.appendChild(canvas);
  const ctx = canvas.getContext("2d");

  let theta = (28 * Math.PI) / 180;
  let phi = (40 * Math.PI) / 180;
  let camYaw = 0.52, camPitch = 0.30;
  let dragging = false, lx = 0, ly = 0;

  const thSlider = document.getElementById("theta-slider");
  const phSlider = document.getElementById("phi-slider");

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = wrap.clientWidth * dpr;
    canvas.height = wrap.clientHeight * dpr;
    canvas.style.width = `${wrap.clientWidth}px`;
    canvas.style.height = `${wrap.clientHeight}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    draw();
  }

  function project(x, y, z, cx, cy, R) {
    const x1 = x * Math.cos(camYaw) - y * Math.sin(camYaw);
    const y1 = x * Math.sin(camYaw) + y * Math.cos(camYaw);
    const z2 = z * Math.cos(camPitch) - y1 * Math.sin(camPitch);
    const y2 = z * Math.sin(camPitch) + y1 * Math.cos(camPitch);
    const persp = 1 / (1 - y2 * 0.18);
    return [cx + x1 * R * persp, cy - z2 * R * persp, y2];
  }

  function updateReadout() {
    const degT = Math.round((theta * 180) / Math.PI);
    const degP = ((Math.round((phi * 180) / Math.PI) % 360) + 360) % 360;
    thSlider.value = String(degT);
    phSlider.value = String(degP);
    document.getElementById("theta-val").textContent = `${degT}°`;
    document.getElementById("phi-val").textContent = `${degP}°`;

    const c = Math.cos(theta / 2), s = Math.sin(theta / 2);
    const p0 = c * c * 100, p1 = s * s * 100;
    document.getElementById("ket-readout").textContent =
      `|ψ_YoC⟩ = ${c.toFixed(3)}|0⟩ + (${(s * Math.cos(phi)).toFixed(3)} + ${(s * Math.sin(phi)).toFixed(3)}i)|1⟩`;
    document.getElementById("p0-txt").textContent = `${p0.toFixed(1)}%`;
    document.getElementById("p1-txt").textContent = `${p1.toFixed(1)}%`;
    document.getElementById("p0-fill").style.width = `${p0.toFixed(1)}%`;
    document.getElementById("p1-fill").style.width = `${p1.toFixed(1)}%`;
  }

  function draw() {
    const w = wrap.clientWidth, h = wrap.clientHeight;
    ctx.clearRect(0, 0, w, h);
    const cx = w / 2, cy = h / 2 + 18, R = Math.min(w, h) * 0.325;

    ctx.strokeStyle = "rgba(158, 183, 180, 0.28)";
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    ctx.arc(cx, cy, R, 0, Math.PI * 2);
    ctx.stroke();

    for (const mode of ["eq", "m1", "m2"]) {
      ctx.beginPath();
      for (let k = 0; k <= 72; k++) {
        const a = (k / 72) * Math.PI * 2;
        const px = mode === "eq" ? Math.cos(a) : mode === "m1" ? Math.cos(a) : 0;
        const py = mode === "eq" ? Math.sin(a) : mode === "m1" ? 0 : Math.cos(a);
        const pz = mode === "eq" ? 0 : Math.sin(a);
        const [sx, sy] = project(px, py, pz, cx, cy, R);
        if (k === 0) ctx.moveTo(sx, sy); else ctx.lineTo(sx, sy);
      }
      ctx.strokeStyle = mode === "eq" ? "rgba(56, 214, 196, 0.26)" : "rgba(158, 183, 180, 0.14)";
      ctx.stroke();
    }

    const [nx, ny] = project(0, 0, 1.07, cx, cy, R);
    const [sx2, sy2] = project(0, 0, -1.11, cx, cy, R);
    ctx.fillStyle = "#38d6c4";
    ctx.font = "600 11px 'JetBrains Mono', monospace";
    ctx.textAlign = "center";
    ctx.fillText("|0⟩ Unified MDT", nx, ny - 5);
    ctx.fillStyle = "#f06a3b";
    ctx.fillText("|1⟩ Siloed Drift", sx2, sy2 + 13);

    const vx = Math.sin(theta) * Math.cos(phi);
    const vy = Math.sin(theta) * Math.sin(phi);
    const vz = Math.cos(theta);
    const [tx, ty] = project(vx, vy, vz, cx, cy, R);

    ctx.strokeStyle = "#f4ae42";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(tx, ty);
    ctx.stroke();

    ctx.fillStyle = "#f4ae42";
    ctx.beginPath();
    ctx.arc(tx, ty, 6, 0, Math.PI * 2);
    ctx.fill();
  }

  wrap.addEventListener("pointerdown", e => { dragging = true; lx = e.clientX; ly = e.clientY; wrap.setPointerCapture(e.pointerId); });
  wrap.addEventListener("pointermove", e => {
    if (!dragging) return;
    camYaw += (e.clientX - lx) * 0.01;
    camPitch = Math.max(-1.05, Math.min(1.05, camPitch + (e.clientY - ly) * 0.01));
    lx = e.clientX; ly = e.clientY;
    draw();
  });
  wrap.addEventListener("pointerup", () => { dragging = false; });

  thSlider?.addEventListener("input", () => { theta = (Number(thSlider.value) * Math.PI) / 180; updateReadout(); draw(); });
  phSlider?.addEventListener("input", () => { phi = (Number(phSlider.value) * Math.PI) / 180; updateReadout(); draw(); });

  document.querySelectorAll("[data-bloch-gate]").forEach(btn => {
    btn.addEventListener("click", () => {
      const g = btn.dataset.blochGate;
      document.getElementById("bloch-gate-cue").textContent = BLOCH_CUES[g] || "";
      if (g === "H") { theta = Math.PI / 2 - theta * 0.25; phi = 0; }
      else if (g === "RX") { theta = Math.min(Math.PI, Math.max(0, theta + Math.PI / 4)); phi = (phi + Math.PI / 3) % (Math.PI * 2); }
      else if (g === "S") { phi = (phi + Math.PI / 2) % (Math.PI * 2); }
      else if (g === "Z") { phi = (phi + Math.PI) % (Math.PI * 2); }
      else if (g === "ZENO") { theta = theta * 0.30; }
      else if (g === "COLLAPSE") { theta = Math.random() < 0.5 ? 0 : Math.PI; phi = 0; }
      else if (g === "RESET") { theta = 0; phi = 0; }
      updateReadout();
      draw();
    });
  });

  window.addEventListener("resize", resize);
  updateReadout();
  resize();

  const pillsWrap = document.getElementById("discopy-pills");
  let step = 4, timer = null;
  function setStep(s) {
    step = (s + DISCOPY_STEPS.length) % DISCOPY_STEPS.length;
    document.querySelectorAll(".step-pill").forEach((el, idx) => el.classList.toggle("active", idx === step));
    for (let i = 0; i < 5; i++) {
      const layer = document.getElementById(`dc-layer-${i}`);
      if (!layer) continue;
      layer.classList.toggle("lit", i <= step);
      layer.classList.toggle("current", i === step);
    }
    document.getElementById("discopy-step-title").textContent = DISCOPY_STEPS[step].title;
    document.getElementById("discopy-step-circuit").textContent = DISCOPY_STEPS[step].circuit;
    document.getElementById("discopy-step-desc").textContent = DISCOPY_STEPS[step].desc;
  }
  DISCOPY_STEPS.forEach((st, idx) => {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "step-pill";
    b.textContent = st.short;
    b.addEventListener("click", () => setStep(idx));
    pillsWrap?.appendChild(b);
  });
  document.getElementById("discopy-next")?.addEventListener("click", () => setStep(step + 1));
  document.getElementById("discopy-autoplay")?.addEventListener("click", e => {
    if (timer) {
      clearInterval(timer); timer = null;
      e.currentTarget.textContent = "▶ Auto-Play";
    } else {
      e.currentTarget.textContent = "⏸ Pause";
      timer = setInterval(() => setStep(step + 1), 1900);
    }
  });
  setStep(4);
}

/* ── 5. Apache ECharts Multi-Scale Benchmark Gallery (5 Cards) + 300-DPI Print Lightbox ── */
function initChartsAndLightbox() {
  const cards = [...document.querySelectorAll("#benchmarks .fig-card")];
  const btnInt = document.getElementById("btn-chart-interactive");
  const btnStat = document.getElementById("btn-chart-static");
  const charts = [];

  btnInt?.addEventListener("click", () => {
    btnInt.classList.add("active");
    btnInt.setAttribute("aria-selected", "true");
    btnStat.classList.remove("active");
    btnStat.setAttribute("aria-selected", "false");
    cards.forEach(c => c.classList.add("interactive-mode"));
    setTimeout(() => charts.forEach(ch => ch.resize()), 50);
  });

  btnStat?.addEventListener("click", () => {
    btnStat.classList.add("active");
    btnStat.setAttribute("aria-selected", "true");
    btnInt.classList.remove("active");
    btnInt.setAttribute("aria-selected", "false");
    cards.forEach(c => c.classList.remove("interactive-mode"));
  });

  const lb = document.getElementById("img-lightbox");
  const lbImg = document.getElementById("lightbox-img");
  const lbCap = document.getElementById("lightbox-caption");

  function openLightbox(src, alt, caption) {
    lbImg.src = src;
    lbImg.alt = alt || "300-DPI Monograph Figure";
    lbCap.textContent = caption || "";
    lb.classList.add("open");
  }

  cards.forEach(card => {
    card.addEventListener("click", (e) => {
      if (e.target.closest("[data-open-fig]")) return;
      if (card.classList.contains("interactive-mode")) return;
      const img = card.querySelector("img");
      if (!img) return;
      const capText = card.querySelector("figcaption > div")?.innerText || card.querySelector("figcaption")?.innerText || "";
      openLightbox(card.dataset.zoomSrc || img.src, img.alt, capText);
    });
  });

  document.querySelectorAll("[data-open-fig]").forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const card = btn.closest("figure");
      const img = card?.querySelector("img");
      const capText = card?.querySelector("figcaption > div")?.innerText || card?.querySelector("figcaption")?.innerText || "";
      openLightbox(btn.dataset.openFig, img?.alt, capText);
    });
  });

  document.getElementById("lightbox-close")?.addEventListener("click", () => lb.classList.remove("open"));
  lb?.addEventListener("click", e => { if (e.target === lb) lb.classList.remove("open"); });

  let mounted = false;
  function mountCharts() {
    if (mounted || !window.echarts || !PORTAL_DATA) return;
    mounted = true;

    const baseAxis = {
      axisLabel: { color: "#9eb7b4", fontSize: 10.5, fontFamily: "JetBrains Mono, monospace" },
      axisLine: { lineStyle: { color: "rgba(158,183,180,0.25)" } },
      splitLine: { lineStyle: { color: "rgba(158,183,180,0.09)" } }
    };
    const darkTooltip = {
      trigger: "axis",
      backgroundColor: "rgba(11, 21, 23, 0.96)",
      borderColor: "rgba(56, 214, 196, 0.45)",
      textStyle: { color: "#eef7f5", fontSize: 12 }
    };

    // Chart 1: Era III Binary Memory Wall (Krylov vs Volume-Law MPDO vs MCWF vs Bounded MPDO)
    const elR = document.getElementById("echart-roadmap");
    if (elR && PORTAL_DATA.crossover) {
      const c1 = window.echarts.init(elR);
      const rows = PORTAL_DATA.crossover;
      c1.setOption({
        tooltip: darkTooltip,
        legend: {
          data: ["Exact Krylov (GiB)", "Volume-Law MPDO (GiB)", "MCWF m=30 (GiB)", "MPDO χ=64 (GiB)"],
          textStyle: { color: "#eef7f5", fontSize: 10.5 },
          top: 6
        },
        grid: { left: 56, right: 16, top: 56, bottom: 34 },
        xAxis: {
          type: "category",
          data: rows.map(r => `n=${r.n_organ_spins}\n(${r.ftqc_logical_qubits_required}L)`),
          ...baseAxis,
          axisLabel: { color: "#9eb7b4", fontSize: 9.5, interval: 0, lineHeight: 12 }
        },
        yAxis: {
          type: "log",
          logBase: 10,
          min: 1e-5,
          max: 1e7,
          ...baseAxis,
          axisLabel: {
            color: "#9eb7b4",
            fontSize: 9.5,
            formatter: v => (v >= 1024 ? `${Math.round(v / 1024)} TiB` : v >= 1 ? `${v} GiB` : `${(v * 1024).toFixed(1)} MiB`)
          }
        },
        series: [
          {
            name: "Exact Krylov (GiB)",
            type: "line",
            symbolSize: 7,
            data: rows.map(r => Math.max(1e-5, r.classical_krylov_m30_ram_gib)),
            itemStyle: { color: "#f06a3b" },
            lineStyle: { width: 3 },
            markLine: {
              silent: true,
              lineStyle: { color: "#f4ae42", type: "dashed", width: 1.5 },
              label: { formatter: "1 TiB Wall", color: "#f4ae42", fontSize: 9.5 },
              data: [{ yAxis: 1024 }]
            }
          },
          {
            name: "Volume-Law MPDO (GiB)",
            type: "line",
            symbolSize: 6,
            data: rows.map(r => Math.max(1e-5, r.mpdo_volume_law_ram_gib)),
            itemStyle: { color: "#a78bfa" },
            lineStyle: { width: 2.2, type: "dashed" }
          },
          {
            name: "MCWF m=30 (GiB)",
            type: "line",
            symbolSize: 6,
            data: rows.map(r => Math.max(1e-5, r.mcwf_krylov_m30_mib / 1024)),
            itemStyle: { color: "#38d6c4" },
            lineStyle: { width: 2.5 }
          },
          {
            name: "MPDO χ=64 (GiB)",
            type: "line",
            symbolSize: 5,
            data: rows.map(r => Math.max(1e-5, r.mpdo_bounded_chi64_mib / 1024)),
            itemStyle: { color: "#f4ae42" },
            lineStyle: { width: 2, type: "dotted" }
          }
        ]
      });
      charts.push(c1);
    }

    // Chart 2: Live Nexus Helios-1E-lite 8-Rung Self-Calibrating MCMR Ladder (R^2 = 0.9979)
    const elN = document.getElementById("echart-nexus-haiqu");
    if (elN && PORTAL_DATA.nexus_ladder) {
      const c2 = window.echarts.init(elN);
      const lRows = PORTAL_DATA.nexus_ladder;
      c2.setOption({
        tooltip: darkTooltip,
        legend: {
          data: ["Raw Helios-1E-lite Contrast", "Affine SPAM-Calibrated (R²=0.9979)"],
          textStyle: { color: "#eef7f5", fontSize: 10.5 },
          top: 6
        },
        grid: { left: 48, right: 16, top: 54, bottom: 44 },
        xAxis: {
          type: "category",
          data: lRows.map((_, i) => `Rung ${i + 1}`),
          ...baseAxis
        },
        yAxis: { type: "value", min: -1.05, max: 1.05, interval: 0.5, ...baseAxis },
        series: [
          {
            name: "Raw Helios-1E-lite Contrast",
            type: "bar",
            barWidth: "36%",
            data: lRows.map(r => r.raw),
            itemStyle: { color: "rgba(244,174,66,0.58)", borderRadius: [3, 3, 0, 0] }
          },
          {
            name: "Affine SPAM-Calibrated (R²=0.9979)",
            type: "line",
            smooth: true,
            symbolSize: 7,
            data: lRows.map(r => r.calibrated),
            itemStyle: { color: "#38d6c4" },
            lineStyle: { width: 3 }
          }
        ]
      });
      charts.push(c2);
    }

    // Chart 3: Decoupled 4-Regime HQS Cardiorenal-Pulmonary Lindbladian
    const elB = document.getElementById("echart-biophys");
    if (elB && PORTAL_DATA.lindblad_regimes) {
      const c3 = window.echarts.init(elB);
      const regs = PORTAL_DATA.lindblad_regimes;
      c3.setOption({
        tooltip: darkTooltip,
        legend: {
          data: ["Vascular BP", "Hepatic HbA1c", "Renal uACR", "Airway IL-6"],
          textStyle: { color: "#eef7f5", fontSize: 10.5 },
          top: 6
        },
        grid: { left: 44, right: 16, top: 54, bottom: 48 },
        xAxis: {
          type: "category",
          data: ["Regime A\nStress", "Regime B\nΩ_pro Only", "Regime C\nCoexisting", "Regime C\n(g_ij=0)", "Regime D\nFlip"],
          ...baseAxis,
          axisLabel: { color: "#9eb7b4", fontSize: 9.5, interval: 0, lineHeight: 12 }
        },
        yAxis: { type: "value", min: 0, max: 1.05, interval: 0.25, ...baseAxis },
        series: [
          { name: "Vascular BP", type: "bar", barGap: "10%", data: regs.map(r => r.bp), itemStyle: { color: "#f06a3b" } },
          { name: "Hepatic HbA1c", type: "bar", data: regs.map(r => r.glyc), itemStyle: { color: "#f4ae42" } },
          { name: "Renal uACR", type: "bar", data: regs.map(r => r.renal), itemStyle: { color: "#38d6c4" } },
          { name: "Airway IL-6", type: "bar", data: regs.map(r => r.il6), itemStyle: { color: "#a78bfa" } }
        ]
      });
      charts.push(c3);
    }

    // Chart 4: 5-Seed Modal QLTCMLM vs Classical Baselines (8 Models)
    const elQ = document.getElementById("echart-qml");
    if (elQ && PORTAL_DATA.qltcmlm_models) {
      const c4 = window.echarts.init(elQ);
      const mRows = PORTAL_DATA.qltcmlm_models;
      c4.setOption({
        tooltip: darkTooltip,
        legend: {
          data: ["Task A: 4-Tier Risk Acc (%)", "Task B: Care Bundle Acc (%)"],
          textStyle: { color: "#eef7f5", fontSize: 10.5 },
          top: 6
        },
        grid: { left: 44, right: 14, top: 54, bottom: 48 },
        xAxis: {
          type: "category",
          data: mRows.map(m => m.label),
          ...baseAxis,
          axisLabel: { color: "#9eb7b4", fontSize: 9, interval: 0, lineHeight: 11.5 }
        },
        yAxis: { type: "value", min: 0, max: 100, interval: 25, ...baseAxis },
        series: [
          {
            name: "Task A: 4-Tier Risk Acc (%)",
            type: "bar",
            barGap: "12%",
            data: mRows.map(m => m.risk_pct),
            itemStyle: { color: "#38d6c4", borderRadius: [3, 3, 0, 0] }
          },
          {
            name: "Task B: Care Bundle Acc (%)",
            type: "bar",
            data: mRows.map(m => m.bundle_pct),
            itemStyle: { color: "#f4ae42", borderRadius: [3, 3, 0, 0] }
          }
        ]
      });
      charts.push(c4);
    }

    // Chart 4b (Full-Width): Ab-Initio PySCF 2.15 CYP3A4 (1TQN) DF-QPE Logical Qubits vs Exponential FCI RAM Wall
    const elM = document.getElementById("echart-metalloenzyme");
    if (elM && PORTAL_DATA.metalloenzyme_ftqc) {
      const cM = window.echarts.init(elM);
      const dfRows = PORTAL_DATA.metalloenzyme_ftqc.df_frontier;
      cM.setOption({
        tooltip: darkTooltip,
        legend: {
          data: [
            "log₁₀(Single Exact FCI Statevector TiB)",
            "Ancilla-Complete Cholesky DF-QPE Logical Qubits (#L)"
          ],
          textStyle: { color: "#eef7f5", fontSize: 11 },
          top: 6
        },
        grid: { left: 56, right: 64, top: 54, bottom: 42 },
        xAxis: {
          type: "category",
          data: dfRows.map(r => `M=${r.M}o\n(λ=${r.lambda_df_ha} Ha)`),
          ...baseAxis,
          axisLabel: { color: "#bfece6", fontSize: 10.2, interval: 0, lineHeight: 13 }
        },
        yAxis: [
          {
            type: "value",
            min: -6,
            max: 35,
            ...baseAxis,
            name: "log₁₀(FCI Statevector TiB)",
            nameTextStyle: { color: "#f06a3b", fontSize: 10.5 }
          },
          {
            type: "value",
            min: 0,
            max: 210,
            ...baseAxis,
            splitLine: { show: false },
            name: "DF-QPE Logical Qubits",
            nameTextStyle: { color: "#38d6c4", fontSize: 10.5 }
          }
        ],
        series: [
          {
            name: "log₁₀(Single Exact FCI Statevector TiB)",
            type: "line",
            yAxisIndex: 0,
            symbolSize: 8,
            data: dfRows.map(r => r.log10_fci_tib),
            itemStyle: { color: "#f06a3b" },
            lineStyle: { width: 3 },
            markLine: {
              silent: true,
              lineStyle: { color: "#f4ae42", type: "dashed", width: 1.5 },
              label: { formatter: "1.00 TiB Single-Node RAM Wall (M ≥ 22)", color: "#f4ae42", fontSize: 10 },
              data: [{ yAxis: 0 }]
            }
          },
          {
            name: "Ancilla-Complete Cholesky DF-QPE Logical Qubits (#L)",
            type: "bar",
            yAxisIndex: 1,
            barWidth: "34%",
            data: dfRows.map(r => r.logical_qubits),
            itemStyle: { color: "rgba(56, 214, 196, 0.72)", borderColor: "#38d6c4", borderWidth: 1.5, borderRadius: [4, 4, 0, 0] },
            label: { show: true, position: "top", formatter: "{c}L", color: "#38d6c4", fontSize: 10.5, fontFamily: "JetBrains Mono, monospace" }
          }
        ]
      });
      charts.push(cM);
    }

    // Chart 4c (Full-Width): Gate 1 Clinical Quantum Wedge — PDB 5TE8 def2-SVP Barriers & Live ChEMBL340 + AG2 PBPK AUCR
    const elGate1 = document.getElementById("echart-gate1-cyp3a4");
    if (elGate1 && PORTAL_DATA.gate1_cyp3a4) {
      const cG1 = window.echarts.init(elGate1);
      const hatRows = PORTAL_DATA.gate1_cyp3a4.hat_barriers;
      const ddiRows = PORTAL_DATA.gate1_cyp3a4.pbpk_ddis;
      cG1.setOption({
        tooltip: {
          trigger: "axis",
          backgroundColor: "rgba(11, 21, 23, 0.96)",
          borderColor: "rgba(56, 214, 196, 0.45)",
          textStyle: { color: "#eef7f5", fontSize: 12 }
        },
        legend: [
          {
            data: ["Doublet S=1/2 ΔE‡ (kcal/mol)", "Quartet S=3/2 ΔE‡ (kcal/mol)"],
            textStyle: { color: "#eef7f5", fontSize: 10.5 },
            left: "5%",
            top: 6
          },
          {
            data: ["ChEMBL340 PBPK AUCR (WT)", "AG2 CYP3A4*22 Exposure", "Published Clinical Midpoint"],
            textStyle: { color: "#eef7f5", fontSize: 10.5 },
            right: "3%",
            top: 6
          }
        ],
        grid: [
          { left: 54, width: "41%", top: 64, bottom: 54 },
          { right: 28, width: "41%", top: 64, bottom: 54 }
        ],
        xAxis: [
          {
            gridIndex: 0,
            type: "category",
            data: ["BS-PBE\n(GGA)", "BS-BLYP\n(GGA)", "BS-B3LYP\n(Hybrid)", "BS-PBE0\n(Hybrid)", "SA-CASSCF\n(9e,9o)", "SC-NEVPT2\n(def2-SVP)"],
            ...baseAxis,
            axisLabel: { color: "#bfece6", fontSize: 9.2, interval: 0, lineHeight: 12 }
          },
          {
            gridIndex: 1,
            type: "category",
            data: ddiRows.map(d => d.label),
            ...baseAxis,
            axisLabel: { color: "#bfece6", fontSize: 9.2, interval: 0, lineHeight: 12 }
          }
        ],
        yAxis: [
          {
            gridIndex: 0,
            type: "value",
            min: 0,
            max: 52,
            ...baseAxis,
            name: "PDB 5TE8 ΔE‡ (kcal/mol)",
            nameTextStyle: { color: "#a78bfa", fontSize: 10.5 }
          },
          {
            gridIndex: 1,
            type: "log",
            logBase: 10,
            min: 1,
            max: 30,
            ...baseAxis,
            name: "Clinical Fold Exposure (AUCR)",
            nameTextStyle: { color: "#38d6c4", fontSize: 10.5 }
          }
        ],
        series: [
          {
            name: "Doublet S=1/2 ΔE‡ (kcal/mol)",
            type: "bar",
            xAxisIndex: 0,
            yAxisIndex: 0,
            barGap: "10%",
            data: hatRows.map(r => r.barrier_doublet_kcal_mol),
            itemStyle: { color: "#a78bfa", borderRadius: [3, 3, 0, 0] },
            label: { show: true, position: "top", color: "#c4b5fd", fontSize: 9.2 }
          },
          {
            name: "Quartet S=3/2 ΔE‡ (kcal/mol)",
            type: "bar",
            xAxisIndex: 0,
            yAxisIndex: 0,
            data: hatRows.map(r => r.barrier_quartet_kcal_mol),
            itemStyle: { color: "#38d6c4", borderRadius: [3, 3, 0, 0] },
            label: { show: true, position: "top", color: "#38d6c4", fontSize: 9.2 }
          },
          {
            name: "ChEMBL340 PBPK AUCR (WT)",
            type: "bar",
            xAxisIndex: 1,
            yAxisIndex: 1,
            barGap: "10%",
            data: ddiRows.map(d => d.aucr_wt),
            itemStyle: { color: "#38d6c4", borderRadius: [3, 3, 0, 0] }
          },
          {
            name: "AG2 CYP3A4*22 Exposure",
            type: "bar",
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: ddiRows.map(d => d.aucr_star22),
            itemStyle: { color: "#f06a3b", borderRadius: [3, 3, 0, 0] }
          },
          {
            name: "Published Clinical Midpoint",
            type: "bar",
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: ddiRows.map(d => d.clin_mid),
            itemStyle: { color: "#f4ae42", borderRadius: [3, 3, 0, 0] }
          }
        ]
      });
      charts.push(cG1);
    }

    // Chart 5 (Full-Width): TypeSafe Jev 1.14 Multi-Method Health AI Audit across CUJ-1..4
    const elG = document.getElementById("echart-governance");
    if (elG && PORTAL_DATA.jev_cujs) {
      const c5 = window.echarts.init(elG);
      const cujs = PORTAL_DATA.jev_cujs;
      c5.setOption({
        tooltip: darkTooltip,
        legend: {
          data: [
            "Safety (/5 · DCB0129/0160)",
            "NHS Usefulness (/5 · CUJ-1 Peak 4.32)",
            "Empirical Accuracy (/5 · Calibrated Skepticism)",
            "Autonomous Live Deployment Prob (0.00)"
          ],
          textStyle: { color: "#eef7f5", fontSize: 11 },
          top: 6
        },
        grid: { left: 48, right: 24, top: 56, bottom: 40 },
        xAxis: {
          type: "category",
          data: cujs.map(c => c.short_label),
          ...baseAxis,
          axisLabel: { color: "#bfece6", fontSize: 10.8 }
        },
        yAxis: {
          type: "value",
          min: 0,
          max: 5.0,
          ...baseAxis,
          name: "Score (/5)",
          nameTextStyle: { color: "#9eb7b4", fontSize: 11 }
        },
        series: [
          {
            name: "Safety (/5 · DCB0129/0160)",
            type: "bar",
            barGap: "14%",
            data: cujs.map(c => c.safety),
            itemStyle: { color: "#38d6c4", borderRadius: [4, 4, 0, 0] },
            label: { show: true, position: "top", color: "#38d6c4", fontSize: 10.5 }
          },
          {
            name: "NHS Usefulness (/5 · CUJ-1 Peak 4.32)",
            type: "bar",
            data: cujs.map(c => c.usefulness),
            itemStyle: { color: "#f4ae42", borderRadius: [4, 4, 0, 0] },
            label: { show: true, position: "top", color: "#f4ae42", fontSize: 10.5 }
          },
          {
            name: "Empirical Accuracy (/5 · Calibrated Skepticism)",
            type: "bar",
            data: cujs.map(c => c.accuracy),
            itemStyle: { color: "#a78bfa", borderRadius: [4, 4, 0, 0] },
            label: { show: true, position: "top", color: "#c4b5fd", fontSize: 10.5 }
          },
          {
            name: "Autonomous Live Deployment Prob (0.00)",
            type: "line",
            symbolSize: 8,
            data: cujs.map(c => c.auto_prob),
            itemStyle: { color: "#f06a3b" },
            lineStyle: { width: 2.5, type: "dashed" }
          }
        ]
      });
      charts.push(c5);
    }

    window.addEventListener("resize", () => charts.forEach(c => c.resize()));
  }

  let tries = 0;
  const poll = setInterval(() => {
    tries++;
    if (window.echarts && PORTAL_DATA) {
      clearInterval(poll);
      mountCharts();
    } else if (tries > 60) {
      clearInterval(poll);
    }
  }, 60);
  mountCharts();
}

/* ── 6. Kashefi Atlas v0.4 Filter, Receipt JSON Inspector & BibTeX ── */
function initTablesAndCitations() {
  if (!PORTAL_DATA) return;
  const atlasTbody = document.getElementById("atlas-tbody");
  const atlasInput = document.getElementById("atlas-search");
  const atlasCount = document.getElementById("atlas-count");

  function renderAtlas(q) {
    const needle = (q || "").trim().toLowerCase();
    const rows = PORTAL_DATA.atlas_contracts.filter(r =>
      !needle || JSON.stringify(r).toLowerCase().includes(needle)
    );
    atlasCount.textContent = `${rows.length} / ${PORTAL_DATA.atlas_contracts.length} Contracts Shown (42 Cards Audited)`;
    atlasTbody.innerHTML = rows.map(r => `
      <tr>
        <td><code>${r.id}</code><br/><span style="font-size:0.72rem;color:var(--ink-dim);text-transform:capitalize">${r.category}</span></td>
        <td><strong style="color:var(--ink)">${r.name}</strong><br/><span style="font-family:var(--font-mono);font-size:0.73rem;color:var(--amber)">${r.paper}</span></td>
        <td>${r.ltc_use_html}</td>
        <td style="font-size:0.81rem;color:var(--signal)">${r.era}</td>
        <td style="color:var(--ink-muted);font-size:0.8rem">${r.caveat}</td>
      </tr>
    `).join("");
  }
  renderAtlas("");
  atlasInput?.addEventListener("input", e => renderAtlas(e.target.value));

  const recTbody = document.getElementById("receipts-tbody");
  const modal = document.getElementById("json-modal");
  const modalTitle = document.getElementById("json-modal-title");
  const modalPre = document.getElementById("json-modal-pre");
  const modalDl = document.getElementById("json-modal-dl");

  recTbody.innerHTML = PORTAL_DATA.receipts_summary.map(r => `
    <tr>
      <td><code>${r.file}</code><br/><span style="font-family:var(--font-mono);font-size:0.69rem;color:var(--ink-dim)">SHA-256: ${r.sha256.slice(0, 16)}…</span></td>
      <td>${r.platforms}</td>
      <td>${r.metrics}</td>
      <td><code>${r.floor}</code></td>
      <td style="white-space:nowrap">
        <button type="button" class="btn btn-sm" data-inspect-json="${r.file}">🔍 Inspect JSON</button>
      </td>
    </tr>
  `).join("");

  recTbody.querySelectorAll("[data-inspect-json]").forEach(btn => {
    btn.addEventListener("click", async () => {
      const f = btn.dataset.inspectJson;
      modalTitle.textContent = `receipts/${f}`;
      modalDl.href = `receipts/${f}`;
      modalDl.download = f;
      modalPre.textContent = "Loading verified JSON receipt…";
      modal.classList.add("open");
      try {
        const res = await fetch(`receipts/${f}`);
        const txt = await res.text();
        modalPre.textContent = txt;
      } catch (err) {
        modalPre.textContent = `Unable to fetch receipt inline: ${err}`;
      }
    });
  });
  document.getElementById("json-modal-close")?.addEventListener("click", () => modal.classList.remove("open"));
  modal?.addEventListener("click", e => { if (e.target === modal) modal.classList.remove("open"); });

  const bibPre = document.getElementById("bibtex-code");
  let activeBib = "monograph";
  if (bibPre) bibPre.textContent = BIBTEX_ENTRIES.monograph;
  document.querySelectorAll("[data-bib-tab]").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("[data-bib-tab]").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeBib = btn.dataset.bibTab;
      bibPre.textContent = BIBTEX_ENTRIES[activeBib];
    });
  });
  document.getElementById("copy-bibtex-btn")?.addEventListener("click", async () => {
    await navigator.clipboard.writeText(BIBTEX_ENTRIES[activeBib]);
    showToast("Copied BibTeX citation to clipboard");
  });
  document.getElementById("download-bibtex-btn")?.addEventListener("click", () => {
    const blob = new Blob([Object.values(BIBTEX_ENTRIES).join("\n\n")], { type: "text/plain" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "quantum_ltc.bib";
    a.click();
  });
}

/* ── 7. Interactive Apache ECharts Knowledge Graph Explorer (57 Nodes, 114 Triples) ── */
function initKnowledgeGraph() {
  const el = document.getElementById("echart-kg");
  if (!el || !PORTAL_DATA?.knowledge_graph) return;

  const kg = PORTAL_DATA.knowledge_graph;
  const catMap = Object.fromEntries(kg.categories.map(c => [c.id, c]));
  const nodeMap = Object.fromEntries(kg.nodes.map(n => [n.id, n]));
  const activeCats = new Set(kg.categories.map(c => c.id));
  let currentLayout = "concentric";
  let searchNeedle = "";
  let selectedId = "plat_nexus_helios";
  let pathNodes = new Set();
  let pathEdges = new Set();

  const shaEl = document.getElementById("kg-sha-lbl");
  if (shaEl) shaEl.textContent = `SHA-256: ${kg.receipt_sha256.slice(0, 16)}…`;

  const adj = {};
  const incident = {};
  kg.nodes.forEach(n => { adj[n.id] = []; incident[n.id] = []; });
  kg.edges.forEach((e, idx) => {
    adj[e.source].push({ neighbor: e.target, edge: e, idx });
    adj[e.target].push({ neighbor: e.source, edge: e, idx });
    incident[e.source].push({ ...e, dir: "OUT" });
    incident[e.target].push({ ...e, dir: "IN" });
  });

  function shortLabel(n) {
    const base = n.label.split("(")[0].trim();
    return base.length > 24 ? base.slice(0, 23).trim() + "…" : base;
  }

  const concentricPos = {};
  (function computeConcentric() {
    const rings = {
      Logical_Era: [145, 0.2],
      HouseOfCare_Stage: [275, 0.05],
      NCL_LTC_Condition: [420, 0.18],
      Intervention: [545, -0.4],
      Molecular_Target: [675, 0.3],
      Quantum_Primitive: [795, 0.12],
      Platform_Receipt: [905, -0.22],
      DCB0129_Hazard: [1010, 0.42]
    };
    const grouped = {};
    kg.categories.forEach(c => { grouped[c.id] = []; });
    kg.nodes.forEach(n => grouped[n.category].push(n));
    Object.entries(grouped).forEach(([cid, items]) => {
      const [rad, phase] = rings[cid] || [500, 0];
      items.forEach((it, i) => {
        const a = phase + (2 * Math.PI * i) / Math.max(1, items.length);
        concentricPos[it.id] = [rad * Math.cos(a), -rad * Math.sin(a)];
      });
    });
  })();

  function nodeMatches(n) {
    if (!activeCats.has(n.category)) return false;
    if (!searchNeedle) return true;
    const q = searchNeedle.toLowerCase();
    return (
      n.id.toLowerCase().includes(q) ||
      n.label.toLowerCase().includes(q) ||
      (n.external_id || "").toLowerCase().includes(q) ||
      (n.metric || "").toLowerCase().includes(q)
    );
  }

  function renderInspector(nid) {
    selectedId = nid;
    const n = nodeMap[nid];
    const box = document.getElementById("kg-inspector");
    if (!n || !box) return;
    const cat = catMap[n.category];
    const edges = incident[nid] || [];

    const edgeHtml = edges.map(e => {
      const peerId = e.dir === "OUT" ? e.target : e.source;
      const peer = nodeMap[peerId];
      const arrow = e.dir === "OUT" ? "→" : "←";
      return `
        <button type="button" class="kg-edge-btn" data-kg-hop="${peerId}">
          <div style="display:flex;justify-content:space-between;gap:0.4rem;font-family:var(--font-mono);font-size:0.71rem">
            <span style="color:var(--signal);font-weight:700">${arrow} ${e.relation}</span>
          </div>
          <div style="font-size:0.8rem;margin-top:0.15rem;color:var(--ink)">${peer ? peer.label : peerId}</div>
          <div style="font-size:0.71rem;margin-top:0.1rem;color:var(--ink-dim)">${e.weight}</div>
        </button>
      `;
    }).join("");

    box.innerHTML = `
      <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:0.4rem">
        <span class="pill" style="border-color:${cat.color};color:${cat.color}">${cat.short} · ${n.tier}</span>
        <code style="font-size:0.72rem;color:var(--ink-dim)">${n.id}</code>
      </div>
      <h3 style="margin:0.65rem 0 0.35rem;font-size:1.12rem">${n.label}</h3>
      <div class="ket-readout" style="margin-top:0.3rem;font-size:0.73rem;color:var(--amber)">${n.external_id}</div>

      <div style="margin-top:0.75rem;padding:0.7rem 0.8rem;border-radius:6px;background:#081012;border:1px solid var(--border);font-size:0.83rem;line-height:1.5">
        <div style="font-family:var(--font-mono);font-size:0.69rem;color:var(--ink-muted);text-transform:uppercase;margin-bottom:0.25rem">Ontology &amp; Receipt Telemetry</div>
        <div>${n.metric}</div>
        <div style="margin-top:0.45rem;padding-top:0.4rem;border-top:1px solid var(--border);font-size:0.77rem;color:var(--ink-muted)">
          <strong>Epistemic Status:</strong> ${n.epistemic_status}
        </div>
      </div>

      <div style="margin-top:0.7rem;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0.45rem;text-align:center">
        <div class="ket-readout" style="margin:0;padding:0.45rem">
          <div style="font-size:0.68rem;color:var(--ink-muted)">Degree</div>
          <strong style="color:var(--ink)">${n.total_degree}</strong> <span style="font-size:0.68rem;color:var(--ink-dim)">(${n.in_degree}↓/${n.out_degree}↑)</span>
        </div>
        <div class="ket-readout" style="margin:0;padding:0.45rem">
          <div style="font-size:0.68rem;color:var(--ink-muted)">Betweenness</div>
          <strong style="color:var(--signal)">${n.betweenness_centrality.toFixed(4)}</strong>
        </div>
        <div class="ket-readout" style="margin:0;padding:0.45rem">
          <div style="font-size:0.68rem;color:var(--ink-muted)">PageRank</div>
          <strong style="color:var(--amber)">${n.pagerank.toFixed(4)}</strong>
        </div>
      </div>

      <div style="margin-top:0.8rem">
        <div style="font-family:var(--font-mono);font-size:0.71rem;color:var(--ink-muted);text-transform:uppercase">
          Incident Semantic Triples (${edges.length}) — Click to Hop
        </div>
        <div class="kg-edge-list">${edgeHtml}</div>
      </div>
    `;

    box.querySelectorAll("[data-kg-hop]").forEach(b => {
      b.addEventListener("click", () => {
        renderInspector(b.dataset.kgHop);
        updateChart();
      });
    });
  }

  let chart = null;
  function updateChart() {
    if (!chart) return;
    const visNodes = kg.nodes.filter(nodeMatches);
    const visSet = new Set(visNodes.map(n => n.id));
    const hasPath = pathNodes.size > 0;

    const eNodes = visNodes.map(n => {
      const catIdx = kg.categories.findIndex(c => c.id === n.category);
      const col = catMap[n.category].color;
      const onPath = hasPath && pathNodes.has(n.id);
      const isSel = n.id === selectedId;
      const [cx, cy] = concentricPos[n.id] || [0, 0];
      const base = {
        id: n.id,
        name: shortLabel(n),
        fullLabel: n.label,
        metric: n.metric,
        external_id: n.external_id,
        category: catIdx,
        symbolSize: 13 + Math.min(18, n.total_degree * 1.55),
        draggable: true,
        itemStyle: {
          color: col,
          borderColor: onPath ? "#f4ae42" : (isSel ? "#ffffff" : "#0b1517"),
          borderWidth: onPath || isSel ? 2.8 : 1.2,
          opacity: hasPath && !onPath ? 0.25 : 1.0
        },
        label: {
          show: true,
          fontSize: 9.8,
          color: "#eef7f5",
          backgroundColor: "rgba(11,21,23,0.82)",
          borderColor: onPath ? "#f4ae42" : col,
          borderWidth: 0.7,
          borderRadius: 4,
          padding: [2, 5]
        }
      };
      if (currentLayout === "concentric") {
        base.x = cx;
        base.y = cy;
      }
      return base;
    });

    const eLinks = [];
    kg.edges.forEach((e, idx) => {
      if (!visSet.has(e.source) || !visSet.has(e.target)) return;
      const onPath = hasPath && pathEdges.has(idx);
      const isFocus = !hasPath && (e.source === selectedId || e.target === selectedId);
      eLinks.push({
        source: e.source,
        target: e.target,
        relation: e.relation,
        weightLabel: e.weight,
        lineStyle: {
          color: onPath
            ? "#f4ae42"
            : (isFocus ? (e.relation.includes("HAZARD") || e.target.startsWith("haz_") ? "#f06a3b" : "#38d6c4") : "rgba(158,183,180,0.28)"),
          width: onPath ? 3.2 : (isFocus ? 2.1 : 1.0),
          opacity: hasPath && !onPath ? 0.14 : 0.85,
          curveness: 0.11
        }
      });
    });

    const statusPill = document.getElementById("kg-status-pill");
    if (statusPill) statusPill.textContent = `${eNodes.length} / ${kg.nodes.length} Nodes · ${eLinks.length} Triples`;

    chart.setOption({
      tooltip: {
        trigger: "item",
        backgroundColor: "rgba(11, 21, 23, 0.96)",
        borderColor: "rgba(56, 214, 196, 0.48)",
        textStyle: { color: "#eef7f5", fontSize: 12 },
        formatter: (params) => {
          if (params.dataType === "edge") {
            return `<strong>${params.data.relation}</strong><br/><span style="color:#f4ae42">${params.data.weightLabel}</span><br/>${params.data.source} → ${params.data.target}`;
          }
          const d = params.data;
          return `<strong>${d.fullLabel}</strong><br/><span style="color:#f4ae42">${d.external_id}</span>`;
        }
      },
      categories: kg.categories.map(c => ({ name: c.short, itemStyle: { color: c.color } })),
      series: [
        {
          type: "graph",
          layout: currentLayout === "concentric" ? "none" : currentLayout,
          data: eNodes,
          links: eLinks,
          categories: kg.categories.map(c => ({ name: c.short })),
          roam: true,
          zoom: currentLayout === "concentric" ? 0.74 : 0.86,
          edgeSymbol: ["none", "arrow"],
          edgeSymbolSize: [4, 7],
          emphasis: { focus: "adjacency", lineStyle: { width: 2.6 } },
          force: { repulsion: 520, edgeLength: [110, 195], gravity: 0.06, layoutAnimation: true },
          labelLayout: { hideOverlap: true }
        }
      ]
    }, true);
  }

  const chipWrap = document.getElementById("kg-cat-chips");
  kg.categories.forEach(c => {
    const cnt = kg.topology_metrics.category_counts[c.id] || 0;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "kg-cat-chip";
    btn.innerHTML = `<span class="kg-cat-dot" style="background:${c.color}"></span><span>${c.short} (${cnt})</span>`;
    btn.addEventListener("click", () => {
      if (activeCats.has(c.id) && activeCats.size > 1) {
        activeCats.delete(c.id);
        btn.classList.add("muted");
      } else {
        activeCats.add(c.id);
        btn.classList.remove("muted");
      }
      updateChart();
    });
    chipWrap?.appendChild(btn);
  });

  document.querySelectorAll("[data-kg-layout]").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("[data-kg-layout]").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentLayout = btn.dataset.kgLayout;
      updateChart();
    });
  });

  const searchInput = document.getElementById("kg-search");
  searchInput?.addEventListener("input", () => {
    searchNeedle = searchInput.value.trim();
    const matches = kg.nodes.filter(nodeMatches);
    if (searchNeedle && matches.length > 0 && !matches.some(m => m.id === selectedId)) {
      renderInspector(matches[0].id);
    }
    updateChart();
  });

  const srcSel = document.getElementById("kg-path-src");
  const dstSel = document.getElementById("kg-path-dst");
  kg.nodes.forEach(n => {
    const opt = document.createElement("option");
    opt.value = n.id;
    opt.textContent = `[${catMap[n.category].short}] ${shortLabel(n)}`;
    srcSel?.appendChild(opt);
    dstSel?.appendChild(opt.cloneNode(true));
  });
  if (srcSel) srcSel.value = "ltc_htn";
  if (dstSel) dstSel.value = "mol_pdb_1o86";

  function runShortestPath(sId, dId) {
    pathNodes.clear();
    pathEdges.clear();
    const rib = document.getElementById("kg-path-ribbon");
    if (!sId || !dId || sId === dId) {
      rib?.classList.remove("visible");
      updateChart();
      return;
    }
    kg.categories.forEach(c => activeCats.add(c.id));
    chipWrap?.querySelectorAll(".kg-cat-chip").forEach(b => b.classList.remove("muted"));

    const prev = {};
    const vis = new Set([sId]);
    const q = [sId];
    while (q.length > 0) {
      const cur = q.shift();
      if (cur === dId) break;
      for (const step of adj[cur] || []) {
        if (!vis.has(step.neighbor)) {
          vis.add(step.neighbor);
          prev[step.neighbor] = { from: cur, edgeIdx: step.idx, rel: step.edge.relation };
          q.push(step.neighbor);
        }
      }
    }
    if (!vis.has(dId)) return;
    const chain = [];
    let cur = dId;
    pathNodes.add(cur);
    while (cur !== sId) {
      const p = prev[cur];
      pathEdges.add(p.edgeIdx);
      pathNodes.add(p.from);
      chain.unshift({ from: p.from, to: cur, rel: p.rel });
      cur = p.from;
    }
    if (rib) {
      rib.innerHTML =
        `<strong style="color:var(--amber)">Shortest Multi-Layer Path (${chain.length} hops):</strong> ` +
        chain.map(s => `<strong>${shortLabel(nodeMap[s.from])}</strong> <code style="color:var(--signal)">--[${s.rel}]--&gt;</code> `).join("") +
        `<strong>${shortLabel(nodeMap[dId])}</strong>`;
      rib.classList.add("visible");
    }
    renderInspector(dId);
    updateChart();
  }

  document.getElementById("kg-trace-btn")?.addEventListener("click", () => runShortestPath(srcSel.value, dstSel.value));
  document.getElementById("kg-clear-path-btn")?.addEventListener("click", () => {
    pathNodes.clear();
    pathEdges.clear();
    document.getElementById("kg-path-ribbon")?.classList.remove("visible");
    updateChart();
  });
  document.querySelectorAll("[data-kg-preset]").forEach(btn => {
    btn.addEventListener("click", () => {
      const [s, d] = btn.dataset.kgPreset.split("|");
      if (srcSel) srcSel.value = s;
      if (dstSel) dstSel.value = d;
      runShortestPath(s, d);
    });
  });

  renderInspector("plat_nexus_helios");

  function mountKg() {
    if (chart || !window.echarts) return;
    chart = window.echarts.init(el);
    chart.on("click", params => {
      if (params.dataType === "node" && params.data?.id) {
        renderInspector(params.data.id);
        updateChart();
      }
    });
    updateChart();
    window.addEventListener("resize", () => chart && chart.resize());
  }

  let tries = 0;
  const poll = setInterval(() => {
    tries++;
    if (window.echarts) {
      clearInterval(poll);
      mountKg();
    } else if (tries > 60) {
      clearInterval(poll);
    }
  }, 60);
  mountKg();
}

async function boot() {
  if (typeof window === "undefined") return;
  initNav();
  initPdfReader();
  initEraSimulator();
  initBlochAndDisCoPy();
  const [dataRes, weightsRes] = await Promise.all([
    fetch("assets/data.json").then(r => r.json()),
    fetch("receipts/qltcmlm_weights.json").then(r => r.json())
  ]);
  PORTAL_DATA = dataRes;
  QLTC_WEIGHTS = weightsRes;
  initQLTCMLMSimulator();
  initChartsAndLightbox();
  initKnowledgeGraph();
  initTablesAndCitations();
}

if (typeof window !== "undefined") {
  boot();
}
