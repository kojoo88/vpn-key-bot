#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, urllib.error, base64, os, time, sys

VERSION = "v9.1 WORKING SOURCES ONLY"

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
    print(f"""{C.CY}{C.BD}
╔══════════════════════════════════════════════════════╗
║     🚀  VPN KEY FINDER  —  {VERSION:^30}║
║     ✅ Working Sources Only • Fast • Reliable          ║
╚══════════════════════════════════════════════════════╝{C.RS}""")

# ==============================================================
# ✅ အလုပ်လုပ်နေတဲ့ လင့်ခ်များသာ ထည့်ထားသည်
# ==============================================================
SOURCES = [
    # 🏆 အကောင်းဆုံး အလုပ်လုပ်နေသည်
    ("Shadowmere B64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("Shadowmere TXT", "https://shadowmere.xyz/api/sub/", "txt"),
    
    # 🌍 အခြားအလုပ်လုပ်နေသည့် အရင်းအမြစ်များ
    ("V2Ray Seeker ALL", "https://raw.githubusercontent.com/v2ray-seeker/v2rayseeker/main/sub.txt", "txt"),
    ("Awesome VPN Daily", "https://raw.githubusercontent.com/awesome-vpn/awesome-vpn/master/all", "txt"),
    ("IRCF Space", "https://raw.githubusercontent.com/ircfspace/ircf.github.io/main/configs.txt", "txt"),
    ("TGParse Mixed", "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/splitted/mixed", "txt"),
    ("Argh73 Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
    ("V2Ray Pool ALL", "https://raw.githubusercontent.com/v2ray-pool/v2ray-pool/main/sub.txt", "txt"),
    
    # 🇸🇬 အာရှဆာဗာများ
    ("🇸🇬 SG Servers", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/singapore.txt", "txt"),
    ("🇲🇾 MY Servers", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/malaysia.txt", "txt"),
    ("🇹🇭 TH Servers", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/thailand.txt", "txt"),
]

def get(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
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
    working = 0
    total = len(SOURCES)
    print(f"  {C.Y}🔄 Checking {total} sources...{C.RS}\n")
    
    for idx, (name, url, fmt) in enumerate(SOURCES, 1):
        print(f"  {C.B}[{idx}/{total}]{C.RS} → {name}", end="\r")
        text = get(url)
        if text:
            ks = parse(text, fmt)
            if ks:
                working += 1
                for k in ks:
                    if k["key"] not in seen:
                        seen.add(k["key"])
                        all_keys.append(k)
                print(f"  {C.G}✓ {name} — {len(ks)} keys{C.RS}")
            else:
                print(f"  {C.Y}⚠ {name} — No keys{C.RS}")
        else:
            print(f"  {C.R}✗ {name} — Offline{C.RS}")
    
    print(f"\n  {C.G}{C.BD}✅ Done! Working: {working}/{total} | Total Keys: {len(all_keys)}{C.RS}\n")
    return all_keys

def show(keys, proto_filter=None):
    if proto_filter:
        keys = [k for k in keys if k["proto"] == proto_filter]
    if not keys:
        print(f"  {C.R}❌ No keys found!{C.RS}")
        print(f"  {C.Y}💡 Try option [4] to reload{C.RS}\n")
        input("  Press Enter")
        return
    
    icons = {"VLESS": "🟦", "SS": "🟩", "VMESS": "🟧", "TROJAN": "🟪"}
    top5 = keys[:5]
    
    print(f"  {C.G}{C.BD}══════════════════════════════════════════════════════{C.RS}")
    print(f"  {C.G}✅ Showing first {min(5, len(keys))} of {len(keys)} keys{C.RS}")
    print(f"  {C.G}{C.BD}══════════════════════════════════════════════════════{C.RS}\n")
    
    for i, k in enumerate(top5, 1):
        print(f"  {C.BD}{i}.{C.RS} {icons.get(k['proto'],'⬜')} {k['proto']} — {k['name'][:50]}")
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
    
    while True:
        header()
        vless = [k for k in keys if k["proto"] == "VLESS"]
        ss = [k for k in keys if k["proto"] == "SS"]
        vmess = [k for k in keys if k["proto"] == "VMESS"]
        trojan = [k for k in keys if k["proto"] == "TROJAN"]
        
        print(f"  {C.BD}{C.WT}📊 STATISTICS{C.RS}")
        print(f"  🟦 VLESS: {len(vless):>4}  🟩 SS: {len(ss):>4}  🟧 VMESS: {len(vmess):>4}  🟪 TROJAN: {len(trojan):>4}")
        print(f"  📦 TOTAL: {len(keys)} keys\n")
        
        print(f"  {C.BD}{C.WT}🎯 MAIN MENU{C.RS}")
        print(f"  ┌──────────────────────────────────────────────────────────────┐")
        print(f"  │  [1] 🟦 Show VLESS Keys    [2] 🟩 Show SS Keys                │")
        print(f"  │  [3] 📋 Show All Keys       [4] 🔄 Reload All Sources         │")
        print(f"  │  [0] ❌ Exit                                                  │")
        print(f"  └──────────────────────────────────────────────────────────────┘\n")
        
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
            input("  Press Enter")
        elif sel == "0":
            print(f"\n  {C.G}👋 Thanks for using! Goodbye!{C.RS}")
            break
        else:
            print(f"  {C.R}❌ Invalid option. Choose 0-4{C.RS}\n")
            time.sleep(1)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        print(f"\n  {C.Y}⚠️ Stopped by user{C.RS}\n")
    except Exception as e:
        print(f"\n  {C.R}❌ Error: {e}{C.RS}\n")
        input("  Press Enter")
                           
