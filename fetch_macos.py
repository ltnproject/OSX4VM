#!/usr/bin/env python3
import os
import sys
import subprocess

# OSX4VM - Master Recovery Engine (Mastered Edition)
# ------------------------------------------------
# Supports macOS 10.7 (Lion) to 26.0 (Tahoe)
# Powered by official acidanthera/macrecovery logic.

RECOVERY_DATA = [
    {"name": "Lion (10.7)", "bid": "Mac-2E6FAB96566FE58C", "m": "00000000000F25Y00"},
    {"name": "Mountain Lion (10.8)", "bid": "Mac-7DF2A3B5E5D671ED", "m": "00000000000F65100"},
    {"name": "Mavericks (10.9)", "bid": "Mac-F60DEB81FF30ACF6", "m": "00000000000FNN100"},
    {"name": "Yosemite (10.10)", "bid": "Mac-E43C1C25D4880AD6", "m": "00000000000GDVW00"},
    {"name": "El Capitan (10.11)", "bid": "Mac-FFE5EF870D7BA81A", "m": "00000000000GQRX00"},
    {"name": "Sierra (10.12)", "bid": "Mac-77F17D7DA9285301", "m": "00000000000J0DX00"},
    {"name": "High Sierra (10.13)", "bid": "Mac-7BA5B2D9E42DDD94", "m": "00000000000J80300"},
    {"name": "Mojave (10.14)", "bid": "Mac-7BA5B2DFE22DDD8C", "m": "00000000000KXPG00"},
    {"name": "Catalina (10.15)", "bid": "Mac-00BE6ED71E35EB86", "m": "00000000000000000"},
    {"name": "Big Sur (11)", "bid": "Mac-2BD1B31983FE1663", "m": "00000000000000000"},
    {"name": "Monterey (12)", "bid": "Mac-E43C1C25D4880AD6", "m": "00000000000000000"},
    {"name": "Ventura (13)", "bid": "Mac-B4831CEBD52A0C4C", "m": "00000000000000000"},
    {"name": "Sonoma (14)", "bid": "Mac-827FAC58A8FDFA22", "m": "00000000000000000"},
    {"name": "Sequoia (15)", "bid": "Mac-7BA5B2D9E42DDD94", "m": "00000000000000000"},
    {"name": "Tahoe (26)", "bid": "Mac-CFF7D910A743CAAF", "m": "00000000000000000", "os": "latest"},
]

def main():
    print("\033[1;36mOSX4VM Master Recovery Engine\033[0m")
    print("-----------------------------------")
    
    for i, target in enumerate(RECOVERY_DATA, 1):
        print(f"{str(i).rjust(2)}. {target['name']}")
    
    try:
        choice = input(f"\nSelect version to fetch (1-{len(RECOVERY_DATA)}): ")
        if not choice.isdigit() or not (1 <= int(choice) <= len(RECOVERY_DATA)):
            print("[-] Invalid selection.")
            return

        target = RECOVERY_DATA[int(choice)-1]
        print(f"[*] Initializing secure stream for {target['name']}...")

        cmd = [
            str(sys.executable), "macrecovery.py",
            "--board", str(target["bid"]),
            "--mlb", str(target["m"]),
            "--os-type", str(target.get("os", "default")),
            "--action", "download"
        ]

        print(f"[*] Executing official recovery logic...")
        subprocess.run(cmd, check=True)

        print("\n[!] Success. BaseSystem.dmg and chunklist should be in this folder.")
        print("[!] Next Step: Run ./boot.sh to begin installation.")

    except KeyboardInterrupt:
        print("\n[-] Operation cancelled.")
    except subprocess.CalledProcessError:
        print("\n[-] Error: The recovery download failed. Check your internet connection.")
    except Exception as e:
        print(f"[-] Unexpected Error: {e}")

if __name__ == "__main__":
    main()
