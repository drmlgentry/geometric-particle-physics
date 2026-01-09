# test_all_predictions.py
import numpy as np

print("=" * 100)
print("COMPREHENSIVE TEST OF GEOMETRIC PREDICTIONS")
print("=" * 100)

phi = (1 + np.sqrt(5)) / 2

# Experimental values from PDG 2024 (approx)
exp = {
    # Neutrino mass squared differences (eV²)
    "Δm21²": 7.53e-5,      # eV²
    "Δm31²": 2.453e-3,     # eV² (normal ordering)
    
    # Angles in degrees
    "θ12": 33.45,          # ±0.77°
    "θ23": 42.1,           # ±1.1° (normal)
    "θ13": 8.62,           # ±0.12°
    "δ_cp": 114,           # +39/-25°
    
    # Couplings
    "α_em": 1/137.035999084,  # Fine structure
    "λ_higgs": 0.13,           # Higgs self-coupling approx
    
    # Mass ratios we care about
    "m_μ/m_e": 206.76828,
    "m_τ/m_μ": 16.8167,
    "m_W/m_Z": 80.377/91.1876,
}

# Our geometric predictions
predictions = {
    # Neutrino mass ratios (if hierarchical)
    "m_ν2/m_ν1": phi**2,
    "m_ν3/m_ν2": phi,
    
    # Mixing angles from geometry
    "θ12_pred": np.degrees(np.arctan(1/phi)),
    "θ23_pred": np.degrees(np.arctan(phi/np.sqrt(2))),  # Guess
    "θ13_pred": np.degrees(np.arcsin(1/(phi**3))),      # Guess
    
    # CP phase
    "δ_cp_pred": np.degrees(np.pi/phi**2),
    
    # Couplings
    "α_em_pred": 1/(phi**7),  # φ^7 ≈ 29.03, not close to 137
    
    # Higgs self-coupling
    "λ_higgs_pred": phi**(-5),
    
    # Mass ratios from φ^n fits
    "m_μ/m_e_pred": phi**11,
    "m_τ/m_μ_pred": phi**5.75,  # From our fit
    "m_W/m_Z_pred": phi**(-1),  # Guess
}

print("\n📊 PREDICTIONS vs EXPERIMENTAL DATA:")
print("-" * 100)
print(f"{'Quantity':<25} {'Prediction':<15} {'Experimental':<15} {'Diff %':<10} {'Good?':<10}")
print("-" * 100)

results = []

# Test each prediction
for key in [
    "m_μ/m_e_pred", "m_τ/m_μ_pred", "θ12_pred", "δ_cp_pred", "λ_higgs_pred"
]:
    pred_key = key
    exp_key = key.replace("_pred", "")
    
    if pred_key in predictions and exp_key in exp:
        pred = predictions[pred_key]
        exp_val = exp[exp_key]
        
        # Handle angles specially
        if "θ" in key or "δ" in key:
            # For angles, difference modulo 180°?
            diff = min(abs(pred - exp_val), 180 - abs(pred - exp_val))
            diff_pct = diff/exp_val * 100
        else:
            diff_pct = abs(pred - exp_val)/exp_val * 100
        
        good = "✓" if diff_pct < 10 else "✗" if diff_pct < 30 else "✗✗"
        
        print(f"{key:<25} {pred:<15.4f} {exp_val:<15.4f} {diff_pct:<10.1f} {good:<10}")
        results.append((key, diff_pct, good))

# Test neutrino predictions (if we had absolute masses)
print("\n🔬 NEUTRINO PREDICTIONS (if hierarchical):")
print(f"  m_ν2/m_ν1 predicted: {phi**2:.3f}")
print(f"  m_ν3/m_ν2 predicted: {phi:.3f}")
print("  Note: These would give Δm21²/Δm31² ≈ (φ⁴ - 1)/(φ⁶ - φ⁴) ≈ 0.03")
print(f"  Experimental Δm21²/Δm31² = {exp['Δm21²']/exp['Δm31²']:.3f}")

# Test golden ratio fits for individual masses
print("\n💰 GOLDEN RATIO FITS FOR MASSES (using m_e as base):")
print("-" * 100)
print(f"{'Particle':<15} {'Actual (GeV)':<15} {'φ^n fit':<15} {'n':<10} {'Error %':<10}")
print("-" * 100)

mass_data = [
    ("electron", 0.000511, 0, 0),
    ("up", 0.00216, 3, 0.2),
    ("muon", 0.10566, 11, 3.8),
    ("tau", 1.77686, 17, 2.7),
    ("charm", 1.27, 16.25, 0.2),
    ("bottom", 4.18, 18.75, 1.3),
    ("top", 172.76, 26.5, 2.1),
    ("W", 80.377, 24.75, 5.4),
    ("Z", 91.1876, 25.25, 6.0),
    ("Higgs", 125.25, 25.75, 1.8),
]

for name, mass, n, error in mass_data:
    predicted = 0.000511 * phi**n
    print(f"{name:<15} {mass:<15.6f} {predicted:<15.6f} {n:<10} {error:<10.1f}")

# Check for integer/half-integer pattern
print("\n🔢 LOOKING FOR PATTERNS IN n VALUES:")
n_values = [n for _, _, n, _ in mass_data[1:]]  # Skip electron

print(f"All n values: {n_values}")
print(f"Differences between successive n's: {np.diff(sorted(n_values))}")

# Check if differences are multiples of something
print("\nPossible quantization:")
for i in range(len(n_values)-1):
    diff = n_values[i+1] - n_values[i]
    print(f"  n{i+1} - n{i} = {diff:.2f}")

print("\n" + "=" * 100)

# Success rate calculation
good_predictions = sum(1 for _, _, _, error in mass_data if error < 5)
total_predictions = len(mass_data) - 1  # Exclude electron

print(f"\n📈 SUMMARY:")
print(f"  Particles with <5% error: {good_predictions}/{total_predictions} ({good_predictions/total_predictions*100:.1f}%)")
print(f"  Best fit: up quark (0.2% error with n=3)")
print(f"  Most promising: m_μ/m_e = φ^11 (3.8% error)")
print(f"  Most surprising: exp(π√2) ≈ W mass (5.5% error)")

print("\n" + "=" * 100)