#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import json
import os
import socket
import time
from datetime import datetime

VERSION = "5.5 ⚡ FULL"
FAV_FILE = os.path.join(os.path.expanduser("~"), "vpn-key-bot", "favorites.txt")

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    WHITE = "\033[97m"
    RESET = "\033[0m"

C = Colors()

PRIORITY = ["singapore", "malaysia", "thailand", "vietnam", "hong", "japan", "korea"]

def clear():
    os.system("clear")

def header():
    clear()
    print(f"{C.CYAN}{'='*50}{C.RESET}")
    print(f"{C.CYAN}⚡ VPN KEY GENERATOR  —  {VERSION}{C.RESET}")
    print(f"{C.CYAN}{'='*50}{C.RESET}")
    print()

def get_flag(name):
    n = name.lower()
    if "singapore" in n: return "🇸🇬"
    if "malaysia" in n: return "🇲🇾"
    if "thailand" in n: return "🇹🇭"
    if "vietnam" in n: return "🇻🇳"
    if "hong" in n: return "🇭🇰"
    if "japan" in n: return "🇯🇵"
    if "korea" in n: return "🇰🇷"
    return "🌐"

def ping_test(host, port=443, timeout=0.3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        start = time.time()
        s.connect((host, int(port)))
        s.close()
        return round((time.time() - start) * 1000)
    except:
        return 9999

def fetch_data(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as res:
            return json.loads(res.read().decode())
    except:
        return None

def get_keys():
    keys = []
    data = fetch_data("https://shadowmere.xyz/api/sub/")
    if data and isinstance(data, list):
        for item in data:
            key = item.get("url") or item.get("link") or ""
            name = item.get("name") or "Server"
            if key and ("vless://" in key or "ss://" in key):
                priority = 99
                for i, country in enumerate(PRIORITY):
                    if country in name.lower():
                        priority = i
                        break
                keys.append({"name": name, "key": key, "priority": priority})
    keys.sort(key=lambda x: x["priority"])
    return keys

def extract_host(key):
    try:
        if "://" in key:
            from urllib.parse import urlparse
            return urlparse(key).hostname or "", urlparse(key).port or 443
    except:
        return "", 443

def copy_to_clipboard(text):
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", text])
        return True
    except:
        return False

def save_favorite(item):
    try:
        os.makedirs(os.path.dirname(FAV_FILE), exist_ok=True)
        with open(FAV_FILE, "a", encoding="utf-8") as f:
            f.write(f"{item['name']}|{item['key']}|{datetime.now().strftime('%H:%M:%S')}\n")
        return True
    except:
        return False

def show_key(item, ms=0):
    print(f"{C.GREEN}{'-'*50}{C.RESET}")
    print(f"  {get_flag(item['name'])} {item['name']}")
    if ms > 0:
        status = f"{C.GREEN}{ms}ms{C.RESET}" if ms < 200 else f"{C.YELLOW}{ms}ms{C.RESET}" if ms < 400 else f"{C.RED}{ms}ms{C.RESET}"
        print(f"  📶 Ping: {status}")
    print(f"  🔑 KEY:")
    print(f"  {C.WHITE}{item['key']}{C.RESET}")
    print(f"{C.GREEN}{'-'*50}{C.RESET}")
    
    print(f"  {C.CYAN}[1]{C.RESET} Copy Key    {C.CYAN}[2]{C.RESET} Save to Favorites    {C.CYAN}[Q]{C.RESET} Back")
    sel = input("  Choose: ").strip().upper()
    if sel == "1":
        if copy_to_clipboard(item["key"]):
            print(f"  {C.GREEN}✅ Copied!{C.RESET}")
        else:
            print(f"  ⚠️ Copy manually: {item['key']}")
    elif sel == "2":
        if save_favorite(item):
            print(f"  {C.GREEN}✅ Saved!{C.RESET}")
    input("  Press Enter...")

def find_best():
    header()
    print("  🔍 Finding best server...")
    print("  📍 Priority: SG > MY > TH > VN > HK > JP > KR")
    print()
    
    keys = get_keys()
    if not keys:
        print(f"  {C.RED}❌ No keys found!{C.RESET}")
        input("  Enter to go back...")
        return
    
    best_ms = 9999
    best_server = None
    
    for i, item in enumerate(keys[:15], 1):
        host, port = extract_host(item["key"])
        if not host:
            continue
        ms = ping_test(host, port)
        status = f"{C.GREEN}{ms}ms{C.RESET}" if ms < 200 else f"{C.RED}{ms}ms{C.RESET}"
        print(f"  {get_flag(item['name'])} {i}. {item['name'][:25]:<28} → {status}")
        
        if ms < best_ms:
            best_ms = ms
            best_server = item
            if ms < 80:
                break
    
    if not best_server:
        print(f"\n  {C.RED}❌ No server responded{C.RESET}")
        input("  Enter to go back...")
        return
    
    print()
    show_key(best_server, best_ms)

def find_fastest():
    header()
    print("  🏆 Finding fastest server...")
    print()
    
    keys = get_keys()
    if not keys:
        print(f"  {C.RED}❌ No keys found!{C.RESET}")
        input("  Enter to go back...")
        return
    
    fastest_ms = 9999
    fastest_server = None
    
    for i, item in enumerate(keys[:20], 1):
        host, port = extract_host(item["key"])
        if not host:
            continue
        ms = ping_test(host, port)
        print(f"  {get_flag(item['name'])} {i}. {item['name'][:25]:<28} → {f'{C.GREEN}{ms}ms ← NEW BEST!{C.RESET}' if ms < fastest_ms else f'{ms}ms'}")
        if ms < fastest_ms:
            fastest_ms = ms
            fastest_server = item
    
    if not fastest_server:
        print(f"\n  {C.RED}❌ No server responded{C.RESET}")
        input("  Enter to go back...")
        return
    
    print()
    show_key(fastest_server, fastest_ms)

def browse_all():
    header()
    print("  📋 Loading all servers...")
    print()
    
    keys = get_keys()
    if not keys:
        print(f"  {C.RED}❌ No keys found!{C.RESET}")
        input("  Enter to go back...")
        return
    
    idx = 0
    while True:
        item = keys[idx]
        host, port = extract_host(item["key"])
        ms = ping_test(host, port) if host else 9999
        
        header()
        print(f"  📋 Server {idx+1}/{len(keys)}")
        print(f"  {get_flag(item['name'])} {item['name']}")
        if ms < 9999:
            status = f"{C.GREEN}{ms}ms{C.RESET}" if ms < 200 else f"{C.YELLOW}{ms}ms{C.RESET}" if ms < 400 else f"{C.RED}{ms}ms{C.RESET}"
            print(f"  📶 Ping: {status}")
        print(f"  🔑 KEY:\n  {C.WHITE}{item['key']}{C.RESET}")
        print()
        print(f"  {C.CYAN}[←] Previous    {C.CYAN}[→] Next    {C.CYAN}[1]{C.RESET} Copy    {C.CYAN}[2]{C.RESET} Save    {C.CYAN}[Q]{C.RESET} Back")
        
        sel = input("  Choose: ").strip().upper()
        if sel == "Q":
            break
        elif sel == "1":
            copy_to_clipboard(item["key"])
            print(f"  {C.GREEN}✅ Copied!{C.RESET}")
            time.sleep(0.8)
        elif sel == "2":
            save_favorite(item)
            print(f"  {C.GREEN}✅ Saved!{C.RESET}")
            time.sleep(0.8)
        elif sel == "" or sel == "→":
            idx = (idx + 1) % len(keys)
        elif sel == "←":
            idx = (idx - 1) % len(keys)

def show_favorites():
    header()
    print("  ⭐ Your Favorites")
    print()
    
    if not os.path.exists(FAV_FILE):
        print(f"  {C.YELLOW}No favorites saved yet.{C.RESET}")
    else:
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            print(f"  {C.YELLOW}No favorites saved yet.{C.RESET}")
        else:
            for i, line in enumerate(lines, 1):
                parts = line.strip().split("|", 2)
                name = parts[0] if len(parts) > 0 else "Server"
                key = parts[1] if len(parts) > 1 else ""
                t = parts[2] if len(parts) > 2 else ""
                print(f"  {C.CYAN}[{i}]{C.RESET} {get_flag(name)} {name}")
                if t:
                    print(f"     🕐 {t}")
                print(f"     🔑 {key[:40]}...")
                print()
    input("  Enter to go back...")

def main_menu():
    while True:
        header()
        print("  ⚡ [F] Find Best Server — Auto match")
        print("  🏆 [0] Fastest Server Only")
        print("  📋 [B] Browse All Servers")
        print("  ⭐ [4] My Favorites")
        print("  🚪 [X] Exit")
        print()
        sel = input("  Choose: ").strip().upper()
        if sel == "F":
            find_best()
        elif sel == "0":
            find_fastest()
        elif sel == "B":
            browse_all()
        elif sel == "4":
            show_favorites()
        elif sel == "X":
            print("  👋 Goodbye!")
            break

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n  👋 Goodbye!")
        
