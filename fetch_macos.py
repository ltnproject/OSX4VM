#!/usr/bin/env python3
import os
import sys
import subprocess

# OSX4VM - Master Recovery Engine (Personal Edition)
# ------------------------------------------------
# Supports macOS 10.7 (Lion) to 26.0 (Tahoe)
# Uses robust Board ID / MLB matching for official Apple downloads.

RECOVERY_DATA = {
    "1":  {"name": "Lion (10.7)", "bid": "Mac-2E6FAB96566FE58C", "m": "00000000000F25Y00"},
    "2":  {"name": "Mountain Lion (10.8)", "bid": "Mac-7DF2A3B5E5D671ED", "m": "00000000000F65100"},
    "3":  {"name": "Mavericks (10.9)", "bid": "Mac-F60DEB81FF30ACF6", "m": "00000000000FNN100"},
    "4":  {"name": "Yosemite (10.10)", "bid": "Mac-E43C1C25D4880AD6", "m": "00000000000GDVW00"},
    "5":  {"name": "El Capitan (10.11)", "bid": "Mac-FFE5EF870D7BA81A", "m": "00000000000GQRX00"},
    "6":  {"name": "Sierra (10.12)", "bid": "Mac-77F17D7DA9285301", "m": "00000000000J0DX00"},
    "7":  {"name": "High Sierra (10.13)", "bid": "Mac-7BA5B2D9E42DDD94", "m": "00000000000J80300"},
    "8":  {"name": "Mojave (10.14)", "bid": "Mac-7BA5B2DFE22DDD8C", "m": "00000000000KXPG00"},
    "9":  {"name": "Catalina (10.15)", "bid": "Mac-CFF7D910A743CAAF", "m": "00000000000PHCD00"},
    "10": {"name": "Big Sur (11)", "bid": "Mac-2BD1B31983FE1663", "m": "00000000000000000"},
    "11": {"name": "Monterey (12)", "bid": "Mac-E43C1C25D4880AD6", "m": "00000000000000000"},
    "12": {"name": "Ventura (13)", "bid": "Mac-B4831CEBD52A0C4C", "m": "00000000000000000"},
    "13": {"name": "Sonoma (14)", "bid": "Mac-827FAC58A8FDFA22", "m": "00000000000000000"},
    "14": {"name": "Sequoia (15)", "bid": "Mac-7BA5B2D9E42DDD94", "m": "00000000000000000"},
    "15": {"name": "Tahoe (26, Latest)", "bid": "Mac-CFF7D910A743CAAF", "m": "00000000000000000", "latest": True},
}

def main():
    print("\033[1;36mOSX4VM Master Recovery Engine\033[0m")
    print("-----------------------------------")
    
    for k, v in RECOVERY_DATA.items():
        print(f"{k.rjust(2)}. {v['name']}")
    
    try:
        choice = input("\nSelect version to fetch (1-15): ")
        if choice not in RECOVERY_DATA:
            print("[-] Invalid selection.")
            return

        target = RECOVERY_DATA[choice]
        print(f"[*] Fetching recovery data for {target['name']}...")

        # Ensure macrecovery.py exists or is fetched if needed
        # For the Mastered Edition, we assume it's part of the engine
        cmd = [
            sys.executable, "macrecovery.py",
            "-b", target["bid"],
            "-m", target["m"]
        ]
        
        if target.get("latest"):
            cmd += ["-os", "latest"]
            
        cmd.append("download")

        print(f"[*] Executing: {' '.join(cmd)}")
        subprocess.run(cmd)

        print("\n[!] If download succeeded, you will see BaseSystem.dmg/chunklist in this folder.")
        print("[!] Run ./boot.sh to begin installation.")

    except KeyboardInterrupt:
        print("\n[-] Operation cancelled.")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    main()
