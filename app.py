"""
ExpoInsight V4 — Ultimate Occupational Health Dashboard
========================================================
Dark mode default, facility heatmap, manual simulation input,
donut emoji fix, all 11 enhancements.
Run: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os, math

st.set_page_config(page_title="ExpoInsight V4",page_icon="🛡️",layout="wide",initial_sidebar_state="collapsed")

# ═══════════════ DARK MODE ALWAYS ON ═══════════════
dm = True
C = {
    "bg":"#1A1A2E","bg2":"#16213E","card":"#1E293B",
    "card_border":"rgba(255,255,255,0.06)",
    "text1":"#F1F5F9","text2":"#94A3B8","text3":"#64748B",
    "table_bg":"#0F172A","table_hover":"#1E293B","table_border":"#334155",
    "grid":"#334155","safe":"#2E7D32","warn":"#F57F17","crit":"#C62828",
    "safe_bg":"#1B5E20","warn_bg":"#4E3A00","crit_bg":"#4A0E0E",
    "safe_txt":"#81C784","warn_txt":"#FFD54F","crit_txt":"#EF9A9A",
    "accent":"#4FC3F7","shadow":"rgba(0,0,0,0.3)",
}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
#MainMenu,header,footer,.stDeployButton,div[data-testid="stToolbar"],div[data-testid="stDecoration"]{{display:none!important;visibility:hidden!important}}
html,body,.stApp{{font-family:'Inter',-apple-system,sans-serif!important;background:linear-gradient(160deg,{C["bg"]},{C["bg2"]})!important;color:#E0E0E0!important}}
.main .block-container{{padding-top:0;padding-bottom:1rem;max-width:100%}}
.stApp p,.stApp label,.stMarkdown p,.stMarkdown span,
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] strong{{font-family:'Inter',sans-serif!important;color:#E0E0E0!important}}
[data-testid="stMarkdownContainer"] div{{font-family:'Inter',sans-serif!important}}

div[data-testid="stRadio"]>label{{display:none!important}}
div[data-testid="stRadio"]>div>label>div:first-child{{display:none!important}}
div[data-testid="stRadio"]>div{{gap:0!important}}
div[data-testid="stRadio"]>div>label{{background:transparent!important;padding:0!important;margin:0!important;min-height:0!important}}
div[data-testid="stRadio"]>div>label>div:last-child{{display:none!important}}

@keyframes fadeUp{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes pulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.03)}}}}
@keyframes glow{{0%,100%{{box-shadow:0 0 5px rgba(76,175,80,0.3)}}50%{{box-shadow:0 0 18px rgba(76,175,80,0.6)}}}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:0.4}}}}

.nav-bar{{background:linear-gradient(135deg,#0B3558,#0F4C75 60%,#1565C0);margin:-1rem -3rem 1.5rem;padding:0;display:flex;align-items:center;border-radius:0 0 20px 20px;box-shadow:0 8px 32px rgba(11,53,88,0.35);z-index:999;overflow:hidden;position:relative}}
.nav-bar::before{{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle at 30% 50%,rgba(79,195,247,0.08),transparent 50%)}}
.nav-logo{{display:flex;align-items:center;padding:16px 32px;gap:14px;position:relative}}
.nav-logo-icon{{width:46px;height:46px;background:linear-gradient(135deg,#4FC3F7,#0288D1);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:22px;box-shadow:0 4px 16px rgba(79,195,247,0.35)}}
.nav-logo-text{{color:#FFF;font-size:22px;font-weight:900;letter-spacing:2.5px}}
.nav-logo-sub{{color:rgba(255,255,255,0.55);font-size:11px;letter-spacing:1.2px}}
.nav-right{{margin-left:auto;padding:16px 32px;display:flex;align-items:center;gap:10px}}
.live-dot{{width:9px;height:9px;background:#4CAF50;border-radius:50%;animation:glow 2s infinite}}
.live-txt{{color:rgba(255,255,255,0.65);font-size:11px;font-weight:600;letter-spacing:1px}}

.stTabs [data-baseweb="tab-list"]{{background:linear-gradient(135deg,#0B3558,#0F4C75);border-radius:14px;padding:5px;gap:0;box-shadow:0 4px 16px rgba(11,53,88,0.2)}}
.stTabs [data-baseweb="tab"]{{color:rgba(255,255,255,0.65)!important;font-weight:700!important;font-size:12px!important;letter-spacing:1px!important;text-transform:uppercase!important;border-radius:10px!important;padding:11px 18px!important;background:transparent!important;border:none!important}}
.stTabs [data-baseweb="tab"]:hover{{color:#FFF!important;background:rgba(255,255,255,0.08)!important}}
.stTabs [aria-selected="true"]{{color:#FFF!important;background:rgba(255,255,255,0.13)!important;border-bottom:3px solid #4FC3F7!important}}
.stTabs [data-baseweb="tab-highlight"]{{background:#4FC3F7!important}}
.stTabs [data-baseweb="tab-border"]{{display:none}}
.stTabs [data-baseweb="tab-panel"]{{padding-top:1.5rem}}

.kpi-card{{background:{C["card"]};border-radius:20px;padding:22px 18px;box-shadow:0 4px 20px {C["shadow"]};border:1px solid {C["card_border"]};text-align:center;overflow:hidden;transition:all .3s;position:relative;animation:fadeUp .5s ease-out}}
.kpi-card:hover{{transform:translateY(-4px);box-shadow:0 8px 30px {C["shadow"]}}}
.kpi-card::after{{content:'';position:absolute;top:0;left:0;right:0;height:4px;border-radius:20px 20px 0 0}}
.kpi-card.safe::after{{background:linear-gradient(90deg,#2E7D32,#66BB6A)}}
.kpi-card.warning::after{{background:linear-gradient(90deg,#F57F17,#FFB300)}}
.kpi-card.critical::after{{background:linear-gradient(90deg,#C62828,#EF5350)}}
.kpi-icon{{font-size:30px;margin-bottom:6px}}
.kpi-label{{font-size:11px;color:{C["text3"]};font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px}}
.kpi-value{{font-size:34px;font-weight:900;color:{C["text1"]};line-height:1.1}}
.kpi-unit{{font-size:14px;color:{C["text3"]};font-weight:500}}
.kpi-exposure{{font-size:13px;font-weight:700;margin-top:6px}}
.kpi-status{{display:inline-block;padding:4px 14px;border-radius:20px;font-size:11px;font-weight:800;letter-spacing:.7px;margin-top:6px;text-transform:uppercase}}
.status-safe{{background:{C["safe_bg"]};color:{C["safe_txt"]}}}
.status-warning{{background:{C["warn_bg"]};color:{C["warn_txt"]}}}
.status-critical{{background:{C["crit_bg"]};color:{C["crit_txt"]};animation:pulse 2s infinite}}

.sparkline-row{{display:flex;justify-content:center;gap:2px;margin-top:8px;align-items:flex-end;height:24px}}
.spark-bar{{width:4px;border-radius:2px}}
.exp-bar-container{{width:100%;height:8px;background:#334155;border-radius:10px;overflow:hidden;margin-top:4px}}
.exp-bar-fill{{height:100%;border-radius:10px;transition:width 1s ease-out}}

.panel{{background:{C["card"]};border-radius:20px;padding:24px;box-shadow:0 4px 20px {C["shadow"]};border:1px solid {C["card_border"]};margin-bottom:16px;animation:fadeUp .5s ease-out}}
.panel-title{{font-size:16px;font-weight:800;color:{C["text1"]};margin-bottom:18px;display:flex;align-items:center;gap:10px}}

.mini-kpi{{background:{C["card"]};border-radius:16px;padding:16px 20px;box-shadow:0 3px 14px {C["shadow"]};display:flex;align-items:center;gap:14px;animation:fadeUp .6s ease-out}}
.mini-kpi-icon{{font-size:22px;width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center;flex-shrink:0}}
.mini-kpi-label{{font-size:11px;color:{C["text3"]};font-weight:700;text-transform:uppercase;letter-spacing:.6px}}
.mini-kpi-value{{font-size:22px;font-weight:900;color:{C["text1"]}}}

.zone-card{{padding:14px 18px;border-radius:14px;margin-bottom:8px;display:flex;align-items:center;gap:12px;border:2px solid #334155;background:{C["card"]};transition:all .25s}}
.zone-card:hover{{border-color:#0F4C75}}
.zone-card.active{{background:#1E3A5F;border-color:#0F4C75;box-shadow:0 3px 12px rgba(15,76,117,0.15)}}
.zone-dot{{width:12px;height:12px;border-radius:50%;flex-shrink:0;box-shadow:0 0 0 3px rgba(0,0,0,0.06)}}
.zone-card-name{{font-size:14px;font-weight:700;color:{C["text1"]}}}
.zone-card-sub{{font-size:11px;color:{C["text3"]};font-weight:500}}

.status-banner{{padding:16px 28px;border-radius:16px;font-size:17px;font-weight:800;text-align:center;letter-spacing:1.5px;text-transform:uppercase;color:#FFF;animation:fadeUp .4s ease-out;box-shadow:0 4px 16px rgba(0,0,0,0.15)}}
.banner-safe{{background:linear-gradient(135deg,#2E7D32,#43A047)}}
.banner-warning{{background:linear-gradient(135deg,#F57F17,#F9A825)}}
.banner-critical{{background:linear-gradient(135deg,#C62828,#E53935);animation:pulse 2.5s infinite}}

.styled-table{{width:100%;border-collapse:separate;border-spacing:0;font-size:13px;overflow:hidden;border-radius:14px}}
.styled-table th{{background:linear-gradient(135deg,#0B3558,#0F4C75);color:#FFF;padding:12px 16px;text-align:left;font-weight:700;font-size:11px;text-transform:uppercase;letter-spacing:.8px}}
.styled-table td{{padding:11px 16px;border-bottom:1px solid {C["table_border"]};color:{C["text2"]}!important;font-weight:500;background:{C["table_bg"]}}}
.styled-table tr:hover td{{background:{C["table_hover"]}}}
.styled-table tr:last-child td{{border-bottom:none}}

.worker-card{{background:{C["card"]};border-radius:16px;padding:18px;box-shadow:0 3px 14px {C["shadow"]};border-left:5px solid #0F4C75;margin-bottom:10px;animation:fadeUp .5s ease-out}}
.worker-card-name{{font-size:15px;font-weight:800;color:{C["text1"]};margin-bottom:4px}}
.worker-card-sub{{font-size:12px;color:{C["text2"]};font-weight:500}}
.worker-card-hours{{font-size:14px;color:#4FC3F7;font-weight:700;margin-top:4px}}

.alert-bar{{background:linear-gradient(135deg,#C62828,#D32F2F);color:#FFF;padding:10px 20px;border-radius:12px;display:flex;align-items:center;gap:10px;margin-bottom:16px;font-size:13px;font-weight:600;animation:fadeUp .4s ease-out}}
.alert-blink{{animation:blink 1.5s infinite}}
.alert-item{{background:{C["card"]};border-radius:12px;padding:14px 18px;margin-bottom:8px;display:flex;align-items:center;gap:14px;border-left:4px solid #C62828;box-shadow:0 2px 8px {C["shadow"]}}}
.alert-item.warn-item{{border-left-color:#F57F17}}

.sim-input-card{{background:#0F172A;border:2px solid #334155;border-radius:16px;padding:20px;margin-bottom:12px}}
.sim-input-title{{color:#4FC3F7;font-size:14px;font-weight:700;margin-bottom:12px}}

div[data-baseweb="select"]>div{{border-radius:12px!important;border-color:#334155!important;background:{C["card"]}!important}}
div[data-baseweb="input"]>div{{background:{C["card"]}!important;border-color:#334155!important;border-radius:10px!important}}
.stNumberInput>div>div>input{{background:{C["card"]}!important;color:{C["text1"]}!important}}

/* ═══ MOBILE RESPONSIVE ═══ */
@media (max-width: 768px) {{
    .main .block-container{{padding-left:0.5rem!important;padding-right:0.5rem!important;max-width:100%!important}}
    .nav-bar{{flex-direction:column;margin:-1rem -0.5rem 1rem;border-radius:0 0 14px 14px;padding:8px!important}}
    .nav-logo{{padding:10px 16px!important}}
    .nav-logo-text{{font-size:16px!important}}
    .nav-right{{padding:4px 16px 8px!important}}
    .kpi-card{{padding:14px 10px!important;border-radius:14px!important}}
    .kpi-value{{font-size:22px!important}}
    .kpi-icon{{font-size:22px!important}}
    .kpi-label{{font-size:9px!important}}
    .panel{{padding:14px!important;border-radius:14px!important;margin-bottom:10px!important}}
    .panel-title{{font-size:14px!important;margin-bottom:12px!important}}
    .styled-table th,.styled-table td{{padding:8px 10px!important;font-size:11px!important}}
    .mini-kpi{{padding:10px 12px!important}}
    .mini-kpi-value{{font-size:18px!important}}
    .alert-item{{padding:10px 12px!important;flex-wrap:wrap!important}}
    .stTabs [data-baseweb="tab-list"]{{border-radius:10px!important;padding:3px!important;flex-wrap:wrap!important}}
    .stTabs [data-baseweb="tab"]{{font-size:9px!important;padding:8px 10px!important;letter-spacing:0!important}}
    .sim-input-card{{padding:12px!important}}
    .zone-card{{padding:10px 12px!important}}
    .alert-bar{{padding:8px 12px!important;font-size:11px!important}}
    div[data-testid="column"]{{padding:0 2px!important}}
}}
@media (max-width: 480px) {{
    .nav-logo-icon{{width:32px!important;height:32px!important;font-size:16px!important;border-radius:10px!important}}
    .nav-logo-text{{font-size:14px!important;letter-spacing:1px!important}}
    .kpi-value{{font-size:18px!important}}
    .kpi-card{{padding:10px 8px!important}}
    .panel-title{{font-size:13px!important}}
    .stTabs [data-baseweb="tab"]{{font-size:8px!important;padding:6px 6px!important}}
}}
</style>
""", unsafe_allow_html=True)

# Auto-refresh
st.markdown('<script>setTimeout(function(){window.location.reload()},30000);</script>',unsafe_allow_html=True)

# ═══════════════ DATA ═══════════════
@st.cache_data
def load_data():
    fp=next((f for f in ["ExpoInsight-v_1.xlsx",os.path.join(os.path.dirname(os.path.abspath(__file__)),"ExpoInsight-v_1.xlsx")] if os.path.exists(f)),None)
    if not fp: st.error("Excel file not found."); st.stop()
    z=pd.read_excel(fp,sheet_name="Zones",header=2).dropna(subset=["ZoneID"])
    w=pd.read_excel(fp,sheet_name="Workers",header=2).dropna(subset=["WorkerID"])
    p=pd.read_excel(fp,sheet_name="PresenceLog",header=2).dropna(subset=["PresenceID"])
    r=pd.read_excel(fp,sheet_name="EnvironmentalReadings",header=2).dropna(subset=["ReadingID","MeasuredValue"])
    l=pd.read_excel(fp,sheet_name="ExposureLimits",header=2).dropna(subset=["HazardType"])
    ah=pd.read_excel(fp,sheet_name="AllowedExposureHours",header=2)
    s=pd.read_excel(fp,sheet_name="Simulation",header=2).dropna(subset=["ScenarioName"])
    try:
        wh=pd.read_excel(fp,sheet_name="WorkerHealth",header=2).dropna(subset=["WorkerID"])
    except:
        wh=pd.DataFrame()
    for c in r.columns:
        if "datetime" in c.lower() or "timestamp" in c.lower():
            if c!="ReadingDateTime": r=r.rename(columns={c:"ReadingDateTime"})
    r["ReadingDateTime"]=pd.to_datetime(r["ReadingDateTime"],errors="coerce")
    for c in p.columns:
        if "entry" in c.lower() and "date" in c.lower():
            if c!="EntryDateTime": p=p.rename(columns={c:"EntryDateTime"})
        if "exit" in c.lower() and "date" in c.lower():
            if c!="ExitDateTime": p=p.rename(columns={c:"ExitDateTime"})
    p["EntryDateTime"]=pd.to_datetime(p["EntryDateTime"],errors="coerce")
    p["ExitDateTime"]=pd.to_datetime(p["ExitDateTime"],errors="coerce")
    return z,w,p,r,l,ah,s,wh
zones_df,workers_df,presence_df,readings_df,limits_df,allowed_hours_df,simulation_df,health_df=load_data()

# ═══════════════ HELPERS ═══════════════
def get_ld(): return dict(zip(limits_df["HazardType"],limits_df["LimitValue"]))
def get_ud(): return dict(zip(limits_df["HazardType"],limits_df["Unit"]))
HI={"CO2":"💨","HeatIndex":"🌡️","Noise":"🔊","Gas":"⚗️"}
HD={"CO2":"CO₂","HeatIndex":"Heat","Noise":"Noise","Gas":"Gas"}
HO=["CO2","HeatIndex","Noise","Gas"]
HC={"CO2":"#1565C0","HeatIndex":"#E65100","Noise":"#6A1B9A","Gas":"#2E7D32"}
PL=dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(family="Inter,sans-serif",color=C["text2"],size=12),margin=dict(l=50,r=20,t=40,b=50))

def cexp(v,l): return v/l if l else 0
def gstat(e):
    if e<0.8: return "Safe"
    if e<1.0: return "Warning"
    return "Critical"
def scolor(s): return {"Safe":C["safe"],"Warning":C["warn"],"Critical":C["crit"]}.get(s,"#999")
def sbg(s): return {"Safe":C["safe_bg"],"Warning":C["warn_bg"],"Critical":C["crit_bg"]}.get(s,"#333")
def stxt(s): return {"Safe":C["safe_txt"],"Warning":C["warn_txt"],"Critical":C["crit_txt"]}.get(s,"#999")
def sicon(s): return {"Safe":"✅","Warning":"⚠️","Critical":"🚨"}.get(s,"❓")
def scss(s): return s.lower()
def zname(zid):
    r=zones_df[zones_df["ZoneID"]==zid]
    return r.iloc[0]["ZoneName"] if len(r)>0 else zid
def zhstats(zone_id=None):
    ld=get_ld();ud=get_ud()
    df=readings_df[readings_df["ZoneID"]==zone_id] if zone_id else readings_df
    res=[]
    for h in HO:
        hdf=df[df["HazardType"]==h]
        c=hdf["MeasuredValue"].mean() if len(hdf)>0 else 0
        if pd.isna(c): c=0
        l=ld.get(h,1) if isinstance(ld,dict) else 1
        u=ud.get(h,"") if isinstance(ud,dict) else ""
        e=cexp(c,l)
        res.append({"HazardType":h,"DisplayName":HD.get(h,h),"Icon":HI.get(h,"📊"),"CurrentValue":round(c,1),"Limit":l,"Unit":u,"ExposurePct":e,"Status":gstat(e)})
    return res
def get_sparkline(zone_id,hazard,n=8):
    df=readings_df[readings_df["HazardType"]==hazard]
    if zone_id: df=df[df["ZoneID"]==zone_id]
    return df.sort_values("ReadingDateTime").tail(n)["MeasuredValue"].tolist()
def zoverall(zid):
    ss=[s["Status"] for s in zhstats(zid)]
    if "Critical" in ss: return "Critical"
    if "Warning" in ss: return "Warning"
    return "Safe"
def w_risk():
    cz=[z["ZoneID"] for _,z in zones_df.iterrows() if zoverall(z["ZoneID"])=="Critical"]
    return presence_df[presence_df["ZoneID"].isin(cz)]["WorkerID"].nunique() if cz else 0
def sz_count(): return sum(1 for _,z in zones_df.iterrows() if zoverall(z["ZoneID"])=="Safe")
def last_upd(): return readings_df["ReadingDateTime"].max()
def spark_html(vals,color="#4FC3F7"):
    if not vals: return ""
    mx=max(vals) if max(vals)>0 else 1
    bars="".join(f'<div class="spark-bar" style="height:{max(4,int(v/mx*22))}px;background:{color};opacity:0.7"></div>' for v in vals)
    return f'<div class="sparkline-row">{bars}</div>'
def pbar(pct,status):
    return f'<div class="exp-bar-container"><div class="exp-bar-fill" style="width:{min(pct*100,100)}%;background:{scolor(status)}"></div></div>'
def gauge_svg(pct,status,sz=76):
    a=min(pct,1.3)/1.3*270; r=sz/2-6; cx=cy=sz/2
    sa=135; ea=sa+a; clr=scolor(status)
    def p2c(cx,cy,r,ad): ar=math.radians(ad); return cx+r*math.cos(ar),cy+r*math.sin(ar)
    sx,sy=p2c(cx,cy,r,sa); ex,ey=p2c(cx,cy,r,ea)
    bsx,bsy=p2c(cx,cy,r,sa); bex,bey=p2c(cx,cy,r,sa+270)
    lg=1 if a>180 else 0
    return f'<svg width="{sz}" height="{sz}" viewBox="0 0 {sz} {sz}" style="margin:0 auto;display:block"><path d="M {bsx} {bsy} A {r} {r} 0 1 1 {bex} {bey}" fill="none" stroke="#334155" stroke-width="7" stroke-linecap="round"/><path d="M {sx} {sy} A {r} {r} 0 {lg} 1 {ex} {ey}" fill="none" stroke="{clr}" stroke-width="7" stroke-linecap="round"/><text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="14" font-weight="800" fill="{clr}">{pct:.0%}</text></svg>'

def rkpi(icon,label,value,unit,ep,status,zid=None,hazard=None):
    g=gauge_svg(ep,status)
    sp=spark_html(get_sparkline(zid,hazard),scolor(status)) if hazard else ""
    return f'<div class="kpi-card {scss(status)}"><div class="kpi-icon">{icon}</div><div class="kpi-label">{label}</div>{g}<div class="kpi-value">{value} <span class="kpi-unit">{unit}</span></div><div class="kpi-status status-{scss(status)}">{sicon(status)} {status}</div>{sp}</div>'

def rkpi_s(icon,label,value,unit,ep,status):
    return f'<div class="kpi-card {scss(status)}"><div class="kpi-icon">{icon}</div><div class="kpi-label">{label}</div><div class="kpi-value">{value} <span class="kpi-unit">{unit}</span></div><div class="kpi-exposure" style="color:{stxt(status)}">Exposure: {ep:.0%}</div><div class="kpi-status status-{scss(status)}">{sicon(status)} {status}</div></div>'

def rmkpi(icon,label,value,bg=None):
    bg=bg or C["safe_bg"]
    return f'<div class="mini-kpi"><div class="mini-kpi-icon" style="background:{bg}">{icon}</div><div><div class="mini-kpi-label">{label}</div><div class="mini-kpi-value">{value}</div></div></div>'

def gen_alerts():
    ld=get_ld(); alerts=[]
    for _,r in readings_df.iterrows():
        lim=ld.get(r["HazardType"],1e9); exp=r["MeasuredValue"]/lim if lim else 0
        if exp>=0.8:
            alerts.append({"DateTime":r["ReadingDateTime"],"ZoneID":r["ZoneID"],"Zone":zname(r["ZoneID"]),"Hazard":r["HazardType"],"Value":round(r["MeasuredValue"],1),"Limit":lim,"ExposurePct":exp,"Status":gstat(exp),"Unit":r.get("Unit","")})
    return pd.DataFrame(alerts).sort_values("DateTime",ascending=False) if alerts else pd.DataFrame()

# ═══════════════ FACILITY HEATMAP FUNCTION ═══════════════
def render_facility_map():
    """Interactive facility floor plan with thermal heatmap overlay"""
    # Zone positions on facility layout (x, y, width, height)
    zone_layout = {
        "Z001": {"name":"Generator Area","x":1,"y":5,"w":3.5,"h":3,"type":"Production"},
        "Z002": {"name":"Fuel Unloading","x":5.5,"y":5,"w":3.5,"h":3,"type":"Logistics"},
        "Z003": {"name":"Control Room","x":10,"y":5.5,"w":3,"h":2.5,"type":"Office"},
        "Z004": {"name":"Workshop","x":1,"y":1,"w":3.5,"h":3,"type":"Maintenance"},
        "Z005": {"name":"Storage Area","x":5.5,"y":1,"w":3.5,"h":3,"type":"Warehouse"},
        "Z006": {"name":"Laboratory","x":10,"y":1,"w":3,"h":3,"type":"Testing"},
    }
    fig = go.Figure()

    # Background - facility outline
    fig.add_shape(type="rect",x0=-0.5,y0=-0.5,x1=14.5,y1=9.5,fillcolor="rgba(15,23,42,0.3)",line=dict(color="#334155",width=2,dash="dot"))

    # Roads / paths between zones
    fig.add_shape(type="line",x0=4.75,y0=0,x1=4.75,y1=9,line=dict(color="#475569",width=1,dash="dash"))
    fig.add_shape(type="line",x0=9.25,y0=0,x1=9.25,y1=9,line=dict(color="#475569",width=1,dash="dash"))
    fig.add_shape(type="line",x0=0,y0=4.5,x1=14,y1=4.5,line=dict(color="#475569",width=1,dash="dash"))

    for zid, zl in zone_layout.items():
        stats = zhstats(zid)
        max_exp = max(s["ExposurePct"] for s in stats)
        status = gstat(max_exp)
        clr = scolor(status)

        # Zone rectangle with color intensity based on exposure
        opacity = min(0.15 + max_exp * 0.35, 0.6)
        fig.add_shape(type="rect", x0=zl["x"], y0=zl["y"], x1=zl["x"]+zl["w"], y1=zl["y"]+zl["h"],
            fillcolor=f"rgba({int(clr[1:3],16)},{int(clr[3:5],16)},{int(clr[5:7],16)},{opacity})",
            line=dict(color=clr, width=2.5), layer="below")

        # Zone label
        cx = zl["x"] + zl["w"]/2
        cy = zl["y"] + zl["h"]/2
        fig.add_trace(go.Scatter(x=[cx], y=[cy+0.5], mode="text",
            text=[f"<b>{zl['name']}</b>"], textfont=dict(size=11, color="#F1F5F9"),
            showlegend=False, hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=[cx], y=[cy-0.1], mode="text",
            text=[f"{max_exp:.0%}"], textfont=dict(size=18, color=clr, family="Inter"),
            showlegend=False, hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=[cx], y=[cy-0.8], mode="text",
            text=[f"{sicon(status)} {status}"], textfont=dict(size=10, color=stxt(status)),
            showlegend=False, hoverinfo="skip"))

        # Hazard mini-dots inside zone
        dots_x = [zl["x"]+0.6, zl["x"]+zl["w"]-0.6, zl["x"]+0.6, zl["x"]+zl["w"]-0.6]
        dots_y = [zl["y"]+zl["h"]-0.4, zl["y"]+zl["h"]-0.4, zl["y"]+0.4, zl["y"]+0.4]
        for i, s in enumerate(stats):
            if i < len(dots_x):
                fig.add_trace(go.Scatter(x=[dots_x[i]], y=[dots_y[i]], mode="markers",
                    marker=dict(size=10, color=scolor(s["Status"]), symbol="circle",
                        line=dict(color="#0F172A",width=1.5)),
                    showlegend=False,
                    hovertemplate=f"<b>{zl['name']}</b><br>{s['Icon']} {s['DisplayName']}: {s['CurrentValue']} {s['Unit']}<br>Exposure: {s['ExposurePct']:.0%}<br>Status: {s['Status']}<extra></extra>"))

    # Title
    fig.add_annotation(x=7, y=9.8, text="<b>🏭 FACILITY FLOOR PLAN — THERMAL HAZARD MAP</b>",
        showarrow=False, font=dict(size=14, color=C["text1"]))
    # Legend
    for i, (lbl, clr) in enumerate([("Safe","#2E7D32"),("Warning","#F57F17"),("Critical","#C62828")]):
        fig.add_trace(go.Scatter(x=[11+i*1.3], y=[-0.8], mode="markers+text",
            marker=dict(size=12, color=clr, symbol="square"),
            text=[f" {lbl}"], textposition="middle right", textfont=dict(size=10, color=C["text2"]),
            showlegend=False, hoverinfo="skip"))

    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter,sans-serif", color=C["text2"], size=12),
        height=480, margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(visible=False, range=[-1, 15]),
        yaxis=dict(visible=False, range=[-1.5, 10.5]))
    return fig

# ═══════════════ NAV BAR ═══════════════
now = datetime.now()
time_str = now.strftime("%H:%M:%S")
date_str = now.strftime("%A, %d %B %Y")
# Riyadh weather estimate based on season
month = now.month
if month in [6,7,8]: wx_icon="☀️"; wx_txt="Hot & Sunny · ~45°C"
elif month in [12,1,2]: wx_icon="🌤️"; wx_txt="Mild · ~20°C"
elif month in [3,4,5]: wx_icon="⛅"; wx_txt="Warm · ~32°C"
else: wx_icon="🌤️"; wx_txt="Warm · ~35°C"

st.markdown(f'''
<div class="nav-bar">
    <div class="nav-logo"><div class="nav-logo-icon">🛡️</div>
        <div>
            <div class="nav-logo-text">EXPOINSIGHT</div>
            <div class="nav-logo-sub">Occupational Exposure Monitoring</div>
        </div>
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;padding:8px 20px;border-left:1px solid rgba(255,255,255,0.1);border-right:1px solid rgba(255,255,255,0.1);margin:0 10px">
        <div style="color:#4FC3F7;font-size:15px;font-weight:900;letter-spacing:1px">Power Plant 0</div>
        <div style="color:rgba(255,255,255,0.5);font-size:11px;font-weight:500">📍 Saudi Arabia — Riyadh</div>
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;padding:8px 16px">
        <div style="color:rgba(255,255,255,0.8);font-size:13px;font-weight:600">{wx_icon} {wx_txt}</div>
        <div style="color:rgba(255,255,255,0.4);font-size:11px">🕐 {datetime.now().strftime("%H:%M:%S")} (Riyadh) &nbsp;·&nbsp; {datetime.now().strftime("%A, %d %B %Y")}</div>
    </div>
    <div class="nav-right"><div class="live-dot"></div><span class="live-txt">LIVE MONITORING</span></div>
</div>''', unsafe_allow_html=True)

crit_z_names=[z["ZoneName"] for _,z in zones_df.iterrows() if zoverall(z["ZoneID"])=="Critical"]
if crit_z_names:
    st.markdown(f'<div class="alert-bar"><span class="alert-blink">🚨</span><span>CRITICAL ALERT — Limits exceeded in: <strong>{", ".join(crit_z_names)}</strong></span></div>',unsafe_allow_html=True)

# Global language toggle
lc1, lc2 = st.columns([10,2])
with lc1:
    st.markdown(f'<div style="color:{C["text3"]};font-size:12px;margin-bottom:4px">🔄 Auto-refresh: 30s &nbsp;|&nbsp; 📡 {datetime.now().strftime("%H:%M:%S")}</div>',unsafe_allow_html=True)
with lc2:
    LANG = st.selectbox("🌐", ["English", "العربية"], key="global_lang", label_visibility="collapsed")
AR = LANG == "العربية"

if AR:
    tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab9,tab_ask=st.tabs(["🏠 الرئيسية","📊 نظرة عامة","🏭 المناطق","🔬 المحاكاة","👷 العمال","🚨 التنبيهات","🎯 التنفيذي","🌡️ الإجهاد الحراري","🤖 اسألني"])
else:
    tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab9,tab_ask=st.tabs(["🏠 HOME","📊 OVERVIEW","🏭 ZONES","🔬 SIMULATION","👷 WORKERS","🚨 ALERTS","🎯 EXECUTIVE","🌡️ HEAT STRESS","🤖 ASK ME"])

# ═══════════════ TAB 1: HOME ═══════════════
with tab1:
    zo=["All Zones"]+[f"{r['ZoneID']} - {r['ZoneName']}" for _,r in zones_df.iterrows()]
    sel=st.selectbox("🏭 اختر المنطقة" if AR else "🏭 Select Zone",zo,key="hz")
    szid=None if sel=="All Zones" else sel.split(" - ")[0]
    stats=zhstats(szid)
    cols=st.columns(4)
    for i,s in enumerate(stats):
        with cols[i]: st.markdown(rkpi(s["Icon"],s["DisplayName"],s["CurrentValue"],s["Unit"],s["ExposurePct"],s["Status"],szid,s["HazardType"]),unsafe_allow_html=True)
    st.markdown("<div style='height:20px'></div>",unsafe_allow_html=True)

    c1,c2,c3=st.columns([3,4,3])
    with c1:
        st.markdown(f'<div class="panel"><div class="panel-title">{"📋 مستويات التعرض الحالية" if AR else "📋 Current Exposure Levels"}</div>',unsafe_allow_html=True)
        h='<table class="styled-table"><tr><th>Hazard</th><th>Current</th><th>Limit</th><th>Exposure</th><th>Status</th></tr>'
        for s in stats:
            pb=pbar(s["ExposurePct"],s["Status"])
            h+=f'<tr><td style="color:{C["text1"]}!important;font-weight:700">{s["Icon"]} {s["DisplayName"]}</td><td style="color:{C["text2"]}!important">{s["CurrentValue"]} {s["Unit"]}</td><td style="color:{C["text2"]}!important">{s["Limit"]} {s["Unit"]}</td><td style="color:{stxt(s["Status"])}!important;font-weight:800">{s["ExposurePct"]:.0%}{pb}</td><td><span class="kpi-status status-{scss(s["Status"])}">{sicon(s["Status"])} {s["Status"]}</span></td></tr>'
        h+='</table></div>'
        st.markdown(h,unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="panel"><div class="panel-title">{"📊 التعرض حسب المنطقة" if AR else "📊 Exposure by Zone"}</div>',unsafe_allow_html=True)
        ze=[{"Zone":z["ZoneName"],"Exp":max(s["ExposurePct"] for s in zhstats(z["ZoneID"]))*100} for _,z in zones_df.iterrows()]
        zdf=pd.DataFrame(ze)
        colors=["#C62828" if v>=100 else "#F9A825" if v>=80 else "#2E7D32" for v in zdf["Exp"]]
        fig=go.Figure()
        fig.add_trace(go.Bar(x=zdf["Zone"],y=zdf["Exp"],marker_color=colors,text=[f"{v:.0f}%" for v in zdf["Exp"]],textposition="outside",textfont=dict(size=12,color=C["text2"])))
        fig.add_hline(y=100,line_dash="dash",line_color="#C62828",line_width=2,annotation_text="⚠️ Limit",annotation_position="top right",annotation_font=dict(color="#C62828",size=11))
        fig.update_layout(**PL,height=380,showlegend=False,yaxis=dict(title="Exposure %",gridcolor=C["grid"],range=[0,max(zdf["Exp"].max()*1.2,130)]),xaxis=dict(tickangle=-25))
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("</div>",unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="panel"><div class="panel-title">{"◉ توزيع المخاطر" if AR else "◉ Risk Distribution"}</div>',unsafe_allow_html=True)
        scc={"Safe":0,"Warning":0,"Critical":0}
        for _,z in zones_df.iterrows(): scc[zoverall(z["ZoneID"])]+=1
        fig=go.Figure(data=[go.Pie(labels=list(scc.keys()),values=list(scc.values()),hole=0.6,marker_colors=[C["safe"],C["warn"],C["crit"]],textinfo="label+value",textfont=dict(size=13,color="#FFF"),pull=[0,0,0.05])])
        fig.update_layout(**PL,height=380,showlegend=False,annotations=[dict(text="<b>Risk</b>",x=.5,y=.5,font_size=18,font_color=C["text1"],showarrow=False)])
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("</div>",unsafe_allow_html=True)

    # FACILITY HEATMAP
    st.markdown(f'<div class="panel"><div class="panel-title">{"🏭 خريطة المنشأة الحرارية" if AR else "🏭 Facility Thermal Hazard Map"}</div>',unsafe_allow_html=True)
    st.plotly_chart(render_facility_map(),use_container_width=True)
    st.markdown("</div>",unsafe_allow_html=True)

    # Bottom KPIs
    m1,m2,m3,m4=st.columns(4)
    tw=workers_df["WorkerID"].nunique();ar=w_risk();szc=sz_count();tz=len(zones_df);lu=last_upd();lus=lu.strftime("%Y-%m-%d %H:%M") if pd.notna(lu) else "N/A"
    with m1: st.markdown(rmkpi("👷","Total Workers",tw,C["safe_bg"]),unsafe_allow_html=True)
    with m2: st.markdown(rmkpi("🚨","Workers at Risk",ar,C["crit_bg"]),unsafe_allow_html=True)
    with m3: st.markdown(rmkpi("✅","Safe Zones",f"{szc}/{tz}",C["safe_bg"]),unsafe_allow_html=True)
    with m4: st.markdown(rmkpi("🕐","Last Updated",lus,C["warn_bg"]),unsafe_allow_html=True)

# ═══════════════ TAB 2: OVERVIEW ═══════════════
with tab2:
    tr=st.selectbox("📅 الفترة الزمنية" if AR else "📅 Time Range",["Last 7 days","Last 30 days","All time"],key="ovt")
    mdt=readings_df["ReadingDateTime"].max()
    if tr=="Last 7 days": mndt=mdt-timedelta(days=7)
    elif tr=="Last 30 days": mndt=mdt-timedelta(days=30)
    else: mndt=readings_df["ReadingDateTime"].min()
    fr=readings_df[(readings_df["ReadingDateTime"]>=mndt)&(readings_df["ReadingDateTime"]<=mdt)]
    ld=get_ld()
    exc=sum(1 for _,r in fr.iterrows() if ld.get(r["HazardType"],1e9)<r["MeasuredValue"])
    hex_d={};
    for _,r in fr.iterrows():
        if ld.get(r["HazardType"],1e9)<r["MeasuredValue"]: hex_d[r["HazardType"]]=hex_d.get(r["HazardType"],0)+1
    mf=HD.get(max(hex_d,key=hex_d.get),"None") if hex_d else "None"
    ph=presence_df.copy();ph["Hours"]=(ph["ExitDateTime"]-ph["EntryDateTime"]).dt.total_seconds()/3600
    thr=ph["Hours"].sum();czl=[z["ZoneID"] for _,z in zones_df.iterrows() if zoverall(z["ZoneID"])=="Critical"]

    o1,o2,o3,o4=st.columns(4)
    with o1: st.markdown(rkpi_s("⚡","Exceedances",exc,"readings",0,"Critical" if exc else "Safe"),unsafe_allow_html=True)
    with o2: st.markdown(rkpi_s("🔥","Most Frequent",mf,"",0,"Warning"),unsafe_allow_html=True)
    with o3: st.markdown(rkpi_s("⏱️","Monitored Hrs",f"{thr:.0f}","hrs",0,"Safe"),unsafe_allow_html=True)
    with o4: st.markdown(rkpi_s("🏭","Critical Zones",len(czl),f"/ {len(zones_df)}",0,"Critical" if czl else "Safe"),unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>",unsafe_allow_html=True)
    ch,ct=st.columns([5,5])
    with ch:
        st.markdown(f'<div class="panel"><div class="panel-title">{"🗺️ خريطة المنطقة × الخطر" if AR else "🗺️ Zone vs Hazard Heatmap"}</div>',unsafe_allow_html=True)
        zns=zones_df["ZoneName"].tolist();zis=zones_df["ZoneID"].tolist()
        mx=[[round(cexp(fr[(fr["ZoneID"]==zid)&(fr["HazardType"]==h)]["MeasuredValue"].mean() if len(fr[(fr["ZoneID"]==zid)&(fr["HazardType"]==h)])>0 else 0,ld.get(h,1))*100,1) for h in HO] for zid in zis]
        fig=go.Figure(data=go.Heatmap(z=mx,x=[HD.get(h,h) for h in HO],y=zns,colorscale=[[0,"#1B5E20"],[0.5,"#F57F17"],[0.8,"#E65100"],[1,"#C62828"]],text=[[f"{v:.0f}%" for v in r] for r in mx],texttemplate="%{text}",textfont=dict(size=13,color="#FFF"),zmin=0,zmax=130,colorbar=dict(title="Exp%",ticksuffix="%")))
        fig.update_layout(**PL,height=370,xaxis_side="top")
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("</div>",unsafe_allow_html=True)
    with ct:
        st.markdown(f'<div class="panel"><div class="panel-title">{"📈 اتجاه مستويات الخطر" if AR else "📈 Hazard Levels Trend"}</div>',unsafe_allow_html=True)
        fig=go.Figure()
        for h in HO:
            hdf=fr[fr["HazardType"]==h].copy()
            if len(hdf)==0: continue
            hdf=hdf.sort_values("ReadingDateTime");hdf["Hour"]=hdf["ReadingDateTime"].dt.floor("h")
            t=hdf.groupby("Hour")["MeasuredValue"].mean().reset_index();t["Exp"]=t["MeasuredValue"]/ld.get(h,1)*100
            fig.add_trace(go.Scatter(x=t["Hour"],y=t["Exp"],name=HD.get(h,h),line=dict(color=HC.get(h,"#333"),width=2.5),mode="lines"))
        fig.add_hline(y=100,line_dash="dash",line_color="#C62828",line_width=2,annotation_text="Limit 100%",annotation_position="top right",annotation_font_color="#C62828")
        fig.update_layout(**PL,height=370,yaxis_title="Exposure %",yaxis=dict(gridcolor=C["grid"]),xaxis=dict(gridcolor=C["grid"]),legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("</div>",unsafe_allow_html=True)

    st.markdown(f'<div class="panel"><div class="panel-title">{"👷 أكثر 5 عمال تعرضاً" if AR else "👷 Top 5 Workers"}</div>',unsafe_allow_html=True)
    pm=ph.merge(workers_df[["WorkerID","FullName"]],on="WorkerID",how="left")
    t5=pm.groupby(["WorkerID","FullName"])["Hours"].sum().reset_index().sort_values("Hours",ascending=True).tail(5)
    fig=go.Figure();fig.add_trace(go.Bar(y=t5["FullName"],x=t5["Hours"],orientation="h",marker_color="#0F4C75",text=[f"{h:.1f} hrs" for h in t5["Hours"]],textposition="outside",textfont=dict(size=12,color=C["text2"])))
    fig.update_layout(**PL,height=260,xaxis_title="Hours",showlegend=False,yaxis=dict(tickfont=dict(size=13,color=C["text1"])))
    st.plotly_chart(fig,use_container_width=True)
    st.markdown("</div>",unsafe_allow_html=True)

# ═══════════════ TAB 3: ZONES ═══════════════
with tab3:
    zl,zd=st.columns([3,7])
    with zl:
        st.markdown(f'<div class="panel"><div class="panel-title">{"🏭 قائمة المناطق" if AR else "🏭 Zone List"}</div>',unsafe_allow_html=True)
        zlabels=[f"{z['ZoneID']} - {z['ZoneName']}" for _,z in zones_df.iterrows()]
        selz=st.selectbox("🏭 Select Zone" if not AR else "🏭 اختر المنطقة",zlabels,key="zs",label_visibility="collapsed")
        for _,z in zones_df.iterrows():
            s=zoverall(z["ZoneID"]);dc=scolor(s);act="active" if f"{z['ZoneID']} - {z['ZoneName']}"==selz else ""
            st.markdown(f'<div class="zone-card {act}"><div class="zone-dot" style="background:{dc}"></div><div><div class="zone-card-name">{z["ZoneName"]}</div><div class="zone-card-sub">{z["ZoneType"]} · Cap: {z["Capacity"]}</div></div></div>',unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)
        st.markdown(f'<div class="panel"><div class="panel-title">{"⚖️ مقارنة" if AR else "⚖️ Compare"}</div>',unsafe_allow_html=True)
        comp_zone=st.selectbox("Compare with:",["None"]+zlabels,key="zcomp")
        st.markdown("</div>",unsafe_allow_html=True)
    with zd:
        szid=selz.split(" - ")[0];szn=zname(szid);zst=zoverall(szid)
        st.markdown(f'<div class="status-banner banner-{zst.lower()}">{sicon(zst)} {szn} — {zst.upper()}</div>',unsafe_allow_html=True)
        st.markdown("<div style='height:14px'></div>",unsafe_allow_html=True)
        zsts=zhstats(szid)
        hc=st.columns(4)
        for i,s in enumerate(zsts):
            with hc[i]: st.markdown(rkpi(s["Icon"],s["DisplayName"],s["CurrentValue"],s["Unit"],s["ExposurePct"],s["Status"],szid,s["HazardType"]),unsafe_allow_html=True)
        st.markdown("<div style='height:16px'></div>",unsafe_allow_html=True)
        if comp_zone!="None":
            czid=comp_zone.split(" - ")[0];czn=zname(czid);czsts=zhstats(czid)
            st.markdown(f'<div class="panel"><div class="panel-title">⚖️ {szn} vs {czn}</div>',unsafe_allow_html=True)
            fig=go.Figure()
            fig.add_trace(go.Bar(name=szn,x=[s["DisplayName"] for s in zsts],y=[s["ExposurePct"]*100 for s in zsts],marker_color="#0F4C75",text=[f"{s['ExposurePct']:.0%}" for s in zsts],textposition="outside"))
            fig.add_trace(go.Bar(name=czn,x=[s["DisplayName"] for s in czsts],y=[s["ExposurePct"]*100 for s in czsts],marker_color="#4FC3F7",text=[f"{s['ExposurePct']:.0%}" for s in czsts],textposition="outside"))
            fig.add_hline(y=100,line_dash="dash",line_color="#C62828",line_width=2)
            fig.update_layout(**PL,height=320,barmode="group",yaxis=dict(title="Exposure %",gridcolor=C["grid"]),legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("</div>",unsafe_allow_html=True)

        d1,d2=st.columns([5,5])
        with d1:
            st.markdown(f'<div class="panel"><div class="panel-title">🗺️ Sensor Map</div>',unsafe_allow_html=True)
            sns=[{"n":"Sensor A","x":2,"y":6,"t":"CO2"},{"n":"Sensor B","x":8,"y":6,"t":"Noise"},{"n":"Sensor C","x":2,"y":2,"t":"Gas"},{"n":"Sensor D","x":8,"y":2,"t":"HeatIndex"}]
            fig=go.Figure()
            fig.add_shape(type="rect",x0=0,y0=0,x1=10,y1=8,fillcolor="rgba(30,41,59,0.5)",line=dict(color="#0F4C75",width=2,dash="dot"))
            for gx in range(1,10): fig.add_shape(type="line",x0=gx,y0=0,x1=gx,y1=8,line=dict(color="#334155",width=0.5))
            for gy in range(1,8): fig.add_shape(type="line",x0=0,y0=gy,x1=10,y1=gy,line=dict(color="#334155",width=0.5))
            for sn in sns:
                hs=next((s for s in zsts if s["HazardType"]==sn["t"]),None);clr=scolor(hs["Status"]) if hs else "#999";et=f"{hs['ExposurePct']:.0%}" if hs else "N/A"
                fig.add_trace(go.Scatter(x=[sn["x"]],y=[sn["y"]],mode="markers+text",marker=dict(size=30,color=clr,symbol="hexagon2",line=dict(color="#0F172A",width=3),opacity=0.9),text=[f"<b>{sn['n']}</b><br>{HD.get(sn['t'],sn['t'])}: {et}"],textposition="top center",textfont=dict(size=10,color=C["text1"]),showlegend=False,hovertemplate=f"<b>{sn['n']}</b><br>{sn['t']}: {et}<extra></extra>"))
                fig.add_trace(go.Scatter(x=[sn["x"]],y=[sn["y"]],mode="markers",marker=dict(size=45,color=clr,opacity=0.12),showlegend=False,hoverinfo="skip"))
            fig.add_annotation(x=5,y=-0.8,text=f"<b>{szn}</b>",showarrow=False,font=dict(size=15,color=C["text1"]))
            fig.update_layout(**PL,height=320,xaxis=dict(visible=False,range=[-1.5,11.5]),yaxis=dict(visible=False,range=[-1.8,9.5]))
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("</div>",unsafe_allow_html=True)
        with d2:
            st.markdown(f'<div class="panel"><div class="panel-title">📋 Sensor Readings</div>',unsafe_allow_html=True)
            snm=["Sensor A","Sensor B","Sensor C","Sensor D"]
            t='<table class="styled-table"><tr><th>Sensor</th><th>Hazard</th><th>Value</th><th>Exp%</th><th>Status</th></tr>'
            for i,s in enumerate(zsts):
                pb=pbar(s["ExposurePct"],s["Status"])
                t+=f'<tr><td style="color:{C["text1"]}!important;font-weight:700">{snm[i]}</td><td style="color:{C["text2"]}!important">{s["Icon"]} {s["DisplayName"]}</td><td style="color:{C["text2"]}!important;font-weight:600">{s["CurrentValue"]} {s["Unit"]}</td><td style="color:{stxt(s["Status"])}!important;font-weight:800">{s["ExposurePct"]:.0%}{pb}</td><td><span class="kpi-status status-{scss(s["Status"])}">{s["Status"]}</span></td></tr>'
            t+='</table></div>'
            st.markdown(t,unsafe_allow_html=True)
            st.markdown(f'<div class="panel"><div class="panel-title">📡 Radar</div>',unsafe_allow_html=True)
            cats=[s["DisplayName"] for s in zsts]+[zsts[0]["DisplayName"]];vals=[s["ExposurePct"]*100 for s in zsts]+[zsts[0]["ExposurePct"]*100]
            fig=go.Figure()
            fig.add_trace(go.Scatterpolar(r=vals,theta=cats,fill='toself',fillcolor="rgba(79,195,247,0.15)",line=dict(color="#4FC3F7",width=2.5),name="Current"))
            fig.add_trace(go.Scatterpolar(r=[100]*5,theta=cats,line=dict(color="#C62828",width=2,dash="dash"),name="Limit"))
            fig.update_layout(**PL,height=280,polar=dict(radialaxis=dict(visible=True,range=[0,max(max(vals)*1.1,120)],gridcolor=C["grid"],tickfont=dict(size=10,color=C["text3"])),angularaxis=dict(tickfont=dict(size=12,color=C["text1"]))),showlegend=True,legend=dict(orientation="h",y=-0.1,x=0.5,xanchor="center"))
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("</div>",unsafe_allow_html=True)
        st.markdown(f'<div class="panel"><div class="panel-title">👷 Present Workers</div>',unsafe_allow_html=True)
        zw=presence_df[presence_df["ZoneID"]==szid].merge(workers_df,on="WorkerID",how="left")
        if len(zw)>0:
            wcs=st.columns(min(4,len(zw)))
            for i,(_,w) in enumerate(zw.iterrows()):
                ent=w["EntryDateTime"].strftime("%H:%M") if pd.notna(w["EntryDateTime"]) else "N/A"
                dur=f'{(w["ExitDateTime"]-w["EntryDateTime"]).total_seconds()/3600:.1f} hrs' if pd.notna(w["EntryDateTime"]) and pd.notna(w["ExitDateTime"]) else ""
                with wcs[i%min(4,len(zw))]:
                    st.markdown(f'<div class="worker-card"><div class="worker-card-name">👤 {w.get("FullName",w["WorkerID"])}</div><div class="worker-card-sub">{w.get("JobTitle","N/A")} · Entry: {ent}</div><div class="worker-card-hours">{dur}</div></div>',unsafe_allow_html=True)
        else: st.info("No workers currently present.")
        st.markdown("</div>",unsafe_allow_html=True)

# ═══════════════ TAB 4: SIMULATION (with manual input) ═══════════════
with tab4:
    ld = get_ld()
    sim_mode = "✏️ Manual Input"

    if True:  # Manual Input Mode — Equipment-based
        st.markdown(f'<div class="panel"><div class="panel-title">{"✏️ حاسبة تأثير المعدة الجديدة" if AR else "✏️ New Equipment Impact Calculator"}</div>', unsafe_allow_html=True)
        st.markdown(f'''<p style="color:{C["text2"]};font-size:13px;margin-bottom:16px">
        {"أدخل مواصفات المعدة من الكتالوج. النظام يحسب التأثير تلقائياً." if AR else "Enter the <strong style='color:{C['accent']}'>equipment specifications</strong> from the manual/datasheet. The system calculates the impact automatically."}</p>''', unsafe_allow_html=True)

        # Zone + Equipment name
        mz1, mz2 = st.columns(2)
        with mz1:
            man_zone = st.selectbox("🏭 Select Target Zone", [f"{z['ZoneID']} - {z['ZoneName']}" for _, z in zones_df.iterrows()], key="man_zone")
        with mz2:
            equip_name = st.text_input("🔧 Equipment Name (from manual)", value="New Equipment", key="eq_name")
        man_zid = man_zone.split(" - ")[0]
        man_zname = zname(man_zid)
        cur_stats = zhstats(man_zid)

        st.markdown(f'<div style="color:{C["accent"]};font-size:14px;font-weight:700;margin:12px 0">📖 Enter values from <em>{equip_name}</em> manual / datasheet:</div>', unsafe_allow_html=True)

        # Input fields — equipment emission values
        mc1, mc2, mc3, mc4 = st.columns(4)
        equip_vals = {}
        input_labels = {
            "CO2": ("💨 CO₂ Emission" if not AR else "💨 انبعاث CO₂", "ppm" if not AR else "جزء بالمليون"),
            "HeatIndex": ("🌡️ Equipment Temperature" if not AR else "🌡️ درجة حرارة المعدة", "°C" if not AR else "درجة مئوية"),
            "Noise": ("🔊 Noise Level" if not AR else "🔊 مستوى الضوضاء", "dBA" if not AR else "ديسيبل"),
            "Gas": ("⚗️ Gas Emission" if not AR else "⚗️ انبعاث الغاز", "ppm" if not AR else "جزء بالمليون"),
        }
        for i, (col, s) in enumerate(zip([mc1, mc2, mc3, mc4], cur_stats)):
            with col:
                lbl = input_labels.get(s["HazardType"], ("📊 Value", ""))
                st.markdown(f'''<div class="sim-input-card">
                    <div class="sim-input-title">{lbl[0]}</div>
                    <div style="color:{C["text3"]};font-size:10px;margin-top:-8px;margin-bottom:8px">{lbl[1]}</div>
                </div>''', unsafe_allow_html=True)
                equip_vals[s["HazardType"]] = st.number_input(
                    f'{s["DisplayName"]}',
                    min_value=0.0,
                    max_value=s["Limit"] * 5.0,
                    value=0.0,
                    step=1.0,
                    key=f"eq_{s['HazardType']}",
                    label_visibility="collapsed"
                )
                st.markdown(f'<span style="color:{C["text3"]};font-size:11px">{"الحالي" if AR else "Current"}: <strong style="color:{C["text1"]}">{s["CurrentValue"]}</strong> {s["Unit"]} | {"الحد" if AR else "Limit"}: {s["Limit"]}</span>', unsafe_allow_html=True)

        # Calculate combined values using correct physics
        def calc_combined(hazard_type, current_val, equip_val):
            """Calculate combined value using correct method per hazard type"""
            if equip_val == 0:
                return current_val

            if hazard_type == "Noise":
                # Logarithmic addition for dBA
                # L_total = 10 * log10(10^(L1/10) + 10^(L2/10))
                if current_val <= 0: return equip_val
                if equip_val <= 0: return current_val
                combined = 10 * math.log10(10**(current_val/10) + 10**(equip_val/10))
                return round(combined, 1)

            elif hazard_type == "HeatIndex":
                # Heat: take the maximum (dominant source) + small additive factor
                # In reality, heat index is affected by the hottest source primarily
                # Adding a small contribution: max + 10% of the difference
                if equip_val > current_val:
                    combined = equip_val + (current_val * 0.1)
                else:
                    combined = current_val + (equip_val * 0.1)
                return round(combined, 1)

            elif hazard_type in ["CO2", "Gas"]:
                # Concentration: additive (ppm accumulates in air)
                return round(current_val + equip_val, 1)

            return round(current_val + equip_val, 1)

        # Show simple results (formulas hidden internally)
        st.markdown(f'<div style="color:{C["accent"]};font-size:14px;font-weight:700;margin:16px 0">{"🔬 النتائج المتوقعة:" if AR else "🔬 Expected Results:"}</div>', unsafe_allow_html=True)
        calc_cols = st.columns(4)
        combined_vals = {}
        for i, (col, s) in enumerate(zip(calc_cols, cur_stats)):
            h = s["HazardType"]
            eq_v = equip_vals.get(h, 0)
            cur_v = s["CurrentValue"]
            comb = calc_combined(h, cur_v, eq_v)
            combined_vals[h] = comb

            with col:
                delta = round(comb - cur_v, 1)
                new_exp = cexp(comb, s["Limit"])
                new_st = gstat(new_exp)
                ds = f"+{delta}" if delta > 0 else str(delta)
                dc = "#EF5350" if delta > 0 else "#81C784" if delta < 0 else C["text3"]

                st.markdown(f'''<div style="background:#0F172A;border:1px solid #334155;border-radius:12px;padding:14px;text-align:center">
                    <div style="font-size:12px;color:{C["text3"]};font-weight:700">{s["Icon"]} {s["DisplayName"]}</div>
                    <div style="font-size:12px;color:{C["text3"]};margin:4px 0">{cur_v} → <strong style="color:{C["text1"]}">{comb}</strong> {s["Unit"]}</div>
                    <div style="font-size:22px;font-weight:900;color:{dc};margin:6px 0">{ds}</div>
                    <div><span class="kpi-status status-{scss(new_st)}">{sicon(new_st)} {new_st} ({new_exp:.0%})</span></div>
                </div>''', unsafe_allow_html=True)

        # Build comparison dataframe
        cr = []
        for _, z in zones_df.iterrows():
            for h in HO:
                rdf = readings_df[(readings_df["ZoneID"] == z["ZoneID"]) & (readings_df["HazardType"] == h)]
                cur = rdf["MeasuredValue"].mean() if len(rdf) > 0 else 0

                if z["ZoneID"] == man_zid:
                    proj = combined_vals.get(h, cur)
                    delta = round(proj - cur, 1)
                else:
                    proj = cur; delta = 0

                lm = ld.get(h, 1)
                cr.append({"Zone":z["ZoneName"],"ZoneID":z["ZoneID"],"Hazard":HD.get(h,h),"HazardType":h,"Before":round(cur,1),"Delta":delta,"After":round(proj,1),"Limit":lm,"BExp":cexp(cur,lm),"AExp":cexp(proj,lm),"BSt":gstat(cexp(cur,lm)),"ASt":gstat(cexp(proj,lm))})
        comp = pd.DataFrame(cr)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Simulation Results (shared for both modes) ──
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    sk1, sk2, sk3 = st.columns(3)
    ac = comp[comp["ASt"] == "Critical"]["Zone"].nunique()
    aw = comp[comp["ASt"] == "Warning"]["Zone"].nunique()
    mxa = comp["AExp"].max() * 100
    with sk1: st.markdown(rmkpi("🚨", "Zones → Critical", ac, C["crit_bg"]), unsafe_allow_html=True)
    with sk2: st.markdown(rmkpi("⚠️", "Zones → Warning", aw, C["warn_bg"]), unsafe_allow_html=True)
    with sk3: st.markdown(rmkpi("📊", "Max Exposure", f"{mxa:.0f}%", C["safe_bg"]), unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    s1, s2 = st.columns(2)
    with s1:
        st.markdown(f'<div class="panel"><div class="panel-title">📊 Before vs After</div>', unsafe_allow_html=True)
        zc = comp.groupby("Zone").agg(B=("BExp", "max"), A=("AExp", "max")).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Before", x=zc["Zone"], y=zc["B"]*100, marker_color="#0F4C75", text=[f"{v:.0f}%" for v in zc["B"]*100], textposition="outside"))
        fig.add_trace(go.Bar(name="After", x=zc["Zone"], y=zc["A"]*100, marker_color="#4FC3F7", text=[f"{v:.0f}%" for v in zc["A"]*100], textposition="outside"))
        fig.add_hline(y=100, line_dash="dash", line_color="#C62828", line_width=2)
        fig.update_layout(**PL, height=400, barmode="group", yaxis_title="Exposure %", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), yaxis=dict(gridcolor=C["grid"]))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="panel"><div class="panel-title">📋 Impact Details</div>', unsafe_allow_html=True)
        chg = comp[comp["Delta"] != 0]
        if len(chg) > 0:
            # Gauge cards for affected zone
            if sim_mode == "✏️ Manual Input":
                st.markdown(f"**Impact on {man_zname}:**", unsafe_allow_html=True)
                gc = st.columns(4)
                man_stats = comp[comp["ZoneID"] == man_zid]
                for i, (_, r) in enumerate(man_stats.iterrows()):
                    with gc[i]:
                        st.markdown(rkpi(HI.get(r["HazardType"],""), r["Hazard"], r["After"], "", r["AExp"], r["ASt"]), unsafe_allow_html=True)

            t = '<table class="styled-table"><tr><th>Zone</th><th>Hazard</th><th>Before</th><th>Δ</th><th>After</th><th>Exp%</th><th>Status</th></tr>'
            for _, r in chg.iterrows():
                ds = "+" if r["Delta"] > 0 else ""; dc = "#EF5350" if r["Delta"] > 0 else "#81C784"
                t += f'<tr><td style="color:{C["text1"]}!important;font-weight:700">{r["Zone"]}</td><td style="color:{C["text2"]}!important">{HI.get(r["HazardType"],"")} {r["Hazard"]}</td><td style="color:{C["text2"]}!important">{r["Before"]}</td><td style="color:{dc}!important;font-weight:800">{ds}{r["Delta"]}</td><td style="color:{C["text1"]}!important;font-weight:700">{r["After"]}</td><td style="color:{stxt(r["ASt"])}!important;font-weight:800">{r["AExp"]:.0%}</td><td><span class="kpi-status status-{scss(r["ASt"])}">{r["ASt"]}</span></td></tr>'
            t += '</table>'
            st.markdown(t, unsafe_allow_html=True)
        else:
            st.info("No changes in this scenario.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Simulation Report Export ──
    if sim_mode == "✏️ Manual Input":
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="panel"><div class="panel-title">📄 Simulation Report — {man_zname}</div>', unsafe_allow_html=True)

        # Before vs After detail cards
        man_data = comp[comp["ZoneID"] == man_zid]
        bc1, bc2 = st.columns(2)
        with bc1:
            st.markdown(f'<div style="background:#0F172A;border:2px solid #1E3A5F;border-radius:16px;padding:20px;margin-bottom:12px"><div style="color:#4FC3F7;font-size:15px;font-weight:800;margin-bottom:14px;text-align:center">📊 BEFORE (Current Readings)</div>', unsafe_allow_html=True)
            tb = '<table class="styled-table"><tr><th>Hazard</th><th>Value</th><th>Limit</th><th>Exp%</th><th>Status</th></tr>'
            for _, r in man_data.iterrows():
                tb += f'<tr><td style="color:{C["text1"]}!important;font-weight:700">{HI.get(r["HazardType"],"")} {r["Hazard"]}</td><td style="color:{C["text2"]}!important">{r["Before"]} </td><td style="color:{C["text2"]}!important">{r["Limit"]}</td><td style="color:{stxt(r["BSt"])}!important;font-weight:800">{r["BExp"]:.0%}</td><td><span class="kpi-status status-{scss(r["BSt"])}">{r["BSt"]}</span></td></tr>'
            tb += '</table></div>'
            st.markdown(tb, unsafe_allow_html=True)
        with bc2:
            st.markdown(f'<div style="background:#0F172A;border:2px solid #1E3A5F;border-radius:16px;padding:20px;margin-bottom:12px"><div style="color:#EF5350;font-size:15px;font-weight:800;margin-bottom:14px;text-align:center">🔬 AFTER (Simulated Readings)</div>', unsafe_allow_html=True)
            ta = '<table class="styled-table"><tr><th>Hazard</th><th>Value</th><th>Δ Change</th><th>Exp%</th><th>Status</th></tr>'
            for _, r in man_data.iterrows():
                ds = "+" if r["Delta"] > 0 else ""
                dc = "#EF5350" if r["Delta"] > 0 else "#81C784" if r["Delta"] < 0 else C["text3"]
                ta += f'<tr><td style="color:{C["text1"]}!important;font-weight:700">{HI.get(r["HazardType"],"")} {r["Hazard"]}</td><td style="color:{C["text1"]}!important;font-weight:700">{r["After"]}</td><td style="color:{dc}!important;font-weight:800">{ds}{r["Delta"]}</td><td style="color:{stxt(r["ASt"])}!important;font-weight:800">{r["AExp"]:.0%}</td><td><span class="kpi-status status-{scss(r["ASt"])}">{r["ASt"]}</span></td></tr>'
            ta += '</table></div>'
            st.markdown(ta, unsafe_allow_html=True)

        # Summary verdict
        before_status = "Critical" if any(r["BSt"] == "Critical" for _, r in man_data.iterrows()) else "Warning" if any(r["BSt"] == "Warning" for _, r in man_data.iterrows()) else "Safe"
        after_status = "Critical" if any(r["ASt"] == "Critical" for _, r in man_data.iterrows()) else "Warning" if any(r["ASt"] == "Warning" for _, r in man_data.iterrows()) else "Safe"
        changed_hazards = man_data[man_data["Delta"] != 0]
        improved = sum(1 for _, r in changed_hazards.iterrows() if r["AExp"] < r["BExp"])
        worsened = sum(1 for _, r in changed_hazards.iterrows() if r["AExp"] > r["BExp"])

        v1, v2, v3, v4 = st.columns(4)
        with v1: st.markdown(rmkpi(sicon(before_status), "Before Status", before_status, sbg(before_status)), unsafe_allow_html=True)
        with v2: st.markdown(rmkpi(sicon(after_status), "After Status", after_status, sbg(after_status)), unsafe_allow_html=True)
        with v3: st.markdown(rmkpi("📈", "Worsened", f"{worsened} hazards", C["crit_bg"]), unsafe_allow_html=True)
        with v4: st.markdown(rmkpi("📉", "Improved", f"{improved} hazards", C["safe_bg"]), unsafe_allow_html=True)

        # ── Worker Impact Analysis ──
        # Find workers present in this zone
        zone_workers = presence_df[presence_df["ZoneID"] == man_zid]["WorkerID"].unique()
        zone_worker_data = []
        for wid in zone_workers:
            wi_row = workers_df[workers_df["WorkerID"]==wid]
            if len(wi_row)==0: continue
            wi_row = wi_row.iloc[0]
            wh_row = health_df[health_df["WorkerID"]==wid].iloc[0] if len(health_df)>0 and wid in health_df["WorkerID"].values else None
            zone_worker_data.append({"wid":wid, "wi":wi_row, "wh":wh_row})

        if zone_worker_data:
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            lbl_wi = "تأثير المعدة على العمال في هذه المنطقة" if AR else f"Worker Impact — {len(zone_worker_data)} workers in {man_zname}"
            st.markdown(f'<div class="panel"><div class="panel-title">👷 {lbl_wi}</div>', unsafe_allow_html=True)

            for wd in zone_worker_data:
                wid = wd["wid"]; wi_r = wd["wi"]; wh_r = wd["wh"]
                w_name = wi_r["FullName"]; w_job = wi_r["JobTitle"]

                # Build per-worker risks based on AFTER values + health profile
                w_risks = []
                w_color = "#81C784"  # default green

                if wh_r is not None:
                    w_age = wh_r.get("Age", 30)
                    w_bmi_cat = wh_r.get("BMICategory", "Normal")
                    w_fitness = wh_r.get("FitnessLevel", "Fit")
                    w_hearing = wh_r.get("HearingTest", "Pass")
                    w_lung = wh_r.get("LungFunction", "Normal")

                    # Check each hazard AFTER value against worker profile
                    for _, r in man_data.iterrows():
                        h = r["HazardType"]
                        a_exp = r["AExp"]
                        a_st = r["ASt"]

                        if h == "Noise" and a_st in ["Warning","Critical"]:
                            if w_hearing == "Fail":
                                w_risks.append(("🔴", "Hearing impaired — MUST NOT work in this zone after equipment install. Double protection insufficient at this level." if not AR else "ضعف سمع — يُمنع من العمل بهذه المنطقة بعد تركيب المعدة. الحماية المزدوجة غير كافية."))
                                w_color = "#EF9A9A"
                            elif w_hearing == "Partial Loss":
                                w_risks.append(("🟡", f"Partial hearing loss — Noise at {r['After']} dBA requires double ear protection and max 2-hour shifts." if not AR else f"ضعف سمع جزئي — الضوضاء عند {r['After']} ديسيبل تتطلب حماية أذن مزدوجة وورديات ساعتين كحد أقصى."))
                                if w_color != "#EF9A9A": w_color = "#FFD54F"

                        if h == "HeatIndex" and a_st in ["Warning","Critical"]:
                            if isinstance(w_age,(int,float)) and w_age >= 50:
                                w_risks.append(("🔴", f"Age {w_age} + Heat at {r['After']} — Max 2 hours, mandatory breaks every 30 min, priority hydration." if not AR else f"العمر {w_age} + حرارة {r['After']} — ساعتان كحد أقصى، استراحة كل 30 دقيقة، ترطيب إلزامي."))
                                w_color = "#EF9A9A"
                            elif isinstance(w_age,(int,float)) and w_age >= 45:
                                w_risks.append(("🟡", f"Age {w_age} — Monitor closely during heat exposure at {r['After']}." if not AR else f"العمر {w_age} — مراقبة دقيقة أثناء التعرض للحرارة عند {r['After']}."))
                                if w_color != "#EF9A9A": w_color = "#FFD54F"
                            if w_bmi_cat == "Obese":
                                w_risks.append(("🔴", f"BMI Obese + Heat at {r['After']} — Max 2 hours, hydration every 20 min. Consider reassignment." if not AR else f"سمنة + حرارة {r['After']} — ساعتان كحد أقصى، شرب ماء كل 20 دقيقة. يُنظر في نقله."))
                                w_color = "#EF9A9A"

                        if h in ["Gas","CO2"] and a_st in ["Warning","Critical"]:
                            if w_lung == "Reduced":
                                w_risks.append(("🔴", f"Reduced lung function — {r['Hazard']} at {r['After']} is dangerous. MUST use respiratory PPE or be reassigned." if not AR else f"ضعف وظائف الرئة — {r['Hazard']} عند {r['After']} خطر. يجب ارتداء كمامة تنفس أو النقل."))
                                w_color = "#EF9A9A"

                    if w_fitness == "Unfit":
                        w_risks.append(("🔴", "Classified UNFIT — Should not remain in this zone after equipment install." if not AR else "مصنّف غير لائق — لا يجب أن يبقى في هذه المنطقة بعد تركيب المعدة."))
                        w_color = "#EF9A9A"

                if not w_risks:
                    w_risks.append(("🟢", "No additional risk from this equipment based on health profile." if not AR else "لا توجد مخاطر إضافية من هذه المعدة بناءً على ملفه الصحي."))

                # Render worker card
                fit_lbl = ""
                if wh_r is not None:
                    fit_lbl = f" · Age: {wh_r.get('Age','')} · BMI: {wh_r.get('BMI','')} ({wh_r.get('BMICategory','')})"

                st.markdown(f'''<div style="background:#0F172A;border:1px solid {w_color};border-radius:14px;padding:16px 20px;margin-bottom:12px">
                    <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px">
                        <span style="font-size:28px">👤</span>
                        <div>
                            <div style="color:{C["text1"]};font-size:16px;font-weight:800">{w_name}</div>
                            <div style="color:{C["text3"]};font-size:12px">{w_job}{fit_lbl}</div>
                        </div>
                    </div>''', unsafe_allow_html=True)

                for icon, text in w_risks:
                    rbg = "#4A0E0E" if icon=="🔴" else "#4E3A00" if icon=="🟡" else "#1B3A1B"
                    rbd = "#C62828" if icon=="🔴" else "#F57F17" if icon=="🟡" else "#2E7D32"
                    d = "rtl" if AR else "ltr"
                    a = "right" if AR else "left"
                    st.markdown(f'''<div style="background:{rbg};border-left:3px solid {rbd};border-radius:8px;padding:10px 14px;margin-bottom:6px;direction:{d};text-align:{a}">
                        <span style="font-size:14px;margin-right:6px">{icon}</span>
                        <span style="color:{C["text1"]};font-size:13px">{text}</span>
                    </div>''', unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # Export button
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        if st.button("📥 Export Simulation Report", key="sim_report"):
            sim_html = f"""<html><head><style>
            body{{font-family:Inter,sans-serif;padding:40px;color:#FFF;background:#0F172A}}
            h1{{color:#4FC3F7;border-bottom:3px solid #0F4C75;padding-bottom:10px}}
            h2{{color:#4FC3F7;margin-top:30px}} h3{{color:#94A3B8}}
            table{{width:100%;border-collapse:collapse;margin:15px 0}}
            th{{background:#0B3558;color:white;padding:10px;text-align:left}}
            td{{padding:8px 10px;border-bottom:1px solid #334155;color:#94A3B8}}
            .safe{{color:#81C784;font-weight:bold}} .warning{{color:#FFD54F;font-weight:bold}} .critical{{color:#EF9A9A;font-weight:bold}}
            .badge{{padding:4px 12px;border-radius:12px;font-size:12px;font-weight:700}}
            .badge-safe{{background:#1B5E20;color:#81C784}} .badge-warning{{background:#4E3A00;color:#FFD54F}} .badge-critical{{background:#4A0E0E;color:#EF9A9A}}
            .section{{background:#1E293B;border-radius:12px;padding:20px;margin:16px 0}}
            .formula{{background:#0F172A;border:1px solid #334155;border-radius:8px;padding:10px;font-family:monospace;font-size:13px;color:#4FC3F7;margin:6px 0}}
            </style></head><body>
            <h1>🛡️ ExpoInsight — Equipment Impact Report</h1>
            <h3>Power Plant 0 · Saudi Arabia — Riyadh</h3>
            <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
            <p><strong>Zone:</strong> {man_zname} &nbsp;|&nbsp; <strong>Equipment:</strong> {equip_name}</p>
            <hr style="border-color:#334155">

            <div class="section">
            <h2>📖 Equipment Specifications (from manual)</h2>
            <table><tr><th>Hazard</th><th>Equipment Output</th><th>Unit</th></tr>"""
            for s in cur_stats:
                eq_v = equip_vals.get(s["HazardType"], 0)
                if eq_v > 0:
                    sim_html += f'<tr><td>{s["Icon"]} {s["DisplayName"]}</td><td>{eq_v}</td><td>{s["Unit"]}</td></tr>'
            sim_html += """</table></div>

            <div class="section">
            <h2>🔬 Calculation Methods</h2>
            <table><tr><th>Hazard</th><th>Method</th><th>Formula</th></tr>
            <tr><td>🔊 Noise</td><td>Logarithmic Addition</td><td><code>L = 10 × log₁₀(10^(L₁/10) + 10^(L₂/10))</code></td></tr>
            <tr><td>🌡️ Heat</td><td>Maximum + Factor</td><td><code>max(zone, equip) + 10% of minor source</code></td></tr>
            <tr><td>💨 CO₂</td><td>Additive Concentration</td><td><code>zone_ppm + equipment_ppm</code></td></tr>
            <tr><td>⚗️ Gas</td><td>Additive Concentration</td><td><code>zone_ppm + equipment_ppm</code></td></tr>
            </table></div>"""

            sim_html += f"""<div class="section">
            <h2>📊 BEFORE — Current Zone Readings</h2>
            <p>Zone Status: <span class="badge badge-{scss(before_status)}">{before_status}</span></p>
            <table><tr><th>Hazard</th><th>Current Value</th><th>Limit</th><th>Exposure %</th><th>Status</th></tr>"""
            for _, r in man_data.iterrows():
                sim_html += f'<tr><td>{HI.get(r["HazardType"],"")} {r["Hazard"]}</td><td>{r["Before"]}</td><td>{r["Limit"]}</td><td class="{scss(r["BSt"])}">{r["BExp"]:.0%}</td><td class="{scss(r["BSt"])}">{r["BSt"]}</td></tr>'
            sim_html += """</table></div>

            <div class="section">
            <h2>🔧 AFTER — With """ + equip_name + """ Installed</h2>"""
            sim_html += f'<p>Zone Status: <span class="badge badge-{scss(after_status)}">{after_status}</span></p>'
            sim_html += '<table><tr><th>Hazard</th><th>Zone Before</th><th>Equipment</th><th>Combined</th><th>Exposure %</th><th>Status</th></tr>'
            for _, r in man_data.iterrows():
                eq_v = equip_vals.get(r["HazardType"], 0)
                sim_html += f'<tr><td>{HI.get(r["HazardType"],"")} {r["Hazard"]}</td><td>{r["Before"]}</td><td>+{eq_v}</td><td class="{"critical" if r["AExp"]>=1 else "warning" if r["AExp"]>=0.8 else "safe"}">{r["After"]}</td><td class="{scss(r["ASt"])}">{r["AExp"]:.0%}</td><td class="{scss(r["ASt"])}">{r["ASt"]}</td></tr>'
            sim_html += '</table></div>'

            sim_html += f"""<div class="section">
            <h2>📋 Summary</h2>
            <table><tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Zone Overall Before</td><td class="{scss(before_status)}">{before_status}</td></tr>
            <tr><td>Zone Overall After</td><td class="{scss(after_status)}">{after_status}</td></tr>
            <tr><td>Hazards Worsened</td><td class="critical">{worsened}</td></tr>
            <tr><td>Hazards Improved</td><td class="safe">{improved}</td></tr>
            </table></div>

            <div class="section">
            <h2>💡 Recommendations</h2><ul style="color:#94A3B8">"""
            for _, r in man_data.iterrows():
                if r["ASt"] == "Critical":
                    sim_html += f'<li><strong style="color:#EF9A9A">{r["Hazard"]}</strong>: Exposure at {r["AExp"]:.0%} exceeds limit. Immediate engineering controls or PPE required.</li>'
                elif r["ASt"] == "Warning":
                    sim_html += f'<li><strong style="color:#FFD54F">{r["Hazard"]}</strong>: Exposure at {r["AExp"]:.0%} approaching limit. Monitor closely and consider preventive measures.</li>'
                else:
                    sim_html += f'<li><strong style="color:#81C784">{r["Hazard"]}</strong>: Exposure at {r["AExp"]:.0%} within safe limits.</li>'
            sim_html += '</ul></div>'

            # Worker impact in report
            if zone_worker_data:
                sim_html += '<div class="section"><h2>👷 Worker Impact Analysis</h2>'
                for wd in zone_worker_data:
                    wid=wd["wid"]; wi_r=wd["wi"]; wh_r=wd["wh"]
                    w_name=wi_r["FullName"]; w_job=wi_r["JobTitle"]
                    fit_info = f" · Age: {wh_r.get('Age','')} · BMI: {wh_r.get('BMI','')} ({wh_r.get('BMICategory','')})" if wh_r is not None else ""
                    sim_html += f'<div style="border:1px solid #334155;border-radius:8px;padding:12px;margin:8px 0"><strong style="color:#4FC3F7">{w_name}</strong> <span style="color:#94A3B8">— {w_job}{fit_info}</span><ul style="margin:8px 0">'
                    has_risk = False
                    if wh_r is not None:
                        for _, r in man_data.iterrows():
                            h=r["HazardType"]; a_st=r["ASt"]
                            if h=="Noise" and a_st in ["Warning","Critical"] and wh_r.get("HearingTest") in ["Fail","Partial Loss"]:
                                sim_html += f'<li class="critical">Hearing: {wh_r.get("HearingTest")} — Noise at {r["After"]} dBA requires additional protection</li>'
                                has_risk = True
                            if h=="HeatIndex" and a_st in ["Warning","Critical"]:
                                wa = wh_r.get("Age",30)
                                if isinstance(wa,(int,float)) and wa>=45:
                                    sim_html += f'<li class="warning">Age {wa} — Heat at {r["After"]} requires reduced shifts and breaks</li>'
                                    has_risk = True
                                if wh_r.get("BMICategory")=="Obese":
                                    sim_html += f'<li class="critical">BMI Obese — Heat at {r["After"]} requires max 2hr shifts and hydration</li>'
                                    has_risk = True
                            if h in ["Gas","CO2"] and a_st in ["Warning","Critical"] and wh_r.get("LungFunction")=="Reduced":
                                sim_html += f'<li class="critical">Reduced lung function — {r["Hazard"]} at {r["After"]} requires respiratory PPE</li>'
                                has_risk = True
                        if wh_r.get("FitnessLevel")=="Unfit":
                            sim_html += '<li class="critical">Classified UNFIT — Should not remain in this zone</li>'
                            has_risk = True
                    if not has_risk:
                        sim_html += '<li class="safe">No additional risk from this equipment</li>'
                    sim_html += '</ul></div>'
                sim_html += '</div>'

            sim_html += '</body></html>'

            st.download_button("📥 Download Simulation Report", data=sim_html,
                file_name=f"Simulation_{man_zname.replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                mime="text/html", key="dl_sim")
            st.success("✅ Report ready!")

        st.markdown("</div>", unsafe_allow_html=True)
with tab5:
    wo=[f"{w['WorkerID']} - {w['FullName']}" for _,w in workers_df.iterrows()]
    sw=st.selectbox("👷 اختر العامل" if AR else "👷 Select Worker",wo,key="ws");swid=sw.split(" - ")[0]
    wi=workers_df[workers_df["WorkerID"]==swid].iloc[0]
    wp=presence_df[presence_df["WorkerID"]==swid].copy()

    # Get health data
    wh = health_df[health_df["WorkerID"]==swid].iloc[0] if len(health_df)>0 and swid in health_df["WorkerID"].values else None

    # ── Worker Identity Card ──
    duty_color = "#2E7D32" if wh is not None and wh.get("FitnessForDuty")=="Fit for Duty" else "#F57F17" if wh is not None and "Restrictions" in str(wh.get("FitnessForDuty","")) else "#C62828"
    duty_label = wh["FitnessForDuty"] if wh is not None else "No Data"
    duty_bg = C["safe_bg"] if "Fit for Duty"==duty_label else C["warn_bg"] if "Restrictions" in duty_label else C["crit_bg"]

    st.markdown(f'''<div class="panel" style="border-left:6px solid {duty_color}">
        <div style="display:flex;align-items:center;gap:24px;flex-wrap:wrap">
            <div style="font-size:56px;line-height:1">👤</div>
            <div style="flex:1;min-width:200px">
                <div style="font-size:24px;font-weight:900;color:{C["text1"]}">{wi["FullName"]}</div>
                <div style="font-size:14px;color:{C["text2"]};margin-top:2px">{wi["JobTitle"]} · {wi["Department"]} · Shift: {wi["Shift"]}</div>
                <div style="margin-top:8px"><span class="kpi-status" style="background:{duty_bg};color:{"#81C784" if duty_label=="Fit for Duty" else "#FFD54F" if "Restrictions" in duty_label else "#EF9A9A"};font-size:13px;padding:6px 16px">{duty_label}</span></div>
            </div>
            <div style="text-align:right;min-width:160px">
                <div style="color:{C["text3"]};font-size:10px;font-weight:700;letter-spacing:1px">NCOSH COMPLIANCE</div>
                <div style="color:{C["text3"]};font-size:11px;margin-top:2px">لائحة فحوصات اللياقة المهنية</div>
            </div>
        </div>
    </div>''', unsafe_allow_html=True)

    # ── Exposure data — calculate first for recommendations ──
    tth=0;zvs=set()
    if len(wp)>0:
        wp["Hours"]=(wp["ExitDateTime"]-wp["EntryDateTime"]).dt.total_seconds()/3600;tth=wp["Hours"].sum();zvs=set(wp["ZoneID"].unique())
    cv=[z for z in zvs if zoverall(z)=="Critical"];rl="At Risk" if cv else "Safe";rs="Critical" if cv else "Safe"

    # Use global AR variable for language
    ar = AR

    # ── Health Profile Card ──
    if wh is not None:
        title_health = "ملف العامل — الفحص السنوي" if ar else "Worker Profile — Annual Fitness Exam"
        st.markdown(f'<div class="panel"><div class="panel-title">🏥 {title_health}</div>', unsafe_allow_html=True)

        age = wh.get("Age","N/A")
        height = wh.get("Height_cm","N/A")
        weight = wh.get("Weight_kg","N/A")
        bmi = wh.get("BMI","N/A")
        bmi_cat = wh.get("BMICategory","N/A")
        fitness = wh.get("FitnessLevel","N/A")
        exam_status = wh.get("ExamStatus","N/A")
        last_exam = wh.get("LastMedicalExam","N/A")
        next_exam = wh.get("NextExamDue","N/A")
        hearing = wh.get("HearingTest","Pass")
        lung = wh.get("LungFunction","Normal")

        if fitness == "Fit": fit_icon="✅"; fit_color="#81C784"; fit_lbl="لائق" if ar else "Fit"
        elif fitness == "Moderate": fit_icon="⚠️"; fit_color="#FFD54F"; fit_lbl="لائق مع قيود" if ar else "Fit with Restrictions"
        else: fit_icon="❌"; fit_color="#EF9A9A"; fit_lbl="غير لائق" if ar else "Unfit"

        bmi_color = "#81C784" if bmi_cat=="Normal" else "#FFD54F" if bmi_cat in ["Overweight","Underweight"] else "#EF9A9A"
        bmi_lbl = {"Normal":"طبيعي","Overweight":"وزن زائد","Obese":"سمنة","Underweight":"نقص وزن"}.get(bmi_cat,bmi_cat) if ar else bmi_cat

        hp1,hp2,hp3,hp4 = st.columns(4)
        with hp1:
            st.markdown(f'''<div style="background:#0F172A;border-radius:14px;padding:18px;text-align:center;border:1px solid #334155">
                <div style="font-size:11px;color:{C["text3"]};font-weight:700">{"العمر" if ar else "Age"}</div>
                <div style="font-size:32px;font-weight:900;color:{C["text1"]};margin:6px 0">{age}</div>
                <div style="font-size:12px;color:{C["text3"]}">{"سنة" if ar else "years"}</div>
            </div>''',unsafe_allow_html=True)
        with hp2:
            st.markdown(f'''<div style="background:#0F172A;border-radius:14px;padding:18px;text-align:center;border:1px solid #334155">
                <div style="font-size:11px;color:{C["text3"]};font-weight:700">{"الطول / الوزن" if ar else "Height / Weight"}</div>
                <div style="font-size:24px;font-weight:900;color:{C["text1"]};margin:6px 0">{height} <span style="font-size:13px;color:{C["text3"]}">cm</span></div>
                <div style="font-size:18px;font-weight:700;color:{C["text2"]}">{weight} kg</div>
            </div>''',unsafe_allow_html=True)
        with hp3:
            st.markdown(f'''<div style="background:#0F172A;border-radius:14px;padding:18px;text-align:center;border:1px solid #334155">
                <div style="font-size:11px;color:{C["text3"]};font-weight:700">{"مؤشر كتلة الجسم" if ar else "BMI"}</div>
                <div style="font-size:32px;font-weight:900;color:{bmi_color};margin:6px 0">{bmi}</div>
                <div style="font-size:12px;color:{bmi_color};font-weight:700">{bmi_lbl}</div>
            </div>''',unsafe_allow_html=True)
        with hp4:
            st.markdown(f'''<div style="background:#0F172A;border-radius:14px;padding:18px;text-align:center;border:2px solid {fit_color}">
                <div style="font-size:11px;color:{C["text3"]};font-weight:700">{"اللياقة المهنية" if ar else "Occupational Fitness"}</div>
                <div style="font-size:36px;margin:6px 0">{fit_icon}</div>
                <div style="font-size:16px;color:{fit_color};font-weight:800">{fit_lbl}</div>
            </div>''',unsafe_allow_html=True)

        exam_color = "#81C784" if exam_status=="Valid" else "#EF9A9A"
        lbl_last = "آخر فحص سنوي" if ar else "Last Annual Exam"
        lbl_next = "الفحص القادم" if ar else "Next Exam Due"
        lbl_expired = "— منتهي!" if ar else "— OVERDUE!"
        st.markdown(f'''<div style="display:flex;gap:12px;margin-top:14px;flex-wrap:wrap">
            <div style="background:#0F172A;border-radius:12px;padding:12px 18px;border:1px solid #334155;flex:1;display:flex;align-items:center;gap:8px">
                <span style="font-size:18px">📋</span>
                <div><div style="font-size:10px;color:{C["text3"]};font-weight:700">{lbl_last}</div><div style="font-size:14px;color:{C["text1"]};font-weight:700">{last_exam}</div></div>
            </div>
            <div style="background:#0F172A;border-radius:12px;padding:12px 18px;border:1px solid {exam_color};flex:1;display:flex;align-items:center;gap:8px">
                <span style="font-size:18px">{"⚠️" if exam_status=="Expired" else "📅"}</span>
                <div><div style="font-size:10px;color:{C["text3"]};font-weight:700">{lbl_next}</div><div style="font-size:14px;color:{exam_color};font-weight:700">{next_exam} {lbl_expired if exam_status=="Expired" else ""}</div></div>
            </div>
        </div>''', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Recommendations ──
        title_rec = "التوصيات" if ar else "Recommendations"
        st.markdown(f'<div class="panel"><div class="panel-title">💡 {title_rec}</div>', unsafe_allow_html=True)

        recs = []

        if isinstance(age,(int,float)) and age >= 50:
            en = "Age over 50 — Limit heat zone exposure to 4 hours max. Mandatory rest breaks every 45 minutes in hot zones."
            a2 = "العمر فوق 50 — يُمنع من العمل في مناطق الحرارة أكثر من 4 ساعات. استراحة إلزامية كل 45 دقيقة في المناطق الحارة."
            recs.append(("🔴", en, a2))
        elif isinstance(age,(int,float)) and age >= 45:
            en = "Age over 45 — Requires additional monitoring during heat zone shifts."
            a2 = "العمر فوق 45 — يحتاج مراقبة إضافية أثناء العمل في المناطق الحارة."
            recs.append(("🟡", en, a2))

        if bmi_cat == "Obese":
            en = "BMI over 30 (Obese) — Limit heat zone work to 3 hours per shift. Mandatory hydration every 30 minutes (500ml). Consider reassignment from high-heat zones."
            a2 = "مؤشر كتلة الجسم فوق 30 (سمنة) — يُمنع من العمل في مناطق الحرارة أكثر من 3 ساعات لكل وردية. شرب الماء إلزامي كل 30 دقيقة. يُنظر في نقله من المناطق شديدة الحرارة."
            recs.append(("🔴", en, a2))
        elif bmi_cat == "Overweight":
            en = "BMI 25-30 (Overweight) — Increase hydration in hot zones. Monitor during next periodic exam."
            a2 = "مؤشر كتلة الجسم 25-30 (وزن زائد) — زيادة شرب الماء في المناطق الحارة. متابعة في الفحص الدوري القادم."
            recs.append(("🟡", en, a2))

        if hearing == "Fail":
            en = "Hearing test failed — Must wear double hearing protection (earplugs + earmuffs) in all noise zones. Maximum 2 hours in Warning/Critical noise zones. Refer to ENT specialist."
            a2 = "فحص السمع: غير ناجح — يجب ارتداء حماية سمع مزدوجة (سدادات + غطاء أذن) في جميع مناطق الضوضاء. الحد الأقصى ساعتان في مناطق الضوضاء التحذيرية والحرجة. تحويل لأخصائي أنف وأذن وحنجرة."
            recs.append(("🔴", en, a2))
        elif hearing == "Partial Loss":
            en = "Partial hearing loss detected — Mandatory ear protection in all noise zones. Hearing test every 6 months. Maximum 4 hours in zones above 80 dBA."
            a2 = "تم اكتشاف ضعف سمع جزئي — حماية الأذن إلزامية في جميع مناطق الضوضاء. فحص سمع كل 6 أشهر. الحد الأقصى 4 ساعات في المناطق فوق 80 ديسيبل."
            recs.append(("🟡", en, a2))

        if lung == "Reduced":
            en = "Reduced lung function — Mandatory respiratory PPE (N95 minimum) in Gas and CO₂ zones. Maximum 2 hours in Gas Warning zones. Prohibited from entering Critical gas zones."
            a2 = "وظائف الرئة منخفضة — معدات حماية الجهاز التنفسي إلزامية (N95 كحد أدنى) في مناطق الغاز وثاني أكسيد الكربون. الحد الأقصى ساعتان في مناطق الغاز التحذيرية. يُمنع من دخول مناطق الغاز الحرجة."
            recs.append(("🔴", en, a2))

        if fitness == "Unfit":
            en = "Classified as UNFIT — Must be reassigned to low-risk zones only. Prohibited from high-heat, high-noise, and confined space work. Re-evaluation required within 3 months."
            a2 = "مصنّف: غير لائق — يجب نقله إلى مناطق منخفضة المخاطر فقط. يُمنع من العمل في الحرارة العالية والضوضاء العالية والأماكن المغلقة. إعادة تقييم خلال 3 أشهر."
            recs.append(("🔴", en, a2))

        if exam_status == "Expired":
            en = "URGENT: Annual medical exam has expired. Worker must complete the periodic medical examination before continuing work in high-risk zones. Schedule immediately."
            a2 = "عاجل: الفحص الطبي السنوي منتهي الصلاحية. يجب على العامل إكمال الفحص الطبي الدوري قبل الاستمرار في العمل بالمناطق عالية المخاطر. يجب الجدولة فوراً."
            recs.append(("🔴", en, a2))

        cv_zones=[z for z in zvs if zoverall(z)=="Critical"] if len(wp)>0 else []
        if cv_zones:
            zn2 = ", ".join([zname(z) for z in cv_zones])
            en = f"Currently assigned to Critical zone(s): {zn2} — Ensure all required PPE is worn. Rotate with workers from safe zones. Document all exposure hours."
            a2 = f"يعمل حالياً في منطقة/مناطق حرجة: {zn2} — التأكد من ارتداء جميع معدات الحماية المطلوبة. التناوب مع عمال من مناطق آمنة. توثيق جميع ساعات التعرض."
            recs.append(("🔴", en, a2))

        if not recs:
            en = "All indicators within normal limits. Continue standard work schedule. Next periodic exam as scheduled."
            a2 = "جميع المؤشرات ضمن الحدود الطبيعية. يستمر في جدول العمل العادي. الفحص الدوري القادم في موعده."
            recs.append(("🟢", en, a2))

        for icon, en_text, ar_text in recs:
            text = ar_text if ar else en_text
            direction = "rtl" if ar else "ltr"
            align = "right" if ar else "left"
            border_side = "border-right" if ar else "border-left"
            bg = "#4A0E0E" if icon=="🔴" else "#4E3A00" if icon=="🟡" else "#1B3A1B"
            border = "#C62828" if icon=="🔴" else "#F57F17" if icon=="🟡" else "#2E7D32"
            st.markdown(f'''<div style="background:{bg};{border_side}:4px solid {border};border-radius:12px;padding:14px 18px;margin-bottom:8px;direction:{direction};text-align:{align}">
                <span style="font-size:16px;{"margin-left" if ar else "margin-right"}:8px">{icon}</span>
                <span style="color:{C["text1"]};font-size:14px;font-weight:600">{text}</span>
            </div>''', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No health data available.")

    # ── Exposure KPIs ──
    w1,w2,w3=st.columns(3)
    with w1: st.markdown(rmkpi("⏱️","Total Hours",f"{tth:.1f} hrs",C["safe_bg"]),unsafe_allow_html=True)
    with w2: st.markdown(rmkpi("🏭","Zones Visited",len(zvs),C["safe_bg"]),unsafe_allow_html=True)
    with w3: st.markdown(rmkpi(sicon(rs),"Risk Status",rl,sbg(rs)),unsafe_allow_html=True)
    st.markdown("<div style='height:16px'></div>",unsafe_allow_html=True)
    wd1,wd2=st.columns(2)
    with wd1:
        st.markdown(f'<div class="panel"><div class="panel-title">{"📋 سجل الزيارات" if AR else "📋 Visit Log"}</div>',unsafe_allow_html=True)
        if len(wp)>0:
            t='<table class="styled-table"><tr><th>Zone</th><th>Entry</th><th>Exit</th><th>Duration</th><th>Status</th></tr>'
            for _,p in wp.iterrows():
                zn=zname(p["ZoneID"]);ent=p["EntryDateTime"].strftime("%Y-%m-%d %H:%M") if pd.notna(p["EntryDateTime"]) else "N/A"
                ext=p["ExitDateTime"].strftime("%H:%M") if pd.notna(p["ExitDateTime"]) else "N/A"
                dur=f"{p['Hours']:.1f} hrs" if "Hours" in p and pd.notna(p.get("Hours")) else "N/A";zs=zoverall(p["ZoneID"])
                t+=f'<tr><td style="color:{C["text1"]}!important;font-weight:700">{zn}</td><td style="color:{C["text2"]}!important">{ent}</td><td style="color:{C["text2"]}!important">{ext}</td><td style="color:{C["text1"]}!important;font-weight:600">{dur}</td><td><span class="kpi-status status-{scss(zs)}">{zs}</span></td></tr>'
            t+='</table>';st.markdown(t,unsafe_allow_html=True)
        else: st.info("No records.")
        st.markdown("</div>",unsafe_allow_html=True)
    with wd2:
        st.markdown(f'<div class="panel"><div class="panel-title">{"📊 ملخص التعرض" if AR else "📊 Exposure Summary"}</div>',unsafe_allow_html=True)
        if len(wp)>0:
            he={h:[] for h in HO}
            for _,p in wp.iterrows():
                zs2=zhstats(p["ZoneID"]);hrs=p.get("Hours",0)
                for s in zs2: he[s["HazardType"]].append({"e":s["ExposurePct"],"h":hrs if pd.notna(hrs) else 0})
            ed=[]
            for h in HO:
                items=he[h]
                if items:
                    th=sum(i["h"] for i in items)
                    wa=sum(i["e"]*i["h"] for i in items)/th if th>0 else np.mean([i["e"] for i in items])
                    ed.append({"Hazard":HD.get(h,h),"Exp":wa*100})
            edf=pd.DataFrame(ed);colors=["#C62828" if v>=100 else "#F9A825" if v>=80 else "#2E7D32" for v in edf["Exp"]]
            fig=go.Figure();fig.add_trace(go.Bar(x=edf["Hazard"],y=edf["Exp"],marker_color=colors,text=[f"{v:.0f}%" for v in edf["Exp"]],textposition="outside"))
            fig.add_hline(y=100,line_dash="dash",line_color="#C62828",line_width=2)
            fig.update_layout(**PL,height=320,yaxis_title="Exposure %",showlegend=False,yaxis=dict(gridcolor=C["grid"],range=[0,max(edf["Exp"].max()*1.2,130)]))
            st.plotly_chart(fig,use_container_width=True)
        else: st.info("No data.")
        st.markdown("</div>",unsafe_allow_html=True)
    st.markdown(f'<div class="panel"><div class="panel-title">{"📖 ساعات التعرض المسموحة" if AR else "📖 Allowed Exposure Hours"}</div>',unsafe_allow_html=True)
    t='<table class="styled-table"><tr><th>Hazard</th><th>Max Daily</th><th>Break</th></tr>'
    for _,r in allowed_hours_df.iterrows():
        t+=f'<tr><td style="color:{C["text1"]}!important;font-weight:700">{HI.get(r["HazardType"],"📊")} {HD.get(r["HazardType"],r["HazardType"])}</td><td style="color:{C["text2"]}!important">{r["MaxDailyHours"]} hrs</td><td style="color:{C["text2"]}!important">{r["RecommendedBreak"]}</td></tr>'
    t+='</table></div>';st.markdown(t,unsafe_allow_html=True)

# ═══════════════ TAB 6: ALERTS ═══════════════
with tab6:
    st.markdown(f'<div class="panel"><div class="panel-title">{"🚨 مركز التنبيهات" if AR else "🚨 Alert Center"}</div>',unsafe_allow_html=True)
    alerts_df=gen_alerts()
    if len(alerts_df)>0:
        af1,af2,af3=st.columns(3)
        with af1: a_st=st.selectbox("Status",["All","Critical","Warning"],key="ast")
        with af2: a_zn=st.selectbox("Zone",["All"]+zones_df["ZoneName"].tolist(),key="azn")
        with af3: a_hz=st.selectbox("Hazard",["All"]+[HD.get(h,h) for h in HO],key="ahz")
        filt=alerts_df.copy()
        if a_st!="All": filt=filt[filt["Status"]==a_st]
        if a_zn!="All": filt=filt[filt["Zone"]==a_zn]
        if a_hz!="All":
            hk=next((k for k,v in HD.items() if v==a_hz),a_hz);filt=filt[filt["Hazard"]==hk]
        ak1,ak2,ak3,ak4=st.columns(4)
        with ak1: st.markdown(rmkpi("📊","Total",len(filt),C["safe_bg"]),unsafe_allow_html=True)
        with ak2: st.markdown(rmkpi("🚨","Critical",len(filt[filt["Status"]=="Critical"]),C["crit_bg"]),unsafe_allow_html=True)
        with ak3: st.markdown(rmkpi("⚠️","Warning",len(filt[filt["Status"]=="Warning"]),C["warn_bg"]),unsafe_allow_html=True)
        with ak4: st.markdown(rmkpi("🏭","Zones",filt["Zone"].nunique(),C["safe_bg"]),unsafe_allow_html=True)
        st.markdown("<div style='height:16px'></div>",unsafe_allow_html=True)
        al1,al2=st.columns([6,4])
        with al1:
            st.markdown(f'<div class="panel"><div class="panel-title">📅 Alerts Timeline</div>',unsafe_allow_html=True)
            fc=filt.copy();fc["Date"]=fc["DateTime"].dt.date
            daily=fc.groupby(["Date","Status"]).size().reset_index(name="Count")
            fig=go.Figure()
            for sn,sc2 in [("Critical","#C62828"),("Warning","#F9A825")]:
                sd2=daily[daily["Status"]==sn]
                if len(sd2)>0: fig.add_trace(go.Bar(x=sd2["Date"],y=sd2["Count"],name=sn,marker_color=sc2))
            fig.update_layout(**PL,height=300,barmode="stack",yaxis_title="Count",yaxis=dict(gridcolor=C["grid"]),legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("</div>",unsafe_allow_html=True)
        with al2:
            st.markdown(f'<div class="panel"><div class="panel-title">📊 By Hazard</div>',unsafe_allow_html=True)
            hzc=filt.groupby("Hazard").size().reset_index(name="Count");hzc["Label"]=hzc["Hazard"].map(HD)
            fig=go.Figure(data=[go.Pie(labels=hzc["Label"],values=hzc["Count"],hole=0.5,marker_colors=["#1565C0","#E65100","#6A1B9A","#2E7D32"][:len(hzc)],textinfo="label+value",textfont=dict(size=12,color="#FFF"))])
            fig.update_layout(**PL,height=300,showlegend=False)
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("</div>",unsafe_allow_html=True)
        st.markdown(f'<div class="panel"><div class="panel-title">📜 Log (latest 30)</div>',unsafe_allow_html=True)
        for _,a in filt.head(30).iterrows():
            ic="warn-item" if a["Status"]=="Warning" else ""
            dt2=a["DateTime"].strftime("%Y-%m-%d %H:%M") if pd.notna(a["DateTime"]) else ""
            st.markdown(f'<div class="alert-item {ic}"><div style="min-width:90px;font-size:11px;color:{C["text3"]};font-weight:600">{dt2}</div><div style="font-size:13px;color:{C["text1"]};font-weight:600">{HI.get(a["Hazard"],"")} {a["Zone"]} — {HD.get(a["Hazard"],a["Hazard"])}: {a["Value"]} ({a["ExposurePct"]:.0%})</div><div style="margin-left:auto"><span class="kpi-status status-{scss(a["Status"])}">{a["Status"]}</span></div></div>',unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)
    else: st.success("✅ No alerts!")
    st.markdown("</div>",unsafe_allow_html=True)

    # ── Worker Violation Alerts ──
    st.markdown(f'<div class="panel"><div class="panel-title">{"👷 تنبيهات العمال — تجاوز الحدود المسموحة" if AR else "👷 Worker Violation Alerts — Exceeded Exposure Limits"}</div>', unsafe_allow_html=True)

    worker_violations = []
    for _, w in workers_df.iterrows():
        wid = w["WorkerID"]
        wp2 = presence_df[presence_df["WorkerID"]==wid]
        if len(wp2) == 0: continue
        wh_r = health_df[health_df["WorkerID"]==wid].iloc[0] if len(health_df)>0 and wid in health_df["WorkerID"].values else None

        for _, p in wp2.iterrows():
            zs = zhstats(p["ZoneID"])
            z_name = zname(p["ZoneID"])
            for s in zs:
                if s["Status"] in ["Warning", "Critical"]:
                    reasons = []
                    if wh_r is not None:
                        if s["HazardType"] == "Noise" and wh_r.get("HearingTest") in ["Fail","Partial Loss"]:
                            reasons.append("🔊 " + ("ضعف سمع" if AR else "Hearing impaired"))
                        if s["HazardType"] == "HeatIndex":
                            age = wh_r.get("Age",30)
                            if isinstance(age,(int,float)) and age >= 45:
                                reasons.append("🎂 " + (f"عمره {age}" if AR else f"Age {age}"))
                            if wh_r.get("BMICategory") == "Obese":
                                reasons.append("⚖️ " + ("سمنة" if AR else "Obese"))
                        if s["HazardType"] in ["Gas","CO2"] and wh_r.get("LungFunction") == "Reduced":
                            reasons.append("🫁 " + ("ضعف تنفس" if AR else "Reduced lung"))
                        if wh_r.get("FitnessLevel") == "Unfit":
                            reasons.append("❌ " + ("غير لائق" if AR else "Unfit"))

                    worker_violations.append({
                        "name": w["FullName"], "job": w["JobTitle"], "zone": z_name,
                        "hazard": s["DisplayName"], "icon": s["Icon"],
                        "value": s["CurrentValue"], "unit": s["Unit"],
                        "limit": s["Limit"], "exp": s["ExposurePct"],
                        "status": s["Status"], "reasons": reasons
                    })

    if worker_violations:
        # Summary
        n_crit_w = len([v for v in worker_violations if v["status"]=="Critical"])
        n_warn_w = len([v for v in worker_violations if v["status"]=="Warning"])
        unique_workers = len(set(v["name"] for v in worker_violations))
        vk1,vk2,vk3 = st.columns(3)
        with vk1: st.markdown(rmkpi("👷", "عمال متأثرين" if AR else "Workers Affected", unique_workers, C["crit_bg"]), unsafe_allow_html=True)
        with vk2: st.markdown(rmkpi("🚨", "حرج" if AR else "Critical", n_crit_w, C["crit_bg"]), unsafe_allow_html=True)
        with vk3: st.markdown(rmkpi("⚠️", "تحذير" if AR else "Warning", n_warn_w, C["warn_bg"]), unsafe_allow_html=True)

        # Worker cards
        seen = set()
        for v in worker_violations:
            key = f"{v['name']}_{v['zone']}_{v['hazard']}"
            if key in seen: continue
            seen.add(key)

            vc = "#C62828" if v["status"]=="Critical" else "#F9A825"
            vbg = "#4A0E0E" if v["status"]=="Critical" else "#4E3A00"
            reason_txt = " · ".join(v["reasons"]) if v["reasons"] else ("لا توجد عوامل صحية إضافية" if AR else "No additional health factors")
            health_flag = "🔴" if v["reasons"] else "🟢"

            d = "rtl" if AR else "ltr"
            a = "right" if AR else "left"
            st.markdown(f'''<div style="background:{vbg};border-left:4px solid {vc};border-radius:12px;padding:14px 18px;margin-bottom:8px;direction:{d};text-align:{a}">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
                    <div>
                        <span style="color:{C["text1"]};font-size:15px;font-weight:800">👤 {v["name"]}</span>
                        <span style="color:{C["text3"]};font-size:12px;margin:0 8px">({v["job"]})</span>
                    </div>
                    <span class="kpi-status status-{scss(v["status"])}">{v["status"]}</span>
                </div>
                <div style="color:{C["text2"]};font-size:13px;margin-top:6px">
                    🏭 {v["zone"]} — {v["icon"]} {v["hazard"]}: <strong style="color:{vc}">{v["value"]} {v["unit"]}</strong>
                    {"(الحد" if AR else "(Limit"}: {v["limit"]}) — {"التعرض" if AR else "Exposure"}: <strong style="color:{vc}">{v["exp"]:.0%}</strong>
                </div>
                <div style="color:{C["text3"]};font-size:12px;margin-top:4px">{health_flag} {"عوامل صحية" if AR else "Health factors"}: {reason_txt}</div>
            </div>''', unsafe_allow_html=True)

    else:
        st.markdown(f'''<div style="background:#1B3A1B;border-radius:12px;padding:20px;text-align:center">
            <div style="font-size:36px">✅</div>
            <div style="color:#81C784;font-size:16px;font-weight:700">{"لا يوجد عمال تجاوزوا الحدود" if AR else "No workers exceeding exposure limits"}</div>
        </div>''', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════ TAB 7: EXECUTIVE DASHBOARD ═══════════════
with tab7:
    st.markdown(f'<div class="panel"><div class="panel-title">{"🎯 لوحة القيادة التنفيذية" if AR else "🎯 Executive Dashboard — Plant Safety Overview"}</div>', unsafe_allow_html=True)

    # Calculate plant-wide health compliance score
    all_stats = zhstats()
    max_exps = []
    for _, z in zones_df.iterrows():
        zs = zhstats(z["ZoneID"])
        mx = max(s["ExposurePct"] for s in zs) if zs else 0
        max_exps.append(mx)
    avg_exp = np.mean(max_exps) if max_exps else 0
    # Safety score: 100 = all safe, 0 = all at 200%+. Cap exposure at 2.0 for scoring
    capped_exps = [min(e, 2.0) for e in max_exps]
    avg_capped = np.mean(capped_exps) if capped_exps else 0
    safety_score = max(0, round((1 - avg_capped / 2.0) * 100))

    # Safety Score Gauge
    sc_color = "#81C784" if safety_score >= 70 else "#FFD54F" if safety_score >= 40 else "#EF9A9A"
    sc_label = ("ممتاز" if safety_score>=80 else "جيد" if safety_score>=60 else "تحذير" if safety_score>=40 else "خطر") if AR else ("Excellent" if safety_score>=80 else "Good" if safety_score>=60 else "Warning" if safety_score>=40 else "Critical")

    st.markdown(f'''<div style="text-align:center;padding:20px 0">
        <div style="display:inline-block;width:220px;height:220px;border-radius:50%;border:12px solid {sc_color};position:relative;box-shadow:0 0 40px {sc_color}40">
            <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%)">
                <div style="font-size:56px;font-weight:900;color:{sc_color}">{safety_score}</div>
                <div style="font-size:14px;color:{C["text3"]};font-weight:700">{"درجة الامتثال الصحي" if AR else "HEALTH COMPLIANCE"}</div>
                <div style="font-size:16px;color:{sc_color};font-weight:800;margin-top:4px">{sc_label}</div>
            </div>
        </div>
    </div>''', unsafe_allow_html=True)

    # Reference legend
    if AR:
        ref_rows = '''<tr><td style="color:#81C784;font-weight:800">80 — 100</td><td style="color:#81C784;font-weight:700">ممتاز</td><td style="color:{t3}">جميع المناطق ضمن الحدود المسموحة</td></tr>
        <tr><td style="color:#4FC3F7;font-weight:800">60 — 79</td><td style="color:#4FC3F7;font-weight:700">جيد</td><td style="color:{t3}">أغلب المناطق آمنة مع مراقبة بسيطة</td></tr>
        <tr><td style="color:#FFD54F;font-weight:800">40 — 59</td><td style="color:#FFD54F;font-weight:700">تحذير</td><td style="color:{t3}">بعض المناطق تقترب من الحدود — يحتاج تدخل</td></tr>
        <tr><td style="color:#EF9A9A;font-weight:800">0 — 39</td><td style="color:#EF9A9A;font-weight:700">خطر</td><td style="color:{t3}">تجاوزات متعددة — إجراء فوري مطلوب</td></tr>'''.format(t3=C["text3"])
        ref_title = "📖 مرجع درجة الامتثال الصحي"
        ref_h1 = "الدرجة"; ref_h2 = "التصنيف"; ref_h3 = "الوصف"
    else:
        ref_rows = '''<tr><td style="color:#81C784;font-weight:800">80 — 100</td><td style="color:#81C784;font-weight:700">Excellent</td><td style="color:{t3}">All zones within permissible exposure limits</td></tr>
        <tr><td style="color:#4FC3F7;font-weight:800">60 — 79</td><td style="color:#4FC3F7;font-weight:700">Good</td><td style="color:{t3}">Most zones safe with minor monitoring needed</td></tr>
        <tr><td style="color:#FFD54F;font-weight:800">40 — 59</td><td style="color:#FFD54F;font-weight:700">Warning</td><td style="color:{t3}">Some zones approaching limits — intervention needed</td></tr>
        <tr><td style="color:#EF9A9A;font-weight:800">0 — 39</td><td style="color:#EF9A9A;font-weight:700">Critical</td><td style="color:{t3}">Multiple limit exceedances — immediate action required</td></tr>'''.format(t3=C["text3"])
        ref_title = "📖 Health Compliance Score Reference"
        ref_h1 = "Score"; ref_h2 = "Rating"; ref_h3 = "Description"

    st.markdown(f'''<div style="background:#0F172A;border:1px solid #334155;border-radius:14px;padding:16px 20px;margin:12px auto;max-width:600px">
        <div style="color:{C["accent"]};font-size:13px;font-weight:700;margin-bottom:10px;text-align:center">{ref_title}</div>
        <table style="width:100%;border-collapse:collapse">
            <tr><th style="color:{C["text3"]};font-size:11px;padding:6px 8px;text-align:left;border-bottom:1px solid #334155">{ref_h1}</th>
                <th style="color:{C["text3"]};font-size:11px;padding:6px 8px;text-align:left;border-bottom:1px solid #334155">{ref_h2}</th>
                <th style="color:{C["text3"]};font-size:11px;padding:6px 8px;text-align:left;border-bottom:1px solid #334155">{ref_h3}</th></tr>
            {ref_rows}
        </table>
    </div>''', unsafe_allow_html=True)

    # Key metrics row
    n_crit = sum(1 for e in max_exps if e >= 1.0)
    n_warn = sum(1 for e in max_exps if 0.8 <= e < 1.0)
    n_safe = sum(1 for e in max_exps if e < 0.8)
    w_at_risk = 0
    for wid in workers_df["WorkerID"]:
        wp2 = presence_df[presence_df["WorkerID"]==wid]
        for _, p in wp2.iterrows():
            if zoverall(p["ZoneID"]) == "Critical": w_at_risk += 1; break

    e1,e2,e3,e4,e5,e6 = st.columns(6)
    with e1: st.markdown(rmkpi("🏭", "المناطق" if AR else "Total Zones", len(zones_df), C["safe_bg"]), unsafe_allow_html=True)
    with e2: st.markdown(rmkpi("✅", "آمنة" if AR else "Safe", n_safe, C["safe_bg"]), unsafe_allow_html=True)
    with e3: st.markdown(rmkpi("⚠️", "تحذير" if AR else "Warning", n_warn, C["warn_bg"]), unsafe_allow_html=True)
    with e4: st.markdown(rmkpi("🚨", "حرجة" if AR else "Critical", n_crit, C["crit_bg"]), unsafe_allow_html=True)
    with e5: st.markdown(rmkpi("👷", "العمال" if AR else "Workers", len(workers_df), C["safe_bg"]), unsafe_allow_html=True)
    with e6: st.markdown(rmkpi("⚠️", "معرضون" if AR else "At Risk", w_at_risk, C["crit_bg"]), unsafe_allow_html=True)

    # Most dangerous zone + most exposed worker
    ex1, ex2 = st.columns(2)
    worst_idx = np.argmax(max_exps)
    worst_zone = zones_df.iloc[worst_idx]
    worst_exp = max_exps[worst_idx]
    with ex1:
        wz_st = gstat(worst_exp)
        st.markdown(f'''<div class="panel" style="border-left:4px solid {stxt(wz_st)}">
            <div style="font-size:12px;color:{C["text3"]};font-weight:700">{"🔴 أخطر منطقة" if AR else "🔴 Most Dangerous Zone"}</div>
            <div style="font-size:22px;font-weight:900;color:{C["text1"]};margin:6px 0">{worst_zone["ZoneName"]}</div>
            <div style="font-size:14px;color:{stxt(wz_st)};font-weight:700">{"التعرض" if AR else "Exposure"}: {worst_exp:.0%} — {wz_st}</div>
        </div>''', unsafe_allow_html=True)

    # Most exposed worker
    with ex2:
        w_exps = []
        for _, w in workers_df.iterrows():
            wp2 = presence_df[presence_df["WorkerID"]==w["WorkerID"]]
            if len(wp2) > 0:
                zone_exps = [max(s["ExposurePct"] for s in zhstats(p["ZoneID"])) for _, p in wp2.iterrows()]
                w_exps.append({"name": w["FullName"], "job": w["JobTitle"], "exp": max(zone_exps)})
        if w_exps:
            top_w = max(w_exps, key=lambda x: x["exp"])
            tw_st = gstat(top_w["exp"])
            st.markdown(f'''<div class="panel" style="border-left:4px solid {stxt(tw_st)}">
                <div style="font-size:12px;color:{C["text3"]};font-weight:700">{"👷 أكثر عامل تعرضاً" if AR else "👷 Most Exposed Worker"}</div>
                <div style="font-size:22px;font-weight:900;color:{C["text1"]};margin:6px 0">{top_w["name"]}</div>
                <div style="font-size:14px;color:{stxt(tw_st)};font-weight:700">{top_w["job"]} — {top_w["exp"]:.0%} {tw_st}</div>
            </div>''', unsafe_allow_html=True)

    # Zone ranking bar chart
    st.markdown(f'<div style="margin-top:16px;color:{C["accent"]};font-size:14px;font-weight:700">{"📊 ترتيب المناطق حسب الخطورة" if AR else "📊 Zone Risk Ranking"}</div>', unsafe_allow_html=True)
    zrank = pd.DataFrame({"Zone": [z["ZoneName"] for _,z in zones_df.iterrows()], "Exposure": [e*100 for e in max_exps]}).sort_values("Exposure", ascending=True)
    colors_r = ["#C62828" if v>=100 else "#F9A825" if v>=80 else "#2E7D32" for v in zrank["Exposure"]]
    fig_r = go.Figure(go.Bar(x=zrank["Exposure"], y=zrank["Zone"], orientation="h", marker_color=colors_r, text=[f"{v:.0f}%" for v in zrank["Exposure"]], textposition="outside"))
    fig_r.add_vline(x=100, line_dash="dash", line_color="#C62828", line_width=2)
    fig_r.update_layout(plot_bgcolor=C["bg"], paper_bgcolor=C["bg"], font=dict(color=C["text2"]), height=300, xaxis_title="Exposure %", yaxis=dict(gridcolor=C["grid"]), margin=dict(l=10,r=10,t=10,b=40))
    st.plotly_chart(fig_r, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════ TAB 9: HEAT STRESS CALCULATOR ═══════════════
with tab9:
    st.markdown(f'<div class="panel"><div class="panel-title">{"🌡️ حاسبة الإجهاد الحراري — قرار حظر العمل" if AR else "🌡️ Heat Stress Calculator — NCOSH Work Ban Compliance"}</div>', unsafe_allow_html=True)

    st.markdown(f'''<div style="background:#4E3A00;border:1px solid #F57F17;border-radius:12px;padding:16px;margin-bottom:16px">
        <div style="color:#FFD54F;font-size:13px;font-weight:700">{"📋 قرار حظر العمل تحت أشعة الشمس — المجلس الوطني للسلامة والصحة المهنية" if AR else "📋 NCOSH Sun Work Ban — June 15 to September 15, 12:00 PM to 3:00 PM"}</div>
        <div style="color:{C["text2"]};font-size:12px;margin-top:6px">{"يُمنع العمل تحت أشعة الشمس من 15 يونيو إلى 15 سبتمبر، من الساعة 12 ظهراً إلى 3 عصراً" if AR else "All outdoor work is prohibited under direct sunlight during this period per NCOSH regulations."}</div>
    </div>''', unsafe_allow_html=True)

    # Check if currently in ban period
    month = datetime.now().month
    hour = datetime.now().hour
    in_ban_period = month in [6,7,8,9] or (month == 6 and datetime.now().day >= 15) or (month == 9 and datetime.now().day <= 15)
    in_ban_hours = 12 <= hour < 15

    if in_ban_period and in_ban_hours:
        st.markdown(f'''<div style="background:#C62828;border-radius:16px;padding:24px;text-align:center;animation:pulse 2s infinite">
            <div style="font-size:48px">🚫</div>
            <div style="color:white;font-size:22px;font-weight:900;margin:8px 0">{"العمل الخارجي محظور الآن!" if AR else "OUTDOOR WORK CURRENTLY BANNED!"}</div>
            <div style="color:#EF9A9A;font-size:14px">12:00 PM — 3:00 PM</div>
        </div>''', unsafe_allow_html=True)
    elif in_ban_period:
        st.markdown(f'''<div style="background:#4E3A00;border-radius:16px;padding:20px;text-align:center">
            <div style="font-size:36px">⚠️</div>
            <div style="color:#FFD54F;font-size:18px;font-weight:800">{"فترة حظر نشطة — العمل الخارجي ممنوع 12-3" if AR else "Ban Period Active — Outdoor work prohibited 12-3 PM"}</div>
        </div>''', unsafe_allow_html=True)
    else:
        st.markdown(f'''<div style="background:#1B3A1B;border-radius:16px;padding:20px;text-align:center">
            <div style="font-size:36px">✅</div>
            <div style="color:#81C784;font-size:18px;font-weight:800">{"خارج فترة الحظر — العمل الخارجي مسموح" if AR else "Outside Ban Period — Outdoor work permitted"}</div>
        </div>''', unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # WBGT Calculator
    st.markdown(f'<div style="color:{C["accent"]};font-size:14px;font-weight:700;margin-bottom:12px">{"🔬 حاسبة مؤشر الحرارة — OSHA/NWS" if AR else "🔬 Heat Index Calculator (OSHA/NWS Rothfusz Equation)"}</div>', unsafe_allow_html=True)

    hc1, hc2, hc3 = st.columns(3)
    with hc1:
        temp_c = st.number_input("🌡️ Temperature (°C)" if not AR else "🌡️ درجة الحرارة (°C)", 0.0, 60.0, 0.0, 1.0, key="wbgt_t")
    with hc2:
        humidity = st.number_input("💧 Humidity (%)" if not AR else "💧 الرطوبة (%)", 0.0, 100.0, 0.0, 5.0, key="wbgt_h")
    with hc3:
        sun = st.selectbox("☀️ Sun Exposure" if not AR else "☀️ التعرض للشمس", ["Direct Sun", "Shade", "Indoor"], key="wbgt_s")

    # NWS/OSHA Heat Index (Rothfusz regression equation)
    # Convert to Fahrenheit for the formula
    T = temp_c * 9/5 + 32  # °F
    RH = humidity

    # Simple formula for low HI
    HI_simple = 0.5 * (T + 61.0 + ((T - 68.0) * 1.2) + (RH * 0.094))

    if HI_simple >= 80:
        # Full Rothfusz regression
        HI = (-42.379
              + 2.04901523 * T
              + 10.14333127 * RH
              - 0.22475541 * T * RH
              - 0.00683783 * T * T
              - 0.05481717 * RH * RH
              + 0.00122874 * T * T * RH
              + 0.00085282 * T * RH * RH
              - 0.00000199 * T * T * RH * RH)

        # Adjustments
        if RH < 13 and 80 < T < 112:
            HI -= ((13 - RH) / 4) * math.sqrt((17 - abs(T - 95)) / 17)
        elif RH > 85 and 80 < T < 87:
            HI += ((RH - 85) / 10) * ((87 - T) / 5)
    else:
        HI = HI_simple

    # Convert back to Celsius
    heat_index_c = round((HI - 32) * 5/9, 1)

    # Sun exposure adjustment (OSHA recommends +15°F for direct sun)
    sun_add_f = 15 if sun=="Direct Sun" else 5 if sun=="Shade" else 0
    sun_add_c = round(sun_add_f * 5/9, 1)
    heat_index_c = round(heat_index_c + sun_add_c, 1)

    # Show placeholder if inputs are 0
    if temp_c == 0 and humidity == 0:
        st.markdown(f'''<div style="text-align:center;padding:20px">
            <div style="display:inline-block;background:#0F172A;border:4px solid {C["text3"]};border-radius:20px;padding:30px 50px">
                <div style="font-size:14px;color:{C["text3"]};font-weight:700">{"مؤشر الحرارة" if AR else "HEAT INDEX"} (OSHA/NWS)</div>
                <div style="font-size:48px;font-weight:900;color:{C["text3"]}">—</div>
                <div style="font-size:14px;color:{C["text3"]};margin:4px 0">{"أدخل القيم أعلاه" if AR else "Enter values above"}</div>
            </div>
        </div>''', unsafe_allow_html=True)
    else:
        # OSHA risk categories based on Heat Index
        if heat_index_c >= 54: hi_level = "Extreme Danger"; hi_color = "#C62828"; hi_ar = "خطر شديد جداً"
        elif heat_index_c >= 41: hi_level = "Danger"; hi_color = "#E65100"; hi_ar = "خطر"
        elif heat_index_c >= 33: hi_level = "Extreme Caution"; hi_color = "#F57F17"; hi_ar = "حذر شديد"
        elif heat_index_c >= 27: hi_level = "Caution"; hi_color = "#81C784"; hi_ar = "حذر"
        else: hi_level = "Safe"; hi_color = "#4FC3F7"; hi_ar = "آمن"

        st.markdown(f'''<div style="text-align:center;padding:20px">
            <div style="display:inline-block;background:#0F172A;border:4px solid {hi_color};border-radius:20px;padding:30px 50px;box-shadow:0 0 30px {hi_color}30">
                <div style="font-size:14px;color:{C["text3"]};font-weight:700">{"مؤشر الحرارة" if AR else "HEAT INDEX"} (OSHA/NWS)</div>
                <div style="font-size:48px;font-weight:900;color:{hi_color}">{heat_index_c}°C</div>
                <div style="font-size:14px;color:{C["text3"]};margin:4px 0">({round(HI + sun_add_f)}°F)</div>
                <div style="font-size:16px;color:{hi_color};font-weight:800">{hi_ar if AR else hi_level}</div>
            </div>
        </div>''', unsafe_allow_html=True)

    # OSHA Reference table
    st.markdown(f'''<div style="background:#0F172A;border:1px solid #334155;border-radius:14px;padding:14px 18px;margin:12px auto;max-width:550px">
        <div style="color:{C["accent"]};font-size:12px;font-weight:700;margin-bottom:8px;text-align:center">{"📖 مرجع OSHA — مستويات مؤشر الحرارة" if AR else "📖 OSHA Heat Index Reference"}</div>
        <table style="width:100%;border-collapse:collapse;font-size:12px">
            <tr><td style="color:#4FC3F7;padding:4px 8px;font-weight:700">{"أقل من" if AR else "Below"} 27°C (80°F)</td><td style="color:#4FC3F7">{"آمن" if AR else "Safe"}</td></tr>
            <tr><td style="color:#81C784;padding:4px 8px;font-weight:700">27 — 32°C (80-90°F)</td><td style="color:#81C784">{"حذر" if AR else "Caution"}</td></tr>
            <tr><td style="color:#FFD54F;padding:4px 8px;font-weight:700">33 — 40°C (91-103°F)</td><td style="color:#FFD54F">{"حذر شديد" if AR else "Extreme Caution"}</td></tr>
            <tr><td style="color:#E65100;padding:4px 8px;font-weight:700">41 — 54°C (104-125°F)</td><td style="color:#E65100">{"خطر" if AR else "Danger"}</td></tr>
            <tr><td style="color:#EF9A9A;padding:4px 8px;font-weight:700">{"أكثر من" if AR else "Above"} 54°C (125°F)</td><td style="color:#EF9A9A">{"خطر شديد جداً" if AR else "Extreme Danger"}</td></tr>
        </table>
    </div>''', unsafe_allow_html=True)

    # Work/rest schedule based on WBGT
    st.markdown(f'<div style="color:{C["accent"]};font-size:14px;font-weight:700;margin:16px 0">{"📋 جدول العمل والراحة المقترح" if AR else "📋 Recommended Work/Rest Schedule"}</div>', unsafe_allow_html=True)

    work_cats = [
        ("Light Work" if not AR else "عمل خفيف", "Control room, monitoring", 75 if heat_index_c<33 else 50 if heat_index_c<41 else 25 if heat_index_c<54 else 0),
        ("Moderate Work" if not AR else "عمل متوسط", "Maintenance, inspection", 75 if heat_index_c<30 else 50 if heat_index_c<36 else 25 if heat_index_c<41 else 0),
        ("Heavy Work" if not AR else "عمل شاق", "Equipment install, manual labor", 50 if heat_index_c<30 else 25 if heat_index_c<33 else 0),
    ]

    for cat_name, cat_desc, work_pct in work_cats:
        rest_pct = 100 - work_pct
        bar_color = "#81C784" if work_pct >= 75 else "#FFD54F" if work_pct >= 50 else "#EF9A9A" if work_pct > 0 else "#C62828"
        w_label = "عمل" if AR else "work"
        r_label = "راحة" if AR else "rest"
        status_txt = f"{work_pct}% {w_label} / {rest_pct}% {r_label}" if work_pct > 0 else ("⛔ يُمنع العمل" if AR else "⛔ WORK PROHIBITED")
        st.markdown(f'''<div style="background:#0F172A;border-radius:12px;padding:14px 18px;margin-bottom:8px;border:1px solid #334155">
            <div style="display:flex;justify-content:space-between;align-items:center">
                <div><div style="color:{C["text1"]};font-size:14px;font-weight:700">{cat_name}</div><div style="color:{C["text3"]};font-size:11px">{cat_desc}</div></div>
                <div style="color:{bar_color};font-size:14px;font-weight:800">{status_txt}</div>
            </div>
            <div style="background:#1E293B;border-radius:6px;height:8px;margin-top:8px;overflow:hidden">
                <div style="background:{bar_color};height:100%;width:{work_pct}%;border-radius:6px;transition:width 0.5s"></div>
            </div>
        </div>''', unsafe_allow_html=True)

    # Worker-specific heat tolerance
    st.markdown(f'<div style="color:{C["accent"]};font-size:14px;font-weight:700;margin:16px 0">{"👷 تحمّل العمال للحرارة (بناءً على الملف الصحي)" if AR else "👷 Worker Heat Tolerance (based on health profile)"}</div>', unsafe_allow_html=True)

    if len(health_df) > 0:
        ht_data = []
        for _, w in workers_df.iterrows():
            wh_r = health_df[health_df["WorkerID"]==w["WorkerID"]].iloc[0] if w["WorkerID"] in health_df["WorkerID"].values else None
            if wh_r is None: continue
            w_age = wh_r.get("Age", 30)
            w_bmi = wh_r.get("BMI", 25)
            w_fit = wh_r.get("FitnessLevel", "Fit")

            # Calculate max hours based on WBGT + profile
            base_hours = 8 if heat_index_c < 33 else 6 if heat_index_c < 41 else 4 if heat_index_c < 54 else 2
            if isinstance(w_age,(int,float)) and w_age >= 50: base_hours *= 0.5
            elif isinstance(w_age,(int,float)) and w_age >= 45: base_hours *= 0.7
            if isinstance(w_bmi,(int,float,float)) and w_bmi >= 30: base_hours *= 0.6
            if w_fit == "Unfit": base_hours *= 0.3
            elif w_fit == "Moderate": base_hours *= 0.7
            base_hours = max(0, round(base_hours, 1))

            risk = "🔴" if base_hours <= 2 else "🟡" if base_hours <= 4 else "🟢"
            ht_data.append({"name": w["FullName"], "age": w_age, "bmi": w_bmi, "fit": w_fit, "hours": base_hours, "risk": risk})

        ht_data.sort(key=lambda x: x["hours"])
        t = f'<table class="styled-table"><tr><th>{"العامل" if AR else "Worker"}</th><th>{"العمر" if AR else "Age"}</th><th>BMI</th><th>{"اللياقة" if AR else "Fitness"}</th><th>{"الحد الأقصى" if AR else "Max Hours"}</th><th>{"الحالة" if AR else "Status"}</th></tr>'
        for d in ht_data:
            hc = "#EF9A9A" if d["hours"]<=2 else "#FFD54F" if d["hours"]<=4 else "#81C784"
            t += f'<tr><td style="color:{C["text1"]}!important;font-weight:700">{d["name"]}</td><td style="color:{C["text2"]}!important">{d["age"]}</td><td style="color:{C["text2"]}!important">{d["bmi"]}</td><td style="color:{C["text2"]}!important">{d["fit"]}</td><td style="color:{hc}!important;font-weight:800">{d["hours"]} hrs</td><td>{d["risk"]}</td></tr>'
        t += '</table>'
        st.markdown(t, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════ TAB: ASK ME — AI Assistant ═══════════════
with tab_ask:
    st.markdown(f"""
    <div class="panel" style="border-left:4px solid {C['accent']}">
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:8px">
            <div style="font-size:40px">🤖</div>
            <div>
                <div style="font-size:22px;font-weight:800;color:{C['text1']}">{"مساعد ExpoInsight" if AR else "ExpoInsight Assistant"}</div>
                <div style="font-size:13px;color:{C['text2']}">{"اسأل أي سؤال عن البيانات، النظام، أو السيناريوهات — بالعربي أو الإنجليزي" if AR else "Ask anything about the data, system, or scenarios — in Arabic or English"}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Build live data context for the AI ──
    def build_data_context():
        """Generate a comprehensive text summary of all current dashboard data for the AI."""
        ld = get_ld() if callable(get_ld) else {}
        ud = get_ud() if callable(get_ud) else {}
        if not isinstance(ld, dict): ld = {}
        if not isinstance(ud, dict): ud = {}
        lines = []
        lines.append("=== EXPOINSIGHT SYSTEM OVERVIEW ===")
        lines.append("ExpoInsight is an occupational health monitoring system for power plants.")
        lines.append("It monitors 4 hazards (CO2, HeatIndex, Noise, Gas) across 6 facility zones.")
        lines.append(f"Data source: {len(readings_df)} environmental readings, {len(workers_df)} workers, {len(zones_df)} zones.")
        lines.append(f"Last updated: {readings_df['ReadingDateTime'].max()}")
        lines.append("")

        lines.append("=== CORE CALCULATIONS ===")
        lines.append("Exposure % = Current Value / Limit Value")
        lines.append("Status: Safe (<80%), Warning (80-99%), Critical (>=100%)")
        lines.append("Workers at Risk = workers present in Critical zones")
        lines.append("")

        lines.append("=== EXPOSURE LIMITS (REGULATORY) ===")
        for _,r in limits_df.iterrows():
            lines.append(f"  {r['HazardType']}: {r['LimitValue']} {r['Unit']} ({r.get('RegulatoryStandard','N/A')})")
        lines.append("")

        lines.append("=== ALLOWED EXPOSURE HOURS ===")
        for _,r in allowed_hours_df.iterrows():
            lines.append(f"  {r['HazardType']}: Max {r['MaxDailyHours']} hrs/day, Break: {r['RecommendedBreak']}")
        lines.append("")

        lines.append("=== OVERALL EXPOSURE (ALL ZONES AVERAGE) ===")
        overall = zhstats()
        for s in overall:
            lines.append(f"  {s['Icon']} {s['DisplayName']}: {s['CurrentValue']} {s['Unit']} | Limit: {s['Limit']} | Exposure: {s['ExposurePct']:.1%} | Status: {s['Status']}")
        lines.append(f"  Workers at Risk: {w_risk()}")
        lines.append(f"  Safe Zones: {sz_count()}/{len(zones_df)}")
        lines.append("")

        lines.append("=== ZONE-BY-ZONE BREAKDOWN ===")
        for _,z in zones_df.iterrows():
            zs = zhstats(z["ZoneID"])
            ov = zoverall(z["ZoneID"])
            lines.append(f"\n  [{z['ZoneID']}] {z['ZoneName']} ({z['ZoneType']}, Capacity: {z['Capacity']}) — Overall: {ov}")
            for s in zs:
                lines.append(f"    {s['Icon']} {s['DisplayName']}: {s['CurrentValue']} {s['Unit']} → Exposure: {s['ExposurePct']:.1%} ({s['Status']})")
            # Workers in this zone
            zw = presence_df[presence_df["ZoneID"]==z["ZoneID"]].merge(workers_df, on="WorkerID", how="left")
            if len(zw) > 0:
                wnames = ", ".join(zw["FullName"].dropna().tolist())
                lines.append(f"    Workers present: {wnames}")
        lines.append("")

        lines.append("=== WORKERS ===")
        for _,w in workers_df.iterrows():
            wp = presence_df[presence_df["WorkerID"]==w["WorkerID"]]
            total_h = 0
            visited = []
            if len(wp) > 0:
                wp2 = wp.copy()
                wp2["Hours"] = (wp2["ExitDateTime"] - wp2["EntryDateTime"]).dt.total_seconds() / 3600
                total_h = wp2["Hours"].sum()
                visited = wp2["ZoneID"].unique().tolist()
            lines.append(f"  {w['WorkerID']} {w['FullName']} | {w['JobTitle']} | {w['Department']} | Shift: {w['Shift']} | Hours: {total_h:.1f} | Zones: {', '.join(visited)}")
        lines.append("")

        lines.append("=== SIMULATION SCENARIOS ===")
        for sc in simulation_df["ScenarioName"].unique():
            sd = simulation_df[simulation_df["ScenarioName"]==sc]
            lines.append(f"\n  Scenario: {sc}")
            for _,r in sd.iterrows():
                if r["DeltaValue"] != 0:
                    zn = zname(r["ZoneID"])
                    # compute projected
                    rdf = readings_df[(readings_df["ZoneID"]==r["ZoneID"])&(readings_df["HazardType"]==r["HazardType"])]
                    curr = rdf["MeasuredValue"].mean() if len(rdf)>0 else 0
                    proj = curr + r["DeltaValue"]
                    lim = ld.get(r["HazardType"], 1)
                    exp_before = cexp(curr, lim)
                    exp_after = cexp(proj, lim)
                    lines.append(f"    {zn} / {r['HazardType']}: Δ{r['DeltaValue']:+g} → Before: {curr:.1f} ({exp_before:.0%}) → After: {proj:.1f} ({exp_after:.0%}) [{gstat(exp_after)}]")

        return "\n".join(lines)

    # ── Quick-action buttons ──
    st.markdown(f"<div style='margin:12px 0 8px;color:{C['text2']};font-size:13px;font-weight:600'>{'💡 أسئلة سريعة:' if AR else '💡 Quick Questions:'}</div>", unsafe_allow_html=True)

    qcols = st.columns(4)
    quick_qs = [
        ("🏭", "ما هي أخطر منطقة؟" if AR else "What's the most dangerous zone?"),
        ("📊", "اشرح لي النظام" if AR else "Explain the system"),
        ("📐", "اشرح المعادلات" if AR else "Explain the equations"),
        ("👷", "من هم العمال المعرضين للخطر؟" if AR else "Which workers are at risk?"),
    ]

    for i, (ic, q) in enumerate(quick_qs):
        with qcols[i]:
            if st.button(f"{ic} {q}", key=f"qq_{i}", use_container_width=True):
                st.session_state["ask_input"] = q

    # ── Chat history ──
    if "ask_messages" not in st.session_state:
        st.session_state["ask_messages"] = []

    # ── User input ──
    user_q = st.chat_input("اكتب سؤالك هنا..." if AR else "Type your question here...")

    # Check if quick question was pressed
    if "ask_input" in st.session_state and st.session_state["ask_input"]:
        user_q = st.session_state["ask_input"]
        st.session_state["ask_input"] = ""

    # ── Display chat history ──
    for msg in st.session_state["ask_messages"]:
        with st.chat_message(msg["role"], avatar="👤" if msg["role"]=="user" else "🤖"):
            st.markdown(msg["content"])

    # ── Process new question ──
    if user_q:
        # Add user message
        st.session_state["ask_messages"].append({"role": "user", "content": user_q})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_q)

        # Build context and generate response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🔍 جاري التحليل..." if AR else "🔍 Analyzing..."):
                data_context = build_data_context()

                system_prompt = f"""أنت "مساعد ExpoInsight" — محلل متخصص في الصحة المهنية والسلامة، مدمج داخل لوحة مراقبة ExpoInsight لمحطات الطاقة في المملكة العربية السعودية.

IDENTITY RULES (CRITICAL — NEVER BREAK THESE):
- You are "ExpoInsight Assistant" / "مساعد ExpoInsight". That is your ONLY identity.
- NEVER mention Claude, Anthropic, AI model, language model, LLM, GPT, or any AI technology.
- NEVER say "I am an AI" or "I am a language model" or anything similar.
- If asked "who are you?" or "what are you?", say: "أنا مساعد ExpoInsight — نظام تحليل الصحة المهنية المدمج في لوحة المراقبة" (or English equivalent).
- If asked who made you, say: "أنا جزء من نظام ExpoInsight لمراقبة الصحة المهنية" — do NOT mention Anthropic or Claude.
- You are a BUILT-IN feature of the ExpoInsight dashboard, like a calculator or report generator.

SCOPE RULES (CRITICAL):
- ONLY answer questions related to: occupational health, safety, the dashboard data, zones, workers, hazards, exposure, simulations, regulatory standards (OSHA, ACGIH, NCOSH), Saudi workplace safety.
- If asked about ANYTHING outside this scope (cooking, sports, politics, coding, personal advice, weather, etc.), politely decline:
  Arabic: "عذراً، أنا متخصص فقط في الصحة المهنية وبيانات ExpoInsight. كيف أقدر أساعدك في تحليل السلامة؟"
  English: "Sorry, I only handle occupational health and ExpoInsight data. How can I help you with safety analysis?"
- Do NOT try to be helpful with off-topic questions. Just redirect to your scope.

CAPABILITIES:
1. Answer questions about current hazard readings, exposure levels, and zone statuses
2. Explain how the ExpoInsight system works (formulas, thresholds, regulatory standards)
3. Analyze simulation scenarios and predict impacts
4. Identify workers at risk and recommend actions
5. Provide safety recommendations based on OSHA, ACGIH, and Saudi NCOSH standards
6. Compare zones, identify trends, and flag concerns

RESPONSE STYLE:
- If the user writes in Arabic, respond in Arabic. If English, respond in English.
- Be concise but thorough
- Use numbers and data from the context provided below
- Use emoji for visual clarity
- For scenarios, show before/after comparisons
- Always provide actionable recommendations when relevant

CURRENT LIVE DATA:
{data_context}
"""
                # Build messages for API call
                api_messages = [{"role": "user", "content": user_q}]

                # Include last few messages for context (keep conversation flowing)
                history_for_api = st.session_state["ask_messages"][-6:-1]  # last 3 exchanges
                if history_for_api:
                    api_messages = [{"role": m["role"], "content": m["content"]} for m in history_for_api] + api_messages

                try:
                    import urllib.request
                    import json

                    request_body = json.dumps({
                        "model": "claude-sonnet-4-20250514",
                        "max_tokens": 2000,
                        "system": system_prompt,
                        "messages": api_messages,
                    }).encode("utf-8")

                    req = urllib.request.Request(
                        "https://api.anthropic.com/v1/messages",
                        data=request_body,
                        headers={
                            "Content-Type": "application/json",
                        },
                        method="POST",
                    )

                    with urllib.request.urlopen(req, timeout=30) as resp:
                        result = json.loads(resp.read().decode("utf-8"))

                    # Extract text from response
                    answer = ""
                    for block in result.get("content", []):
                        if block.get("type") == "text":
                            answer += block["text"]

                    if not answer:
                        answer = "⚠️ لم أتمكن من إنشاء رد. حاول مرة أخرى." if AR else "⚠️ Could not generate a response. Please try again."

                except Exception as e:
                    # Fallback: generate answer locally from data
                    answer = generate_local_answer(user_q, data_context, AR)

                st.markdown(answer)
                st.session_state["ask_messages"].append({"role": "assistant", "content": answer})

    # ── Clear chat button ──
    if st.session_state["ask_messages"]:
        if st.button("🗑️ مسح المحادثة" if AR else "🗑️ Clear Chat", key="clear_ask"):
            st.session_state["ask_messages"] = []
            st.rerun()


def generate_local_answer(question, data_context, is_arabic=False):
    """Fallback: generate an intelligent answer locally by parsing the data context.
    Acts as ExpoInsight's built-in assistant — never mentions AI/Claude/Anthropic.
    Only answers occupational health & ExpoInsight-related questions."""
    q = question.lower()
    lines = data_context.split("\n")

    # ── SCOPE GUARD: reject off-topic questions ──
    safety_keywords = ["خطر","منطقة","عامل","تعرض","حرار","ضوضاء","غاز","co2","zone","worker","hazard",
                       "exposure","noise","heat","gas","safe","critical","warning","سيناريو","scenario",
                       "simulation","محاكاة","اشرح","explain","نظام","system","expoinsight","حد","limit",
                       "osha","ncosh","acgih","سلام","safety","صحة","health","sensor","حساس","تنبيه","alert",
                       "risk","خطر","مراقب","monitor","dashboard","لوحة","report","تقرير","wbgt","حراري",
                       "thermal","ملخص","summary","status","حالة","reading","قراء","calibrat","معاير"]
    is_on_topic = any(kw in q for kw in safety_keywords)

    if not is_on_topic:
        if is_arabic:
            return "عذراً، أنا متخصص فقط في الصحة المهنية وبيانات ExpoInsight. 🛡️\n\nيمكنني مساعدتك في:\n- تحليل مستويات التعرض والمخاطر\n- شرح النظام ومعادلاته\n- تحليل السيناريوهات\n- معلومات عن العمال والمناطق\n\nكيف أقدر أساعدك في تحليل السلامة؟"
        else:
            return "Sorry, I specialize only in occupational health and ExpoInsight data. 🛡️\n\nI can help you with:\n- Analyzing exposure levels and hazards\n- Explaining the system and its formulas\n- Scenario analysis\n- Worker and zone information\n\nHow can I help you with safety analysis?"

    # Helper to find zone stats
    def find_zone_info():
        zone_data = {}
        current_zone = None
        for line in lines:
            if line.strip().startswith("[Z0"):
                parts = line.strip()
                zid = parts[1:5]
                current_zone = zid
                zone_data[zid] = {"line": parts, "hazards": []}
            elif current_zone and ("Exposure:" in line):
                zone_data[current_zone]["hazards"].append(line.strip())
        return zone_data

    # ── System explanation ──
    if any(w in q for w in ["اشرح", "explain", "شرح", "كيف يعمل", "how does", "what is expoinsight", "ما هو", "من أنت", "who are you", "what are you", "وش أنت"]):
        if is_arabic:
            return """## 🛡️ شرح نظام ExpoInsight

أنا **مساعد ExpoInsight** — محلل الصحة المهنية المدمج في لوحة المراقبة.

**ExpoInsight** هو نظام مراقبة الصحة المهنية لمحطات الطاقة في المملكة العربية السعودية.

### 📊 ماذا يراقب؟
يتابع **4 مخاطر رئيسية** في **6 مناطق** بالمحطة:
- 💨 **ثاني أكسيد الكربون (CO₂)** — الحد: 1,000 ppm (معيار OSHA)
- 🌡️ **مؤشر الحرارة (Heat Index)** — الحد: 40 درجة (معيار ACGIH)
- 🔊 **الضوضاء (Noise)** — الحد: 85 ديسيبل (معيار OSHA)
- ⚗️ **الغازات السامة (Gas)** — الحد: 25 ppm (معيار OSHA PEL)

### 📐 المعادلة الأساسية
```
نسبة التعرض = القراءة الحالية ÷ الحد المسموح × 100%
```

### 🚦 قواعد الحالة
- ✅ **آمن (Safe)**: أقل من 80%
- ⚠️ **تحذير (Warning)**: من 80% إلى 99%
- 🚨 **خطر (Critical)**: 100% أو أكثر

### 📱 الصفحات
1. **الرئيسية** — لوحة المراقبة الرئيسية بالأرقام والرسوم البيانية
2. **نظرة عامة** — تحليل شامل مع خريطة حرارية واتجاهات
3. **المناطق** — تفاصيل كل منطقة وحساساتها وعمالها
4. **المحاكاة** — سيناريوهات "ماذا لو" لتقييم المخاطر المستقبلية
5. **العمال** — متابعة تعرض كل عامل على حدة
6. **التنبيهات** — إنذارات فورية عند تجاوز الحدود
7. **التنفيذي** — ملخص للإدارة العليا
8. **الإجهاد الحراري** — حسابات WBGT المتقدمة"""
        else:
            return """## 🛡️ ExpoInsight System Explanation

I'm the **ExpoInsight Assistant** — the built-in occupational health analyst in this monitoring dashboard.

**ExpoInsight** is an occupational health monitoring system for Saudi power plants.

### 📊 What it monitors
It tracks **4 hazards** across **6 facility zones**:
- 💨 **CO₂** — Limit: 1,000 ppm (OSHA 1910.1000)
- 🌡️ **Heat Index** — Limit: 40 (ACGIH TLV)
- 🔊 **Noise** — Limit: 85 dBA (OSHA 1910.95)
- ⚗️ **Gas** — Limit: 25 ppm (OSHA PEL)

### 📐 Core Formula
```
Exposure % = Current Value ÷ Limit Value × 100%
```

### 🚦 Status Rules
- ✅ **Safe**: Below 80%
- ⚠️ **Warning**: 80% to 99%
- 🚨 **Critical**: 100% or above

### 📱 Dashboard Pages
1. **HOME** — Main KPIs, charts, and zone comparison
2. **OVERVIEW** — Heatmap, trends, and top exposed workers
3. **ZONES** — Detailed zone analysis with sensor maps
4. **SIMULATION** — "What if" scenarios for risk planning
5. **WORKERS** — Individual worker exposure tracking
6. **ALERTS** — Real-time warnings for threshold breaches
7. **EXECUTIVE** — Management summary dashboard
8. **HEAT STRESS** — Advanced WBGT calculations"""

    # ── Most dangerous zone ──
    if any(w in q for w in ["أخطر", "خطر", "dangerous", "worst zone", "critical zone", "most dangerous"]):
        zone_data = find_zone_info()
        # Find zones with Critical status
        critical_zones = []
        warning_zones = []
        for line in lines:
            if "Overall: Critical" in line:
                critical_zones.append(line.strip())
            elif "Overall: Warning" in line:
                warning_zones.append(line.strip())

        if is_arabic:
            resp = "## 🚨 تحليل أخطر المناطق\n\n"
            if critical_zones:
                resp += "### المناطق الحرجة (Critical):\n"
                for cz in critical_zones:
                    resp += f"- 🔴 {cz}\n"
            if warning_zones:
                resp += "\n### مناطق التحذير (Warning):\n"
                for wz in warning_zones:
                    resp += f"- 🟡 {wz}\n"
            if not critical_zones and not warning_zones:
                resp += "✅ جميع المناطق آمنة حالياً!"
            resp += "\n\n💡 **التوصية**: التركيز على المناطق الحرجة وتقليل وقت تواجد العمال فيها."
        else:
            resp = "## 🚨 Most Dangerous Zones Analysis\n\n"
            if critical_zones:
                resp += "### Critical Zones:\n"
                for cz in critical_zones:
                    resp += f"- 🔴 {cz}\n"
            if warning_zones:
                resp += "\n### Warning Zones:\n"
                for wz in warning_zones:
                    resp += f"- 🟡 {wz}\n"
            if not critical_zones and not warning_zones:
                resp += "✅ All zones are currently Safe!"
            resp += "\n\n💡 **Recommendation**: Focus on critical zones and minimize worker presence."
        return resp

    # ── Workers at risk ──
    if any(w in q for w in ["عمال", "معرض", "workers", "risk", "at risk", "خطر"]):
        worker_lines = [l for l in lines if l.strip().startswith("W0")]
        risk_count = w_risk()
        if is_arabic:
            resp = f"## 👷 تحليل العمال المعرضين للخطر\n\n"
            resp += f"**عدد العمال المعرضين للخطر: {risk_count}**\n\n"
            resp += "هؤلاء هم العمال المتواجدون في مناطق حالتها Critical:\n\n"
            for wl in worker_lines[:10]:
                resp += f"- {wl.strip()}\n"
            resp += "\n💡 **التوصية**: إخلاء العمال من المناطق الحرجة أو توفير معدات حماية إضافية."
        else:
            resp = f"## 👷 Workers at Risk Analysis\n\n"
            resp += f"**Workers at Risk: {risk_count}**\n\n"
            resp += "Workers currently present in Critical zones:\n\n"
            for wl in worker_lines[:10]:
                resp += f"- {wl.strip()}\n"
            resp += "\n💡 **Recommendation**: Evacuate workers from critical zones or provide additional PPE."
        return resp

    # ── Simulation / Scenario ──
    if any(w in q for w in ["سيناريو", "محاكاة", "scenario", "simulation", "worst case", "increased", "new equipment"]):
        sim_section = False
        sim_lines = []
        for line in lines:
            if "=== SIMULATION" in line:
                sim_section = True
                continue
            if sim_section:
                if line.strip():
                    sim_lines.append(line.strip())
        if is_arabic:
            resp = "## 🔬 تحليل السيناريوهات\n\n"
            resp += "السيناريوهات المتاحة في النظام:\n\n"
            for sl in sim_lines[:20]:
                resp += f"- {sl}\n"
            resp += "\n💡 **التوصية**: سيناريو Worst Case يحتاج خطة طوارئ جاهزة."
        else:
            resp = "## 🔬 Scenario Analysis\n\n"
            resp += "Available simulation scenarios:\n\n"
            for sl in sim_lines[:20]:
                resp += f"- {sl}\n"
            resp += "\n💡 **Recommendation**: Worst Case scenario requires emergency preparedness plan."
        return resp

    # ── Generic / fallback — provide full summary ──
    overall = zhstats()
    if is_arabic:
        resp = "## 📊 ملخص الوضع الحالي\n\n"
        for s in overall:
            resp += f"- {s['Icon']} **{s['DisplayName']}**: {s['CurrentValue']} {s['Unit']} — التعرض: {s['ExposurePct']:.0%} — الحالة: {s['Status']}\n"
        resp += f"\n- 👷 عدد العمال: {workers_df['WorkerID'].nunique()}\n"
        resp += f"- 🚨 عمال في خطر: {w_risk()}\n"
        resp += f"- ✅ مناطق آمنة: {sz_count()}/{len(zones_df)}\n"
        resp += f"\n💡 هل تريد تفاصيل أكثر عن منطقة أو عامل معين؟ اسألني!"
    else:
        resp = "## 📊 Current Status Summary\n\n"
        for s in overall:
            resp += f"- {s['Icon']} **{s['DisplayName']}**: {s['CurrentValue']} {s['Unit']} — Exposure: {s['ExposurePct']:.0%} — Status: {s['Status']}\n"
        resp += f"\n- 👷 Total Workers: {workers_df['WorkerID'].nunique()}\n"
        resp += f"- 🚨 Workers at Risk: {w_risk()}\n"
        resp += f"- ✅ Safe Zones: {sz_count()}/{len(zones_df)}\n"
        resp += f"\n💡 Want more details about a specific zone or worker? Just ask!"
    return resp


# ═══════════════ EXPORT + FOOTER ═══════════════
st.markdown("---")
st.markdown(f"### 📄 Export Report")
if st.button("📥 Generate Report",key="pdf"):
    sa=zhstats()
    rh=f'<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{{font-family:-apple-system,Inter,sans-serif;padding:20px;color:#FFF;background:#0F172A;direction:ltr}}h1{{color:#4FC3F7;border-bottom:3px solid #0F4C75;padding-bottom:10px;font-size:22px}}h2{{color:#4FC3F7;margin-top:30px;font-size:18px}}table{{width:100%;border-collapse:collapse;margin:15px 0}}th{{background:#0B3558;color:white;padding:10px;text-align:left;font-size:13px}}td{{padding:8px 10px;border-bottom:1px solid #334155;color:#94A3B8;font-size:13px}}.safe{{color:#81C784;font-weight:bold}}.warning{{color:#FFD54F;font-weight:bold}}.critical{{color:#EF9A9A;font-weight:bold}}.summary{{background:#0B3558;border-radius:12px;padding:16px;margin:16px 0}}.summary span{{display:inline-block;margin:0 12px;font-size:14px}}</style></head><body>'
    rh+=f'<h1>ExpoInsight Report</h1><p style="color:#94A3B8">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")} (Riyadh)</p>'
    rh+=f'<div class="summary"><span style="color:#4FC3F7">Workers: <strong>{workers_df["WorkerID"].nunique()}</strong></span><span style="color:#EF9A9A">At Risk: <strong>{w_risk()}</strong></span><span style="color:#81C784">Safe Zones: <strong>{sz_count()}/{len(zones_df)}</strong></span></div>'
    rh+='<h2>Exposure Summary</h2><table><tr><th>Hazard</th><th>Value</th><th>Limit</th><th>Exposure %</th><th>Status</th></tr>'
    for s in sa: rh+=f'<tr><td>{s["DisplayName"]}</td><td>{s["CurrentValue"]} {s["Unit"]}</td><td>{s["Limit"]}</td><td class="{scss(s["Status"])}">{s["ExposurePct"]:.0%}</td><td class="{scss(s["Status"])}">{s["Status"]}</td></tr>'
    rh+='</table><h2>Zones</h2><table><tr><th>Zone</th><th>Type</th><th>Status</th><th>Max Exposure</th></tr>'
    for _,z in zones_df.iterrows():
        zs2=zhstats(z["ZoneID"]);mx2=max(s["ExposurePct"] for s in zs2);os2=zoverall(z["ZoneID"])
        rh+=f'<tr><td>{z["ZoneName"]}</td><td>{z["ZoneType"]}</td><td class="{scss(os2)}">{os2}</td><td class="{scss(os2)}">{mx2:.0%}</td></tr>'
    # Workers section
    rh+='</table><h2>Workers at Risk</h2><table><tr><th>Worker</th><th>Job</th><th>Zone</th><th>Hours</th><th>Status</th></tr>'
    for _,w in workers_df.iterrows():
        wid=w["WorkerID"];wp=presence_df[presence_df["WorkerID"]==wid]
        if len(wp)==0: continue
        total_hrs=wp["Hours"].sum() if "Hours" in wp.columns else 0
        zones_visited=wp["ZoneID"].unique()
        w_status="Safe"; w_class="safe"
        for zid in zones_visited:
            if zoverall(zid)=="Critical": w_status="Critical"; w_class="critical"; break
            elif zoverall(zid)=="Warning" and w_status!="Critical": w_status="Warning"; w_class="warning"
        zone_names=", ".join([zname(zid) for zid in zones_visited])
        rh+=f'<tr><td style="color:#E0E0E0;font-weight:700">{w["FullName"]}</td><td>{w["JobTitle"]}</td><td>{zone_names}</td><td>{total_hrs:.1f}h</td><td class="{w_class}">{w_status}</td></tr>'
    # Recommendations
    rh+='</table><h2>Recommendations</h2><ul style="color:#94A3B8;line-height:2">'
    for _,z in zones_df.iterrows():
        zs2=zhstats(z["ZoneID"]);os2=zoverall(z["ZoneID"])
        if os2=="Critical":
            worst=max(zs2,key=lambda s:s["ExposurePct"])
            rh+=f'<li><strong style="color:#EF9A9A">{z["ZoneName"]}</strong> — Critical: {worst["DisplayName"]} at {worst["ExposurePct"]:.0%}. Immediate action required.</li>'
        elif os2=="Warning":
            worst=max(zs2,key=lambda s:s["ExposurePct"])
            rh+=f'<li><strong style="color:#FFD54F">{z["ZoneName"]}</strong> — Warning: {worst["DisplayName"]} at {worst["ExposurePct"]:.0%}. Monitor closely.</li>'
    rh+='</ul></body></html>'
    st.download_button("📥 Download",data=rh,file_name=f"ExpoInsight_{datetime.now().strftime('%Y%m%d_%H%M')}.html",mime="text/html")
    st.success("✅ Report ready!")

st.markdown(f'<div style="text-align:center;padding:32px 0 12px;color:{C["text3"]};font-size:12px">🛡️ <strong style="color:{C["text1"]}">ExpoInsight V4</strong> — Occupational Health Monitoring · © 2025</div>',unsafe_allow_html=True)
