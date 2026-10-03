import streamlit as st
import pandas as pd
import numpy as np
import pulp
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="PV-BESS Digital Twin Optimizer",
    page_icon="☀️",
    layout="wide"
)

st.title("☀️ Co-located PV-BESS Asset Digital Twin")
st.markdown("Advanced MILP optimization dashboard for optimal day-ahead energy dispatch and revenue maximization.")

# Sidebar Controls
st.sidebar.header("Simulation Parameters")
pv_capacity = st.sidebar.slider("PV Capacity (MW)", 1.0, 10.0, 3.0, 0.5)
bess_power = st.sidebar.slider("BESS Max Power (MW)", 0.5, 5.0, 1.0, 0.5)
bess_energy = st.sidebar.slider("BESS Capacity (MWh)", 1.0, 10.0, 4.0, 0.5)
initial_soc = st.sidebar.slider("Initial State of Charge (MWh)", 0.5, bess_energy, 2.0, 0.5)

# Run Simulation Button
if st.sidebar.button("Run MILP Optimization"):
    with st.spinner("Solving Mixed-Integer Linear Programming model..."):
        T = list(range(24))
        
        # Synthetic weather & prices
        np.random.seed(42)
        solar = np.maximum(0, pv_capacity * np.sin(np.pi * (np.array(T) - 6) / 12))
        solar[0:6] = 0
        solar[19:] = 0

        prices = 50 + 20 * np.sin(2 * np.pi * np.array(T) / 24) + np.random.normal(0, 5, 24)
        prices[17:21] += 40

        # PuLP Model
        model = pulp.LpProblem("PV_BESS_Digital_Twin", pulp.LpMaximize)

        bp = float(bess_power)
        be = float(bess_energy)
        init_s = float(initial_soc)

        # Using positional arguments for bulletproof PuLP compatibility
        P_charge = {t: pulp.LpVariable(f"P_charge_{t}", 0.0, bp, 'Continuous') for t in T}
        P_discharge = {t: pulp.LpVariable(f"P_discharge_{t}", 0.0, bp, 'Continuous') for t in T}
        SOC = {t: pulp.LpVariable(f"SOC_{t}", 0.5, be, 'Continuous') for t in T}
        u_charge = {t: pulp.LpVariable(f"u_charge_{t}", cat='Binary') for t in T}
        u_discharge = {t: pulp.LpVariable(f"u_discharge_{t}", cat='Binary') for t in T}

        revenue_expr = pulp.lpSum([(solar[t] + P_discharge[t] - P_charge[t]) * prices[t] for t in T])
        degradation_penalty = pulp.lpSum([(P_charge[t] + P_discharge[t]) * 1.5 for t in T])
        model += revenue_expr - degradation_penalty

        model += SOC[0] == init_s

        for t in T:
            model += u_charge[t] + u_discharge[t] <= 1
            model += P_charge[t] <= bp * u_charge[t]
            model += P_discharge[t] <= bp * u_discharge[t]
            
            if t > 0:
                model += SOC[t] == SOC[t-1] + (0.95 * P_charge[t] - (1 / 0.95) * P_discharge[t])
                
            model += solar[t] + P_discharge[t] - P_charge[t] >= 0

        model.solve(pulp.PULP_CBC_CMD(msg=False))

        # Extract results
        results = []
        for t in T:
            results.append({
                'hour': t,
                'solar_mw': solar[t],
                'price_eur': prices[t],
                'charge_mw': pulp.value(P_charge[t]),
                'discharge_mw': pulp.value(P_discharge[t]),
                'net_export_mw': solar[t] + pulp.value(P_discharge[t]) - pulp.value(P_charge[t]),
                'soc_mwh': pulp.value(SOC[t])
            })

        df_opt = pd.DataFrame(results)
        total_rev = pulp.value(model.objective)

        # Metrics display
        col1, col2, col3 = st.columns(3)
        col1.metric("Optimization Status", pulp.LpStatus[model.status])
        col2.metric("Total Daily Revenue", f"€{total_rev:,.2f}")
        col3.metric("Peak Generation", f"{solar.max():.2f} MW")

        # Plotting
        st.subheader("📊 Optimized Operational Dispatch Profile")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df_opt['hour'], df_opt['solar_mw'], label='Solar PV (MW)', color='orange', linewidth=2)
        ax.plot(df_opt['hour'], df_opt['net_export_mw'], label='Grid Export (MW)', color='green', linestyle='--', linewidth=2)
        ax.plot(df_opt['hour'], df_opt['soc_mwh'], label='Battery SOC (MWh)', color='blue', linewidth=2)
        ax.set_xlabel("Hour of Day")
        ax.set_ylabel("Power / Energy")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

        st.subheader("📋 Detailed Hourly Dispatch Table")
        st.dataframe(df_opt, use_container_width=True)
else:
    st.info("👈 Use the sidebar parameters and click **Run MILP Optimization** to launch the digital twin simulation.")
