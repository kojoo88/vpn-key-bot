#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, urllib.error, base64, os, socket, time, sys

VERSION = "v9.0 SIMPLE & FAST"

class C:
    G = "\033[92m"
    B = "\033[94m"
    Y = "\033[93m"
    R = "\033[91m"
    CY = "\033[96m"
    WT = "\033[97m"
    RS = "\033[0m"
    BD = "\033[1m"

def clear(): os.system("clear")

def header():
    clear()
    print(f"""{C.BD}{C.CY}
╔══════════════════════════════════════════════════════╗
║     🚀  VPN KEY FINDER  —  {VERSION:^30}║
║     Simple • Fast • Reliable                          ║
╚══════════════════════════════════════════════════════╝{C.RS}""")

# ✅ အလုပ်လုပ်နေတဲ့ လင့်ခ်များသာ ထည့်ထားသည်
SOURCES = [
    ("Shadowmere B64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("Shadowmere TXT", "https://shadowmere.xyz/api/sub/", "txt"),
    ("Epodonios VLESS", "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/vless.txt", "txt"),
    ("Epodonios SS", "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/ss.txt", "txt"),
    ("FreeV2Ray All", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/all.txt", "txt"),
]

def get(url, timeout=12):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  {C.R}✗ Failed:{C.RS} {url[:40]}...")
        return None

def parse(text, fmt):
    keys = []
    if not text: return keys
    try:
        if fmt == "b64":
            text = base64.b64decode(text).decode("utf-8", errors="ignore")
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"): continue
            proto = None
            if line.startswith("vless://"): proto = "VLESS"
            elif line.startswith("ss://"): proto = "SS"
            elif line.startswith("vmess://"): proto = "VMESS"
            elif line.startswith("trojan://"): proto = "TROJAN"
            if proto:
                name = "Server"
                if "#" in line:
                    name = line.split("#")[-1]
                    try:
                        from urllib.parse import unquote
                        name = unquote(name)
                    except: pass
                keys.append({"proto": proto, "name": name, "key": line})
    except: pass
    return keys

def load_all():
    all_keys = []
    seen = set()
    print(f"  {C.Y}🔄 Loading sources...{C.RS}\n")
    for name, url, fmt in SOURCES:
        print(f"  {C.B}→ {name}{C.RS}")
        text = get(url)
        ks = parse(text, fmt)
        for k in ks:
            if k["key"] not in seen:
                seen.add(k["key"])
                all_keys.append(k)
        if ks:
            print(f"     {C.G}✓ Found {len(ks)} keys{C.RS}\n")
        else:
            print(f"     {C.R}✗ No keys found{C.RS}\n")
    return all_keys

def show(keys, proto_filter=None):
    if proto_filter:
        keys = [k for k in keys if k["proto"] == proto_filter]
    if not keys:
        print(f"  {C.R}❌ No keys found!{C.RS}")
        print(f"  {C.Y}💡 Try option [4] to reload{C.RS}\n")
        input("  Press Enter")
        return
    
    print(f"  {C.G}{C.BD}══════════════════════════════════════════════════════{C.RS}")
    print(f"  {C.G}✅ Found {len(keys)} keys! Showing first 5{C.RS}")
    print(f"  {C.G}{C.BD}══════════════════════════════════════════════════════{C.RS}\n")
    
    icons = {"VLESS": "🟦", "SS": "🟩", "VMESS": "🟧", "TROJAN": "🟪"}
    top5 = keys[:5]
    
    for i, k in enumerate(top5, 1):
        print(f"  {C.BD}{i}.{C.RS} {icons.get(k['proto'],'⬜')} {k['proto']} — {k['name'][:40]}")
        print(f"     {C.CY}{k['key']}{C.RS}\n")
    
    all_text = "\n".join([k["key"] for k in top5])
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", all_text])
        print(f"  {C.G}✅ First 5 keys copied to clipboard!{C.RS}\n")
    except:
        pass
    
    print(f"  📱 How to use: V2RayNG → + → Import from Clipboard → Connect")
    print(f"  ──────────────────────────────────────────────────────────\n")
    input("  Press Enter to go back")

def main():
    header()
    keys = load_all()
    print(f"  {C.G}{C.BD}✅ Total unique keys: {len(keys)}{C.RS}\n")
    time.sleep(1)
    
    while True:
        header()
        vless = [k for k in keys if k["proto"] == "VLESS"]
        ss = [k for k in keys if k["proto"] == "SS"]
        
        print(f"  {C.BD}{C.WT}📊 Stats{C.RS}")
        print(f"  🟦 VLESS: {len(vless)}  |  🟩 SS: {len(ss)}  |  📦 Total: {len(keys)}\n")
        
        print(f"  {C.BD}{C.WT}🎯 Menu{C.RS}")
        print(f"  ┌──────────────────────────────────────────────────────┐")
        print(f"  │  [1] 🟦 Show VLESS Keys    [2] 🟩 Show SS Keys          │")
        print(f"  │  [3] 📋 Show All Keys       [4] 🔄 Reload All          │")
        print(f"  │  [0] ❌ Exit                                           │")
        print(f"  └──────────────────────────────────────────────────────┘\n")
        
        sel = input(f"  {C.BD}Choose → {C.RS}").strip()
        
        if sel == "1":
            show(keys, "VLESS")
        elif sel == "2":
            show(keys, "SS")
        elif sel == "3":
            show(keys)
        elif sel == "4":
            header()
            keys = load_all()
            print(f"  {C.G}✅ Reloaded! Total keys: {len(keys)}{C.RS}\n")
            input("  Press Enter")
        elif sel == "0":
            print(f"\n  {C.G}👋 Goodbye!{C.RS}")
            break
        else:
            print(f"  {C.R}❌ Invalid option{C.RS}\n")
            time.sleep(1)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        print(f"\n  {C.Y}⚠️ Stopped by user{C.RS}\n")
    except Exception as e:
        print(f"\n  {C.R}❌ Error: {e}{C.RS}\n")
        input("  Press Enter")
                
