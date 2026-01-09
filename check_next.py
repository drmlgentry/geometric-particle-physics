# check_next.py
print("Checking next.txt...")
with open("next.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print("Current next steps:")
    print("-"*40)
    print(content)
    print("-"*40)
    print(f"Length: {len(content)} characters")