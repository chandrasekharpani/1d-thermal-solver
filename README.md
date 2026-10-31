# 1D Transient Multilayer Thermal Solver

A numerical engineering tool designed to solve 1D transient heat conduction across multi-layer material stacks incorporating interfacial Thermal Contact Resistance ($R_{tc}$). Built with Python, featuring native desktop (Tkinter/Matplotlib) and mobile (Flet) dynamic user interfaces.

##  Features
- **Numerical Engine:** 1D Fully Implicit Backward Euler finite difference solver for robust numerical stability.
- **Interfacial Resistance:** Accurately models temperature drops across material contact boundaries ($R_{tc}$).
- **Dynamic Layer Stacking:** Interactive "Outer-to-Inner" material selection (Aluminum, Copper, Stainless Steel, TIM, Silicon).
- **Visualization:** Real-time plotting of transient temperature profiles across spatial nodes.
- **Multi-Platform:** Native Tkinter Desktop GUI and Flet cross-platform mobile UI.

##  Tech Stack
- **Language:** Python 3.15.0
- **GUI Frameworks:** Tkinter, Flet
- **Numerical & Plotting:** NumPy, Matplotlib

##  How to Run

### Desktop Application
1. Ensure dependencies are installed:
   ```bash
   pip install matplotlib numpy
   