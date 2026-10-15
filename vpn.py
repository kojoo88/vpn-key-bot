#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import base64
import socket
import time
import os
import subprocess
import sys
import re

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

ADMIN_LINK = "https://www.facebook.com/share/19TVQNTUGZ/"

def clear():
    os.system("clear")

def open_admin_link():
    clear()
    print(PUR + "="*60 + RST)
    print(PUR + "|        ADMIN FACEBOOK                   |" + RST)
    print(PUR + "="*60 + RST)
    print("\n  LINK: " + CYN + ADMIN_LINK + RST)
    print("\n  Opening Facebook...")
    
    opened = False
    try:
        subprocess.run(['termux-open-url', ADMIN_LINK], capture_output=True, timeout=5)
        opened = True
    except:
        pass
    
    if not opened:
        try:
            subprocess.run(['am', 'start', '-a', 'android.intent.action.VIEW', '-d', ADMIN_LINK], capture_output=True, timeout=5)
            opened = True
        except:
            pass
    
    if opened:
        print("  " + GRN + "OK - Opening in browser" + RST)
    else:
        print("  " + YEL + "Please copy link and open manually" + RST)
    
    input("\n  Press Enter to go back...")

def extract_ip_from_url(url):
    ip_pattern = r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
    match = re.search(ip_pattern, url)
    if match:
        return match.group(0)
    try:
        parsed = urllib.parse.urlparse(url.replace('vless://', '').replace('ss://', 'https://'))
        return parsed.hostname
    except:
        return None

def get_country_by_ip(ip):
    if not ip:
        return "??", "Unknown"
    try:
        url = f"https://ipapi.co/{ip}/json/"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=8)
        with urllib.request.urlopen(req) as r:
            import json
            data = json.loads(r.read().decode())
        code = data.get('country_code', '??')
        name = data.get('country_name', 'Unknown')
        return code, name
    except:
        return "??", "Checking..."

def fetch_real_ping(host, port=443, timeout=3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        start = time.perf_counter()
        s.connect((host, port))
        ms = int((time.perf_counter() - start) * 1000)
        s.close()
        if ms < 50:
            return True, ms, "Fast", 5
        elif ms < 100:
            return True, ms, "Good", 4
        elif ms < 200:
            return True, ms, "Normal", 3
        elif ms < 400:
            return True, ms, "Slow", 2
        else:
            return True, ms, "VerySlow", 1
    except:
        return False, 999, "Offline", 0

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

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=25)
        with urllib.request.urlopen(req) as r:
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
                ip = extract_ip_from_url(line)
                country_code, country_name = get_country_by_ip(ip)
                keys.append({
                    "ip": ip,
                    "country": country_code,
                    "country_name": country_name,
                    "protocol": protocol,
                    "url": line
                })
    except:
        pass
    return keys

def load_all():
    vless = []
    ss = []
    clear()
    print(PUR + "="*60 + RST)
    print(PUR + "|         LOADING SOURCES...              |" + RST)
    print(PUR + "-"*60 + RST)
    success_count = 0
    for idx, (name, url, fmt) in enumerate(SOURCES, 1):
        print("  [" + str(idx) + "/" + str(len(SOURCES)) + "] " + name.ljust(25), end=" ")
        content = fetch(url)
        if content:
            keys = parse(content, fmt)
            for k in keys:
                if k["protocol"] == "VLESS":
                    vless.append(k)
                else:
                    ss.append(k)
            print(GRN + "OK " + str(len(keys)) + " keys" + RST)
            success_count += 1
        else:
            print(RED + "FAILED" + RST)
    print(PUR + "="*60 + RST)
    print(GRN + "DONE: " + str(success_count) + "/" + str(len(SOURCES)) + " sources" + RST)
    print("   VLESS: " + str(len(vless)) + "  |  SS: " + str(len(ss)) + WHT)
    load_favorites()
    input("\n  Press Enter to continue...")
    return vless, ss

def scan_and_show(keys, title, count=10):
    if not keys:
        print("\n" + YEL + "Load sources first from Menu [1]" + RST)
        time.sleep(1.5)
        return
    results = []
    clear()
    print(PUR + "="*70 + RST)
    print(PUR + "|  " + title + " "*(66-len(title)) + "|" + RST)
    print(PUR + "-"*70 + RST)
    total = len(keys)
    for i, k in enumerate(keys, 1):
        pct = int(i/total*100)
        print("  Checking: " + str(pct) + "%", end="\r")
        if k.get("ip"):
            ok, ms, lvl, sc = fetch_real_ping(k["ip"])
            if ok and sc > 0:
                k["ms"] = ms
                k["lvl"] = lvl
                k["sc"] = sc
                results.append(k)
    
    results.sort(key=lambda x: x["ms"])
    top = results[:count]
    
    print("\n" + GRN + "FOUND: " + str(len(results)) + " working servers" + RST)
    print(PUR + "="*70 + RST)
    
    for idx, s in enumerate(top, 1):
        stars = "*"*s["sc"] + "-"*(5-s["sc"])
        print("\n" + PUR + "[" + str(idx) + "] " + s["country"] + " | " + s.get("country_name", "") + RST)
        print("  IP  : " + CYN + str(s.get("ip", "N/A")) + RST)
        print("  Ping: " + CYN + str(s["ms"]) + "ms" + RST + "  |  " + stars + "  " + GRN + s["lvl"] + RST)
        print("  Type: " + s["protocol"])
        print(CYN + "FULL KEY:" + RST)
        print(WHT + s["url"] + RST)
        print(PUR + "-"*70 + RST)
    
    input("\n  Press Enter to go back to Menu...")

def best_for_me(all_keys):
    if not all_keys:
        print("\n" + YEL + "Load sources first from Menu [1]" + RST)
        time.sleep(1.5)
        return
    clear()
    print(PUR + "="*70 + RST)
    print(PUR + "|     FINDING BEST SERVER FOR YOU         |" + RST)
    print(PUR + "-"*70 + RST)
    
    results = []
    total = len(all_keys)
    for i, k in enumerate(all_keys, 1):
        pct = int(i/total*100)
        print("  Checking: " + str(pct) + "%", end="\r")
        if k.get("ip"):
            ok, ms, lvl, sc = fetch_real_ping(k["ip"])
            if ok and sc > 0:
                k["ms"] = ms
                k["lvl"] = lvl
                k["sc"] = sc
                results.append(k)
    
    results.sort(key=lambda x: x["ms"])
    if results:
        best = results[0]
        stars = "*"*best["sc"] + "-"*(5-best["sc"])
        
        clear()
        print(PUR + "="*70 + RST)
        print(PUR + "|       BEST SERVER FOUND!                |" + RST)
        print(PUR + "-"*70 + RST)
        print("\n  Country : " + GRN + best["country"] + " - " + best.get("country_name", "") + RST)
        print("  IP      : " + CYN + str(best.get("ip", "N/A")) + RST)
        print("  Protocol: " + best["protocol"])
        print("  Ping    : " + GRN + str(best["ms"]) + "ms" + RST)
        print("  Speed   : " + stars + "  " + GRN + best["lvl"] + RST)
        print("\n" + CYN + "YOUR FULL VPN KEY:" + RST)
        print(WHT + best["url"] + RST)
        print(PUR + "="*70 + RST)
        
        choice = input("\n  [S] Save to Favorites  |  [X] Back to Menu  -> ").upper()
        if choice == "S":
            if best["url"] not in favorites:
                favorites.append(best["url"])
                save_favorites()
                print("\n" + GRN + "SAVED TO FAVORITES!" + RST)
            else:
                print("\n" + YEL + "Already in Favorites" + RST)
        time.sleep(1.5)
    else:
        print("\n" + RED + "No working server found" + RST)
        time.sleep(1.5)

def show_favorites():
    clear()
    print(PUR + "="*70 + RST)
    print(PUR + "|          MY FAVORITE KEYS               |" + RST)
    print(PUR + "-"*70 + RST)
    if not favorites:
        print("\n  No favorites saved yet")
    else:
        print("  Total: " + str(len(favorites)) + " keys\n")
        for idx, url in enumerate(favorites, 1):
            print(PUR + "[" + str(idx) + "]" + RST)
            print(CYN + "FULL KEY:" + RST)
            print(WHT + url + RST)
            print(PUR + "-"*70 + RST)
    input("\n  Press Enter to go back...")

def main():
    vless, ss = [], []
    while True:
        clear()
        net_type = get_net()
        total_keys = len(vless) + len(ss)
        print(PUR + "="*70 + RST)
        print(PUR + "|   VPN KEY FINDER - ACCURATE VERSION     |" + RST)
        print(PUR + "-"*70 + RST)
        print("  Network : " + CYN + net_type + RST)
        print("  Keys Loaded: " + GRN + str(total_keys) + RST)
        print(PUR + "-"*70 + RST)
        print("  [1] Load All Sources")
        print("  [2] Show VLESS Servers (Real Ping & Country)")
        print("  [3] Show SS Servers (Real Ping & Country)")
        print("  [4] Find Best Server")
        print("  [5] My Favorites")
        print("  [6] Open Facebook Page")
        print(PUR + "-"*70 + RST)
        print("  [0] Exit")
        print(PUR + "="*70 + RST)
        choice = input("\n  Enter your choice: ")
        
        if choice == "0":
            clear()
            print("\n  " + GRN + "Goodbye!" + RST + "\n")
            break
        elif choice == "1":
            vless, ss = load_all()
        elif choice == "2":
            scan_and_show(vless, "VLESS SERVERS - FASTEST FIRST", 10)
        elif choice == "3":
            scan_and_show(ss, "SS SERVERS - FASTEST FIRST", 10)
        elif choice == "4":
            best_for_me(vless + ss)
        elif choice == "5":
            show_favorites()
        elif choice == "6":
            open_admin_link()
        else:
            print("\n  " + RED + "Invalid choice! Try again" + RST)
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("\n\n  " + GRN + "Exited. Goodbye!" + RST + "\n")
        sys.exit(0)
    except Exception as e:
        print("\n  " + RED + "ERROR: " + str(e) + RST)
        input("  Press Enter to exit...")
    
