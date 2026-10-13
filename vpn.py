#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import json
import os
import socket
import time
from datetime import datetime

VERSION = "5.4 ⚡ FAST"
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
    print(f"{C.CYAN}{'='*42}{C.RESET}")
    print(f"{C.CYAN}⚡ VPN Key Finder — {VERSION}{C.RESET}")
    print(f"{C.CYAN}{'='*42}{C.RESET}")
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
    return keys[:15]

def extract_host(key):
    try:
        if "://" in key:
            from urllib.parse import urlparse
            return urlparse(key).hostname or ""
    except:
        return ""

def copy_to_clipboard(text):
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", text])
        return True
    except:
        return False

def find_best():
    header()
    print("  🔍 Finding best server...")
    print("  📍 Priority: SG > MY > TH > VN > HK > JP > KR")
    print()
    
    keys = get_keys()
    if not keys:
        print(f"  {C.RED}❌ No keys found!{C.RESET}")
        input("  Press Enter to exit...")
        return
    
    best_ms = 9999
    best_server = None
    
    for i, item in enumerate(keys, 1):
        host = extract_host(item["key"])
        if not host:
            continue
        ms = ping_test(host)
        display = f"{C.GREEN}{ms}ms{C.RESET}" if ms < 200 else f"{C.RED}{ms}ms{C.RESET}"
        print(f"  {get_flag(item['name'])} {i}. {item['name'][:25]:<28} → {display}")
        
        if ms < best_ms:
            best_ms = ms
            best_server = item
            if ms < 80:
                break
    
    if not best_server:
        print(f"\n  {C.RED}❌ No server responded{C.RESET}")
        return
    
    now = datetime.now().strftime("%H:%M:%S")
    print()
    print(f"{C.GREEN}{'='*42}{C.RESET}")
    print(f"{C.GREEN} ✅ BEST: {get_flag(best_server['name'])} {best_server['name']}{C.RESET}")
    print(f" 📶 Ping: {C.GREEN}{best_ms}ms{C.RESET}  🕐 Time: {now}")
    print(f"{C.GREEN}{'='*42}{C.RESET}")
    print()
    print(f"  🔑 KEY:")
    print(f"  {C.WHITE}{best_server['key']}{C.RESET}")
    print()
    
    if copy_to_clipboard(best_server["key"]):
        print(f"  {C.GREEN}✅ Copied to clipboard!{C.RESET}")
    else:
        print(f"  ⚠️ Copy the key above manually")
    
    input("\n  Press Enter to exit...")

def main_menu():
    while True:
        header()
        print("  ⚡ [F] Find Best Server")
        print("  🚪 [X] Exit")
        print()
        choice = input("  Choose: ").strip().upper()
        if choice == "F":
            find_best()
        elif choice == "X":
            print("  👋 Goodbye!")
            break

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n  👋 Goodbye!")
        
