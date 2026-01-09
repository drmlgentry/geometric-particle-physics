# setup_project.py - PART 1
print("🚀 Starting Geometric Particle Physics Project Setup...")
import os
import json
import shutil
from datetime import datetime

# Create directory structure
print("\n📁 Creating directory structure...")
for directory in ['data', 'scripts', 'paper', 'visualizations', 'docs', 'tests', 'output', 'notebooks', 'config']:
    os.makedirs(directory, exist_ok=True)
    print(f"  Created: {directory}/")
os.makedirs('paper/figures', exist_ok=True)
os.makedirs('paper/tables', exist_ok=True)
os.makedirs('.github/workflows', exist_ok=True)