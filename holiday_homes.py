import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
from datetime import datetime

st.set_page_config(page_title="Uzair Finance - Holiday Homes vs Long-Term", page_icon="🏖️", layout="wide")

# ==========================================
# UZAIR FINANCE BRANDING & CSS
# ==========================================
st.markdown("""
<style>
    .main-header { background: linear-gradient(135deg, #0a2540 0%, #1e3a5f 50%, #2d5a87 100%); color: white; padding: 40px; border-radius: 20px; text-align: center; margin-bottom: 30px; box-shadow: 0 15px 35px rgba(10,37,64,0.3); }
    .main-header h1 { font-size: 48px; font-weight: 800; margin: 0; letter-spacing: 2px; }
    .main-header .tagline { font-size: 16px; color: #ffd700; margin-top: 10px; letter-spacing: 3px; text-transform: uppercase; }
    .kpi-card { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 25px; border-radius: 15px; border-left: 5px solid #0a2540; box-shadow: 0 5px 15px rgba(0,0,0,0.08); text-align: center; }
    .kpi-label { font-size: 12px; color: #6c757d; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
    .kpi-value { font-size: 28px; font-weight: 800; color: #0a2540; margin-top: 8px; }
    .kpi-value.highlight { color: #2e7d32; }
    .section-title { color: #0a2540; font-size: 24px; font-weight: 700; margin: 30px 0 20px 0; padding-bottom: 10px; border-bottom: 3px solid #ffd700; }
    .disclaimer-box { background: #fff3cd; border-left: 5px solid #ffc107; padding: 20px; border-radius: 10px; margin-top: 30px; font-size: 12px; color: #856404; }
    .footer { text-align: center; padding: 30px; margin-top: 50px; background: #0a2540; color: white; border-radius: 15px; }
    
    /* Custom Table Styles for Battle Section */
    .battle-table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 15px; }
    .battle-table th { background-color: #0a2540; color: white; padding: 15px; text-align: left; font-weight: 700; }
    .battle-table td { padding: 15px; border-bottom: 1px solid #e9ecef; }
    .battle-table tr:nth-child(even) { background-color: #f8f9fa; }
    .winner-text { color: #2e7d32; font-weight: 800; font-size: 16px; }
    .normal-text { color: #555; font-weight: 600; }
    .header-cell { font-weight: 800; color: #0a2540; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🏖️ UZAIR FINANCE</h1><div class="tagline">Investment Battle: Long-Term vs Holiday Homes</div></div>', unsafe_allow_html=True)

# ==========================================
# UNIFIED MASTER DATA
# ==========================================
secondary_data = """ol,Sec_Min,Sec_Avg,Sec_Max,Sec_Rent_Yield,Sec_Cap_App,Crash_Drop
Bulgari Resort,2000,2307,2600,0.05,0.05,-0.15
Jumeirah Bay Island,1400,1644,1900,0.05,0.05,-0.15
Pearl Jumeira,1000,1180,1400,0.06,0.05,-0.15
DIFC,1000,1153,1300,0.06,0.05,-0.15
La Mer,900,1058,1200,0.06,0.05,-0.15
Emirates Hills,800,938,1100,0.05,0.05,-0.15
Downtown Dubai,800,933,1100,0.06,0.05,-0.15
Palm Jumeirah,750,895,1050,0.06,0.05,-0.15
World Islands,700,869,1000,0.06,0.05,-0.15
Madinat Jumeirah Living,700,865,1000,0.06,0.05,-0.15
Dubai Harbour,650,777,900,0.06,0.05,-0.15
Umm Suqeim,650,776,900,0.06,0.05,-0.15
City Walk,650,769,900,0.06,0.05,-0.15
Bluewaters Island,600,746,900,0.06,0.05,-0.15
Jumeirah 2,600,734,850,0.06,0.05,-0.15
Jumeirah 3,600,719,850,0.06,0.05,-0.15
Jumeirah 1,600,710,850,0.06,0.05,-0.15
Business Bay,500,618,750,0.07,0.06,-0.18
Jumeirah Islands,450,560,700,0.06,0.05,-0.15
Mohammed Bin Rashid City,450,554,700,0.06,0.05,-0.15
Sobha Hartland,450,552,700,0.06,0.05,-0.15
Jumeirah Beach Residence,450,542,650,0.07,0.06,-0.18
Dubai Islands,400,516,650,0.07,0.06,-0.18
Meydan,400,509,650,0.07,0.06,-0.18
Dubai Marina,400,506,650,0.07,0.06,-0.18
Dubai Hills Estate,400,499,650,0.06,0.05,-0.15
Dubai Creek Harbour,400,497,650,0.07,0.06,-0.18
The Meadows,400,494,650,0.06,0.05,-0.15
Jumeirah Park,400,488,650,0.06,0.05,-0.15
The Lakes,400,487,650,0.06,0.05,-0.15
Arabian Ranches 2,350,474,600,0.06,0.05,-0.15
Arabian Ranches 3,350,468,600,0.06,0.05,-0.15
Maritime City,350,462,600,0.07,0.06,-0.18
Jumeirah Golf Estates,350,457,600,0.06,0.05,-0.15
Arabian Ranches,350,437,600,0.06,0.05,-0.15
Azizi Riviera,350,436,600,0.07,0.06,-0.18
The Views,350,427,600,0.07,0.06,-0.18
The Springs,350,426,600,0.06,0.05,-0.15
The Greens,300,394,500,0.07,0.06,-0.18
Dubai Festival City,300,387,500,0.07,0.06,-0.18
Al Reem,300,362,500,0.06,0.05,-0.15
Bukadra,300,360,500,0.07,0.06,-0.18
Tilal Al Ghaf,250,329,450,0.06,0.05,-0.15
Al Mamzar,250,312,450,0.07,0.06,-0.18
DAMAC Lagoons,250,310,450,0.06,0.05,-0.15
Al Barsha,250,307,450,0.07,0.06,-0.18
Damac Hills,200,287,400,0.07,0.06,-0.18
Jumeirah Lake Towers,200,282,400,0.07,0.06,-0.18
Sustainable City,200,277,400,0.06,0.05,-0.15
Karama,200,273,400,0.07,0.06,-0.18
Al Furjan,200,272,400,0.07,0.06,-0.18
Reem Mira,200,268,400,0.07,0.06,-0.18
Mira,200,266,400,0.07,0.06,-0.18
Mudon,200,265,400,0.07,0.06,-0.18
Living Legends,200,263,400,0.07,0.06,-0.18
Al Barsha South,200,257,400,0.07,0.06,-0.18
Al Warqa,200,256,400,0.07,0.06,-0.18
Bur Dubai,200,254,400,0.07,0.06,-0.18
Motor City,200,248,400,0.07,0.06,-0.18
Deira,200,247,400,0.07,0.06,-0.18
Green Community,200,240,400,0.06,0.05,-0.15
Mirdif,200,240,400,0.06,0.05,-0.15
Jumeirah Village Triangle,200,239,400,0.07,0.06,-0.18
Falcon City of Wonders,200,234,400,0.07,0.06,-0.18
Jumeirah Village Circle,180,227,350,0.08,0.07,-0.25
Al Nahda,180,222,350,0.07,0.06,-0.18
Expo City,180,217,350,0.07,0.06,-0.18
Dubai Silicon Oasis,160,207,300,0.08,0.07,-0.25
Majan,160,207,300,0.08,0.07,-0.25
Al Qusais,160,205,300,0.07,0.06,-0.18
Dubai Sports City,160,204,300,0.08,0.07,-0.25
Liwan,160,201,300,0.08,0.07,-0.25
The Valley,150,190,280,0.07,0.06,-0.18
Damac Hills 2,150,190,280,0.07,0.06,-0.18
Discovery Gardens,150,188,280,0.08,0.07,-0.25
Dubai Studio City,140,181,250,0.08,0.07,-0.25
Dubai Production City,140,174,250,0.08,0.07,-0.25
Town Square,130,171,250,0.08,0.07,-0.25
Dubai Investment Park,130,171,250,0.07,0.06,-0.18
Dubailand,130,171,250,0.08,0.07,-0.25
Jebel Ali,120,150,220,0.07,0.06,-0.18
Remraam,110,148,200,0.08,0.07,-0.25
International City,100,131,180,0.08,0.07,-0.25
Dubai South,90,122,180,0.08,0.07,-0.25"""

df_secondary = pd.read_csv(StringIO(secondary_data))
communities = sorted(df_secondary['ol'].unique())

# Location-based Holiday Home Multipliers
hh_multipliers = {
    'Downtown Dubai': 1.9, 'Palm Jumeirah': 2.0, 'Dubai Marina': 1.8, 'Jumeirah Beach Residence': 1.8,
    'Bluewaters Island': 1.9, 'City Walk': 1.8, 'Business Bay': 1.6, 'Jumeirah Village Circle': 1.5,
    'Dubai Hills Estate': 1.5, 'Arabian Ranches': 1.4, 'Arabian Ranches 2': 1.4, 'Arabian Ranches 3': 1.4,
    'Dubai Creek Harbour': 1.6, 'Jumeirah Lake Towers': 1.6, 'Meydan': 1.5, 'Dubai South': 1.2,
    'International City': 1.2, 'Discovery Gardens': 1.3, 'Jumeirah Village Triangle': 1.5
}

# ==========================================
# SIDEBAR INPUTS
# ==========================================
st.sidebar.markdown("### ⚙️ Property Parameters")
selected_community = st.sidebar.selectbox("Select Community", communities)
row = df_secondary[df_secondary['ol'] == selected_community].iloc[0]
base_price_psf = row['Sec_Avg']
base_lt_yield = row['Sec_Rent_Yield']

property_size = st.sidebar.number_input("Property Size (sqft)", value=800, step=50)
property_price = property_size * base_price_psf

st.sidebar.markdown("### 🏢 Building Age Factor")
age_bracket = st.sidebar.selectbox("Building Age", ["0-5 Years (New)", "5-10 Years (Mid)", "10+ Years (Old)"])

if "0-5" in age_bracket:
    age_yield_mod = 1.0
    maint_cost_psf = 5
elif "5-10" in age_bracket:
    age_yield_mod = 0.9
    maint_cost_psf = 8
else:
    age_yield_mod = 0.8
    maint_cost_psf = 12

st.sidebar.markdown("### 💸 Operational Costs")
lt_mgmt_fee = st.sidebar.slider("Long-Term Agent Fee (%)", 0, 10, 5, help="Annual renewal/management fee")
hh_mgmt_fee = st.sidebar.slider("Holiday Home Mgmt & Platform Fee (%)", 10, 25, 18)
furniture_cost = st.sidebar.number_input("One-time Furniture & Setup (AED)", value=60000, step=5000)

# ==========================================
# FINANCIAL MODELS & CALCULATIONS
# ==========================================
# 1. Normal Long-Term Rental Model
lt_gross_yield = base_lt_yield
lt_gross_income = property_price * lt_gross_yield
lt_expenses = lt_gross_income * (lt_mgmt_fee / 100) # Tenant pays DEWA/Maintenance in Dubai
lt_net_income = lt_gross_income - lt_expenses
lt_net_yield = (lt_net_income / property_price) * 100

# 2. Holiday Homes (Short-Term) Model
location_mult = hh_multipliers.get(selected_community, 1.4)
hh_gross_yield = base_lt_yield * location_mult * age_yield_mod
hh_gross_income = property_price * hh_gross_yield

hh_mgmt_cost = hh_gross_income * (hh_mgmt_fee / 100)
hh_maintenance = property_size * maint_cost_psf
hh_total_expenses = hh_mgmt_cost + hh_maintenance
hh_net_income = hh_gross_income - hh_total_expenses
hh_net_yield = (hh_net_income / property_price) * 100

# 3. True ROI & Payback (Holiday Homes)
acquisition_cost = property_price * 0.06 # 4% DLD + 2% Agency
total_hh_investment = property_price + acquisition_cost + furniture_cost
hh_true_roi = (hh_net_income / total_hh_investment) * 100
hh_payback = total_hh_investment / hh_net_income if hh_net_income > 0 else 0

# 4. 5-Year Wealth Projection (Holiday Homes)
years = list(range(1, 6))
hh_wealth = []
current_val = property_price
for i in years:
    current_val = current_val * 1.05
    hh_wealth.append(current_val + (hh_net_income * i))

# ==========================================
# THE HEAD-TO-HEAD BATTLE TABLE
# ==========================================
st.markdown('<div class="section-title">⚔️ The Investment Battle: Long-Term vs Holiday Homes</div>', unsafe_allow_html=True)

battle_html = f"""
<table class="battle-table">
    <tr>
        <th style="width: 30%;">Financial Metric</th>
        <th style="width: 35%;">🏢 Normal Long-Term Rental</th>
        <th style="width: 35%;">️ Holiday Homes (Short-Term)</th>
    </tr>
    <tr>
        <td class="header-cell">Gross Annual Yield</td>
        <td class="normal-text">{lt_gross_yield*100:.1f}%</td>
        <td class="winner-text">{hh_gross_yield*100:.1f}%</td>
    </tr>
    <tr>
        <td class="header-cell">Gross Annual Income</td>
        <td class="normal-text">AED {lt_gross_income:,.0f}</td>
        <td class="winner-text">AED {hh_gross_income:,.0f}</td>
    </tr>
    <tr>
        <td class="header-cell">Management / Agent Fees</td>
        <td class="normal-text">AED {lt_expenses:,.0f} ({lt_mgmt_fee}%)</td>
        <td class="normal-text">AED {hh_mgmt_cost:,.0f} ({hh_mgmt_fee}%)</td>
    </tr>
    <tr>
        <td class="header-cell">Maintenance & Bills</td>
        <td class="normal-text">AED 0 (Paid by Tenant)</td>
        <td class="normal-text">AED {hh_maintenance:,.0f} (Paid by Owner)</td>
    </tr>
    <tr>
        <td class="header-cell">One-Time Setup (Furniture)</td>
        <td class="normal-text">AED 0</td>
        <td class="normal-text">AED {furniture_cost:,}</td>
    </tr>
    <tr style="background-color: #e8f5e9;">
        <td class="header-cell" style="font-size: 18px;">NET POCKET YIELD</td>
        <td class="normal-text" style="font-size: 18px;">{lt_net_yield:.2f}%</td>
        <td class="winner-text" style="font-size: 20px;">{hh_net_yield:.2f}% </td>
    </tr>
    <tr style="background-color: #e8f5e9;">
        <td class="header-cell" style="font-size: 18px;">ANNUAL CASH IN HAND</td>
        <td class="normal-text" style="font-size: 18px;">AED {lt_net_income:,.0f}</td>
        <td class="winner-text" style="font-size: 20px;">AED {hh_net_income:,.0f} </td>
    </tr>
</table>
"""
st.markdown(battle_html, unsafe_allow_html=True)

# ==========================================
# KPI CARDS (Holiday Homes Deep Dive)
# ==========================================
st.markdown('<div class="section-title">📊 Holiday Homes Deep-Dive Financials</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">True ROI (incl. Setup)</div><div class="kpi-value highlight">{hh_true_roi:.2f}%</div></div>', unsafe_allow_html=True)
with col2: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Payback Period</div><div class="kpi-value">{hh_payback:.1f} Years</div></div>', unsafe_allow_html=True)
with col3: st.markdown(f'<div class="kpi-card"><div class="kpi-label">5-Year Total Wealth</div><div class="kpi-value highlight">AED {hh_wealth[-1]:,.0f}</div></div>', unsafe_allow_html=True)
with col4: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Extra Cash vs Long-Term</div><div class="kpi-value highlight">AED {hh_net_income - lt_net_income:,.0f}</div></div>', unsafe_allow_html=True)

st.info(f"💡 **Uzair Finance Insight:** By choosing Holiday Homes over Long-Term rental in **{selected_community}**, you generate **AED {hh_net_income - lt_net_income:,.0f}** extra cash every year. Your additional furniture investment of AED {furniture_cost:,} will be fully recovered in just **{furniture_cost / (hh_net_income - lt_net_income):.1f} years** purely from the extra income!")

# ==========================================
# CHARTS
# ==========================================
st.markdown('<div class="section-title">📉 5-Year Wealth Projection (Holiday Homes)</div>', unsafe_allow_html=True)
wealth_data = pd.DataFrame({
    'Year': years,
    'Property Value': [property_price * (1.05 ** y) for y in years],
    'Total Wealth (Value + Cashflow)': hh_wealth
}).set_index('Year')
st.line_chart(wealth_data)

# ==========================================
# AI ADVISOR
# ==========================================
st.markdown('<div class="section-title">🤖 Uzair Finance AI Advisor</div>', unsafe_allow_html=True)
user_question = st.text_input("💬 Ask the AI Advisor:", placeholder="e.g., Which one is better for passive income? or How fast will I recover furniture cost?")

if user_question:
    q = user_question.lower()
    extra_income = hh_net_income - lt_net_income
    recovery_time = furniture_cost / extra_income if extra_income > 0 else 0
    
    if any(w in q for w in ["better", "choose", "which", "recommend"]):
        st.info(f"**AI Advisor:** If your goal is maximum cash flow and wealth creation, **Holiday Homes** is the clear winner, yielding {hh_net_yield:.2f}% vs {lt_net_yield:.2f}%. However, if you want zero headaches and true 'passive' income, Long-Term is better. For investors, Holiday Homes mathematically outperforms.")
    elif any(w in q for w in ["passive", "hassle", "effort"]):
        st.info(f"**AI Advisor:** Long-Term rental is 95% passive. Holiday Homes requires professional management (which we factored in at {hh_mgmt_fee}%). Even with management fees, Holiday Homes still puts **AED {extra_income:,.0f}** more in your pocket annually.")
    elif any(w in q for w in ["furniture", "recover", "payback"]):
        st.info(f"**AI Advisor:** Your one-time furniture cost of AED {furniture_cost:,} will be completely recovered in just **{recovery_time:.1f} years** through the extra rental income. After that, it's pure extra profit for the lifespan of the property.")
    else:
        st.info("**AI Advisor:** I can help you compare yields, calculate payback periods, and understand the effort vs reward of both models. Ask specifically!")

# ==========================================
# FOOTER
# ==========================================
st.markdown('<div class="disclaimer-box"><strong>Disclaimer:</strong> Projections use unified secondary market averages adjusted for holiday home multipliers and building age. Actual performance varies by seasonality, DTCM regulations, and operator efficiency. True ROI includes 6% acquisition costs and furnishing.</div>', unsafe_allow_html=True)
st.markdown(f'<div class="footer"><h3>💼 UZAIR FINANCE</h3><p>Holiday Homes Intelligence • Dubai Real Estate</p><p style="font-size: 11px; opacity: 0.7;">© {datetime.now().year} Uzair Finance. All rights reserved.</p></div>', unsafe_allow_html=True)
