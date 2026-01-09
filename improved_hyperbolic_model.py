# improved_hyperbolic_model.py
import numpy as np
from scipy.optimize import curve_fit

print("=" * 80)
print("IMPROVED HYPERBOLIC GEOMETRY MASS MODEL")
print("=" * 80)

# Physical constants
m_planck = 1.22e19  # GeV (Planck mass)
m_e = 0.0005109989461  # electron mass in GeV

# We'll try to relate hyperbolic eigenvalues to physical masses
# Hypothesis: m_i = m_planck * exp(-S_i) where S_i is "action" from geometry

def hyperbolic_spectrum(p, q, n_max=20):
    """Improved eigenvalue formula for {p,q} tessellations"""
    eigenvalues = []
    
    # Curvature radius R: for hyperbolic plane, R^2 = -1/K
    # Area of fundamental polygon: A = 4π(g-1) for genus g surface
    # For {p,q} tessellation: A = 2π|χ| where χ = V - E + F
    
    # Better formula from Selberg trace formula for hyperbolic surfaces
    # Eigenvalues: λ_k = 1/4 + r_k^2, r_k real
    
    # For a compact hyperbolic surface, eigenvalues are discrete
    # We'll use a simple progression based on area and topology
    
    area = 2 * np.pi * (1/2 - 1/p - 1/q)  # Gaussian curvature = -1
    if area <= 0:
        return []  # Not hyperbolic
    
    # Approximate eigenvalues: λ_n ≈ (2πn/area)^2 for large n
    # But we need low-lying spectrum
    
    # Use Weyl's law: N(λ) ~ area/(4π) * λ for λ large
    # For small n, use random matrix theory inspired spacing
    
    for n in range(1, n_max + 1):
        # Try different functional forms
        # Form 1: quadratic in n
        λ1 = 0.25 + (n * 2*np.pi / area)**2
        
        # Form 2: linear + quadratic (like quantum harmonic oscillator)
        λ2 = 0.25 + n * (n + 1)
        
        # Form 3: exponential spacing (like string vibrations)
        λ3 = 0.25 + np.exp(n / np.sqrt(area))
        
        # Average them for now
        λ = (λ1 + λ2 + λ3) / 3
        eigenvalues.append(λ)
    
    return eigenvalues

# Mass mapping function
def map_to_masses(eigenvalues, m0, alpha):
    """Map eigenvalues to masses: m = m0 * eigenvalues^alpha"""
    return m0 * np.array(eigenvalues)**alpha

# Target masses (first generation + some others)
target_names = ['electron', 'muon', 'tau', 'strange_quark', 'charm_quark', 'bottom_quark', 'W_boson', 'Z_boson', 'higgs_boson', 'top_quark']
target_masses = [0.000511, 0.10566, 1.77686, 0.093, 1.27, 4.18, 80.377, 91.188, 125.25, 172.76]

print("\n🔍 Testing different tessellations for best fit:")
print("-" * 80)

# Try various {p,q} tessellations
test_tessellations = [
    (3, 7),   # Common in hyperbolic geometry
    (4, 5),   # Gave good results earlier
    (5, 4),   # Dual of {4,5}
    (7, 3),   # Gave good results earlier
    (5, 5),   # Self-dual
    (6, 4),   # Another possibility
    (4, 6),   # Dual of {6,4}
    (8, 3),   # More extreme
]

best_fit = {'tessellation': None, 'rmse': float('inf'), 'params': None}

for p, q in test_tessellations:
    evals = hyperbolic_spectrum(p, q, n_max=len(target_masses))
    
    if len(evals) == 0:
        continue
    
    # Try to fit: m = a * λ^b
    try:
        # Use log-log fit
        log_evals = np.log(evals)
        log_masses = np.log(target_masses)
        
        # Linear fit: log(m) = log(a) + b*log(λ)
        A = np.vstack([log_evals, np.ones(len(log_evals))]).T
        b, log_a = np.linalg.lstsq(A, log_masses, rcond=None)[0]
        a = np.exp(log_a)
        
        # Calculate predicted masses
        predicted = a * evals**b
        
        # Calculate error
        rmse = np.sqrt(np.mean((predicted - target_masses)**2))
        mean_abs_error = np.mean(np.abs(predicted - target_masses))
        
        # Check if this is our best fit so far
        if rmse < best_fit['rmse'] and b > 0:  # b should be positive
            best_fit = {
                'tessellation': (p, q),
                'rmse': rmse,
                'params': (a, b),
                'predicted': predicted,
                'evals': evals
            }
        
        print(f"\n{p},{q}-tessellation:")
        print(f"  Area per polygon: {2*np.pi*(1/2 - 1/p - 1/q):.4f}")
        print(f"  Fit: m = {a:.2e} * λ^{b:.3f}")
        print(f"  RMSE: {rmse:.3f} GeV, Mean abs error: {mean_abs_error:.3f} GeV")
        
        # Show worst prediction
        worst_idx = np.argmax(np.abs(predicted - target_masses))
        print(f"  Worst: {target_names[worst_idx]}: pred={predicted[worst_idx]:.3f}, actual={target_masses[worst_idx]:.3f}")
        
    except Exception as e:
        print(f"\n{p},{q}-tessellation: Error in fitting - {e}")

# Show best fit
if best_fit['tessellation']:
    p, q = best_fit['tessellation']
    a, b = best_fit['params']
    
    print("\n" + "=" * 80)
    print("🏆 BEST FIT FOUND:")
    print("=" * 80)
    print(f"Tessellation: {{{p},{q}}}")
    print(f"Area per polygon: {2*np.pi*(1/2 - 1/p - 1/q):.4f}")
    print(f"Mass formula: m = {a:.3e} × λ^{b:.3f}")
    print(f"RMSE: {best_fit['rmse']:.3f} GeV")
    
    print("\n📊 Detailed comparison:")
    print("-" * 80)
    print(f"{'Particle':<15} {'Actual (GeV)':<12} {'Predicted':<12} {'Diff %':<8}")
    print("-" * 80)
    
    for i in range(len(target_masses)):
        actual = target_masses[i]
        pred = best_fit['predicted'][i]
        diff_pct = abs(pred - actual)/actual * 100
        print(f"{target_names[i]:<15} {actual:<12.6f} {pred:<12.6f} {diff_pct:<8.1f}")

# Try to interpret the parameters
print("\n" + "=" * 80)
print("🔬 PHYSICAL INTERPRETATION OF PARAMETERS:")
print("=" * 80)

if best_fit['params']:
    a, b = best_fit['params']
    
    # What could 'a' represent?
    # If m = a * λ^b, and λ is dimensionless (eigenvalue)
    # then 'a' has dimensions of mass
    
    # Natural scales:
    m_planck = 1.22e19  # GeV
    m_electroweak = 100  # GeV
    m_proton = 0.938    # GeV
    
    print(f"\nScale parameter a = {a:.3e} GeV")
    print(f"This is:")
    print(f"  • {a/m_planck:.3e} × Planck mass")
    print(f"  • {a/m_electroweak:.3e} × electroweak scale")
    print(f"  • {a/m_proton:.3e} × proton mass")
    
    print(f"\nExponent b = {b:.3f}")
    print(f"Possible interpretations:")
    print(f"  • If b ≈ 0.5: m ∝ √λ (like non-relativistic quantum mechanics)")
    print(f"  • If b ≈ 1: m ∝ λ (linear spectrum)")
    print(f"  • If b ≈ 2: m ∝ λ² (quadratic, like excited states)")
    
    # Could 'a' be related to compactification scale?
    # In extra dimensions: m ~ 1/R * (quantum numbers)
    R = 1/a  # in GeV^-1 = ħc/GeV
    R_cm = (6.582e-25 * 3e10) / (a * 1e9)  # Convert GeV^-1 to cm
    print(f"\nIf a = 1/R (compactification scale):")
    print(f"  R = {R:.3e} GeV⁻¹")
    print(f"  R = {R_cm:.3e} cm")
    print(f"  This is {R_cm/1e-13:.1e} × nuclear size (10⁻¹³ cm)")
    print(f"  This is {R_cm/1e-4:.1e} × atomic size (10⁻⁴ cm)")

print("\n" + "=" * 80)