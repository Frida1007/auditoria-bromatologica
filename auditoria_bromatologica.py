import streamlit as st
from datetime import datetime, date
from fpdf import FPDF
import base64, io, tempfile, os

st.set_page_config(
    page_title="Informe de Visita Bromatologica",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #f0f4f8; }
    .header-banner {
        background: linear-gradient(135deg, #1a3a2e 0%, #2d5a45 100%);
        color: white; padding: 20px 24px 16px;
        border-radius: 0 0 16px 16px; text-align: center;
        margin: -4rem -4rem 1.5rem -4rem;
        border-bottom: 4px solid #4caf7d;
    }
    .header-sub  { color: #a7f3c5; font-size: 11px; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 6px; }
    .header-title{ font-size: 22px; font-weight: 800; margin: 0; }
    .header-desc { color: #cbd5e1; font-size: 11px; margin-top: 4px; }
    .stat-row { display: flex; gap: 8px; margin: 10px 0; }
    .stat-pill { flex: 1; padding: 8px 4px; border-radius: 10px; text-align: center; font-weight: 700; }
    .stat-num { font-size: 20px; font-weight: 800; line-height: 1.1; }
    .stat-lbl { font-size: 9px; font-weight: 600; margin-top: 2px; text-transform: uppercase; }
    .s-cumple   { background:#d1fae5; color:#065f46; border:2px solid #6ee7b7; }
    .s-mejora   { background:#fef3c7; color:#92400e; border:2px solid #fcd34d; }
    .s-nocumple { background:#fee2e2; color:#991b1b; border:2px solid #fca5a5; }
    .s-noaplica { background:#f3f4f6; color:#374151; border:2px solid #d1d5db; }
    .s-pct-good { background:#065f46; color:#ffffff; border:2px solid #059669; }
    .s-pct-reg  { background:#92400e; color:#ffffff; border:2px solid #d97706; }
    .s-pct-bad  { background:#991b1b; color:#ffffff; border:2px solid #dc2626; }
    .s-pct-cls  { background:#7f1d1d; color:#ffffff; border:2px solid #b91c1c; }
    .item-cumple  {background:#f0fdf4;border-left:4px solid #34d399;border-radius:8px;padding:10px 14px;margin:5px 0;}
    .item-mejora  {background:#fffbeb;border-left:4px solid #fbbf24;border-radius:8px;padding:10px 14px;margin:5px 0;}
    .item-nocumple{background:#fff1f2;border-left:4px solid #f87171;border-radius:8px;padding:10px 14px;margin:5px 0;}
    .item-noaplica{background:#f9fafb;border-left:4px solid #d1d5db;border-radius:8px;padding:10px 14px;margin:5px 0;}
    .item-default {background:#ffffff;border-left:4px solid #e5e7eb;border-radius:8px;padding:10px 14px;margin:5px 0;}
    .score-good  {background:#d1fae5;color:#065f46;border:2px solid #6ee7b7;}
    .score-reg   {background:#fef3c7;color:#92400e;border:2px solid #fcd34d;}
    .score-bad   {background:#fee2e2;color:#991b1b;border:2px solid #fca5a5;}
    .score-close {background:#fca5a5;color:#7f1d1d;border:2px solid #f87171;}
    .score-card  {padding:16px;border-radius:12px;text-align:center;font-weight:700;font-size:22px;margin-top:12px;}
    footer{visibility:hidden;} #MainMenu{visibility:hidden;}
</style>
""", unsafe_allow_html=True)
SECTIONS = [
    ("Instalaciones y Estructura Edilicia", "🏗️", "sec-1", [
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
    ("Higiene y Limpieza", "🧹", "sec-2", [
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
    ("Personal Manipulador", "👨‍🍳", "sec-3", [
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
    ("Control de Temperaturas", "🌡️", "sec-4", [
        "Heladeras funcionando entre 0 y 5 grados C",
        "Freezers funcionando a -15 grados C o menos",
        "Registros de temperatura de equipos de frio actualizados",
        "Termometros calibrados disponibles",
        "Alimentos calientes mantenidos a mas de 65 grados C",
        "Sin alimentos que requieran frio a temperatura ambiente",
        "Descongelamiento correcto (en heladera o agua fria corriente)",
        "Control de temperatura al recibir mercaderia",
    ]),
    ("Almacenamiento y Conservacion", "📦", "sec-5", [
        "Alimentos almacenados en orden FIFO (primero entrado, primero salido)",
        "Separacion entre alimentos crudos y cocidos",
        "Alimentos separados del suelo y de paredes",
        "Envases en buen estado, sin roturas ni oxidacion",
        "Rotulado completo: nombre, fecha de elaboracion y vencimiento",
        "Sin alimentos vencidos o en mal estado",
        "Productos de limpieza almacenados separados de los alimentos",
        "Deposito seco, fresco, ventilado y protegido de plagas",
    ]),
    ("Agua y Saneamiento", "💧", "sec-6", [
        "Agua potable de red o con certificado de potabilidad",
        "Tanque de agua limpio y con tapa",
        "Ultimo analisis de agua disponible y vigente",
        "Instalaciones sanitarias (banos) en buen estado e higiene",
        "Banos con jabon, papel y medios de secado",
        "Banos con carteleria de lavado de manos",
        "Sistema de desague cloacal habilitado",
    ]),
    ("Documentacion y Habilitaciones", "📋", "sec-7", [
        "Habilitacion municipal vigente y visible",
        "RNPA / RPPA de los productos (si aplica)",
        "RNE / RPE del establecimiento (si aplica)",
        "Libreta sanitaria del personal al dia",
        "Manual de BPM disponible",
        "Plan HACCP implementado (si aplica por categoria)",
        "Registros de control de procesos disponibles",
        "Ultima auditoria/inspeccion archivada",
    ]),
    ("Gestion de Residuos", "♻️", "sec-8", [
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
        "checks":{}, "observations":{}, "photos":{},
        "establishment":"", "address":"", "auditor":"",
        "audit_date": date.today(),
        "audit_time": datetime.now().strftime("%H:%M"),
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def calc_score():
    vals = list(st.session_state.checks.values())
    c=vals.count("Cumple"); m=vals.count("Necesita Mejora")
    nc=vals.count("No Cumple"); na=vals.count("No Aplica")
    ev=c+m+nc
    pct=round((c/ev)*100) if ev>0 else 0
    return c,m,nc,na,ev,pct

def score_state(pct):
    if pct>=80: return "BUENO",        "score-good",  "s-pct-good"
    if pct>=60: return "REGULAR",      "score-reg",   "s-pct-reg"
    if pct>=40: return "INSUFICIENTE", "score-bad",   "s-pct-bad"
    return             "CLAUSURA",     "score-close", "s-pct-cls"
def generate_pdf():
    cumple,mejora,nocumple,noaplica,evaluados,pct = calc_score()
    estado_label,_,_ = score_state(pct)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_margins(14,14,14)
    pdf.set_fill_color(26,58,46)
    pdf.rect(0,0,210,42,"F")
    pdf.set_fill_color(76,175,125)
    pdf.rect(0,40,210,2,"F")
    pdf.set_xy(70,8)
    pdf.set_font("Helvetica","",7)
    pdf.set_text_color(167,243,197)
    pdf.cell(120,5,"SEGURIDAD ALIMENTARIA - BUENAS PRACTICAS DE MANUFACTURA",align="C")
    pdf.set_xy(70,15)
    pdf.set_font("Helvetica","B",16)
    pdf.set_text_color(255,255,255)
    pdf.cell(120,9,"INFORME DE VISITA BROMATOLOGICA",align="C")
    pdf.set_xy(70,26)
    pdf.set_font("Helvetica","I",8)
    pdf.set_text_color(203,213,225)
    pdf.cell(120,6,"Lic. C. Anabel Marin - Food Quality & Safety Consulting",align="C")
    pdf.set_xy(70,33)
    pdf.set_font("Helvetica","",7)
    pdf.set_text_color(167,243,197)
    pdf.cell(120,5,f"Fecha: {st.session_state.audit_date}   Hora: {st.session_state.audit_time}",align="C")
    y=48
    pdf.set_fill_color(240,253,244)
    pdf.set_draw_color(76,175,125)
    pdf.rect(14,y,182,30,"FD")
    info_items = [
        ("ESTABLECIMIENTO", st.session_state.establishment or "-", 18, y+9),
        ("AUDITOR/A",       st.session_state.auditor or "-",       18, y+20),
        ("DIRECCION",       st.session_state.address or "-",      105, y+9),
        ("FECHA Y HORA",    f"{st.session_state.audit_date}   {st.session_state.audit_time}", 105, y+20),
    ]
    for lbl,val,x,fy in info_items:
        pdf.set_xy(x,fy)
        pdf.set_font("Helvetica","B",7)
        pdf.set_text_color(107,114,128)
        pdf.cell(30,5,lbl+":")
        pdf.set_xy(x+30,fy)
        pdf.set_font("Helvetica","",9)
        pdf.set_text_color(26,58,46)
        pdf.cell(70,5,str(val)[:38])
    badge_colors = {"BUENO":(16,185,129),"REGULAR":(217,119,6),"INSUFICIENTE":(220,38,38),"CLAUSURA":(127,29,29)}
    bc = badge_colors.get(estado_label,(26,58,46))
    pdf.set_fill_color(*bc)
    pdf.rect(162,y+2,32,26,"F")
    pdf.set_xy(162,y+6)
    pdf.set_font("Helvetica","B",18)
    pdf.set_text_color(255,255,255)
    pdf.cell(32,10,f"{pct}%",align="C")
    pdf.set_xy(162,y+18)
    pdf.set_font("Helvetica","B",6)
    pdf.cell(32,5,estado_label,align="C")
    y2=y+36
    stats=[("Cumple",cumple,(16,185,129)),("Nec. Mejora",mejora,(217,119,6)),
           ("No Cumple",nocumple,(220,38,38)),("No Aplica",noaplica,(156,163,175)),
           ("Total Evaluados",evaluados,(26,58,46))]
    bw=182/5
    for i,(ls,vs,cs) in enumerate(stats):
        x=14+i*bw
        pdf.set_fill_color(*cs)
        pdf.rect(x,y2,bw-1,14,"F")
        pdf.set_xy(x,y2+1)
        pdf.set_font("Helvetica","B",13)
        pdf.set_text_color(255,255,255)
        pdf.cell(bw-1,6,str(vs),align="C")
        pdf.set_xy(x,y2+8)
        pdf.set_font("Helvetica","",5.5)
        pdf.cell(bw-1,4,ls,align="C")
    pdf.set_y(y2+20)
    for sec_name,icon,_,items in SECTIONS:
        if pdf.get_y()>240: pdf.add_page()
        pdf.set_fill_color(26,58,46)
        pdf.set_text_color(255,255,255)
        pdf.set_font("Helvetica","B",9)
        pdf.cell(182,8,f"{sec_name}",fill=True,ln=True)
        pdf.set_fill_color(240,253,244)
        pdf.set_text_color(26,58,46)
        pdf.set_font("Helvetica","B",7)
        pdf.cell(8,6,"#",border=1,fill=True,align="C")
        pdf.cell(84,6,"Item",border=1,fill=True)
        pdf.cell(26,6,"Estado",border=1,fill=True,align="C")
        pdf.cell(34,6,"Observacion",border=1,fill=True)
        pdf.cell(30,6,"Foto",border=1,fill=True,align="C")
        pdf.ln()
        for idx,item in enumerate(items):
            key=f"{sec_name}_{idx}"
            val=st.session_state.checks.get(key,"")
            obs=st.session_state.observations.get(key,"")
            photos=st.session_state.photos.get(key,[])
            if val=="Cumple":           pdf.set_fill_color(209,250,229);tc=(6,95,70)
            elif val=="Necesita Mejora":pdf.set_fill_color(254,243,199);tc=(146,64,14)
            elif val=="No Cumple":      pdf.set_fill_color(254,226,226);tc=(153,27,27)
            elif val=="No Aplica":      pdf.set_fill_color(243,244,246);tc=(107,114,128)
            else:                       pdf.set_fill_color(255,255,255);tc=(55,65,81)
            row_y=pdf.get_y()
            pdf.set_text_color(*tc)
            pdf.set_font("Helvetica","B",7)
            pdf.cell(8,8,str(idx+1),border=1,fill=True,align="C")
            pdf.set_font("Helvetica","",7)
            pdf.cell(84,8,item[:58],border=1,fill=True)
            pdf.set_font("Helvetica","B",6.5)
            pdf.cell(26,8,val or "Sin eval.",border=1,fill=True,align="C")
            pdf.set_font("Helvetica","",6)
            pdf.set_text_color(80,80,80)
            pdf.cell(34,8,obs[:28],border=1,fill=True)
            pdf.cell(30,8,"",border=1,fill=True)
            pdf.ln()
        pdf.ln(3)
    obs_items=[(k,v) for k,v in st.session_state.observations.items() if v.strip()]
    if obs_items:
        if pdf.get_y()>220: pdf.add_page()
        pdf.set_fill_color(26,58,46); pdf.set_text_color(255,255,255)
        pdf.set_font("Helvetica","B",9)
        pdf.cell(182,8,"OBSERVACIONES Y EVIDENCIA FOTOGRAFICA",fill=True,ln=True)
        pdf.ln(2)
        for key,obs in obs_items:
            if pdf.get_y()>240: pdf.add_page()
            parts=key.split("_"); sec="_".join(parts[:-1]); idx=int(parts[-1])
            sec_items=next((it for n,_,_,it in SECTIONS if n==sec),[])
            item_txt=sec_items[idx] if idx<len(sec_items) else ""
            photos=st.session_state.photos.get(key,[])
            pdf.set_fill_color(254,243,199); pdf.set_draw_color(217,119,6)
            pdf.set_text_color(146,64,14); pdf.set_font("Helvetica","B",7)
            pdf.cell(182,5,f"{sec} - Item {idx+1}: {item_txt}"[:90],border=1,fill=True,ln=True)
            pdf.set_text_color(55,65,81); pdf.set_font("Helvetica","",7)
            pdf.cell(182,5,obs[:100],border=1,fill=True,ln=True)
            if photos:
                px=14; py=pdf.get_y()+2
                for i,ph in enumerate(photos[:3]):
                    try:
                        img_data=base64.b64decode(ph)
                        with tempfile.NamedTemporaryFile(suffix=".jpg",delete=False) as tmp3:
                            tmp3.write(img_data);tmp3_path=tmp3.name
                        pdf.image(tmp3_path,x=px+i*62,y=py,w=58,h=44)
                        os.unlink(tmp3_path)
                    except: pass
                pdf.set_y(py+48)
            pdf.ln(2)
    if pdf.get_y()>240: pdf.add_page()
    pdf.ln(8)
    pdf.set_fill_color(249,250,251); pdf.set_draw_color(229,231,235)
    half=88
    pdf.rect(14,pdf.get_y(),half,30,"FD")
    pdf.rect(14+half+6,pdf.get_y(),half,30,"FD")
    sig_y=pdf.get_y()+26
    pdf.set_xy(14,sig_y); pdf.set_font("Helvetica","",7)
    pdf.set_text_color(107,114,128)
    pdf.cell(half,4,f"Firma Auditor/a: {st.session_state.auditor or ''}",align="C")
    pdf.set_xy(14+half+6,sig_y)
    pdf.cell(half,4,"Firma Responsable del Local",align="C")
    total_pages=pdf.page
    for pg in range(1,total_pages+1):
        pdf.page=pg
        pdf.set_y(-10); pdf.set_fill_color(26,58,46)
        pdf.rect(0,287,210,10,"F")
        pdf.set_xy(14,289); pdf.set_font("Helvetica","",6)
        pdf.set_text_color(167,243,197)
        est=st.session_state.establishment or "Establecimiento"
        pdf.cell(130,4,f"Informe Visita Bromatologica - {est} - {st.session_state.audit_date} {st.session_state.audit_time}")
        pdf.set_xy(150,289)
        pdf.cell(46,4,f"Pagina {pg} de {total_pages}",align="R")
    return bytes(pdf.output())
st.markdown("""
<div class="header-banner">
  <div class="header-sub">Food Quality & Safety Consulting</div>
  <h1 class="header-title">Informe de Visita Bromatologica</h1>
  <p class="header-desc">Lic. C. Anabel Marin — Lista de verificacion BPM</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### Datos del Establecimiento")
c1,c2=st.columns(2)
with c1:
    st.session_state.establishment=st.text_input("Establecimiento",st.session_state.establishment,placeholder="Nombre del local")
    st.session_state.address=st.text_input("Direccion",st.session_state.address,placeholder="Calle, numero, ciudad")
with c2:
    st.session_state.auditor=st.text_input("Auditor/a",st.session_state.auditor,placeholder="Nombre del auditor")
    dc1,dc2=st.columns(2)
    with dc1: st.session_state.audit_date=st.date_input("Fecha",st.session_state.audit_date)
    with dc2: st.session_state.audit_time=st.text_input("Hora",st.session_state.audit_time,placeholder="HH:MM")

st.divider()

total_items=sum(len(it) for _,_,_,it in SECTIONS)
answered=len([v for v in st.session_state.checks.values() if v])
st.markdown(f"**Progreso:** {answered} / {total_items} items respondidos")
st.progress(answered/total_items if total_items>0 else 0)

if answered>0:
    cumple,mejora,nocumple,noaplica,evaluados,pct=calc_score()
    estado_label,_,pct_cls=score_state(pct)
    st.markdown(f"""
    <div class="stat-row">
      <div class="stat-pill s-cumple"><div class="stat-num">{cumple}</div><div class="stat-lbl">Cumple</div></div>
      <div class="stat-pill s-mejora"><div class="stat-num">{mejora}</div><div class="stat-lbl">Nec. Mejora</div></div>
      <div class="stat-pill s-nocumple"><div class="stat-num">{nocumple}</div><div class="stat-lbl">No Cumple</div></div>
      <div class="stat-pill s-noaplica"><div class="stat-num">{noaplica}</div><div class="stat-lbl">No Aplica</div></div>
      <div class="stat-pill {pct_cls}"><div class="stat-num">{pct}%</div><div class="stat-lbl">{estado_label}</div></div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

st.divider()

for sec_idx,(sec_name,icon,sec_cls,items) in enumerate(SECTIONS):
    sec_checks=[st.session_state.checks.get(f"{sec_name}_{i}","") for i in range(len(items))]
    sec_ans=len([v for v in sec_checks if v])
    sec_c=sec_checks.count("Cumple")
    sec_ev=len([v for v in sec_checks if v and v!="No Aplica"])
    sec_pct=f"{round(sec_c/sec_ev*100)}%" if sec_ev>0 else ""
    with st.expander(f"{icon}  {sec_name}   {sec_ans}/{len(items)}  {sec_pct}", expanded=False):
        for idx,item in enumerate(items):
            key=f"{sec_name}_{idx}"
            cur=st.session_state.checks.get(key,"")
            css=STATUS_STYLE.get(cur,("item-default",""))[0] if cur else "item-default"
            icon2=STATUS_STYLE.get(cur,("",""))[1] if cur else "o"
            st.markdown(f'<div class="{css}"><strong>[{icon2}] {idx+1}.</strong> <span style="font-size:14px;font-weight:600;">{item}</span></div>',unsafe_allow_html=True)
            col_sel,col_obs=st.columns([1,2])
            with col_sel:
                opts=STATUS_OPTIONS
                sel_i=opts.index(cur) if cur in opts else 0
                nv=st.selectbox("Estado",opts,index=sel_i,key=f"sel_{key}",label_visibility="collapsed")
                if nv!="-- Seleccionar --": st.session_state.checks[key]=nv
                elif key in st.session_state.checks: del st.session_state.checks[key]
            with col_obs:
                if cur in ("Necesita Mejora","No Cumple"):
                    obs=st.text_area("Obs",value=st.session_state.observations.get(key,""),
                        placeholder="Observacion / accion correctiva...",
                        key=f"obs_{key}",height=60,label_visibility="collapsed")
                    st.session_state.observations[key]=obs
                    uploaded=st.file_uploader("Agregar foto(s)",type=["jpg","jpeg","png"],
                        accept_multiple_files=True,key=f"photo_{key}")
                    if uploaded:
                        photos_b64=[]
                        for uf in uploaded[:3]:
                            b64=base64.b64encode(uf.read()).decode()
                            photos_b64.append(b64)
                            st.image(uf,width=120)
                        st.session_state.photos[key]=photos_b64
        st.write("")

st.divider()

if answered>0:
    cumple,mejora,nocumple,noaplica,evaluados,pct=calc_score()
    estado_label,estado_cls,_=score_state(pct)
    with st.expander("Ver Resumen de la Visita",expanded=False):
        cols=st.columns([3,1,1,1,1,1])
        for col,h in zip(cols,["Seccion","Cumple","Nec. Mejora","No Cumple","No Aplica","% Cump."]):
            col.markdown(f"**{h}**")
        for sn,_,_,it in SECTIONS:
            vals=[st.session_state.checks.get(f"{sn}_{i}","") for i in range(len(it))]
            sc=vals.count("Cumple");nm=vals.count("Necesita Mejora")
            nc=vals.count("No Cumple");na=vals.count("No Aplica")
            ev=sc+nm+nc;p=f"{round(sc/ev*100)}%" if ev>0 else "-"
            cols=st.columns([3,1,1,1,1,1])
            cols[0].write(sn);cols[1].write(f"OK {sc}");cols[2].write(f"!! {nm}")
            cols[3].write(f"X {nc}");cols[4].write(f"- {na}");cols[5].write(p)
        st.markdown(f'<div class="score-card {estado_cls}">{pct}%  —  {estado_label}</div>',unsafe_allow_html=True)

st.markdown("### Generar Informe PDF")
col_pdf,col_reset=st.columns([3,1])
with col_pdf:
    if st.button("Generar PDF para el Responsable del Local",use_container_width=True,type="primary"):
        with st.spinner("Generando PDF..."):
            pdf_bytes=generate_pdf()
        fname=f"Visita_{(st.session_state.establishment or 'local').replace(' ','_')}_{st.session_state.audit_date}.pdf"
        st.download_button(label="Descargar PDF",data=pdf_bytes,file_name=fname,mime="application/pdf",use_container_width=True)
with col_reset:
    if st.button("Nueva Visita",use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

st.markdown("---")
st.markdown("<p style='text-align:center;color:#9ca3af;font-size:10px;'>Lic. C. Anabel Marin - Food Quality & Safety Consulting | Codigo Alimentario Argentino (CAA)</p>",unsafe_allow_html=True)
