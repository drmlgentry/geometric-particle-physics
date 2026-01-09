# focused_a5_analysis.py

import sqlite3
import numpy as np
from math import log, sqrt, pi, cos, sin
import itertools

phi = (1 + sqrt(5)) / 2

def load_particle_data():
    """Load particle data with computed values"""
    conn = sqlite3.connect('particle_physics.db')
    cursor = conn.cursor()
    
    # Get electron mass as reference
    cursor.execute("SELECT mass_gev FROM particles WHERE name='electron'")
    m_e_row = cursor.fetchone()
    m_e = m_e_row[0] if m_e_row else 0.0005109989461
    
    # Load all particles with masses
    cursor.execute("""
        SELECT name, mass_gev, category, generation
        FROM particles 
        WHERE mass_gev IS NOT NULL AND mass_gev > 0
        ORDER BY mass_gev
    """)
    
    particles = []
    for name, mass, category, generation in cursor.fetchall():
        if mass <= 0:
            continue
        
        # Compute n = log_φ(mass/m_e)
        try:
            n_raw = log(mass/m_e) / log(phi)
        except:
            continue
        
        # Quantize to nearest 0.25
        n_quantized = round(n_raw * 4) / 4
        
        particles.append({
            'name': name,
            'mass': mass,
            'n_raw': n_raw,
            'n_quantized': n_quantized,
            'k': n_quantized * 4,  # Integer k = 4n
            'category': category,
            'generation': generation if generation else 0
        })
    
    conn.close()
    return particles, m_e

def golden_matrix_M0():
    """Return the golden matrix M0 from the paper"""
    M0 = np.array([
        [-2/sqrt(3), 1/sqrt(3), -phi**-1],
        [1/sqrt(3), (2/sqrt(3))*phi**-1, -phi**-2],
        [-phi**-1, -phi**-2, (2/sqrt(3))*phi**-2]
    ])
    return M0

def analyze_eigenvalues():
    """Analyze the eigenvalues of the golden matrix M0"""
    M0 = golden_matrix_M0()
    eigenvalues = np.linalg.eigvals(M0)
    sorted_eigen = sorted(eigenvalues, key=abs, reverse=True)
    
    print("Eigenvalues of M0 (sorted by magnitude):")
    for i, val in enumerate(sorted_eigen):
        print(f"  λ_{i+1} = {val:.6f}")
    
    # Normalize to largest magnitude
    norm = abs(sorted_eigen[0])
    ratios = [abs(val)/norm for val in sorted_eigen]
    
    print(f"\nMagnitude ratios: {ratios[0]:.6f} : {ratios[1]:.6f} : {ratios[2]:.6f}")
    print(f"Predicted: 1 : {phi**-1:.6f} : {phi**-2:.6f}")
    
    return sorted_eigen

def find_best_triplet(particles):
    """Find the triplet that best matches the eigenvalue ratios"""
    # We are looking for three particles with mass ratios close to 1 : φ⁻¹ : φ⁻²
    best_error = float('inf')
    best_triplet = None
    
    # Consider all combinations of 3 particles
    for combo in itertools.combinations(particles, 3):
        # Sort by mass
        sorted_combo = sorted(combo, key=lambda x: x['mass'])
        masses = [p['mass'] for p in sorted_combo]
        
        # Normalize to the lightest
        m0 = masses[0]
        ratios = [m/m0 for m in masses]
        
        # Target ratios
        target_ratios = [1, phi**-1, phi**-2]
        
        # Calculate error
        error = 0
        for i in range(3):
            error += (ratios[i] - target_ratios[i])**2
        error = sqrt(error/3)
        
        if error < best_error:
            best_error = error
            best_triplet = sorted_combo
    
    return best_triplet, best_error

def main():
    print("FOCUSED A5 GOLDEN RATIO MODEL ANALYSIS")
    print("="*60)
    
    # Load data
    particles, m_e = load_particle_data()
    print(f"Loaded {len(particles)} particles")
    
    # Analyze eigenvalues of M0
    print("\n" + "-"*60)
    print("1. Golden Matrix M0 Eigenvalue Analysis")
    print("-"*60)
    eigenvalues = analyze_eigenvalues()
    
    # Find best triplet
    print("\n" + "-"*60)
    print("2. Searching for particle triplet matching eigenvalue ratios")
    print("-"*60)
    best_triplet, error = find_best_triplet(particles)
    
    if best_triplet:
        print(f"\nBest matching triplet (error = {error:.4f}):")
        for p in best_triplet:
            print(f"  {p['name']:15s} : mass = {p['mass']:.6e} GeV, n = {p['n_quantized']:.2f}")
        
        masses = [p['mass'] for p in best_triplet]
        ratios = [m/masses[0] for m in masses]
        print(f"\nRatios (to lightest): 1 : {ratios[1]:.6f} : {ratios[2]:.6f}")
        print(f"Target ratios: 1 : {phi**-1:.6f} : {phi**-2:.6f}")
        
        err1 = abs(ratios[1] - phi**-1)/phi**-1 * 100
        err2 = abs(ratios[2] - phi**-2)/phi**-2 * 100
        print(f"Percentage errors: {err1:.2f}%, {err2:.2f}%")
    else:
        print("No triplet found.")
    
    # Modular weight analysis
    print("\n" + "-"*60)
    print("3. Modular Weight Analysis")
    print("-"*60)
    print("Assuming electron has modular weight 0 (n_e = 0)")
    print("Then for any particle: k = -2n")
    print("\nParticle        | n      | k = -2n | Nearest Int | Error")
    print("-"*55)
    
    for p in particles[:15]:  # Show first 15
        n = p['n_quantized']
        k = -2 * n
        k_int = round(k)
        error = abs(k - k_int)
        
        print(f"{p['name']:15s} {n:7.2f} {k:9.2f} {k_int:11d} {error:8.3f}")
    
    # Overall statistics
    k_errors = []
    for p in particles:
        n = p['n_quantized']
        k = -2 * n
        k_int = round(k)
        error = abs(k - k_int)
        k_errors.append(error)
    
    good_matches = sum(1 for err in k_errors if err < 0.1)
    print(f"\nParticles with k within 0.1 of integer: {good_matches}/{len(particles)}")
    print(f"Average error: {np.mean(k_errors):.3f}")
    
    # Check for Fibonacci pattern in k
    print("\n" + "-"*60)
    print("4. Fibonacci Pattern in k = 4n")
    print("-"*60)
    
    fibonacci = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    fib_count = 0
    for p in particles:
        k = int(round(p['k']))
        if k in fibonacci:
            fib_count += 1
            print(f"  {p['name']:15s} : k = {k} (Fibonacci)")
    
    print(f"\nTotal particles with k as Fibonacci number: {fib_count}/{len(particles)}")

if __name__ == "__main__":
    main()