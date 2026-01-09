# modular_forms_a4_fixed_v2.py
import numpy as np
import mpmath as mp

print("=" * 80)
print("MODULAR FORMS FOR Γ(3) (A₄ SYMMETRY) - FIXED V2")
print("=" * 80)

# Set precision
mp.mp.dps = 50

# Golden ratio
phi = (1 + mp.sqrt(5)) / 2

# Choose τ = i * φ (imaginary axis, magnitude φ)
tau = 1j * phi
print(f"Using τ = iφ = (0 + {float(phi)}i)")
print(f"q = exp(2πiτ) = exp(-2πφ) = {float(mp.e**(-2*mp.pi*phi)):.10e}")

# Dedekind eta function
def eta(tau):
    """Dedekind eta function η(τ) = q^(1/24) ∏_{n=1}∞ (1 - q^n)"""
    q = mp.e**(2j * mp.pi * tau)
    result = q**(1/24)
    for n in range(1, 100):
        result *= (1 - q**n)
    return result

# Modular forms of weight 2 for Γ(3)
print("\n🔢 Weight 2 modular forms for Γ(3):")
print("-" * 80)

# f1(τ) = η(3τ)^3 / η(τ)
f1 = eta(3*tau)**3 / eta(tau)
print(f"f1(τ) = η(3τ)³/η(τ) = {complex(f1)}")

# f2(τ) = η(τ/3)^3 / η(τ)  
f2 = eta(tau/3)**3 / eta(tau)
print(f"f2(τ) = η(τ/3)³/η(τ) = {complex(f2)}")

# Convert to regular complex numbers for easier handling
f1_c = complex(f1)
f2_c = complex(f2)

# A₄ triplet from f1 and f2
Y1 = f1_c + f2_c
Y2 = f1_c * np.exp(2j*np.pi/3) + f2_c * np.exp(4j*np.pi/3)
Y3 = f1_c * np.exp(4j*np.pi/3) + f2_c * np.exp(2j*np.pi/3)

# Normalize
norm = np.sqrt(abs(Y1)**2 + abs(Y2)**2 + abs(Y3)**2)
Y1 /= norm
Y2 /= norm
Y3 /= norm

print(f"\nNormalized A₄ triplet:")
print(f"Y1 = {Y1:.6f}")
print(f"Y2 = {Y2:.6f}")
print(f"Y3 = {Y3:.6f}")

# Try to match with lepton masses
print("\n🔗 Attempt to match with charged lepton masses:")
print("-" * 80)

# Charged lepton masses in GeV
m_e = 0.0005109989461
m_mu = 0.1056583745
m_tau = 1.77686

print("Attempt 1: m_i ∝ |Y_i|²")
masses_from_Y = [abs(Y1)**2, abs(Y2)**2, abs(Y3)**2]
scale = m_tau / max(masses_from_Y)
predicted = [scale * m for m in masses_from_Y]
print(f"Predicted: e={predicted[0]:.6f}, μ={predicted[1]:.6f}, τ={predicted[2]:.6f}")
print(f"Actual:    e={m_e:.6f}, μ={m_mu:.6f}, τ={m_tau:.6f}")

# Calculate errors
errors = [abs(p - a)/a * 100 for p, a in zip(predicted, [m_e, m_mu, m_tau])]
print(f"Errors:    e={errors[0]:.1f}%, μ={errors[1]:.1f}%, τ={errors[2]:.1f}%")

print("\n" + "=" * 80)