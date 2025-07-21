
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🌱 Sustainable Business Practices Simulation Tool")
st.subheader("What-If Impact Visualizer powered by OptimScale")

st.markdown("Adjust the levers below to simulate the impact of sustainability strategies on key KPIs.")

# Define simulation horizon
T = 12  # 12 months
time = np.arange(T)

# Initial state values (x₁ to x₉)
x0 = np.array([20000, 50000, 100, 10, 1000, 5, 50, 10000000, 2000000], dtype=float)

# Control inputs (sliders)
st.sidebar.header("🔧 Control Levers")

u1 = st.sidebar.slider("u1 – Material Greening (% budget)", 0, 100, 20)
u2 = st.sidebar.slider("u2 – Energy Optimization", 0, 100, 30)
u3 = st.sidebar.slider("u3 – Take-back Incentives", 0, 100, 10)
u4 = st.sidebar.slider("u4 – Recycling Investment", 0, 100, 15)
u5 = st.sidebar.slider("u5 – Local Sourcing (%)", 0, 100, 40)
u6 = st.sidebar.slider("u6 – Green Marketing", 0, 100, 25)
u7 = st.sidebar.slider("u7 – Pricing Level", 50, 150, 100)
u8 = st.sidebar.slider("u8 – Circular R&D", 0, 100, 20)

u = np.array([u1, u2, u3, u4, u5, u6, u7, u8], dtype=float) / 100  # Normalize

# Define simple B matrix (effect of controls on states)
B = np.array([
    [-300, -1000, 0, -200, 0, 0, 0, 0],
    [-500, -3000, 0, 0, 0, 0, 0, 0],
    [-50, 0, 0, -300, 0, 0, 0, 0],
    [20, 0, 0, 200, 0, 0, 0, 200],
    [0, 0, 100, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, -1, 0, 0, 0],
    [0, 0, 10, 0, 0, 10, 0, 0],
    [50000, 10000, 5000, 2000, 2000, 15000, 100000, 25000],
    [10000, 30000, 5000, 5000, 0, 4000, 20000, 15000]
])

# Initialize state tracking
X = np.zeros((T, len(x0)))
X[0] = x0.copy()

# Simulate the model
for t in range(1, T):
    X[t] = X[t - 1] + B @ u

# Compute KPIs
emissions_per_unit = X[:, 0] / X[:, 7]
circularity_index = X[:, 3] / (X[:, 2] + X[:, 3])
energy_cost_per_unit = (X[:, 1] * 0.2) / X[:, 7]
profit_margin = (X[:, 7] - X[:, 8]) / X[:, 7]
sustainability_roi = (x0[0] - X[:, 0]) / (X[:, 8] - x0[8] + 1e-3)

# Layout for visual output
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 KPI Trends Over Time")
    fig, ax = plt.subplots(2, 2, figsize=(10, 6))
    ax[0, 0].plot(time, emissions_per_unit, label="Emissions per Unit")
    ax[0, 1].plot(time, circularity_index, label="Circularity Index")
    ax[1, 0].plot(time, energy_cost_per_unit, label="Energy Cost per Unit")
    ax[1, 1].plot(time, profit_margin, label="Profit Margin")
    for a in ax.flat: a.legend(); a.grid(True)
    st.pyplot(fig)

with col2:
    st.markdown("### 🔢 Final KPI Summary")
    st.metric("Emissions per Unit", f"{emissions_per_unit[-1]:.2f} kg/unit")
    st.metric("Circularity Index", f"{circularity_index[-1]*100:.1f} %")
    st.metric("Energy Cost per Unit", f"{energy_cost_per_unit[-1]:,.0f} FCFA")
    st.metric("Profit Margin", f"{profit_margin[-1]*100:.2f} %")
    st.metric("Sustainability ROI", f"{sustainability_roi[-1]:.2f}")
