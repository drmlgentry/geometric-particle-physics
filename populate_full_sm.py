# populate_full_sm.py
import sqlite3

print("Populating Standard Model particles with PDG 2024 values...")

conn = sqlite3.connect('data/db/particle_physics.db')
cursor = conn.cursor()

# Standard Model particles with latest PDG values (GeV)
# Format: (name, mass_gev, charge, spin, type, generation, quantum_numbers_json)
standard_model = [
    # Leptons
    ('electron', 0.0005109989461, -1, 0.5, 'lepton', 1, '{"lepton_number": 1}'),
    ('electron_neutrino', 0.0000000008, 0, 0.5, 'lepton', 1, '{"lepton_number": 1}'),
    ('muon', 0.1056583745, -1, 0.5, 'lepton', 2, '{"lepton_number": 1}'),
    ('muon_neutrino', 0.00000017, 0, 0.5, 'lepton', 2, '{"lepton_number": 1}'),
    ('tau', 1.77686, -1, 0.5, 'lepton', 3, '{"lepton_number": 1}'),
    ('tau_neutrino', 0.0155, 0, 0.5, 'lepton', 3, '{"lepton_number": 1}'),
    
    # Quarks (current masses)
    ('up_quark', 0.00216, 2/3, 0.5, 'quark', 1, '{"color": 3, "isospin": 0.5}'),
    ('down_quark', 0.00467, -1/3, 0.5, 'quark', 1, '{"color": 3, "isospin": -0.5}'),
    ('charm_quark', 1.27, 2/3, 0.5, 'quark', 2, '{"color": 3, "isospin": 0.5}'),
    ('strange_quark', 0.093, -1/3, 0.5, 'quark', 2, '{"color": 3, "isospin": -0.5}'),
    ('top_quark', 172.76, 2/3, 0.5, 'quark', 3, '{"color": 3, "isospin": 0.5}'),
    ('bottom_quark', 4.18, -1/3, 0.5, 'quark', 3, '{"color": 3, "isospin": -0.5}'),
    
    # Gauge bosons
    ('photon', 0.0, 0, 1, 'gauge_boson', 0, '{"force": "electromagnetic"}'),
    ('W_boson', 80.377, 1, 1, 'gauge_boson', 0, '{"force": "weak", "charge": "±1"}'),
    ('Z_boson', 91.1876, 0, 1, 'gauge_boson', 0, '{"force": "weak"}'),
    ('gluon', 0.0, 0, 1, 'gauge_boson', 0, '{"force": "strong", "color": 8}'),
    
    # Scalar
    ('higgs_boson', 125.25, 0, 0, 'scalar', 0, '{"mechanism": "BEH"}'),
]

# First, update our table structure to include type and generation
cursor.execute('''
    CREATE TABLE IF NOT EXISTS particles_full (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        mass_gev REAL,
        charge REAL,
        spin REAL,
        type TEXT,
        generation INTEGER,
        quantum_numbers TEXT
    )
''')

# Insert all particles
for particle in standard_model:
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO particles_full 
            (name, mass_gev, charge, spin, type, generation, quantum_numbers)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', particle)
    except Exception as e:
        print(f"Error inserting {particle[0]}: {e}")

conn.commit()

# Count by type
cursor.execute('SELECT type, COUNT(*) FROM particles_full GROUP BY type')
print("\nParticles by type:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

# Total count
cursor.execute('SELECT COUNT(*) FROM particles_full')
total = cursor.fetchone()[0]
print(f"\nTotal Standard Model particles: {total}")

conn.close()
print("\n✅ Database populated with full Standard Model!")