import streamlit as st
from datetime import datetime, date
from fpdf import FPDF
import io
import os

st.set_page_config(
    page_title="Auditoría Bromatológica",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #f8f7f4; }
    .header-banner {
        background: linear-gradient(135deg, #1a3a2e 0%, #2d5a45 100%);
        color: white; padding: 32px 24px 20px;
        border-radius: 0 0 16px 16px; text-align: center;
        margin: -4rem -4rem 2rem -4rem;
        border-bottom: 4px solid #4caf7d;
    }
    .header-sub { color: #a7f3c5; font-size: 12px; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 8px; }
    .header-title { font-size: 28px; font-weight: 700; margin: 0; }
    .header-desc { color: #cbd5e1; font-size: 13px; margin-top: 6px; }
    .score-good    { background: #d1fae5; color: #065f46; border: 2px solid #6ee7b7; }
    .score-regular { background: #fef3c7; color: #92400e; border: 2px solid #fcd34d; }
    .score-bad     { background: #fee2e2; color: #991b1b; border: 2px solid #fca5a5; }
    .score-close   { background: #fca5a5; color: #7f1d1d; border: 2px solid #f87171; }
    .item-cumple   { background: #f0fdf4; border-left: 4px solid #34d399; border-radius: 8px; padding: 10px 14px; margin: 6px 0; }
    .item-mejora   { background: #fffbeb; border-left: 4px solid #fbbf24; border-radius: 8px; padding: 10px 14px; margin: 6px 0; }
    .item-nocumple { background: #fff1f2; border-left: 4px solid #f87171; border-radius: 8px; padding: 10px 14px; margin: 6px 0; }
    .item-noaplica { background: #f9fafb; border-left: 4px solid #d1d5db; border-radius: 8px; padding: 10px 14px; margin: 6px 0; }
    .item-default  { background: #ffffff; border-left: 4px solid #e5e7eb; border-radius: 8px; padding: 10px 14px; margin: 6px 0; }
    .stat-box { padding: 14px; border-radius: 10px; text-align: center; }
    .stat-num { font-size: 28px; font-weight: 700; }
    .stat-lbl { font-size: 11px; font-weight: 600; margin-top: 2px; }
    .score-card { padding: 16px; border-radius: 12px; text-align: center; font-weight: 700; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

SECTIONS = [
    ("Instalaciones y Estructura Edilicia", [
        "Pisos en buen estado, sin grietas ni deterioro",
        "Paredes lisas, lavables y en buen estado de higiene",
        "Techos y cielorrasos sin humedad ni desprendimientos",
        "Ventanas y aberturas con proteccion contra insectos (mallas)",
        "Puertas de cierre hermetico y buen estado",
        "Iluminacion adecuada en todos los sectores",
        "Ventilacion suficiente (natural o artificial)",
        "Desagues y sifones en correcto funcionamiento",
        "Separacion entre sectores limpios y sucios",
    ]),
    ("Higiene y Limpieza", [
        "Plan de limpieza y desinfeccion documentado",
        "Productos de limpieza habilitados y correctamente almacenados",
        "Superficies de trabajo limpias y desinfectadas",
        "Equipos y utensilios limpios antes y despues del uso",
        "Cestos de residuos con tapa, limpios y no sobrecargados",
        "Ausencia de olores desagradables en el establecimiento",
        "Programa de control de plagas activo (MIP)",
        "Sin evidencia de roedores o insectos en superficies o alimentos",
        "Registros de limpieza disponibles y actualizados",
    ]),
    ("Personal Manipulador", [
        "Uso de indumentaria adecuada (ropa limpia, cofia, delantal)",
        "Personal sin joyas, anillos ni accesorios",
        "Correcto lavado de manos (tecnica y frecuencia)",
        "Unas cortas, limpias y sin esmalte",
        "Ausencia de personal con sintomas de enfermedad",
        "Capacitacion en BPM (Buenas Practicas de Manufactura)",
        "Registros de capacitacion disponibles",
        "Prohibicion de comer, fumar o beber en el area de trabajo",
        "Uso de guantes donde corresponda",
    ]),
    ("Control de Temperaturas", [
        "Heladeras funcionando entre 0 y 5 grados C",
        "Freezers funcionando a -15 grados C o menos",
        "Registros de temperatura de equipos de frio actualizados",
        "Termometros calibrados disponibles",
        "Alimentos calientes mantenidos a mas de 65 grados C",
        "Sin alimentos que requieran frio a temperatura ambiente",
        "Descongelamiento correcto (en heladera o agua fria corriente)",
        "Control de temperatura al recibir mercaderia",
    ]),
    ("Almacenamiento y Conservacion", [
        "Alimentos almacenados en orden FIFO (primero entrado, primero salido)",
        "Separacion entre alimentos crudos y cocidos",
        "Alimentos separados del suelo y de paredes",
        "Envases en buen estado, sin roturas ni oxidacion",
        "Rotulado completo: nombre, fecha de elaboracion y vencimiento",
        "Sin alimentos vencidos o en mal estado",
        "Productos de limpieza almacenados separados de los alimentos",
        "Deposito seco, fresco, ventilado y protegido de plagas",
    ]),
    ("Agua y Saneamiento", [
        "Agua potable de red o con certificado de potabilidad",
        "Tanque de agua limpio y con tapa",
        "Ultimo analisis de agua disponible y vigente",
        "Instalaciones sanitarias (banos) en buen estado e higiene",
        "Banos con jabon, papel y medios de secado",
        "Banos con carteleria de lavado de manos",
        "Sistema de desague cloacal habilitado",
    ]),
    ("Documentacion y Habilitaciones", [
        "Habilitacion municipal vigente y visible",
        "RNPA / RPPA de los productos (si aplica)",
        "RNE / RPE del establecimiento (si aplica)",
        "Libreta sanitaria del personal al dia",
        "Manual de BPM disponible",
        "Plan HACCP implementado (si aplica por categoria)",
        "Registros de control de procesos disponibles",
        "Ultima auditoria/inspeccion archivada",
    ]),
    ("Gestion de Residuos", [
        "Residuos clasificados correctamente",
        "Frecuencia de retiro de residuos adecuada",
        "Contenedores de residuos con tapa y en buen estado",
        "Area de acopio de residuos limpia y separada de alimentos",
        "Gestion de aceites y grasas conforme a normativa",
    ]),
]

STATUS_OPTIONS = ["-- Seleccionar --", "Cumple", "Necesita Mejora", "No Cumple", "No Aplica"]
STATUS_STYLE = {
    "Cumple":          ("item-cumple",   "OK"),
    "Necesita Mejora": ("item-mejora",   "!!"),
    "No Cumple":       ("item-nocumple", "X"),
    "No Aplica":       ("item-noaplica", "-"),
}

def init_state():
    defaults = {
        "checks": {}, "observations": {},
        "establishment": "", "address": "", "auditor": "",
        "audit_date": date.today(),
        "audit_time": datetime.now().strftime("%H:%M"),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def calc_score():
    vals = list(st.session_state.checks.values())
    cumple   = vals.count("Cumple")
    mejora   = vals.count("Necesita Mejora")
    nocumple = vals.count("No Cumple")
    noaplica = vals.count("No Aplica")
    evaluados = cumple + mejora + nocumple
    pct = round((cumple / evaluados) * 100) if evaluados > 0 else 0
    return cumple, mejora, nocumple, noaplica, evaluados, pct

def score_state(pct):
    if pct >= 80: return "BUENO",        "score-good"
    if pct >= 60: return "REGULAR",      "score-regular"
    if pct >= 40: return "INSUFICIENTE", "score-bad"
    return              "CLAUSURA",      "score-close"

def generate_pdf():
    cumple, mejora, nocumple, noaplica, evaluados, pct = calc_score()
    estado_label, _ = score_state(pct)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_margins(14, 14, 14)
    pdf.set_fill_color(26, 58, 46)
    pdf.rect(0, 0, 210, 38, "F")
    pdf.set_fill_color(76, 175, 125)
    pdf.rect(0, 36, 210, 2, "F")
    pdf.set_xy(0, 8)
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(167, 243, 197)
    pdf.cell(210, 5, "SEGURIDAD ALIMENTARIA - BUENAS PRACTICAS DE MANUFACTURA", align="C")
    pdf.set_xy(0, 14)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(210, 10, "AUDITORIA BROMATOLOGICA", align="C")
    pdf.set_xy(0, 26)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(203, 213, 225)
    pdf.cell(210, 8, "Lista de Verificacion Oficial", align="C")
    pdf.set_xy(14, 44)
    pdf.set_fill_color(240, 253, 244)
    pdf.set_draw_color(76, 175, 125)
    pdf.rect(14, 44, 182, 26, "FD")
    info = [
        ("ESTABLECIMIENTO", st.session_state.establishment or "-", 18, 52),
        ("AUDITOR/A",       st.session_state.auditor or "-",       18, 62),
        ("DIRECCION",       st.session_state.address or "-",      110, 52),
        ("FECHA Y HORA",    f"{st.session_state.audit_date}  {st.session_state.audit_time}", 110, 62),
    ]
    for lbl, val, x, y in info:
        pdf.set_xy(x, y)
        pdf.set_font("Helvetica", "B", 6)
        pdf.set_text_color(107, 114, 128)
        pdf.cell(28, 4, lbl + ":")
        pdf.set_xy(x + 28, y)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(26, 58, 46)
        pdf.cell(60, 4, str(val)[:40])
    badge_colors = {
        "BUENO": (16,185,129), "REGULAR": (217,119,6),
        "INSUFICIENTE": (220,38,38), "CLAUSURA": (127,29,29),
    }
    bc = badge_colors.get(estado_label, (26,58,46))
    pdf.set_fill_color(*bc)
    pdf.rect(160, 44, 36, 26, "F")
    pdf.set_xy(160, 50)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(36, 8, f"{pct}%", align="C")
    pdf.set_xy(160, 60)
    pdf.set_font("Helvetica", "B", 7)
    pdf.cell(36, 4, estado_label, align="C")
    stats = [
        ("Cumple", cumple, (16,185,129)),
        ("Nec. Mejora", mejora, (217,119,6)),
        ("No Cumple", nocumple, (220,38,38)),
        ("No Aplica", noaplica, (156,163,175)),
        ("Total", evaluados, (26,58,46)),
    ]
    bw = 182 / 5
    for i, (lbl_s, val_s, col_s) in enumerate(stats):
        x = 14 + i * bw
        pdf.set_fill_color(*col_s)
        pdf.rect(x, 76, bw-1, 14, "F")
        pdf.set_xy(x, 78)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(bw-1, 5, str(val_s), align="C")
        pdf.set_xy(x, 84)
        pdf.set_font("Helvetica", "", 5)
        pdf.cell(bw-1, 4, lbl_s, align="C")
    pdf.set_y(96)
    for sec_name, items in SECTIONS:
        if pdf.get_y() > 240:
            pdf.add_page()
        pdf.set_fill_color(26, 58, 46)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(182, 8, sec_name, fill=True, ln=True)
        pdf.set_fill_color(240, 253, 244)
        pdf.set_text_color(26, 58, 46)
        pdf.set_font("Helvetica", "B", 7)
        pdf.cell(8,  6, "#",           border=1, fill=True, align="C")
        pdf.cell(90, 6, "Item",        border=1, fill=True)
        pdf.cell(28, 6, "Estado",      border=1, fill=True, align="C")
        pdf.cell(56, 6, "Observacion", border=1, fill=True)
        pdf.ln()
        for idx, item in enumerate(items):
            key = f"{sec_name}_{idx}"
            val = st.session_state.checks.get(key, "")
            obs = st.session_state.observations.get(key, "")
            if val == "Cumple":
                pdf.set_fill_color(209,250,229); tc=(6,95,70)
            elif val == "Necesita Mejora":
                pdf.set_fill_color(254,243,199); tc=(146,64,14)
            elif val == "No Cumple":
                pdf.set_fill_color(254,226,226); tc=(153,27,27)
            elif val == "No Aplica":
                pdf.set_fill_color(243,244,246); tc=(107,114,128)
            else:
                pdf.set_fill_color(255,255,255); tc=(55,65,81)
            pdf.set_text_color(*tc)
            pdf.set_font("Helvetica", "B", 7)
            pdf.cell(8, 7, str(idx+1), border=1, fill=True, align="C")
            pdf.set_font("Helvetica", "", 7)
            pdf.cell(90, 7, item[:65], border=1, fill=True)
            pdf.set_font("Helvetica", "B", 7)
            pdf.cell(28, 7, val or "Sin evaluar", border=1, fill=True, align="C")
            pdf.set_font("Helvetica", "", 6)
            pdf.set_text_color(100,100,100)
            pdf.cell(56, 7, obs[:45], border=1, fill=True)
            pdf.ln()
        pdf.ln(3)
    obs_items = [(k,v) for k,v in st.session_state.observations.items() if v.strip()]
    if obs_items:
        if pdf.get_y() > 220:
            pdf.add_page()
        pdf.set_fill_color(26,58,46)
        pdf.set_text_color(255,255,255)
        pdf.set_font("Helvetica","B",9)
        pdf.cell(182,8,"OBSERVACIONES Y ACCIONES CORRECTIVAS",fill=True,ln=True)
        pdf.ln(2)
        for key, obs in obs_items:
            if pdf.get_y() > 260:
                pdf.add_page()
            parts = key.split("_")
            sec  = "_".join(parts[:-1])
            idx  = int(parts[-1])
            sec_items = next((it for n,it in SECTIONS if n==sec),[])
            item_txt  = sec_items[idx] if idx < len(sec_items) else ""
            pdf.set_fill_color(254,243,199)
            pdf.set_draw_color(217,119,6)
            pdf.set_text_color(146,64,14)
            pdf.set_font("Helvetica","B",7)
            pdf.cell(182,5,f"{sec} - Item {idx+1}: {item_txt}"[:100],border=1,fill=True,ln=True)
            pdf.set_text_color(55,65,81)
            pdf.set_font("Helvetica","",7)
            pdf.cell(182,5,obs[:100],border=1,fill=True,ln=True)
            pdf.ln(1)
    if pdf.get_y() > 240:
        pdf.add_page()
    pdf.ln(8)
    pdf.set_fill_color(249,250,251)
    pdf.set_draw_color(229,231,235)
    half = 88
    pdf.rect(14, pdf.get_y(), half, 28, "FD")
    pdf.rect(14+half+6, pdf.get_y(), half, 28, "FD")
    sig_y = pdf.get_y()+24
    pdf.set_xy(14, sig_y)
    pdf.set_font("Helvetica","",7)
    pdf.set_text_color(107,114,128)
    pdf.cell(half,4,f"Firma Auditor/a: {st.session_state.auditor or ''}",align="C")
    pdf.set_xy(14+half+6, sig_y)
    pdf.cell(half,4,"Firma Responsable del Local",align="C")
    total_pages = pdf.page
    for pg in range(1, total_pages+1):
        pdf.page = pg
        pdf.set_y(-10)
        pdf.set_fill_color(26,58,46)
        pdf.rect(0,287,210,10,"F")
        pdf.set_xy(14,289)
        pdf.set_font("Helvetica","",6)
        pdf.set_text_color(167,243,197)
        est = st.session_state.establishment or "Establecimiento"
        pdf.cell(130,4,f"Auditoria Bromatologica - {est} - {st.session_state.audit_date} {st.session_state.audit_time}")
        pdf.set_xy(150,289)
        pdf.cell(46,4,f"Pagina {pg} de {total_pages}",align="R")
    return bytes(pdf.output())

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
  <div class="header-sub">Seguridad Alimentaria</div>
  <h1 class="header-title">Auditoria Bromatologica</h1>
  <p class="header-desc">Lista de verificacion — Buenas Practicas de Manufactura</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### Datos del Establecimiento")
c1, c2 = st.columns(2)
with c1:
    st.session_state.establishment = st.text_input("Establecimiento", st.session_state.establishment, placeholder="Nombre del local")
    st.session_state.address       = st.text_input("Direccion", st.session_state.address, placeholder="Calle, numero, ciudad")
with c2:
    st.session_state.auditor = st.text_input("Auditor/a", st.session_state.auditor, placeholder="Nombre del auditor")
    dc1, dc2 = st.columns(2)
    with dc1:
        st.session_state.audit_date = st.date_input("Fecha", st.session_state.audit_date)
    with dc2:
        st.session_state.audit_time = st.text_input("Hora", st.session_state.audit_time, placeholder="HH:MM")

st.divider()

total_items  = sum(len(items) for _, items in SECTIONS)
answered     = len([v for v in st.session_state.checks.values() if v])
progress_pct = answered / total_items if total_items > 0 else 0

st.markdown(f"**Progreso:** {answered} / {total_items} items respondidos")
st.progress(progress_pct)

if answered > 0:
    cumple, mejora, nocumple, noaplica, evaluados, pct = calc_score()
    estado_label, estado_class = score_state(pct)
    sc1,sc2,sc3,sc4,sc5 = st.columns(5)
    with sc1:
        st.markdown(f'<div class="stat-box" style="background:#d1fae5;color:#065f46"><div class="stat-num">{cumple}</div><div class="stat-lbl">Cumple</div></div>',unsafe_allow_html=True)
    with sc2:
        st.markdown(f'<div class="stat-box" style="background:#fef3c7;color:#92400e"><div class="stat-num">{mejora}</div><div class="stat-lbl">Nec. Mejora</div></div>',unsafe_allow_html=True)
    with sc3:
        st.markdown(f'<div class="stat-box" style="background:#fee2e2;color:#991b1b"><div class="stat-num">{nocumple}</div><div class="stat-lbl">No Cumple</div></div>',unsafe_allow_html=True)
    with sc4:
        st.markdown(f'<div class="stat-box" style="background:#f3f4f6;color:#6b7280"><div class="stat-num">{noaplica}</div><div class="stat-lbl">No Aplica</div></div>',unsafe_allow_html=True)
    with sc5:
        st.markdown(f'<div class="stat-box {estado_class}"><div class="stat-num">{pct}%</div><div class="stat-lbl">{estado_label}</div></div>',unsafe_allow_html=True)
    st.write("")

st.divider()

for sec_name, items in SECTIONS:
    sec_checks  = [st.session_state.checks.get(f"{sec_name}_{i}","") for i in range(len(items))]
    sec_answered = len([v for v in sec_checks if v])
    sec_cumple   = sec_checks.count("Cumple")
    sec_eval     = len([v for v in sec_checks if v and v != "No Aplica"])
    sec_pct      = f"{round(sec_cumple/sec_eval*100)}%" if sec_eval > 0 else ""
    with st.expander(f"{sec_name}  —  {sec_answered}/{len(items)} respondidos  {sec_pct}", expanded=False):
        for idx, item in enumerate(items):
            key = f"{sec_name}_{idx}"
            cur = st.session_state.checks.get(key, "")
            css_class = STATUS_STYLE.get(cur,("item-default",""))[0] if cur else "item-default"
            icon      = STATUS_STYLE.get(cur,("",""))[1] if cur else "o"
            st.markdown(f'<div class="{css_class}"><strong>[{icon}] {idx+1}.</strong> {item}</div>',unsafe_allow_html=True)
            col_sel, col_obs = st.columns([1,2])
            with col_sel:
                options = STATUS_OPTIONS
                sel_idx = options.index(cur) if cur in options else 0
                new_val = st.selectbox("Estado", options, index=sel_idx, key=f"sel_{key}", label_visibility="collapsed")
                if new_val != "-- Seleccionar --":
                    st.session_state.checks[key] = new_val
                elif key in st.session_state.checks:
                    del st.session_state.checks[key]
            with col_obs:
                if cur in ("Necesita Mejora","No Cumple"):
                    obs = st.text_area("Observacion", value=st.session_state.observations.get(key,""),
                        placeholder="Observacion / accion correctiva...",
                        key=f"obs_{key}", height=68, label_visibility="collapsed")
                    st.session_state.observations[key] = obs
        st.write("")

st.divider()

if answered > 0:
    cumple, mejora, nocumple, noaplica, evaluados, pct = calc_score()
    estado_label, estado_class = score_state(pct)
    with st.expander("Ver Resumen de Auditoria", expanded=False):
        st.markdown("#### Resultados por Seccion")
        cols = st.columns([3,1,1,1,1,1])
        for col, h in zip(cols,["Seccion","Cumple","Nec. Mejora","No Cumple","No Aplica","% Cump."]):
            col.markdown(f"**{h}**")
        for sec_name, items in SECTIONS:
            vals = [st.session_state.checks.get(f"{sec_name}_{i}","") for i in range(len(items))]
            sc=vals.count("Cumple"); nm=vals.count("Necesita Mejora")
            nc=vals.count("No Cumple"); na=vals.count("No Aplica")
            ev=sc+nm+nc; p=f"{round(sc/ev*100)}%" if ev>0 else "-"
            cols=st.columns([3,1,1,1,1,1])
            cols[0].write(sec_name); cols[1].write(f"OK {sc}")
            cols[2].write(f"!! {nm}"); cols[3].write(f"X {nc}")
            cols[4].write(f"- {na}");  cols[5].write(p)
        st.markdown(f'<div class="score-card {estado_class}" style="margin-top:16px;font-size:22px;">{pct}%  —  {estado_label}</div>',unsafe_allow_html=True)

st.markdown("### Generar Informe")
col_pdf, col_reset = st.columns([3,1])
with col_pdf:
    if st.button("Generar PDF para el Responsable del Local", use_container_width=True, type="primary"):
        with st.spinner("Generando PDF..."):
            pdf_bytes = generate_pdf()
        fname = f"Auditoria_{(st.session_state.establishment or 'local').replace(' ','_')}_{st.session_state.audit_date}.pdf"
        st.download_button(label="Descargar PDF", data=pdf_bytes, file_name=fname,
            mime="application/pdf", use_container_width=True)
with col_reset:
    if st.button("Nueva Auditoria", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.markdown("---")
st.markdown("<p style='text-align:center;color:#9ca3af;font-size:11px;'>Basado en el Codigo Alimentario Argentino (CAA) y normativas BPM vigentes</p>", unsafe_allow_html=True)
