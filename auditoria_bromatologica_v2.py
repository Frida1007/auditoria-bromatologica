import streamlit as st
from datetime import datetime, date
from fpdf import FPDF
import base64, tempfile, os

st.set_page_config(
    page_title="Informe de Visita Bromatologica",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #f0f4f8 !important; color: #1a1a1a !important; }
    .stApp { background-color: #f0f4f8 !important; }
    .stApp > div { background-color: #f0f4f8 !important; }
    div[data-testid="stExpander"] { background-color: #ffffff !important; color: #1a1a1a !important; }
    div[data-testid="stExpander"] p, div[data-testid="stExpander"] span { color: #1a1a1a !important; }
    .streamlit-expanderContent { background-color: #ffffff !important; }
    div[data-testid="stTextInput"] input { background-color: #ffffff !important; color: #1a1a1a !important; font-size: 15px !important; border: 1px solid #d1d5db !important; }
    div[data-testid="stSelectbox"] > div { background-color: #ffffff !important; color: #1a1a1a !important; font-size: 14px !important; }
    div[data-testid="stTextArea"] textarea { background-color: #ffffff !important; color: #1a1a1a !important; font-size: 14px !important; }
    label { color: #1a1a1a !important; } p { color: #1a1a1a !important; } h1,h2,h3 { color: #1a2e1a !important; }
    .header-banner {
        background: linear-gradient(135deg, #1a3a2e 0%, #2d5a45 100%);
        color: white; padding: 10px 16px;
        border-radius: 0 0 12px 12px; text-align: center;
        margin: -4rem -4rem 1rem -4rem;
        border-bottom: 3px solid #4caf7d;
    }
    .header-sub   { color: #a7f3c5; font-size: 10px; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 2px; }
    .header-title { font-size: 15px; font-weight: 800; margin: 0; color: white !important; }
    .header-desc  { color: #cbd5e1; font-size: 10px; margin-top: 2px; }
    .stat-row { display: flex; gap: 5px; margin: 6px 0; }
    .stat-pill { flex: 1; padding: 5px 2px; border-radius: 8px; text-align: center; font-weight: 700; }
    .stat-num { font-size: 15px; font-weight: 800; line-height: 1.1; }
    .stat-lbl { font-size: 8px; font-weight: 600; margin-top: 1px; text-transform: uppercase; }
    .s-cumple   { background:#d1fae5; color:#065f46 !important; border:2px solid #6ee7b7; }
    .s-mejora   { background:#fef3c7; color:#92400e !important; border:2px solid #fcd34d; }
    .s-nocumple { background:#fee2e2; color:#991b1b !important; border:2px solid #fca5a5; }
    .s-noaplica { background:#f3f4f6; color:#374151 !important; border:2px solid #d1d5db; }
    .s-pct-good { background:#065f46; color:#fff !important; border:2px solid #059669; }
    .s-pct-reg  { background:#92400e; color:#fff !important; border:2px solid #d97706; }
    .s-pct-bad  { background:#991b1b; color:#fff !important; border:2px solid #dc2626; }
    .s-pct-cls  { background:#7f1d1d; color:#fff !important; border:2px solid #b91c1c; }
    .item-box { border-radius: 8px; padding: 10px 14px; margin: 6px 0; font-size: 15px !important; font-weight: 600 !important; line-height: 1.4; color: #1a1a1a !important; }
    .item-cumple   { background:#f0fdf4; border-left:5px solid #34d399; }
    .item-mejora   { background:#fffbeb; border-left:5px solid #fbbf24; }
    .item-nocumple { background:#fff1f2; border-left:5px solid #f87171; }
    .item-noaplica { background:#f9fafb; border-left:5px solid #d1d5db; }
    .item-default  { background:#ffffff; border-left:5px solid #e5e7eb; }
    div[data-testid="stTextInput"] label  { font-size: 15px !important; font-weight: 600 !important; color: #1a1a1a !important; }
    div[data-testid="stDateInput"] label  { font-size: 15px !important; font-weight: 600 !important; color: #1a1a1a !important; }
    div[data-testid="stFileUploader"] label { font-size: 13px !important; font-weight: 600 !important; }
    .stButton > button { border-radius: 10px; font-weight: 700; height: 46px; font-size: 13px; }
    footer { visibility: hidden; } #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

SECTIONS = [
    ("Instalaciones y Estructura Edilicia", "\U0001f3d7\ufe0f", [
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
    ("Higiene y Limpieza", "\U0001f9f9", [
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
    ("Personal Manipulador", "\U0001f468\u200d\U0001f373", [
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
    ("Control de Temperaturas", "\U0001f321\ufe0f", [
        "Heladeras funcionando entre 0 y 5 grados C",
        "Freezers funcionando a -15 grados C o menos",
        "Registros de temperatura de equipos de frio actualizados",
        "Termometros calibrados disponibles",
        "Alimentos calientes mantenidos a mas de 65 grados C",
        "Sin alimentos que requieran frio a temperatura ambiente",
        "Descongelamiento correcto (en heladera o agua fria corriente)",
        "Control de temperatura al recibir mercaderia",
    ]),
    ("Almacenamiento y Conservacion", "\U0001f4e6", [
        "Alimentos almacenados en orden FIFO (primero entrado, primero salido)",
        "Separacion entre alimentos crudos y cocidos",
        "Alimentos separados del suelo y de paredes",
        "Envases en buen estado, sin roturas ni oxidacion",
        "Rotulado completo: nombre, fecha de elaboracion y vencimiento",
        "Sin alimentos vencidos o en mal estado",
        "Productos de limpieza almacenados separados de los alimentos",
        "Deposito seco, fresco, ventilado y protegido de plagas",
    ]),
    ("Agua y Saneamiento", "\U0001f4a7", [
        "Agua potable de red o con certificado de potabilidad",
        "Tanque de agua limpio y con tapa",
        "Ultimo analisis de agua disponible y vigente",
        "Instalaciones sanitarias (banos) en buen estado e higiene",
        "Banos con jabon, papel y medios de secado",
        "Banos con carteleria de lavado de manos",
        "Sistema de desague cloacal habilitado",
    ]),
    ("Documentacion y Habilitaciones", "\U0001f4cb", [
        "Habilitacion municipal vigente y visible",
        "RNPA / RPPA de los productos (si aplica)",
        "RNE / RPE del establecimiento (si aplica)",
        "Libreta sanitaria del personal al dia",
        "Manual de BPM disponible",
        "Plan HACCP implementado (si aplica por categoria)",
        "Registros de control de procesos disponibles",
        "Ultima auditoria/inspeccion archivada",
    ]),
    ("Gestion de Residuos", "\u267b\ufe0f", [
        "Residuos clasificados correctamente",
        "Frecuencia de retiro de residuos adecuada",
        "Contenedores de residuos con tapa y en buen estado",
        "Area de acopio de residuos limpia y separada de alimentos",
        "Gestion de aceites y grasas conforme a normativa",
    ]),
]

ITEM_STYLE = {
    "Cumple":          "item-cumple",
    "Necesita Mejora": "item-mejora",
    "No Cumple":       "item-nocumple",
    "No Aplica":       "item-noaplica",
}

def init_state():
    now = datetime.now()
    defaults = {
        "checks": {}, "observations": {}, "photos": {},
        "establishment": "", "address": "", "auditor": "",
        "audit_date": date.today(),
        "audit_time": now.strftime("%H:%M"),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def fmt_date(d):
    return d.strftime("%d/%m/%Y") if d else ""

def calc_score():
    vals = list(st.session_state.checks.values())
    c  = vals.count("Cumple")
    m  = vals.count("Necesita Mejora")
    nc = vals.count("No Cumple")
    na = vals.count("No Aplica")
    ev = c + m + nc
    pct = round((c / ev) * 100) if ev > 0 else 0
    return c, m, nc, na, ev, pct

def score_state(pct):
    if pct >= 80: return "BUENO",        "s-pct-good"
    if pct >= 60: return "REGULAR",      "s-pct-reg"
    if pct >= 40: return "INSUFICIENTE", "s-pct-bad"
    return             "CLAUSURA",       "s-pct-cls"

def pdf_footer(pdf, est, fecha, hora):
    total = pdf.page
    for pg in range(1, total + 1):
        pdf.page = pg
        pdf.set_y(-10)
        pdf.set_fill_color(26, 58, 46)
        pdf.rect(0, 287, 210, 10, "F")
        pdf.set_xy(14, 289)
        pdf.set_font("Helvetica", "", 6)
        pdf.set_text_color(167, 243, 197)
        pdf.cell(130, 4, f"Informe Visita Bromatologica - {est} - {fecha} {hora}")
        pdf.set_xy(150, 289)
        pdf.cell(46, 4, f"Pagina {pg} de {total}", align="R")

def generate_pdf():
    cumple, mejora, nocumple, noaplica, evaluados, pct = calc_score()
    estado_label, _ = score_state(pct)
    est   = st.session_state.establishment or "Establecimiento"
    fecha = fmt_date(st.session_state.audit_date)
    hora  = st.session_state.audit_time

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(14, 14, 14)
    pdf.add_page()

    pdf.set_fill_color(26, 58, 46)
    pdf.rect(0, 0, 210, 44, "F")
    pdf.set_fill_color(76, 175, 125)
    pdf.rect(0, 42, 210, 2, "F")
    pdf.set_xy(14, 7)
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(167, 243, 197)
    pdf.cell(182, 5, "SEGURIDAD ALIMENTARIA - BUENAS PRACTICAS DE MANUFACTURA", align="C")
    pdf.set_xy(14, 14)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(182, 8, "INFORME DE VISITA BROMATOLOGICA", align="C")
    pdf.set_xy(14, 24)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(203, 213, 225)
    pdf.cell(182, 5, "Lic. C. Anabel Marin - Food Quality & Safety Consulting", align="C")
    pdf.set_xy(14, 32)
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(167, 243, 197)
    pdf.cell(182, 5, f"Fecha: {fecha}   Hora: {hora}", align="C")

    y = 50
    pdf.set_fill_color(240, 253, 244)
    pdf.set_draw_color(76, 175, 125)
    pdf.rect(14, y, 144, 26, "FD")
    info_rows = [
        ("ESTABLECIMIENTO", est,                              y + 7),
        ("AUDITOR/A",       st.session_state.auditor or "-", y + 17),
    ]
    for lbl, val, fy in info_rows:
        pdf.set_xy(18, fy)
        pdf.set_font("Helvetica", "B", 7)
        pdf.set_text_color(107, 114, 128)
        pdf.cell(32, 5, lbl + ":")
        pdf.set_xy(50, fy)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(26, 58, 46)
        pdf.cell(80, 5, str(val)[:40])

    badge_colors = {
        "BUENO": (16, 185, 129),
        "REGULAR": (217, 119, 6),
        "INSUFICIENTE": (220, 38, 38),
        "CLAUSURA": (127, 29, 29)
    }
    bc = badge_colors.get(estado_label, (26, 58, 46))
    pdf.set_fill_color(*bc)
    pdf.rect(160, y, 36, 26, "F")
    pdf.set_xy(160, y + 4)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(36, 10, f"{pct}%", align="C")
    pdf.set_xy(160, y + 16)
    pdf.set_font("Helvetica", "B", 6)
    pdf.cell(36, 5, estado_label, align="C")

    y2 = y + 32
    stats = [
        ("Cumple",    cumple,    (16, 185, 129)),
        ("Nec. Mej.", mejora,    (217, 119, 6)),
        ("No Cumple", nocumple,  (220, 38, 38)),
        ("No Aplica", noaplica,  (156, 163, 175)),
        ("Total",     evaluados, (26, 58, 46)),
    ]
    bw = 182 / 5
    for i, (ls, vs, cs) in enumerate(stats):
        x = 14 + i * bw
        pdf.set_fill_color(*cs)
        pdf.rect(x, y2, bw - 1, 13, "F")
        pdf.set_xy(x, y2 + 1)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(bw - 1, 5, str(vs), align="C")
        pdf.set_xy(x, y2 + 7)
        pdf.set_font("Helvetica", "", 5.5)
        pdf.cell(bw - 1, 4, ls, align="C")
    pdf.set_y(y2 + 18)

    for sec_idx, (sec_name, icon, items) in enumerate(SECTIONS):
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
        pdf.cell(86, 6, "Item",        border=1, fill=True)
        pdf.cell(26, 6, "Estado",      border=1, fill=True, align="C")
        pdf.cell(50, 6, "Observacion", border=1, fill=True)
        pdf.cell(12, 6, "Ref.",        border=1, fill=True, align="C")
        pdf.ln()
        for idx, item in enumerate(items):
            key    = f"{sec_name}_{idx}"
            val    = st.session_state.checks.get(key, "")
            obs    = st.session_state.observations.get(key, "")
            photos = st.session_state.photos.get(key, [])
            ref    = f"F-{sec_idx+1}.{idx+1}" if photos else ""
            if val == "Cumple":
                pdf.set_fill_color(209, 250, 229); tc = (6, 95, 70)
            elif val == "Necesita Mejora":
                pdf.set_fill_color(254, 243, 199); tc = (146, 64, 14)
            elif val == "No Cumple":
                pdf.set_fill_color(254, 226, 226); tc = (153, 27, 27)
            elif val == "No Aplica":
                pdf.set_fill_color(243, 244, 246); tc = (107, 114, 128)
            else:
                pdf.set_fill_color(255, 255, 255); tc = (55, 65, 81)
            pdf.set_text_color(*tc)
            pdf.set_font("Helvetica", "B", 7)
            pdf.cell(8,  7, str(idx + 1),      border=1, fill=True, align="C")
            pdf.set_font("Helvetica", "", 7)
            pdf.cell(86, 7, item[:62],          border=1, fill=True)
            pdf.set_font("Helvetica", "B", 6.5)
            pdf.cell(26, 7, val or "Sin eval.", border=1, fill=True, align="C")
            pdf.set_font("Helvetica", "", 6)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(50, 7, obs[:40],           border=1, fill=True)
            pdf.set_font("Helvetica", "B", 7)
            if ref:
                pdf.set_text_color(26, 58, 46)
            else:
                pdf.set_text_color(180, 180, 180)
            pdf.cell(12, 7, ref,                border=1, fill=True, align="C")
            pdf.ln()
        pdf.ln(3)

    obs_items = [(k, v) for k, v in st.session_state.observations.items() if v.strip()]
    if obs_items:
        if pdf.get_y() > 220:
            pdf.add_page()
        pdf.set_fill_color(26, 58, 46)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(182, 8, "OBSERVACIONES Y ACCIONES CORRECTIVAS", fill=True, ln=True)
        pdf.ln(2)
        for key, obs in obs_items:
            if pdf.get_y() > 255:
                pdf.add_page()
            parts     = key.split("_")
            sec       = "_".join(parts[:-1])
            idx       = int(parts[-1])
            sec_idx2  = next((i for i, (n, _, _) in enumerate(SECTIONS) if n == sec), 0)
            sec_items = next((it for n, _, it in SECTIONS if n == sec), [])
            item_txt  = sec_items[idx] if idx < len(sec_items) else ""
            ref       = f"F-{sec_idx2+1}.{idx+1}" if st.session_state.photos.get(key) else ""
            pdf.set_fill_color(254, 243, 199)
            pdf.set_draw_color(217, 119, 6)
            pdf.set_text_color(146, 64, 14)
            pdf.set_font("Helvetica", "B", 7)
            ref_txt = f"  [Ver {ref} en Anexo]" if ref else ""
            pdf.cell(182, 5, f"{sec} - Item {idx+1}: {item_txt}{ref_txt}"[:95], border=1, fill=True, ln=True)
            pdf.set_text_color(55, 65, 81)
            pdf.set_font("Helvetica", "", 7)
            pdf.cell(182, 5, obs[:100], border=1, fill=True, ln=True)
            pdf.ln(1)

    if pdf.get_y() > 245:
        pdf.add_page()
    pdf.ln(8)
    half = 88
    pdf.set_fill_color(249, 250, 251)
    pdf.set_draw_color(229, 231, 235)
    pdf.rect(14, pdf.get_y(), half, 28, "FD")
    pdf.rect(14 + half + 6, pdf.get_y(), half, 28, "FD")
    sig_y = pdf.get_y() + 24
    pdf.set_xy(14, sig_y)
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(107, 114, 128)
    aud = st.session_state.auditor or ""
    pdf.cell(half, 4, f"Firma Auditor/a: {aud}", align="C")
    pdf.set_xy(14 + half + 6, sig_y)
    pdf.cell(half, 4, "Firma Responsable del Local", align="C")

    all_photos = []
    for sec_idx2, (sec_name, icon, items) in enumerate(SECTIONS):
        for idx, item in enumerate(items):
            key    = f"{sec_name}_{idx}"
            photos = st.session_state.photos.get(key, [])
            obs    = st.session_state.observations.get(key, "")
            if photos:
                all_photos.append({
                    "ref":    f"F-{sec_idx2+1}.{idx+1}",
                    "sec":    sec_name,
                    "idx":    idx + 1,
                    "item":   item,
                    "obs":    obs,
                    "photos": photos,
                })

    if all_photos:
        pdf.add_page()
        pdf.set_fill_color(26, 58, 46)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(182, 12, "ANEXO FOTOGRAFICO", fill=True, ln=True, align="C")
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(107, 114, 128)
        pdf.cell(182, 6, "Evidencia fotografica vinculada a las observaciones del informe", ln=True, align="C")
        pdf.ln(4)
        for entry in all_photos:
            ref    = entry["ref"]
            sec    = entry["sec"]
            idx    = entry["idx"]
            item   = entry["item"]
            obs    = entry["obs"]
            photos = entry["photos"]
            if pdf.get_y() > 200:
                pdf.add_page()
            pdf.set_fill_color(26, 58, 46)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", "B", 8)
            pdf.cell(182, 7, f"{ref}  |  {sec}  -  Item {idx}: {item[:60]}", fill=True, ln=True)
            if obs:
                pdf.set_fill_color(254, 243, 199)
                pdf.set_text_color(146, 64, 14)
                pdf.set_font("Helvetica", "", 7)
                pdf.cell(182, 5, f"Observacion: {obs[:90]}", fill=True, ln=True, border=1)
            photo_w = 58
            photo_h = 50
            gap     = (182 - 3 * photo_w) / 2
            start_x = 14
            py      = pdf.get_y() + 2
            for pi, ph in enumerate(photos[:3]):
                try:
                    img_data = base64.b64decode(ph)
                    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                        tmp.write(img_data)
                        tmp_path = tmp.name
                    px = start_x + pi * (photo_w + gap)
                    pdf.image(tmp_path, x=px, y=py, w=photo_w, h=photo_h)
                    os.unlink(tmp_path)
                    pdf.set_xy(px, py + photo_h + 1)
                    pdf.set_font("Helvetica", "B", 6)
                    pdf.set_text_color(26, 58, 46)
                    pdf.cell(photo_w, 4, f"{ref} - Foto {pi+1}", align="C")
                except Exception:
                    pass
            pdf.set_y(py + photo_h + 7)
            pdf.ln(3)

    pdf_footer(pdf, est, fecha, hora)
    return bytes(pdf.output())


st.markdown(f"""
<div class="header-banner">
  <div class="header-sub">Food Quality &amp; Safety Consulting</div>
  <h1 class="header-title">Informe de Visita Bromatologica</h1>
  <p class="header-desc">Lic. C. Anabel Marin - Lista de verificacion BPM</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### \U0001f4cd Datos del Establecimiento")
c1, c2 = st.columns(2)
with c1:
    st.session_state.establishment = st.text_input("**Establecimiento**", st.session_state.establishment, placeholder="Nombre del local")
    st.session_state.address       = st.text_input("**Direccion**",       st.session_state.address,       placeholder="Calle, numero, ciudad")
with c2:
    st.session_state.auditor = st.text_input("**Auditor/a**", st.session_state.auditor, placeholder="Nombre del auditor")
    dc1, dc2 = st.columns(2)
    with dc1:
        st.session_state.audit_date = st.date_input("**Fecha**", st.session_state.audit_date, format="DD/MM/YYYY")
    with dc2:
        st.session_state.audit_time = st.text_input("**Hora**", st.session_state.audit_time, placeholder="HH:MM")

st.divider()

total_items = sum(len(it) for _, _, it in SECTIONS)
answered    = len([v for v in st.session_state.checks.values() if v])
st.markdown(f"**Progreso:** {answered} / {total_items} items respondidos")
st.progress(answered / total_items if total_items > 0 else 0)

if answered > 0:
    cumple, mejora, nocumple, noaplica, evaluados, pct = calc_score()
    estado_label, pct_cls = score_state(pct)
    st.markdown(f"""
    <div class="stat-row">
      <div class="stat-pill s-cumple"><div class="stat-num">{cumple}</div><div class="stat-lbl">Cumple</div></div>
      <div class="stat-pill s-mejora"><div class="stat-num">{mejora}</div><div class="stat-lbl">Mejora</div></div>
      <div class="stat-pill s-nocumple"><div class="stat-num">{nocumple}</div><div class="stat-lbl">No Cumple</div></div>
      <div class="stat-pill s-noaplica"><div class="stat-num">{noaplica}</div><div class="stat-lbl">No Aplica</div></div>
      <div class="stat-pill {pct_cls}"><div class="stat-num">{pct}%</div><div class="stat-lbl">{estado_label}</div></div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

for sec_name, icon, items in SECTIONS:
    sec_checks = [st.session_state.checks.get(f"{sec_name}_{i}", "") for i in range(len(items))]
    sec_ans    = len([v for v in sec_checks if v])
    sec_cumple = sec_checks.count("Cumple")
    sec_ev     = len([v for v in sec_checks if v and v != "No Aplica"])
    sec_pct    = f"  {round(sec_cumple/sec_ev*100)}%" if sec_ev > 0 else ""

    with st.expander(f"{icon}  **{sec_name}**  -  {sec_ans}/{len(items)}{sec_pct}", expanded=False):
        for idx, item in enumerate(items):
            key = f"{sec_name}_{idx}"
            cur = st.session_state.checks.get(key, "")
            css = ITEM_STYLE.get(cur, "item-default")
            st.markdown(f'<div class="item-box {css}"><b>{idx+1}.</b> {item}</div>', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("\u2705 Cumple",          key=f"c_{key}",  use_container_width=True):
                    st.session_state.checks[key] = "Cumple";          st.rerun()
            with col2:
                if st.button("\u26a0\ufe0f Nec. Mejora", key=f"m_{key}",  use_container_width=True):
                    st.session_state.checks[key] = "Necesita Mejora"; st.rerun()
            with col3:
                if st.button("\u274c No Cumple",        key=f"nc_{key}", use_container_width=True):
                    st.session_state.checks[key] = "No Cumple";       st.rerun()
            with col4:
                if st.button("\u2796 No Aplica",        key=f"na_{key}", use_container_width=True):
                    st.session_state.checks[key] = "No Aplica";       st.rerun()
            if cur in ("Necesita Mejora", "No Cumple"):
                st.markdown("**\U0001f4dd Observacion / Accion correctiva:**")
                obs = st.text_area("obs", value=st.session_state.observations.get(key, ""),
                    placeholder="Escribi la observacion o accion correctiva aqui...",
                    key=f"obs_{key}", height=80, label_visibility="collapsed")
                st.session_state.observations[key] = obs
                st.markdown("**\U0001f4f7 Agregar fotos (se incluyen en Anexo del PDF):**")
                uploaded = st.file_uploader("Subir fotos", type=["jpg","jpeg","png"],
                    accept_multiple_files=True, key=f"photo_{key}", label_visibility="collapsed")
                if uploaded:
                    photos_b64 = []
                    cols_img   = st.columns(min(len(uploaded), 3))
                    for i, uf in enumerate(uploaded[:3]):
                        b64 = base64.b64encode(uf.read()).decode()
                        photos_b64.append(b64)
                        with cols_img[i]:
                            st.image(uf, use_container_width=True)
                    st.session_state.photos[key] = photos_b64
                    sec_idx3 = next((i for i, (n, _, _) in enumerate(SECTIONS) if n == sec_name), 0)
                    st.info(f"\U0001f4ce Referencia en PDF: F-{sec_idx3+1}.{idx+1}")
            st.markdown("---")
        st.write("")

st.divider()

st.markdown("### \U0001f4c4 Generar Informe")
col_pdf, col_reset = st.columns([3, 1])
with col_pdf:
    if st.button("\U0001f4c4 Generar PDF para el Responsable del Local", use_container_width=True, type="primary"):
        with st.spinner("Generando PDF con Anexo Fotografico..."):
            pdf_bytes = generate_pdf()
            fname = (
                "Visita_"
                + (st.session_state.establishment or "local").replace(" ", "_")
                + "_"
                + fmt_date(st.session_state.audit_date).replace("/", "_")
                + ".pdf"
            )
            st.download_button(label="\u2b07\ufe0f Descargar PDF", data=pdf_bytes,
                file_name=fname, mime="application/pdf", use_container_width=True)
with col_reset:
    if st.button("\U0001f504 Nueva Visita", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#9ca3af;font-size:10px;'>"
    "Lic. C. Anabel Marin - Food Quality &amp; Safety Consulting | Codigo Alimentario Argentino (CAA)"
    "</p>",
    unsafe_allow_html=True,
)
