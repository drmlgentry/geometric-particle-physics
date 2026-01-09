# view_database.py
import sqlite3

# Connect to database
conn = sqlite3.connect('data/db/particle_physics.db')
cursor = conn.cursor()

# Get all particles
cursor.execute('SELECT * FROM particles ORDER BY mass_gev')
particles = cursor.fetchall()

print("=" * 50)
print("PARTICLE DATABASE CONTENTS")
print("=" * 50)
print(f"{'ID':<4} {'Name':<12} {'Mass (GeV)':<12} {'Charge':<8} {'Spin':<6}")
print("-" * 50)

for particle in particles:
    pid, name, mass, charge, spin = particle
    print(f"{pid:<4} {name:<12} {mass:<12.6f} {charge:<8} {spin:<6}")

print("=" * 50)

# Calculate some ratios
cursor.execute('SELECT name, mass_gev FROM particles ORDER BY mass_gev')
results = cursor.fetchall()

if len(results) >= 2:
    electron_mass = results[0][1]  # First row, second column
    muon_mass = results[1][1]
    tau_mass = results[2][1] if len(results) >= 3 else 0
    
    print(f"\nMass Ratios:")
    print(f"m_μ/m_e = {muon_mass/electron_mass:.2f}")
    if tau_mass:
        print(f"m_τ/m_μ = {tau_mass/muon_mass:.2f}")
        print(f"m_τ/m_e = {tau_mass/electron_mass:.2f}")

conn.close()