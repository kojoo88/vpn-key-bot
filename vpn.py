#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import json
import os
import socket
import time
import base64
from datetime import datetime

VERSION = "5.6 ⚡ NEW SOURCES"
FAV_FILE = os.path.join(os.path.expanduser("~"), "vpn-key-bot", "favorites.txt")

class Colors:
    C = "\033[96m"
    G = "\033[92m"
    Y = "\033[93m"
    R = "\033[91m"
    W = "\033[97m"
    RESET = "\033[0m"

PRIORITY = ["sg", "my", "th", "vn", "hk", "jp", "kr", "us", "tw"]

def clear(): os.system("clear")
def header():
    clear()
    print(f"{Colors.C}{'='*50}{Colors.RESET}")
    print(f"{Colors.C} VPN KEY FINDER — {VERSION}{Colors.RESET}")
    print(f"{Colors.C}{'='*50}{Colors.RESET}")
    print()

def get_flag(name):
    n = name.lower()
    if "sg" in n or "singapore" in n: return "🇸🇬"
    if "my" in n or "malaysia" in n: return "🇲🇾"
    if "th" in n or "thai" in n: return "🇹🇭"
    if "vn" in n or "vietnam" in n: return "🇻🇳"
    if "hk" in n or "hong" in n: return "🇭🇰"
    if "jp" in n or "japan" in n: return "🇯🇵"
    if "kr" in n or "korea" in n: return "🇰🇷"
    if "us" in n or "united states" in n: return "🇺🇸"
    return "🌐"

def ping_test(host, port=443, timeout=0.4):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        st = time.time()
        s.connect((host, int(port)))
        s.close()
        return round((time.time() - st) * 1000)
    except:
        return 9999

def read_links():
    sources = [
        ("https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/sub_merge.txt", "base64"),
        ("https://raw.githubusercontent.com/awesome-vpn/awesome-vpn/main/vless.txt", "plain"),
        ("https://raw.githubusercontent.com/ircfspace/ircfspace/main/config/normal", "plain")
    ]
    all_keys = []
    
    for idx, (url, fmt) in enumerate(sources, 1):
        print(f"  Source {idx}/{len(sources)}: Reading...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as res:
                content = res.read().decode().strip()
                if fmt == "base64":
                    content = base64.b64decode(content).decode("utf-8", errors="ignore")
                lines = content.splitlines()
                count = 0
                for line in lines:
                    line = line.strip()
                    if line.startswith("vless://") or line.startswith("ss://"):
                        name = "Server"
                        if "#" in line:
                            try:
                                from urllib.parse import unquote
                                name = unquote(line.split("#")[-1])
                            except:
                                name = line.split("#")[-1][:30]
                        prio = 99
                        for i, kw in enumerate(PRIORITY):
                            if kw in name.lower():
                                prio = i
                                break
                        all_keys.append({"name":name, "key":line, "prio":prio})
                        count += 1
                print(f"    Found {count} keys")
        except Exception as e:
            print(f"    Failed: {str(e)[:40]}")
    
    all_keys.sort(key=lambda x:x["prio"])
    return all_keys

def extract_host(key):
    try:
        if "://" in key:
            from urllib.parse import urlparse
            u = urlparse(key)
            return u.hostname or "", u.port or 443
    except:
        return "", 443

def copy_key(text):
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", text])
        return True
    except:
        return False

def save_to_fav(item):
    try:
        os.makedirs(os.path.dirname(FAV_FILE), exist_ok=True)
        with open(FAV_FILE, "a", encoding="utf-8") as f:
            f.write(f"{item['name']}|{item['key']}|{datetime.now().strftime('%H:%M')}\n")
        return True
    except:
        return False

def display_key(item, ms=0):
    print(f"\n{Colors.G}{'-'*50}{Colors.RESET}")
    print(f"  {get_flag(item['name'])} {item['name'][:40]}")
    if ms > 0:
        status = f"{Colors.G}{ms}ms{Colors.RESET}" if ms<200 else f"{Colors.Y}{ms}ms{Colors.RESET}" if ms<400 else f"{Colors.R}{ms}ms{Colors.RESET}"
        print(f"  Ping: {status}")
    print(f"  KEY:\n  {Colors.W}{item['key']}{Colors.RESET}")
    print(f"{Colors.G}{'-'*50}{Colors.RESET}")
    print()
    if copy_key(item["key"]):
        print(f"  {Colors.G}✅ Copied to clipboard!{Colors.RESET}")
    else:
        print(f"  ⚠️ Copy manually above")
    input("\nPress Enter...")

def find_best():
    header()
    print("  Searching for best server...")
    print("  Priority: SG > MY > TH > VN > HK > JP > KR")
    print()
    
    keys = read_links()
    if not keys:
        print(f"\n  {Colors.R}❌ No keys found. Check internet connection.{Colors.RESET}")
        input("Enter to go back...")
        return
    
    print(f"\n  Total: {len(keys)} servers found\n")
    
    best_ms = 9999
    best = None
    
    for i, item in enumerate(keys[:12], 1):
        host, port = extract_host(item["key"])
        if not host:
            continue
        ms = ping_test(host, port)
        status = f"{Colors.G}{ms}ms{Colors.RESET}" if ms<200 else f"{Colors.R}{ms}ms{Colors.RESET}"
        print(f"  {get_flag(item['name'])} {i}. {item['name'][:25]:<28} → {status}")
        if ms < best_ms:
            best_ms = ms
            best = item
            if ms < 100:
                break
    
    if not best:
        print(f"\n  {Colors.R}❌ No server responded{Colors.RESET}")
        input("Enter to go back...")
        return
    
    display_key(best, best_ms)

def browse():
    header()
    print("  Loading all servers...\n")
    keys = read_links()
    if not keys:
        print(f"  {Colors.R}❌ No keys found{Colors.RESET}")
        input("Enter to go back...")
        return
    
    idx = 0
    while True:
        item = keys[idx]
        host, port = extract_host(item["key"])
        ms = ping_test(host, port) if host else 9999
        
        header()
        print(f"  Server {idx+1}/{len(keys)}")
        print(f"  {get_flag(item['name'])} {item['name']}")
        if ms < 9999:
            s = f"{Colors.G}{ms}ms{Colors.RESET}" if ms<200 else f"{Colors.Y}{ms}ms{Colors.RESET}" if ms<400 else f"{Colors.R}{ms}ms{Colors.RESET}"
            print(f"  Ping: {s}")
        print(f"  KEY:\n  {Colors.W}{item['key']}{Colors.RESET}")
        print()
        print(f"  [Q] Back  [←] Prev  [→] Next  [C] Copy  [S] Save")
        sel = input("Choose: ").strip().upper()
        if sel == "Q": break
        elif sel == "C":
            copy_key(item["key"])
            print(f"  {Colors.G}✅ Copied!{Colors.RESET}")
            time.sleep(0.7)
        elif sel == "S":
            save_to_fav(item)
            print(f"  {Colors.G}✅ Saved!{Colors.RESET}")
            time.sleep(0.7)
        elif sel == "" or sel == "→":
            idx = (idx + 1) % len(keys)
        elif sel == "←":
            idx = (idx - 1) % len(keys)

def favorites():
    header()
    print("  ⭐ Your Favorites\n")
    if not os.path.exists(FAV_FILE):
        print("  No favorites saved yet")
    else:
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            print("  No favorites saved yet")
        else:
            for i, line in enumerate(lines, 1):
                parts = line.strip().split("|", 2)
                name = parts[0] if len(parts)>0 else "Server"
                key = parts[1] if len(parts)>1 else ""
                t = parts[2] if len(parts)>2 else ""
                print(f"  [{i}] {get_flag(name)} {name}  {t}")
                print(f"      {key[:50]}...")
                print()
    input("Enter to go back...")

def menu():
    while True:
        header()
        print("  [F] Find Best Server")
        print("  [B] Browse All Servers")
        print("  [S] Favorites")
        print("  [X] Exit")
        print()
        sel = input("Choose: ").strip().upper()
        if sel == "F": find_best()
        elif sel == "B": browse()
        elif sel == "S": favorites()
        elif sel == "X": break

if __name__ == "__main__":
    try: menu()
    except KeyboardInterrupt: print("\nGoodbye!")
    
