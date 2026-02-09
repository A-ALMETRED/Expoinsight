"""
ExpoInsight V3 — Ultimate Occupational Health Dashboard
========================================================
All 11 enhancements: Gauges, Auto-refresh, Alerts page, PDF export,
Dark mode, Interactive sensor map, Sparklines, Progress bars,
Zone comparison, Staggered animations, Notification indicators.

Run: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import os, math, base64, io

st.set_page_config(page_title="ExpoInsight V3", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

# ═══════════════════════════════════════════════════
# DARK MODE STATE
# ═══════════════════════════════════════════════════
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def toggle_dark():
    st.session_state.dark_mode = not st.session_state.dark_mode

dm = st.session_state.dark_mode

# Color palette based on mode
C = {
    "bg": "#1A1A2E" if dm else "#EEF2F7",
    "bg2": "#16213E" if dm else "#E2E8F0",
    "card": "#1E293B" if dm else "#FFFFFF",
    "card_border": "rgba(255,255,255,0.06)" if dm else "rgba(0,0,0,0.04)",
    "text1": "#F1F5F9" if dm else "#0B3558",
    "text2": "#94A3B8" if dm else "#546E7A",
    "text3": "#64748B" if dm else "#78909C",
    "table_bg": "#0F172A" if dm else "#FFFFFF",
    "table_row_hover": "#1E293B" if dm else "#F6F9FC",
    "table_border": "#334155" if dm else "#F0F0F0",
    "grid": "#334155" if dm else "#ECEFF1",
    "nav1": "#0B3558", "nav2": "#0F4C75",
    "safe": "#2E7D32", "warn": "#F57F17", "crit": "#C62828",
    "safe_bg": "#1B5E20" if dm else "#E8F5E9",
    "warn_bg": "#F57F17" if dm else "#FFF8E1",
    "crit_bg": "#B71C1C" if dm else "#FFEBEE",
    "safe_txt": "#81C784" if dm else "#2E7D32",
    "warn_txt": "#FFD54F" if dm else "#F57F17",
    "crit_txt": "#EF9A9A" if dm else "#C62828",
    "accent": "#4FC3F7",
    "shadow": "rgba(0,0,0,0.3)" if dm else "rgba(0,0,0,0.06)",
}

# ═══════════════════════════════════════════════════
# MEGA CSS
# ═══════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
#MainMenu,header,footer,.stDeployButton,div[data-testid="stToolbar"],div[data-testid="stDecoration"]{{display:none!important;visibility:hidden!important}}
html,body,.stApp{{font-family:'Inter',-apple-system,sans-serif!important;background:linear-gradient(160deg,{C["bg"]},{C["bg2"]})!important}}
.main .block-container{{padding-top:0;padding-bottom:1rem;max-width:100%}}

/* Force text visibility */
.stApp p,.stApp span,.stApp div,.stApp label,.stMarkdown p,.stMarkdown span,.stMarkdown div,
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] div,[data-testid="stMarkdownContainer"] strong{{font-family:'Inter',sans-serif!important}}

/* Hide radio dots */
div[data-testid="stRadio"]>label{{display:none!important}}
div[data-testid="stRadio"]>div>label>div:first-child{{display:none!important}}
div[data-testid="stRadio"]>div{{gap:0!important}}
div[data-testid="stRadio"]>div>label{{background:transparent!important;padding:0!important;margin:0!important;min-height:0!important}}
div[data-testid="stRadio"]>div>label>div:last-child{{display:none!important}}

@keyframes fadeUp{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes fadeUp1{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes fadeUp2{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes fadeUp3{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes fadeUp4{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes pulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.03)}}}}
@keyframes glow{{0%,100%{{box-shadow:0 0 5px rgba(76,175,80,0.3)}}50%{{box-shadow:0 0 18px rgba(76,175,80,0.6)}}}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:0.4}}}}
@keyframes countUp{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}

/* Nav */
.nav-bar{{background:linear-gradient(135deg,#0B3558,#0F4C75 60%,#1565C0);margin:-1rem -3rem 1.5rem;padding:0;display:flex;align-items:center;border-radius:0 0 20px 20px;box-shadow:0 8px 32px rgba(11,53,88,0.35);z-index:999;overflow:hidden;position:relative}}
.nav-bar::before{{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle at 30% 50%,rgba(79,195,247,0.08),transparent 50%)}}
.nav-logo{{display:flex;align-items:center;padding:16px 32px;gap:14px;position:relative}}
.nav-logo-icon{{width:46px;height:46px;background:linear-gradient(135deg,#4FC3F7,#0288D1);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:22px;box-shadow:0 4px 16px rgba(79,195,247,0.35)}}
.nav-logo-text{{color:#FFF;font-size:22px;font-weight:900;letter-spacing:2.5px}}
.nav-logo-sub{{color:rgba(255,255,255,0.55);font-size:11px;letter-spacing:1.2px}}
.nav-right{{margin-left:auto;padding:16px 32px;display:flex;align-items:center;gap:16px}}
.live-dot{{width:9px;height:9px;background:#4CAF50;border-radius:50%;animation:glow 2s infinite}}
.live-txt{{color:rgba(255,255,255,0.65);font-size:11px;font-weight:600;letter-spacing:1px}}
.dm-btn{{background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#FFF;border-radius:10px;padding:6px 14px;font-size:12px;cursor:pointer;font-weight:600;transition:all .2s}}
.dm-btn:hover{{background:rgba(255,255,255,0.2)}}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{{background:linear-gradient(135deg,#0B3558,#0F4C75);border-radius:14px;padding:5px;gap:0;box-shadow:0 4px 16px rgba(11,53,88,0.2)}}
.stTabs [data-baseweb="tab"]{{color:rgba(255,255,255,0.65)!important;font-weight:700!important;font-size:12px!important;letter-spacing:1px!important;text-transform:uppercase!important;border-radius:10px!important;padding:11px 20px!important;background:transparent!important;border:none!important}}
.stTabs [data-baseweb="tab"]:hover{{color:#FFF!important;background:rgba(255,255,255,0.08)!important}}
.stTabs [aria-selected="true"]{{color:#FFF!important;background:rgba(255,255,255,0.13)!important;border-bottom:3px solid #4FC3F7!important}}
.stTabs [data-baseweb="tab-highlight"]{{background:#4FC3F7!important}}
.stTabs [data-baseweb="tab-border"]{{display:none}}
.stTabs [data-baseweb="tab-panel"]{{padding-top:1.5rem}}

/* KPI Card with staggered animation */
.kpi-card{{background:{C["card"]};border-radius:20px;padding:22px 18px;box-shadow:0 4px 20px {C["shadow"]};border:1px solid {C["card_border"]};text-align:center;overflow:hidden;transition:all .3s;position:relative}}
.kpi-card:hover{{transform:translateY(-4px);box-shadow:0 8px 30px {C["shadow"]}}}
.kpi-card::after{{content:'';position:absolute;top:0;left:0;right:0;height:4px;border-radius:20px 20px 0 0}}
.kpi-card.safe::after{{background:linear-gradient(90deg,#2E7D32,#66BB6A)}}
.kpi-card.warning::after{{background:linear-gradient(90deg,#F57F17,#FFB300)}}
.kpi-card.critical::after{{background:linear-gradient(90deg,#C62828,#EF5350)}}
.kpi-icon{{font-size:30px;margin-bottom:6px}}
.kpi-label{{font-size:11px;color:{C["text3"]};font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px}}
.kpi-value{{font-size:34px;font-weight:900;color:{C["text1"]};line-height:1.1;animation:countUp .6s ease-out}}
.kpi-unit{{font-size:14px;color:{C["text3"]};font-weight:500}}
.kpi-exposure{{font-size:13px;font-weight:700;margin-top:6px}}
.kpi-status{{display:inline-block;padding:4px 14px;border-radius:20px;font-size:11px;font-weight:800;letter-spacing:.7px;margin-top:6px;text-transform:uppercase}}
.status-safe{{background:{C["safe_bg"]};color:{C["safe_txt"]}}}
.status-warning{{background:{C["warn_bg"]};color:{C["warn_txt"]}}}
.status-critical{{background:{C["crit_bg"]};color:{C["crit_txt"]};animation:pulse 2s infinite}}

/* Sparkline container */
.sparkline-row{{display:flex;justify-content:center;gap:2px;margin-top:8px;align-items:flex-end;height:24px}}
.spark-bar{{width:4px;border-radius:2px;transition:height .3s}}

/* Progress bar for exposure */
.exp-bar-container{{width:100%;height:8px;background:{"#334155" if dm else "#E8EDF2"};border-radius:10px;overflow:hidden;margin-top:4px}}
.exp-bar-fill{{height:100%;border-radius:10px;transition:width 1s ease-out}}

/* Panel */
.panel{{background:{C["card"]};border-radius:20px;padding:24px;box-shadow:0 4px 20px {C["shadow"]};border:1px solid {C["card_border"]};margin-bottom:16px;animation:fadeUp .5s ease-out}}
.panel-title{{font-size:16px;font-weight:800;color:{C["text1"]};margin-bottom:18px;display:flex;align-items:center;gap:10px}}

/* Mini KPI */
.mini-kpi{{background:{C["card"]};border-radius:16px;padding:16px 20px;box-shadow:0 3px 14px {C["shadow"]};display:flex;align-items:center;gap:14px;animation:fadeUp .6s ease-out}}
.mini-kpi-icon{{font-size:22px;width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center;flex-shrink:0}}
.mini-kpi-label{{font-size:11px;color:{C["text3"]};font-weight:700;text-transform:uppercase;letter-spacing:.6px}}
.mini-kpi-value{{font-size:22px;font-weight:900;color:{C["text1"]}}}

/* Zone card */
.zone-card{{padding:14px 18px;border-radius:14px;margin-bottom:8px;display:flex;align-items:center;gap:12px;border:2px solid {"#334155" if dm else "#EEE"};background:{C["card"]};transition:all .25s}}
.zone-card:hover{{border-color:#0F4C75}}
.zone-card.active{{background:{"#1E3A5F" if dm else "#E3F2FD"};border-color:#0F4C75;box-shadow:0 3px 12px rgba(15,76,117,0.15)}}
.zone-dot{{width:12px;height:12px;border-radius:50%;flex-shrink:0;box-shadow:0 0 0 3px rgba(0,0,0,0.06)}}
.zone-card-name{{font-size:14px;font-weight:700;color:{C["text1"]}}}
.zone-card-sub{{font-size:11px;color:{C["text3"]};font-weight:500}}

/* Status banner */
.status-banner{{padding:16px 28px;border-radius:16px;font-size:17px;font-weight:800;text-align:center;letter-spacing:1.5px;text-transform:uppercase;color:#FFF;animation:fadeUp .4s ease-out;box-shadow:0 4px 16px rgba(0,0,0,0.15)}}
.banner-safe{{background:linear-gradient(135deg,#2E7D32,#43A047)}}
.banner-warning{{background:linear-gradient(135deg,#F57F17,#F9A825)}}
.banner-critical{{background:linear-gradient(135deg,#C62828,#E53935);animation:pulse 2.5s infinite}}

/* Table */
.styled-table{{width:100%;border-collapse:separate;border-spacing:0;font-size:13px;overflow:hidden;border-radius:14px}}
.styled-table th{{background:linear-gradient(135deg,#0B3558,#0F4C75);color:#FFF;padding:12px 16px;text-align:left;font-weight:700;font-size:11px;text-transform:uppercase;letter-spacing:.8px}}
.styled-table td{{padding:11px 16px;border-bottom:1px solid {C["table_border"]};color:{C["text2"]}!important;font-weight:500;background:{C["table_bg"]}}}
.styled-table tr:hover td{{background:{C["table_row_hover"]}}}
.styled-table tr:last-child td{{border-bottom:none}}

/* Worker card */
.worker-card{{background:{C["card"]};border-radius:16px;padding:18px;box-shadow:0 3px 14px {C["shadow"]};border-left:5px solid #0F4C75;margin-bottom:10px;animation:fadeUp .5s ease-out}}
.worker-card-name{{font-size:15px;font-weight:800;color:{C["text1"]};margin-bottom:4px}}
.worker-card-sub{{font-size:12px;color:{C["text2"]};font-weight:500}}
.worker-card-hours{{font-size:14px;color:#4FC3F7;font-weight:700;margin-top:4px}}

/* Alert bar */
.alert-bar{{background:linear-gradient(135deg,#C62828,#D32F2F);color:#FFF;padding:10px 20px;border-radius:12px;display:flex;align-items:center;gap:10px;margin-bottom:16px;font-size:13px;font-weight:600;animation:fadeUp .4s ease-out}}
.alert-blink{{animation:blink 1.5s infinite}}

/* Alert log item */
.alert-item{{background:{C["card"]};border-radius:12px;padding:14px 18px;margin-bottom:8px;display:flex;align-items:center;gap:14px;border-left:4px solid #C62828;box-shadow:0 2px 8px {C["shadow"]}}}
.alert-item.warn-item{{border-left-color:#F57F17}}
.alert-time{{font-size:11px;color:{C["text3"]};font-weight:600;min-width:90px}}
.alert-text{{font-size:13px;color:{C["text1"]};font-weight:600}}
.alert-badge{{font-size:11px;padding:3px 10px;border-radius:10px;font-weight:700}}

/* Refresh counter */
.refresh-bar{{background:{C["card"]};border-radius:10px;padding:8px 16px;display:inline-flex;align-items:center;gap:8px;font-size:12px;color:{C["text3"]};font-weight:600;box-shadow:0 2px 8px {C["shadow"]};margin-bottom:12px}}

div[data-baseweb="select"]>div{{border-radius:12px!important;border-color:{"#334155" if dm else "#CFD8DC"}!important;background:{C["card"]}!important}}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# AUTO-REFRESH EVERY 30 SECONDS
# ═══════════════════════════════════════════════════
st.markdown("""
<script>
setTimeout(function(){window.location.reload()}, 30000);
</script>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════
@st.cache_data
def load_data():
    fp = next((f for f in ["ExpoInsight-v_1.xlsx",os.path.join(os.path.dirname(os.path.abspath(__file__)),"ExpoInsight-v_1.xlsx")] if os.path.exists(f)),None)
    if not fp: st.error("Excel file not found."); st.stop()
    z=pd.read_excel(fp,sheet_name="Zones",header=2).dropna(subset=["ZoneID"])
    w=pd.read_excel(fp,sheet_name="Workers",header=2).dropna(subset=["WorkerID"])
    p=pd.read_excel(fp,sheet_name="PresenceLog",header=2).dropna(subset=["PresenceID"])
    r=pd.read_excel(fp,sheet_name="EnvironmentalReadings",header=2).dropna(subset=["ReadingID","MeasuredValue"])
    l=pd.read_excel(fp,sheet_name="ExposureLimits",header=2).dropna(subset=["HazardType"])
    ah=pd.read_excel(fp,sheet_name="AllowedExposureHours",header=2)
    s=pd.read_excel(fp,sheet_name="Simulation",header=2).dropna(subset=["ScenarioName"])
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
    return z,w,p,r,l,ah,s

zones_df,workers_df,presence_df,readings_df,limits_df,allowed_hours_df,simulation_df=load_data()

# ═══════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════
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
def sbg(s): return {"Safe":C["safe_bg"],"Warning":C["warn_bg"],"Critical":C["crit_bg"]}.get(s,"#EEE")
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
        l=ld.get(h,1);e=cexp(c,l)
        res.append({"HazardType":h,"DisplayName":HD.get(h,h),"Icon":HI.get(h,"📊"),
            "CurrentValue":round(c,1),"Limit":l,"Unit":ud.get(h,""),"ExposurePct":e,"Status":gstat(e)})
    return res

def get_sparkline_data(zone_id, hazard, n=8):
    """Get last n readings for sparkline mini-chart"""
    df = readings_df[(readings_df["HazardType"]==hazard)]
    if zone_id: df = df[df["ZoneID"]==zone_id]
    df = df.sort_values("ReadingDateTime").tail(n)
    return df["MeasuredValue"].tolist() if len(df)>0 else []

def zoverall(zid):
    ss=[s["Status"] for s in zhstats(zid)]
    if "Critical" in ss: return "Critical"
    if "Warning" in ss: return "Warning"
    return "Safe"

def w_risk():
    cz=[z["ZoneID"] for _,z in zones_df.iterrows() if zoverall(z["ZoneID"])=="Critical"]
    return presence_df[presence_df["ZoneID"].isin(cz)]["WorkerID"].nunique() if cz else 0

def sz_count():
    return sum(1 for _,z in zones_df.iterrows() if zoverall(z["ZoneID"])=="Safe")

def last_upd(): return readings_df["ReadingDateTime"].max()

def build_sparkline_html(values, color="#4FC3F7"):
    """Build mini bar sparkline from values"""
    if not values: return ""
    mx = max(values) if max(values)>0 else 1
    bars = ""
    for v in values:
        h = max(4, int(v/mx*22))
        bars += f'<div class="spark-bar" style="height:{h}px;background:{color};opacity:0.7"></div>'
    return f'<div class="sparkline-row">{bars}</div>'

def build_progress_bar(pct, status):
    """Build progress bar HTML for exposure percentage"""
    w = min(pct*100, 100)
    clr = scolor(status)
    return f'<div class="exp-bar-container"><div class="exp-bar-fill" style="width:{w}%;background:{clr}"></div></div>'

def generate_alerts_log():
    """Generate alert records from readings that exceeded limits"""
    ld = get_ld()
    alerts = []
    for _, r in readings_df.iterrows():
        lim = ld.get(r["HazardType"], 1e9)
        val = r["MeasuredValue"]
        exp = val/lim if lim else 0
        if exp >= 0.8:
            alerts.append({
                "DateTime": r["ReadingDateTime"],
                "ZoneID": r["ZoneID"],
                "Zone": zname(r["ZoneID"]),
                "Hazard": r["HazardType"],
                "Value": round(val,1),
                "Limit": lim,
                "ExposurePct": exp,
                "Status": gstat(exp),
                "Unit": r.get("Unit",""),
            })
    return pd.DataFrame(alerts).sort_values("DateTime", ascending=False) if alerts else pd.DataFrame()

# ═══════════════════════════════════════════════════
# HTML RENDERERS (with Gauge + Sparkline + Progress)
# ═══════════════════════════════════════════════════
def render_gauge(pct, status, size=80):
    """SVG gauge arc for KPI card"""
    angle = min(pct, 1.3) / 1.3 * 270
    r = size/2 - 6
    cx, cy = size/2, size/2
    start_angle = 135
    end_angle = start_angle + angle
    clr = scolor(status)

    def polar_to_cart(cx, cy, r, angle_deg):
        a = math.radians(angle_deg)
        return cx + r*math.cos(a), cy + r*math.sin(a)

    sx, sy = polar_to_cart(cx, cy, r, start_angle)
    ex, ey = polar_to_cart(cx, cy, r, end_angle)
    bsx, bsy = polar_to_cart(cx, cy, r, start_angle)
    bex, bey = polar_to_cart(cx, cy, r, start_angle + 270)
    large1 = 1 if angle > 180 else 0

    bg_color = "#334155" if dm else "#E8EDF2"

    return f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="margin:0 auto;display:block">
        <path d="M {bsx} {bsy} A {r} {r} 0 1 1 {bex} {bey}" fill="none" stroke="{bg_color}" stroke-width="7" stroke-linecap="round"/>
        <path d="M {sx} {sy} A {r} {r} 0 {large1} 1 {ex} {ey}" fill="none" stroke="{clr}" stroke-width="7" stroke-linecap="round"/>
        <text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="14" font-weight="800" fill="{clr}">{pct:.0%}</text>
    </svg>'''

def rkpi(icon, label, value, unit, ep, status, zone_id=None, hazard=None, delay=0):
    """Render KPI card with gauge + sparkline"""
    gauge = render_gauge(ep, status, 76)
    # Sparkline
    spark_html = ""
    if hazard:
        sp_data = get_sparkline_data(zone_id, hazard)
        spark_html = build_sparkline_html(sp_data, scolor(status))

    anim_delay = f"animation-delay:{delay*0.12}s;opacity:0;animation-fill-mode:forwards;" if delay else ""

    return f'''<div class="kpi-card {scss(status)}" style="animation:fadeUp .5s ease-out;{anim_delay}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        {gauge}
        <div class="kpi-value">{value} <span class="kpi-unit">{unit}</span></div>
        <div class="kpi-status status-{scss(status)}">{sicon(status)} {status}</div>
        {spark_html}
    </div>'''

def rkpi_simple(icon, label, value, unit, ep, status):
    """Simple KPI without gauge for overview page"""
    return f'''<div class="kpi-card {scss(status)}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value} <span class="kpi-unit">{unit}</span></div>
        <div class="kpi-exposure" style="color:{stxt(status)}">Exposure: {ep:.0%}</div>
        <div class="kpi-status status-{scss(status)}">{sicon(status)} {status}</div>
    </div>'''

def rmkpi(icon,label,value,bg="#E3F2FD"):
    return f'''<div class="mini-kpi"><div class="mini-kpi-icon" style="background:{bg}">{icon}</div><div><div class="mini-kpi-label">{label}</div><div class="mini-kpi-value">{value}</div></div></div>'''


# ═══════════════════════════════════════════════════
# NAV BAR
# ═══════════════════════════════════════════════════
dm_label = "☀️ Light" if dm else "🌙 Dark"
st.markdown(f'''
<div class="nav-bar">
    <div class="nav-logo">
        <div class="nav-logo-icon">🛡️</div>
        <div><div class="nav-logo-text">EXPOINSIGHT</div><div class="nav-logo-sub">Occupational Health Monitoring</div></div>
    </div>
    <div class="nav-right">
        <div class="live-dot"></div><span class="live-txt">LIVE MONITORING</span>
    </div>
</div>''', unsafe_allow_html=True)

# Dark mode toggle button
col_dm = st.columns([10,1])
with col_dm[1]:
    st.button(dm_label, on_click=toggle_dark, key="dm_toggle")

# Alert bar
crit_z_names=[z["ZoneName"] for _,z in zones_df.iterrows() if zoverall(z["ZoneID"])=="Critical"]
if crit_z_names:
    st.markdown(f'<div class="alert-bar"><span class="alert-blink">🚨</span><span>CRITICAL ALERT — Limits exceeded in: <strong>{", ".join(crit_z_names)}</strong></span><span style="margin-left:auto;opacity:0.7;font-size:11px">{datetime.now().strftime("%H:%M:%S")}</span></div>',unsafe_allow_html=True)

# Auto-refresh indicator
st.markdown(f'<div class="refresh-bar">🔄 Auto-refresh: 30s &nbsp;|&nbsp; 📡 Last update: {datetime.now().strftime("%H:%M:%S")}</div>',unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# TABS (6 tabs now - added ALERTS)
# ═══════════════════════════════════════════════════
tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs(["🏠 HOME","📊 OVERVIEW","🏭 ZONES","🔬 SIMULATION","👷 WORKERS","🚨 ALERTS"])


# ═══════════════════════════════════════════════════
# TAB 1: HOME
# ═══════════════════════════════════════════════════
with tab1:
    zo=["All Zones"]+[f"{r['ZoneID']} - {r['ZoneName']}" for _,r in zones_df.iterrows()]
    sel=st.selectbox("🏭 Select Zone",zo,key="hz")
    szid=None if sel=="All Zones" else sel.split(" - ")[0]
    stats=zhstats(szid)

    # Top 4 KPI with gauge + sparkline + staggered animation
    cols=st.columns(4)
    for i,s in enumerate(stats):
        with cols[i]:
            st.markdown(rkpi(s["Icon"],s["DisplayName"],s["CurrentValue"],s["Unit"],
                s["ExposurePct"],s["Status"],szid,s["HazardType"],delay=i),unsafe_allow_html=True)
    st.markdown("<div style='height:20px'></div>",unsafe_allow_html=True)

    # Middle row: Table + Bar + Donut
    c1,c2,c3=st.columns([3,4,3])
    with c1:
        st.markdown(f'<div class="panel"><div class="panel-title">📋 Current Exposure Levels</div>',unsafe_allow_html=True)
        h='<table class="styled-table"><tr><th>Hazard</th><th>Current</th><th>Limit</th><th>Exposure</th><th>Status</th></tr>'
        for s in stats:
            pbar = build_progress_bar(s["ExposurePct"], s["Status"])
            h+=f'''<tr><td style="color:{C["text1"]}!important;font-weight:700">{s["Icon"]} {s["DisplayName"]}</td>
            <td style="color:{C["text2"]}!important">{s["CurrentValue"]} {s["Unit"]}</td>
            <td style="color:{C["text2"]}!important">{s["Limit"]} {s["Unit"]}</td>
            <td style="color:{stxt(s["Status"])}!important;font-weight:800">{s["ExposurePct"]:.0%}{pbar}</td>
            <td><span class="kpi-status status-{scss(s["Status"])}">{sicon(s["Status"])} {s["Status"]}</span></td></tr>'''
        h+='</table></div>'
        st.markdown(h,unsafe_allow_html=True)

    with c2:
        st.markdown(f'<div class="panel"><div class="panel-title">📊 Exposure by Zone</div>',unsafe_allow_html=True)
        ze=[]
        for _,z in zones_df.iterrows():
            zs=zhstats(z["ZoneID"]);mx=max(s["ExposurePct"] for s in zs)*100
            ze.append({"Zone":z["ZoneName"],"Exp":mx})
        zdf=pd.DataFrame(ze)
        colors=["#C62828" if v>=100 else "#F9A825" if v>=80 else "#2E7D32" for v in zdf["Exp"]]
        fig=go.Figure()
        fig.add_trace(go.Bar(x=zdf["Zone"],y=zdf["Exp"],marker_color=colors,text=[f"{v:.0f}%" for v in zdf["Exp"]],textposition="outside",textfont=dict(size=12,color=C["text2"])))
        fig.add_hline(y=100,line_dash="dash",line_color="#C62828",line_width=2,annotation_text="⚠️ Limit 100%",annotation_position="top right",annotation_font=dict(color="#C62828",size=11))
        fig.update_layout(**PL,height=380,showlegend=False,yaxis=dict(title="Exposure %",gridcolor=C["grid"],range=[0,max(zdf["Exp"].max()*1.2,130)]),xaxis=dict(tickangle=-25))
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("</div>",unsafe_allow_html=True)

    with c3:
        st.markdown(f'<div class="panel"><div class="panel-title">🍩 Risk Distribution</div>',unsafe_allow_html=True)
        scc={"Safe":0,"Warning":0,"Critical":0}
        for _,z in zones_df.iterrows(): scc[zoverall(z["ZoneID"])]+=1
        fig=go.Figure(data=[go.Pie(labels=list(scc.keys()),values=list(scc.values()),hole=0.6,marker_colors=[C["safe"],C["warn"],C["crit"]],textinfo="label+value",textfont=dict(size=13,color="#FFF"),pull=[0,0,0.05])])
        fig.update_layout(**PL,height=380,showlegend=False,annotations=[dict(text="<b>Risk</b>",x=.5,y=.5,font_size=18,font_color=C["text1"],showarrow=False)])
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("</div>",unsafe_allow_html=True)

    # Bottom mini KPIs
    st.markdown("<div style='height:12px'></div>",unsafe_allow_html=True)
    m1,m2,m3,m4=st.columns(4)
    tw=workers_df["WorkerID"].nunique();ar=w_risk();szc=sz_count();tz=len(zones_df)
    lu=last_upd();lus=lu.strftime("%Y-%m-%d %H:%M") if pd.notna(lu) else "N/A"
    with m1: st.markdown(rmkpi("👷","Total Workers",tw,C["safe_bg"]),unsafe_allow_html=True)
    with m2: st.markdown(rmkpi("🚨","Workers at Risk",ar,C["crit_bg"]),unsafe_allow_html=True)
    with m3: st.markdown(rmkpi("✅","Safe Zones",f"{szc}/{tz}",C["safe_bg"]),unsafe_allow_html=True)
    with m4: st.markdown(rmkpi("🕐","Last Updated",lus,C["warn_bg"]),unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# TAB 2: OVERVIEW
# ═══════════════════════════════════════════════════
with tab2:
    tr=st.selectbox("📅 Time Range",["Last 7 days","Last 30 days","All time"],key="ovt")
    mdt=readings_df["ReadingDateTime"].max()
    if tr=="Last 7 days": mndt=mdt-timedelta(days=7)
    elif tr=="Last 30 days": mndt=mdt-timedelta(days=30)
    else: mndt=readings_df["ReadingDateTime"].min()
    fr=readings_df[(readings_df["ReadingDateTime"]>=mndt)&(readings_df["ReadingDateTime"]<=mdt)]
    ld=get_ld()
    exc=sum(1 for _,r in fr.iterrows() if ld.get(r["HazardType"],1e9)<r["MeasuredValue"])
    hex_d={}
    for _,r in fr.iterrows():
        if ld.get(r["HazardType"],1e9)<r["MeasuredValue"]: hex_d[r["HazardType"]]=hex_d.get(r["HazardType"],0)+1
    mf=HD.get(max(hex_d,key=hex_d.get),"None") if hex_d else "None"
    ph=presence_df.copy();ph["Hours"]=(ph["ExitDateTime"]-ph["EntryDateTime"]).dt.total_seconds()/3600
    thr=ph["Hours"].sum();czl=[z["ZoneID"] for _,z in zones_df.iterrows() if zoverall(z["ZoneID"])=="Critical"]

    o1,o2,o3,o4=st.columns(4)
    with o1: st.markdown(rkpi_simple("⚡","Exceedances",exc,"readings",0,"Critical" if exc else "Safe"),unsafe_allow_html=True)
    with o2: st.markdown(rkpi_simple("🔥","Most Frequent",mf,"",0,"Warning"),unsafe_allow_html=True)
    with o3: st.markdown(rkpi_simple("⏱️","Monitored Hrs",f"{thr:.0f}","hrs",0,"Safe"),unsafe_allow_html=True)
    with o4: st.markdown(rkpi_simple("🏭","Critical Zones",len(czl),f"/ {len(zones_df)}",0,"Critical" if czl else "Safe"),unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>",unsafe_allow_html=True)
    ch,ct=st.columns([5,5])
    with ch:
        st.markdown(f'<div class="panel"><div class="panel-title">🗺️ Zone vs Hazard Heatmap</div>',unsafe_allow_html=True)
        zns=zones_df["ZoneName"].tolist();zis=zones_df["ZoneID"].tolist()
        mx=[]
        for zid in zis:
            row=[]
            for h in HO:
                hdf=fr[(fr["ZoneID"]==zid)&(fr["HazardType"]==h)]
                avg=hdf["MeasuredValue"].mean() if len(hdf)>0 else 0
                row.append(round(cexp(avg,ld.get(h,1))*100,1))
            mx.append(row)
        fig=go.Figure(data=go.Heatmap(z=mx,x=[HD.get(h,h) for h in HO],y=zns,
            colorscale=[[0,"#E8F5E9"],[0.5,"#FFF8E1"],[0.8,"#FFCC80"],[1,"#C62828"]],
            text=[[f"{v:.0f}%" for v in r] for r in mx],texttemplate="%{text}",
            textfont=dict(size=13,color=C["text1"]),zmin=0,zmax=130,
            colorbar=dict(title="Exp%",ticksuffix="%")))
        fig.update_layout(**PL,height=370,xaxis_side="top")
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("</div>",unsafe_allow_html=True)
    with ct:
        st.markdown(f'<div class="panel"><div class="panel-title">📈 Hazard Levels Trend</div>',unsafe_allow_html=True)
        fig=go.Figure()
        for h in HO:
            hdf=fr[fr["HazardType"]==h].copy()
            if len(hdf)==0: continue
            hdf=hdf.sort_values("ReadingDateTime");hdf["Hour"]=hdf["ReadingDateTime"].dt.floor("h")
            t=hdf.groupby("Hour")["MeasuredValue"].mean().reset_index()
            t["Exp"]=t["MeasuredValue"]/ld.get(h,1)*100
            fig.add_trace(go.Scatter(x=t["Hour"],y=t["Exp"],name=HD.get(h,h),line=dict(color=HC.get(h,"#333"),width=2.5),mode="lines"))
        fig.add_hline(y=100,line_dash="dash",line_color="#C62828",line_width=2,annotation_text="Limit 100%",annotation_position="top right",annotation_font_color="#C62828")
        fig.update_layout(**PL,height=370,yaxis_title="Exposure %",yaxis=dict(gridcolor=C["grid"]),xaxis=dict(gridcolor=C["grid"]),
            legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("</div>",unsafe_allow_html=True)

    st.markdown(f'<div class="panel"><div class="panel-title">👷 Top 5 Workers by Cumulative Exposure Hours</div>',unsafe_allow_html=True)
    pm=ph.merge(workers_df[["WorkerID","FullName"]],on="WorkerID",how="left")
    t5=pm.groupby(["WorkerID","FullName"])["Hours"].sum().reset_index().sort_values("Hours",ascending=True).tail(5)
    fig=go.Figure()
    fig.add_trace(go.Bar(y=t5["FullName"],x=t5["Hours"],orientation="h",marker_color="#0F4C75",
        text=[f"{h:.1f} hrs" for h in t5["Hours"]],textposition="outside",textfont=dict(size=12,color=C["text2"])))
    fig.update_layout(**PL,height=260,xaxis_title="Hours",showlegend=False,yaxis=dict(tickfont=dict(size=13,color=C["text1"])))
    st.plotly_chart(fig,use_container_width=True)
    st.markdown("</div>",unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# TAB 3: ZONES (with comparison feature)
# ═══════════════════════════════════════════════════
with tab3:
    zl,zd=st.columns([3,7])
    with zl:
        st.markdown(f'<div class="panel"><div class="panel-title">🏭 Zone List</div>',unsafe_allow_html=True)
        zlabels=[f"{z['ZoneID']} - {z['ZoneName']}" for _,z in zones_df.iterrows()]
        selz=st.radio("z",zlabels,key="zs",label_visibility="collapsed")
        for _,z in zones_df.iterrows():
            s=zoverall(z["ZoneID"]);dc=scolor(s)
            act="active" if f"{z['ZoneID']} - {z['ZoneName']}"==selz else ""
            st.markdown(f'<div class="zone-card {act}"><div class="zone-dot" style="background:{dc}"></div><div><div class="zone-card-name">{z["ZoneName"]}</div><div class="zone-card-sub">{z["ZoneType"]} · Cap: {z["Capacity"]}</div></div></div>',unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

        # Zone comparison selector
        st.markdown(f'<div class="panel"><div class="panel-title">⚖️ Compare Zones</div>',unsafe_allow_html=True)
        comp_zone = st.selectbox("Compare with:", ["None"]+zlabels, key="zcomp")
        st.markdown("</div>",unsafe_allow_html=True)

    with zd:
        szid=selz.split(" - ")[0];szn=zname(szid);zst=zoverall(szid)
        st.markdown(f'<div class="status-banner banner-{zst.lower()}">{sicon(zst)} {szn} — {zst.upper()}</div>',unsafe_allow_html=True)
        st.markdown("<div style='height:14px'></div>",unsafe_allow_html=True)
        zsts=zhstats(szid)
        hc=st.columns(4)
        for i,s in enumerate(zsts):
            with hc[i]: st.markdown(rkpi(s["Icon"],s["DisplayName"],s["CurrentValue"],s["Unit"],s["ExposurePct"],s["Status"],szid,s["HazardType"],delay=i),unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>",unsafe_allow_html=True)

        # Zone comparison side by side
        if comp_zone != "None":
            czid = comp_zone.split(" - ")[0]
            czn = zname(czid)
            czsts = zhstats(czid)
            st.markdown(f'<div class="panel"><div class="panel-title">⚖️ Comparison: {szn} vs {czn}</div>',unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Bar(name=szn, x=[s["DisplayName"] for s in zsts], y=[s["ExposurePct"]*100 for s in zsts],
                marker_color="#0F4C75", text=[f"{s['ExposurePct']:.0%}" for s in zsts], textposition="outside"))
            fig.add_trace(go.Bar(name=czn, x=[s["DisplayName"] for s in czsts], y=[s["ExposurePct"]*100 for s in czsts],
                marker_color="#4FC3F7", text=[f"{s['ExposurePct']:.0%}" for s in czsts], textposition="outside"))
            fig.add_hline(y=100, line_dash="dash", line_color="#C62828", line_width=2)
            fig.update_layout(**PL, height=320, barmode="group", yaxis=dict(title="Exposure %", gridcolor=C["grid"]),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>",unsafe_allow_html=True)

        d1,d2=st.columns([5,5])
        with d1:
            st.markdown(f'<div class="panel"><div class="panel-title">🗺️ Zone Layout & Sensor Map</div>',unsafe_allow_html=True)
            sns=[{"n":"Sensor A","x":2,"y":6,"t":"CO2"},{"n":"Sensor B","x":8,"y":6,"t":"Noise"},{"n":"Sensor C","x":2,"y":2,"t":"Gas"},{"n":"Sensor D","x":8,"y":2,"t":"HeatIndex"}]
            fig=go.Figure()
            fig.add_shape(type="rect",x0=0,y0=0,x1=10,y1=8,fillcolor="rgba(227,242,253,0.3)" if not dm else "rgba(30,41,59,0.5)",line=dict(color="#0F4C75",width=2,dash="dot"))
            for gx in range(1,10): fig.add_shape(type="line",x0=gx,y0=0,x1=gx,y1=8,line=dict(color=C["grid"],width=0.5))
            for gy in range(1,8): fig.add_shape(type="line",x0=0,y0=gy,x1=10,y1=gy,line=dict(color=C["grid"],width=0.5))
            for sn in sns:
                hs=next((s for s in zsts if s["HazardType"]==sn["t"]),None)
                clr=scolor(hs["Status"]) if hs else "#999"
                et=f"{hs['ExposurePct']:.0%}" if hs else "N/A"
                fig.add_trace(go.Scatter(x=[sn["x"]],y=[sn["y"]],mode="markers+text",
                    marker=dict(size=30,color=clr,symbol="hexagon2",line=dict(color="white",width=3),opacity=0.9),
                    text=[f"<b>{sn['n']}</b><br>{HD.get(sn['t'],sn['t'])}: {et}"],
                    textposition="top center",textfont=dict(size=10,color=C["text1"]),showlegend=False,
                    hovertemplate=f"<b>{sn['n']}</b><br>{sn['t']}: {et}<extra></extra>"))
                fig.add_trace(go.Scatter(x=[sn["x"]],y=[sn["y"]],mode="markers",
                    marker=dict(size=45,color=clr,opacity=0.12),showlegend=False,hoverinfo="skip"))
            fig.add_annotation(x=5,y=-0.8,text=f"<b>{szn}</b>",showarrow=False,font=dict(size=15,color=C["text1"]))
            fig.update_layout(**PL,height=320,xaxis=dict(visible=False,range=[-1.5,11.5]),yaxis=dict(visible=False,range=[-1.8,9.5]))
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("</div>",unsafe_allow_html=True)

        with d2:
            st.markdown(f'<div class="panel"><div class="panel-title">📋 Sensor Readings</div>',unsafe_allow_html=True)
            snm=["Sensor A","Sensor B","Sensor C","Sensor D"]
            t='<table class="styled-table"><tr><th>Sensor</th><th>Hazard</th><th>Value</th><th>Exposure</th><th>Status</th></tr>'
            for i,s in enumerate(zsts):
                pbar=build_progress_bar(s["ExposurePct"],s["Status"])
                t+=f'<tr><td style="color:{C["text1"]}!important;font-weight:700">{snm[i]}</td><td style="color:{C["text2"]}!important">{s["Icon"]} {s["DisplayName"]}</td><td style="color:{C["text2"]}!important;font-weight:600">{s["CurrentValue"]} {s["Unit"]}</td><td style="color:{stxt(s["Status"])}!important;font-weight:800">{s["ExposurePct"]:.0%}{pbar}</td><td><span class="kpi-status status-{scss(s["Status"])}">{s["Status"]}</span></td></tr>'
            t+='</table></div>'
            st.markdown(t,unsafe_allow_html=True)

            # Radar
            st.markdown(f'<div class="panel"><div class="panel-title">📡 Hazard Radar</div>',unsafe_allow_html=True)
            cats=[s["DisplayName"] for s in zsts]+[zsts[0]["DisplayName"]]
            vals=[s["ExposurePct"]*100 for s in zsts]+[zsts[0]["ExposurePct"]*100]
            fig=go.Figure()
            fig.add_trace(go.Scatterpolar(r=vals,theta=cats,fill='toself',fillcolor="rgba(15,76,117,0.15)",line=dict(color="#0F4C75",width=2.5),name="Current"))
            fig.add_trace(go.Scatterpolar(r=[100]*5,theta=cats,line=dict(color="#C62828",width=2,dash="dash"),name="Limit"))
            fig.update_layout(**PL,height=280,polar=dict(radialaxis=dict(visible=True,range=[0,max(max(vals)*1.1,120)],gridcolor=C["grid"],tickfont=dict(size=10)),
                angularaxis=dict(tickfont=dict(size=12,color=C["text1"]))),showlegend=True,legend=dict(orientation="h",y=-0.1,x=0.5,xanchor="center"))
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("</div>",unsafe_allow_html=True)

        # Workers in zone
        st.markdown(f'<div class="panel"><div class="panel-title">👷 Currently Present Workers</div>',unsafe_allow_html=True)
        zw=presence_df[presence_df["ZoneID"]==szid].merge(workers_df,on="WorkerID",how="left")
        if len(zw)>0:
            wcs=st.columns(min(4,len(zw)))
            for i,(_,w) in enumerate(zw.iterrows()):
                ci=i%min(4,len(zw))
                ent=w["EntryDateTime"].strftime("%H:%M") if pd.notna(w["EntryDateTime"]) else "N/A"
                dur=""
                if pd.notna(w["EntryDateTime"]) and pd.notna(w["ExitDateTime"]): dur=f'{(w["ExitDateTime"]-w["EntryDateTime"]).total_seconds()/3600:.1f} hrs'
                with wcs[ci]:
                    st.markdown(f'<div class="worker-card"><div class="worker-card-name">👤 {w.get("FullName",w["WorkerID"])}</div><div class="worker-card-sub">{w.get("JobTitle","N/A")} · Entry: {ent}</div><div class="worker-card-hours">{dur}</div></div>',unsafe_allow_html=True)
        else: st.info("No workers currently present.")
        st.markdown("</div>",unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# TAB 4: SIMULATION
# ═══════════════════════════════════════════════════
with tab4:
    scns=simulation_df["ScenarioName"].unique().tolist()
    sels=st.selectbox("🔬 Select Scenario",scns,key="ss")
    sd=simulation_df[simulation_df["ScenarioName"]==sels]
    ld=get_ld()
    cr=[]
    for _,z in zones_df.iterrows():
        for h in HO:
            rdf=readings_df[(readings_df["ZoneID"]==z["ZoneID"])&(readings_df["HazardType"]==h)]
            cur=rdf["MeasuredValue"].mean() if len(rdf)>0 else 0
            dr=sd[(sd["ZoneID"]==z["ZoneID"])&(sd["HazardType"]==h)]
            delta=dr["DeltaValue"].iloc[0] if len(dr)>0 else 0
            proj=cur+delta;lm=ld.get(h,1)
            cr.append({"Zone":z["ZoneName"],"ZoneID":z["ZoneID"],"Hazard":HD.get(h,h),"HazardType":h,"Before":round(cur,1),"Delta":delta,"After":round(proj,1),"Limit":lm,"BExp":cexp(cur,lm),"AExp":cexp(proj,lm),"BSt":gstat(cexp(cur,lm)),"ASt":gstat(cexp(proj,lm))})
    comp=pd.DataFrame(cr)

    sk1,sk2,sk3=st.columns(3)
    ac=comp[comp["ASt"]=="Critical"]["Zone"].nunique();aw=comp[comp["ASt"]=="Warning"]["Zone"].nunique();mxa=comp["AExp"].max()*100
    with sk1: st.markdown(rmkpi("🚨","Zones → Critical",ac,C["crit_bg"]),unsafe_allow_html=True)
    with sk2: st.markdown(rmkpi("⚠️","Zones → Warning",aw,C["warn_bg"]),unsafe_allow_html=True)
    with sk3: st.markdown(rmkpi("📊","Max Exposure",f"{mxa:.0f}%",C["safe_bg"]),unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>",unsafe_allow_html=True)
    s1,s2=st.columns(2)
    with s1:
        st.markdown(f'<div class="panel"><div class="panel-title">📊 Before vs After</div>',unsafe_allow_html=True)
        zc=comp.groupby("Zone").agg(B=("BExp","max"),A=("AExp","max")).reset_index()
        fig=go.Figure()
        fig.add_trace(go.Bar(name="Before",x=zc["Zone"],y=zc["B"]*100,marker_color="#0F4C75",text=[f"{v:.0f}%" for v in zc["B"]*100],textposition="outside"))
        fig.add_trace(go.Bar(name="After",x=zc["Zone"],y=zc["A"]*100,marker_color="#4FC3F7",text=[f"{v:.0f}%" for v in zc["A"]*100],textposition="outside"))
        fig.add_hline(y=100,line_dash="dash",line_color="#C62828",line_width=2)
        fig.update_layout(**PL,height=400,barmode="group",yaxis_title="Exposure %",
            legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),yaxis=dict(gridcolor=C["grid"]))
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("</div>",unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="panel"><div class="panel-title">📋 Delta Matrix</div>',unsafe_allow_html=True)
        chg=comp[comp["Delta"]!=0]
        if len(chg)>0:
            t='<table class="styled-table"><tr><th>Zone</th><th>Hazard</th><th>Before</th><th>Δ</th><th>After</th><th>Exp%</th><th>Status</th></tr>'
            for _,r in chg.iterrows():
                ds="+" if r["Delta"]>0 else "";dc="#C62828" if r["Delta"]>0 else "#2E7D32"
                t+=f'<tr><td style="color:{C["text1"]}!important;font-weight:700">{r["Zone"]}</td><td style="color:{C["text2"]}!important">{HI.get(r["HazardType"],"")} {r["Hazard"]}</td><td style="color:{C["text2"]}!important">{r["Before"]}</td><td style="color:{dc}!important;font-weight:800">{ds}{r["Delta"]}</td><td style="color:{C["text1"]}!important;font-weight:700">{r["After"]}</td><td style="color:{stxt(r["ASt"])}!important;font-weight:800">{r["AExp"]:.0%}</td><td><span class="kpi-status status-{scss(r["ASt"])}">{r["ASt"]}</span></td></tr>'
            t+='</table>'
            st.markdown(t,unsafe_allow_html=True)
        else: st.info("No changes in Baseline scenario.")
        st.markdown("</div>",unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# TAB 5: WORKERS
# ═══════════════════════════════════════════════════
with tab5:
    wo=[f"{w['WorkerID']} - {w['FullName']}" for _,w in workers_df.iterrows()]
    sw=st.selectbox("👷 Select Worker",wo,key="ws")
    swid=sw.split(" - ")[0]
    wi=workers_df[workers_df["WorkerID"]==swid].iloc[0]
    wp=presence_df[presence_df["WorkerID"]==swid].copy()

    st.markdown(f'<div class="panel" style="border-left:6px solid #0F4C75;display:flex;align-items:center;gap:24px"><div style="font-size:52px;line-height:1">👤</div><div><div style="font-size:24px;font-weight:900;color:{C["text1"]}">{wi["FullName"]}</div><div style="font-size:14px;color:{C["text2"]};margin-top:2px">{wi["JobTitle"]} · {wi["Department"]} · Shift: {wi["Shift"]}</div></div></div>',unsafe_allow_html=True)

    tth=0;zvs=set()
    if len(wp)>0:
        wp["Hours"]=(wp["ExitDateTime"]-wp["EntryDateTime"]).dt.total_seconds()/3600
        tth=wp["Hours"].sum();zvs=set(wp["ZoneID"].unique())
    cv=[z for z in zvs if zoverall(z)=="Critical"];rl="At Risk" if cv else "Safe";rs="Critical" if cv else "Safe"

    w1,w2,w3=st.columns(3)
    with w1: st.markdown(rmkpi("⏱️","Total Hours",f"{tth:.1f} hrs",C["safe_bg"]),unsafe_allow_html=True)
    with w2: st.markdown(rmkpi("🏭","Zones Visited",len(zvs),C["safe_bg"]),unsafe_allow_html=True)
    with w3: st.markdown(rmkpi(sicon(rs),"Risk Status",rl,sbg(rs)),unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>",unsafe_allow_html=True)
    wd1,wd2=st.columns(2)
    with wd1:
        st.markdown(f'<div class="panel"><div class="panel-title">📋 Zone Visit Log</div>',unsafe_allow_html=True)
        if len(wp)>0:
            t='<table class="styled-table"><tr><th>Zone</th><th>Entry</th><th>Exit</th><th>Duration</th><th>Status</th></tr>'
            for _,p in wp.iterrows():
                zn=zname(p["ZoneID"]);ent=p["EntryDateTime"].strftime("%Y-%m-%d %H:%M") if pd.notna(p["EntryDateTime"]) else "N/A"
                ext=p["ExitDateTime"].strftime("%H:%M") if pd.notna(p["ExitDateTime"]) else "N/A"
                dur=f"{p['Hours']:.1f} hrs" if "Hours" in p and pd.notna(p.get("Hours")) else "N/A"
                zs=zoverall(p["ZoneID"])
                t+=f'<tr><td style="color:{C["text1"]}!important;font-weight:700">{zn}</td><td style="color:{C["text2"]}!important">{ent}</td><td style="color:{C["text2"]}!important">{ext}</td><td style="color:{C["text1"]}!important;font-weight:600">{dur}</td><td><span class="kpi-status status-{scss(zs)}">{zs}</span></td></tr>'
            t+='</table>'
            st.markdown(t,unsafe_allow_html=True)
        else: st.info("No presence records.")
        st.markdown("</div>",unsafe_allow_html=True)
    with wd2:
        st.markdown(f'<div class="panel"><div class="panel-title">📊 Exposure Summary</div>',unsafe_allow_html=True)
        if len(wp)>0:
            he={h:[] for h in HO}
            for _,p in wp.iterrows():
                zs=zhstats(p["ZoneID"]);hrs=p.get("Hours",0)
                for s in zs: he[s["HazardType"]].append({"e":s["ExposurePct"],"h":hrs if pd.notna(hrs) else 0})
            ed=[]
            for h in HO:
                items=he[h]
                if items:
                    th=sum(i["h"] for i in items)
                    wa=sum(i["e"]*i["h"] for i in items)/th if th>0 else np.mean([i["e"] for i in items])
                    ed.append({"Hazard":HD.get(h,h),"Exp":wa*100})
            edf=pd.DataFrame(ed)
            colors=["#C62828" if v>=100 else "#F9A825" if v>=80 else "#2E7D32" for v in edf["Exp"]]
            fig=go.Figure()
            fig.add_trace(go.Bar(x=edf["Hazard"],y=edf["Exp"],marker_color=colors,text=[f"{v:.0f}%" for v in edf["Exp"]],textposition="outside"))
            fig.add_hline(y=100,line_dash="dash",line_color="#C62828",line_width=2)
            fig.update_layout(**PL,height=320,yaxis_title="Exposure %",showlegend=False,yaxis=dict(gridcolor=C["grid"],range=[0,max(edf["Exp"].max()*1.2,130)]))
            st.plotly_chart(fig,use_container_width=True)
        else: st.info("No data.")
        st.markdown("</div>",unsafe_allow_html=True)

    st.markdown(f'<div class="panel"><div class="panel-title">📖 Allowed Exposure Hours</div>',unsafe_allow_html=True)
    t='<table class="styled-table"><tr><th>Hazard</th><th>Max Daily Hours</th><th>Recommended Break</th></tr>'
    for _,r in allowed_hours_df.iterrows():
        t+=f'<tr><td style="color:{C["text1"]}!important;font-weight:700">{HI.get(r["HazardType"],"📊")} {HD.get(r["HazardType"],r["HazardType"])}</td><td style="color:{C["text2"]}!important">{r["MaxDailyHours"]} hours</td><td style="color:{C["text2"]}!important">{r["RecommendedBreak"]}</td></tr>'
    t+='</table></div>'
    st.markdown(t,unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# TAB 6: ALERTS (NEW)
# ═══════════════════════════════════════════════════
with tab6:
    st.markdown(f'<div class="panel"><div class="panel-title">🚨 Alert Center — Exposure Limit Events</div>',unsafe_allow_html=True)

    alerts_df = generate_alerts_log()

    if len(alerts_df) > 0:
        # Filters
        af1,af2,af3 = st.columns(3)
        with af1:
            a_status = st.selectbox("Filter by Status", ["All","Critical","Warning"], key="a_st")
        with af2:
            a_zone = st.selectbox("Filter by Zone", ["All"] + zones_df["ZoneName"].tolist(), key="a_zn")
        with af3:
            a_hazard = st.selectbox("Filter by Hazard", ["All"] + [HD.get(h,h) for h in HO], key="a_hz")

        filt = alerts_df.copy()
        if a_status != "All": filt = filt[filt["Status"]==a_status]
        if a_zone != "All": filt = filt[filt["Zone"]==a_zone]
        if a_hazard != "All":
            hz_key = next((k for k,v in HD.items() if v==a_hazard), a_hazard)
            filt = filt[filt["Hazard"]==hz_key]

        # Summary KPIs
        ak1,ak2,ak3,ak4 = st.columns(4)
        total_alerts = len(filt)
        crit_alerts = len(filt[filt["Status"]=="Critical"])
        warn_alerts = len(filt[filt["Status"]=="Warning"])
        unique_zones = filt["Zone"].nunique()
        with ak1: st.markdown(rmkpi("📊","Total Alerts",total_alerts,C["safe_bg"]),unsafe_allow_html=True)
        with ak2: st.markdown(rmkpi("🚨","Critical",crit_alerts,C["crit_bg"]),unsafe_allow_html=True)
        with ak3: st.markdown(rmkpi("⚠️","Warning",warn_alerts,C["warn_bg"]),unsafe_allow_html=True)
        with ak4: st.markdown(rmkpi("🏭","Affected Zones",unique_zones,C["safe_bg"]),unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>",unsafe_allow_html=True)

        # Alerts by day chart
        al1,al2 = st.columns([6,4])
        with al1:
            st.markdown(f'<div class="panel"><div class="panel-title">📅 Alerts Over Time</div>',unsafe_allow_html=True)
            filt_copy = filt.copy()
            filt_copy["Date"] = filt_copy["DateTime"].dt.date
            daily = filt_copy.groupby(["Date","Status"]).size().reset_index(name="Count")
            fig = go.Figure()
            for s_name, s_color in [("Critical","#C62828"),("Warning","#F9A825")]:
                sd = daily[daily["Status"]==s_name]
                if len(sd)>0:
                    fig.add_trace(go.Bar(x=sd["Date"],y=sd["Count"],name=s_name,marker_color=s_color))
            fig.update_layout(**PL,height=300,barmode="stack",yaxis_title="Alert Count",
                yaxis=dict(gridcolor=C["grid"]),legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("</div>",unsafe_allow_html=True)

        with al2:
            st.markdown(f'<div class="panel"><div class="panel-title">📊 Alerts by Hazard</div>',unsafe_allow_html=True)
            hz_counts = filt.groupby("Hazard").size().reset_index(name="Count")
            hz_counts["Label"] = hz_counts["Hazard"].map(HD)
            fig = go.Figure(data=[go.Pie(labels=hz_counts["Label"],values=hz_counts["Count"],hole=0.5,
                marker_colors=["#1565C0","#E65100","#6A1B9A","#2E7D32"][:len(hz_counts)],
                textinfo="label+value",textfont=dict(size=12))])
            fig.update_layout(**PL,height=300,showlegend=False)
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("</div>",unsafe_allow_html=True)

        # Alert log
        st.markdown(f'<div class="panel"><div class="panel-title">📜 Alert Log (showing latest 50)</div>',unsafe_allow_html=True)
        for _,a in filt.head(50).iterrows():
            item_class = "warn-item" if a["Status"]=="Warning" else ""
            dt_str = a["DateTime"].strftime("%Y-%m-%d %H:%M") if pd.notna(a["DateTime"]) else "N/A"
            badge_css = f"background:{sbg(a['Status'])};color:{stxt(a['Status'])}"
            st.markdown(f'''
            <div class="alert-item {item_class}">
                <div class="alert-time">{dt_str}</div>
                <div class="alert-text">{HI.get(a["Hazard"],"")} {a["Zone"]} — {HD.get(a["Hazard"],a["Hazard"])}: {a["Value"]} {a["Unit"]} ({a["ExposurePct"]:.0%})</div>
                <div style="margin-left:auto"><span class="alert-badge" style="{badge_css}">{a["Status"]}</span></div>
            </div>''', unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

    else:
        st.success("✅ No alerts found. All readings are within safe limits!")

    st.markdown("</div>",unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# PDF EXPORT BUTTON (in sidebar or bottom)
# ═══════════════════════════════════════════════════
st.markdown("---")
st.markdown(f"### 📄 Export Report")
if st.button("📥 Generate PDF Summary Report", key="pdf_btn"):
    # Build a simple HTML report and offer download
    stats_all = zhstats()
    report_html = f"""
    <html><head><style>
    body{{font-family:Inter,sans-serif;padding:40px;color:#0B3558}}
    h1{{color:#0B3558;border-bottom:3px solid #0F4C75;padding-bottom:10px}}
    h2{{color:#0F4C75;margin-top:30px}}
    table{{width:100%;border-collapse:collapse;margin:15px 0}}
    th{{background:#0B3558;color:white;padding:10px;text-align:left}}
    td{{padding:8px 10px;border-bottom:1px solid #EEE}}
    .safe{{color:#2E7D32;font-weight:bold}} .warning{{color:#F57F17;font-weight:bold}} .critical{{color:#C62828;font-weight:bold}}
    </style></head><body>
    <h1>🛡️ ExpoInsight — Safety Report</h1>
    <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
    <p><strong>Total Workers:</strong> {workers_df["WorkerID"].nunique()} | <strong>Workers at Risk:</strong> {w_risk()} | <strong>Safe Zones:</strong> {sz_count()}/{len(zones_df)}</p>

    <h2>Overall Exposure Summary</h2>
    <table><tr><th>Hazard</th><th>Current Value</th><th>Limit</th><th>Exposure %</th><th>Status</th></tr>"""
    for s in stats_all:
        cls = scss(s["Status"])
        report_html += f'<tr><td>{s["Icon"]} {s["DisplayName"]}</td><td>{s["CurrentValue"]} {s["Unit"]}</td><td>{s["Limit"]} {s["Unit"]}</td><td class="{cls}">{s["ExposurePct"]:.0%}</td><td class="{cls}">{s["Status"]}</td></tr>'
    report_html += "</table>"

    report_html += "<h2>Zone Status</h2><table><tr><th>Zone</th><th>Type</th><th>Status</th><th>Max Exposure</th></tr>"
    for _,z in zones_df.iterrows():
        zs=zhstats(z["ZoneID"]); mx=max(s["ExposurePct"] for s in zs)
        ost=zoverall(z["ZoneID"]); cls=scss(ost)
        report_html += f'<tr><td>{z["ZoneName"]}</td><td>{z["ZoneType"]}</td><td class="{cls}">{ost}</td><td class="{cls}">{mx:.0%}</td></tr>'
    report_html += "</table>"

    if len(crit_z_names) > 0:
        report_html += f"<h2>⚠️ Critical Zones Requiring Immediate Action</h2><ul>"
        for czn in crit_z_names:
            report_html += f"<li><strong>{czn}</strong></li>"
        report_html += "</ul>"

    report_html += "</body></html>"

    st.download_button(
        label="📥 Download HTML Report",
        data=report_html,
        file_name=f"ExpoInsight_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
        mime="text/html",
    )
    st.success("✅ Report generated! Click the download button above.")


# ═══════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════
st.markdown(f'<div style="text-align:center;padding:32px 0 12px;color:{C["text3"]};font-size:12px">🛡️ <strong style="color:{C["text1"]}">ExpoInsight V3</strong> — Occupational Health Monitoring · Auto-refresh 30s · © 2025</div>',unsafe_allow_html=True)
