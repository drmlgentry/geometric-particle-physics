import datetime
import json

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
what = input("What did we just do? (1-2 sentences): ")

try:
    with open("saves.json", "r") as f:
        saves = json.load(f)
except:
    saves = []

saves.append({"time": timestamp, "what": what})

saves = saves[-3:]

with open("saves.json", "w") as f:
    json.dump(saves, f, indent=2)

with open("last_save.txt", "w") as f:
    f.write(f"{timestamp}\n{what}")

print(f"\nSAVED: {timestamp}")
print(f"What: {what}")