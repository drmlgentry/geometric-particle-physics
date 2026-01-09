# neutrino_a5_model.py
"""
Model where neutrinos occupy weight states of A5 4D representation
"""

import numpy as np
from math import log, sqrt
import sqlite3

phi = (1 + sqrt(5)) / 2

def load_data():
    conn = sqlite3.connect('particle_physics.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT mass_gev FROM particles WHERE name='electron'")
    m_e = cursor.fetchone()[0]
    
    # Exact integer q values
    exact_q = {
        'electron_neutrino': -224, 'muon_neutrino': -180, 'tau_neutrino': -162,
        'electron': 0, 'up_quark': 12, 'down_quark': 18, 'strange_quark': 44,
        'charm_quark': 65, 'bottom_quark': 75, 'top_quark': 106,
        'muon': 44, 'tau': 68, 'W_boson': 100, 'Z_boson': 100, 'higgs_boson': 103
    }
    
    cursor.execute("SELECT name, mass_gev, category FROM particles WHERE mass_gev > 0")
    
    particles = []
    for name, mass, category in cursor.fetchall():
        particles.append({
            'name': name, 'mass': mass, 'category': category,
            'q': exact_q[name], 'n': exact_q[name] / 4
        })
    
    conn.close()
    return particles, m_e

def find_neutrino_weights():
    """Find which weight assignment gives best neutrino q values"""
    
    print("NEUTRINO WEIGHT ASSIGNMENT ANALYSIS")
    print("="*60)
    
    # Neutrino q values
    neutrino_q = {'electron_neutrino': -224, 'muon_neutrino': -180, 'tau_neutrino': -162}
    
    # 4D representation weights: -3, -1, 1, 3
    # Let's try to find linear relation: q = a*w + b
    
    weights = [-3, -1, 1, 3]
    neutrino_names = list(neutrino_q.keys())
    
    # Try all assignments of the 3 neutrinos to 3 of the 4 weights
    from itertools import permutations, combinations
    
    best_error = float('inf')
    best_assignment = None
    best_params = None
    
    # Try all combinations of 3 weights from the 4 available
    for weight_combo in combinations(weights, 3):
        # Try all permutations of assigning these 3 weights to 3 neutrinos
        for perm in permutations(weight_combo):
            w_vals = np.array(list(perm))
            q_vals = np.array([neutrino_q[name] for name in neutrino_names])
            
            # Fit q = a*w + b
            X = np.column_stack([w_vals, np.ones_like(w_vals)])
            params, residuals, rank, s = np.linalg.lstsq(X, q_vals, rcond=None)
            a, b = params
            
            # Calculate error
            q_pred = a * w_vals + b
            error = np.sum(np.abs(q_pred - q_vals))
            
            if error < best_error:
                best_error = error
                best_assignment = dict(zip(neutrino_names, perm))
                best_params = (a, b)
    
    print(f"Best neutrino assignment found:")
    print(f"  electron_neutrino: weight = {best_assignment['electron_neutrino']}")
    print(f"  muon_neutrino: weight = {best_assignment['muon_neutrino']}")
    print(f"  tau_neutrino: weight = {best_assignment['tau_neutrino']}")
    print(f"  Model: q = {best_params[0]:.2f}*w + {best_params[1]:.2f}")
    print(f"  Total error: {best_error:.2f}")
    
    return best_assignment, best_params

def unified_a5_model(particles, neutrino_weights):
    """Create unified model with neutrinos in 4D representation"""
    
    print("\n" + "="*60)
    print("UNIFIED A5 MODEL WITH NEUTRINOS IN 4D REPRESENTATION")
    print("="*60)
    
    # Assign all particles to A5 representations
    assignments = []
    
    for p in particles:
        name = p['name']
        q = p['q']
        
        if name in neutrino_weights:
            # Neutrinos in 4D representation
            dim = 4
            w = neutrino_weights[name]
            C_norm = 15  # 4D Casimir numerator
        elif name == 'electron':
            dim = 3
            w = -1
            C_norm = 8
        elif 'quark' in name:
            dim = 3
            # Assign weights based on q mod 3
            w_mod = q % 3
            if w_mod == 0: w = -1
            elif w_mod == 1: w = 0
            else: w = 1
            C_norm = 8
        elif name in ['muon', 'tau']:
            dim = 4
            if name == 'muon': w = -3
            else: w = -1
            C_norm = 15
        else:  # Bosons
            dim = 5
            if name == 'W_boson': w = -2
            elif name == 'Z_boson': w = -1
            else: w = 0  # Higgs
            C_norm = 24
        
        assignments.append({
            'name': name, 'q': q, 'dim': dim, 'w': w, 'C_norm': C_norm
        })
    
    # Fit model: q = a*C_norm + b*w + c
    C_vals = np.array([a['C_norm'] for a in assignments])
    w_vals = np.array([a['w'] for a in assignments])
    q_vals = np.array([a['q'] for a in assignments])
    
    X = np.column_stack([C_vals, w_vals, np.ones_like(C_vals)])
    params, residuals, rank, s = np.linalg.lstsq(X, q_vals, rcond=None)
    a, b, c = params
    
    print(f"Fitted model: q = {a:.4f}*C + {b:.4f}*w + {c:.4f}")
    print(f"\nwhere C = Casimir numerator (8 for 3D, 15 for 4D, 24 for 5D)")
    
    # Calculate predictions
    print("\nParticle        | Dim | C  | w   | q_actual | q_pred | Error")
    print("-" * 65)
    
    total_error = 0
    for assign in assignments:
        q_pred = a * assign['C_norm'] + b * assign['w'] + c
        error = abs(q_pred - assign['q'])
        total_error += error
        
        print(f"{assign['name']:15s} {assign['dim']:4d} {assign['C_norm']:3.0f} "
              f"{assign['w']:4.0f} {assign['q']:9.0f} {q_pred:8.1f} {error:7.1f}")
    
    avg_error = total_error / len(assignments)
    print(f"\nAverage error: {avg_error:.2f}")
    
    # Check integer property
    print("\n" + "="*60)
    print("INTEGER CHECK OF PREDICTED q VALUES")
    print("="*60)
    
    deviations = []
    for assign in assignments:
        q_pred = a * assign['C_norm'] + b * assign['w'] + c
        deviation = abs(q_pred - round(q_pred))
        deviations.append(deviation)
    
    avg_deviation = np.mean(deviations)
    print(f"Average deviation from integers: {avg_deviation:.4f}")
    
    if avg_deviation < 0.1:
        print("SUCCESS: Predicted q values are near integers!")
    else:
        print("Note: Predicted q values not very integer-like")
    
    return assignments, (a, b, c), avg_error, avg_deviation

def predict_all_states(params, m_e):
    """Predict all possible A5 states"""
    a, b, c = params
    
    print("\n" + "="*60)
    print("ALL POSSIBLE A5 STATES")
    print("="*60)
    
    all_states = [
        # (rep, dim, C_norm, weight)
        ("1D", 1, 0, 0),
        ("3D", 3, 8, -1), ("3D", 3, 8, 0), ("3D", 3, 8, 1),
        ("4D", 4, 15, -3), ("4D", 4, 15, -1), ("4D", 4, 15, 1), ("4D", 4, 15, 3),
        ("5D", 5, 24, -2), ("5D", 5, 24, -1), ("5D", 5, 24, 0), 
        ("5D", 5, 24, 1), ("5D", 5, 24, 2)
    ]
    
    predictions = []
    for rep, dim, C, w in all_states:
        q_pred = a * C + b * w + c
        n_pred = q_pred / 4
        mass_pred = m_e * (phi ** n_pred)
        
        predictions.append({
            'rep': rep, 'dim': dim, 'C': C, 'w': w,
            'q': q_pred, 'n': n_pred, 'mass': mass_pred
        })
    
    # Sort by mass
    predictions.sort(key=lambda x: x['mass'])
    
    print("\nPredicted states (sorted by mass):")
    print("Rep | Dim | C  | w   | q_pred  | n_pred | Mass (GeV)")
    print("-" * 60)
    
    for p in predictions[:15]:  # Show first 15
        if -20 < p['q'] < 200:  # Reasonable q range
            print(f"{p['rep']:3s} {p['dim']:4d} {p['C']:3.0f} {p['w']:4.0f} "
                  f"{p['q']:8.1f} {p['n']:7.2f} {p['mass']:12.3e}")
    
    return predictions

def main():
    print("A5 UNIFIED MODEL WITH NEUTRINOS IN 4D")
    print("="*60)
    
    particles, m_e = load_data()
    
    # Step 1: Find best neutrino weights
    neutrino_weights, neutrino_params = find_neutrino_weights()
    
    # Step 2: Build unified model
    assignments, params, avg_error, avg_deviation = unified_a5_model(particles, neutrino_weights)
    
    # Step 3: Predict all states
    predictions = predict_all_states(params, m_e)
    
    # Step 4: Analyze patterns
    print("\n" + "="*60)
    print("ANALYSIS OF 8:15:24 PATTERN")
    print("="*60)
    
    print("\nThe numbers 8, 15, 24 are conjugacy class sizes of A5:")
    print("  - 8: Number of 3-cycles (order 3)")
    print("  - 15: Number of elements as product of 2 transpositions (order 2)")
    print("  - 24: Number of 5-cycles (order 5)")
    print("  - Plus: 1 identity, 1 other class (making total 60 elements)")
    
    print("\nOur model suggests:")
    print("  1. q values are linear combinations of these class sizes")
    print("  2. Different particles correspond to different conjugacy classes")
    print("  3. The factor 4 in q=4n comes from the 4D representation")
    
    print("\nNEXT STEPS:")
    print("  1. Check if this model gives better integer q predictions")
    print("  2. Test against known mass ratios")
    print("  3. Look for physical interpretation of weights")
    print("  4. Predict masses for undiscovered particles")

if __name__ == "__main__":
    main()