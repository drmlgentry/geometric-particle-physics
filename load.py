import json
import os

print("\n" + "="*60)
print("GEOMETRIC PARTICLE PHYSICS - QUICK LOAD")
print("="*60)

if os.path.exists("saves.json"):
    with open("saves.json", "r") as f:
        saves = json.load(f)
    
    if saves:
        latest = saves[-1]
        print(f"\nLAST SESSION: {latest['time']}")
        print(f"WHAT WE DID: {latest['what']}")
        
        if len(saves) > 1:
            print(f"\nPREVIOUS: {saves[-2]['time']}")
            print(f"  {saves[-2]['what'][:50]}...")
    else:
        print("No saves found.")
else:
    print("Starting fresh - no saves found.")

if os.path.exists("next.txt"):
    print("\nNEXT STEPS:")
    with open("next.txt", "r") as f:
        print(f.read())
else:
    print("\nNo next.txt found.")

print("\n" + "="*60)
print("TO SAVE: python save.py")
print("TO ADD STEP: edit next.txt")
print("="*60)