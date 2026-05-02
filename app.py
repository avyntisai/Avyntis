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
    /* Global */
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
    
    /* Header */
    .avyntis-header {
        background: linear-gradient(135deg, var(--primary) 0%, #1e3a5f 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(15, 42, 74, 0.15);
    }
    .avyntis-header h1 { margin: 0; font-size: 1.8rem; font-weight: 700; }
    .avyntis-header p { margin: 0.25rem 0 0; opacity: 0.85; font-size: 0.95rem; }
    
    /* KPI Cards */
    .kpi-container { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
    .kpi-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1.25rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .kpi-label { font-size: 0.85rem; color: var(--text-light); font-weight: 500; margin-bottom: 0.5rem; }
    .kpi-value { font-size: 1.75rem; font-weight: 700; color: var(--text); }
    .kpi-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
    
    /* Section Headers */
    .section-title { font-size: 1.25rem; font-weight: 600; color: var(--primary); margin: 1.5rem 0 1rem; border-bottom: 2px solid var(--border); padding-bottom: 0.5rem; }
    
    /* Alert Panel */
    .alert-panel {
        background: #fef3f2;
        border: 1px solid #fecaca;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 1.5rem;
    }
    .alert-panel.warning { background: #fffbeb; border-color: #fde68a; }
    .alert-title { font-weight: 600; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem; }
    
    /* Tables */
    .stDataFrame { border-radius: 8px; border: 1px solid var(--border); }
    .stDataFrame th { background: #f8fafc !important; font-weight: 600; color: var(--primary) !important; }
    
    /* Sidebar */
    .stSidebar { background: #f8f9fb; }
    .stSidebar .css-1d391kg { padding-top: 2rem; }
    
    /* Buttons */
    .stButton>button { border-radius: 6px; font-weight: 500; }
    
    /* Validation */
    .validation-box { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 0.75rem 1rem; margin-top: 1rem; }
    .validation-box.error { background: #fef2f2; border-color: #fecaca; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 📦 Constants & Schema
# ==========================================
REQUIRED_COLS = [
    'Fleet', 'Consumable', 'ItemType', 'Unit', 'ForecastPeriod',
    'UsageRatePerFH', 'TotalFlightHours', 'UsageRatePerFC', 'TotalFlightCycles',
    'ScheduledQtyPerCheck', 'NumberOfChecks', 'ExpectedFailureEvents',
    'UnscheduledQtyPerEvent', 'SafetyBufferPct', 'CurrentStock'
]

COL_MAPPING = {
    'Substance': 'ItemType',
    'Rate per Flight Hour': 'UsageRatePerFH',
    'Total flight  hours': 'TotalFlightHours',
    'Rate per flight cycle': 'UsageRatePerFC',
    'Total  flight Cycle': 'TotalFlightCycles',
    'Quantity in Schedule Check': 'ScheduledQtyPerCheck',
    'Number of Checks': 'NumberOfChecks',
    'Expected Failure Events': 'ExpectedFailureEvents',
    'Consumables Used per Event': 'UnscheduledQtyPerEvent',
    'Safety Buffer': 'SafetyBufferPct',
    'Current Stock': 'CurrentStock'
}

SAMPLE_DATA = [
    {"Fleet": "Fleet-A", "Consumable": "Engine Oil", "ItemType": "Liquid", "Unit": "Liters",
     "ForecastPeriod": "Monthly", "UsageRatePerFH": 0.5, "TotalFlightHours": 1200,
     "UsageRatePerFC": 0.0, "TotalFlightCycles": 150, "ScheduledQtyPerCheck": 10,
     "NumberOfChecks": 4, "ExpectedFailureEvents": 2, "UnscheduledQtyPerEvent": 5,
     "SafetyBufferPct": 0.10, "CurrentStock": 400},
    {"Fleet": "Fleet-B", "Consumable": "Brake Kit", "ItemType": "Hard", "Unit": "Sets",
     "ForecastPeriod": "Monthly", "UsageRatePerFH": 0.0, "TotalFlightHours": 800,
     "UsageRatePerFC": 0.02, "TotalFlightCycles": 100, "ScheduledQtyPerCheck": 0,
     "NumberOfChecks": 0, "ExpectedFailureEvents": 1, "UnscheduledQtyPerEvent": 1,
     "SafetyBufferPct": 0.05, "CurrentStock": 2}
]

# ==========================================
# 🧮 Forecasting & Alert Logic
# ==========================================
def classify_alert(total_demand, current_stock):
    if total_demand <= 0: return "Normal", "✅"
    stock_pct = (current_stock / total_demand) * 100
    if stock_pct < 20: return "Critical", "🔴"
    elif stock_pct < 50: return "Warning", "🟡"
    else: return "Normal", "🟢"

def calculate_demand(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    num_cols = [c for c in REQUIRED_COLS if c not in ['Fleet', 'Consumable', 'ItemType', 'Unit', 'ForecastPeriod']]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    df['FH_Component'] = df['UsageRatePerFH'] * df['TotalFlightHours']
    df['FC_Component'] = df['UsageRatePerFC'] * df['TotalFlightCycles']
    df.loc[df['ItemType'] == 'Liquid', 'FC_Component'] = 0
    df.loc[df['ItemType'] == 'Hard', 'FH_Component'] = 0

    df['Scheduled_Component'] = df['ScheduledQtyPerCheck'] * df['NumberOfChecks']
    df['Unscheduled_Component'] = df['ExpectedFailureEvents'] * df['UnscheduledQtyPerEvent']
    
    df['BaseDemand'] = df['FH_Component'] + df['FC_Component'] + df['Scheduled_Component'] + df['Unscheduled_Component']
    df['TotalDemand'] = df['BaseDemand'] * (1 + df['SafetyBufferPct'])
    
    df['Shortage_Flag'] = df['CurrentStock'] < df['TotalDemand']
    df['RecommendedOrderQty'] = np.where(df['Shortage_Flag'], df['TotalDemand'] - df['CurrentStock'], 0)
    
    df[['Alert_Status', 'Alert_Icon']] = df.apply(
        lambda row: pd.Series(classify_alert(row['TotalDemand'], row['CurrentStock'])), axis=1
    )
    
    df['TotalDemand'] = df['TotalDemand'].round(2)
    df['RecommendedOrderQty'] = df['RecommendedOrderQty'].round(2)
    return df

# ==========================================
# 📥 Sidebar & Data Loading
# ==========================================
with st.sidebar:
    st.header("📥 Data Input")
    uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])
    
    df_input = pd.DataFrame(SAMPLE_DATA)
    if uploaded_file is not None:
        try:
            df_input = pd.read_csv(uploaded_file)
            df_input.columns = df_input.columns.str.strip()
            
            # Debug: Show original columns
            with st.expander("📊 Debug: Column Mapping", expanded=False):
                st.write("### Original Columns:")
                st.write(list(df_input.columns))
            
            df_input.rename(columns=COL_MAPPING, inplace=True)
            
            # Debug: Show mapped columns
            with st.expander("📊 Debug: Column Mapping", expanded=False):
                st.write("### Mapped Columns:")
                st.write(list(df_input.columns))
            
            if 'ForecastPeriod' not in df_input.columns:
                df_input['ForecastPeriod'] = 'Monthly'
            
            missing = set(REQUIRED_COLS) - set(df_input.columns)
            if missing:
                st.error(f"❌ Missing/Unmapped: {', '.join(missing)}")
                st.stop()
            st.success("✅ CSV Loaded & Standardized")
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.stop()

    st.markdown("---")
    st.header("⚙️ System Checks")
    liquid_fc = df_input[(df_input['ItemType'] == 'Liquid') & (df_input['TotalFlightCycles'] > 0)]
    if not liquid_fc.empty:
        st.warning(f"⚠️ {len(liquid_fc)} Liquid items have FC data (ignored)")
    hard_fh = df_input[(df_input['ItemType'] == 'Hard') & (df_input['TotalFlightHours'] > 0)]
    if not hard_fh.empty:
        st.warning(f"⚠️ {len(hard_fh)} Hard items have FH data (ignored)")

# ==========================================
# 📊 Main Dashboard
# ==========================================
st.markdown('<div class="avyntis-header"><h1>✈️ Project Avyntis</h1><p>Unified Consumable Demand Forecasting & Procurement Alerts</p></div>', unsafe_allow_html=True)

# Filters
st.markdown('<div class="section-title">🔍 Filter Fleet & Consumables</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
fleets = df_input['Fleet'].unique()
consumables = df_input['Consumable'].unique()
selected_fleets = col1.multiselect("Fleets", fleets, default=fleets)
selected_consumables = col2.multiselect("Consumables", consumables, default=consumables)

df_filtered = df_input[
    (df_input['Fleet'].isin(selected_fleets)) & 
    (df_input['Consumable'].isin(selected_consumables))
]

# Debug: Show uploaded data before calculation
if uploaded_file is not None:
    with st.expander("📊 Debug: Uploaded Data Preview", expanded=False):
        st.dataframe(df_filtered, use_container_width=True)
        st.write("### Raw Values for First Row:")
        if len(df_filtered) > 0:
            first_row = df_filtered.iloc[0]
            for col in df_filtered.columns:
                st.write(f"- **{col}**: `{first_row[col]}` (type: {type(first_row[col]).__name__})")

df_result = calculate_demand(df_filtered)

# Debug: Show calculation breakdown
if uploaded_file is not None:
    with st.expander("📊 Debug: Calculation Breakdown", expanded=False):
        st.write("### Component Calculations:")
        debug_df = df_result[['Fleet', 'Consumable', 'FH_Component', 'FC_Component', 'Scheduled_Component', 'Unscheduled_Component', 'BaseDemand', 'TotalDemand']].copy()
        st.dataframe(debug_df, use_container_width=True, hide_index=True)

# KPI Cards
st.markdown('<div class="section-title">📈 Forecast Summary</div>', unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown(f"""<div class="kpi-container" style="grid-template-columns:1fr"><div class="kpi-card">
        <div class="kpi-icon">📦</div><div class="kpi-label">Total Forecasted Demand</div>
        <div class="kpi-value">{df_result['TotalDemand'].sum():,.2f}</div></div></div>""", unsafe_allow_html=True)
with kpi2:
    st.markdown(f"""<div class="kpi-container" style="grid-template-columns:1fr"><div class="kpi-card">
        <div class="kpi-icon">📋</div><div class="kpi-label">Items Forecasted</div>
        <div class="kpi-value">{len(df_result)}</div></div></div>""", unsafe_allow_html=True)
with kpi3:
    alerts = df_result['Alert_Status'].value_counts()
    crit = alerts.get('Critical', 0)
    warn = alerts.get('Warning', 0)
    st.markdown(f"""<div class="kpi-container" style="grid-template-columns:1fr"><div class="kpi-card" style="border-color: {'#fecaca' if crit > 0 else '#fde68a'}">
        <div class="kpi-icon">🚨</div><div class="kpi-label">Active Alerts</div>
        <div class="kpi-value">{crit + warn}</div></div></div>""", unsafe_allow_html=True)
with kpi4:
    st.markdown(f"""<div class="kpi-container" style="grid-template-columns:1fr"><div class="kpi-card">
        <div class="kpi-icon">🛒</div><div class="kpi-label">Total Reorder Qty</div>
        <div class="kpi-value">{df_result['RecommendedOrderQty'].sum():,.2f}</div></div></div>""", unsafe_allow_html=True)

# Alert Panel
alert_df = df_result[df_result['Alert_Status'].isin(['Critical', 'Warning'])]
if not alert_df.empty:
    st.markdown('<div class="section-title">⚠️ Procurement Alerts</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="alert-panel">🔴 <strong>Critical:</strong> {alerts.get("Critical", 0)} items | 🟡 <strong>Warning:</strong> {alerts.get("Warning", 0)} items</div>', unsafe_allow_html=True)
    st.dataframe(alert_df[['Fleet', 'Consumable', 'ItemType', 'CurrentStock', 'TotalDemand', 'RecommendedOrderQty', 'Alert_Status']], use_container_width=True, hide_index=True)

# Detailed Table
st.markdown('<div class="section-title">📋 Detailed Demand Matrix</div>', unsafe_allow_html=True)
def highlight_row(row):
    if row['Alert_Status'] == 'Critical': return ['background-color: #fef2f2; color: #991b1b; font-weight: 600'] * len(row)
    elif row['Alert_Status'] == 'Warning': return ['background-color: #fffbeb; color: #92400e; font-weight: 600'] * len(row)
    return [''] * len(row)

cols_display = ['Fleet', 'Consumable', 'ItemType', 'BaseDemand', 'TotalDemand', 'CurrentStock', 'Alert_Status', 'RecommendedOrderQty']
styled_df = df_result[cols_display].style.apply(highlight_row, axis=1)
st.dataframe(styled_df, use_container_width=True, hide_index=True)

# Export
st.markdown('<div class="section-title">💾 Export & Validation</div>', unsafe_allow_html=True)
col_exp1, col_exp2 = st.columns(2)
with col_exp1:
    if not alert_df.empty:
        buf = io.StringIO()
        alert_df.to_csv(buf, index=False)
        st.download_button("📥 Download Alert Report", data=buf.getvalue(), file_name="avyntis_alerts.csv", mime="text/csv")
    else:
        st.success("✅ No shortages detected")
with col_exp2:
    buf = io.StringIO()
    df_result.to_csv(buf, index=False)
    st.download_button("📥 Download Full Forecast", data=buf.getvalue(), file_name="avyntis_full.csv", mime="text/csv")

# Validation
def validate_logic(df):
    errors = []
    for _, row in df.iterrows():
        if row['ItemType'] == 'Liquid' and row['FC_Component'] != 0: errors.append(f"{row['Consumable']} Liquid has FC data")
        if row['ItemType'] == 'Hard' and row['FH_Component'] != 0: errors.append(f"{row['Consumable']} Hard has FH data")
        expected = row['BaseDemand'] * (1 + row['SafetyBufferPct'])
        if abs(row['TotalDemand'] - expected) > 0.01: errors.append(f"{row['Consumable']} buffer mismatch")
        if row['Alert_Status'] == 'Critical' and (row['CurrentStock'] / row['TotalDemand']) >= 0.2: errors.append(f"{row['Consumable']} alert misclassified")
    return errors

errs = validate_logic(df_result)
if errs:
    st.markdown('<div class="validation-box error">❌ Validation Failed:<br>' + '<br>'.join(errs) + '</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="validation-box">✅ Logic & Alert Validation Passed</div>', unsafe_allow_html=True)
