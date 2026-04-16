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

ICON_B64 = "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"

def inject_icon():
    st.markdown(
        f'''<head>
        <link rel="apple-touch-icon" href="data:image/png;base64,{ICON_B64}">
        <link rel="shortcut icon" type="image/png" href="data:image/png;base64,{ICON_B64}">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="Auditoria BPM">
        <meta name="theme-color" content="#1a3a2e">
        </head>''',
        unsafe_allow_html=True,
    )

inject_icon()

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

    # Header
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

    # Info block
    y = 50
    pdf.set_fill_color(240, 253, 244)
    pdf.set_draw_color(76, 175, 125)
    pdf.rect(14, y, 144, 26, "FD")
    # Fila 1: Establecimiento
    pdf.set_xy(18, y + 7)
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(32, 5, "ESTABLECIMIENTO:")
    pdf.set_xy(50, y + 7)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(26, 58, 46)
    pdf.cell(80, 5, str(est)[:40])
    # Fila 2: Auditor + Fecha + Hora en el mismo renglon
    pdf.set_xy(18, y + 17)
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(22, 5, "AUDITOR/A:")
    pdf.set_xy(40, y + 17)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(26, 58, 46)
    pdf.cell(38, 5, str(st.session_state.auditor or "-")[:22])
    pdf.set_xy(80, y + 17)
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(16, 5, "FECHA:")
    pdf.set_xy(96, y + 17)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(26, 58, 46)
    pdf.cell(28, 5, fecha)
    pdf.set_xy(126, y + 17)
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(12, 5, "HORA:")
    pdf.set_xy(138, y + 17)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(26, 58, 46)
    pdf.cell(18, 5, hora)

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

    # Stats
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

    # Section tables
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

    # Observations summary
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
            parts    = key.split("_")
            sec      = "_".join(parts[:-1])
            idx      = int(parts[-1])
            sec_idx2 = next((i for i, (n, _, _) in enumerate(SECTIONS) if n == sec), 0)
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

    # Signatures
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

    # Anexo fotografico
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


# ═══════════════════════════════════════════════════════════ UI ═══

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
                obs = st.text_area(
                    "obs",
                    value=st.session_state.observations.get(key, ""),
                    placeholder="Escribi la observacion o accion correctiva aqui...",
                    key=f"obs_{key}",
                    height=80,
                    label_visibility="collapsed",
                )
                st.session_state.observations[key] = obs

                st.markdown("**\U0001f4f7 Agregar fotos (se incluyen en Anexo del PDF):**")
                uploaded = st.file_uploader(
                    "Subir fotos",
                    type=["jpg", "jpeg", "png"],
                    accept_multiple_files=True,
                    key=f"photo_{key}",
                    label_visibility="collapsed",
                )
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
            st.download_button(
                label="\u2b07\ufe0f Descargar PDF",
                data=pdf_bytes,
                file_name=fname,
                mime="application/pdf",
                use_container_width=True,
            )
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
