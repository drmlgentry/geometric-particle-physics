# golden_modular_analysis.py
"""
Test predictions from the A5 modular symmetry framework against our mass data
"""

import sqlite3
import numpy as np
from math import log, sqrt

phi = (1 + sqrt(5)) / 2

def load_particle_data():
    """Load particle masses and compute n-values"""
    conn = sqlite3.connect('particle_physics.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name, mass_gev, category 
        FROM particles 
        WHERE mass_gev IS NOT NULL AND mass_gev > 0
        ORDER BY mass_gev
    """)
    
    particles = []
    m_e = 0.0005109989461  # electron mass in GeV
    
    for name, mass, category in cursor.fetchall():
        if mass <= 0:
            continue
        
        # Compute n = log_φ(mass/m_e)
        n = log(mass/m_e) / log(phi)
        
        # Quantize to nearest 0.25
        n_quantized = round(n * 4) / 4
        
        particles.append({
            'name': name,
            'mass': mass,
            'n_raw': n,
            'n_quantized': n_quantized,
            'k': n_quantized * 4,  # Integer k = 4n
            'category': category
        })
    
    conn.close()
    return particles

def test_modular_weight_hypothesis(particles):
    """
    Test if n_i = -k_i/2 + constant as predicted by modular theory
    where k_i are modular weights (integers)
    """
    print("\n" + "="*60)
    print("TESTING MODULAR WEIGHT HYPOTHESIS")
    print("="*60)
    
    # In modular theory: mass ∝ φ^{-k/2} for weight k
    # So n = constant - k/2
    
    # For each particle, solve for k = 2*(constant - n)
    # Try to find constant that makes k near-integers
    
    # Use electron as reference: n_e = 0, assume k_e = 0
    constant = 0  # If k_e = 0, then constant = n_e = 0
    
    print("\nAssuming electron has modular weight k=0 (n=0)")
    print("Then k_i = -2n_i")
    print("\nParticle | n (quantized) | k = -2n | Nearest Int | Error")
    print("-"*55)
    
    for p in particles:
        n = p['n_quantized']
        k = -2 * n
        k_int = round(k)
        error = abs(k - k_int)
        
        print(f"{p['name']:12s} {n:8.2f} {k:10.2f} {k_int:11d} {error:10.3f}")
        
        p['k_modular'] = k
        p['k_int'] = k_int
        p['k_error'] = error

def analyze_fibonacci_patterns(particles):
    """Check if k values are Fibonacci or Lucas numbers"""
    print("\n" + "="*60)
    print("FIBONACCI/LUCAS NUMBER ANALYSIS")
    print("="*60)
    
    # Fibonacci numbers (F_n where F_0=0, F_1=1)
    fib = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
    
    # Lucas numbers (L_n where L_0=2, L_1=1)
    lucas = [2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123]
    
    print("\nParticle | k = 4n | Is Fibonacci? | Is Lucas?")
    print("-"*50)
    
    fib_count = 0
    lucas_count = 0
    
    for p in particles:
        k = int(round(p['k']))
        is_fib = k in fib
        is_lucas = k in lucas
        
        if is_fib:
            fib_count += 1
        if is_lucas:
            lucas_count += 1
        
        print(f"{p['name']:12s} {k:6d} {str(is_fib):14s} {str(is_lucas):12s}")
    
    print(f"\nSummary: {fib_count}/{len(particles)} are Fibonacci numbers")
    print(f"         {lucas_count}/{len(particles)} are Lucas numbers")

def test_eigenvalue_ratios(particles):
    """
    Test if mass ratios within families follow 1 : φ⁻¹ : φ⁻²
    as predicted by the golden matrix M₀ eigenvalues
    """
    print("\n" + "="*60)
    print("TESTING EIGENVALUE RATIO PREDICTION")
    print("="*60)
    
    # Group by category
    categories = {}
    for p in particles:
        cat = p['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(p)
    
    for cat, parts in categories.items():
        if len(parts) < 3:
            continue
            
        # Sort by mass
        parts_sorted = sorted(parts, key=lambda x: x['mass'])
        
        print(f"\n{cat}:")
        print("Particle | Mass (GeV) | Ratio to lightest")
        print("-"*45)
        
        lightest = parts_sorted[0]['mass']
        for i, p in enumerate(parts_sorted[:3]):  # First three
            ratio = p['mass'] / lightest
            print(f"{p['name']:12s} {p['mass']:10.2e} {ratio:15.3f}")
        
        # Predicted ratios: 1 : φ⁻¹ : φ⁻² ≈ 1 : 0.618 : 0.382
        if len(parts_sorted) >= 3:
            ratio1 = parts_sorted[1]['mass'] / lightest
            ratio2 = parts_sorted[2]['mass'] / lightest
            
            print(f"\nPredicted: 1 : {phi**-1:.3f} : {phi**-2:.3f}")
            print(f"Actual:    1 : {ratio1:.3f} : {ratio2:.3f}")
            print(f"Errors:      {abs(ratio1 - phi**-1)/phi**-1*100:.1f}%  {abs(ratio2 - phi**-2)/phi**-2*100:.1f}%")

def analyze_digital_root_patterns(particles):
    """Deep analysis of digital root patterns"""
    print("\n" + "="*60)
    print("DIGITAL ROOT PATTERN ANALYSIS")
    print("="*60)
    
    def digital_root(n):
        if n == 0:
            return 0
        return 1 + ((n - 1) % 9)
    
    fibonacci_dr = {1, 2, 3, 5, 8}  # Digital roots of Fibonacci numbers
    
    print("\nParticle | k=4n | DR(k) | DR(2k) | DR(3k) | Fibonacci DRs")
    print("-"*65)
    
    for p in particles:
        k = int(round(p['k']))
        
        dr1 = digital_root(k)
        dr2 = digital_root(2*k)
        dr3 = digital_root(3*k)
        
        # Count how many are Fibonacci digital roots
        fib_count = sum(1 for dr in [dr1, dr2, dr3] if dr in fibonacci_dr)
        
        print(f"{p['name']:12s} {k:6d} {dr1:7d} {dr2:8d} {dr3:8d} {fib_count}/3")

def main():
    print("ANALYZING PARTICLES THROUGH MODULAR SYMMETRY LENS")
    print("Based on theoretical framework from A5 modular flavor symmetry")
    print("="*60)
    
    particles = load_particle_data()
    
    print(f"Loaded {len(particles)} particles with mass data")
    
    # Run analyses
    test_modular_weight_hypothesis(particles)
    analyze_fibonacci_patterns(particles)
    test_eigenvalue_ratios(particles)
    analyze_digital_root_patterns(particles)
    
    # Special analysis: Check if 4n = Fibonacci or Lucas
    print("\n" + "="*60)
    print("SPECIAL ANALYSIS: 4n AS FIBONACCI/LUCAS NUMBERS")
    print("="*60)
    
    # Extended Fibonacci (including negative indices)
    # F_{-n} = (-1)^{n+1} F_n
    fib_extended = []
    for n in range(-10, 11):
        if n >= 0:
            # Standard Fibonacci
            if n == 0:
                val = 0
            elif n == 1:
                val = 1
            else:
                a, b = 0, 1
                for _ in range(n-1):
                    a, b = b, a+b
                val = b
        else:
            # Fibonacci with negative indices
            m = -n
            val = (-1)**(m+1) * fib_extended[10 + m][1]  # Get from positive side
        
        fib_extended.append((n, val))
    
    print("\nFirst few Fibonacci numbers (including negative indices):")
    for n, val in fib_extended[:15]:
        print(f"F_{n} = {val}")
    
    # Check each particle
    print("\nChecking if 4n matches any Fibonacci number:")
    for p in particles:
        k = p['k']
        for n, fib_val in fib_extended:
            if abs(k - fib_val) < 0.1:  # Allow small rounding
                print(f"{p['name']:12s}: 4n = {k:.1f} ≈ F_{n} = {fib_val}")
                break

if __name__ == "__main__":
    main()