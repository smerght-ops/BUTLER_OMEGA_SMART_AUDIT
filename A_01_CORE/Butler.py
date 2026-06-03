import sys, os, logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from A_02_TOOLS import GO

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def main():
    if not os.path.exists(config.MEMORY_DIR): os.makedirs(config.MEMORY_DIR)
    
    files = [f for f in os.listdir(config.ARCHIVE_DIR) if not f.startswith(".")]
    for f in files:
        path = os.path.join(config.ARCHIVE_DIR, f)
        ext = os.path.splitext(f)[1].lower()
        
        if ext in [".jpg", ".jpeg", ".png", ".webp"]:
            print(f"Processing {f}...")
            res = GO.process_image(path)
            with open(os.path.join(config.MEMORY_DIR, f"REPORT_{f}.txt"), "w", encoding="utf-8") as r:
                r.write(res)
            print("Done.")
        else:
            print(f"Skipping {f}")

if __name__ == "__main__":
    main()
