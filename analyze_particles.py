# analyze_particles.py
import sqlite3
import json
import numpy as np

print("=" * 70)
print("GEOMETRIC PARTICLE PHYSICS ANALYSIS")
print("=" * 70)

conn = sqlite3.connect('data/db/particle_physics.db')
cursor = conn.cursor()

# Get all particles sorted by mass
cursor.execute('''
    SELECT name, mass_gev, charge, spin, type, generation 
    FROM particles_full 
    WHERE mass_gev > 0 
    ORDER BY mass_gev
''')

particles = cursor.fetchall()

print("\nMASS SPECTRUM (in GeV):")
print("-" * 70)
print(f"{'Particle':<20} {'Mass':<12} {'Charge':<8} {'Spin':<6} {'Type':<12} {'Gen':<4}")
print("-" * 70)

for p in particles:
    name, mass, charge, spin, ptype, gen = p
    print(f"{name:<20} {mass:<12.6f} {charge:<8.2f} {spin:<6.1f} {ptype:<12} {gen if gen>0 else '-'}")

print("-" * 70)

# Calculate geometric relationships
print("\n🔍 GEOMETRIC RELATIONSHIPS ANALYSIS:")
print("-" * 70)

# 1. Mass ratios within generations
leptons = [p for p in particles if p[4] == 'lepton' and p[5] > 0]
quarks = [p for p in particles if p[4] == 'quark']

print("\n1. Lepton Mass Ratios (by generation):")
for gen in [1, 2, 3]:
    gen_leptons = [p for p in leptons if p[5] == gen]
    if len(gen_leptons) >= 2:
        neutrino = next((p for p in gen_leptons if 'neutrino' in p[0]), None)
        charged = next((p for p in gen_leptons if 'neutrino' not in p[0]), None)
        if neutrino and charged:
            ratio = charged[1] / neutrino[1] if neutrino[1] > 0 else float('inf')
            print(f"   Generation {gen}: m_charged/m_neutrino = {ratio:.2e}")

# 2. Golden ratio exploration
phi = (1 + np.sqrt(5)) / 2
print(f"\n2. Golden Ratio (φ = {phi:.6f}) relationships:")

# Check if any mass ratios approximate φ^n
masses = [p[1] for p in particles if p[1] > 0]
masses.sort()

for i in range(len(masses)):
    for j in range(i+1, len(masses)):
        ratio = masses[j] / masses[i]
        
        # Check closeness to φ^n for n = 1..10
        for n in range(1, 11):
            phi_power = phi ** n
            if abs(ratio - phi_power) / phi_power < 0.05:  # 5% tolerance
                p1 = next(p[0] for p in particles if abs(p[1] - masses[i]) < 1e-10)
                p2 = next(p[0] for p in particles if abs(p[1] - masses[j]) < 1e-10)
                print(f"   {p2}/{p1} ≈ {ratio:.3f} ~ φ^{n} = {phi_power:.3f}")

# 3. Logarithmic spacing analysis
print("\n3. Logarithmic Spacing Analysis:")
log_masses = np.log([m for m in masses if m > 0])
log_diffs = np.diff(log_masses)

print(f"   Average log spacing: {np.mean(log_diffs):.3f}")
print(f"   Spacing std dev: {np.std(log_diffs):.3f}")
print(f"   Min spacing: {np.min(log_diffs):.3f}")
print(f"   Max spacing: {np.max(log_diffs):.3f}")

# 4. Special ratio: m_tau/m_mu
m_tau = next(p[1] for p in particles if p[0] == 'tau')
m_mu = next(p[1] for p in particles if p[0] == 'muon')
ratio_taumu = m_tau / m_mu

print(f"\n4. Notable Ratio:")
print(f"   m_τ/m_μ = {ratio_taumu:.4f}")
print(f"   Compare to: (π+1)/2 = {(np.pi+1)/2:.4f}")
print(f"   Compare to: φ^2 = {phi**2:.4f}")
print(f"   Compare to: e^(π/2) = {np.exp(np.pi/2):.4f}")

conn.close()