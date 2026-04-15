import streamlit as st
from datetime import datetime, date
from fpdf import FPDF
import base64
import tempfile
import os

# ================= CONFIG =================
st.set_page_config(
    page_title="Informe de Visita Bromatologica",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ================= CSS =================
st.markdown("""
<style>
html, body {
    font-family: Arial, sans-serif;
}
.item-box {
    border-radius: 8px;
    padding: 10px;
    margin: 8px 0;
    font-weight: 600;
}
.item-cumple { background:#f0fdf4; border-left:5px solid #34d399; }
.item-mejora { background:#fffbeb; border-left:5px solid #fbbf24; }
.item-nocumple { background:#fff1f2; border-left:5px solid #f87171; }
.item-noaplica { background:#f9fafb; border-left:5px solid #d1d5db; }
.item-default { background:#ffffff; border-left:5px solid #e5e7eb; }
</style>
""", unsafe_allow_html=True)

# ================= SECCIONES =================
SECTIONS = [
    ("Instalaciones", "🏗️", [
        "Pisos en buen estado",
        "Paredes limpias",
        "Techos sin humedad",
        "Ventilacion adecuada"
    ]),
    ("Higiene", "🧹", [
        "Superficies limpias",
        "Control de plagas",
        "Productos habilitados"
    ]),
    ("Personal", "👨‍🍳", [
        "Uso de cofia",
        "Lavado de manos",
        "Capacitacion BPM"
    ]),
    ("Temperaturas", "🌡️", [
        "Heladeras entre 0 y 5°C",
        "Freezer bajo -15°C"
    ])
]

ITEM_STYLE = {
    "Cumple": "item-cumple",
    "Necesita Mejora": "item-mejora",
    "No Cumple": "item-nocumple",
    "No Aplica": "item-noaplica",
}

# ================= SESSION =================
def init_state():
    now = datetime.now()

    defaults = {
        "checks": {},
        "observations": {},
        "establishment": "",
        "address": "",
        "auditor": "",
        "audit_date": date.today(),
        "audit_time": now.strftime("%H:%M"),
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()

# ================= HELPERS =================
def calc_score():
    vals = list(st.session_state.checks.values())

    cumple = vals.count("Cumple")
    mejora = vals.count("Necesita Mejora")
    nocumple = vals.count("No Cumple")
    noaplica = vals.count("No Aplica")

    evaluados = cumple + mejora + nocumple
    pct = round((cumple / evaluados) * 100) if evaluados > 0 else 0

    return cumple, mejora, nocumple, noaplica, evaluados, pct


def generate_pdf():
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "INFORME DE VISITA BROMATOLOGICA", ln=True, align="C")

    pdf.ln(5)

    pdf.set_font("Arial", "", 11)
    pdf.cell(190, 8, f"Establecimiento: {st.session_state.establishment}", ln=True)
    pdf.cell(190, 8, f"Direccion: {st.session_state.address}", ln=True)
    pdf.cell(190, 8, f"Auditor: {st.session_state.auditor}", ln=True)
    pdf.cell(190, 8, f"Fecha: {st.session_state.audit_date}", ln=True)
    pdf.cell(190, 8, f"Hora: {st.session_state.audit_time}", ln=True)

    pdf.ln(8)

    for section_name, _, items in SECTIONS:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(190, 8, section_name, ln=True)

        pdf.set_font("Arial", "", 10)

        for idx, item in enumerate(items):
            key = f"{section_name}_{idx}"
            estado = st.session_state.checks.get(key, "Sin evaluar")
            obs = st.session_state.observations.get(key, "")

            pdf.multi_cell(
                190,
                7,
                f"- {item}: {estado}" + (f" | Obs: {obs}" if obs else "")
            )

        pdf.ln(4)

    return bytes(pdf.output(dest="S").encode("latin-1"))

# ================= HEADER =================
st.title("📋 Informe de Visita Bromatologica")

# ================= DATOS =================
st.subheader("📍 Datos del Establecimiento")

col1, col2 = st.columns(2)

with col1:
    st.session_state.establishment = st.text_input(
        "Establecimiento",
        st.session_state.establishment
    )

    st.session_state.address = st.text_input(
        "Direccion",
        st.session_state.address
    )

with col2:
    st.session_state.auditor = st.text_input(
        "Auditor",
        st.session_state.auditor
    )

    st.session_state.audit_date = st.date_input(
        "Fecha",
        st.session_state.audit_date
    )

# ================= CHECKLIST =================
st.divider()

for sec_name, icon, items in SECTIONS:
    with st.expander(f"{icon} {sec_name}", expanded=False):

        for idx, item in enumerate(items):
            key = f"{sec_name}_{idx}"

            estado_actual = st.session_state.checks.get(key, "")
            css = ITEM_STYLE.get(estado_actual, "item-default")

            st.markdown(
                f'<div class="item-box {css}">{idx+1}. {item}</div>',
                unsafe_allow_html=True
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                if st.button("✅ Cumple", key=f"c_{key}"):
                    st.session_state.checks[key] = "Cumple"
                    st.rerun()

            with col2:
                if st.button("⚠️ Mejora", key=f"m_{key}"):
                    st.session_state.checks[key] = "Necesita Mejora"
                    st.rerun()

            with col3:
                if st.button("❌ No Cumple", key=f"nc_{key}"):
                    st.session_state.checks[key] = "No Cumple"
                    st.rerun()

            with col4:
                if st.button("➖ N/A", key=f"na_{key}"):
                    st.session_state.checks[key] = "No Aplica"
                    st.rerun()

            if st.session_state.checks.get(key) in ["Necesita Mejora", "No Cumple"]:
                st.session_state.observations[key] = st.text_area(
                    f"Observacion {idx+1}",
                    st.session_state.observations.get(key, ""),
                    key=f"obs_{key}"
                )

            st.markdown("---")

# ================= RESUMEN =================
st.divider()

cumple, mejora, nocumple, noaplica, evaluados, pct = calc_score()

st.subheader("📊 Resumen")
st.write(f"✅ Cumple: {cumple}")
st.write(f"⚠️ Mejora: {mejora}")
st.write(f"❌ No Cumple: {nocumple}")
st.write(f"➖ No aplica: {noaplica}")
st.write(f"📈 Cumplimiento: {pct}%")

# ================= PDF =================
st.divider()

if st.button("📄 Generar PDF"):
    pdf_bytes = generate_pdf()

    st.download_button(
        "⬇ Descargar PDF",
        data=pdf_bytes,
        file_name="informe_bromatologico.pdf",
        mime="application/pdf"
    )
