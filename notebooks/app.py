import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="QCR | Road Quality & Compliance",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
.stApp { background:#0b1117; color:#e8eef4; }
.block-container { max-width:1450px; padding-top:1.6rem; }
.hero { padding:1.1rem 1.3rem; border:1px solid #263440; border-radius:18px;
        background:linear-gradient(135deg,#111a23,#0d151d); margin-bottom:1rem; }
.hero-title { font-size:2.2rem; font-weight:800; letter-spacing:-.04em; }
.hero-subtitle { color:#9fb0bf; font-size:.95rem; margin-top:.15rem; }
.status { padding:.35rem .65rem; border-radius:999px; background:#10251b;
          border:1px solid #1f6a40; color:#74e2a0; font-size:.75rem; font-weight:700; }
.section { color:#8fa5b6; font-size:.78rem; font-weight:800;
           letter-spacing:.10em; margin:.9rem 0 .55rem; }
.card { border:1px solid #263440; border-radius:16px; background:#101820; padding:1rem; }
.metric { border:1px solid #263440; border-radius:14px; background:#101820;
          padding:.8rem .95rem; min-height:86px; }
.label { color:#8fa5b6; font-size:.7rem; font-weight:700; text-transform:uppercase; }
.value { color:#f1f6fa; font-size:1.18rem; font-weight:800; margin-top:.25rem; }
.pipe { display:inline-block; padding:.5rem .7rem; border:1px solid #2b3b49;
        border-radius:10px; background:#0c141b; margin:.15rem; font-size:.78rem; font-weight:700; }
.done { border-color:#1f6a40; color:#74e2a0; }
.partial { border-color:#775d1e; color:#f0c96b; }
.muted { color:#7f92a0; font-size:.76rem; }
.result { border:1px solid #2b3b49; border-radius:12px; background:#0c141b;
          padding:.8rem; white-space:pre-wrap; font-family:monospace; font-size:.8rem; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_pipeline():
    from pipeline_bridge import process_evidence
    return process_evidence


st.markdown("""
<div class="hero">
  <div style="display:flex;justify-content:space-between;gap:1rem;align-items:flex-start;">
    <div>
      <div class="hero-title">Q-RECON</div>
      <div class="hero-subtitle">AI-Powered Road Quality & Compliance Platform</div>
    </div>
    <div class="status">● PROTOTYPE ONLINE</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section">01 — EVIDENCE INPUT</div>', unsafe_allow_html=True)

left, right = st.columns([1.1, .9], gap="large")

with left:
    uploaded = st.file_uploader(
        "Upload inspection evidence",
        type=["png", "jpg", "jpeg", "webp"],
        help="Use a PNG/JPG/WEBP document image for the current OCR pipeline.",
    )

with right:
    st.markdown("""
    <div class="card">
      <b>Current prototype</b><br><br>
      <span class="muted">
      Real EasyOCR + structured field extraction from the current
      SIH notebook. Handwritten OCR is currently not validated.
      </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section">02 — AI ANALYSIS PIPELINE</div>', unsafe_allow_html=True)

st.markdown("""
<span class="pipe done">✓ Evidence</span>
<span>→</span>
<span class="pipe done">✓ EasyOCR</span>
<span>→</span>
<span class="pipe done">✓ Text Normalization</span>
<span>→</span>
<span class="pipe done">✓ Line Reconstruction</span>
<span>→</span>
<span class="pipe done">✓ Field Extraction</span>
<span>→</span>
<span class="pipe partial">◐ QCR Decision</span>
""", unsafe_allow_html=True)

a, b = st.columns([1,1], gap="large")

with a:
    st.markdown('<div class="section">EVIDENCE PREVIEW</div>', unsafe_allow_html=True)
    if uploaded:
        image = Image.open(uploaded)
        st.image(image, use_container_width=True)
    else:
        st.markdown("""
        <div class="card" style="height:280px;display:flex;align-items:center;
             justify-content:center;text-align:center;color:#718391;">
          <div><div style="font-size:2rem;">🛣️</div>
          <b>No evidence selected</b><br>
          <span class="muted">Upload a QCR inspection image</span></div>
        </div>
        """, unsafe_allow_html=True)

with b:
    st.markdown('<div class="section">03 — INTELLIGENCE OUTPUT</div>', unsafe_allow_html=True)

    if st.button("▶  ANALYZE EVIDENCE", type="primary", use_container_width=True):
        if not uploaded:
            st.warning("Upload an evidence image first.")
        else:
            try:
                with st.spinner("Running OCR + structured extraction..."):
                    processor = get_pipeline()
                    result = processor(
                        file_bytes=uploaded.getvalue(),
                        filename=uploaded.name,
                        mime_type=uploaded.type,
                    )
                st.session_state["result"] = result
            except Exception as e:
                st.error("Pipeline execution failed.")
                st.exception(e)

    result = st.session_state.get("result")

    if result:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f'<div class="metric"><div class="label">Status</div>'
                f'<div class="value">{result.get("status","—")}</div></div>',
                unsafe_allow_html=True)
        with c2:
            conf = result.get("ocr_confidence")
            conf_text = f"{conf:.1f}%" if conf is not None else "—"
            st.markdown(
                f'<div class="metric"><div class="label">OCR Confidence</div>'
                f'<div class="value">{conf_text}</div></div>',
                unsafe_allow_html=True)
        with c3:
            st.markdown(
                f'<div class="metric"><div class="label">Text Regions</div>'
                f'<div class="value">{result.get("detections",0)}</div></div>',
                unsafe_allow_html=True)

        st.write("")
        st.markdown("**STRUCTURED FIELDS**")
        fields = result.get("extracted_fields", {})
        if fields:
            st.dataframe(
                [{"Field": k, "Extracted Value": v} for k, v in fields.items()],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No configured fields were extracted from this image.")

        st.markdown("**RAW / RECONSTRUCTED OCR**")
        st.markdown(
            f'<div class="result">{result.get("ocr_text","")}</div>',
            unsafe_allow_html=True,
        )

        st.write("")
        st.markdown("**VALIDATION STATUS**")
        st.warning(
            "Handwritten OCR: NOT VALIDATED — current notebook uses "
            "EasyOCR English OCR and synthetic PMGSY-grounded QCR images."
        )

    else:
        st.info("Run the analysis to display OCR and structured extraction results.")

st.markdown('<div class="section">04 — PROTOTYPE STATUS</div>', unsafe_allow_html=True)

cols = st.columns(5)
items = [
    ("Evidence Input", "READY", "done"),
    ("EasyOCR", "READY", "done"),
    ("Line Reconstruction", "READY", "done"),
    ("Field Extraction", "READY", "done"),
    ("QCR Decision", "INTEGRATING", "partial"),
]

for col, (name, val, state) in zip(cols, items):
    with col:
        icon = "✓" if state == "done" else "◐"
        st.markdown(
            f'<div class="metric"><div class="label">{name}</div>'
            f'<div class="value" style="font-size:.95rem">{icon} {val}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown(
    '<p style="text-align:center;color:#667987;font-size:.7rem;margin-top:1.2rem">'
    'QCR • SIH 2026 Internal Evaluation Prototype</p>',
    unsafe_allow_html=True,
)
