# tau_search.py
import numpy as np
import cmath

print("=" * 80)
print("SEARCH FOR τ THAT GIVES BETTER MASS PREDICTIONS")
print("=" * 80)

# Target mass ratios (experimental)
target_ratios = {
    "mμ/me": 206.76828,
    "mτ/mμ": 16.8167,
}

def compute_Y(tau):
    """Compute A₄ triplet modular forms at given τ"""
    # Simplified approximation for modular forms
    q = cmath.exp(2j * np.pi * tau)
    
    # Approximate eta functions (first few terms)
    eta_tau = q**(1/24) * (1 - q) * (1 - q**2) * (1 - q**3)
    eta_3tau = (q**3)**(1/24) * (1 - q**3) * (1 - q**6) * (1 - q**9)
    eta_tau3 = (q**(1/3))**(1/24) * (1 - q**(1/3)) * (1 - q**(2/3)) * (1 - q)
    
    f1 = eta_3tau**3 / eta_tau
    f2 = eta_tau3**3 / eta_tau
    
    # A₄ triplet
    Y1 = f1 + f2
    Y2 = f1 * cmath.exp(2j*np.pi/3) + f2 * cmath.exp(4j*np.pi/3)
    Y3 = f1 * cmath.exp(4j*np.pi/3) + f2 * cmath.exp(2j*np.pi/3)
    
    # Normalize
    norm = np.sqrt(abs(Y1)**2 + abs(Y2)**2 + abs(Y3)**2)
    return Y1/norm, Y2/norm, Y3/norm

def error_for_tau(tau):
    """Calculate how well this τ predicts mass ratios"""
    Y1, Y2, Y3 = compute_Y(tau)
    
    # Try simple mapping: m ∝ |Y|^(-k) to get hierarchy
    # We need |Y_e| >> |Y_μ| >> |Y_τ| to get m_e << m_μ << m_τ
    # Actually, since |Y| are ~0.5-0.6, we need inverse relationship
    
    # Try: m_i ∝ |Y_i|^(-p)
    p = 10  # Arbitrary, will optimize
    
    # Calculate predicted ratios
    # Let |Y| sorted: smallest |Y| gives largest mass
    Y_abs = sorted([abs(Y1), abs(Y2), abs(Y3)])
    # Assume correspondence: smallest |Y| -> τ, middle -> μ, largest -> e
    
    pred_mτ_over_mμ = (Y_abs[1]/Y_abs[0])**p  # since m ∝ |Y|^(-p)
    pred_mμ_over_me = (Y_abs[2]/Y_abs[1])**p
    
    error = (abs(pred_mτ_over_mμ - target_ratios["mτ/mμ"])/target_ratios["mτ/mμ"] +
             abs(pred_mμ_over_me - target_ratios["mμ/me"])/target_ratios["mμ/me"])
    
    return error, Y_abs, pred_mτ_over_mμ, pred_mμ_over_me

# Search along imaginary axis (τ = i*t, t > 0)
print("\n🔍 Searching along imaginary axis τ = i*t:")
print("-" * 80)
print(f"{'t (Im τ)':<10} {'Error':<10} {'|Y| values':<25} {'mτ/mμ pred':<12} {'mμ/me pred':<12}")
print("-" * 80)

best_error = float('inf')
best_t = 0
best_Y_abs = []

for t in np.linspace(0.1, 10, 100):
    tau = 1j * t
    error, Y_abs, pred1, pred2 = error_for_tau(tau)
    Y_sorted = sorted(Y_abs)
    
    if error < best_error:
        best_error = error
        best_t = t
        best_Y_abs = Y_abs
    
    if error < 10:  # Only show reasonably good fits
        print(f"{t:<10.3f} {error:<10.3f} {str([f'{y:.3f}' for y in Y_sorted]):<25} {pred1:<12.3f} {pred2:<12.3f}")

print(f"\n🎯 Best found: t = {best_t:.3f}, error = {best_error:.3f}")
print(f"   Corresponding |Y| values: {sorted(best_Y_abs)}")

# Try specific interesting values
print("\n🌟 Trying special τ values:")
special_taus = {
    "i": 1j,
    "i√2": 1j*np.sqrt(2),
    "iφ": 1j*(1+np.sqrt(5))/2,
    "e^(πi/3)": cmath.exp(1j*np.pi/3),
    "2i": 2j,
}

for name, tau in special_taus.items():
    error, Y_abs, pred1, pred2 = error_for_tau(tau)
    print(f"{name:<10} τ = {tau}: error = {error:.3f}, |Y| = {sorted([abs(y) for y in Y_abs])}")

print("\n" + "=" * 80)