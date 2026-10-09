import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO
from datetime import datetime

# ==========================================
# UZAIR FINANCE BRANDING
# ==========================================
st.set_page_config(page_title="Uzair Finance Calculator", page_icon="💼", layout="wide")

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0a2540 0%, #1e3a5f 50%, #2d5a87 100%);
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(10,37,64,0.3);
    }
    .main-header h1 {
        font-size: 48px;
        font-weight: 800;
        margin: 0;
        letter-spacing: 2px;
    }
    .main-header .tagline {
        font-size: 16px;
        color: #ffd700;
        margin-top: 10px;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    .kpi-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #0a2540;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    .kpi-label {
        font-size: 12px;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 800;
        color: #0a2540;
        margin-top: 8px;
    }
    .section-title {
        color: #0a2540;
        font-size: 24px;
        font-weight: 700;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid #ffd700;
    }
    .disclaimer-box {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 20px;
        border-radius: 10px;
        margin-top: 30px;
        font-size: 12px;
        color: #856404;
    }
    .footer {
        text-align: center;
        padding: 30px;
        margin-top: 50px;
        background: #0a2540;
        color: white;
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>💼 UZAIR FINANCE</h1>
    <div class="tagline">Executive Wealth Calculator • Dubai Real Estate Intelligence</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 1. LOAD MASTER DATASETS
# ==========================================
offplan_data = """Community,OP_Min,OP_Avg,OP_Max,OP_Cap_App,Crash_Drop
Bulgari Resort,1737,2916,4678,0.1,-0.15
Emirates Hills,888,1694,2641,0.1,-0.15
Bluewaters Island,606,1246,1731,0.12,-0.18
Madinat Jumeirah Living,648,1133,1735,0.12,-0.18
City Walk,605,997,1547,0.12,-0.18
Jumeirah 1,598,992,1696,0.12,-0.18
Downtown Dubai,523,963,1423,0.1,-0.15
Jumeirah 3,523,963,1614,0.12,-0.18
Jumeirah Park,502,934,1432,0.12,-0.18
Arabian Ranches 2,535,927,1416,0.12,-0.18
Sobha Hartland,456,874,1319,0.12,-0.18
Dubai Marina,455,829,1270,0.1,-0.15
Mohammed Bin Rashid City,366,822,1312,0.12,-0.18
The Springs,385,811,1287,0.12,-0.18
Jumeirah Golf Estates,404,784,1195,0.12,-0.18
Meydan,399,721,1176,0.12,-0.18
Maritime City,408,651,932,0.12,-0.18
Al Reem,341,636,988,0.12,-0.18
Business Bay,314,608,931,0.12,-0.18
The Views,340,568,933,0.12,-0.18
Sustainable City,293,535,788,0.12,-0.18
Bukadra,288,529,797,0.12,-0.18
Jumeirah Lake Towers,285,503,727,0.12,-0.18
Damac Hills,253,486,786,0.12,-0.18
Green Community,242,482,748,0.12,-0.18
Living Legends,221,453,713,0.12,-0.18
Al Furjan,227,442,717,0.12,-0.18
Mudon,232,436,692,0.12,-0.18
Motor City,234,426,686,0.12,-0.18
Jumeirah Village Triangle,247,393,581,0.12,-0.18
Jumeirah Village Circle,197,363,610,0.15,-0.25
Liwan,194,344,500,0.15,-0.25
Dubai Silicon Oasis,172,332,499,0.15,-0.25
Dubailand,155,318,510,0.15,-0.25
Dubai Studio City,156,311,491,0.15,-0.25
Discovery Gardens,174,305,494,0.15,-0.25
Dubai Production City,170,297,444,0.15,-0.25
Dubai South,133,279,427,0.15,-0.25
Remraam,154,266,402,0.15,-0.25"""

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

df_offplan = pd.read_csv(StringIO(offplan_data))
df_secondary = pd.read_csv(StringIO(secondary_data))
locations = sorted(list(set(df_offplan['Community'].tolist() + df_secondary['ol'].tolist())))

# ==========================================
# 2. SIDEBAR INPUTS
# ==========================================
st.sidebar.markdown("### ⚙️ Portfolio Parameters")
client_name = st.sidebar.text_input("Client Name", value="Mr. Investor")
budget = st.sidebar.number_input("Total Budget (AED)", value=5000000, step=100000)
location = st.sidebar.selectbox("Preferred Location", locations, index=locations.index("Dubai South") if "Dubai South" in locations else 0)
market_split = st.sidebar.selectbox("Market Split (Secondary / Off-Plan)", ["60/40", "50/50", "40/60", "30/70", "70/30"], index=0)
horizon = st.sidebar.slider("Investment Horizon (Years)", 3, 15, 5)
friction_cost = st.sidebar.number_input("Friction Cost (DLD + Agency)", value=0.06, step=0.01, format="%.2f")

# ==========================================
# 3. FINANCIAL CALCULATIONS
# ==========================================
sec_pct, op_pct = map(int, market_split.split('/'))
sec_pct /= 100
op_pct /= 100

budg_sec = budget * sec_pct
budg_op = budget * op_pct

principal_sec = budg_sec / (1 + friction_cost)
principal_op = budg_op / (1 + friction_cost)

op_data = df_offplan[df_offplan['Community'] == location]
sec_data = df_secondary[df_secondary['ol'] == location]

op_cap_app = op_data['OP_Cap_App'].values[0] if not op_data.empty else 0.10
crash_drop = sec_data['Crash_Drop'].values[0] if not sec_data.empty else (op_data['Crash_Drop'].values[0] if not op_data.empty else -0.15)
sec_rent_yield = sec_data['Sec_Rent_Yield'].values[0] if not sec_data.empty else 0.06
sec_cap_app = sec_data['Sec_Cap_App'].values[0] if not sec_data.empty else 0.05

value_op = principal_op * ((1 + op_cap_app) ** horizon)
annual_rent = principal_sec * sec_rent_yield
total_rent = annual_rent * horizon
value_sec = principal_sec * ((1 + sec_cap_app) ** horizon)

total_portfolio_value = value_op + value_sec + total_rent
projected_capital_gain = (value_op - principal_op) + (value_sec - principal_sec)

weighted_return = (sec_cap_app * sec_pct) + (op_cap_app * op_pct) + (sec_rent_yield * sec_pct)
risk_score = min(10.0, round((weighted_return / abs(crash_drop)) * 10, 1))

# ==========================================
# 4. KPI CARDS
# ==========================================
st.markdown('<div class="section-title">📊 Portfolio Summary</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Projected Capital Gain</div>
        <div class="kpi-value">AED {projected_capital_gain:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Expected Rental Income</div>
        <div class="kpi-value">AED {total_rent:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Portfolio Value</div>
        <div class="kpi-value">AED {total_portfolio_value:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Risk Adjusted Score</div>
        <div class="kpi-value">{risk_score} / 10</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. PHASED DEPLOYMENT TABLE
# ==========================================
st.markdown('<div class="section-title">📈 Phased Capital Deployment & Equity Recycling</div>', unsafe_allow_html=True)

rows = []
for t in [3, 5, 10]:
    op_10 = principal_op * ((1 + 0.10) ** t)
    op_15 = principal_op * ((1 + 0.15) ** t)
    
    if t <= 3:
        op_100 = principal_op * (1 + (1.0 * (t/3)))
    else:
        op_100 = (principal_op * 2.0) * ((1 + sec_cap_app) ** (t - 3))
        
    sec_7 = (principal_sec * ((1 + 0.07) ** t)) + (principal_sec * sec_rent_yield * t)
    sec_10 = (principal_sec * ((1 + 0.10) ** t)) + (principal_sec * sec_rent_yield * t)
    
    realistic_value = (principal_op * ((1 + op_cap_app) ** t)) + (principal_sec * ((1 + sec_cap_app) ** t)) + (principal_sec * sec_rent_yield * t)
    net_profit_pct = round(((realistic_value - budget) / budget) * 100, 1)
    
    rows.append({
        "Timeframe": f"{t} Years",
        "Off-Plan (10% Cons.)": f"AED {op_10:,.0f}",
        "Off-Plan (15% Real.)": f"AED {op_15:,.0f}",
        "Off-Plan (100% Special)": f"AED {op_100:,.0f}",
        "Secondary (7% + Rent)": f"AED {sec_7:,.0f}",
        "Secondary (10% + Rent)": f"AED {sec_10:,.0f}",
        "Net Profit %": f"{net_profit_pct}%"
    })

df_table = pd.DataFrame(rows)
st.dataframe(df_table, use_container_width=True, height=200)

# ==========================================
# 6. CHARTS
# ==========================================
st.markdown('<div class="section-title"> Portfolio Growth Visualization</div>', unsafe_allow_html=True)

years = list(range(1, horizon + 1))
growth_op = [principal_op * ((1 + op_cap_app) ** t) for t in years]
growth_sec = [principal_sec * ((1 + sec_cap_app) ** t) for t in years]
growth_rent = [principal_sec * sec_rent_yield * t for t in years]
total_growth = [growth_op[i] + growth_sec[i] + growth_rent[i] for i in range(len(years))]

fig_g = go.Figure()
fig_g.add_trace(go.Scatter(x=years, y=growth_op, mode='lines+markers', name='Off-Plan Capital', line=dict(color='#ff9800', width=3)))
fig_g.add_trace(go.Scatter(x=years, y=growth_sec, mode='lines+markers', name='Secondary Capital', line=dict(color='#2196f3', width=3)))
fig_g.add_trace(go.Scatter(x=years, y=growth_rent, mode='lines+markers', name='Cumulative Rent', line=dict(color='#4caf50', width=3)))
fig_g.add_trace(go.Scatter(x=years, y=total_growth, mode='lines+markers', name='Total Portfolio Value', line=dict(width=5, color='#673ab7')))
fig_g.update_layout(title="Portfolio Growth Over Time", xaxis_title="Years", yaxis_title="Value (AED)", template="plotly_white", height=500)

col_chart1, col_chart2 = st.columns(2)
with col_chart1:
    st.plotly_chart(fig_g, use_container_width=True)

with col_chart2:
    fig_s = px.pie(values=[budg_sec, budg_op], names=["Secondary Market", "Off-Plan Market"], 
                   title="Budget Allocation", color_discrete_sequence=['#2196f3', '#ff9800'], hole=0.4)
    fig_s.update_layout(template="plotly_white", height=500)
    st.plotly_chart(fig_s, use_container_width=True)

# ==========================================
# 7. CRASH SCENARIO
# ==========================================
st.markdown('<div class="section-title">⚠️ Risk Management & Market Crash Scenario</div>', unsafe_allow_html=True)

crash_value = total_portfolio_value * (1 + crash_drop)
crash_loss = budget - crash_value

col_c1, col_c2, col_c3 = st.columns(3)
with col_c1:
    st.metric("Historical Crash Drop", f"{crash_drop*100:.0f}%")
with col_c2:
    st.metric("Portfolio Value in Crash", f"AED {crash_value:,.0f}")
with col_c3:
    st.metric("Potential Loss", f"AED {crash_loss:,.0f}")

# ==========================================
# 8. AI FINANCIAL ADVISOR (Agentic Feel)
# ==========================================
st.markdown('<div class="section-title">🤖 Uzair Finance AI Advisor</div>', unsafe_allow_html=True)

st.markdown("*Ask questions about your investment strategy. The AI analyzes your portfolio and provides personalized recommendations.*")

# Rule-based AI agent
ai_responses = {
    "risk": f"Based on your portfolio, your risk-adjusted score is {risk_score}/10. "
            f"Your selected location ({location}) has a historical crash drop of {crash_drop*100:.0f}%. "
            f"{'This is a relatively safe investment.' if risk_score > 7 else 'Consider diversifying to reduce risk.'}",
    
    "rental": f"Your expected annual rental income is AED {annual_rent:,.0f}, "
              f"with a yield of {sec_rent_yield*100:.1f}%. "
              f"Over {horizon} years, you'll earn AED {total_rent:,.0f} in rent alone.",
    
    "growth": f"Your portfolio is projected to grow from AED {budget:,.0f} to AED {total_portfolio_value:,.0f} "
              f"over {horizon} years, representing a {((total_portfolio_value/budget)-1)*100:.1f}% total return.",
    
    "recommendation": f"For your budget of AED {budget:,.0f} with a {market_split} split, "
                      f"I recommend focusing on {location} which shows strong fundamentals. "
                      f"Consider increasing off-plan allocation if you have a longer horizon (7+ years).",
    
    "default": "I can help you with: risk analysis, rental income projections, growth forecasts, and investment recommendations. Please ask specific questions about your portfolio."
}

user_question = st.text_input("💬 Ask the AI Advisor:", placeholder="e.g., What is my risk level? or Tell me about rental income")

if user_question:
    question_lower = user_question.lower()
    
    if any(word in question_lower for word in ["risk", "safe", "crash"]):
        response = ai_responses["risk"]
    elif any(word in question_lower for word in ["rent", "rental", "income", "yield"]):
        response = ai_responses["rental"]
    elif any(word in question_lower for word in ["growth", "return", "profit", "gain"]):
        response = ai_responses["growth"]
    elif any(word in question_lower for word in ["recommend", "suggest", "advice", "best"]):
        response = ai_responses["recommendation"]
    else:
        response = ai_responses["default"]
    
    st.info(f"**AI Advisor:** {response}")

# ==========================================
# 9. DISCLAIMER & FOOTER
# ==========================================
st.markdown("""
<div class="disclaimer-box">
    <strong>Disclaimer:</strong> The '100% Special Case' represents extreme outlier projects achieving 100% total appreciation at handover. 
    This is not an annualized rate. Standard market expectation remains 10% to 15% annually. 
    All projections include friction cost for DLD and Agency fees. Past performance does not guarantee future results.
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="footer">
    <h3>💼 UZAIR FINANCE</h3>
    <p>Executive Wealth Calculator • Dubai Real Estate Intelligence</p>
    <p style="font-size: 11px; opacity: 0.7;">© {datetime.now().year} Uzair Finance. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
