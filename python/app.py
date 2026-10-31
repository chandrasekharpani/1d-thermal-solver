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

# Multi-layer material definitions
layers = [
    {"k": 167.0, "rho": 2700, "cp": 896, "thickness": 0.01, "nodes": 15},   # Aluminum
    {"k": 2.0, "rho": 1500, "cp": 1000, "thickness": 0.002, "nodes": 10}, # TIM
    {"k": 14.9, "rho": 7900, "cp": 477, "thickness": 0.015, "nodes": 15}, # Steel
]
R_contacts = [1.2e-4, 2.5e-4]

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
        title="Temperature Distribution Across Multilayer Wall",
        xaxis_title="Spatial Position x [m]",
        yaxis_title="Temperature [K]",
        yaxis=dict(range=[T_cold - 5, T_hot + 5]),
        hovermode="x unified",
        height=550
    )
    
    st.plotly_chart(fig, use_container_width=True)