import streamlit as st
import pandas as pd
import io
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Project Avyntis",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
html, body, [class*="css"] { background: #0d1117 !important; color: #e6edf3 !important; }
.main .block-container { padding: 1.5rem 2rem 3rem; max-width: 100%; }

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* === UPLOAD SCREEN === */
.upload-screen {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    min-height: 80vh; text-align: center; padding: 2rem;
}
.upload-logo { font-size: 3rem; margin-bottom: 1rem; }
.upload-title { font-size: 2.2rem; font-weight: 700; color: #e6edf3; margin-bottom: 0.4rem; }
.upload-sub { font-size: 1rem; color: #7d8590; margin-bottom: 2.5rem; }
.upload-zone {
    border: 1.5px dashed #30363d; border-radius: 16px;
    padding: 3rem 4rem; background: #161b22;
    width: 100%; max-width: 540px;
}
.upload-zone-icon { font-size: 2rem; margin-bottom: 0.75rem; }
.upload-zone p { color: #7d8590; font-size: 0.9rem; margin: 0; }
.upload-zone strong { color: #58a6ff; }
.col-list {
    display: flex; flex-wrap: wrap; gap: 6px; justify-content: center;
    margin-top: 1.5rem; max-width: 540px;
}
.col-pill {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 20px; padding: 3px 10px;
    font-size: 0.72rem; color: #8b949e;
}

/* === TOP NAV === */
.topnav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.75rem 0 1.25rem;
    border-bottom: 1px solid #21262d;
    margin-bottom: 1.5rem;
}
.topnav-brand { display: flex; align-items: center; gap: 10px; }
.topnav-brand .icon { font-size: 1.4rem; }
.topnav-brand .name { font-size: 1.15rem; font-weight: 700; color: #e6edf3; }
.topnav-brand .tag { font-size: 0.75rem; color: #7d8590; margin-left: 4px; }
.topnav-meta { font-size: 0.8rem; color: #8b949e; }
.badge-file { background: #1f2937; border: 1px solid #374151; border-radius: 20px; padding: 3px 10px; color: #58a6ff; font-size: 0.75rem; }

/* === KPI CARDS === */
.kpi-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 1.5rem; }
.kpi-card {
    background: #161b22; border: 1px solid #21262d;
    border-radius: 12px; padding: 1.1rem 1.25rem;
    position: relative; overflow: hidden;
}
.kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 3px; border-radius: 12px 12px 0 0;
}
.kpi-card.blue::before { background: #58a6ff; }
.kpi-card.green::before { background: #3fb950; }
.kpi-card.amber::before { background: #d29922; }
.kpi-card.red::before { background: #f85149; }
.kpi-card.purple::before { background: #bc8cff; }
.kpi-label { font-size: 0.72rem; color: #7d8590; font-weight: 500; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.6rem; }
.kpi-value { font-size: 1.9rem; font-weight: 700; color: #e6edf3; line-height: 1; margin-bottom: 0.35rem; }
.kpi-value.green { color: #3fb950; }
.kpi-value.red { color: #f85149; }
.kpi-value.amber { color: #d29922; }
.kpi-value.blue { color: #58a6ff; }
.kpi-sub { font-size: 0.72rem; color: #7d8590; }

/* === SECTION HEADERS === */
.section-header {
    display: flex; align-items: center; justify-content: space-between;
    margin: 1.75rem 0 0.75rem;
}
.section-title { font-size: 0.95rem; font-weight: 600; color: #e6edf3; }
.section-sub { font-size: 0.8rem; color: #7d8590; }

/* === ALERT STRIP === */
.alert-strip {
    display: flex; align-items: center; gap: 12px;
    background: #1a1115; border: 1px solid #6e2a2a;
    border-left: 4px solid #f85149;
    border-radius: 10px; padding: 0.75rem 1rem;
    margin-bottom: 1.25rem; font-size: 0.85rem;
}
.alert-strip .dot { width: 8px; height: 8px; border-radius: 50%; background: #f85149; flex-shrink: 0; }
.alert-strip .text { color: #e6edf3; }
.alert-strip .count { font-weight: 700; color: #f85149; }
.alert-strip .warn-count { font-weight: 700; color: #d29922; }

/* === FILTER BAR === */
.filter-bar {
    display: flex; gap: 12px; align-items: center;
    background: #161b22; border: 1px solid #21262d;
    border-radius: 10px; padding: 0.85rem 1.1rem;
    margin-bottom: 1.25rem; flex-wrap: wrap;
}
.filter-label { font-size: 0.75rem; color: #7d8590; font-weight: 500; white-space: nowrap; }

/* === TABLE OVERRIDES === */
.stDataFrame { border-radius: 10px !important; border: 1px solid #21262d !important; overflow: hidden; }
.stDataFrame [data-testid="stDataFrameResizable"] { background: #161b22 !important; }
div[data-testid="stDataFrame"] > div { background: #161b22 !important; }

/* === PLOTLY OVERRIDES === */
.js-plotly-plot { border-radius: 12px; overflow: hidden; }

/* === STREAMLIT WIDGETS === */
div[data-baseweb="select"] > div { background: #161b22 !important; border: 1px solid #30363d !important; border-radius: 8px !important; color: #e6edf3 !important; }
div[data-baseweb="select"] span { color: #e6edf3 !important; }
div[data-baseweb="select"] svg { color: #7d8590 !important; }
div[data-baseweb="popover"] { background: #161b22 !important; border: 1px solid #30363d !important; }
.stMultiSelect [data-baseweb="tag"] { background: #1f3a5f !important; color: #58a6ff !important; border: none !important; }
.stDownloadButton button {
    background: #21262d !important; border: 1px solid #30363d !important;
    color: #e6edf3 !important; border-radius: 8px !important;
    font-size: 0.82rem !important; padding: 0.45rem 1rem !important;
    transition: all .15s !important;
}
.stDownloadButton button:hover { background: #30363d !important; border-color: #58a6ff !important; }
.stFileUploader {
    background: #161b22 !important; border: 1.5px dashed #30363d !important;
    border-radius: 12px !important;
}
label[data-testid="stWidgetLabel"] { color: #7d8590 !important; font-size: 0.78rem !important; font-weight: 500 !important; }

/* === TABS === */
.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid #21262d; gap: 0; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: #7d8590 !important; border: none !important; border-bottom: 2px solid transparent !important; padding: 0.6rem 1.1rem !important; font-size: 0.85rem !important; }
.stTabs [aria-selected="true"] { color: #e6edf3 !important; border-bottom-color: #58a6ff !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 1rem !important; }

/* === STATUS CHIPS === */
.chip { display: inline-block; padding: 2px 8px; border-radius: 20px; font-size: 0.72rem; font-weight: 600; }
.chip-green  { background: #122117; color: #3fb950; border: 1px solid #1a3a25; }
.chip-red    { background: #2d1010; color: #f85149; border: 1px solid #4a1515; }
.chip-amber  { background: #2a1e0a; color: #d29922; border: 1px solid #3d2d0e; }

/* === DIVIDER === */
.divider { border: none; border-top: 1px solid #21262d; margin: 1.5rem 0; }

/* === VALIDATION BOX === */
.val-box { border-radius: 8px; padding: 0.75rem 1rem; font-size: 0.83rem; margin-top: 1rem; }
.val-ok   { background: #0d2010; border: 1px solid #1a3a25; color: #3fb950; }
.val-err  { background: #2d1010; border: 1px solid #4a1515; color: #f85149; }

/* streamlit spacing fixes */
.element-container { margin-bottom: 0 !important; }
div[data-testid="column"] { padding: 0 6px !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 📦 Column Mapping & Schema
# ==========================================
COL_MAPPING = {
    'Substance': 'ItemType',
    'Rate per Flight Hour': 'UsageRatePerFH',
    'Total flight  hours': 'TotalFlightHours',
    'Total flight hours': 'TotalFlightHours',
    'Rate per flight cycle': 'UsageRatePerFC',
    'Total  flight Cycle': 'TotalFlightCycles',
    'Total flight Cycle': 'TotalFlightCycles',
    'Quantity in Schedule Check': 'ScheduledQtyPerCheck',
    'Number of Checks': 'NumberOfChecks',
    'Expected Failure Events': 'ExpectedFailureEvents',
    'Consumables Used per Event': 'UnscheduledQtyPerEvent',
    'Safety Buffer': 'SafetyBufferPct',
    'Current Stock': 'CurrentStock',
    'MRO Company': 'MROCompany',
}

REQUIRED_COLS = [
    'MROCompany', 'Fleet', 'Consumable', 'ItemType', 'Unit',
    'UsageRatePerFH', 'TotalFlightHours', 'UsageRatePerFC', 'TotalFlightCycles',
    'ScheduledQtyPerCheck', 'NumberOfChecks', 'ExpectedFailureEvents',
    'UnscheduledQtyPerEvent', 'SafetyBufferPct', 'CurrentStock'
]

PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter, sans-serif', color='#8b949e', size=11),
    margin=dict(l=16, r=16, t=32, b=16),
    xaxis=dict(gridcolor='#21262d', linecolor='#30363d', zerolinecolor='#21262d'),
    yaxis=dict(gridcolor='#21262d', linecolor='#30363d', zerolinecolor='#21262d'),
    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='#30363d'),
    colorway=['#58a6ff','#3fb950','#d29922','#f85149','#bc8cff','#79c0ff'],
)

# ==========================================
# 🧮 Forecasting Logic
# ==========================================
def classify_alert(total_demand, current_stock):
    if total_demand <= 0:
        return "Normal"
    pct = (current_stock / total_demand) * 100
    if pct < 20: return "Critical"
    if pct < 50: return "Warning"
    return "Normal"

def calculate_demand(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    num_cols = [c for c in REQUIRED_COLS if c not in
                ['MROCompany', 'Fleet', 'Consumable', 'ItemType', 'Unit']]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    df['FH_Demand']        = np.where(df['ItemType'] == 'Liquid', df['UsageRatePerFH'] * df['TotalFlightHours'], 0)
    df['FC_Demand']        = np.where(df['ItemType'] == 'Hard',   df['UsageRatePerFC'] * df['TotalFlightCycles'], 0)
    df['Sched_Demand']     = df['ScheduledQtyPerCheck'] * df['NumberOfChecks']
    df['Unsched_Demand']   = df['ExpectedFailureEvents'] * df['UnscheduledQtyPerEvent']
    df['Base_Demand']      = df['FH_Demand'] + df['FC_Demand'] + df['Sched_Demand'] + df['Unsched_Demand']
    df['Total_Demand']     = (df['Base_Demand'] * (1 + df['SafetyBufferPct'])).round(2)
    df['Stock_Status']     = np.where(df['CurrentStock'] >= df['Total_Demand'], 'In Stock', 'Short')
    df['Coverage_Pct']     = np.where(df['Total_Demand'] > 0,
                                       (df['CurrentStock'] / df['Total_Demand'] * 100).round(1), 100.0)
    df['Reorder_Qty']      = np.where(df['CurrentStock'] < df['Total_Demand'],
                                       (df['Total_Demand'] - df['CurrentStock']).round(2), 0)
    df['Alert_Status']     = df.apply(lambda r: classify_alert(r['Total_Demand'], r['CurrentStock']), axis=1)
    return df

# ==========================================
# 📥 Load File Helper
# ==========================================
def load_file(f):
    if f.name.endswith('.csv'):
        df = pd.read_csv(f)
    else:
        df = pd.read_excel(f)
    df.columns = df.columns.str.strip()
    df.rename(columns=COL_MAPPING, inplace=True)
    if 'ForecastPeriod' not in df.columns:
        df['ForecastPeriod'] = 'Monthly'
    missing = set(REQUIRED_COLS) - set(df.columns)
    return df, missing

# ==========================================
# 🚦 UPLOAD SCREEN (no file uploaded)
# ==========================================
if 'df_raw' not in st.session_state:
    st.markdown("""
    <div class="upload-screen">
        <div class="upload-logo">✈️</div>
        <div class="upload-title">Project Avyntis</div>
        <div class="upload-sub">Consumable Demand Forecasting & Procurement Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    col_c, col_r = st.columns([1, 2, 1])[:2]  # center trick
    _, center, _ = st.columns([1, 1.4, 1])
    with center:
        uploaded = st.file_uploader("", type=["xlsx", "csv"], label_visibility="collapsed")
        st.markdown("""
        <p style="text-align:center; color:#7d8590; font-size:0.8rem; margin-top:0.5rem;">
        Supports <strong style="color:#58a6ff">.xlsx</strong> and <strong style="color:#58a6ff">.csv</strong> formats
        </p>
        <div class="col-list">
            <span class="col-pill">MRO Company</span><span class="col-pill">Fleet</span>
            <span class="col-pill">Consumable</span><span class="col-pill">Substance</span>
            <span class="col-pill">Unit</span><span class="col-pill">Rate per Flight Hour</span>
            <span class="col-pill">Total flight hours</span><span class="col-pill">Rate per flight cycle</span>
            <span class="col-pill">Total flight Cycle</span><span class="col-pill">Qty in Schedule Check</span>
            <span class="col-pill">Number of Checks</span><span class="col-pill">Expected Failure Events</span>
            <span class="col-pill">Consumables Used per Event</span><span class="col-pill">Safety Buffer</span>
            <span class="col-pill">Current Stock</span>
        </div>
        """, unsafe_allow_html=True)

    if uploaded:
        df_raw, missing = load_file(uploaded)
        if missing:
            st.error(f"Missing columns: **{', '.join(sorted(missing))}**")
        else:
            st.session_state['df_raw'] = df_raw
            st.session_state['filename'] = uploaded.name
            st.rerun()
    st.stop()

# ==========================================
# 📊 MAIN DASHBOARD
# ==========================================
df_raw  = st.session_state['df_raw']
fname   = st.session_state.get('filename', 'dataset')

# ── Top Nav ──────────────────────────────
n1, n2 = st.columns([3, 1])
with n1:
    st.markdown(f"""
    <div class="topnav">
        <div class="topnav-brand">
            <span class="icon">✈️</span>
            <span class="name">Project Avyntis</span>
            <span class="tag">Demand Forecasting</span>
        </div>
    </div>""", unsafe_allow_html=True)
with n2:
    st.markdown(f"""
    <div style="display:flex;justify-content:flex-end;align-items:center;gap:10px;padding-top:0.75rem">
        <span class="badge-file">📄 {fname}</span>
    </div>""", unsafe_allow_html=True)
    if st.button("↩ Upload new file", use_container_width=False):
        del st.session_state['df_raw']
        st.rerun()

# ── Filters ──────────────────────────────
mro_opts  = sorted(df_raw['MROCompany'].dropna().unique())
fleet_opts = sorted(df_raw['Fleet'].dropna().unique())
item_opts  = ['All', 'Liquid', 'Hard']
alert_opts = ['All', 'Critical', 'Warning', 'Normal']

f1, f2, f3, f4 = st.columns([2, 2, 1.2, 1.2])
with f1:
    sel_mro    = st.multiselect("MRO Company", mro_opts,  default=mro_opts,  key="mro")
with f2:
    sel_fleet  = st.multiselect("Fleet", fleet_opts, default=fleet_opts, key="fleet")
with f3:
    sel_type   = st.selectbox("Item Type", item_opts,  index=0, key="itype")
with f4:
    sel_alert  = st.selectbox("Alert Status", alert_opts, index=0, key="astatus")

df_f = df_raw[df_raw['MROCompany'].isin(sel_mro) & df_raw['Fleet'].isin(sel_fleet)]
if sel_type != 'All':
    df_f = df_f[df_f['ItemType'] == sel_type]

df = calculate_demand(df_f)

if sel_alert != 'All':
    df_view = df[df['Alert_Status'] == sel_alert]
else:
    df_view = df

# ── Alert Strip ──────────────────────────
crit  = int((df['Alert_Status'] == 'Critical').sum())
warn  = int((df['Alert_Status'] == 'Warning').sum())
if crit > 0 or warn > 0:
    st.markdown(f"""
    <div class="alert-strip">
        <div class="dot"></div>
        <div class="text">
            <span class="count">{crit} Critical</span> items below 20% stock coverage &nbsp;·&nbsp;
            <span class="warn-count">{warn} Warning</span> items below 50% coverage — immediate procurement review required
        </div>
    </div>""", unsafe_allow_html=True)

# ── KPI Cards ────────────────────────────
total_demand  = df['Total_Demand'].sum()
instock       = int((df['Stock_Status'] == 'In Stock').sum())
short         = int((df['Stock_Status'] == 'Short').sum())
reorder_total = df['Reorder_Qty'].sum()
total_items   = len(df)

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card blue">
        <div class="kpi-label">Total Forecasted Demand</div>
        <div class="kpi-value blue">{total_demand:,.1f}</div>
        <div class="kpi-sub">across {total_items} items</div>
    </div>
    <div class="kpi-card green">
        <div class="kpi-label">In Stock</div>
        <div class="kpi-value green">{instock}</div>
        <div class="kpi-sub">items fully covered</div>
    </div>
    <div class="kpi-card amber">
        <div class="kpi-label">Short / At Risk</div>
        <div class="kpi-value amber">{short}</div>
        <div class="kpi-sub">items need reorder</div>
    </div>
    <div class="kpi-card red">
        <div class="kpi-label">Critical Alerts</div>
        <div class="kpi-value red">{crit}</div>
        <div class="kpi-sub">&lt;20% stock coverage</div>
    </div>
    <div class="kpi-card purple">
        <div class="kpi-label">Total Reorder Qty</div>
        <div class="kpi-value">{reorder_total:,.1f}</div>
        <div class="kpi-sub">units to procure</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Charts Row ───────────────────────────
ch1, ch2, ch3 = st.columns([1.2, 1.2, 1])

with ch1:
    st.markdown('<div class="section-title">Demand vs Stock by Item</div>', unsafe_allow_html=True)
    fig1 = go.Figure()
    color_map = {'Critical': '#f85149', 'Warning': '#d29922', 'Normal': '#3fb950'}
    df_sorted = df.sort_values('Total_Demand', ascending=True).tail(20)
    fig1.add_trace(go.Bar(
        y=df_sorted['Consumable'], x=df_sorted['Total_Demand'],
        name='Demand', orientation='h',
        marker_color=[color_map[s] for s in df_sorted['Alert_Status']],
        opacity=0.85,
    ))
    fig1.add_trace(go.Bar(
        y=df_sorted['Consumable'], x=df_sorted['CurrentStock'],
        name='Current Stock', orientation='h',
        marker_color='#30363d', opacity=0.9,
    ))
    fig1.update_layout(
        **PLOTLY_LAYOUT,
        barmode='overlay', height=340,
        legend=dict(orientation='h', y=1.08, x=0, bgcolor='rgba(0,0,0,0)'),
        xaxis_title=None, yaxis_title=None,
        yaxis=dict(tickfont=dict(size=10), gridcolor='#21262d'),
    )
    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

with ch2:
    st.markdown('<div class="section-title">Stock Coverage by Fleet</div>', unsafe_allow_html=True)
    fleet_cov = df.groupby('Fleet').apply(
        lambda g: (g['CurrentStock'].sum() / g['Total_Demand'].sum() * 100) if g['Total_Demand'].sum() > 0 else 100
    ).reset_index(name='Coverage_Pct').round(1)
    fleet_cov['color'] = fleet_cov['Coverage_Pct'].apply(
        lambda v: '#f85149' if v < 20 else ('#d29922' if v < 50 else '#3fb950')
    )
    fig2 = go.Figure(go.Bar(
        x=fleet_cov['Fleet'], y=fleet_cov['Coverage_Pct'],
        marker_color=fleet_cov['color'],
        text=fleet_cov['Coverage_Pct'].astype(str) + '%',
        textposition='outside', textfont=dict(size=10, color='#8b949e'),
    ))
    fig2.add_hline(y=50, line_dash='dash', line_color='#d29922', opacity=0.5, annotation_text='Warning (50%)', annotation_font_size=9)
    fig2.add_hline(y=20, line_dash='dash', line_color='#f85149', opacity=0.5, annotation_text='Critical (20%)', annotation_font_size=9)
    fig2.update_layout(**PLOTLY_LAYOUT, height=340, yaxis_title='Coverage %', yaxis_range=[0, max(fleet_cov['Coverage_Pct'].max() * 1.2, 110)])
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

with ch3:
    st.markdown('<div class="section-title">Alert Breakdown</div>', unsafe_allow_html=True)
    alert_counts = df['Alert_Status'].value_counts().reset_index()
    alert_counts.columns = ['Status', 'Count']
    color_seq = {'Critical': '#f85149', 'Warning': '#d29922', 'Normal': '#3fb950'}
    fig3 = go.Figure(go.Pie(
        labels=alert_counts['Status'],
        values=alert_counts['Count'],
        hole=0.65,
        marker_colors=[color_seq.get(s, '#58a6ff') for s in alert_counts['Status']],
        textinfo='label+percent',
        textfont=dict(size=10, color='#8b949e'),
        hovertemplate='%{label}: %{value} items<extra></extra>',
    ))
    fig3.update_layout(
        **PLOTLY_LAYOUT, height=340,
        showlegend=False,
        annotations=[dict(text=f'<b>{total_items}</b><br>items', x=0.5, y=0.5,
                          font=dict(size=14, color='#e6edf3'), showarrow=False)]
    )
    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

# ── Demand Composition Chart ─────────────
st.markdown('<div class="section-title" style="margin-top:1.5rem">Demand Composition by MRO Company</div>', unsafe_allow_html=True)

mro_comp = df.groupby('MROCompany')[['FH_Demand','FC_Demand','Sched_Demand','Unsched_Demand']].sum().reset_index()
fig4 = go.Figure()
comp_colors = {'FH_Demand': '#58a6ff', 'FC_Demand': '#3fb950', 'Sched_Demand': '#d29922', 'Unsched_Demand': '#bc8cff'}
comp_labels = {'FH_Demand': 'Flight Hour', 'FC_Demand': 'Flight Cycle', 'Sched_Demand': 'Scheduled', 'Unsched_Demand': 'Unscheduled'}
for col, color in comp_colors.items():
    fig4.add_trace(go.Bar(
        name=comp_labels[col], x=mro_comp['MROCompany'], y=mro_comp[col].round(1),
        marker_color=color, opacity=0.9,
    ))
fig4.update_layout(**PLOTLY_LAYOUT, barmode='stack', height=280,
                   legend=dict(orientation='h', y=1.12, x=0))
st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})

# ── Tabs: Data Tables ─────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["📋  Full Forecast Matrix", "🚨  Procurement Alerts", "🟢  In-Stock Items"])

DISPLAY_COLS = {
    'MROCompany': 'MRO Company', 'Fleet': 'Fleet', 'Consumable': 'Consumable',
    'ItemType': 'Type', 'Unit': 'Unit',
    'FH_Demand': 'FH Demand', 'FC_Demand': 'FC Demand',
    'Sched_Demand': 'Scheduled', 'Unsched_Demand': 'Unscheduled',
    'Base_Demand': 'Base Demand', 'Total_Demand': 'Total Demand',
    'CurrentStock': 'Current Stock', 'Coverage_Pct': 'Coverage %',
    'Reorder_Qty': 'Reorder Qty', 'Alert_Status': 'Status'
}

def style_table(df_in, cols):
    sub = df_in[list(cols.keys())].rename(columns=cols).copy()
    if 'Coverage %' in sub.columns:
        sub['Coverage %'] = sub['Coverage %'].apply(lambda v: f"{v:.1f}%")
    return sub

with tab1:
    full_df = style_table(df_view, DISPLAY_COLS)
    st.dataframe(full_df, use_container_width=True, hide_index=True, height=380)

with tab2:
    alert_df = df_view[df_view['Alert_Status'].isin(['Critical', 'Warning'])]
    if alert_df.empty:
        st.markdown('<p style="color:#3fb950;padding:1rem 0">✓ No procurement alerts for selected filters.</p>', unsafe_allow_html=True)
    else:
        alert_show_cols = {
            'MROCompany': 'MRO Company', 'Fleet': 'Fleet', 'Consumable': 'Consumable',
            'ItemType': 'Type', 'Unit': 'Unit', 'CurrentStock': 'Stock',
            'Total_Demand': 'Demand', 'Coverage_Pct': 'Coverage %',
            'Reorder_Qty': 'Reorder Qty', 'Alert_Status': 'Status'
        }
        st.dataframe(style_table(alert_df.sort_values('Coverage_Pct'), alert_show_cols),
                     use_container_width=True, hide_index=True, height=380)

with tab3:
    instock_df = df_view[df_view['Stock_Status'] == 'In Stock']
    if instock_df.empty:
        st.markdown('<p style="color:#d29922;padding:1rem 0">⚠ No fully in-stock items for selected filters.</p>', unsafe_allow_html=True)
    else:
        ins_cols = {
            'MROCompany': 'MRO Company', 'Fleet': 'Fleet', 'Consumable': 'Consumable',
            'ItemType': 'Type', 'Unit': 'Unit', 'CurrentStock': 'Stock',
            'Total_Demand': 'Demand', 'Coverage_Pct': 'Coverage %', 'Alert_Status': 'Status'
        }
        st.dataframe(style_table(instock_df, ins_cols),
                     use_container_width=True, hide_index=True, height=380)

# ── Coverage Scatter ─────────────────────
st.markdown('<div class="section-title" style="margin-top:1.75rem">Stock Coverage Map — All Items</div>', unsafe_allow_html=True)
st.markdown('<p style="color:#7d8590;font-size:0.8rem;margin-bottom:0.5rem">Bubble size = reorder quantity. Hover for details.</p>', unsafe_allow_html=True)

fig5 = px.scatter(
    df, x='Total_Demand', y='CurrentStock',
    color='Alert_Status',
    color_discrete_map={'Critical': '#f85149', 'Warning': '#d29922', 'Normal': '#3fb950'},
    size=np.where(df['Reorder_Qty'] > 0, df['Reorder_Qty'], df['Total_Demand'] * 0.05),
    size_max=40,
    hover_name='Consumable',
    hover_data={'Fleet': True, 'MROCompany': True, 'Total_Demand': ':.1f',
                'CurrentStock': ':.1f', 'Coverage_Pct': ':.1f', 'Alert_Status': False},
    labels={'Total_Demand': 'Total Demand', 'CurrentStock': 'Current Stock', 'Alert_Status': 'Status'},
)
fig5.add_shape(type='line', x0=0, y0=0, x1=df['Total_Demand'].max()*1.1, y1=df['Total_Demand'].max()*1.1,
               line=dict(color='#3fb950', dash='dash', width=1), opacity=0.5)
fig5.add_annotation(x=df['Total_Demand'].max()*0.8, y=df['Total_Demand'].max()*0.85,
                    text='Stock = Demand', font=dict(size=9, color='#3fb950'), showarrow=False)
fig5.update_layout(**PLOTLY_LAYOUT, height=380,
                   legend=dict(orientation='h', y=1.05, x=0))
st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False})

# ── Export Row ───────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Export Reports</div>', unsafe_allow_html=True)
e1, e2, e3, e4 = st.columns(4)

def to_excel(df_exp):
    buf = io.BytesIO()
    df_exp.to_excel(buf, index=False)
    return buf.getvalue()

with e1:
    st.download_button("📥 Full Forecast", data=to_excel(df), file_name="avyntis_forecast.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       use_container_width=True)
with e2:
    alert_exp = df[df['Alert_Status'].isin(['Critical', 'Warning'])]
    st.download_button("🚨 Alert Report", data=to_excel(alert_exp), file_name="avyntis_alerts.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       use_container_width=True, disabled=alert_exp.empty)
with e3:
    reorder_exp = df[df['Reorder_Qty'] > 0][['MROCompany','Fleet','Consumable','Unit','Reorder_Qty','Alert_Status']]
    st.download_button("🛒 Reorder List", data=to_excel(reorder_exp), file_name="avyntis_reorder.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       use_container_width=True, disabled=reorder_exp.empty)
with e4:
    instock_exp = df[df['Stock_Status'] == 'In Stock']
    st.download_button("✅ In-Stock List", data=to_excel(instock_exp), file_name="avyntis_instock.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       use_container_width=True, disabled=instock_exp.empty)

# ── Validation ───────────────────────────
errs = []
for _, r in df.iterrows():
    exp = round(r['Base_Demand'] * (1 + r['SafetyBufferPct']), 2)
    if abs(r['Total_Demand'] - exp) > 0.05:
        errs.append(f"{r['Consumable']} ({r['Fleet']}): buffer mismatch")
    if r['Alert_Status'] == 'Critical' and r['Total_Demand'] > 0:
        if (r['CurrentStock'] / r['Total_Demand']) >= 0.2:
            errs.append(f"{r['Consumable']} ({r['Fleet']}): alert misclassified")

if errs:
    st.markdown('<div class="val-box val-err">❌ Validation issues:<br>' + '<br>'.join(errs) + '</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="val-box val-ok">✓ All calculations validated — no logic errors detected</div>', unsafe_allow_html=True)
