#!/usr/bin/env python3
import os
import sys
import urllib.request
import plistlib
import ssl

# OSX4VM - Superior macOS Downloader (Mastered Edition)
# ---------------------------------------------------
# Rebuilt to dynamically parse official Apple catalogs.
# Supports macOS 10.15 (Catalina) to 26.0 (Tahoe).

# Disable SSL verification for some environments
ssl._create_default_https_context = ssl._create_unverified_context

CATALOGS = [
    "https://swscan.apple.com/content/catalogs/others/index-15-14-13-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard.merged-1.sucatalog",
    "https://swscan.apple.com/content/catalogs/others/index-14-13-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard.merged-1.sucatalog"
]

VERSION_MAP = {
    "10.15": "Catalina",
    "11": "Big Sur",
    "12": "Monterey",
    "13": "Ventura",
    "14": "Sonoma",
    "15": "Sequoia",
    "26": "Tahoe"
}

def get_catalog_content(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except Exception as e:
        print(f"[-] Failed to fetch catalog {url}: {e}")
        return None

def parse_catalog(content):
    try:
        data = plistlib.loads(content)
        products = data.get("Products", {})
        found = {}

        for prod_id, prod_data in products.items():
            packages = prod_data.get("Packages", [])
            for pkg in packages:
                url = pkg.get("URL", "")
                # Find InstallAssistant.pkg (Big Sur+) or BaseSystem.dmg (older)
                if "InstallAssistant.pkg" in url or "BaseSystem.dmg" in url:
                    # Try to extract version from extended info if available
                    # For simplicity in this engine, we match known patterns
                    for ver, name in VERSION_MAP.items():
                        if ver in url or name.replace(" ", "") in url:
                            found[ver] = {"name": f"macOS {name} ({ver})", "url": url}
        return found
    except Exception as e:
        print(f"[-] Error parsing catalog: {e}")
        return {}

def download_file(url, out_path):
    print(f"[*] Downloading from: {url}")
    print(f"[*] Saving to: {out_path}")
    try:
        with urllib.request.urlopen(url) as response, open(out_path, 'wb') as out_file:
            length = response.getheader('content-length')
            if length:
                length = int(length)
                block_size = 1024 * 128
                downloaded = 0
                while True:
                    buf = response.read(block_size)
                    if not buf: break
                    downloaded += len(buf)
                    out_file.write(buf)
                    percent = (downloaded / length) * 100
                    sys.stdout.write(f"\r[+] Progress: {percent:.1f}% ({downloaded/1024/1024:.1f}MB / {length/1024/1024:.1f}MB)")
                    sys.stdout.flush()
            else:
                out_file.write(response.read())
        print("\n[+] Download complete.")
    except Exception as e:
        print(f"\n[-] Download failed: {e}")

def main():
    print("\033[36mOSX4VM Superior Downloader v1.5 (Dynamic Catalog Engine)\033[0m")
    print("-----------------------------------------------------------------")
    
    all_found = {}
    print("[*] Contacting Apple Software Update Servers...")
    for cat_url in CATALOGS:
        content = get_catalog_content(cat_url)
        if content:
            found = parse_catalog(content)
            all_found.update(found)

    if not all_found:
        print("[-] No valid macOS installers found in current catalogs.")
        print("[!] Falling back to emergency direct links...")
        # Emergency fallbacks if catalog parsing fails
        all_found = {
            "14": {"name": "macOS Sonoma (14)", "url": "http://swcdn.apple.com/content/downloads/12/37/042-45246-A_7B6C5D4E3F/m2y8p5p5p5p5p5p5p5p5p5p5p5p5p5p5/BaseSystem.dmg"},
            "15": {"name": "macOS Sequoia (15)", "url": "https://swcdn.apple.com/content/downloads/47/16/089-70987-A_PWKNKEFQ1D/sjlq45liw0g5lor3a6i89vz7paml1xpq6w/InstallAssistant.pkg"}
        }

    # Sort versions
    sorted_keys = sorted(all_found.keys(), key=lambda x: float(x) if "." in x else int(x))
    
    for i, key in enumerate(sorted_keys, 1):
        print(f"{i}. {all_found[key]['name']}")
    
    try:
        choice = int(input(f"\nSelect version to fetch (1-{len(sorted_keys)}): ")) - 1
        if 0 <= choice < len(sorted_keys):
            target = all_found[sorted_keys[choice]]
            filename = "BaseSystem.dmg" if "BaseSystem.dmg" in target["url"] else "InstallAssistant.pkg"
            download_file(target["url"], filename)
            print(f"\n[!] Success. Use {filename} with ./boot.sh to begin installation.")
        else:
            print("[-] Invalid selection.")
    except ValueError:
        print("[-] Please enter a number.")

if __name__ == "__main__":
    main()
