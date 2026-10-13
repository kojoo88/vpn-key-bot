#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import json
import os
import socket
import time
from datetime import datetime

VERSION = "5.5.1 ⚡ FIXED"
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
API_URLS = [
    "https://shadowmere.xyz/api/sub/",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vless.txt"
]

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

def ping_test(host, port=443, timeout=0.35):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        start = time.time()
        s.connect((host, int(port)))
        s.close()
        return round((time.time() - start) * 1000)
    except:
        return 9999

def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as res:
            return json.loads(res.read().decode())
    except Exception as e:
        print(f"  {C.YELLOW}⚠️  {url} မအောင်မြင်ပါ: {str(e)[:40]}{C.RESET}")
        return None

def fetch_text(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as res:
            return res.read().decode().splitlines()
    except Exception as e:
        print(f"  {C.YELLOW}⚠️  {url} မအောင်မြင်ပါ{C.RESET}")
        return None

def get_keys():
    all_keys = []
    
    # Source 1: Shadowmere JSON
    print(f"  📥 ရှာဖွေနေသည်... (အရင်းအမြစ် ၁/၂)")
    data = fetch_json(API_URLS[0])
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
                all_keys.append({"name": name, "key": key, "priority": priority})
    
    # Source 2: GitHub VLESS list
    print(f"  📥 ရှာဖွေနေသည်... (အရင်းအမြစ် ၂/၂)")
    lines = fetch_text(API_URLS[1])
    if lines:
        for line in lines:
            line = line.strip()
            if line.startswith("vless://"):
                name = "VLESS Server"
                if "#" in line:
                    try:
                        from urllib.parse import unquote
                        name = unquote(line.split("#")[-1])
                    except:
                        pass
                priority = 99
                for i, country in enumerate(PRIORITY):
                    if country.lower() in name.lower():
                        priority = i
                        break
                all_keys.append({"name": name, "key": line, "priority": priority})
    
    if all_keys:
        all_keys.sort(key=lambda x: x["priority"])
        print(f"  ✅ စုစုပေါင်း {len(all_keys)} ခု တွေ့ရှိခဲ့သည်")
    return all_keys

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
    print(f"\n{C.GREEN}{'-'*50}{C.RESET}")
    print(f"  {get_flag(item['name'])} {item['name']}")
    if ms > 0:
        status = f"{C.GREEN}{ms}ms{C.RESET}" if ms < 200 else f"{C.YELLOW}{ms}ms{C.RESET}" if ms < 400 else f"{C.RED}{ms}ms{C.RESET}"
        print(f"  📶 မြန်နှုန်း: {status}")
    print(f"  🔑 ကီး:")
    print(f"  {C.WHITE}{item['key']}{C.RESET}")
    print(f"{C.GREEN}{'-'*50}{C.RESET}")
    
    print(f"  {C.CYAN}[1]{C.RESET} ကီးကိုကူးယူမယ်    {C.CYAN}[2]{C.RESET} အကြိုက်ဆုံးထဲသိမ်းမယ်    {C.CYAN}[Q]{C.RESET} နောက်သို့")
    sel = input("  ရွေးပါ: ").strip().upper()
    if sel == "1":
        if copy_to_clipboard(item["key"]):
            print(f"  {C.GREEN}✅ ကူးယူပြီးပါပြီ!{C.RESET}")
        else:
            print(f"  ⚠️ အထက်ကကီးကို ကိုယ်တိုင်ကူးယူပါ")
    elif sel == "2":
        if save_favorite(item):
            print(f"  {C.GREEN}✅ သိမ်းပြီးပါပြီ!{C.RESET}")
    input("  ဆက်ရန် Enter နှိပ်ပါ...")

def find_best():
    header()
    print("  🔍 အကောင်းဆုံးဆာဗာကို ရှာဖွေနေသည်...")
    print("  📍 ဦးစားပေး → စင်ကာပူ > မလေးရှား > ထိုင်း > ဗီယက်နမ် > ဟောင်ကောင်း > ဂျပန် > ကိုရီးယား")
    print()
    
    keys = get_keys()
    if not keys:
        print(f"  {C.RED}❌ ကီးမတွေ့ပါ။ အင်တာနက်ချိတ်ဆက်မှု စစ်ဆေးပါ။{C.RESET}")
        input("  ပြန်ရန် Enter နှိပ်ပါ...")
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
        print(f"\n  {C.RED}❌ မည်သည့်ဆာဗာမှ အကျဉ်းမတုံ့ပြန်ပါ{C.RESET}")
        input("  ပြန်ရန် Enter နှိပ်ပါ...")
        return
    
    show_key(best_server, best_ms)

def find_fastest():
    header()
    print("  🏆 အမြန်ဆုံးဆာဗာကို ရှာဖွေနေသည်...")
    print()
    
    keys = get_keys()
    if not keys:
        print(f"  {C.RED}❌ ကီးမတွေ့ပါ။ အင်တာနက်ချိတ်ဆက်မှု စစ်ဆေးပါ။{C.RESET}")
        input("  ပြန်ရန် Enter နှိပ်ပါ...")
        return
    
    fastest_ms = 9999
    fastest_server = None
    
    for i, item in enumerate(keys[:20], 1):
        host, port = extract_host(item["key"])
        if not host:
            continue
        ms = ping_test(host, port)
        marker = " ← အမြန်ဆုံး!" if ms < fastest_ms else ""
        print(f"  {get_flag(item['name'])} {i}. {item['name'][:25]:<28} → {ms}ms{marker}")
        if ms < fastest_ms:
            fastest_ms = ms
            fastest_server = item
    
    if not fastest_server:
        print(f"\n  {C.RED}❌ မည်သည့်ဆာဗာမှ အကျဉ်းမတုံ့ပြန်ပါ{C.RESET}")
        input("  ပြန်ရန် Enter နှိပ်ပါ...")
        return
    
    show_key(fastest_server, fastest_ms)

def browse_all():
    header()
    print("  📋 ဆာဗာအားလုံးကို ဖတ်နေသည်...")
    print()
    
    keys = get_keys()
    if not keys:
        print(f"  {C.RED}❌ ကီးမတွေ့ပါ။ အင်တာနက်ချိတ်ဆက်မှု စစ်ဆေးပါ။{C.RESET}")
        input("  ပြန်ရန် Enter နှိပ်ပါ...")
        return
    
    idx = 0
    while True:
        item = keys[idx]
        host, port = extract_host(item["key"])
        ms = ping_test(host, port) if host else 9999
        
        header()
        print(f"  📋 ဆာဗာ {idx+1}/{len(keys)}")
        print(f"  {get_flag(item['name'])} {item['name']}")
        if ms < 9999:
            status = f"{C.GREEN}{ms}ms{C.RESET}" if ms < 200 else f"{C.YELLOW}{ms}ms{C.RESET}" if ms < 400 else f"{C.RED}{ms}ms{C.RESET}"
            print(f"  📶 မြန်နှုန်း: {status}")
        print(f"  🔑 ကီး:\n  {C.WHITE}{item['key']}{C.RESET}")
        print()
        print(f"  {C.CYAN}[←] အရင်    {C.CYAN}[→] နောက်    {C.CYAN}[1]{C.RESET} ကူးယူ    {C.CYAN}[2]{C.RESET} သိမ်း    {C.CYAN}[Q]{C.RESET} နောက်သို့")
        
        sel = input("  ရွေးပါ: ").strip().upper()
        if sel == "Q":
            break
        elif sel == "1":
            copy_to_clipboard(item["key"])
            print(f"  {C.GREEN}✅ ကူးယူပြီးပါပြီ!{C.RESET}")
            time.sleep(0.8)
        elif sel == "2":
            save_favorite(item)
            print(f"  {C.GREEN}✅ သိမ်းပြီးပါပြီ!{C.RESET}")
            time.sleep(0.8)
        elif sel == "" or sel == "→":
            idx = (idx + 1) % len(keys)
        elif sel == "←":
            idx = (idx - 1) % len(keys)

def show_favorites():
    header()
    print("  ⭐ သင့်အကြိုက်ဆုံးများ")
    print()
    
    if not os.path.exists(FAV_FILE):
        print(f"  {C.YELLOW}အကြိုက်ဆုံး မသိမ်းရသေးပါ။{C.RESET}")
    else:
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            print(f"  {C.YELLOW}အကြိုက်ဆုံး မသိမ်းရသေးပါ။{C.RESET}")
        else:
            for i, line in enumerate(lines, 1):
                parts = line.strip().split("|", 2)
                name = parts[0] if len(parts) > 0 else "Server"
                key = parts[1] if len(parts) > 1 else ""
                t = parts[2] if len(parts) > 2 else ""
                print(f"  {C.CYAN}[{i}]{C.RESET} {get_flag(name)} {name}")
                if t:
                    print(f"     🕐 {t}")
                print(f"     🔑 {key[:50]}...")
                print()
    input("  ပြန်ရန် Enter နှိပ်ပါ...")

def main_menu():
    while True:
        header()
        print("  ⚡ [F] အကောင်းဆုံးဆာဗာကို ရှာမယ်")
        print("  🏆 [0] အမြန်ဆုံးဆာဗာကို ရှာမယ်")
        print("  📋 [B] ဆာဗာအားလုံးကို ကြည့်မယ်")
        print("  ⭐ [4] အကြိုက်ဆုံးများ")
        print("  🚪 [X] ပိတ်မည်")
        print()
        sel = input("  ရွေးပါ: ").strip().upper()
        if sel == "F":
            find_best()
        elif sel == "0":
            find_fastest()
        elif sel == "B":
            browse_all()
        elif sel == "4":
            show_favorites()
        elif sel == "X":
            print("  👋 ပျော်ရွှင်ဖွယ်ရှိပါစေ!")
            break

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n  👋 ပျော်ရွှင်ဖွယ်ရှိပါစေ!")
