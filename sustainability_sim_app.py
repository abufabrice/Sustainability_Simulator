import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample data — replace with real simulation results
baseline_data = {
    'CO₂ Emissions (kg)': 21300,
    'Energy Use (kWh)': 105000,
    'Waste Volume (tons)': 180,
    'Profit Margin (%)': 12
}

scenario_data = {
    'CO₂ Emissions (kg)': 14900,
    'Energy Use (kWh)': 92000,
    'Waste Volume (tons)': 110,
    'Profit Margin (%)': 15
}

# Delta computation
delta_data = {k: scenario_data[k] - v for k, v in baseline_data.items()}
delta_df = pd.DataFrame({
    'KPI': baseline_data.keys(),
    'Baseline': baseline_data.values(),
    'Scenario': scenario_data.values(),
    'Change': delta_data.values()
})

# Streamlit App UI
st.set_page_config(page_title="Sustainability Simulator", layout="wide")
st.title("🌿 Sustainability Simulator")
st.markdown("### ⚖️ Compare the impact of your sustainability strategies")

# KPI Table
st.subheader("📋 KPI Delta Table")
st.dataframe(delta_df)

# Bar Chart
st.subheader("📊 Baseline vs Scenario")
fig_bar, ax = plt.subplots(figsize=(8, 5))
x = list(baseline_data.keys())
x_pos = range(len(x))
width = 0.35
ax.bar([p - width/2 for p in x_pos], baseline_data.values(), width=width, label='Baseline')
ax.bar([p + width/2 for p in x_pos], scenario_data.values(), width=width, label='Scenario')
ax.set_xticks(x_pos)
ax.set_xticklabels(x, rotation=45, ha='right')
ax.set_ylabel('Values')
ax.set_title('Baseline vs Scenario KPIs')
ax.legend()
st.pyplot(fig_bar)

# Pie Chart
st.subheader("🥧 CO₂ Emissions Share")
fig_pie, ax_pie = plt.subplots()
labels = ['Baseline Emissions', 'Scenario Emissions']
values = [baseline_data['CO₂ Emissions (kg)'], scenario_data['CO₂ Emissions (kg)']]
ax_pie.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
ax_pie.axis('equal')
st.pyplot(fig_pie)

# Export CSV
csv = delta_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Results CSV", data=csv, file_name="sustainability_kpi_comparison.csv")
