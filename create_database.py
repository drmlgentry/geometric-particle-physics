# create_database.py
import sqlite3
import os

print("Creating particle physics database...")

# Create database directory if it doesn't exist
os.makedirs('data/db', exist_ok=True)

# Connect to database
conn = sqlite3.connect('data/db/particle_physics.db')
cursor = conn.cursor()

# Create just ONE simple table for now
cursor.execute('''
CREATE TABLE IF NOT EXISTS particles (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    mass_gev REAL,
    charge REAL,
    spin REAL
)
''')

# Insert just 3 test particles
test_particles = [
    ('electron', 0.000511, -1, 0.5),
    ('muon', 0.10566, -1, 0.5),
    ('tau', 1.777, -1, 0.5)
]

cursor.executemany('INSERT OR IGNORE INTO particles (name, mass_gev, charge, spin) VALUES (?, ?, ?, ?)', test_particles)

# Commit and verify
conn.commit()

# Count entries
cursor.execute('SELECT COUNT(*) FROM particles')
count = cursor.fetchone()[0]

print(f"Database created at: data/db/particle_physics.db")
print(f"Particles in database: {count}")
print("\nYou can view the database using:")
print("• DB Browser for SQLite (free download)")
print("• Or we'll write a simple viewer script")

conn.close()