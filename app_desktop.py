import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from solver import solve_transient_thermal

# Material Database
MATERIAL_DB = {
    "Aluminum (6061)": {"k": 167.0, "rho": 2700, "cp": 896},
    "Copper": {"k": 401.0, "rho": 8933, "cp": 385},
    "Stainless Steel": {"k": 14.9, "rho": 7900, "cp": 477},
    "Thermal Interface Material (TIM)": {"k": 2.0, "rho": 1500, "cp": 1000},
    "Silicon": {"k": 148.0, "rho": 2330, "cp": 712}
}

def run_simulation():
    try:
        t_final = float(entry_t_final.get())
        dt = float(entry_dt.get())
        T_hot = float(entry_hot.get())
        T_cold = float(entry_cold.get())
        
        # Build layers dynamically from Outer to Inner selections
        mat1 = combo_layer1.get()
        thick1 = float(entry_thick1.get())
        
        mat2 = combo_layer2.get()
        thick2 = float(entry_thick2.get())
        
        mat3 = combo_layer3.get()
        thick3 = float(entry_thick3.get())
        
        layers = [
            {"k": MATERIAL_DB[mat1]["k"], "rho": MATERIAL_DB[mat1]["rho"], "cp": MATERIAL_DB[mat1]["cp"], "thickness": thick1, "nodes": 15},
            {"k": MATERIAL_DB[mat2]["k"], "rho": MATERIAL_DB[mat2]["rho"], "cp": MATERIAL_DB[mat2]["cp"], "thickness": thick2, "nodes": 10},
            {"k": MATERIAL_DB[mat3]["k"], "rho": MATERIAL_DB[mat3]["rho"], "cp": MATERIAL_DB[mat3]["cp"], "thickness": thick3, "nodes": 15},
        ]
        
        # Contact resistances between layers
        R_contacts = [1.2e-4, 2.5e-4] 
        
        # Run core solver engine
        x_vec, time_axis, history = solve_transient_thermal(layers, R_contacts, t_final, dt, T_hot, T_cold)
        
        # Clear previous plot and draw new profile
        ax.clear()
        final_T = history[-1]
        
        ax.plot(x_vec * 1000, final_T, color='crimson', linewidth=2.5, label=f't = {t_final} s')
        ax.set_title(f'Outer-to-Inner Thermal Profile\n({mat1} -> {mat2} -> {mat3})', fontsize=10, fontweight='bold')
        ax.set_xlabel('Position [mm]', fontsize=9)
        ax.set_ylabel('Temperature [K]', fontsize=9)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(fontsize=8)
        
        canvas.draw()
        lbl_result.config(text=f"✅ Success!\nMax: {max(final_T):.1f} K | Min: {min(final_T):.1f} K", fg="green")
        
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Setup Desktop GUI Window
root = tk.Tk()
root.title("Multilayer Thermal Solver - Outer to Inner Stack")
root.geometry("900x600")

# Left Sidebar for Parameters & Material Selection
frame_left = tk.Frame(root, width=300, padx=10, pady=10)
frame_left.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(frame_left, text="Simulation Settings", font=("Arial", 10, "bold")).pack(anchor="w", pady=2)

# Global inputs
tk.Label(frame_left, text="Total Time [s]:").pack(anchor="w")
entry_t_final = tk.Entry(frame_left); entry_t_final.insert(0, "20"); entry_t_final.pack(fill=tk.X)

tk.Label(frame_left, text="Time Step (dt):").pack(anchor="w")
entry_dt = tk.Entry(frame_left); entry_dt.insert(0, "0.05"); entry_dt.pack(fill=tk.X)

tk.Label(frame_left, text="Hot Temp [K]:").pack(anchor="w")
entry_hot = tk.Entry(frame_left); entry_hot.insert(0, "400"); entry_hot.pack(fill=tk.X)

tk.Label(frame_left, text="Cold Temp [K]:").pack(anchor="w")
entry_cold = tk.Entry(frame_left); entry_cold.insert(0, "300"); entry_cold.pack(fill=tk.X)

tk.ttk = ttk
tk.Label(frame_left, text="\n--- Material Stack (Outer to Inner) ---", font=("Arial", 10, "bold")).pack(anchor="w")

# Layer 1 (Outer)
tk.Label(frame_left, text="Layer 1 (Outer):").pack(anchor="w")
combo_layer1 = ttk.Combobox(frame_left, values=list(MATERIAL_DB.keys()), state="readonly")
combo_layer1.set("Aluminum (6061)")
combo_layer1.pack(fill=tk.X)
entry_thick1 = tk.Entry(frame_left); entry_thick1.insert(0, "0.01"); entry_thick1.pack(fill=tk.X)

# Layer 2 (Middle)
tk.Label(frame_left, text="Layer 2 (Middle/TIM):").pack(anchor="w")
combo_layer2 = ttk.Combobox(frame_left, values=list(MATERIAL_DB.keys()), state="readonly")
combo_layer2.set("Thermal Interface Material (TIM)")
combo_layer2.pack(fill=tk.X)
entry_thick2 = tk.Entry(frame_left); entry_thick2.insert(0, "0.002"); entry_thick2.pack(fill=tk.X)

# Layer 3 (Inner)
tk.Label(frame_left, text="Layer 3 (Inner):").pack(anchor="w")
combo_layer3 = ttk.Combobox(frame_left, values=list(MATERIAL_DB.keys()), state="readonly")
combo_layer3.set("Stainless Steel")
combo_layer3.pack(fill=tk.X)
entry_thick3 = tk.Entry(frame_left); entry_thick3.insert(0, "0.015"); entry_thick3.pack(fill=tk.X)

tk.Button(frame_left, text="Run Simulation & Plot", command=run_simulation, bg="#1f77b4", fg="white", font=("Arial", 10, "bold")).pack(pady=10, fill=tk.X)

lbl_result = tk.Label(frame_left, text="Status: Ready", font=("Arial", 9), fg="blue", justify=tk.LEFT)
lbl_result.pack(pady=2)

# Right Area for Matplotlib Graph
frame_right = tk.Frame(root)
frame_right.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

fig, ax = plt.subplots(figsize=(6, 5))
canvas = FigureCanvasTkAgg(fig, master=frame_right)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root.mainloop()