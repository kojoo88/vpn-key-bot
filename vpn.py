#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, base64, os, datetime

G = "\033[92m"
B = "\033[94m"
Y = "\033[93m"
R = "\033[91m"
CY = "\033[96m"
RS = "\033[0m"

FAVORITES_FILE = "favorites.txt"
ALL_KEYS_FILE = "all_keys.txt"

def clear():
    os.system("clear")

SOURCES = [
    ("Shadowmere B64", "https://shadowmere.xyz/api/b64sub/", "b64"),
]

def get_text(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", errors="ignore")
    except:
        return None

def parse(text, fmt):
    keys = []
    if not text:
        return keys
    try:
        if fmt == "b64":
            text = base64.b64decode(text).decode("utf-8", errors="ignore")
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            proto = None
            if line.startswith("vless://"):
                proto = "VLESS"
            elif line.startswith("ss://"):
                proto = "SS"
            elif line.startswith("vmess://"):
                proto = "VMESS"
            elif line.startswith("trojan://"):
                proto = "TROJAN"
            if proto:
                name = "Unknown"
                if "#" in line:
                    name = line.split("#")[-1]
                    try:
                        from urllib.parse import unquote
                        name = unquote(name)
                    except:
                        pass
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                keys.append({
                    "proto": proto,
                    "name": name,
                    "key": line,
                    "added_time": now
                })
    except:
        pass
    return keys

def save_to_file(keys, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("Updated: " + str(datetime.datetime.now()) + "\n")
            f.write("Total Keys: " + str(len(keys)) + "\n\n")
            for k in keys:
                f.write(k["proto"] + " | " + k["name"] + "\n")
                f.write(k["key"] + "\n\n")
        return True
    except:
        return False

def load_favorites():
    favs = []
    if os.path.exists(FAVORITES_FILE):
        try:
            with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("ss://") or line.startswith("vless://"):
                        favs.append(line)
        except:
            pass
    return favs

def add_favorite(key_line):
    try:
        with open(FAVORITES_FILE, "a", encoding="utf-8") as f:
            f.write(key_line + "\n")
        return True
    except:
        return False

def search_by_country(keys, keyword):
    result = []
    keyword = keyword.upper()
    for k in keys:
        if keyword in k["name"].upper():
            result.append(k)
    return result

def show(keys, title="Keys"):
    if not keys:
        print()
        print(R + "[-] No keys found" + RS)
        print()
        input("Press Enter to go back")
        return
    
    print()
    print(CY + "=== " + title + " (" + str(len(keys)) + ") ===" + RS)
    print()
    for i, k in enumerate(keys[:10], 1):
        print(str(i) + ". " + k["proto"] + " | " + k["name"])
        print("   Date: " + k.get("added_time", "Unknown"))
        print("   Key: " + k["key"])
        print()
    
    if len(keys) > 10:
        print(Y + "... " + str(len(keys)-10) + " more keys available" + RS)
        print()
    
    input("Press Enter to go back")
    print()

def main():
    clear()
    print("=" * 50)
    print("      VPN KEY FINDER")
    print("=" * 50)
    print()
    
    all_keys = []
    seen = set()
    
    print(Y + "Loading data..." + RS)
    print()
    
    for name, url, fmt in SOURCES:
        print(name + " ... ", end="")
        text = get_text(url)
        ks = parse(text, fmt)
        if ks:
            for k in ks:
                if k["key"] not in seen:
                    seen.add(k["key"])
                    all_keys.append(k)
            print(G + "OK - " + str(len(ks)) + " keys" + RS)
        else:
            print(R + "Failed" + RS)
    
    print()
    print(CY + "Total Keys: " + str(len(all_keys)) + RS)
    print()
    
    while True:
        print("=" * 50)
        print("MENU")
        print("=" * 50)
        print("  1. Show All Keys")
        print("  2. Show VLESS Only")
        print("  3. Show SS Only")
        print("  4. Search by Country/Name")
        print("  5. Save to File")
        print("  6. Show Favorites")
        print("  7. Add Key to Favorites")
        print("  8. Show Subscribe URL")
        print("  0. Exit")
        print("=" * 50)
        
        choice = input("\nChoose option → ").strip()
        
        if choice == "0":
            print()
            print("Goodbye!")
            break
        
        elif choice == "1":
            show(all_keys, "All Keys")
        
        elif choice == "2":
            vless_keys = [k for k in all_keys if k["proto"] == "VLESS"]
            show(vless_keys, "VLESS Keys")
        
        elif choice == "3":
            ss_keys = [k for k in all_keys if k["proto"] == "SS"]
            show(ss_keys, "SS Keys")
        
        elif choice == "4":
            keyword = input("Enter country code or name → ").strip()
            found = search_by_country(all_keys, keyword)
            show(found, "Search Results")
        
        elif choice == "5":
            if save_to_file(all_keys, ALL_KEYS_FILE):
                print()
                print(G + "[+] Saved to " + ALL_KEYS_FILE + RS)
                print()
            else:
                print()
                print(R + "[-] Failed to save" + RS)
                print()
            input("Press Enter to go back")
        
        elif choice == "6":
            fav_keys = load_favorites()
            print()
            if not fav_keys:
                print(Y + "[*] No favorites yet" + RS)
            else:
                print(CY + "=== Favorites ===" + RS)
                print()
                for i, k in enumerate(fav_keys, 1):
                    print(str(i) + ". " + k)
            print()
            input("Press Enter to go back")
        
        elif choice == "7":
            idx_str = input("Enter key number to add → ").strip()
            try:
                idx = int(idx_str) - 1
                if 0 <= idx < len(all_keys):
                    if add_favorite(all_keys[idx]["key"]):
                        print()
                        print(G + "[+] Added to favorites" + RS)
                        print()
                    else:
                        print()
                        print(R + "[-] Failed to add" + RS)
                        print()
                else:
                    print()
                    print(R + "[-] Invalid number" + RS)
                    print()
            except:
                print()
                print(R + "[-] Please enter a valid number" + RS)
                print()
            input("Press Enter to go back")
        
        elif choice == "8":
            print()
            print(CY + "Subscribe URL:" + RS)
            print("https://shadowmere.xyz/api/b64sub/")
            print()
            print(Y + "Use: V2RayNG → + → Subscribe → Paste URL → Refresh" + RS)
            print()
            input("Press Enter to go back")
        
        else:
            print()
            print(R + "[-] Invalid choice" + RS)
            print()

if __name__ == "__main__":
    main()
