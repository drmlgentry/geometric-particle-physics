# a5_casimir_ratio.py
"""
A5 model using the 8:15:24 Casimir eigenvalue pattern
q = a*(C_normalized) + b*w + c where C_normalized takes values 8, 15, 24
"""

import numpy as np
from math import log, sqrt
import sqlite3

phi = (1 + sqrt(5)) / 2

def casimir_normalized(dim):
    """Return normalized Casimir values: 8, 15, 24 for dim 3,4,5"""
    if dim == 1:
        return 0
    elif dim == 3:
        return 8
    elif dim == 4:
        return 15
    elif dim == 5:
        return 24
    else:
        return dim**2 - 1  # fallback

def load_data_with_exact_q():
    """Load data with exact integer q values (from previous analysis)"""
    conn = sqlite3.connect('particle_physics.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT mass_gev FROM particles WHERE name='electron'")
    m_e = cursor.fetchone()[0]
    
    # Known exact integer q values from our previous analysis
    exact_q_values = {
        'electron': 0,
        'electron_neutrino': -224,
        'muon_neutrino': -180,
        'tau_neutrino': -162,
        'up_quark': 12,
        'down_quark': 18,
        'strange_quark': 44,
        'charm_quark': 65,
        'bottom_quark': 75,
        'top_quark': 106,
        'muon': 44,
        'tau': 68,
        'W_boson': 100,
        'Z_boson': 100,
        'higgs_boson': 103
    }
    
    cursor.execute("""
        SELECT name, mass_gev, category, spin_half 
        FROM particles 
        WHERE mass_gev > 0
        ORDER BY mass_gev
    """)
    
    particles = []
    for name, mass, category, spin in cursor.fetchall():
        n = log(mass/m_e) / log(phi)
        q = exact_q_values.get(name, round(4 * n))
        
        particles.append({
            'name': name,
            'mass': mass,
            'n': n,
            'q': q,
            'category': category,
            'spin': spin * 0.5 if spin else 0
        })
    
    conn.close()
    return particles, m_e

def find_best_assignments(particles):
    """Find the best representation assignments using 8:15:24 pattern"""
    
    print("\n" + "="*60)
    print("FINDING BEST A5 ASSIGNMENTS WITH CASIMIR 8:15:24 PATTERN")
    print("="*60)
    
    # All possible (dim, C_norm, weight) combinations
    possibilities = [
        (1, 0, 0),           # Trivial
        (3, 8, -1), (3, 8, 0), (3, 8, 1),      # 3D rep
        (4, 15, -3), (4, 15, -1), (4, 15, 1), (4, 15, 3),  # 4D rep
        (5, 24, -2), (5, 24, -1), (5, 24, 0), (5, 24, 1), (5, 24, 2)  # 5D rep
    ]
    
    # Try to find a simple linear relationship: q = a*C + b*w
    # We'll use least squares on all possible assignments
    
    best_error = float('inf')
    best_assignments = None
    best_params = None
    
    # For simplicity, let's start with educated guesses
    # Based on the ratio 8:15:24, and q values around 0-100
    # Let a = q/C ≈ 100/24 ≈ 4.1667
    
    print("\nTrying simple model: q = a*C + b*w")
    
    # Group particles by type for assignment
    assignments = []
    
    # Neutrinos: trivial representation
    for p in particles:
        if 'neutrino' in p['name']:
            assignments.append({'name': p['name'], 'q': p['q'], 'C': 0, 'w': 0, 'dim': 1})
    
    # Electron: try 3D representation
    for p in particles:
        if p['name'] == 'electron':
            assignments.append({'name': p['name'], 'q': p['q'], 'C': 8, 'w': -1, 'dim': 3})
    
    # Quarks: 3D representation with different weights
    quark_weights = {'up_quark': -1, 'down_quark': 0, 'strange_quark': 1, 
                     'charm_quark': -1, 'bottom_quark': 0, 'top_quark': 1}
    for p in particles:
        if 'quark' in p['name'] and p['name'] in quark_weights:
            assignments.append({'name': p['name'], 'q': p['q'], 'C': 8, 
                              'w': quark_weights[p['name']], 'dim': 3})
    
    # Charged leptons: 4D representation
    lepton_weights = {'muon': -3, 'tau': -1}
    for p in particles:
        if p['name'] in lepton_weights:
            assignments.append({'name': p['name'], 'q': p['q'], 'C': 15, 
                              'w': lepton_weights[p['name']], 'dim': 4})
    
    # Bosons: 5D representation
    boson_weights = {'W_boson': -2, 'Z_boson': -1, 'higgs_boson': 0}
    for p in particles:
        if p['name'] in boson_weights:
            assignments.append({'name': p['name'], 'q': p['q'], 'C': 24, 
                              'w': boson_weights[p['name']], 'dim': 5})
    
    # Fit model: q = a*C + b*w
    C_vals = np.array([a['C'] for a in assignments])
    w_vals = np.array([a['w'] for a in assignments])
    q_vals = np.array([a['q'] for a in assignments])
    
    X = np.column_stack([C_vals, w_vals])
    params, residuals, rank, s = np.linalg.lstsq(X, q_vals, rcond=None)
    a, b = params
    
    print(f"Fitted: q = {a:.4f}*C + {b:.4f}*w")
    
    # Calculate predictions
    print("\nPredictions with this assignment:")
    print("Particle        | Dim | C   | w   | q_actual | q_pred | Error")
    print("-" * 65)
    
    total_error = 0
    for assign in assignments:
        q_pred = a * assign['C'] + b * assign['w']
        error = abs(q_pred - assign['q'])
        total_error += error
        
        print(f"{assign['name']:15s} {assign['dim']:4d} {assign['C']:4.0f} {assign['w']:4.0f} "
              f"{assign['q']:9.0f} {q_pred:8.1f} {error:7.1f}")
    
    avg_error = total_error / len(assignments)
    print(f"\nAverage error: {avg_error:.2f}")
    
    # Try alternative: q = a*C + b*w + c*(spin)
    print("\n" + "="*60)
    print("TRYING WITH SPIN: q = a*C + b*w + c*spin")
    print("="*60)
    
    # Add spin to assignments
    for assign in assignments:
        for p in particles:
            if p['name'] == assign['name']:
                assign['spin'] = p['spin']
                break
    
    spin_vals = np.array([a['spin'] for a in assignments])
    X2 = np.column_stack([C_vals, w_vals, spin_vals])
    params2, residuals2, rank2, s2 = np.linalg.lstsq(X2, q_vals, rcond=None)
    a2, b2, c2 = params2
    
    print(f"Fitted: q = {a2:.4f}*C + {b2:.4f}*w + {c2:.4f}*spin")
    
    # Show predictions
    print("\nParticle        | q_actual | q_pred  | Error")
    print("-" * 45)
    
    total_error2 = 0
    for i, assign in enumerate(assignments):
        q_pred2 = a2 * assign['C'] + b2 * assign['w'] + c2 * assign['spin']
        error2 = abs(q_pred2 - assign['q'])
        total_error2 += error2
        
        print(f"{assign['name']:15s} {assign['q']:9.0f} {q_pred2:8.1f} {error2:7.1f}")
    
    avg_error2 = total_error2 / len(assignments)
    print(f"\nAverage error with spin: {avg_error2:.2f}")
    
    return assignments, (a, b), (a2, b2, c2), avg_error, avg_error2

def check_integer_property(assignments, params):
    """Check if predicted q values are near integers"""
    a, b = params
    
    print("\n" + "="*60)
    print("CHECKING INTEGER PROPERTY OF q")
    print("="*60)
    
    print("\nFor each particle, predicted q should be integer:")
    print("Particle        | q_pred  | Nearest int | Difference")
    print("-" * 55)
    
    differences = []
    for assign in assignments:
        q_pred = a * assign['C'] + b * assign['w']
        nearest_int = round(q_pred)
        diff = abs(q_pred - nearest_int)
        differences.append(diff)
        
        print(f"{assign['name']:15s} {q_pred:8.2f} {nearest_int:11.0f} {diff:11.3f}")
    
    avg_diff = np.mean(differences)
    max_diff = np.max(differences)
    
    print(f"\nAverage difference from integer: {avg_diff:.4f}")
    print(f"Maximum difference: {max_diff:.4f}")
    
    if avg_diff < 0.1:
        print("SUCCESS: q values are very close to integers!")
    else:
        print("Note: Some q values are not very integer-like")

def explore_8_15_24_multiples():
    """Explore the significance of 8, 15, 24 numbers"""
    
    print("\n" + "="*60)
    print("EXPLORING THE 8:15:24 RATIO")
    print("="*60)
    
    print("\nThese numbers appear in A5 group theory:")
    print("8:  Number of 3-cycles in A5")
    print("15: Number of elements of order 2 in A5 (products of two transpositions)")
    print("24: Number of 5-cycles in A5")
    
    print("\nAlso note: 8 + 15 + 24 = 47")
    print("And 47 is prime!")
    
    print("\nConnection to our q values:")
    print("- The q values we found: -224, -180, -162, 0, 12, 18, 44, 65, 75, 106, etc.")
    
    # Check if q values are multiples of these numbers
    q_samples = [-224, -180, -162, 0, 12, 18, 44, 65, 75, 106, 100, 103]
    
    print("\nChecking divisibility by 8, 15, 24:")
    print("q value | ÷8 | ÷15 | ÷24")
    print("-" * 30)
    
    for q in q_samples:
        if q == 0:
            print(f"{q:7d} | -  | -   | -")
        else:
            div8 = q / 8
            div15 = q / 15
            div24 = q / 24
            print(f"{q:7d} | {div8:4.2f} | {div15:5.2f} | {div24:5.2f}")

def main():
    print("A5 CASIMIR 8:15:24 MODEL")
    print("="*60)
    print("Using Casimir eigenvalue pattern 8:15:24 for A5 representations")
    print("="*60)
    
    particles, m_e = load_data_with_exact_q()
    print(f"Loaded {len(particles)} particles with exact integer q values")
    
    # Find best assignments
    assignments, params1, params2, error1, error2 = find_best_assignments(particles)
    
    # Check integer property
    check_integer_property(assignments, params1)
    
    # Explore the 8:15:24 significance
    explore_8_15_24_multiples()
    
    # Make predictions for all A5 states
    print("\n" + "="*60)
    print("PREDICTING ALL A5 STATES")
    print("="*60)
    
    a, b = params1
    print(f"\nUsing model: q = {a:.4f}*C + {b:.4f}*w")
    
    all_states = [
        ("1D", 1, 0, 0),
        ("3D", 3, 8, -1), ("3D", 3, 8, 0), ("3D", 3, 8, 1),
        ("4D", 4, 15, -3), ("4D", 4, 15, -1), ("4D", 4, 15, 1), ("4D", 4, 15, 3),
        ("5D", 5, 24, -2), ("5D", 5, 24, -1), ("5D", 5, 24, 0), ("5D", 5, 24, 1), ("5D", 5, 24, 2)
    ]
    
    predictions = []
    for rep, dim, C, w in all_states:
        q_pred = a * C + b * w
        n_pred = q_pred / 4
        mass_pred = m_e * (phi ** n_pred)
        
        predictions.append({
            'rep': rep,
            'dim': dim,
            'C': C,
            'w': w,
            'q': q_pred,
            'n': n_pred,
            'mass': mass_pred
        })
    
    # Sort by mass
    predictions.sort(key=lambda x: x['mass'])
    
    print("\nPredicted masses for all A5 states:")
    print("Rep | Dim | C  | w   | q_pred  | Mass (GeV)")
    print("-" * 50)
    
    for p in predictions:
        if 1e-20 < p['mass'] < 1e20:
            print(f"{p['rep']:3s} {p['dim']:4d} {p['C']:3.0f} {p['w']:4.0f} {p['q']:8.1f} {p['mass']:12.3e}")

if __name__ == "__main__":
    main()