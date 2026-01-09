# golden_ratio_model.py
import numpy as np

print("=" * 80)
print("DIRECT GOLDEN RATIO MASS MODEL")
print("=" * 80)

phi = (1 + np.sqrt(5)) / 2

# Particle masses in GeV
particles = {
    'e': 0.0005109989461,
    'μ': 0.1056583745,
    'τ': 1.77686,
    'u': 0.00216,
    'd': 0.00467,
    's': 0.093,
    'c': 1.27,
    'b': 4.18,
    't': 172.76,
    'W': 80.377,
    'Z': 91.1876,
    'H': 125.25
}

# Hypothesis: m_i = m_0 * φ^(n_i) where n_i are integers or simple fractions
m_e = particles['e']

print("\n🔍 Testing m_i = m_e * φ^(n_i) hypothesis:")
print("-" * 80)

print(f"\nUsing m_e = {m_e:.10f} GeV as base")
print("Looking for integer n such that m_e * φ^n matches other masses")

for name, mass in particles.items():
    if name == 'e':
        continue
    
    # Calculate n from: mass = m_e * φ^n => n = log(mass/m_e)/log(φ)
    n = np.log(mass / m_e) / np.log(phi)
    
    # Find closest integer
    n_int = round(n)
    mass_pred = m_e * phi**n_int
    diff_pct = abs(mass_pred - mass) / mass * 100
    
    # Also check half-integers
    n_half = round(2*n)/2
    mass_pred_half = m_e * phi**n_half
    diff_pct_half = abs(mass_pred_half - mass) / mass * 100
    
    # Choose better match
    if diff_pct_half < diff_pct:
        n_best = n_half
        mass_pred_best = mass_pred_half
        diff_pct_best = diff_pct_half
        type_n = "half-integer"
    else:
        n_best = n_int
        mass_pred_best = mass_pred
        diff_pct_best = diff_pct
        type_n = "integer"
    
    print(f"{name:>2}: n = {n:.3f}, closest {type_n}: n = {n_best}")
    print(f"     Predicted: {mass_pred_best:.6f}, Actual: {mass:.6f}, Diff: {diff_pct_best:.1f}%")

# Alternative: Use φ powers directly (not relative to electron)
print("\n" + "=" * 80)
print("Testing m_i = C * φ^k with common C:")
print("=" * 80)

# Try to find common multiplier
for base_mass in [m_e, particles['μ'], particles['τ'], 1.0]:
    print(f"\nUsing base multiplier C = {base_mass:.6f}:")
    print("-" * 60)
    
    for name, mass in particles.items():
        k = np.log(mass / base_mass) / np.log(phi)
        k_rounded = round(k*4)/4  # Round to nearest 0.25
        pred = base_mass * phi**k_rounded
        diff_pct = abs(pred - mass) / mass * 100
        
        if diff_pct < 20:  # Only show reasonable matches
            print(f"{name:>2}: k = {k:.3f} ≈ {k_rounded:.2f}, pred = {pred:.6f}, diff = {diff_pct:.1f}%")

# Special focus: icosahedral connection
print("\n" + "=" * 80)
print("ICOSAHEDRAL SYMMETRY CONNECTION:")
print("=" * 80)

# Icosahedron has 12 vertices, 20 faces, 30 edges
# Symmetry group A₅ (order 60) contains A₄

# Coordinates of icosahedron vertices involve φ
# Distance ratios in icosahedron:
print("\nKey ratios in regular icosahedron:")
print(f"  Edge length to circumradius: 2/√(φ√5) = {2/np.sqrt(phi*np.sqrt(5)):.6f}")
print(f"  Inradius to circumradius: φ²/(√3) = {phi**2/np.sqrt(3):.6f}")
print(f"  Midradius to circumradius: φ/2 = {phi/2:.6f}")

# Check if these ratios appear in mass ratios
print("\nComparing with mass ratios:")
print(f"  m_τ/m_μ = {particles['τ']/particles['μ']:.6f}")
print(f"  φ²/√3 = {phi**2/np.sqrt(3):.6f} (diff: {abs(particles['τ']/particles['μ'] - phi**2/np.sqrt(3))/(phi**2/np.sqrt(3))*100:.1f}%)")
print(f"  φ⁶/20 = {phi**6/20:.6f} (20 faces) (diff: {abs(particles['τ']/particles['μ'] - phi**6/20)/(phi**6/20)*100:.1f}%)")

# Try A₄/A₅ representation dimensions
print("\nA₄/A₅ representation dimensions:")
print("  A₄ irreps: 1, 1', 1'', 3 (total: 6)")
print("  A₅ irreps: 1, 3, 3', 4, 5 (total: 16)")
print("\nMass ratios might correspond to ratios of representation dimensions:")

# Test: m_i/m_j = dim(R_i)/dim(R_j) ?
rep_dims = [1, 1, 1, 3, 4, 5]  # A₄ and A₅ dimensions

for i in range(len(rep_dims)):
    for j in range(i+1, len(rep_dims)):
        ratio = rep_dims[i] / rep_dims[j]
        # Find closest mass ratio
        closest_ratio = None
        closest_name = None
        closest_diff = float('inf')
        
        for name1, mass1 in particles.items():
            for name2, mass2 in particles.items():
                if mass1 > mass2 and mass2 > 0:
                    mass_ratio = mass1 / mass2
                    diff = abs(mass_ratio - ratio) / ratio
                    if diff < closest_diff:
                        closest_diff = diff
                        closest_ratio = mass_ratio
                        closest_name = f"{name1}/{name2}"
        
        if closest_diff < 0.5:  # Within 50%
            print(f"  {rep_dims[i]}/{rep_dims[j]} = {ratio:.3f} ≈ {closest_name} = {closest_ratio:.3f} (diff: {closest_diff*100:.1f}%)")

print("\n" + "=" * 80)