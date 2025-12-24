import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Customer Churn Analysis | Data Analyst Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main-header{font-size:2.5rem;font-weight:700;color:#1E3A5F;text-align:center}
.sub-header{font-size:1.1rem;color:#666;text-align:center;margin-bottom:2rem}
.section-header{font-size:1.5rem;font-weight:600;color:#1E3A5F;border-bottom:2px solid #e0e0e0}
.insight-box{background:#f0f7ff;border-left:4px solid #1E3A5F;padding:1rem}
.warning-box{background:#fff5f5;border-left:4px solid #E94F37;padding:1rem}
.success-box{background:#f0fff4;border-left:4px solid #38a169;padding:1rem}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def generate_data():
    np.random.seed(42)
    n = 7043

    df = pd.DataFrame({
        "CustomerID": [f"CUST{str(i).zfill(6)}" for i in range(1, n+1)],
        "Gender": np.random.choice(["Male", "Female"], n),
        "SeniorCitizen": np.random.choice([0,1], n, p=[0.84,0.16]),
        "ContractType": np.random.choice(["Month-to-Month","One Year","Two Year"], n, p=[0.55,0.25,0.20]),
        "PaymentMethod": np.random.choice(["Electronic Check","Mailed Check","Bank Transfer","Credit Card"], n),
        "InternetService": np.random.choice(["Fiber Optic","DSL","No Internet"], n),
        "Tenure": np.clip(np.random.exponential(24, n).astype(int), 1, 72),
        "MonthlyCharges": np.round(np.clip(np.random.normal(70, 20, n), 18, 120), 2)
    })

    df["TotalCharges"] = np.round(df["Tenure"] * df["MonthlyCharges"], 2)
    churn_prob = (
        (df["ContractType"] == "Month-to-Month") * 0.35 +
        (df["PaymentMethod"] == "Electronic Check") * 0.15 +
        (df["Tenure"] <= 6) * 0.20 +
        (df["MonthlyCharges"] > 80) * 0.08 + 0.15
    )
    df["Churn"] = np.where(np.random.rand(n) < churn_prob.clip(0,0.85), "Yes", "No")
    return df

df = generate_data()

total_customers = len(df)
churned_customers = (df["Churn"]=="Yes").sum()
churn_rate = churned_customers / total_customers * 100
retention_rate = 100 - churn_rate
revenue_at_risk = df.loc[df["Churn"]=="Yes","MonthlyCharges"].sum() * 12
avg_tenure = df["Tenure"].mean()

df["TenureGroup"] = pd.cut(df["Tenure"], [0,6,12,24,48,72],
    labels=["0-6","7-12","13-24","25-48","49-72"])

with st.sidebar:
    page = st.radio(
        "Navigation",
        ["🏠 Executive Dashboard","🔍 Detailed Analysis","💻 SQL Queries",
         "💡 Insights & Recommendations","📋 About This Project"]
    )
    st.metric("Customers", f"{total_customers:,}")
    st.metric("Churn Rate", f"{churn_rate:.1f}%")
    st.metric("Revenue at Risk", f"${revenue_at_risk/1e6:.2f}M")

if page == "🏠 Executive Dashboard":
    st.markdown("<p class='main-header'>Customer Churn Dashboard</p>", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Customers", total_customers)
    c2.metric("Churned", churned_customers)
    c3.metric("Retention Rate", f"{retention_rate:.1f}%")
    c4.metric("Avg Tenure", f"{avg_tenure:.1f} mo")

    c1,c2 = st.columns(2)

    with c1:
        fig = px.pie(
            values=[total_customers-churned_customers, churned_customers],
            names=["Retained","Churned"], hole=0.5
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        churn_contract = df.groupby("ContractType")["Churn"] \
            .apply(lambda x:(x=="Yes").mean()*100).reset_index(name="ChurnRate")
        fig = px.bar(churn_contract, x="ContractType", y="ChurnRate", text="ChurnRate")
        fig.update_traces(texttemplate="%{text:.1f}%")
        st.plotly_chart(fig, use_container_width=True)

elif page == "🔍 Detailed Analysis":
    st.markdown("<p class='main-header'>Detailed Analysis</p>", unsafe_allow_html=True)

    f_contract = st.multiselect("Contract", df["ContractType"].unique(), df["ContractType"].unique())
    f_df = df[df["ContractType"].isin(f_contract)]

    fig = px.scatter(
        f_df, x="Tenure", y="MonthlyCharges",
        color="Churn", opacity=0.6
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "💻 SQL Queries":
    st.markdown("<p class='main-header'>SQL Queries</p>", unsafe_allow_html=True)
    st.code("""
SELECT ContractType,
       ROUND(100.0 * SUM(CASE WHEN Churn='Yes' THEN 1 END)/COUNT(*),2) AS churn_rate
FROM customers
GROUP BY ContractType;
""", language="sql")

elif page == "💡 Insights & Recommendations":
    st.markdown("<p class='main-header'>Insights & Recommendations</p>", unsafe_allow_html=True)
    st.markdown("""
- Month-to-month customers show highest churn
- First 6 months are most critical
- Electronic check users are high risk
- Contract migration has highest ROI
""")

elif page == "📋 About This Project":
    st.markdown("<p class='main-header'>About This Project</p>", unsafe_allow_html=True)
    st.markdown("""
This project demonstrates an end-to-end churn analysis using:
- Python
- Pandas & NumPy
- Plotly
- Streamlit
""")

st.markdown("---")
st.markdown("© 2024 | Customer Churn Analysis Portfolio")
