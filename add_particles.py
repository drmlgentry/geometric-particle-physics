# add_particles.py
import sqlite3

conn = sqlite3.connect('data/db/particle_physics.db')
cursor = conn.cursor()

# New particles to add (name, mass_gev, charge, spin)
new_particles = [
    ('up_quark', 0.00216, 2/3, 0.5),
    ('down_quark', 0.00467, -1/3, 0.5),
    ('charm_quark', 1.27, 2/3, 0.5),
    ('strange_quark', 0.093, -1/3, 0.5),
    ('top_quark', 173.0, 2/3, 0.5),
    ('bottom_quark', 4.18, -1/3, 0.5),
    ('W_boson', 80.377, 1, 1),
    ('Z_boson', 91.1876, 0, 1),
    ('Higgs', 125.25, 0, 0)
]

cursor.executemany('INSERT OR IGNORE INTO particles (name, mass_gev, charge, spin) VALUES (?, ?, ?, ?)', new_particles)

conn.commit()

# Count total particles
cursor.execute('SELECT COUNT(*) FROM particles')
total = cursor.fetchone()[0]
print(f"Total particles in database: {total}")

conn.close()