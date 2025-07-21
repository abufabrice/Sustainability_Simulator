import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sustainability Impact Simulator", layout="wide")

# --- Sidebar Inputs ---
st.sidebar.title("🛠️ Control Levers")
u1 = st.sidebar.slider("Material Greening", 0, 100, 20)
u2 = st.sidebar.slider("Energy Optimization", 0, 100, 40)
u3 = st.sidebar.slider("Take-back Incentives", 0, 100, 30)
u4 = st.sidebar.slider("Recycling Investment", 0, 100, 20)
u5 = st.sidebar.slider("Local Sourcing", 0, 100, 40)
u6 = st.sidebar.slider("Green Marketing", 0, 100, 30)
u7 = st.sidebar.slider("Pricing Level (%)", 50, 150, 100)
u8 = st.sidebar.slider("Circular R&D", 0, 100, 10)

# --- Simulation Function ---
def simulate(u1, u2, u3, u4, u5, u6, u7, u8):
    emissions = 21300 * (1 - 0.005*u1 - 0.006*u2 - 0.004*u3 - 0.003*u4)
    circularity = 16.7 + 0.2*u1 + 0.15*u4 + 0.25*u8
    roi = 2.21 - 0.002*(u2 + u4) + 0.001*u6
    opex = 1.9 + 0.005*(u2 + u4 + u5)
    profit_margin = 0.18 + 0.0005*(u7 - 100) - 0.0004*u6
    return emissions, circularity, roi, opex, profit_margin

# --- Compute Results ---
emissions, circularity, roi, opex, profit_margin = simulate(u1, u2, u3, u4, u5, u6, u7, u8)

baseline = {
    "CO₂ Emissions": 21300,
    "Circularity Index": 16.7,
    "Sustainability ROI": 2.21,
    "Green OpEx": 1.9,
    "Profit Margin": 0.18
}
scenario = {
    "CO₂ Emissions": emissions,
    "Circularity Index": circularity,
    "Sustainability ROI": roi,
    "Green OpEx": opex,
    "Profit Margin": profit_margin
}

# --- Results Table ---
df = pd.DataFrame({
    "KPI": list(baseline.keys()),
    "Baseline": list(baseline.values()),
    "Scenario": list(scenario.values())
})
df["Change"] = df["Scenario"] - df["Baseline"]
df["Change"] = df["Change"].apply(lambda x: f"{x:+.2%}" if isinstance(x, float) else x)

# --- Interface Layout ---
st.title("🌍 Sustainability Impact Simulator")
st.markdown("Simulate how sustainability levers affect environmental and financial KPIs.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Final KPIs - Scenario")
    kpi_df = pd.DataFrame.from_dict(scenario, orient='index', columns=["Value"]).reset_index()
    kpi_df.columns = ["KPI", "Value"]
    st.table(kpi_df)

with col2:
    st.subheader("🧮 Delta Impact Table")
    st.dataframe(df)

st.subheader("📈 Visualize the Impact")

# --- Bar Chart ---
st.markdown("### KPI Comparison: Baseline vs Scenario")
fig_bar, ax = plt.subplots(figsize=(8, 4))
index = np.arange(len(df))
bar_width = 0.35
ax.bar(index, df["Baseline"].astype(float), bar_width, label="Baseline")
ax.bar(index + bar_width, df["Scenario"].astype(float), bar_width, label="Scenario")
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(df["KPI"], rotation=25)
ax.set_ylabel("Value")
ax.legend()
st.pyplot(fig_bar)

# --- Pie Chart for CO2 ---
st.markdown("### CO₂ Emissions Breakdown")
fig_pie, ax_pie = plt.subplots()
emission_reduction = [scenario["CO₂ Emissions"], baseline["CO₂ Emissions"] - scenario["CO₂ Emissions"]]
labels = ["Remaining", "Reduction"]
colors = ["#1f77b4", "#ff7f0e"]
ax_pie.pie(emission_reduction, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
ax_pie.axis('equal')
st.pyplot(fig_pie)

# --- Export ---
st.subheader("📤 Export Results")
st.download_button("Download CSV", df.to_csv(index=False).encode(), file_name="simulation_results.csv", mime="text/csv")

