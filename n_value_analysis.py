# n_value_analysis.py
import numpy as np

print("=" * 80)
print("ANALYSIS OF n-VALUES IN GOLDEN RATIO MODEL")
print("=" * 80)

phi = (1 + np.sqrt(5)) / 2

# Particle masses in GeV (including down and strange)
masses = {
    'e': 0.0005109989461,
    'μ': 0.1056583745,
    'τ': 1.77686,
    'u': 0.00216,
    'd': 0.00467,
    's': 0.093,
    'c': 1.27,
    'b': 4.18,
    't': 172.76,
    'W': 80.377,
    'Z': 91.1876,
    'H': 125.25,
}

# Calculate n for each particle (except e)
print("\n🔍 CALCULATED n VALUES FROM MASSES:")
print("-" * 80)
print(f"{'Particle':<6} {'Mass (GeV)':<12} {'n (exact)':<12} {'n (rounded to 0.25)':<20} {'Error % (rounded)':<15}")
print("-" * 80)

n_values = {}
for name, mass in masses.items():
    if name == 'e':
        continue
    n = np.log(mass / masses['e']) / np.log(phi)
    n_rounded = round(n * 4) / 4
    mass_pred = masses['e'] * phi**n_rounded
    error = abs(mass_pred - mass) / mass * 100
    print(f"{name:<6} {mass:<12.6f} {n:<12.6f} {n_rounded:<20.3f} {error:<15.2f}")
    n_values[name] = n_rounded

# Sort by n
sorted_n = sorted(n_values.items(), key=lambda x: x[1])
print("\n📊 SORTED n VALUES (rounded to 0.25):")
for name, n in sorted_n:
    print(f"{name}: n = {n}")

# Look for patterns in the differences
print("\n🔢 DIFFERENCES BETWEEN SUCCESSIVE n VALUES:")
prev_n = None
prev_name = None
for name, n in sorted_n:
    if prev_n is not None:
        diff = n - prev_n
        print(f"{name} - {prev_name}: {diff:.3f}")
    prev_n = n
    prev_name = name

# Check if differences are multiples of a fundamental unit
print("\n🧮 CHECKING FOR QUANTIZATION OF DIFFERENCES:")
diffs = [sorted_n[i+1][1] - sorted_n[i][1] for i in range(len(sorted_n)-1)]
print(f"All differences: {diffs}")
# Try to find a common divisor
for divisor in [0.25, 0.5, 1, 2, 3]:
    rounded = [round(d/divisor) for d in diffs]
    errors = [abs(d - r*divisor) for d, r in zip(diffs, rounded)]
    if max(errors) < 0.01:
        print(f"  Divisor {divisor} works: differences are multiples of {divisor}")
        print(f"  Multipliers: {rounded}")
    else:
        print(f"  Divisor {divisor} does not work (max error = {max(errors):.3f})")

# Try to see if n values are near integers or half-integers
print("\n🔍 CLOSEST INTEGER OR HALF-INTEGER:")
for name, n in sorted_n:
    closest_int = round(n)
    closest_half = round(2*n)/2
    int_diff = abs(n - closest_int)
    half_diff = abs(n - closest_half)
    
    if int_diff < half_diff:
        closest = closest_int
        type_str = "integer"
        diff = int_diff
    else:
        closest = closest_half
        type_str = "half-integer"
        diff = half_diff
    
    if diff < 0.05:
        print(f"{name}: n = {n:.3f} ≈ {closest} ({type_str})")

print("\n" + "=" * 80)