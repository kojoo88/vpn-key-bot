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

VERSION = "5.3 ✨ PREMIUM"
FAV_FILE = os.path.join(os.path.expanduser("~"), "vpn-key-bot", "favorites.txt")

class Colors:
    P = "\033[95m"
    C = "\033[96m"
    G = "\033[92m"
    Y = "\033[93m"
    R = "\033[91m"
    W = "\033[97m"
    D = "\033[90m"
    rst = "\033[0m"

C = Colors()

API_LIST = {
    "1": ("Shadowmere JSON", "https://shadowmere.xyz/api/sub/", "json"),
    "2": ("Shadowmere Base64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    "3": ("VLESS List", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vless.txt", "txt")
}

NEARBY_COUNTRIES = [
    "singapore", "malaysia", "thailand", "vietnam",
    "indonesia", "philippines", "hong kong", "hongkong",
    "japan", "korea", "india", "australia"
]

def clear():
    os.system("clear")

def header():
    clear()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{C.P}{'='*58}{C.rst}")
    print(f"{C.P}║{C.rst}  ✨ VPN KEY GENERATOR  {VERSION}")
    print(f"{C.P}╠{'═'*56}╣{C.rst}")
    print(f"{C.P}║{C.rst}  📡 Status: Online  |  🕐 {now}")
    print(f"{C.P}{'='*58}{C.rst}\n")

def divider(title=""):
    if title:
        print(f"{C.C}--- {title} {'-'*(50-len(title))}{C.rst}")
    else:
        print(f"{C.D}{'-'*52}{C.rst}")

def get_flag_emoji(name):
    name = name.lower()
    flags = {
        "singapore": "🇸🇬", "malaysia": "🇲🇾", "thailand": "🇹🇭",
        "vietnam": "🇻🇳", "indonesia": "🇮🇩", "philippines": "🇵🇭",
        "hongkong": "🇭🇰", "hong kong": "🇭🇰", "japan": "🇯🇵",
        "korea": "🇰🇷", "india": "🇮🇳", "australia": "🇦🇺",
        "germany": "🇩🇪", "finland": "🇫🇮", "usa": "🇺🇸",
        "united states": "🇺🇸", "uk": "🇬🇧", "russia": "🇷🇺"
    }
    for k, v in flags.items():
        if k in name:
            return v
    return "🌐"

def get_uptime_percent(ping_ms):
    if ping_ms < 100:
        return 100, f"{C.G}⚡ 100%{C.rst}"
    elif ping_ms < 150:
        return 90, f"{C.G}⚡ 90%{C.rst}"
    elif ping_ms < 200:
        return 75, f"{C.Y}⚡ 75%{C.rst}"
    elif ping_ms < 300:
        return 50, f"{C.Y}⚡ 50%{C.rst}"
    else:
        return 25, f"{C.R}⚡ 25%{C.rst}"

def test_ping(host, port=443, timeout=2):
    try:
        ip = socket.gethostbyname(host)
        start = time.time()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, int(port)))
        s.close()
        ms = round((time.time() - start) * 1000)
        if ms < 100:
            return ms, f"{C.G}🟢 {ms}ms{C.rst}"
        elif ms < 250:
            return ms, f"{C.Y}🟡 {ms}ms{C.rst}"
        else:
            return ms, f"{C.R}🔴 {ms}ms{C.rst}"
    except:
        return 9999, f"{C.R}❌ Timeout{C.rst}"

def extract_host_port(key):
    try:
        if "://" in key:
            from urllib.parse import urlparse
            p = urlparse(key)
            return p.hostname or "", p.port or 443
    except:
        return "", 443

def get_country_priority(name):
    name = name.lower()
    for idx, country in enumerate(NEARBY_COUNTRIES):
        if country in name:
            return 100 - (idx * 5)
    return 30

def calculate_score(ping_ms, country_priority, uptime_pct):
    ping_score = max(0, 100 - ping_ms // 2)
    return int((country_priority * 0.5) + (ping_score * 0.35) + (uptime_pct * 0.15))

def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"  {C.R}❌ Error: {str(e)[:40]}{C.rst}")
        return None

def fetch_b64(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return base64.b64decode(r.read()).decode().splitlines()
    except Exception as e:
        print(f"  {C.R}❌ Error: {str(e)[:40]}{C.rst}")
        return None

def fetch_txt(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode().splitlines()
    except Exception as e:
        print(f"  {C.R}❌ Error: {str(e)[:40]}{C.rst}")
        return None

def parse_key_info(key):
    if not key or len(key) < 10:
        return None, None
    name = "Server"
    if "#" in key:
        try:
            from urllib.parse import unquote
            name = unquote(key.split("#")[-1])
        except:
            pass
    return name, key

def get_all_keys():
    all_keys = []
    for sid in ["1", "2", "3"]:
        name, url, dtype = API_LIST[sid]
        data = None
        if dtype == "json":
            data = fetch_json(url)
            if data and isinstance(data, list):
                for item in data:
                    k = item.get("url") or item.get("link") or ""
                    n = item.get("name") or item.get("remarks") or "Server"
                    if k and ("vless://" in k or "ss://" in k):
                        all_keys.append({"name": n, "key": k, "source": name})
        elif dtype == "b64":
            lines = fetch_b64(url)
            if lines:
                for line in lines:
                    n, k = parse_key_info(line.strip())
                    if k:
                        all_keys.append({"name": n, "key": k, "source": name})
        elif dtype == "txt":
            lines = fetch_txt(url)
            if lines:
                for line in lines:
                    n, k = parse_key_info(line.strip())
                    if k:
                        all_keys.append({"name": n, "key": k, "source": name})
    return all_keys

def show_result(item, ping_ms, ping_str):
    fetched_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _, uptime_str = get_uptime_percent(ping_ms)
    flag = get_flag_emoji(item["name"])
    
    divider(f"{flag} {item['name']}")
    print(f"  📌 Source: {item['source']}")
    print(f"  ⚡ Status: {uptime_str}")
    print(f"  📶 Ping: {ping_str}")
    print(f"  🕐 Fetched: {fetched_time}")
    divider()
    print(f"  🔑 Key:\n  {C.W}{item['key']}{C.rst}\n")
    print(f"  {C.C}[1]{C.rst} Copy Key    {C.C}[2]{C.rst} Save to Favorites    {C.C}[Q]{C.rst} Back")
    
    sel = input("  Choose: ").strip().upper()
    if sel == "1":
        try:
            import subprocess
            subprocess.run(["termux-clipboard-set", item["key"]])
            print(f"  {C.G}✅ Copied to clipboard!{C.rst}")
        except:
            print(f"  Key: {item['key']}")
    elif sel == "2":
        try:
            os.makedirs(os.path.dirname(FAV_FILE), exist_ok=True)
            with open(FAV_FILE, "a", encoding="utf-8") as f:
                f.write(f"{item['name']}|{item['key']}|{ping_str}|{fetched_time}\n")
            print(f"  {C.G}✅ Saved!{C.rst}")
        except Exception as e:
            print(f"  {C.R}❌ Save failed: {e}{C.rst}")
    input("\n  Press Enter to continue...")

def find_best_for_me():
    header()
    print(f"  🎯 Finding best for your connection...")
    print(f"  📍 Prioritizing: SG > MY > TH > VN > ID > PH > HK > JP > KR > IN > AU\n")
    
    all_keys = get_all_keys()
    if not all_keys:
        input(f"  {C.R}No keys found. Press Enter...{C.rst}")
        return
    
    scored = []
    print(f"  Testing {len(all_keys)} servers...\n")
    
    for idx, item in enumerate(all_keys, 1):
        host, port = extract_host_port(item["key"])
        if not host:
            continue
        flag = get_flag_emoji(item["name"])
        print(f"  {flag} {idx}/{len(all_keys)}: {item['name'][:25]}...", end=" ")
        
        ping_ms, ping_str = test_ping(host, port, timeout=1.5)
        uptime_pct, _ = get_uptime_percent(ping_ms)
        country_prio = get_country_priority(item["name"])
        score = calculate_score(ping_ms, country_prio, uptime_pct)
        
        scored.append({**item, "ping_ms": ping_ms, "ping_str": ping_str, "score": score})
        print(f"Score: {score}/100")
    
    if not scored:
        input(f"\n  {C.R}No working server found. Press Enter...{C.rst}")
        return
    
    scored.sort(key=lambda x: x["score"], reverse=True)
    best = scored[0]
    
    print(f"\n{C.G}{'='*58}{C.rst}")
    print(f"{C.G}  🎯 BEST MATCH FOUND! Score: {best['score']}/100{C.rst}")
    print(f"{C.G}{'='*58}{C.rst}\n")
    
    show_result(best, best["ping_ms"], best["ping_str"])

def find_fastest():
    header()
    print(f"  🏆 Finding fastest server...\n")
    
    all_keys = get_all_keys()
    if not all_keys:
        input(f"  {C.R}No keys found. Press Enter...{C.rst}")
        return
    
    best_ping = 9999
    best_server = None
    
    for idx, item in enumerate(all_keys, 1):
        host, port = extract_host_port(item["key"])
        if not host:
            continue
        flag = get_flag_emoji(item["name"])
        print(f"  {flag} {idx}/{len(all_keys)}: {item['name'][:25]}...", end=" ")
        
        ping_ms, ping_str = test_ping(host, port, timeout=1.5)
        
        if ping_ms < best_ping:
            best_ping = ping_ms
            best_server = item
            print(f"{C.G}NEW BEST! {ping_str}{C.rst}")
        else:
            print(ping_str)
    
    if not best_server:
        input(f"\n  {C.R}No working server found. Press Enter...{C.rst}")
        return
    
    print(f"\n{C.G}{'='*58}{C.rst}")
    print(f"{C.G}  🏆 FASTEST SERVER FOUND!{C.rst}")
    print(f"{C.G}{'='*58}{C.rst}\n")
    
    show_result(best_server, best_ping, test_ping(extract_host_port(best_server["key"])[0])[1])

def browse_all():
    header()
    print(f"  📋 Loading all keys...\n")
    
    all_keys = get_all_keys()
    if not all_keys:
        input(f"  {C.R}No keys found. Press Enter...{C.rst}")
        return
    
    idx = 0
    while True:
        item = all_keys[idx]
        fetched_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        flag = get_flag_emoji(item["name"])
        host, port = extract_host_port(item["key"])
        ping_ms, ping_str = test_ping(host, port, timeout=2)
        _, uptime_str = get_uptime_percent(ping_ms)
        
        header()
        divider(f"{flag} Server {idx+1}/{len(all_keys)}")
        print(f"  📛 Name: {item['name']}")
        print(f"  📌 Source: {item['source']}")
        print(f"  ⚡ Status: {uptime_str}")
        print(f"  📶 Ping: {ping_str}")
        print(f"  🕐 Fetched: {fetched_time}")
        divider()
        print(f"  🔑 Key:\n  {C.W}{item['key']}{C.rst}\n")
        print(f"  {C.C}[←] Previous    {C.C}[→] Next    {C.C}[1]{C.rst} Copy    {C.C}[Q]{C.rst} Back")
        
        sel = input("  Choose: ").strip().upper()
        if sel == "Q":
            break
        elif sel == "1":
            try:
                import subprocess
                subprocess.run(["termux-clipboard-set", item["key"]])
                print(f"  {C.G}✅ Copied!{C.rst}")
                time.sleep(1)
            except:
                print(f"  Key: {item['key']}")
                input("  Press Enter...")
        elif sel == "" or sel == "→":
            idx = (idx + 1) % len(all_keys)
        elif sel == "←":
            idx = (idx - 1) % len(all_keys)

def show_favorites():
    header()
    print(f"  ⭐ Your Favorites\n")
    
    if not os.path.exists(FAV_FILE):
        print(f"  {C.D}No favorites yet.{C.rst}")
    else:
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            print(f"  {C.D}No favorites yet.{C.rst}")
        else:
            for i, line in enumerate(lines, 1):
                parts = line.strip().split("|", 3)
                name = parts[0] if len(parts)>0 else "Server"
                key = parts[1] if len(parts)>1 else ""
                ping = parts[2] if len(parts)>2 else ""
                t = parts[3] if len(parts)>3 else ""
                flag = get_flag_emoji(name)
                print(f"  {C.C}[{i}]{C.rst} {flag} {name}")
                if ping:
                    print(f"     📶 {ping}")
                if t:
                    print(f"     🕐 {t}")
                print()
    input("  Press Enter to go back...")

def main_menu():
    while True:
        header()
        print(f"  🎯 [M] Best for ME  — Auto match")
        print(f"  🏆 [0] Fastest only")
        print(f"  📋 [B] Browse all servers")
        print(f"  ⭐ [4] My Favorites")
        print(f"  🚪 [9] Exit\n")
        
        sel = input("  Select: ").strip().upper()
        if sel == "M":
            find_best_for_me()
        elif sel == "0":
            find_fastest()
        elif sel == "B":
            browse_all()
        elif sel == "4":
            show_favorites()
        elif sel == "9":
            print(f"  {C.G}👋 Bye!{C.rst}")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n  {C.Y}Exited.{C.rst}")
        sys.exit(0)
    
