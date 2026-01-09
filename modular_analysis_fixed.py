# modular_analysis_fixed.py
import numpy as np
import mpmath as mp

print("=" * 70)
print("MODULAR FORM ANALYSIS OF PARTICLE MASSES (FIXED)")
print("=" * 70)

# Convert mpmath values to float for formatting
def mp_to_float(x):
    return float(str(x))

# Golden ratio and related constants
phi = (1 + np.sqrt(5)) / 2
pi = np.pi
e = np.e

# Particle masses from our database (in GeV)
masses = {
    'e': 0.0005109989461,
    'ν_e': 0.0000000008,
    'μ': 0.1056583745,
    'ν_μ': 0.00000017,
    'τ': 1.77686,
    'ν_τ': 0.0155,
    'u': 0.00216,
    'd': 0.00467,
    'c': 1.27,
    's': 0.093,
    't': 172.76,
    'b': 4.18,
    'W': 80.377,
    'Z': 91.1876,
    'H': 125.25
}

# Sort by mass
sorted_particles = sorted(masses.items(), key=lambda x: x[1])
sorted_names = [p[0] for p in sorted_particles]
sorted_masses = [p[1] for p in sorted_particles]

print("\n🔢 Testing Mathematical Constants as Mass Generators:")
print("-" * 70)

# Test 1: Exponential of modular form values
print("\n1. exp(π√n) values (Ramanujan-type):")
for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]:
    val = mp.e**(pi * mp.sqrt(n))
    val_float = mp_to_float(val)
    # Find closest mass
    closest = min(sorted_masses, key=lambda x: abs(x - val_float))
    closest_name = sorted_names[sorted_masses.index(closest)]
    diff_pct = abs(closest - val_float) / val_float * 100
    if diff_pct < 10:  # Only show close matches
        print(f"  exp(π√{n}) = {val_float:.4f} ≈ {closest_name} ({closest:.4f}, {diff_pct:.1f}%)")

# Test 2: j-invariant related values
print("\n2. j-invariant and modular discriminant:")
# j-invariant at certain points
points = [mp.mpc(0.5, 0.8660254),  # e^(πi/3)
          mp.mpc(0, 1),            # i
          mp.mpc(0.5, 1.5)]        # (1+i√3)/2

for i, τ in enumerate(points):
    # Approximate j(τ) using q-expansion (simplified)
    q = mp.e**(2j * mp.pi * τ)
    j_val = 1/q + 744 + 196884*q + 21493760*q**2
    j_val = abs(j_val)
    j_val_float = mp_to_float(j_val)
    
    # Scale for comparison
    scaled = j_val_float / 1e6  # Arbitrary scaling
    closest = min(sorted_masses, key=lambda x: abs(x - scaled))
    closest_name = sorted_names[sorted_masses.index(closest)]
    diff_pct = abs(closest - scaled) / scaled * 100
    if diff_pct < 50:
        print(f"  j(τ{i}) ≈ {j_val_float:.2e} → scaled {scaled:.4f} ≈ {closest_name}")

# Test 3: Dedekind eta function ratios
print("\n3. η-function ratios (simplified):")
# η(τ) = q^(1/24) ∏(1-q^n)
def approx_eta_ratio(n, m):
    """Approximate η(nτ)/η(τ)"""
    τ = 1j  # at i
    q = mp.e**(2j * mp.pi * τ)
    q_n = mp.e**(2j * mp.pi * n * τ)
    q_m = mp.e**(2j * mp.pi * m * τ)
    
    # First few terms approximation
    eta1 = q**(1/24) * (1 - q) * (1 - q**2) * (1 - q**3)
    eta_n = q_n**(1/24) * (1 - q_n) * (1 - q_n**2) * (1 - q_n**3)
    eta_m = q_m**(1/24) * (1 - q_m) * (1 - q_m**2) * (1 - q_m**3)
    
    return abs(eta_n / eta_m)

ratios = [(3, 1), (5, 1), (7, 1), (2, 1), (4, 1)]
for n, m in ratios:
    ratio = approx_eta_ratio(n, m)
    ratio_float = mp_to_float(ratio)
    # Map to mass scale
    scaled = ratio_float * phi**3
    closest = min(sorted_masses, key=lambda x: abs(x - scaled))
    closest_name = sorted_names[sorted_masses.index(closest)]
    diff_pct = abs(closest - scaled) / scaled * 100
    if diff_pct < 20:
        print(f"  η({n}i)/η({m}i) ≈ {ratio_float:.4f} → {scaled:.4f} ≈ {closest_name} ({diff_pct:.1f}%)")

# Test 4: Mass formula hypothesis
print("\n4. Hypothetical Mass Formula: m = exp(α√β) * γ")
print("   Testing for electron (m_e = 0.000511):")

# Try to express m_e in terms of fundamental constants
m_e_geometric = mp.e**(-pi * phi) * phi**2  # A guess
m_e_geometric_float = mp_to_float(m_e_geometric)
print(f"   exp(-πφ) * φ² = {m_e_geometric_float:.6f} vs m_e = {masses['e']:.6f}")
print(f"   Ratio: {m_e_geometric_float/masses['e']:.3f}")

# Try another: m_e = (α/2π) * m_μ / φ  where α = 1/137.036
alpha = 1/137.035999084
m_e_test = (alpha/(2*pi)) * masses['μ'] / phi
print(f"   (α/2π) * m_μ / φ = {m_e_test:.6f} vs m_e = {masses['e']:.6f}")
print(f"   Ratio: {m_e_test/masses['e']:.3f}")

print("\n" + "=" * 70)