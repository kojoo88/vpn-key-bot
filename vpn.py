#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, urllib.error, base64, os, socket, time, json, sys
from datetime import datetime

VERSION = "v8.9 FAST EDITION"
FAV_FILE = os.path.expanduser("~/.vpn_fast.json")
FACEBOOK_LINK = "https://www.facebook.com/share/18jrazYpmS/"

class C:
    GOLD = "\033[38;5;220m"
    CYAN = "\033[38;5;51m"
    GREEN = "\033[38;5;46m"
    YELLOW = "\033[38;5;226m"
    RED = "\033[38;5;196m"
    BLUE = "\033[38;5;39m"
    GRAY = "\033[38;5;245m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

def clear(): os.system("clear")

def header():
    clear()
    now = datetime.now()
    print(f"""{C.GOLD}{C.BOLD}
╔══════════════════════════════════════════════════════════╗
║     ✨  U L T R A   P R E M I U M   E D I T I O N        ║
║               {VERSION:^46}               ║
╠══════════════════════════════════════════════════════════╣
║   ⚡ Fast VPN Key Finder • VLESS / SS / VMESS / TROJAN    ║
║   🔰 Fast Scan Mode • Optimized for Myanmar               ║
╚══════════════════════════════════════════════════════════╝{C.RESET}""")
    print(f"  {C.GOLD}📅 Date:{C.RESET} {now.strftime('%Y-%m-%d')}   {C.GOLD}⏰ Time:{C.RESET} {now.strftime('%H:%M:%S')}")
    print(f"  {C.CYAN}📘 Share:{C.RESET} {FACEBOOK_LINK}\n")

SOURCES = [
    ("Shadowmere B64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("Shadowmere RAW", "https://shadowmere.xyz/api/sub/", "txt"),
    ("Free V2Ray ALL", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/all.txt", "txt"),
    ("Epodonios VLESS", "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/vless.txt", "txt"),
    ("Epodonios SS", "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/ss.txt", "txt"),
    ("🇸🇬 SG", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/singapore.txt", "txt"),
    ("🇲🇾 MY", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/malaysia.txt", "txt"),
    ("🇹🇭 TH", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/thailand.txt", "txt"),
]

def fetch_content(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except:
        return None

def parse_configs(content, fmt):
    configs = []
    if not content: return configs
    try:
        if fmt == "b64":
            content = base64.b64decode(content).decode("utf-8", errors="ignore")
        lines = content.strip().splitlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"): continue
            proto = ""
            if line.startswith("vless://"): proto = "VLESS"
            elif line.startswith("ss://"): proto = "SS"
            elif line.startswith("vmess://"): proto = "VMESS"
            elif line.startswith("trojan://"): proto = "TROJAN"
            if proto:
                name = ""
                if "#" in line:
                    name = line.split("#")[-1]
                    from urllib.parse import unquote
                    name = unquote(name)
                configs.append({"name": name[:40], "key": line, "proto": proto})
    except: pass
    return configs

def get_hostname(key):
    try:
        if "://" not in key: return "", ""
        rest = key.split("://", 1)[1]
        if "@" in rest: rest = rest.split("@", 1)[1]
        if ":" in rest:
            host, port = rest.rsplit(":", 1)
            if "?" in port: port = port.split("?")[0]
            return host, port
    except: pass
    return "", ""

def ping_server(host, port=443, timeout=0.5):
    if not host: return 9999
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        start = time.time()
        s.connect((host, int(port) if port else 443))
        s.close()
        return round((time.time() - start) * 1000)
    except: return 9999

def tier_text(ms):
    if ms == 9999: return f"{C.RED}❌ OFFLINE{C.RESET}"
    if ms < 60: return f"{C.GOLD}👑 ELITE  {ms}ms{C.RESET}"
    if ms < 100: return f"{C.CYAN}💎 FAST   {ms}ms{C.RESET}"
    if ms < 180: return f"{C.GREEN}⭐ GOOD   {ms}ms{C.RESET}"
    if ms < 300: return f"{C.YELLOW}⚡ OK      {ms}ms{C.RESET}"
    return f"{C.GRAY}⚠️ SLOW    {ms}ms{C.RESET}"

def load_keys():
    all_keys = []
    seen = set()
    total = len(SOURCES)
    for idx, (name, url, fmt) in enumerate(SOURCES, 1):
        print(f"  {C.BLUE}[{idx}/{total}]{C.RESET} Loading {name}...", end="\r")
        content = fetch_content(url)
        if content:
            keys = parse_configs(content, fmt)
            for k in keys:
                if k["key"] not in seen:
                    seen.add(k["key"])
                    all_keys.append(k)
    print(f"\n  {C.GREEN}✅ Loaded! Total: {len(all_keys)} servers{C.RESET}\n")
    return all_keys

def scan_top(keys, limit=15):
    print(f"  {C.YELLOW}⚡ Scanning {limit} servers...{C.RESET}\n")
    results = []
    sample = keys[:limit]
    for i, k in enumerate(sample, 1):
        host, port = get_hostname(k["key"])
        ms = ping_server(host, port)
        results.append({"name": k["name"], "key": k["key"], "proto": k["proto"], "ms": ms})
        pct = int(i / len(sample) * 100)
        bar = f"{C.GOLD}{C.BOLD}" + "█" * int(pct/10) + f"{C.RESET}{C.GRAY}" + "░" * (10 - int(pct/10)) + f"{C.RESET}"
        print(f"  [{bar}] {pct}%", end="\r")
    print("\n")
    results.sort(key=lambda x: x["ms"])
    return [r for r in results if r["ms"] < 500]

def show_top(data, title, count=5):
    if not data:
        print(f"  {C.RED}❌ No working server found{C.RESET}\n")
        input("  Press Enter to go back")
        return
    top = data[:count]
    pi = {"VLESS": "🟦", "SS": "🟩", "VMESS": "🟧", "TROJAN": "🟪"}
    
    print(f"  {C.GOLD}{C.BOLD}══════════════════════════════════════════════════════════{C.RESET}")
    print(f"  {C.GOLD}  ✅ {title}{C.RESET}")
    print(f"  {C.GOLD}{C.BOLD}══════════════════════════════════════════════════════════{C.RESET}\n")
    
    for idx, s in enumerate(top, 1):
        print(f"  {C.GOLD}{idx}.{C.RESET} {pi.get(s['proto'],'⬜')} {s['proto']} | {tier_text(s['ms'])}")
        print(f"     🔑 {C.GREEN}{s['key']}{C.RESET}\n")
    
    all_text = "\n".join([x["key"] for x in top])
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", all_text])
        print(f"  {C.GREEN}✅ Copied to clipboard!{C.RESET}\n")
    except: pass
    
    print(f"  📋 How to use: V2RayNG → + → Import from Clipboard → Connect")
    print(f"  ──────────────────────────────────────────────────────────\n")
    input("  Press Enter to return to menu")

def main():
    header()
    print(f"  {C.YELLOW}⚡ Loading sources...{C.RESET}\n")
    all_keys = load_keys()
    
    vless = [k for k in all_keys if k["proto"] == "VLESS"]
    ss = [k for k in all_keys if k["proto"] == "SS"]
    
    while True:
        header()
        print(f"  {C.GOLD}{C.BOLD}📊 STATS{C.RESET}")
        print(f"  🟦 VLESS: {len(vless):>4}  🟩 SS: {len(ss):>4}  📦 Total: {len(all_keys):>4}\n")
        print(f"  {C.GOLD}{C.BOLD}🎯 MENU{C.RESET}")
        print(f"  ┌──────────────────────────────────────────────────────┐")
        print(f"  │  [1] 🟦 VLESS Fastest 5    [2] 🟩 SS Fastest 5        │")
        print(f"  │  [3] 🏆 All Fastest 5      [4] 🔄 Reload Sources       │")
        print(f"  │  [0] ❌ Exit                                           │")
        print(f"  └──────────────────────────────────────────────────────┘\n")
        
        sel = input(f"  {C.GOLD}Choose → {C.RESET}").strip()
        
        if sel == "1":
            if not vless:
                print(f"  {C.RED}❌ No VLESS keys. Press [4] to reload.{C.RESET}\n")
                time.sleep(1)
                continue
            data = scan_top(vless)
            show_top(data, "VLESS Fastest Servers")
        
        elif sel == "2":
            if not ss:
                print(f"  {C.RED}❌ No SS keys. Press [4] to reload.{C.RESET}\n")
                time.sleep(1)
                continue
            data = scan_top(ss)
            show_top(data, "SS Fastest Servers")
        
        elif sel == "3":
            if not all_keys:
                print(f"  {C.RED}❌ No keys. Press [4] to reload.{C.RESET}\n")
                time.sleep(1)
                continue
            data = scan_top(all_keys)
            show_top(data, "Top 5 Fastest All")
        
        elif sel == "4":
            header()
            print(f"  {C.YELLOW}🔄 Reloading...{C.RESET}\n")
            all_keys = load_keys()
            vless = [k for k in all_keys if k["proto"] == "VLESS"]
            ss = [k for k in all_keys if k["proto"] == "SS"]
            input("  Done! Press Enter")
        
        elif sel == "0":
            header()
            print(f"  {C.GOLD}✨ Thanks for using! ✨{C.RESET}")
            break
        
        else:
            print(f"  {C.RED}❌ Invalid choice 0-4 only{C.RESET}\n")
            time.sleep(0.8)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        header()
        print(f"  {C.GOLD}👑 Exited{C.RESET}\n")
    except Exception as e:
        print(f"  {C.RED}Error: {e}{C.RESET}\n")
        input("  Press Enter")
    
