#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, base64, os, time, re
import socket

VERSION = "v1.0 PREMIUM EDITION"

# 🎨 အရောင်များ
class C:
    G = "\033[92m"    # အစိမ်း
    B = "\033[94m"    # အပြာ
    Y = "\033[93m"    # အဝါ
    R = "\033[91m"    # အနီ
    CY = "\033[96m"   # အပြာဖျော့
    M = "\033[95m"    # ခရမ်းရောင်
    W = "\033[97m"    # အဖြူ
    BD = "\033[1m"    # ထူ
    UL = "\033[4m"    # မျဉ်းကြောင်း
    RS = "\033[0m"    # ပုံမှန်

def clear():
    os.system("clear")

# 🚀 ခေါင်းစဉ်
def header():
    clear()
    print(f"""{C.M}{C.BD}
╔══════════════════════════════════════════════════════════════╗
║   🚀  V P N   K E Y   F I N D E R        {C.CY}{VERSION}         {C.M}║
║   ═══════════════════════════════════════════════════════════  ║
║   ✅ Shadowmere B64  •  ⚡ Fast Ping  •  📊 Server Quality    ║
╚══════════════════════════════════════════════════════════════╝{C.RS}""")

# ✅ အလုပ်လုပ်နေတဲ့ အရင်းအမြစ်
SOURCES = [
    ("Shadowmere B64", "https://shadowmere.xyz/api/b64sub/", "b64"),
]

# ⚡ Ping စစ်ဆေးခြင်း
def ping_server(host, port, timeout=2):
    try:
        start = time.time()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, int(port)))
        ms = int((time.time() - start) * 1000)
        if ms < 100:
            return f"{C.G}{ms} ms ✅ အလွန်မြန်{C.RS}", ms
        elif ms < 200:
            return f"{C.Y}{ms} ms ⚡ ကောင်းမွန်{C.RS}", ms
        elif ms < 400:
            return f"{C.B}{ms} ms 📍 ပုံမှန်{C.RS}", ms
        else:
            return f"{C.R}{ms} ms ⚠️ နှေး{C.RS}", ms
    except:
        return f"{C.R}❌ ချိတ်ဆက်မရှိ{C.RS}", 9999

# 🔗 Host နှင့် Port ကို ထုတ်ယူခြင်း
def extract_host_port(key):
    try:
        if key.startswith("ss://"):
            match = re.search(r"@([^:]+):(\d+)", key)
            if match:
                return match.group(1), match.group(2)
        elif key.startswith("vless://"):
            match = re.search(r"@([^:]+):(\d+)", key)
            if match:
                return match.group(1), match.group(2)
    except:
        pass
    return None, None

# 📡 ဒေတာဖတ်ခြင်း
def get_text(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", errors="ignore")
    except:
        return None

# 🔑 ကီးများဖြတ်ထုတ်ခြင်း
def parse(text, fmt):
    keys = []
    if not text:
        return keys
    try:
        if fmt == "b64":
            text = base64.b64decode(text).decode("utf-8", errors="ignore")
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            proto = None
            if line.startswith("vless://"):
                proto = "VLESS"
            elif line.startswith("ss://"):
                proto = "SS"
            elif line.startswith("vmess://"):
                proto = "VMESS"
            elif line.startswith("trojan://"):
                proto = "TROJAN"
            if proto:
                name = "Unknown Server"
                if "#" in line:
                    name = line.split("#")[-1]
                    try:
                        from urllib.parse import unquote
                        name = unquote(name)
                    except:
                        pass
                keys.append({"proto": proto, "name": name, "key": line})
    except:
        pass
    return keys

# 📋 ကီးများပြသခြင်း
def show_keys(keys, show_ping=False):
    if not keys:
        print(f"\n{C.R}❌ ကီးမတွေ့ရှိပါ{C.RS}\n")
        input(f"{C.Y}ပြန်ရန် Enter နှိပ်ပါ → {C.RS}")
        return
    
    print(f"\n{C.G}{C.BD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RS}")
    print(f"{C.G}✅ စုစုပေါင်း ကီး {len(keys)} ခု တွေ့ရှိပြီးသား{C.RS}")
    print(f"{C.G}{C.BD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RS}\n")
    
    display_count = min(10, len(keys))
    results = []
    
    for i, k in enumerate(keys[:display_count], 1):
        ping_info = ""
        ping_ms = 9999
        if show_ping:
            host, port = extract_host_port(k["key"])
            if host and port:
                print(f"  ⏳ စစ်ဆေးနေသည်... [{i}/{display_count}]", end="\r")
                ping_info, ping_ms = ping_server(host, port)
        
        results.append({"index": i, "ping_ms": ping_ms, "data": k})
        
        print(f"  {C.BD}{str(i).zfill(2)}{C.RS} ｜ {k['proto']:6} ｜ {k['name'][:35]}")
        if show_ping:
            print(f"       ⚡ Ping: {ping_info}")
        print(f"       🔑 {C.CY}{k['key']}{C.RS}\n")
    
    if len(keys) > display_count:
        print(f"{C.Y}... နောက်ထပ် {len(keys)-display_count} ခု ကျန်ရှိနေပါသည်{C.RS}\n")
    
    return results

# 🏆 အကောင်းဆုံးဆာဗာရွေးချယ်ခြင်း
def find_best_server(keys):
    if not keys:
        print(f"\n{C.R}❌ ကီးမရှိပါ{C.RS}\n")
        input(f"{C.Y}ပြန်ရန် Enter နှိပ်ပါ → {C.RS}")
        return
    
    print(f"\n{C.M}{C.BD}🏆 သင့်အတွက် အကောင်းဆုံးဆာဗာကို ရှာဖွေနေသည်...{C.RS}\n")
    
    tested = []
    for i, k in enumerate(keys):
        host, port = extract_host_port(k["key"])
        if host and port:
            print(f"  စစ်ဆေးနေသည်... [{i+1}/{len(keys)}] {k['name'][:25]}", end="\r")
            _, ms = ping_server(host, port, timeout=1.5)
            tested.append({"ms": ms, "data": k})
    
    if not tested:
        print(f"\n{C.R}❌ စစ်ဆေး၍မရပါ{C.RS}\n")
        return
    
    tested.sort(key=lambda x: x["ms"])
    best = tested[0]
    
    print(f"\n\n{C.G}{C.BD}🏆 အကောင်းဆုံး ဆာဗာ တွေ့ရှိပါသည်!{C.RS}")
    print(f"{C.G}{C.BD}═══════════════════════════════════════════════{C.RS}")
    print(f"   📌 အမည်: {best['data']['name']}")
    print(f"   🌐 အမျိုးအစား: {best['data']['proto']}")
    print(f"   ⚡ အနိမ့်ဆုံး Ping: {best['ms']} ms")
    print(f"   🔑 ကီး: {C.CY}{best['data']['key']}{C.RS}")
    print(f"{C.G}{C.BD}═══════════════════════════════════════════════{C.RS}\n")
    
    input(f"{C.Y}ပြန်ရန် Enter နှိပ်ပါ → {C.RS}")

# 📄 Subscribe လင့်ခ်များပြသခြင်း
def show_sub_links():
    print(f"\n{C.CY}{C.BD}📡 Subscribe လင့်ခ်များ{C.RS}")
    print(f"{C.CY}{C.BD}═══════════════════════════════════════════════{C.RS}\n")
    for name, url, _ in SOURCES:
        print(f"   ✅ {name}")
        print(f"   🔗 {C.W}{url}{C.RS}\n")
    print(f"{C.Y}💡 အသုံးပြုနည်း- V2RayNG/NekoBox → + → Subscribe → URL ကူးထည့် → Refresh{C.RS}\n")
    input(f"{C.Y}ပြန်ရန် Enter နှိပ်ပါ → {C.RS}")

# 🚀 အဓိကလုပ်ဆောင်ချက်
def main():
    header()
    all_keys = []
    seen = set()
    
    print(f"\n{C.Y}🔍 အရင်းအမြစ်များကို စစ်ဆေးနေသည်...{C.RS}\n")
    
    for name, url, fmt in SOURCES:
        print(f"  ⏳ {name} ကို ဖတ်နေသည်...", end="\r")
        text = get_text(url)
        ks = parse(text, fmt)
        if ks:
            for k in ks:
                if k["key"] not in seen:
                    seen.add(k["key"])
                    all_keys.append(k)
            print(f"  {C.G}✅ {name} — {len(ks)} ကီး ရရှိ{C.RS}")
        else:
            print(f"  {C.R}❌ {name} — မရရှိ{C.RS}")
    
    print(f"\n{C.G}{C.BD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RS}")
    print(f"{C.CY}📊 စုစုပေါင်း ကီး အရေအတွက်: {C.G}{len(all_keys)}{C.CY} ခု{C.RS}")
    print(f"{C.G}{C.BD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RS}\n")
    
    # 📌 မီနူး
    while True:
        print(f"{C.M}{C.BD}📌  မီနူး ရွေးချယ်မှု{C.RS}")
        print(f"{C.CY}══════════════════════════════════════════════{C.RS}")
        print(f"   {C.BD}[ 1 ]{C.RS}  📋 ကီးအားလုံးကို ကြည့်ရန်")
        print(f"   {C.BD}[ 2 ]{C.RS}  📋 VLESS ကီးများသာ ကြည့်ရန်")
        print(f"   {C.BD}[ 3 ]{C.RS}  📋 SS ကီးများသာ ကြည့်ရန်")
        print(f"   {C.BD}[ 4 ]{C.RS}  ⚡ Ping နှင့်အတူ ကီးများကို ကြည့်ရန်")
        print(f"   {C.BD}[ 5 ]{C.RS}  🏆 အကောင်းဆုံး ဆာဗာကို ရှာပေးရန်")
        print(f"   {C.BD}[ 6 ]{C.RS}  📡 Subscribe လင့်ခ်များ ကြည့်ရန်")
        print(f"   {C.BD}[ 0 ]{C.RS}  ❌ ထွက်ရန်")
        print(f"{C.CY}═══════════════════════════════════════════════{C.RS}")
        
        choice = input(f"\n{C.B}ရွေးချယ်ပါ → {C.RS}").strip()
        
        if choice == "0":
            print(f"\n{C.CY}👋 ကျေးဇူးတင်ပါတယ်! ပြန်လာတန်းမှာ...{C.RS}\n")
            break
        elif choice == "1":
            show_keys(all_keys)
        elif choice == "2":
            show_keys([k for k in all_keys if k["proto"] == "VLESS"])
        elif choice == "3":
            show_keys([k for k in all_keys if k["proto"] == "SS"])
        elif choice == "4":
            show_keys(all_keys, show_ping=True)
        elif choice == "5":
            find_best_server(all_keys)
        elif choice == "6":
            show_sub_links()
        else:
            print(f"\n{C.R}❌ ရွေးချယ်မှုမှားနေပါတယ်၊ ထပ်မံကြိုးစားကြည့်ပါ{C.RS}\n")

if __name__ == "__main__":
    main()
    
