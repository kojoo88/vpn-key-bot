#!/usr/bin/env python3
import urllib.request
import urllib.error
import json
import base64
import os
import sys
import socket
import time
from datetime import datetime

VERSION = "5.4 ⚡ FAST"
FAV_FILE = os.path.join(os.path.expanduser("~"), "vpn-key-bot", "favorites.txt")

class Colors:
    C = "\033[96m"
    G = "\033[92m"
    Y = "\033[93m"
    R = "\033[91m"
    W = "\033[97m"
    rst = "\033[0m"
C = Colors()

API_LIST = {
    "1": ("Shadowmere JSON", "https://shadowmere.xyz/api/sub/", "json"),
    "2": ("Shadowmere Base64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    "3": ("VLESS List", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vless.txt", "txt")
}

PRIORITY = ["singapore", "malaysia", "thailand", "vietnam", "hong", "japan", "korea"]

def clear(): os.system("clear")
def header():
    clear()
    print(f"{C.C}{'='*50}{C.rst}")
    print(f"{C.C}⚡ VPN KEY GENERATOR — {VERSION}{C.rst}")
    print(f"{C.C}{'='*50}{C.rst}\n")

def flag(name):
    n = name.lower()
    if "singapore" in n: return "🇸🇬"
    if "malaysia" in n: return "🇲🇾"
    if "thailand" in n: return "🇹🇭"
    if "vietnam" in n: return "🇻🇳"
    if "hong" in n: return "🇭🇰"
    if "japan" in n: return "🇯🇵"
    if "korea" in n: return "🇰🇷"
    return "🌐"

def ping_fast(host, port=443, timeout=0.3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        st = time.time()
        s.connect((host, int(port)))
        s.close()
        return round((time.time() - st)*1000)
    except:
        return 9999

def fetch_json(url):
    try:
        r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(r, timeout=10) as res:
            return json.loads(res.read().decode())
    except: return None

def get_keys():
    keys = []
    data = fetch_json("https://shadowmere.xyz/api/sub/")
    if data and isinstance(data, list):
        for x in data:
            k = x.get("url") or x.get("link") or ""
            n = x.get("name") or "Server"
            if k and ("vless://" in k or "ss://" in k):
                prio = 99
                for i,c in enumerate(PRIORITY):
                    if c in n.lower(): prio = i; break
                keys.append({"name":n,"key":k,"prio":prio})
    keys.sort(key=lambda x:x["prio"])
    return keys[:15]

def extract_host(key):
    try:
        if "://" in key:
            from urllib.parse import urlparse
            return urlparse(key).hostname or ""
    except: return ""

def copy_text(text):
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", text])
        return True
    except: return False

def find_best():
    header()
    print(f"  🔍 Finding best server...")
    print(f"  📍 Prioritizing: SG → MY → TH → VN → HK → JP → KR\n")
    
    keys = get_keys()
    if not keys:
        print(f"  {C.R}No keys found!{C.rst}")
        input("  Enter to exit...")
        return
    
    best_ms = 9999
    best = None
    
    for i, item in enumerate(keys, 1):
        host = extract_host(item["key"])
        if not host: continue
        ms = ping_fast(host)
        print(f"  {flag(item['name'])} {i}. {item['name'][:20]:<22} → {f'{C.G}{ms}ms{C.rst}' if ms<200 else f'{C.R}{ms}ms{C.rst}'}")
        if ms < best_ms:
            best_ms = ms
            best = item
            if ms < 80: break  # Fast enough!
    
    if not best:
        print(f"\n  {C.R}No server responded{C.rst}")
        return
    
    ft = datetime.now().strftime("%H:%M:%S")
    print(f"\n{C.G}{'='*50}{C.rst}")
    print(f"{C.G}  ✅ BEST: {flag(best['name'])} {best['name']}{C.rst}")
    print(f"  📶 Ping: {C.G}{best_ms}ms{C.rst}  🕐 {ft}")
    print(f"{C.G}{'='*50}{C.rst}")
    print(f"\n  🔑 KEY:\n  {C.W}{best['key']}{C.rst}\n")
    
    if copy_text(best['key']):
        print(f"  {C.G}✅ Copied to clipboard!{C.rst}")
    else:
        print(f"  ⚠️  Copy manually above ↑")
    
    input("\n  Enter to exit...")

def menu():
    while True:
        header()
        print(f"  ⚡ [F] FIND BEST — Fastest mode")
        print(f"  🚪 [X] Exit\n")
        sel = input("  Choose: ").strip().upper()
        if sel == "F": find_best()
        elif sel == "X": break

if __name__ == "__main__":
    try: menu()
    except KeyboardInterrupt: print("\n  Bye!")
    
