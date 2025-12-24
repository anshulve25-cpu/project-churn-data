import os
import sys
os.system(f"{sys.executable} -m pip install plotly")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Customer Churn Analysis | Data Analyst Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A5F;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .insight-box {
        background-color: #f0f7ff;
        border-left: 4px solid #1E3A5F;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
    .recommendation-box {
        background-color: #f0fff4;
        border-left: 4px solid #38a169;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
    .sql-box {
        background-color: #1a1a2e;
        color: #00d4ff;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E3A5F;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def generate_data():
    np.random.seed(42)
    n_customers = 7043
    customer_ids = [f'CUST{str(i).zfill(6)}' for i in range(1, n_customers + 1)]
    contract_types = np.random.choice(
        ['Month-to-Month', 'One Year', 'Two Year'],
        size=n_customers,
        p=[0.55, 0.25, 0.20]
    )
    payment_methods = np.random.choice(
        ['Electronic Check', 'Mailed Check', 'Bank Transfer', 'Credit Card'],
        size=n_customers,
        p=[0.35, 0.20, 0.22, 0.23]
    )
    internet_service = np.random.choice(
        ['Fiber Optic', 'DSL', 'No Internet'],
        size=n_customers,
        p=[0.45, 0.35, 0.20]
    )
    tenure = []
    for contract in contract_types:
        if contract == 'Month-to-Month':
            tenure.append(max(1, int(np.random.exponential(15))))
        elif contract == 'One Year':
            tenure.append(max(12, int(np.random.normal(36, 15))))
        else:
            tenure.append(max(24, int(np.random.normal(50, 12))))
    tenure = np.clip(tenure, 1, 72)
    monthly_charges = []
    for internet in internet_service:
        if internet == 'Fiber Optic':
            monthly_charges.append(np.random.normal(85, 15))
        elif internet == 'DSL':
            monthly_charges.append(np.random.normal(55, 12))
        else:
            monthly_charges.append(np.random.normal(30, 8))
    monthly_charges = np.clip(monthly_charges, 18, 120)
    total_charges = np.array(tenure) * np.array(monthly_charges) * np.random.uniform(0.9, 1.1, n_customers)
    churn = []
    for i in range(n_customers):
        base_prob = 0.15
        if contract_types[i] == 'Month-to-Month':
            base_prob += 0.35
        elif contract_types[i] == 'One Year':
            base_prob += 0.10
        if payment_methods[i] == 'Electronic Check':
            base_prob += 0.15
        elif payment_methods[i] == 'Mailed Check':
            base_prob += 0.05
        if tenure[i] <= 6:
            base_prob += 0.20
        elif tenure[i] <= 12:
            base_prob += 0.10
        elif tenure[i] > 48:
            base_prob -= 0.15
        if monthly_charges[i] > 80:
            base_prob += 0.08
        churn.append('Yes' if np.random.random() < min(base_prob, 0.85) else 'No')
    df = pd.DataFrame({
        'CustomerID': customer_ids,
        'Tenure': tenure,
        'MonthlyCharges': np.round(monthly_charges, 2),
        'TotalCharges': np.round(total_charges, 2),
        'ContractType': contract_types,
        'PaymentMethod': payment_methods,
        'InternetService': internet_service,
        'Churn': churn
    })
    return df

df = generate_data()

total_customers = len(df)
churned_customers = len(df[df['Churn'] == 'Yes'])
churn_rate = (churned_customers / total_customers) * 100
monthly_revenue = df['MonthlyCharges'].sum()
revenue_at_risk = df[df['Churn'] == 'Yes']['MonthlyCharges'].sum() * 12
avg_tenure = df['Tenure'].mean()

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/combo-chart.png", width=80)
    st.title("Navigation")
    page = st.radio(
        "Select Page",
        ["📊 Executive Dashboard", "🔍 Detailed Analysis", "💻 SQL Queries", 
         "💡 Insights & Recommendations", "📋 About This Project"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("### 📁 Project Info")
    st.markdown("""
    **Dataset:** Telecom Customers  
    **Records:** 7,043 customers  
    **Analysis Type:** Churn Analysis  
    **Tools:** Python, SQL, Streamlit
    """)
    st.markdown("---")
    st.markdown("### 🔗 Connect")
    st.markdown("""
    [GitHub](https://github.com) | [LinkedIn](https://linkedin.com)
    """)

if page == "📊 Executive Dashboard":
    st.markdown('<p class="main-header">📊 Customer Churn Analysis Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Telecom Business Intelligence | Real-time Customer Retention Insights</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total Customers",
            value=f"{total_customers:,}",
            delta="Active base"
        )
    
    with col2:
        st.metric(
            label="Churn Rate",
            value=f"{churn_rate:.1f}%",
            delta=f"-{churned_customers:,} customers",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Revenue at Risk",
            value=f"${revenue_at_risk/1e6:.2f}M",
            delta="Annual",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="Avg Monthly Revenue",
            value=f"${df['MonthlyCharges'].mean():.2f}",
            delta="Per customer"
        )
    
    with col5:
        st.metric(
            label="Avg Tenure",
            value=f"{avg_tenure:.1f} months",
            delta="Customer lifetime"
        )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Overall Churn Distribution")
        churn_counts = df['Churn'].value_counts()
        fig = px.pie(
            values=churn_counts.values,
            names=['Retained', 'Churned'],
            color_discrete_sequence=['#2E86AB', '#E94F37'],
            hole=0.4
        )
        fig.update_layout(
            font=dict(size=14),
            showlegend=True,
            height=350
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
       st.subheader("Churn Rate by Contract Type")

       with col2:
        st.subheader("Churn Rate by Contract Type")

    contract_churn = (
        df.assign(ChurnFlag=df['Churn'].map({'Yes': 1, 'No': 0}))
          .groupby('ContractType')
          .agg(churn_rate=('ChurnFlag', 'mean'))
          .reset_index()
    )

    fig2 = px.bar(
        contract_churn,
        x='ContractType',
        y='churn_rate',
        text=contract_churn['churn_rate'].apply(lambda x: f"{x*100:.1f}%"),
        color='ContractType'
    )

    fig2.update_layout(
        yaxis_tickformat=".0%",
        height=350,
        showlegend=False
    )

    st.plotly_chart(fig2, use_container_width=True)


    fig = px.bar(
        contract_churn,
        x='ContractType',
        y='churn_rate',
        text=contract_churn['churn_rate'].apply(lambda x: f"{x*100:.1f}%"),
        color='ContractType',
        color_discrete_sequence=['#E94F37', '#F4A261', '#2E86AB']
    )

    fig.update_layout(
        yaxis_tickformat='.0%',
        height=350,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
           
