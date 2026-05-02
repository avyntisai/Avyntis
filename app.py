import io
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

# ============================================================
# App Config
# ============================================================
APP_TITLE = "Project Avyntis"
APP_ICON = "✈️"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# Styling (CSS)
# ============================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
html, body, [class*="css"] { background: #0d1117 !important; color: #e6edf3 !important; }
.main .block-container { padding: 1.5rem 2rem 3rem; max-width: 100%; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

.upload-screen { display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:78vh; text-align:center; padding:2rem; }
.upload-logo { font-size:3rem; margin-bottom:1rem; }
.upload-title { font-size:2.2rem; font-weight:700; color:#e6edf3; margin-bottom:0.4rem; }
.upload-sub { font-size:1rem; color:#7d8590; margin-bottom:2rem; }
.col-list { display:flex; flex-wrap:wrap; gap:6px; justify-content:center; margin-top:1.25rem; max-width:560px; }
.col-pill { background:#161b22; border:1px solid #30363d; border-radius:20px; padding:3px 10px; font-size:0.72rem; color:#8b949e; }

.topbar { display:flex; align-items:center; justify-content:space-between; padding:0.6rem 0 1.1rem; border-bottom:1px solid #21262d; margin-bottom:1.4rem; }
.brand { display:flex; align-items:center; gap:10px; }
.brand-name { font-size:1.1rem; font-weight:700; color:#e6edf3; }
.brand-tag { font-size:0.75rem; color:#7d8590; }
.badge-file { background:#1f2937; border:1px solid #374151; border-radius:20px; padding:3px 10px; color:#58a6ff; font-size:0.75rem; }

.kpi-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:12px; margin-bottom:1.4rem; }
.kpi-card { background:#161b22; border:1px solid #21262d; border-radius:12px; padding:1.1rem 1.2rem; position:relative; overflow:hidden; }
.kpi-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; border-radius:12px 12px 0 0; }
.kpi-blue::before { background:#58a6ff; }
.kpi-green::before { background:#3fb950; }
.kpi-amber::before { background:#d29922; }
.kpi-red::before { background:#f85149; }
.kpi-purple::before { background:#bc8cff; }
.kpi-label { font-size:0.68rem; color:#7d8590; font-weight:500; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:0.55rem; }
.kpi-value { font-size:1.85rem; font-weight:700; line-height:1; margin-bottom:0.3rem; }
.kpi-sub { font-size:0.7rem; color:#7d8590; }
.v-blue  { color:#58a6ff; } .v-green { color:#3fb950; }
.v-amber { color:#d29922; } .v-red   { color:#f85149; }
.v-white { color:#e6edf3; }

.alert-strip { display:flex; align-items:center; gap:12px; background:#1a1115; border:1px solid #6e2a2a; border-left:4px solid #f85149; border-radius:10px; padding:0.7rem 1rem; margin-bottom:1.2rem; font-size:0.84rem; }
.alert-strip .dot { width:8px; height:8px; border-radius:50%; background:#f85149; flex-shrink:0; }
.cnt-red { font-weight:700; color:#f85149; }
.cnt-amb { font-weight:700; color:#d29922; }

.sec-title { font-size:0.9rem; font-weight:600; color:#e6edf3; margin:1.5rem 0 0.6rem; }
.sec-sub   { font-size:0.78rem; color:#7d8590; margin-bottom:0.5rem; margin-top:-0.4rem; }
.divider   { border:none; border-top:1px solid #21262d; margin:1.5rem 0; }
.val-ok  { background:#0d2010; border:1px solid #1a3a25; color:#3fb950; border-radius:8px; padding:0.7rem 1rem; font-size:0.82rem; margin-top:1rem; }
.val-err { background:#2d1010; border:1px solid #4a1515; color:#f85149; border-radius:8px; padding:0.7rem 1rem; font-size:0.82rem; margin-top:1rem; }

div[data-baseweb="select"]>div { background:#161b22 !important; border:1px solid #30363d !important; border-radius:8px !important; color:#e6edf3 !important; }
div[data-baseweb="select"] span { color:#e6edf3 !important; }
div[data-baseweb="popover"] { background:#161b22 !important; border:1px solid #30363d !important; }
.stMultiSelect [data-baseweb="tag"] { background:#1f3a5f !important; color:#58a6ff !important; border:none !important; }
.stDownloadButton button { background:#21262d !important; border:1px solid #30363d !important; color:#e6edf3 !important; border-radius:8px !important; font-size:0.82rem !important; }
.stDownloadButton button:hover { background:#30363d !important; border-color:#58a6ff !important; }
label[data-testid="stWidgetLabel"] { color:#7d8590 !important; font-size:0.78rem !important; font-weight:500 !important; }
.stTabs [data-baseweb="tab-list"] { background:transparent !important; border-bottom:1px solid #21262d; gap:0; }
.stTabs [data-baseweb="tab"] { background:transparent !important; color:#7d8590 !important; border:none !important; border-bottom:2px solid transparent !important; padding:0.55rem 1rem !important; font-size:0.84rem !important; }
.stTabs [aria-selected="true"] { color:#e6edf3 !important; border-bottom-color:#58a6ff !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top:1rem !important; }
.stDataFrame { border-radius:10px !important; border:1px solid #21262d !important; }
.element-container { margin-bottom:0 !important; }
div[data-testid="column"] { padding:0 6px !important; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ============================================================
# Altair Theme
# ============================================================
ALT_THEME = {
    "config": {
        "background": "#161b22",
        "view": {"stroke": "transparent"},
        "axis": {
            "domainColor": "#30363d", "gridColor": "#21262d",
            "tickColor": "#30363d", "labelColor": "#8b949e",
            "titleColor": "#7d8590", "labelFontSize": 10, "titleFontSize": 10,
        },
        "legend": {"labelColor": "#8b949e", "titleColor": "#7d8590",
                   "labelFontSize": 10, "titleFontSize": 10},
        "title": {"color": "#e6edf3", "fontSize": 12},
        "mark": {"font": "Inter, sans-serif"},
    }
}
alt.themes.register("avyntis", lambda: ALT_THEME)
alt.themes.enable("avyntis")

# ============================================================
# Schema / Column Mapping
# ============================================================
COL_MAPPING = {
    "Substance": "ItemType",
    "Rate per Flight Hour": "UsageRatePerFH",
    "Total flight  hours": "TotalFlightHours",
    "Total flight hours": "TotalFlightHours",
    "Rate per flight cycle": "UsageRatePerFC",
    "Total  flight Cycle": "TotalFlightCycles",
    "Total flight Cycle": "TotalFlightCycles",
    "Quantity in Schedule Check": "ScheduledQtyPerCheck",
    "Qty in Schedule Check": "ScheduledQtyPerCheck",
    "Number of Checks": "NumberOfChecks",
    "Expected Failure Events": "ExpectedFailureEvents",
    "Consumables Used per Event": "UnscheduledQtyPerEvent",
    "Safety Buffer": "SafetyBufferPct",
    "Current Stock": "CurrentStock",
    "MRO Company": "MROCompany",
}

REQUIRED_COLS = [
    "MROCompany", "Fleet", "Consumable", "ItemType", "Unit",
    "UsageRatePerFH", "TotalFlightHours", "UsageRatePerFC", "TotalFlightCycles",
    "ScheduledQtyPerCheck", "NumberOfChecks", "ExpectedFailureEvents",
    "UnscheduledQtyPerEvent", "SafetyBufferPct", "CurrentStock"
]

TEXT_COLS = {"MROCompany", "Fleet", "Consumable", "ItemType", "Unit"}

# ============================================================
# Helpers
# ============================================================
def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()
    df.rename(columns=COL_MAPPING, inplace=True)

    if "ItemType" in df.columns:
        df["ItemType"] = df["ItemType"].astype(str).str.strip().str.title()
        df.loc[~df["ItemType"].isin(["Liquid", "Hard"]), "ItemType"] = "Hard"

    if "ForecastPeriod" not in df.columns:
        df["ForecastPeriod"] = "Monthly"

    return df


def parse_numeric_series(s: pd.Series) -> pd.Series:
    s = s.astype(str).str.replace(",", "", regex=False).str.replace("%", "", regex=False)
    return pd.to_numeric(s, errors="coerce").fillna(0)


def normalize_safety_buffer(buf: pd.Series) -> pd.Series:
    b = parse_numeric_series(buf)
    b = np.where(b > 1, b / 100.0, b)  # accept 20 or 0.2
    b = np.clip(b, 0, 2.0)
    return pd.Series(b, index=buf.index)


def classify_alert_vectorized(total_demand: np.ndarray, current_stock: np.ndarray) -> np.ndarray:
    coverage = np.where(total_demand > 0, (current_stock / total_demand) * 100.0, 100.0)
    return np.where(coverage < 20, "Critical", np.where(coverage < 50, "Warning", "Normal"))


@st.cache_data(show_spinner=False)
def load_dataset(file_bytes: bytes, filename: str, sheet_name: str | None = None) -> tuple[pd.DataFrame, set]:
    buf = io.BytesIO(file_bytes)

    if filename.lower().endswith(".csv"):
        df = pd.read_csv(buf)
    else:
        df = pd.read_excel(buf, engine="openpyxl", sheet_name=sheet_name) if sheet_name else pd.read_excel(buf, engine="openpyxl")

    df = normalize_columns(df)
    missing = set(REQUIRED_COLS) - set(df.columns)
    return df, missing


@st.cache_data(show_spinner=False)
def calculate_demand(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for c in REQUIRED_COLS:
        if c in TEXT_COLS:
            df[c] = df[c].astype(str).str.strip()
        elif c == "SafetyBufferPct":
            df[c] = normalize_safety_buffer(df[c])
        else:
            df[c] = parse_numeric_series(df[c])

    is_liquid = df["ItemType"].eq("Liquid").to_numpy()
    is_hard = df["ItemType"].eq("Hard").to_numpy()

    fh_d = np.where(is_liquid, df["UsageRatePerFH"].to_numpy() * df["TotalFlightHours"].to_numpy(), 0.0)
    fc_d = np.where(is_hard, df["UsageRatePerFC"].to_numpy() * df["TotalFlightCycles"].to_numpy(), 0.0)
    sched_d = df["ScheduledQtyPerCheck"].to_numpy() * df["NumberOfChecks"].to_numpy()
    unsched_d = df["ExpectedFailureEvents"].to_numpy() * df["UnscheduledQtyPerEvent"].to_numpy()

    base = fh_d + fc_d + sched_d + unsched_d
    total = np.round(base * (1.0 + df["SafetyBufferPct"].to_numpy()), 2)

    stock = df["CurrentStock"].to_numpy()
    coverage = np.where(total > 0, np.round((stock / total) * 100.0, 1), 100.0)
    reorder = np.where(stock < total, np.round(total - stock, 2), 0.0)
    status = np.where(stock >= total, "In Stock", "Short")
    alert = classify_alert_vectorized(total, stock)

    df["FH_Demand"] = fh_d
    df["FC_Demand"] = fc_d
    df["Sched_Demand"] = sched_d
    df["Unsched_Demand"] = unsched_d
    df["Base_Demand"] = base
    df["Total_Demand"] = total
    df["Coverage_Pct"] = coverage
    df["Reorder_Qty"] = reorder
    df["Stock_Status"] = status
    df["Alert_Status"] = alert

    return df


def to_excel_bytes(df_exp: pd.DataFrame, sheet_name="Report") -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_exp.to_excel(writer, index=False, sheet_name=sheet_name)
    return output.getvalue()


def fmt_table(df_in: pd.DataFrame, col_map: dict) -> pd.DataFrame:
    out = df_in[list(col_map.keys())].rename(columns=col_map).copy()
    if "Coverage %" in out.columns:
        out["Coverage %"] = out["Coverage %"].astype(float).map(lambda v: f"{v:.1f}%")
    return out


def validation_messages(df: pd.DataFrame) -> list:
    msgs = []

    exp_total = np.round(df["Base_Demand"].to_numpy() * (1.0 + df["SafetyBufferPct"].to_numpy()), 2)
    actual_total = df["Total_Demand"].to_numpy()
    mismatch = np.abs(actual_total - exp_total) > 0.05

    if mismatch.any():
        bad = df.loc[mismatch, ["Consumable", "Fleet"]].head(8)
        for _, r in bad.iterrows():
            msgs.append(f"{r['Consumable']} ({r['Fleet']}): buffer mismatch")

    total = df["Total_Demand"].to_numpy()
    stock = df["CurrentStock"].to_numpy()
    cov = np.where(total > 0, stock / total, 1.0)
    bad_crit = (df["Alert_Status"].eq("Critical").to_numpy()) & (total > 0) & (cov >= 0.2)

    if bad_crit.any():
        bad = df.loc[bad_crit, ["Consumable", "Fleet"]].head(8)
        for _, r in bad.iterrows():
            msgs.append(f"{r['Consumable']} ({r['Fleet']}): alert misclassified")

    return msgs


# ============================================================
# Upload Screen
# ============================================================
if "df_raw" not in st.session_state:
    st.markdown(
        f"""
        <div class="upload-screen">
            <div class="upload-logo">{APP_ICON}</div>
            <div class="upload-title">{APP_TITLE}</div>
            <div class="upload-sub">Consumable Demand Forecasting & Procurement Intelligence</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    _, center, _ = st.columns([1, 1.4, 1])
    with center:
        uploaded = st.file_uploader("", type=["xlsx", "csv"], label_visibility="collapsed")
        st.markdown(
            """
            <p style="text-align:center;color:#7d8590;font-size:0.8rem;margin-top:0.5rem">
            Supports <strong style="color:#58a6ff">.xlsx</strong> and <strong style="color:#58a6ff">.csv</strong>
            </p>
            """,
            unsafe_allow_html=True
        )

    if uploaded:
        file_bytes = uploaded.getvalue()
        filename = uploaded.name

        sheet_name = None
        if filename.lower().endswith(".xlsx"):
            xls = pd.ExcelFile(io.BytesIO(file_bytes), engine="openpyxl")
            if len(xls.sheet_names) > 1:
                sheet_name = st.selectbox("Select sheet", xls.sheet_names, index=0)

        df_raw, missing = load_dataset(file_bytes, filename, sheet_name)

        if missing:
            st.error(f"Missing columns: **{', '.join(sorted(missing))}**")
            st.stop()

        st.session_state["df_raw"] = df_raw
        st.session_state["filename"] = filename
        st.rerun()

    st.stop()

# ============================================================
# Dashboard
# ============================================================
df_raw = st.session_state["df_raw"]
fname = st.session_state.get("filename", "dataset")

# Top bar
n1, n2 = st.columns([4, 1])
with n1:
    st.markdown(
        f"""
        <div class="topbar">
            <div class="brand">
                <span style="font-size:1.3rem">{APP_ICON}</span>
                <span class="brand-name">{APP_TITLE}</span>
                <span class="brand-tag">/ Demand Forecasting</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with n2:
    st.markdown(
        f'<div style="display:flex;justify-content:flex-end;padding-top:0.6rem"><span class="badge-file">📄 {fname}</span></div>',
        unsafe_allow_html=True
    )
    if st.button("↩ New file", use_container_width=True):
        st.session_state.pop("df_raw", None)
        st.session_state.pop("filename", None)
        st.rerun()

# ============================================================
# Filters (UPDATED)
# - Consumables list instead of ItemType
# - Removed Alert Status dropdown
# ============================================================
mro_opts = sorted(df_raw["MROCompany"].dropna().unique())
fleet_opts = sorted(df_raw["Fleet"].dropna().unique())
consumable_opts = sorted(df_raw["Consumable"].dropna().unique())

f1, f2, f3 = st.columns([2, 2, 2])
with f1:
    sel_mro = st.multiselect("MRO Company", mro_opts, default=mro_opts)
with f2:
    sel_fleet = st.multiselect("Fleet", fleet_opts, default=fleet_opts)
with f3:
    sel_consumables = st.multiselect("Consumables", consumable_opts, default=consumable_opts)

df_f = df_raw[
    df_raw["MROCompany"].isin(sel_mro) &
    df_raw["Fleet"].isin(sel_fleet) &
    df_raw["Consumable"].isin(sel_consumables)
]

df = calculate_demand(df_f)
df_view = df  # no alert status filtering anymore

# ============================================================
# Alerts strip
# ============================================================
crit = int((df["Alert_Status"] == "Critical").sum())
warn = int((df["Alert_Status"] == "Warning").sum())

if crit > 0 or warn > 0:
    st.markdown(
        f"""
        <div class="alert-strip">
            <div class="dot"></div>
            <div><span class="cnt-red">{crit} Critical</span> items below 20% coverage &nbsp;·&nbsp;
            <span class="cnt-amb">{warn} Warning</span> items below 50% — procurement review required</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# KPI cards
# ============================================================
total_demand = float(df["Total_Demand"].sum())
instock_n = int((df["Stock_Status"] == "In Stock").sum())
short_n = int((df["Stock_Status"] == "Short").sum())
reorder_total = float(df["Reorder_Qty"].sum())
n_items = int(len(df))

st.markdown(
    f"""
    <div class="kpi-grid">
        <div class="kpi-card kpi-blue">
            <div class="kpi-label">Total Forecasted Demand</div>
            <div class="kpi-value v-blue">{total_demand:,.1f}</div>
            <div class="kpi-sub">across {n_items} line items</div>
        </div>
        <div class="kpi-card kpi-green">
            <div class="kpi-label">In Stock</div>
            <div class="kpi-value v-green">{instock_n}</div>
            <div class="kpi-sub">items fully covered</div>
        </div>
        <div class="kpi-card kpi-amber">
            <div class="kpi-label">Short / At Risk</div>
            <div class="kpi-value v-amber">{short_n}</div>
            <div class="kpi-sub">items need reorder</div>
        </div>
        <div class="kpi-card kpi-red">
            <div class="kpi-label">Critical Alerts</div>
            <div class="kpi-value v-red">{crit}</div>
            <div class="kpi-sub">&lt;20% stock coverage</div>
        </div>
        <div class="kpi-card kpi-purple">
            <div class="kpi-label">Total Reorder Qty</div>
            <div class="kpi-value v-white">{reorder_total:,.1f}</div>
            <div class="kpi-sub">units to procure</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# Charts - Row 1
# ============================================================
ch1, ch2 = st.columns([1.6, 1])

with ch1:
    st.markdown('<div class="sec-title">Demand vs Current Stock — Top items</div>', unsafe_allow_html=True)
    top_df = df.nlargest(15, "Total_Demand")[["Consumable", "Total_Demand", "CurrentStock", "Alert_Status"]].copy()
    top_melt = top_df.melt(
        id_vars=["Consumable", "Alert_Status"],
        value_vars=["Total_Demand", "CurrentStock"],
        var_name="Metric",
        value_name="Value"
    )
    top_melt["Metric"] = top_melt["Metric"].map({"Total_Demand": "Demand", "CurrentStock": "Stock"})

    bars = alt.Chart(top_melt).mark_bar(cornerRadiusTopRight=3, cornerRadiusBottomRight=3).encode(
        y=alt.Y("Consumable:N", sort="-x", title=None, axis=alt.Axis(labelLimit=140)),
        x=alt.X("Value:Q", title="Quantity"),
        color=alt.Color(
            "Metric:N",
            scale=alt.Scale(domain=["Demand", "Stock"], range=["#58a6ff", "#3fb950"]),
            legend=alt.Legend(title=None, orient="top", direction="horizontal")
        ),
        opacity=alt.condition(alt.datum.Metric == "Demand", alt.value(0.9), alt.value(0.6)),
        tooltip=["Consumable:N", "Metric:N", alt.Tooltip("Value:Q", format=".1f")]
    ).properties(height=320, background="#161b22")

    st.altair_chart(bars, use_container_width=True)

with ch2:
    st.markdown('<div class="sec-title">Alert Breakdown</div>', unsafe_allow_html=True)
    alert_counts = df["Alert_Status"].value_counts()
    total_for_pct = len(df)

    for status, color, bg in [
        ("Critical", "#f85149", "#2d1010"),
        ("Warning", "#d29922", "#2a1e0a"),
        ("Normal", "#3fb950", "#0d2010"),
    ]:
        count = int(alert_counts.get(status, 0))
        pct = round(count / total_for_pct * 100, 1) if total_for_pct else 0
        bar_w = int(pct)

        st.markdown(
            f"""
            <div style="background:{bg};border:1px solid {color}22;border-radius:10px;
                        padding:0.85rem 1rem;margin-bottom:10px;">
                <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px">
                    <span style="color:{color};font-weight:600;font-size:0.85rem">{status}</span>
                    <span style="color:#e6edf3;font-size:1.3rem;font-weight:700">{count}</span>
                </div>
                <div style="background:#21262d;border-radius:4px;height:5px;overflow:hidden">
                    <div style="background:{color};width:{bar_w}%;height:100%;border-radius:4px;"></div>
                </div>
                <div style="color:#7d8590;font-size:0.72rem;margin-top:5px">{pct}% of all items</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# Row 2
# ============================================================
st.markdown('<hr class="divider">', unsafe_allow_html=True)
ch3, ch4 = st.columns(2)

with ch3:
    st.markdown('<div class="sec-title">Stock Coverage % by Fleet</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Red line = Critical (20%) · Amber line = Warning (50%)</div>', unsafe_allow_html=True)

    grp = df.groupby("Fleet", as_index=False)[["CurrentStock", "Total_Demand"]].sum()
    grp["Coverage"] = np.where(grp["Total_Demand"] > 0, (grp["CurrentStock"] / grp["Total_Demand"]) * 100, 100.0)
    grp["Coverage"] = grp["Coverage"].round(1)
    grp["Color"] = np.where(grp["Coverage"] < 20, "#f85149", np.where(grp["Coverage"] < 50, "#d29922", "#3fb950"))

    base = alt.Chart(grp)
    bars_cov = base.mark_bar(cornerRadiusTopRight=3, cornerRadiusTopLeft=3).encode(
        x=alt.X("Fleet:N", title=None, axis=alt.Axis(labelAngle=-30)),
        y=alt.Y("Coverage:Q", title="Coverage %", scale=alt.Scale(domain=[0, max(grp["Coverage"].max() * 1.15, 110)])),
        color=alt.Color("Color:N", scale=None, legend=None),
        tooltip=["Fleet:N", alt.Tooltip("Coverage:Q", format=".1f", title="Coverage %")]
    )

    rule_warn = alt.Chart(pd.DataFrame({"y": [50]})).mark_rule(color="#d29922", strokeDash=[4, 3], opacity=0.7).encode(y="y:Q")
    rule_crit = alt.Chart(pd.DataFrame({"y": [20]})).mark_rule(color="#f85149", strokeDash=[4, 3], opacity=0.7).encode(y="y:Q")

    st.altair_chart((bars_cov + rule_warn + rule_crit).properties(height=280, background="#161b22"), use_container_width=True)

with ch4:
    st.markdown('<div class="sec-title">Demand Composition by MRO</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Breakdown of demand drivers per MRO company</div>', unsafe_allow_html=True)

    mro_comp = df.groupby("MROCompany", as_index=False)[["FH_Demand", "FC_Demand", "Sched_Demand", "Unsched_Demand"]].sum().round(1)
    mro_melt = mro_comp.melt(id_vars="MROCompany", var_name="Driver", value_name="Qty")

    driver_labels = {
        "FH_Demand": "Flight Hour",
        "FC_Demand": "Flight Cycle",
        "Sched_Demand": "Scheduled",
        "Unsched_Demand": "Unscheduled",
    }
    mro_melt["Driver"] = mro_melt["Driver"].map(driver_labels)

    comp_chart = alt.Chart(mro_melt).mark_bar(cornerRadiusTopRight=2, cornerRadiusTopLeft=2).encode(
        x=alt.X("MROCompany:N", title=None, axis=alt.Axis(labelAngle=-30)),
        y=alt.Y("Qty:Q", title="Quantity", stack="zero"),
        color=alt.Color(
            "Driver:N",
            scale=alt.Scale(
                domain=["Flight Hour", "Flight Cycle", "Scheduled", "Unscheduled"],
                range=["#58a6ff", "#3fb950", "#d29922", "#bc8cff"],
            ),
            legend=alt.Legend(title=None, orient="top", direction="horizontal"),
        ),
        tooltip=["MROCompany:N", "Driver:N", alt.Tooltip("Qty:Q", format=".1f")]
    ).properties(height=280, background="#161b22")

    st.altair_chart(comp_chart, use_container_width=True)

# ============================================================
# Scatter
# ============================================================
st.markdown('<div class="sec-title">Stock Coverage Map — All Items</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-sub">Size = reorder quantity · Dashed line = perfect coverage (Stock = Demand)</div>', unsafe_allow_html=True)

scatter_df = df[["Consumable", "Fleet", "MROCompany", "Total_Demand", "CurrentStock", "Coverage_Pct", "Reorder_Qty", "Alert_Status"]].copy()
scatter_df["BubbleSize"] = np.where(scatter_df["Reorder_Qty"] > 0, scatter_df["Reorder_Qty"], scatter_df["Total_Demand"] * 0.05)

max_val = max(scatter_df["Total_Demand"].max(), scatter_df["CurrentStock"].max()) * 1.1
diag_df = pd.DataFrame({"x": [0, max_val], "y": [0, max_val]})

diag_line = alt.Chart(diag_df).mark_line(strokeDash=[5, 4], color="#3fb950", opacity=0.4).encode(x="x:Q", y="y:Q")

scatter = alt.Chart(scatter_df).mark_circle(opacity=0.75, stroke="#0d1117", strokeWidth=0.5).encode(
    x=alt.X("Total_Demand:Q", title="Total Demand", scale=alt.Scale(domain=[0, max_val])),
    y=alt.Y("CurrentStock:Q", title="Current Stock", scale=alt.Scale(domain=[0, max_val])),
    color=alt.Color(
        "Alert_Status:N",
        scale=alt.Scale(domain=["Critical", "Warning", "Normal"], range=["#f85149", "#d29922", "#3fb950"]),
        legend=alt.Legend(title="Status", orient="top-right"),
    ),
    size=alt.Size("BubbleSize:Q", legend=None, scale=alt.Scale(range=[60, 600])),
    tooltip=[
        "Consumable:N",
        "Fleet:N",
        alt.Tooltip("MROCompany:N", title="MRO"),
        alt.Tooltip("Total_Demand:Q", format=".1f", title="Demand"),
        alt.Tooltip("CurrentStock:Q", format=".1f", title="Stock"),
        alt.Tooltip("Coverage_Pct:Q", format=".1f", title="Coverage %"),
        "Alert_Status:N",
    ],
)
st.altair_chart((diag_line + scatter).properties(height=380, background="#161b22"), use_container_width=True)

# ============================================================
# Tables
# ============================================================
st.markdown('<hr class="divider">', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📋  Full Forecast Matrix", "🚨  Procurement Alerts", "🟢  In-Stock Items"])

FULL_COLS = {
    "MROCompany": "MRO Company", "Fleet": "Fleet", "Consumable": "Consumable",
    "ItemType": "Type", "Unit": "Unit",
    "FH_Demand": "FH Demand", "FC_Demand": "FC Demand",
    "Sched_Demand": "Scheduled", "Unsched_Demand": "Unscheduled",
    "Base_Demand": "Base Demand", "Total_Demand": "Total Demand",
    "CurrentStock": "Stock", "Coverage_Pct": "Coverage %",
    "Reorder_Qty": "Reorder Qty", "Alert_Status": "Status"
}
ALERT_COLS = {
    "MROCompany": "MRO Company", "Fleet": "Fleet", "Consumable": "Consumable",
    "ItemType": "Type", "Unit": "Unit", "CurrentStock": "Stock",
    "Total_Demand": "Demand", "Coverage_Pct": "Coverage %",
    "Reorder_Qty": "Reorder Qty", "Alert_Status": "Status"
}
INSTOCK_COLS = {
    "MROCompany": "MRO Company", "Fleet": "Fleet", "Consumable": "Consumable",
    "ItemType": "Type", "Unit": "Unit",
    "CurrentStock": "Stock", "Total_Demand": "Demand",
    "Coverage_Pct": "Coverage %", "Alert_Status": "Status"
}

with tab1:
    st.dataframe(fmt_table(df_view, FULL_COLS), use_container_width=True, hide_index=True, height=380)

with tab2:
    alert_df = df_view[df_view["Alert_Status"].isin(["Critical", "Warning"])].sort_values("Coverage_Pct")
    if alert_df.empty:
        st.markdown('<p style="color:#3fb950;padding:0.75rem 0">✓ No procurement alerts for current filters.</p>', unsafe_allow_html=True)
    else:
        st.dataframe(fmt_table(alert_df, ALERT_COLS), use_container_width=True, hide_index=True, height=380)

with tab3:
    instock_df = df_view[df_view["Stock_Status"] == "In Stock"]
    if instock_df.empty:
        st.markdown('<p style="color:#d29922;padding:0.75rem 0">⚠ No fully in-stock items for current filters.</p>', unsafe_allow_html=True)
    else:
        st.dataframe(fmt_table(instock_df, INSTOCK_COLS), use_container_width=True, hide_index=True, height=380)

# ============================================================
# Exports
# ============================================================
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="sec-title">Export Reports</div>', unsafe_allow_html=True)

e1, e2, e3, e4 = st.columns(4)
alert_exp = df[df["Alert_Status"].isin(["Critical", "Warning"])]
reorder_exp = df[df["Reorder_Qty"] > 0][["MROCompany", "Fleet", "Consumable", "Unit", "Reorder_Qty", "Alert_Status"]]
instock_exp = df[df["Stock_Status"] == "In Stock"]

with e1:
    st.download_button(
        "📥 Full Forecast",
        data=to_excel_bytes(df, "Forecast"),
        file_name="avyntis_forecast.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
with e2:
    st.download_button(
        "🚨 Alert Report",
        data=to_excel_bytes(alert_exp, "Alerts"),
        file_name="avyntis_alerts.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        disabled=alert_exp.empty
    )
with e3:
    st.download_button(
        "🛒 Reorder List",
        data=to_excel_bytes(reorder_exp, "Reorder"),
        file_name="avyntis_reorder.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        disabled=reorder_exp.empty
    )
with e4:
    st.download_button(
        "✅ In-Stock List",
        data=to_excel_bytes(instock_exp, "InStock"),
        file_name="avyntis_instock.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        disabled=instock_exp.empty
    )

# ============================================================
# Validation
# ============================================================
errs = validation_messages(df)
if errs:
    st.markdown('<div class="val-err">❌ Validation issues:<br>' + "<br>".join(errs) + "</div>", unsafe_allow_html=True)
else:
    st.markdown('<div class="val-ok">✓ All calculations validated — no logic errors detected</div>', unsafe_allow_html=True)
