# casimir_model.py
"""
Build A5 model using Casimir operator eigenvalues
q = a*C(dim) + b*w + c  where C(dim) is Casimir eigenvalue
"""

import numpy as np
from math import log, sqrt
import sqlite3

# Golden ratio
phi = (1 + sqrt(5)) / 2

# A5 Casimir eigenvalues for irreps
# For A5 group, Casimir eigenvalues are proportional to (dim^2 - 1)/12
def casimir_eigenvalue(dim):
    """Calculate Casimir eigenvalue for A5 irrep of given dimension"""
    return (dim**2 - 1) / 12.0

def load_particle_data():
    """Load particle data with q values"""
    conn = sqlite3.connect('particle_physics.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT mass_gev FROM particles WHERE name='electron'")
    m_e = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT name, mass_gev, category 
        FROM particles 
        WHERE mass_gev > 0
        ORDER BY mass_gev
    """)
    
    particles = []
    for name, mass, category in cursor.fetchall():
        n = log(mass/m_e) / log(phi)
        q = 4 * n  # Our fundamental q value
        
        particles.append({
            'name': name,
            'mass': mass,
            'n': n,
            'q': q,
            'category': category
        })
    
    conn.close()
    return particles, m_e

def fit_casimir_model(particles):
    """Fit model: q = a*C(dim) + b*w + c"""
    
    # First, we need to assign dimensions and weights
    # Let's try the best assignments from our previous analysis
    assignments = []
    
    for p in particles:
        name = p['name']
        category = p['category']
        q = p['q']
        
        # Assign based on category and name patterns
        if 'neutrino' in name:
            dim = 1
            w = 0
        elif name == 'electron':
            dim = 3
            w = -1
        elif category == 'quark' and name != 'top_quark':
            dim = 3
            w = int(round(q % 3)) - 1
        elif name in ['muon', 'tau']:
            dim = 4
            w = -3
        elif category == 'boson':
            dim = 4
            w = 3
        elif name == 'top_quark':
            dim = 5
            w = -2
        else:
            dim = 3
            w = 0
        
        C = casimir_eigenvalue(dim)
        assignments.append({
            'name': name,
            'q_actual': q,
            'dim': dim,
            'w': w,
            'C': C
        })
    
    # Fit linear model: q = a*C + b*w + c
    C_vals = np.array([a['C'] for a in assignments])
    w_vals = np.array([a['w'] for a in assignments])
    q_vals = np.array([a['q_actual'] for a in assignments])
    
    X = np.column_stack([C_vals, w_vals, np.ones_like(C_vals)])
    params, residuals, rank, s = np.linalg.lstsq(X, q_vals, rcond=None)
    a, b, c = params
    
    print("CASIMIR MODEL: q = a*C(dim) + b*w + c")
    print(f"Fitted: q = {a:.4f}*C + {b:.4f}*w + {c:.4f}")
    
    # Calculate predictions
    print("\nPredictions:")
    print("Particle        | q_actual | q_pred | Error | Integer match?")
    print("-" * 60)
    
    total_error = 0
    integer_matches = 0
    
    for i, a_data in enumerate(assignments):
        q_pred = a * a_data['C'] + b * a_data['w'] + c
        error = abs(q_pred - a_data['q_actual'])
        total_error += error
        
        # Check if near integer
        q_rounded = round(q_pred)
        if abs(q_pred - q_rounded) < 0.1:
            integer_matches += 1
            int_match = "YES"
        else:
            int_match = "NO"
        
        print(f"{a_data['name']:15s} {a_data['q_actual']:8.1f} {q_pred:7.1f} {error:6.1f} {int_match:>12}")
    
    avg_error = total_error / len(assignments)
    match_percent = 100 * integer_matches / len(assignments)
    
    print(f"\nAverage error: {avg_error:.2f}")
    print(f"Integer matches: {integer_matches}/{len(assignments)} ({match_percent:.1f}%)")
    
    return a, b, c, assignments, avg_error

def main():
    print("A5 CASIMIR OPERATOR MODEL")
    print("=" * 60)
    print("Model: q = a*C(dim) + b*w + c")
    print("where C(dim) = (dim^2 - 1)/12 (Casimir eigenvalue)")
    print("=" * 60)
    
    particles, m_e = load_particle_data()
    print(f"Loaded {len(particles)} particles")
    
    a, b, c, assignments, avg_error = fit_casimir_model(particles)
    
    # Show Casimir eigenvalues
    print("\n" + "=" * 60)
    print("A5 CASIMIR EIGENVALUES:")
    print("Dimension | Casimir eigenvalue C(dim)")
    print("-" * 40)
    for dim in [1, 3, 4, 5]:
        C = casimir_eigenvalue(dim)
        print(f"{dim:9d} {C:15.4f}")
    
    # Test if q values become more integer-like
    print("\n" + "=" * 60)
    print("TESTING INTEGER HYPOTHESIS:")
    print("If our model is correct, q_pred should be near integers")
    
    q_preds = []
    for a_data in assignments:
        q_pred = a * a_data['C'] + b * a_data['w'] + c
        q_preds.append(q_pred)
    
    deviations = [abs(q - round(q)) for q in q_preds]
    avg_deviation = np.mean(deviations)
    
    print(f"Average deviation from integers: {avg_deviation:.4f}")
    if avg_deviation < 0.05:
        print("SUCCESS: q values are near integers!")
    else:
        print("Note: q values not very integer-like")
    
    return a, b, c, assignments

if __name__ == "__main__":
    main()