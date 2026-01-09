# model_builder_clean.py
"""
Clean A5 model builder - no unicode characters
Builds model: m = m_e * phi^(alpha*dim + beta*w + gamma)
where phi = golden ratio, dim = A5 representation dimension, w = weight
"""

import numpy as np
from math import log, sqrt
import sqlite3

# Golden ratio
phi = (1 + sqrt(5)) / 2

def load_particle_data():
    """Load particle data from database"""
    conn = sqlite3.connect('particle_physics.db')
    cursor = conn.cursor()
    
    # Get electron mass
    cursor.execute("SELECT mass_gev FROM particles WHERE name='electron'")
    m_e = cursor.fetchone()[0]
    
    # Load all particles with mass > 0
    cursor.execute("""
        SELECT name, mass_gev, category, spin_half 
        FROM particles 
        WHERE mass_gev > 0
        ORDER BY mass_gev
    """)
    
    particles = []
    for name, mass, category, spin_half in cursor.fetchall():
        n = log(mass/m_e) / log(phi)
        n_quantized = round(n * 4) / 4  # Quantized in 0.25 steps
        q = n_quantized * 4  # q = 4n (should be integer)
        
        particles.append({
            'name': name,
            'mass': mass,
            'n': n_quantized,
            'q': q,
            'category': category,
            'spin': spin_half * 0.5 if spin_half else 0
        })
    
    conn.close()
    return particles, m_e

def assign_a5_representations(particles):
    """Assign A5 representations to particles based on patterns"""
    
    print("ASSIGNING A5 REPRESENTATIONS TO PARTICLES")
    print("="*60)
    
    # A5 representation dimensions: 1, 3, 4, 5
    # We'll make educated guesses based on q values and categories
    
    assignments = []
    
    for p in particles:
        q = p['q']
        name = p['name']
        category = p['category']
        
        # Make assignments based on patterns we observed
        if name == 'electron':
            # Electron is special - trivial representation
            dim = 1
            weights = [0]
            w = 0
        elif 'neutrino' in name:
            # Neutrinos - also trivial for now
            dim = 1
            weights = [0]
            w = 0
        elif category == 'quark':
            # Quarks - try 3D representation (like triplets)
            dim = 3
            weights = [-1, 0, 1]
            # Assign weight based on q mod 3
            w = int(q % 3) - 1  # Maps to -1, 0, 1
        elif category == 'lepton' and name != 'electron':
            # Charged leptons - try 4D representation
            dim = 4
            weights = [-3, -1, 1, 3]
            # Assign weight based on q mod 4
            w_mod = int(q % 4)
            if w_mod == 0: w = -3
            elif w_mod == 1: w = -1
            elif w_mod == 2: w = 1
            else: w = 3
        else:
            # Bosons - try 5D representation
            dim = 5
            weights = [-2, -1, 0, 1, 2]
            # Assign weight based on q mod 5
            w_mod = int(q % 5)
            if w_mod == 0: w = -2
            elif w_mod == 1: w = -1
            elif w_mod == 2: w = 0
            elif w_mod == 3: w = 1
            else: w = 2
        
        assignments.append({
            'name': name,
            'dim': dim,
            'w': w,
            'weights': weights,
            'q': q,
            'n': p['n']
        })
    
    # Show assignments
    print("\nParticle        | q   | A5 dim | Weight w")
    print("-"*40)
    for a in assignments:
        print(f"{a['name']:15s} {a['q']:5.0f} {a['dim']:7d} {a['w']:8d}")
    
    return assignments

def fit_model(assignments):
    """Fit model parameters alpha, beta, gamma"""
    
    print("\n" + "="*60)
    print("FITTING MODEL: n = alpha*dim + beta*w + gamma")
    print("="*60)
    
    # Prepare data for linear regression
    dims = np.array([a['dim'] for a in assignments])
    weights = np.array([a['w'] for a in assignments])
    n_values = np.array([a['n'] for a in assignments])
    
    # Design matrix: [dim, w, 1]
    X = np.column_stack([dims, weights, np.ones_like(dims)])
    
    # Solve using least squares
    params, residuals, rank, s = np.linalg.lstsq(X, n_values, rcond=None)
    alpha, beta, gamma = params
    
    print(f"\nFitted parameters:")
    print(f"  alpha = {alpha:.6f} (coefficient for dimension)")
    print(f"  beta  = {beta:.6f} (coefficient for weight)")
    print(f"  gamma = {gamma:.6f} (constant offset)")
    
    print("\nMODEL: n_pred = {:.4f}*dim + {:.4f}*w + {:.4f}".format(alpha, beta, gamma))
    
    # Calculate predictions
    print("\nPREDICTIONS vs ACTUAL:")
    print("Particle        | n_actual | n_pred  | Error  | q_pred")
    print("-"*55)
    
    total_error = 0
    q_errors = []
    
    for i, a in enumerate(assignments):
        n_pred = alpha * a['dim'] + beta * a['w'] + gamma
        error = abs(n_pred - a['n'])
        total_error += error
        
        q_pred = 4 * n_pred
        q_error = abs(q_pred - a['q'])
        q_errors.append(q_error)
        
        print(f"{a['name']:15s} {a['n']:9.2f} {n_pred:8.2f} {error:7.2f} {q_pred:7.1f}")
    
    avg_error = total_error / len(assignments)
    avg_q_error = np.mean(q_errors)
    
    print(f"\nAverage error in n: {avg_error:.2f}")
    print(f"Average q quantization error: {avg_q_error:.3f}")
    
    if avg_q_error < 0.1:
        print("GOOD: Predicted q values are near integers")
    else:
        print("NOTE: Predicted q values not very integer-like")
    
    return alpha, beta, gamma, avg_error, avg_q_error

def try_different_assignments(particles, alpha, beta, gamma):
    """Try to find better A5 representation assignments"""
    
    print("\n" + "="*60)
    print("EXPLORING BETTER A5 ASSIGNMENTS")
    print("="*60)
    
    # Possible A5 representations and their dimensions
    possible_reps = [
        (1, [0]),           # 1D trivial
        (3, [-1, 0, 1]),    # 3D
        (4, [-3, -1, 1, 3]), # 4D  
        (5, [-2, -1, 0, 1, 2]) # 5D
    ]
    
    print("\nFor each particle, trying all possible (dim, w) combinations...")
    print("(This might take a moment)")
    
    best_assignments = []
    
    for p in particles:
        best_error = float('inf')
        best_dim = 1
        best_w = 0
        
        # Try each representation
        for dim, weights in possible_reps:
            # Try each weight in this representation
            for w in weights:
                n_pred = alpha * dim + beta * w + gamma
                error = abs(n_pred - p['n'])
                
                if error < best_error:
                    best_error = error
                    best_dim = dim
                    best_w = w
        
        best_assignments.append({
            'name': p['name'],
            'dim': best_dim,
            'w': best_w,
            'n_actual': p['n'],
            'error': best_error
        })
    
    # Show best assignments
    print("\nBEST ASSIGNMENTS FOUND:")
    print("Particle        | A5 dim | Weight w | n_actual | Error")
    print("-"*55)
    
    for a in best_assignments:
        print(f"{a['name']:15s} {a['dim']:7d} {a['w']:8d} {a['n_actual']:9.2f} {a['error']:7.2f}")
    
    return best_assignments

def predict_new_particles(alpha, beta, gamma, m_e):
    """Predict masses of possible new particles"""
    
    print("\n" + "="*60)
    print("PREDICTING NEW PARTICLES")
    print("="*60)
    
    print("\nUsing model: n = alpha*dim + beta*w + gamma")
    print(f"alpha={alpha:.4f}, beta={beta:.4f}, gamma={gamma:.4f}")
    
    # All possible A5 states
    all_states = []
    
    # 1D representation
    all_states.append(("1D", 1, 0))
    
    # 3D representation
    for w in [-1, 0, 1]:
        all_states.append(("3D", 3, w))
    
    # 4D representation
    for w in [-3, -1, 1, 3]:
        all_states.append(("4D", 4, w))
    
    # 5D representation
    for w in [-2, -1, 0, 1, 2]:
        all_states.append(("5D", 5, w))
    
    # Calculate predictions
    predictions = []
    for rep_name, dim, w in all_states:
        n_pred = alpha * dim + beta * w + gamma
        mass = m_e * (phi ** n_pred)
        q_pred = 4 * n_pred
        
        predictions.append({
            'rep': rep_name,
            'dim': dim,
            'w': w,
            'n': n_pred,
            'q': q_pred,
            'mass': mass
        })
    
    # Sort by mass
    predictions.sort(key=lambda x: x['mass'])
    
    # Show predictions
    print("\nALL PREDICTED A5 STATES (sorted by mass):")
    print("Rep | dim | w   | n_pred | q_pred | Mass (GeV)")
    print("-"*50)
    
    for p in predictions:
        if 1e-20 < p['mass'] < 1e20:  # Filter extreme values
            print(f"{p['rep']:3s} {p['dim']:4d} {p['w']:4d} {p['n']:7.2f} {p['q']:7.1f} {p['mass']:10.3e}")
    
    # Compare with known particles
    print("\n" + "-"*60)
    print("COMPARISON WITH KNOWN PARTICLES")
    print("-"*60)
    
    known = [
        ("electron", 0.0005109989461),
        ("muon", 0.1056583745),
        ("tau", 1.77686),
        ("top quark", 173.0),
        ("higgs", 125.1)
    ]
    
    for name, mass in known:
        n_actual = log(mass / m_e) / log(phi)
        print(f"\n{name:12s}: n={n_actual:.2f}, mass={mass:.3e}")
        
        # Find nearest predictions
        nearest = []
        for p in predictions:
            if abs(p['n'] - n_actual) < 5.0:
                nearest.append(p)
        
        # Show up to 3 nearest
        nearest.sort(key=lambda x: abs(x['n'] - n_actual))
        for p in nearest[:3]:
            print(f"  Close: {p['rep']} (dim={p['dim']}, w={p['w']}): n={p['n']:.2f}, mass={p['mass']:.3e}")
    
    return predictions

def save_model(alpha, beta, gamma, assignments, predictions, filename="a5_model.json"):
    """Save model results to JSON file"""
    
    import json
    
    model_data = {
        'parameters': {
            'alpha': alpha,
            'beta': beta,
            'gamma': gamma,
            'phi': phi
        },
        'assignments': assignments,
        'predictions': [
            {
                'representation': p['rep'],
                'dimension': p['dim'],
                'weight': p['w'],
                'n_predicted': p['n'],
                'q_predicted': p['q'],
                'mass_predicted': p['mass']
            }
            for p in predictions
        ]
    }
    
    with open(filename, 'w') as f:
        json.dump(model_data, f, indent=2)
    
    print(f"\nModel saved to {filename}")
    return model_data

def main():
    """Main function - build and test A5 model"""
    
    print("CLEAN A5 MODEL BUILDER")
    print("="*60)
    print("Building model: m = m_e * phi^(alpha*dim + beta*w + gamma)")
    print("where phi = golden ratio, dim = A5 rep dimension, w = weight")
    print("="*60)
    
    # Step 1: Load data
    print("\nSTEP 1: Loading particle data...")
    particles, m_e = load_particle_data()
    print(f"Loaded {len(particles)} particles")
    print(f"Electron mass: m_e = {m_e:.6e} GeV")
    print(f"Golden ratio: phi = {phi:.10f}")
    
    # Step 2: Make initial A5 assignments
    print("\nSTEP 2: Making initial A5 representation assignments...")
    assignments = assign_a5_representations(particles)
    
    # Step 3: Fit model
    print("\nSTEP 3: Fitting model parameters...")
    alpha, beta, gamma, avg_error, avg_q_error = fit_model(assignments)
    
    # Step 4: Try to improve assignments
    print("\nSTEP 4: Searching for better assignments...")
    best_assignments = try_different_assignments(particles, alpha, beta, gamma)
    
    # Step 5: Make predictions
    print("\nSTEP 5: Predicting new particles...")
    predictions = predict_new_particles(alpha, beta, gamma, m_e)
    
    # Step 6: Save results
    print("\nSTEP 6: Saving model...")
    model_data = save_model(alpha, beta, gamma, best_assignments, predictions)
    
    # Final summary
    print("\n" + "="*60)
    print("MODEL BUILDING COMPLETE")
    print("="*60)
    
    print(f"""
SUMMARY:
- Model: n = {alpha:.4f}*dim + {beta:.4f}*w + {gamma:.4f}
- Average error in n: {avg_error:.2f}
- Average q quantization error: {avg_q_error:.3f}
- Predictions saved to a5_model.json

INTERPRETATION:
- The factor 4 in q=4n might come from A5 4D representation
- Different particles are assigned to different A5 representations
- The model tries to predict masses based on representation theory

NEXT STEPS:
1. Examine a5_model.json for details
2. Check if assignments make physical sense
3. Test predictions against neutrino data
4. Refine model with better assignments
""")
    
    print("\nRun 'python save.py' to save this session.")

if __name__ == "__main__":
    main()