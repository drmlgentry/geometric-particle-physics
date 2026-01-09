# hyperbolic_mass_model.py
import numpy as np

print("=" * 70)
print("HYPERBOLIC GEOMETRY MASS MODEL")
print("=" * 70)

# Laplacian eigenvalues on hyperbolic space
# For hyperbolic plane H², eigenvalues: λ = 1/4 + R², where R is related to representation

def hyperbolic_eigenvalues(p, q, n_max=20):
    """
    Eigenvalues of Laplacian on {p,q} tessellation of H²
    p = polygons per face, q = faces per vertex
    """
    eigenvalues = []
    
    # Discrete spectrum
    for n in range(1, n_max + 1):
        # Formula from hyperbolic lattice spectra
        if p == 3 and q == 7:  # {3,7} tessellation
            λ = 1/4 + (2*np.pi*n / np.arccosh((np.cos(np.pi/q)/np.sin(np.pi/p))))**2
        elif p == 5 and q == 4:  # {5,4} tessellation
            λ = 1/4 + (2*np.pi*n / np.arccosh((np.cos(np.pi/q)/np.sin(np.pi/p))))**2
        else:
            # General formula
            χ = 1/p + 1/q - 1/2  # Euler characteristic/area factor
            λ = abs(χ) * n * (n + 1)
        
        eigenvalues.append(λ)
    
    return eigenvalues

# Test different tessellations
tessellations = [(3, 7), (5, 4), (4, 5), (7, 3)]

print("\n📐 Eigenvalues for different hyperbolic tessellations:")
print("-" * 70)

for p, q in tessellations:
    evals = hyperbolic_eigenvalues(p, q, n_max=10)
    print(f"\n{p},{q}-tessellation (first 10 eigenvalues):")
    print(f"  Area per polygon: {2*np.pi*(1/2 - 1/p - 1/q):.3f}")
    print(f"  Eigenvalues: {[f'{x:.3f}' for x in evals]}")
    
    # Try to match with particle masses
    scale = 0.1  # Arbitrary scaling for comparison
    scaled = [scale * x for x in evals]
    
    # Compare with known masses
    known_masses = [0.000511, 0.10566, 1.777, 4.18, 80.377, 91.188, 125.25, 172.76]
    matches = []
    for i, eval_i in enumerate(scaled):
        closest = min(known_masses, key=lambda x: abs(x - eval_i))
        if abs(closest - eval_i)/closest < 0.5:  # Within 50%
            matches.append((i+1, eval_i, closest))
    
    if matches:
        print(f"  Possible mass matches (scale={scale}):")
        for match in matches:
            print(f"    λ_{match[0]} = {match[1]:.3f} ≈ {match[2]:.3f}")

# Try to fit scale to match actual masses
print("\n🔍 Optimizing scale factor:")
print("-" * 70)

for p, q in [(3,7), (5,4)]:
    evals = hyperbolic_eigenvalues(p, q, n_max=15)
    
    # Use first 6 non-zero masses
    target_masses = [0.000511, 0.10566, 1.777, 4.18, 80.377, 91.188]
    
    # Find best scale by linear regression in log space
    log_evals = np.log([e for e in evals[:len(target_masses)] if e > 0])
    log_masses = np.log(target_masses)
    
    # Linear fit: log(m) = log(scale) + exponent * log(λ)
    # Actually simpler: m = scale * λ^exponent
    # Use numpy polyfit
    coeffs = np.polyfit(log_evals, log_masses, 1)
    exponent = coeffs[0]
    log_scale = coeffs[1]
    scale = np.exp(log_scale)
    
    print(f"\n{p},{q}-tessellation fit:")
    print(f"  Scale: {scale:.3e}, Exponent: {exponent:.3f}")
    
    # Calculate predicted masses
    predicted = scale * np.array(evals[:len(target_masses)])**exponent
    
    print(f"  Comparison:")
    for i, (actual, pred) in enumerate(zip(target_masses, predicted)):
        diff_pct = abs(actual - pred)/actual * 100
        print(f"    m{i+1}: actual={actual:.4f}, pred={pred:.4f}, diff={diff_pct:.1f}%")

print("\n" + "=" * 70)