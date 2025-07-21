import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sustainability Simulation Tool", layout="wide")

st.title("🌱 Sustainability Simulation Tool")
st.markdown("Simulate the impact of sustainable business practices and visualize environmental and financial KPIs.")

# Input Controls
st.sidebar.header("🎛️ Control Panel")
u1 = st.sidebar.slider("Material Greening (% biodegradable packaging)", 0, 100, 20)
u2 = st.sidebar.slider("Energy Optimization (investment level)", 0, 100, 40)
u3 = st.sidebar.slider("Take-back Incentives (reward level)", 0, 100, 30)
u4 = st.sidebar.slider("Recycling Investment", 0, 100, 20)
u5 = st.sidebar.slider("Local Sourcing (%)", 0, 100, 40)
u6 = st.sidebar.slider("Green Marketing Budget", 0, 100, 30)
u7 = st.sidebar.slider("Pricing Level (relative %)", 50, 150, 100)
u8 = st.sidebar.slider("Circular R&D", 0, 100, 10)

# Simulation logic
def simulate(u1, u2, u3, u4, u5, u6, u7, u8):
    emissions = 21300 * (1 - 0.005*u1 - 0.006*u2 - 0.004*u3 - 0.003*u4)
    circularity = 16.7 + 0.2*u1 + 0.15*u4 + 0.25*u8
    roi = 2.21 - 0.002*(u2 + u4) + 0.001*u6
    opex = 1.9 + 0.005*(u2 + u4 + u5)
    profit_margin = 0.18 + 0.0005*(u7 - 100) - 0.0004*(u6)
    return emissions, circularity, roi, opex, profit_margin

emissions, circularity, roi, opex, profit_margin = simulate(u1, u2, u3, u4, u5, u6, u7, u8)

# Baseline
baseline = {
    "CO₂ Emissions": 21300,
    "Circularity Index": 16.7,
    "Sustainability ROI": 2.21,
    "Green OpEx": 1.9,
    "Profit Margin": 0.18
}

# Results Table
results = {
    "KPI": list(baseline.keys()),
    "Baseline": list(baseline.values()),
    "Student Scenario": [emissions, circularity, roi, opex, profit_margin]
}
df = pd.DataFrame(results)
df["Change"] = df["Student Scenario"] - df["Baseline"]

# Layout
col1, col2 = st.columns([2, 2])

with col1:
    st.subheader("📊 Bar Chart: KPI Comparison")
    fig_bar, ax = plt.subplots(figsize=(8, 4))
    bar_width = 0.35
    index = np.arange(len(df))
    ax.bar(index, df["Baseline"], bar_width, label="Baseline")
    ax.bar(index + bar_width, df["Student Scenario"], bar_width, label="Scenario")
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(df["KPI"], rotation=30)
    ax.set_ylabel("Value")
    ax.set_title("Baseline vs Scenario KPIs")
    ax.legend()
    st.pyplot(fig_bar)

with col2:
    st.subheader("🥧 Pie Chart: CO₂ Emissions")
    fig_pie, ax1 = plt.subplots()
    emission_reduction = [emissions, baseline["CO₂ Emissions"] - emissions]
    labels = ["Remaining Emissions", "Reduction"]
    ax1.pie(emission_reduction, labels=labels, autopct="%1.1f%%", startangle=90, colors=['#66b3ff', '#ff9999'])
    ax1.set_title("CO₂ Emissions Reduction")
    st.pyplot(fig_pie)

st.subheader("📋 Detailed KPI Table")
st.dataframe(df.style.format({"Baseline": "{:.2f}", "Student Scenario": "{:.2f}", "Change": "{:+.2f}"}))

st.download_button("📥 Download CSV", df.to_csv(index=False).encode("utf-8"), "simulation_results.csv", "text/csv")
