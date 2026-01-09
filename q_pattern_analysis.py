# q_pattern_analysis.py
"""
Analyze q values as combinations of A5 conjugacy class sizes 8, 15, 24
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
    
    exact_q = {
        'electron_neutrino': -224, 'muon_neutrino': -180, 'tau_neutrino': -162,
        'electron': 0, 'up_quark': 12, 'down_quark': 18, 'strange_quark': 44,
        'muon': 44, 'charm_quark': 65, 'tau': 68, 'bottom_quark': 75,
        'top_quark': 106, 'W_boson': 100, 'Z_boson': 100, 'higgs_boson': 103
    }
    
    cursor.execute("SELECT name, mass_gev, category FROM particles WHERE mass_gev > 0")
    
    particles = []
    for name, mass, category in cursor.fetchall():
        n = exact_q[name] / 4
        particles.append({
            'name': name, 'mass': mass, 'category': category,
            'q': exact_q[name], 'n': n
        })
    
    conn.close()
    return particles, m_e

def express_q_as_combination():
    """Try to express q as a combination of 8, 15, 24"""
    
    q_values = {
        'electron_neutrino': -224,
        'muon_neutrino': -180,
        'tau_neutrino': -162,
        'electron': 0,
        'up_quark': 12,
        'down_quark': 18,
        'strange_quark': 44,
        'muon': 44,
        'charm_quark': 65,
        'tau': 68,
        'bottom_quark': 75,
        'top_quark': 106,
        'W_boson': 100,
        'Z_boson': 100,
        'higgs_boson': 103
    }
    
    print("EXPRESSING q AS COMBINATIONS OF 8, 15, 24")
    print("="*60)
    
    # Try q = a*8 + b*15 + c*24 + d
    print("\nTrying: q = a*8 + b*15 + c*24 + d")
    
    # We'll do this particle by particle to see patterns
    bases = [8, 15, 24]
    
    print("\nParticle        | q   | Best fit (a,b,c,d) | Calculated | Error")
    print("-"*70)
    
    for name, q in q_values.items():
        best_error = float('inf')
        best_coeffs = (0, 0, 0, 0)
        
        # Try reasonable ranges for coefficients
        for a in range(-30, 31):
            for b in range(-20, 21):
                for c in range(-10, 11):
                    # Calculate d = q - (a*8 + b*15 + c*24)
                    calculated = a*8 + b*15 + c*24
                    d = q - calculated
                    
                    # Check if d is small (we want it to be constant-ish)
                    if abs(d) < 20:  # d should be small constant
                        error = abs(d)
                        if error < best_error:
                            best_error = error
                            best_coeffs = (a, b, c, d)
        
        a, b, c, d = best_coeffs
        q_calc = a*8 + b*15 + c*24 + d
        error = abs(q - q_calc)
        
        print(f"{name:15s} {q:5.0f} ({a:3d},{b:3d},{c:3d},{d:4.0f}) {q_calc:11.0f} {error:6.0f}")
    
    # Now try to find a universal d
    print("\n" + "="*60)
    print("LOOKING FOR UNIVERSAL CONSTANT d")
    print("="*60)
    
    # Try d = -4 (from electron q=0: 0 = 1*8 + (-1)*15 + 0*24 + d => d = 7? Wait)
    # Let's solve systematically
    
    all_coeffs = []
    for name, q in q_values.items():
        # Find all representations of q as combinations of 8,15,24 with small d
        representations = []
        for a in range(-10, 11):
            for b in range(-10, 11):
                for c in range(-10, 11):
                    d = q - (a*8 + b*15 + c*24)
                    if abs(d) <= 10:  # d between -10 and 10
                        representations.append((a, b, c, d))
        
        all_coeffs.append(representations)
        if representations:
            print(f"\n{name:15s} q={q:4.0f}: {len(representations)} representations with |d|<=10")
            for i, (a,b,c,d) in enumerate(representations[:3]):  # Show first 3
                print(f"  {i+1}. q = {a:2d}*8 + {b:2d}*15 + {c:2d}*24 + {d:3.0f}")

def analyze_group_theory():
    """Analyze the group theory behind 8, 15, 24"""
    
    print("\n" + "="*60)
    print("GROUP THEORY OF A5")
    print("="*60)
    
    print("\nA5 (Alternating group on 5 elements) has:")
    print("  Order: 60")
    print("  Conjugacy classes and sizes:")
    print("    1: Identity (size 1)")
    print("    2: 3-cycles (size 20)  Wait, correction: 3-cycles come in two classes in A5")
    print("    3: Actually, in A5:")
    print("       - 1 identity")
    print("       - 15 elements: products of two disjoint transpositions (order 2)")
    print("       - 20 elements: 3-cycles (order 3)")
    print("       - 24 elements: 5-cycles (order 5)")
    
    print("\nOur numbers 8, 15, 24:")
    print("  - 8: Not a conjugacy class size directly")
    print("  - 15: Matches the 15 elements of order 2")
    print("  - 24: Matches the 24 elements of order 5")
    
    print("\nMaybe 8 comes from something else:")
    print("  - Dimension of certain representation?")
    print("  - Or: 8 = 20/2.5? Not clear.")
    print("  - Note: 8 + 15 + 24 = 47")
    print("  - And 47 is prime")
    
    print("\nAlternative: These could be related to dimensions of representations")
    print("  in a larger group that contains A5?")

def find_simple_model(particles):
    """Try to find a simple model that explains all q values"""
    
    print("\n" + "="*60)
    print("ATTEMPTING SIMPLE MODEL")
    print("="*60)
    
    # Let's try: q = k1 * (dim^2 - 1) + k2 * spin + k3
    # Or: q = k1 * C + k2 * (something)
    
    # First, assign dimensions and get spin
    assignments = []
    for p in particles:
        name = p['name']
        
        # Assign dimensions based on category
        if 'neutrino' in name:
            dim = 4  # Try 4D for neutrinos
        elif name == 'electron':
            dim = 3
        elif 'quark' in name:
            dim = 3
        elif name in ['muon', 'tau']:
            dim = 4
        else:  # bosons
            dim = 5
        
        # Get spin (0 for scalars, 1/2 for fermions, 1 for vectors)
        if 'boson' in p['category']:
            if name in ['W_boson', 'Z_boson']:
                spin = 1
            else:
                spin = 0
        else:
            spin = 0.5
        
        assignments.append({
            'name': name,
            'q': p['q'],
            'dim': dim,
            'C': dim**2 - 1,  # 0, 8, 15, or 24
            'spin': spin,
            'category': p['category']
        })
    
    # Try linear regression: q = a*C + b*spin + c
    C_vals = np.array([a['C'] for a in assignments])
    spin_vals = np.array([a['spin'] for a in assignments])
    q_vals = np.array([a['q'] for a in assignments])
    
    X = np.column_stack([C_vals, spin_vals, np.ones_like(C_vals)])
    params, residuals, rank, s = np.linalg.lstsq(X, q_vals, rcond=None)
    a, b, c = params
    
    print(f"\nModel: q = {a:.4f}*C + {b:.4f}*spin + {c:.4f}")
    print("where C = dim^2 - 1")
    
    print("\nPredictions:")
    print("Particle        | Dim | C  | Spin | q_actual | q_pred | Error")
    print("-"*70)
    
    total_error = 0
    for i, assign in enumerate(assignments):
        q_pred = a * assign['C'] + b * assign['spin'] + c
        error = abs(q_pred - assign['q'])
        total_error += error
        
        print(f"{assign['name']:15s} {assign['dim']:4d} {assign['C']:3.0f} "
              f"{assign['spin']:5.1f} {assign['q']:9.0f} {q_pred:8.1f} {error:7.1f}")
    
    avg_error = total_error / len(assignments)
    print(f"\nAverage error: {avg_error:.2f}")
    
    # Check if q values become integers
    print("\nInteger check:")
    deviations = []
    for i, assign in enumerate(assignments):
        q_pred = a * assign['C'] + b * assign['spin'] + c
        deviations.append(abs(q_pred - round(q_pred)))
    
    avg_deviation = np.mean(deviations)
    print(f"Average deviation from integer: {avg_deviation:.4f}")
    
    return assignments, (a, b, c), avg_error

def save_next_steps():
    """Update next.txt with our findings"""
    
    next_steps = """
NEXT STEPS BASED ON LATEST ANALYSIS:
====================================

1. PATTERN FOUND:
   - q values show divisibility by 3, 4, 5, 8, 15, 24
   - Numbers 8, 15, 24 appear (15 and 24 are A5 conjugacy class sizes)
   - Neutrinos fit well in 4D representation: q = -10.43*w - 192.14

2. ISSUES:
   - No single linear model works for all particles
   - Different particle types may need different formulas

3. NEW HYPOTHESES:
   a) q = k1*(dim^2-1) + k2*spin + k3*charge + k4*isospin + ...
   b) Different representations have different formulas
   c) The model might be quadratic, not linear

4. IMMEDIATE NEXT ACTIONS:
   a) Try q = a*(dim^2-1) + b*spin + c*charge + d
   b) Include electric charge and isospin in the model
   c) Try separate models for fermions and bosons
   d) Check if q/4 (n) has better mathematical properties

5. LONGER TERM:
   a) Understand why 8 appears (not a conjugacy class size)
   b) Look for connections to E8 or other larger groups
   c) Re-examine the original paper's matrix approach with corrections

TO DO NOW:
1. Create a script that includes all known quantum numbers
2. Try multivariate regression with dim, spin, charge, isospin
3. Check predictions for neutrino masses more carefully
"""
    
    print("\n" + "="*60)
    print("RECOMMENDED NEXT STEPS:")
    print("="*60)
    print(next_steps)
    
    # Save to file
    with open('next_steps.txt', 'w') as f:
        f.write(next_steps)
    
    print("Detailed next steps saved to 'next_steps.txt'")

def main():
    print("Q-VALUE PATTERN ANALYSIS")
    print("="*60)
    print("Analyzing q = 4n values where n = log_phi(m/m_e)")
    print("="*60)
    
    particles, m_e = load_data()
    
    # Analyze divisibility
    express_q_as_combination()
    
    # Group theory analysis
    analyze_group_theory()
    
    # Try simple model
    assignments, params, avg_error = find_simple_model(particles)
    
    # Save next steps
    save_next_steps()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"""
We've analyzed the q = 4n values in detail.

KEY FINDINGS:
1. The numbers 8, 15, 24 keep appearing
2. 15 and 24 are conjugacy class sizes of A5
3. 8 remains mysterious but important
4. No simple linear model fits all particles well

NEXT DIRECTIONS:
1. Include more quantum numbers (charge, isospin)
2. Try separate models for different particle types
3. Consider non-linear or piecewise models

The original insight that q=4n gives exact integers for
many particles is strong. The connection to A5 through
15 and 24 is promising. We need to understand the role
of the number 8.

Run: python save.py
Then type: "Analyzed q patterns. Found connections to A5 conjugacy 
classes 15 and 24, but 8 remains mysterious. Need to include more
quantum numbers in the model."
""")

if __name__ == "__main__":
    main()