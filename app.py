import streamlit as st
import pandas as pd
from financial_logic import build_allocation_prompt, analyze_portfolio_csv
from market_data import get_stock_summary
from gemini_utils import setup_gemini, generate_allocation_response
import matplotlib.pyplot as plt
import yfinance as yf

# Set page configuration
st.set_page_config(page_title="AI Financial Advisor 💸", layout="wide", page_icon="📊")

# Custom CSS for larger fonts and styling
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-size: 20px !important;
        }
        h1, h2, h3, h4 {
            font-size: 25px !important;
        }
        .stTextInput>div>div>input,
        .stNumberInput input,
        .stSelectbox div[data-baseweb="select"] {
            font-size: 18px !important;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.6em 2em;
            font-size: 18px !important;
            margin-top: 1em;
        }
        .stMarkdown, .stDataFrame, .stForm {
            font-size: 18px !important;
        }
        .css-1v0mbdj p, .css-1v0mbdj {
            font-size: 18px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Load Gemini model
model = setup_gemini()

# Tabs
tab1, tab2, tab3 = st.tabs(["💼 Financial Planner", "📂 Portfolio Health Analyzer", "📈 Stock Summary"])

# --- Tab 1: Financial Planner ---
with tab1:
    st.header("💼 AI Financial Planner")
    with st.form("user_profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name :")
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            monthly_investment = st.number_input("Monthly Investment (₹)", min_value=1000, step=1000, value=10000)
            horizon = st.number_input("Investment Horizon (Years)", min_value=1, max_value=50, value=10)
        with col2:
            # goal = st.selectbox("Investment Goal", ["Wealth Building", "Retirement", "Child Education", "Other"])
            goal = st.text_input("Investement Goal")
            risk_level = st.selectbox("Risk Tolerance", ["Low", "Moderate", "High"])
        submitted = st.form_submit_button("Generate Plan")

    if submitted:
        profile = {
            "name" : name,
            "age": age,
            "monthly_investment": monthly_investment,
            "horizon": horizon,
            "goal": goal,
            "risk_level": risk_level
        }
        prompt = build_allocation_prompt(profile)
        result = generate_allocation_response(model, prompt)
        st.markdown("### 📊 Recommended Allocation")
        st.markdown(result)

# --- Tab 2: Portfolio Analyzer ---
with tab2:
    st.header("📂 Portfolio Health Analyzer")
    uploaded_file = st.file_uploader("Upload your portfolio CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

        # Analyze
        analysis_prompt = analyze_portfolio_csv(df)
        analysis = generate_allocation_response(model, analysis_prompt)
        st.markdown("### 📈 Portfolio Review")
        st.write(analysis)

        # --- Visualization Section ---
        st.markdown("## 📊 Portfolio Visualizations")

        # 1. Sector Pie Chart
        if "Sector" in df.columns:
            sector_counts = df["Sector"].value_counts()
            fig1, ax1 = plt.subplots()
            ax1.pie(sector_counts, labels=sector_counts.index, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.subheader("🧭 Sector Allocation")
            st.pyplot(fig1)
        else:
            st.info("Add a 'Sector' column to your CSV to view sector allocation pie chart.")

        # 2. P&L Bar Chart
        if all(col in df.columns for col in ["Buy Price", "Current Price", "Quantity"]):
            df["P&L"] = (df["Current Price"] - df["Buy Price"]) * df["Quantity"]
            fig2, ax2 = plt.subplots()
            ax2.bar(df["Stock"], df["P&L"], color=["green" if x >= 0 else "red" for x in df["P&L"]])
            ax2.set_ylabel("Profit / Loss (₹)")
            ax2.set_title("💹 Stock-wise Profit & Loss")
            plt.xticks(rotation=45)
            st.subheader("💸 Profit & Loss Overview")
            st.pyplot(fig2)
        else:
            st.info("Your CSV must include 'Buy Price', 'Current Price', and 'Quantity' for P&L chart.")

# --- Tab 3: Stock Summary ---
with tab3:
    st.markdown("<h2 style='font-size: 32px;'>📈 Stock Summary</h2>", unsafe_allow_html=True)
    ticker = st.text_input("Enter stock ticker (e.g., TCS.NS, INFY.NS, AAPL):", "TCS.NS")
    if st.button("Get Summary"):
        summary = get_stock_summary(ticker)
        st.markdown(f"<div style='font-size: 22px;'>{summary}</div>", unsafe_allow_html=True)

        # --- Show price chart ---
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="7d")
            st.subheader("📉 Price Trend (Last 7 Days)")
            st.line_chart(hist['Close'])
        except Exception as e:
            st.error(f"Could not plot chart: {e}")
