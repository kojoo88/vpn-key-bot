#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import base64
import socket
import time
import os
import subprocess
import sys

# ================== COLORS ==================
BLK = "\033[38;5;234m"
BLU = "\033[38;5;117m"
CYN = "\033[38;5;80m"
GRN = "\033[38;5;114m"
YEL = "\033[38;5;221m"
ORG = "\033[38;5;215m"
RED = "\033[38;5;209m"
PUR = "\033[38;5;141m"
PINK = "\033[38;5;212m"
LIME = "\033[38;5;156m"
WHT = "\033[38;5;255m"
DIM = "\033[2m"
BD = "\033[1m"
RST = "\033[0m"

# ================== ADMIN LINK ==================
ADMIN_LINK = "https://www.facebook.com/share/19TVQNTUGZ/"
# =================================================

def clear():
    os.system("clear")

def open_admin_link():
    clear()
    print(PUR + "="*50 + RST)
    print(PUR + "|    FACEBOOK PAGE LINK                  |" + RST)
    print(PUR + "="*50 + RST)
    print(f"\n  LINK: {CYN}{ADMIN_LINK}{RST}")
    print(f"\n  Copy the link above and open in your browser")
    print(f"\n  Press Enter to go back...")
    input()

# ================== SOURCES ==================
SOURCES = [
    ("V2Nodes", "https://www.v2nodes.com/subscriptions/country/all/?key=72BEE427C23A1AF", "b64"),
    ("Shadowmere B64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("Shadowmere Plain", "https://shadowmere.xyz/api/sub/", "txt"),
    ("V2Ray-Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
    ("Epodon VLESS", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Splitted-By-Protocol/vless.txt", "txt"),
    ("Epodon SS", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/ss.txt", "txt"),
    ("Free V2Ray", "https://raw.githubusercontent.com/freefq/free/master/v2", "b64"),
]

FAV_FILE = "favorites.txt"
favorites = []

def load_favorites():
    global favorites
    favorites = []
    if os.path.exists(FAV_FILE):
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            favorites = [l.strip() for l in f if l.strip()]

def save_favorites():
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        for url in favorites:
            f.write(url + "\n")

def get_net():
    try:
        result = subprocess.run(['ip','link'], capture_output=True, text=True, timeout=3)
        return "WiFi" if 'wlan' in result.stdout.lower() or 'wlp' in result.stdout.lower() else "Mobile"
    except:
        return "Unknown"

def get_country_code(name):
    codes = ["SG", "US", "JP", "KR", "HK", "TW", "UK", "GB", "DE", "NL", "CA", "AU", "IN", "TH", "MY", "CN", "RU", "FR", "IT", "ES"]
    name_upper = name.upper()
    for c in codes:
        if c in name_upper:
            return c
    return "??"

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf-8", errors="ignore")
    except:
        return None

def parse(content, fmt):
    keys = []
    if not content:
        return keys
    try:
        if fmt == "b64":
            content = base64.b64decode(content).decode("utf-8", errors="ignore")
        lines = content.splitlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith(("vless://", "ss://")):
                protocol = "VLESS" if line.startswith("vless://") else "SS"
                code = get_country_code(line)
                name = f"{code}-{protocol}"
                keys.append({"name": name, "url": line, "protocol": protocol, "country": code})
    except:
        pass
    return keys

def ping_test(url):
    try:
        host = "8.8.8.8"
        port = 53
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        start = time.time()
        s.connect((host, port))
        ms = int((time.time() - start) * 1000)
        s.close()
        if ms < 100:
            return True, ms, "Fast", 5
        elif ms < 200:
            return True, ms, "Normal", 4
        elif ms < 300:
            return True, ms, "Medium", 3
        elif ms < 500:
            return True, ms, "Slow", 2
        else:
            return True, ms, "VerySlow", 1
    except:
        return False, 999, "Offline", 0

def load_all():
    all_keys = []
    vless = []
    ss = []
    clear()
    print(PUR + "="*50 + RST)
    print(PUR + "|   LOADING SOURCES...                   |" + RST)
    print(PUR + "-"*50 + RST)
    success_count = 0
    for idx, (name, url, fmt) in enumerate(SOURCES, 1):
        print(f"  [{idx}/{len(SOURCES)}] {name:<25}", end=" ")
        content = fetch(url)
        if content:
            keys = parse(content, fmt)
            for k in keys:
                if k["protocol"] == "VLESS":
                    vless.append(k)
                else:
                    ss.append(k)
            all_keys.extend(keys)
            print(f"{GRN}OK {len(keys)} keys{RST}")
            success_count += 1
        else:
            print(f"{RED}FAILED{RST}")
    print(PUR + "="*50 + RST)
    print(f"{GRN}DONE: {success_count}/{len(SOURCES)} sources{RST}")
    print(f"   VLESS: {len(vless)}  |  SS: {len(ss)}{WHT}")
    load_favorites()
    
    # SAVE ALL KEYS IMMEDIATELY
    with open("all_keys.txt", "w", encoding="utf-8") as f:
        f.write("="*80 + "\n")
        f.write("  ALL KEYS - FULL LIST\n")
        f.write("="*80 + "\n\n")
        f.write(f"Total VLESS: {len(vless)}  |  Total SS: {len(ss)}\n")
        f.write("="*80 + "\n\n")
        idx = 1
        for k in vless:
            f.write(f"[{idx}] {k['country']} | {k['protocol']}\n")
            f.write(f"     KEY: {k['url']}\n")
            f.write("-"*80 + "\n")
            idx += 1
        for k in ss:
            f.write(f"[{idx}] {k['country']} | {k['protocol']}\n")
            f.write(f"     KEY: {k['url']}\n")
            f.write("-"*80 + "\n")
            idx += 1
    print(f"\n{GRN}ALL KEYS SAVED TO: all_keys.txt{RST}")
    print(f"   Type: cat all_keys.txt  to view full keys")
    input(f"\nPress Enter to continue...")
    return vless, ss

def scan_and_show(keys, title, count=20):
    if not keys:
        print(f"\n{YEL}Load sources first!{RST}")
        time.sleep(1.5)
        return
    results = []
    clear()
    print(PUR + "="*70 + RST)
    print(PUR + f"|  {title}{' '*(66-len(title))}|" + RST)
    print(PUR + "-"*70 + RST)
    total = len(keys)
    for i, k in enumerate(keys, 1):
        pct = int(i/total*100)
        print(f"  Checking: {pct}%", end="\r")
        ok, ms, lvl, sc = ping_test(k["url"])
        if ok and sc > 0:
            k["ms"] = ms
            k["lvl"] = lvl
            k["sc"] = sc
            results.append(k)
    
    results.sort(key=lambda x: x["ms"])
    top = results[:count]
    
    # SAVE TO FILE
    with open("results.txt", "w", encoding="utf-8") as f:
        f.write("="*80 + "\n")
        f.write(f"  {title} - TOP {count} (Sorted by Ping)\n")
        f.write("="*80 + "\n\n")
        for idx, s in enumerate(top, 1):
            f.write(f"[{idx}] {s['country']} | Ping: {s['ms']}ms | {s['lvl']}\n")
            f.write(f"     KEY: {s['url']}\n")
            f.write("-"*80 + "\n")
    
    # SHOW SUMMARY ON SCREEN
    print(f"\n{GRN}FOUND: {len(results)} working servers{RST}")
    print(f"{CYN}Full keys saved to: results.txt{RST}")
    print(f"   View with: cat results.txt\n")
    print(PUR + "-"*70 + RST)
    
    for idx, s in enumerate(top, 1):
        stars = "*"*s["sc"] + "-"*(5-s["sc"])
        print(f"  [{idx}] {s['country']:4} | Ping: {CYN}{s['ms']:>4}ms{RST} | {stars} | {GRN}{s['lvl']}{RST}")
    
    print(PUR + "="*70 + RST)
    input(f"\nPress Enter to continue...")

def best_for_me(all_keys):
    if not all_keys:
        print(f"\n{YEL}Load sources first!{RST}")
        time.sleep(1.5)
        return
    clear()
    print(PUR + "="*70 + RST)
    print(PUR + "|  FINDING BEST SERVER FOR YOU...         |" + RST)
    print(PUR + "-"*70 + RST)
    
    results = []
    total = len(all_keys)
    for i, k in enumerate(all_keys, 1):
        pct = int(i/total*100)
        print(f"  Checking: {pct}%", end="\r")
        ok, ms, lvl, sc = ping_test(k["url"])
        if ok and sc > 0:
            k["ms"] = ms
            k["lvl"] = lvl
            k["sc"] = sc
            results.append(k)
    
    results.sort(key=lambda x: x["ms"])
    if results:
        best = results[0]
        
        # SAVE BEST KEY TO FILE
        with open("best_key.txt", "w", encoding="utf-8") as f:
            f.write("="*80 + "\n")
            f.write("  BEST SERVER FOR YOU\n")
            f.write("="*80 + "\n\n")
            f.write(f"Country: {best['country']}\n")
            f.write(f"Protocol: {best['protocol']}\n")
            f.write(f"Ping: {best['ms']}ms\n")
            f.write(f"Speed: {best['lvl']}\n")
            f.write(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n" + "="*80 + "\n")
            f.write(f"FULL KEY:\n{best['url']}\n")
        
        clear()
        print(PUR + "="*70 + RST)
        print(PUR + "|        BEST SERVER FOUND!                |" + RST)
        print(PUR + "-"*70 + RST)
        print(f"\n  Country : {best['country']}")
        print(f"  Protocol: {best['protocol']}")
        print(f"  Ping    : {GRN}{best['ms']}ms{RST}")
        print(f"  Speed   : {GRN}{best['lvl']}{RST}")
        print(f"\n  {PINK}FULL KEY SAVED TO: best_key.txt{RST}")
        print(f"   View with: cat best_key.txt")
        print(f"\n{'─'*70}")
        
        choice = input(f"\n  [S] Save to favorites  |  [X] Back  → ").upper()
        if choice == "S":
            if best["url"] not in favorites:
                favorites.append(best["url"])
                save_favorites()
                print(f"\n{GRN}SAVED TO FAVORITES!{RST}")
            else:
                print(f"\n{YEL}ALREADY IN FAVORITES{RST}")
        time.sleep(1.5)
    else:
        print(f"\n{RED}NO WORKING SERVER FOUND{RST}")
        time.sleep(1.5)

def show_favorites():
    clear()
    print(PUR + "="*70 + RST)
    print(PUR + "|           MY FAVORITES                   |" + RST)
    print(PUR + "-"*70 + RST)
    if not favorites:
        print(f"\n  No favorites saved yet")
    else:
        print(f"  Total: {len(favorites)} keys\n")
        with open("favorites.txt", "r", encoding="utf-8") as f:
            content = f.read()
        print(f"  Full list saved in: favorites.txt")
        print(f"  View with: cat favorites.txt\n")
        for idx, url in enumerate(favorites[:5], 1):
            short = url[:60] + "..." if len(url) > 60 else url
            print(f"  [{idx}] {short}")
        if len(favorites) > 5:
            print(f"  ... and {len(favorites)-5} more")
    input(f"\nPress Enter to continue...")

def main():
    vless, ss = [], []
    while True:
        clear()
        net_type = get_net()
        total_keys = len(vless) + len(ss)
        print(PUR + "="*70 + RST)
        print(PUR + "|      VPN KEY FINDER - PREMIUM            |" + RST)
        print(PUR + "-"*70 + RST)
        print(f"  Network : {CYN}{net_type}{RST}")
        print(f"  Keys Loaded: {GRN}{total_keys}{RST}")
        print(PUR + "-"*70 + RST)
        print(f"  [1] Load All Sources")
        print(f"  [2] Show VLESS Servers")
        print(f"  [3] Show SS Servers")
        print(f"  [4] Find Best Server")
        print(f"  [5] My Favorites")
        print(f"  [6] Admin Facebook Link")
        print(PUR + "-"*70 + RST)
        print(f"  [0] Exit")
        print(PUR + "="*70 + RST)
        choice = input(f"\n  Enter choice: ")
        
        if choice == "0":
            clear()
            print(f"\n  {GRN}GOODBYE!{RST}\n")
            break
        elif choice == "1":
            vless, ss = load_all()
        elif choice == "2":
            scan_and_show(vless, "VLESS SERVERS - FASTEST FIRST", 20)
        elif choice == "3":
            scan_and_show(ss, "SS SERVERS - FASTEST FIRST", 20)
        elif choice == "4":
            best_for_me(vless + ss)
        elif choice == "5":
            show_favorites()
        elif choice == "6":
            open_admin_link()
        else:
            print(f"\n  {RED}INVALID CHOICE!{RST}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print(f"\n\n  {GRN}EXITED{RST}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n  {RED}ERROR: {e}{RST}")
        input(f"  Press Enter to exit...")
