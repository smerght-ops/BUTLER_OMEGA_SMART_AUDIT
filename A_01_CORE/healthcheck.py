import os
import json

def check_system():
    manifest_path = "../A_07_CONFIG/system_manifest.json"
    if not os.path.exists(manifest_path):
        return False, ["✗ Manifest отсутствует"]

    with open(manifest_path, "r") as f:
        config = json.load(f)

    paths = {
        "Workspace": config["workspace"],
        "Storage": config["storage"],
        "Logs": config["logs"]
    }
    
    results = []
    all_ok = True
    
    for name, path in paths.items():
        if os.path.exists(path):
            results.append(f"✓ {name} найден")
        else:
            results.append(f"✗ Каталог {name} ({path}) отсутствует")
            all_ok = False
            
    return all_ok, results

if __name__ == "__main__":
    ok, lines = check_system()
    print("=== BUTLER OMEGA v1.0 FOUNDATION ===")
    for line in lines:
        print(line)
    
    if not ok:
        print("\n!!! SYSTEM NOT READY !!!")
        exit(1)
    else:
        print("\nSYSTEM READY")