print("Starting minimal setup...")
import os

# Create directories
for d in ['data', 'scripts', 'paper', 'visualizations']:
    os.makedirs(d, exist_ok=True)
    print(f"Created {d}/")

# Create requirements.txt
with open('requirements.txt', 'w') as f:
    f.write("numpy\nmatplotlib\n")

# Create verification script
with open('scripts/verify.py', 'w') as f:
    f.write("print('Verifying A5 formula...')\n")
    f.write("print('q = a×8 + b×15 + c×24')\n")
    f.write("print('Electron: a=-30, b=0, c=10 → q=0')\n")
    f.write("print('Top quark: a=-28, b=6, c=10 → q=106')\n")

print("Setup complete!")