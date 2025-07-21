import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sustainability Impact Simulator", layout="wide")

st.title("🌍 Sustainability Impact Simulator")
st.markdown("Simulate how sustainability levers affect environmental and financial KPIs.")

# ---------------------------
# INITIAL STATE / BASELINE
# ---------------------------
baseline_inputs = {
    "Material Greening": 20,
    "Energy Optimization": 30,
    "Take-back Incentives": 15,
    "Recycling Investment": 25,
    "Local Sourcing": 40,
    "Green Marketing": 10,
    "Pricing Level": 50,
    "Circular R&D": 20
}

# ---------------------------
# SIDEBAR INPUTS
# ---------------------------
st.sidebar.header("🛠️ Control Levers")
user_inputs = {}
for key, default in baseline_inputs.items():
    user_inputs[key] = st.sidebar.slider(key, 0, 100, default)

# ---------------------------
# SIMULATE KPIs (Replace with model later)
# ---------------------------
def simulate_kpis(inputs):
    # Dummy model logic for now
    return {
        "CO₂ Emissions": 21300 - inputs["Energy Optimization"] * 50 - inputs["Local Sourcing"] * 30,
        "Circularity Index (%)": 16.7 + inputs["Material Greening"] * 0.3 + inputs["Circular R&D"] * 0.5,
        "Sustainability ROI": 2.21 - inputs["Recycling Investment"] * 0.002,
        "Green OpEx (FCFA)": 1.9e6 + inputs["Green Marketing"] * 10000 + inputs["Recycling Investment"] * 5000,
        "Profit Margin (%)": 28 + inputs["Pricing Level"] * 0.05 - inputs["Green Marketing"] * 0.03
    }

baseline_kpis = simulate_kpis(baseline_inputs)
scenario_kpis = simulate_kpis(user_inputs)

# ---------------------------
# KPI DELTA TABLE
# ---------------------------
delta_table = []
for kpi in baseline_kpis.keys():
    base = baseline_kpis[kpi]
    scen = scenario_kpis[kpi]
    change = ((scen - base) / base) * 100 if base else 0
    delta_table.append([kpi, round(base, 2), round(scen, 2), f"{change:+.1f}%"])

delta_df = pd.DataFrame(delta_table, columns=["KPI", "Baseline", "Scenario", "Change (%)"])

# ---------------------------
# DISPLAY SIDE-BY-SIDE
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Final KPIs - Scenario")
    st.dataframe(pd.DataFrame([scenario_kpis]).T.rename(columns={0: "Value"}), use_container_width=True)

with col2:
    st.subheader("🔁 Delta Impact Table")
    st.dataframe(delta_df, use_container_width=True)

# ---------------------------
# EXPORT BUTTONS
# ---------------------------
st.markdown("### 📤 Export Results")
col1, col2 = st.columns(2)
with col1:
    csv = delta_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "impact_results.csv", "text/csv")

with col2:
    st.info("🔄 Replace dummy model with real simulation logic for full power.")

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.markdown("Built with ❤️ using [OptimScale] for classroom sustainability simulation.")
