import streamlit as st
import pandas as pd
import io
import numpy as np

# ==========================================
# ⚙️ Page Configuration
# ==========================================
st.set_page_config(
    page_title="Project Avyntis - Demand Forecasting",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 🎨 Professional CSS Theme
# ==========================================
st.markdown("""
<style>
    :root {
        --primary: #0f2a4a;
        --accent: #0066cc;
        --bg: #f8f9fb;
        --card: #ffffff;
        --text: #1a1d23;
        --text-light: #6b7280;
        --border: #e5e7eb;
        --critical: #dc2626;
        --warning: #f59e0b;
        --success: #10b981;
    }
    html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    .main .block-container { padding-top: 2rem; }

    .avyntis-header {
        background: linear-gradient(135deg, #0f2a4a 0%, #1e3a5f 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(15,42,74,0.15);
    }
    .avyntis-header h1 { margin: 0; font-size: 1.8rem; font-weight: 700; }
    .avyntis-header p { margin: 0.25rem 0 0; opacity: 0.85; font-size: 0.95rem; }

    .kpi-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 1.25rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }
    .kpi-label { font-size: 0.85rem; color: #6b7280; font-weight: 500; margin-bottom: 0.5rem; }
    .kpi-value { font-size: 1.75rem; font-weight: 700; color: #1a1d23; }
    .kpi-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }

    .section-title {
        font-size: 1.1rem; font-weight: 600; color: #0f2a4a;
        margin: 1.5rem 0 1rem;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.5rem;
    }

    .alert-panel {
        background: #fef3f2;
        border: 1px solid #fecaca;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
    }
    .alert-panel.warning { background: #fffbeb; border-color: #fde68a; }

    .status-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 99px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-critical { background: #fef2f2; color: #991b1b; }
    .badge-warning  { background: #fffbeb; color: #92400e; }
    .badge-normal   { background: #f0fdf4; color: #166534; }

    .validation-box { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 0.75rem 1rem; margin-top: 1rem; }
    .validation-box.error { background: #fef2f2; border-color: #fecaca; }

    .stDataFrame { border-radius: 8px; border: 1px solid #e5e7eb; }
    .stDataFrame th { background: #f8fafc !important; font-weight: 600; color: #0f2a4a !important; }
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
    'MROCompany', 'Fleet', 'Consumable', 'ItemType', 'Unit', 'ForecastPeriod',
    'UsageRatePerFH', 'TotalFlightHours', 'UsageRatePerFC', 'TotalFlightCycles',
    'ScheduledQtyPerCheck', 'NumberOfChecks', 'ExpectedFailureEvents',
    'UnscheduledQtyPerEvent', 'SafetyBufferPct', 'CurrentStock'
]

SAMPLE_DATA = [
    {"MROCompany": "XYZ LTD", "Fleet": "B787 Fleet", "Consumable": "Seal Kit",
     "ItemType": "Hard", "Unit": "KG", "ForecastPeriod": "Monthly",
     "UsageRatePerFH": 0.0, "TotalFlightHours": 0, "UsageRatePerFC": 3.0, "TotalFlightCycles": 2,
     "ScheduledQtyPerCheck": 1, "NumberOfChecks": 10, "ExpectedFailureEvents": 6,
     "UnscheduledQtyPerEvent": 1.8, "SafetyBufferPct": 0.18, "CurrentStock": 38},
    {"MROCompany": "ABC Ltd", "Fleet": "A320 Fleet", "Consumable": "Grease",
     "ItemType": "Liquid", "Unit": "Liter", "ForecastPeriod": "Monthly",
     "UsageRatePerFH": 0.039, "TotalFlightHours": 5287, "UsageRatePerFC": 0.0, "TotalFlightCycles": 0,
     "ScheduledQtyPerCheck": 6, "NumberOfChecks": 8, "ExpectedFailureEvents": 1,
     "UnscheduledQtyPerEvent": 1.4, "SafetyBufferPct": 0.25, "CurrentStock": 12},
]

# ==========================================
# 🧮 Forecasting Logic
# ==========================================
def classify_alert(total_demand, current_stock):
    if total_demand <= 0:
        return "Normal", "🟢"
    stock_pct = (current_stock / total_demand) * 100
    if stock_pct < 20:
        return "Critical", "🔴"
    elif stock_pct < 50:
        return "Warning", "🟡"
    else:
        return "Normal", "🟢"

def calculate_demand(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    num_cols = [c for c in REQUIRED_COLS if c not in
                ['MROCompany', 'Fleet', 'Consumable', 'ItemType', 'Unit', 'ForecastPeriod']]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Flight-hour based (Liquids only)
    df['FH_Component'] = np.where(df['ItemType'] == 'Liquid',
                                   df['UsageRatePerFH'] * df['TotalFlightHours'], 0)
    # Flight-cycle based (Hard parts only)
    df['FC_Component'] = np.where(df['ItemType'] == 'Hard',
                                   df['UsageRatePerFC'] * df['TotalFlightCycles'], 0)

    df['Scheduled_Component'] = df['ScheduledQtyPerCheck'] * df['NumberOfChecks']
    df['Unscheduled_Component'] = df['ExpectedFailureEvents'] * df['UnscheduledQtyPerEvent']

    df['BaseDemand'] = (df['FH_Component'] + df['FC_Component'] +
                        df['Scheduled_Component'] + df['Unscheduled_Component'])
    df['TotalDemand'] = (df['BaseDemand'] * (1 + df['SafetyBufferPct'])).round(2)

    df['StockStatus'] = np.where(df['CurrentStock'] >= df['TotalDemand'],
                                  'In Stock', 'Short')
    df['RecommendedOrderQty'] = np.where(
        df['CurrentStock'] < df['TotalDemand'],
        (df['TotalDemand'] - df['CurrentStock']).round(2), 0)

    df[['Alert_Status', 'Alert_Icon']] = df.apply(
        lambda row: pd.Series(classify_alert(row['TotalDemand'], row['CurrentStock'])), axis=1)

    return df

# ==========================================
# 📥 Sidebar — Data Input
# ==========================================
with st.sidebar:
    st.markdown("## 📥 Data Input")
    uploaded_file = st.file_uploader("Upload Excel / CSV Dataset", type=["xlsx", "csv"])

    df_input = pd.DataFrame(SAMPLE_DATA)

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_raw = pd.read_csv(uploaded_file)
            else:
                df_raw = pd.read_excel(uploaded_file)

            df_raw.columns = df_raw.columns.str.strip()
            df_raw.rename(columns=COL_MAPPING, inplace=True)

            if 'ForecastPeriod' not in df_raw.columns:
                df_raw['ForecastPeriod'] = 'Monthly'

            missing = set(REQUIRED_COLS) - set(df_raw.columns)
            if missing:
                st.error(f"❌ Missing columns: {', '.join(sorted(missing))}")
                st.stop()

            df_input = df_raw
            st.success(f"✅ Loaded {len(df_input)} rows")

        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
            st.stop()
    else:
        st.info("📊 Showing sample data. Upload your file above.")

    st.markdown("---")
    st.markdown("### ⚙️ System Checks")
    if 'ItemType' in df_input.columns:
        liquid_fc = df_input[(df_input['ItemType'] == 'Liquid') &
                             (pd.to_numeric(df_input.get('TotalFlightCycles', pd.Series([0])), errors='coerce').fillna(0) > 0)]
        if not liquid_fc.empty:
            st.warning(f"⚠️ {len(liquid_fc)} Liquid items have FC data (FC ignored for liquids)")
        hard_fh = df_input[(df_input['ItemType'] == 'Hard') &
                           (pd.to_numeric(df_input.get('TotalFlightHours', pd.Series([0])), errors='coerce').fillna(0) > 0)]
        if not hard_fh.empty:
            st.warning(f"⚠️ {len(hard_fh)} Hard items have FH data (FH ignored for hard parts)")

# ==========================================
# 📊 Main Dashboard
# ==========================================
st.markdown("""
<div class="avyntis-header">
  <h1>✈️ Project Avyntis</h1>
  <p>Unified Consumable Demand Forecasting & Procurement Alerts</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 🔍 Filters
# ==========================================
st.markdown('<div class="section-title">🔍 Filters</div>', unsafe_allow_html=True)
fc1, fc2, fc3 = st.columns(3)

mro_options = sorted(df_input['MROCompany'].dropna().unique()) if 'MROCompany' in df_input.columns else []
fleet_options = sorted(df_input['Fleet'].dropna().unique())
consumable_options = sorted(df_input['Consumable'].dropna().unique())

selected_mro = fc1.multiselect("MRO Company", mro_options, default=mro_options)
selected_fleets = fc2.multiselect("Fleet", fleet_options, default=fleet_options)
selected_consumables = fc3.multiselect("Consumables", consumable_options, default=consumable_options)

df_filtered = df_input.copy()
if selected_mro and 'MROCompany' in df_filtered.columns:
    df_filtered = df_filtered[df_filtered['MROCompany'].isin(selected_mro)]
df_filtered = df_filtered[df_filtered['Fleet'].isin(selected_fleets)]
df_filtered = df_filtered[df_filtered['Consumable'].isin(selected_consumables)]

df_result = calculate_demand(df_filtered)

# ==========================================
# 📈 KPI Cards
# ==========================================
st.markdown('<div class="section-title">📈 Forecast Summary</div>', unsafe_allow_html=True)
kc1, kc2, kc3, kc4, kc5 = st.columns(5)

alerts = df_result['Alert_Status'].value_counts()
crit_count = int(alerts.get('Critical', 0))
warn_count = int(alerts.get('Warning', 0))
instock_count = int((df_result['StockStatus'] == 'In Stock').sum())
short_count = int((df_result['StockStatus'] == 'Short').sum())

with kc1:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-icon">📦</div>
        <div class="kpi-label">Total Forecasted Demand</div>
        <div class="kpi-value">{df_result['TotalDemand'].sum():,.2f}</div>
    </div>""", unsafe_allow_html=True)

with kc2:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-icon">✅</div>
        <div class="kpi-label">In Stock Items</div>
        <div class="kpi-value" style="color:#10b981">{instock_count}</div>
    </div>""", unsafe_allow_html=True)

with kc3:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-icon">⚠️</div>
        <div class="kpi-label">Short / At Risk Items</div>
        <div class="kpi-value" style="color:#f59e0b">{short_count}</div>
    </div>""", unsafe_allow_html=True)

with kc4:
    st.markdown(f"""<div class="kpi-card" style="border-color:{'#fecaca' if crit_count > 0 else '#e5e7eb'}">
        <div class="kpi-icon">🚨</div>
        <div class="kpi-label">Critical Alerts</div>
        <div class="kpi-value" style="color:#dc2626">{crit_count}</div>
    </div>""", unsafe_allow_html=True)

with kc5:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-icon">🛒</div>
        <div class="kpi-label">Total Reorder Qty</div>
        <div class="kpi-value">{df_result['RecommendedOrderQty'].sum():,.2f}</div>
    </div>""", unsafe_allow_html=True)

# ==========================================
# 🟢 In-Stock Summary
# ==========================================
st.markdown('<div class="section-title">🟢 In-Stock Items</div>', unsafe_allow_html=True)
instock_df = df_result[df_result['StockStatus'] == 'In Stock'][[
    'MROCompany', 'Fleet', 'Consumable', 'ItemType', 'Unit',
    'CurrentStock', 'TotalDemand', 'Alert_Status'
]].copy()
instock_df.rename(columns={'Alert_Status': 'Status'}, inplace=True)

if instock_df.empty:
    st.info("No items are currently in-stock vs demand.")
else:
    st.dataframe(instock_df, use_container_width=True, hide_index=True)

# ==========================================
# 🔴 Procurement Alerts
# ==========================================
alert_df = df_result[df_result['Alert_Status'].isin(['Critical', 'Warning'])]
if not alert_df.empty:
    st.markdown('<div class="section-title">⚠️ Procurement Alerts</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="alert-panel">🔴 <strong>Critical:</strong> {crit_count} items &nbsp;|&nbsp; '
        f'🟡 <strong>Warning:</strong> {warn_count} items requiring procurement action</div>',
        unsafe_allow_html=True
    )
    alert_display = alert_df[[
        'MROCompany', 'Fleet', 'Consumable', 'ItemType', 'Unit',
        'CurrentStock', 'TotalDemand', 'RecommendedOrderQty', 'Alert_Status'
    ]].copy()
    alert_display.rename(columns={
        'MROCompany': 'MRO Company',
        'RecommendedOrderQty': 'Reorder Qty',
        'Alert_Status': 'Status'
    }, inplace=True)

    def highlight_alerts(row):
        if row['Status'] == 'Critical':
            return ['background-color: #fef2f2; color: #991b1b; font-weight: 600'] * len(row)
        elif row['Status'] == 'Warning':
            return ['background-color: #fffbeb; color: #92400e; font-weight: 600'] * len(row)
        return [''] * len(row)

    st.dataframe(alert_display.style.apply(highlight_alerts, axis=1),
                 use_container_width=True, hide_index=True)

# ==========================================
# 📋 Full Demand Matrix
# ==========================================
st.markdown('<div class="section-title">📋 Full Demand Forecast Matrix</div>', unsafe_allow_html=True)

display_cols = [
    'MROCompany', 'Fleet', 'Consumable', 'ItemType', 'Unit',
    'FH_Component', 'FC_Component', 'Scheduled_Component', 'Unscheduled_Component',
    'BaseDemand', 'SafetyBufferPct', 'TotalDemand',
    'CurrentStock', 'StockStatus', 'RecommendedOrderQty', 'Alert_Status'
]
rename_map = {
    'MROCompany': 'MRO Company',
    'FH_Component': 'FH Demand',
    'FC_Component': 'FC Demand',
    'Scheduled_Component': 'Sched. Demand',
    'Unscheduled_Component': 'Unsched. Demand',
    'SafetyBufferPct': 'Buffer %',
    'RecommendedOrderQty': 'Reorder Qty',
    'Alert_Status': 'Status'
}

full_display = df_result[display_cols].rename(columns=rename_map).copy()
full_display['Buffer %'] = (full_display['Buffer %'] * 100).round(1).astype(str) + '%'

def highlight_full(row):
    status = row.get('Status', '')
    if status == 'Critical':
        return ['background-color: #fef2f2'] * len(row)
    elif status == 'Warning':
        return ['background-color: #fffbeb'] * len(row)
    return [''] * len(row)

st.dataframe(full_display.style.apply(highlight_full, axis=1),
             use_container_width=True, hide_index=True)

# ==========================================
# 💾 Export
# ==========================================
st.markdown('<div class="section-title">💾 Export Reports</div>', unsafe_allow_html=True)
exp1, exp2, exp3 = st.columns(3)

with exp1:
    buf = io.BytesIO()
    df_result.to_excel(buf, index=False)
    st.download_button("📥 Full Forecast (Excel)", data=buf.getvalue(),
                       file_name="avyntis_full_forecast.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

with exp2:
    if not alert_df.empty:
        buf2 = io.BytesIO()
        alert_df.to_excel(buf2, index=False)
        st.download_button("🚨 Alert Report (Excel)", data=buf2.getvalue(),
                           file_name="avyntis_alerts.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.success("✅ No shortage alerts")

with exp3:
    reorder_df = df_result[df_result['RecommendedOrderQty'] > 0][[
        'MROCompany', 'Fleet', 'Consumable', 'Unit', 'RecommendedOrderQty', 'Alert_Status'
    ]]
    if not reorder_df.empty:
        buf3 = io.BytesIO()
        reorder_df.to_excel(buf3, index=False)
        st.download_button("🛒 Reorder List (Excel)", data=buf3.getvalue(),
                           file_name="avyntis_reorder.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ==========================================
# ✅ Logic Validation
# ==========================================
def validate_logic(df):
    errors = []
    for _, row in df.iterrows():
        expected = round(row['BaseDemand'] * (1 + row['SafetyBufferPct']), 2)
        if abs(row['TotalDemand'] - expected) > 0.05:
            errors.append(f"{row['Consumable']} ({row['Fleet']}): buffer mismatch")
        if row['Alert_Status'] == 'Critical' and row['TotalDemand'] > 0:
            stock_pct = row['CurrentStock'] / row['TotalDemand']
            if stock_pct >= 0.2:
                errors.append(f"{row['Consumable']} ({row['Fleet']}): alert misclassified")
    return errors

errs = validate_logic(df_result)
if errs:
    st.markdown('<div class="validation-box error">❌ Validation Issues:<br>' +
                '<br>'.join(errs) + '</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="validation-box">✅ All calculations validated — logic checks passed</div>',
                unsafe_allow_html=True)
