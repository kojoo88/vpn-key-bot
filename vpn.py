#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, base64, os

VERSION = "v9.6 CLEAN — 2 Sources Only"

class C:
    G = "\033[92m"
    B = "\033[94m"
    Y = "\033[93m"
    R = "\033[91m"
    CY = "\033[96m"
    RS = "\033[0m"
    BD = "\033[1m"

def clear(): os.system("clear")

def header():
    clear()
    print(f"""{C.CY}{C.BD}
╔══════════════════════════════════════════════════════╗
║     🚀  VPN KEY FINDER  —  {VERSION:^30}║
║     ✅ 2 Working Sources Only • Clean • Fast         ║
╚══════════════════════════════════════════════════════╝{C.RS}""")

# ✅ အလုပ်လုပ်နေတဲ့ နှစ်ခုသာ
SOURCES = [
    ("Shadowmere B64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("Argh73 Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
]

def get_text(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except:
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

def main():
    header()
    all_keys = []
    seen = set()
    
    print(f"\n{C.Y}🔍 စစ်ဆေးနေသည်...{C.RS}\n")
    
    for name, url, fmt in SOURCES:
        print(f"  → {name} ...", end="\r")
        text = get_text(url)
        ks = parse(text, fmt)
        if ks:
            for k in ks:
                if k["key"] not in seen:
                    seen.add(k["key"])
                    all_keys.append(k)
            print(f"  {C.G}✅ {name} — {len(ks)} keys{C.RS}")
        else:
            print(f"  {C.R}❌ {name} — မရရှိ{C.RS}")
    
    print(f"\n{C.G}{C.BD}══════════════════════════════════════════════════════{C.RS}")
    print(f"{C.G}✅ စုစုပေါင်း ကီး {len(all_keys)} ခု ရရှိပြီးသား{C.RS}")
    print(f"{C.G}{C.BD}══════════════════════════════════════════════════════{C.RS}\n")
    
    while True:
        print(f"{C.B}📌 မီနူး{C.RS}")
        print("  1. အားလုံးပြပါ")
        print("  2. VLESS သီးသန့်ပြပါ")
        print("  3. SS သီးသန့်ပြပါ")
        print("  4. Subscribe လင့်ခ်များပြပါ")
        print("  0. ထွက်ပါ")
        
        choice = input("\nရွေးပါ → ").strip()
        
        if choice == "0":
            print(f"{C.CY}👋 ပါသေး...{C.RS}")
            break
        elif choice == "1":
            show(all_keys)
        elif choice == "2":
            show([k for k in all_keys if k["proto"] == "VLESS"])
        elif choice == "3":
            show([k for k in all_keys if k["proto"] == "SS"])
        elif choice == "4":
            print(f"\n{C.G}✅ Subscribe လင့်ခ်များ{C.RS}")
            for name, url, _ in SOURCES:
                print(f"  {name}: {url}")
            input("\nပြန်ရန် Enter နှိပ်ပါ\n")
        else:
            print(f"{C.R}❌ မှားနေပါတယ်{C.RS}\n")

def show(keys):
    if not keys:
        print(f"{C.R}❌ မတွေ့ပါ{C.RS}\n")
        return
    print(f"\n{C.G}✅ ကီး {len(keys)} ခု{RS}\n")
    for i, k in enumerate(keys[:10], 1):
        print(f"  {i}. {k['proto']} | {k['name'][:40]}")
        print(f"     {k['key']}\n")
    if len(keys) > 10:
        print(f"... နောက်ထပ် {len(keys)-10} ခု ရှိပါသည်\n")
    input("ပြန်ရန် Enter နှိပ်ပါ\n")

if __name__ == "__main__":
    main()
              
