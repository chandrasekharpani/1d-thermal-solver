import streamlit as st
import plotly.graph_objects as go
from solver import solve_transient_thermal

st.set_page_config(page_title="Multilayer Thermal Solver", layout="wide")

st.title("🔥 Transient Multilayer Thermal & TCR Solver")
st.write("Interactive web dashboard powered by Python, SciPy, and Plotly.")

# Sidebar Controls
st.sidebar.header("Simulation Parameters")
t_final = st.sidebar.slider("Total Time [s]", 5.0, 50.0, 20.0, 1.0)
dt = st.sidebar.number_input("Time Step dt [s]", value=0.05, format="%.3f")
T_hot = st.sidebar.number_input("Hot Boundary Temperature [K]", value=400.0)
T_cold = st.sidebar.number_input("Cold Boundary Temperature [K]", value=300.0)

st.sidebar.markdown("---")
st.sidebar.header("Layer Thickness & Mesh Controls")

# Layer 1: Aluminum
st.sidebar.subheader("Layer 1: Aluminum")
L1_thick = st.sidebar.number_input("Thickness 1 [m]", value=0.01, format="%.4f")
L1_nodes = st.sidebar.slider("Nodes 1", 5, 40, 15)

# Layer 2: TIM (Thermal Interface Material)
st.sidebar.subheader("Layer 2: TIM")
L2_thick = st.sidebar.number_input("Thickness 2 [m]", value=0.002, format="%.4f")
L2_nodes = st.sidebar.slider("Nodes 2", 5, 40, 10)

# Layer 3: Steel
st.sidebar.subheader("Layer 3: Steel")
L3_thick = st.sidebar.number_input("Thickness 3 [m]", value=0.015, format="%.4f")
L3_nodes = st.sidebar.slider("Nodes 3", 5, 40, 15)

st.sidebar.markdown("---")
st.sidebar.header("Thermal Contact Resistance ($R_{tc}$)")
Rtc_1 = st.sidebar.number_input("R_tc (Layer 1-2) [m²K/W]", value=1.2e-4, format="%.1e")
Rtc_2 = st.sidebar.number_input("R_tc (Layer 2-3) [m²K/W]", value=2.5e-4, format="%.1e")

# Multi-layer material definitions linked to dynamic inputs
layers = [
    {"k": 167.0, "rho": 2700, "cp": 896, "thickness": L1_thick, "nodes": L1_nodes},   # Aluminum
    {"k": 2.0, "rho": 1500, "cp": 1000, "thickness": L2_thick, "nodes": L2_nodes}, # TIM
    {"k": 14.9, "rho": 7900, "cp": 477, "thickness": L3_thick, "nodes": L3_nodes}, # Steel
]
R_contacts = [Rtc_1, Rtc_2]

if st.button("Run Simulation", type="primary"):
    with st.spinner("Executing sparse matrix time-stepping loop..."):
        x_vec, time_axis, history = solve_transient_thermal(layers, R_contacts, t_final, dt, T_hot, T_cold)
        
    st.success("Simulation completed successfully!")
    
    # Interactive Plotly Visualization
    fig = go.Figure()
    
    # Add a trace for each saved time step
    for idx, t_val in enumerate(time_axis):
        fig.add_trace(go.Scatter(
            x=x_vec, 
            y=history[idx],
            mode='lines+markers',
            name=f"t = {t_val:.2f}s",
            visible=(idx == len(time_axis) - 1) # Show final state by default
        ))
        
    fig.update_layout(
        title="Temperature Distribution Across Multilayer Wall with TCR",
        xaxis_title="Spatial Position x [m]",
        yaxis_title="Temperature [K]",
        yaxis=dict(range=[T_cold - 5, T_hot + 5]),
        hovermode="x unified",
        height=550
    )
    
    st.plotly_chart(fig, use_container_width=True)