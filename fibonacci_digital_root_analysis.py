# fibonacci_digital_root_analysis.py
import numpy as np

print("=" * 100)
print("FIBONACCI DIGITAL ROOT ANALYSIS OF n×4 VALUES")
print("=" * 100)

# Fibonacci numbers (single digit)
fibonacci_digits = {1, 2, 3, 5, 8}

def digital_root(n):
    """Return the digital root of n (repeated digit sum until single digit)"""
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

# Our n×4 values from the golden ratio model (integers)
n_times_4 = {
    'u': 12,   # 3×4
    'd': 18,   # 4.5×4
    's': 43,   # 10.75×4
    'μ': 44,   # 11×4
    'c': 65,   # 16.25×4
    'τ': 68,   # 17×4
    'b': 75,   # 18.75×4
    'W': 99,   # 24.75×4
    'Z': 101,  # 25.25×4
    'H': 103,  # 25.75×4
    't': 106,  # 26.5×4
}

print("\n🔢 ANALYZING EACH n×4 VALUE:")
print("-" * 100)

results = []
for particle, val in n_times_4.items():
    print(f"\n{particle}: n×4 = {val}")
    fib_hits = 0
    for mult in [1, 2, 3, 4]:
        product = val * mult
        dr = digital_root(product)
        is_fib = dr in fibonacci_digits
        if is_fib:
            fib_hits += 1
        print(f"  ×{mult}: {product} → digital root = {dr} {'✓' if is_fib else ''}")
    
    results.append((particle, val, fib_hits))
    print(f"  Fibonacci hits: {fib_hits}/4")

# Summary
print("\n" + "=" * 100)
print("📊 SUMMARY OF FIBONACCI HITS:")
print("-" * 100)

total_hits = sum(hits for _, _, hits in results)
max_possible = len(n_times_4) * 4

print(f"Total Fibonacci hits: {total_hits}/{max_possible}")
print(f"Percentage: {total_hits/max_possible*100:.1f}%")

print("\nParticles with 4/4 Fibonacci hits:")
perfect = [p for p, _, hits in results if hits == 4]
if perfect:
    for p in perfect:
        print(f"  {p}")
else:
    print("  None")

print("\nParticles with 3/4 Fibonacci hits:")
good = [p for p, _, hits in results if hits == 3]
if good:
    for p in good:
        print(f"  {p}")
else:
    print("  None")

print("\n" + "=" * 100)

# Now, let's also check the pattern the user mentioned for 11 and 17 (the n-values)
print("\n🔍 SPECIFIC CHECK FOR n=11 AND n=17 (as in user's example):")
print("-" * 100)

for name, n_val in [("muon", 11), ("tau", 17)]:
    print(f"\n{name} (n={n_val}):")
    for mult in [1, 2, 3, 4]:
        product = n_val * mult
        dr = digital_root(product)
        is_fib = dr in fibonacci_digits
        print(f"  ×{mult}: {product} → digital root = {dr} {'✓' if is_fib else ''}")

print("\n" + "=" * 100)