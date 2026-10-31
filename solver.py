import numpy as np
import scipy.sparse as sp

def solve_transient_thermal(layers, R_contacts, t_final, dt, T_hot, T_cold):
    total_nodes = sum(l['nodes'] for l in layers)
    num_steps = int(t_final / dt)
    
    # Global mesh generation & coordinate tracking
    x_vec = np.zeros(total_nodes)
    curr_x = 0
    idx_tracker = 0
    for m, l in enumerate(layers):
        N = l['nodes']
        dx = l['thickness'] / (N - 1)
        for i in range(N):
            x_vec[idx_tracker] = curr_x
            curr_x += dx
            idx_tracker += 1
        if m < len(layers) - 1:
            curr_x -= dx  # Account for interface touching point
            
    # Initial conditions
    T = T_cold * np.ones(total_nodes)
    T[0] = T_hot
    
    history = [T.copy()]
    time_axis = [0.0]
    
    # Time-stepping loop
    for step in range(1, num_steps + 1):
        A, b_vec = assemble_system(layers, R_contacts, dt, T, T_hot, T_cold, total_nodes)
        T = sp.linalg.spsolve(A, b_vec)
        
        if step % 5 == 0 or step == num_steps:
            history.append(T.copy())
            time_axis.append(step * dt)
            
    return x_vec, time_axis, history


def assemble_system(layers, R_contacts, dt, T_prev, T_hot, T_cold, total_nodes):
    ii, jj, s = [], [], []
    b_vec = np.zeros(total_nodes)
    
    global_idx = 0
    interface_counter = 0
    
    for m, l in enumerate(layers):
        N = l['nodes']
        dx = l['thickness'] / (N - 1)
        k, rho, cp = l['k'], l['rho'], l['cp']
        alpha = (k * dt) / (rho * cp * dx**2)
        
        for i in range(N):
            row = global_idx + i
            
            if row == 0:
                # Left Dirichlet Boundary Condition
                ii.append(row); jj.append(row); s.append(1.0)
                b_vec[row] = T_hot
            elif row == total_nodes - 1:
                # Right Dirichlet Boundary Condition
                ii.append(row); jj.append(row); s.append(1.0)
                b_vec[row] = T_cold
            elif i == N - 1 and m < len(layers) - 1:
                # Interface Node with Thermal Contact Resistance (R_tc)
                R_tc = R_contacts[interface_counter]
                interface_counter += 1
                
                dx_A = dx
                k_A = k
                cap_term = (rho * cp * dx_A / 2.0) / dt
                
                ii.extend([row, row, row])
                jj.extend([row - 1, row, row + 1])
                s.extend([-k_A / dx_A, cap_term + (k_A / dx_A) + (1.0 / R_tc), -1.0 / R_tc])
                b_vec[row] = cap_term * T_prev[row]
            else:
                # Standard Interior Node
                ii.extend([row, row, row])
                jj.extend([row - 1, row, row + 1])
                s.extend([-alpha, 1.0 + 2.0 * alpha, -alpha])
                b_vec[row] = T_prev[row]
                
        global_idx += N
        
    A = sp.coo_matrix((s, (ii, jj)), shape=(total_nodes, total_nodes)).tocsr()
    return A, b_vec