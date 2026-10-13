#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import base64
import os
import socket
import time

VERSION = "SIMPLE PRO 2.0 ⚡"

class C:
    G = "\033[92m"
    B = "\033[94m"
    Y = "\033[93m"
    R = "\033[91m"
    W = "\033[97m"
    N = "\033[0m"

def clear(): os.system("clear")
def line(): print(f"{C.B}{'─'*55}{C.N}")

def logo():
    clear()
    line()
    print(f"{C.G}⚡ VPN KEY FINDER — SIMPLE PRO {VERSION}{C.N}")
    line()
    print()

SOURCES = [
    {"name": "Shadowmere JSON",   "url": "https://shadowmere.xyz/api/sub/",    "type": "json"},
    {"name": "Shadowmere Base64", "url": "https://shadowmere.xyz/api/b64sub/", "type": "b64"},
]

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.read().decode("utf-8", errors="ignore")
    except:
        return None

def parse(text, t):
    keys = []
    if not text: return []
    if t == "json":
        try:
            import json
            data = json.loads(text)
            for x in data:
                k = x.get("url") or x.get("link") or ""
                n = x.get("name") or x.get("remarks") or "Server"
                if "://" in k: keys.append({"name":n,"key":k})
        except: pass
    elif t == "b64":
        try:
            txt = base64.b64decode(text).decode("utf-8", errors="ignore")
            for ln in txt.splitlines():
                ln = ln.strip()
                if "://" in ln:
                    n = "Server"
                    if "#" in ln:
                        try:
                            from urllib.parse import unquote
                            n = unquote(ln.split("#")[-1])
                        except: n = ln.split("#")[-1][:30]
                    keys.append({"name":n,"key":ln})
        except: pass
    return keys

def get_keys():
    all_keys = []
    seen = set()
    logo()
    print(f"{C.B}📡 ကီးများရယူနေသည်...{C.N}\n")
    for i, src in enumerate(SOURCES,1):
        print(f"  [{i}] {src['name']}...", end=" ")
        txt = fetch(src["url"])
        if txt:
            ks = parse(txt, src["type"])
            if ks:
                for k in ks:
                    if k["key"] not in seen:
                        seen.add(k["key"])
                        all_keys.append(k)
                print(f"{C.G}✅ +{len(ks)}  (စုစုပေါင်း: {len(all_keys)}){C.N}")
            else: print(f"{C.Y}⚠️ မတွေ့{C.N}")
        else: print(f"{C.R}❌ မအောင်မြင်{C.N}")
    print()
    return all_keys

def get_host(key):
    try:
        from urllib.parse import urlparse
        u = urlparse(key)
        return u.hostname or "", u.port or 443
    except: return "", 443

def ping(host, port=443, t=0.5):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(t)
        st = time.time()
        s.connect((host, int(port)))
        s.close()
        return round((time.time()-st)*1000)
    except: return 9999

def copy(text):
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", text])
        return True
    except: return False

def flag(n):
    n = n.lower()
    if "singapore" in n or "sg" in n: return "🇸🇬 SG"
    if "malaysia" in n or "my" in n: return "🇲🇾 MY"
    if "thai" in n or "th" in n: return "🇹🇭 TH"
    if "vietnam" in n or "vn" in n: return "🇻🇳 VN"
    if "hongkong" in n or "hk" in n: return "🇭🇰 HK"
    if "japan" in n or "jp" in n: return "🇯🇵 JP"
    if "korea" in n or "kr" in n: return "🇰🇷 KR"
    return "🌐 --"

def ping_str(ms):
    if ms == 9999: return f"{C.R}❌ မတုံ့ပြန်{C.N}"
    if ms < 100: return f"{C.G}✅ {ms}ms  အလွန်မြန်{C.N}"
    if ms < 200: return f"{C.G}✅ {ms}ms  ကောင်း{C.N}"
    if ms < 400: return f"{C.Y}⚠️ {ms}ms  အတန်းအစား{C.N}"
    return f"{C.R}❌ {ms}ms  နှေး{C.N}"

def network_tip():
    print(f"\n{C.B}📱 သင့်ကွန်ရက်နဲ့ အကိုက်အညီဆုံး ဆာဗာ အကြံပြုချက်{C.N}")
    print(f"  MPT     → 🇸🇬 SG စင်ကာပူ  သို့မဟုတ်  🇹🇭 TH ထိုင်း")
    print(f"  Ooredoo → 🇸🇬 SG စင်ကာပူ  သို့မဟုတ်  🇲🇾 MY မလေးရှား")
    print(f"  Telenor → 🇸🇬 SG စင်ကာပူ  သို့မဟုတ်  🇲🇾 MY မလေးရှား")
    print(f"  Mytel   → 🇹🇭 TH ထိုင်း    သို့မဟုတ်  🇻🇳 VN ဗီယက်နမ်")
    print(f"  WiFi    → 🇸🇬 SG စင်ကာပူ  အမြဲပိုမိုမြန်ဆန်တယ်")
    print(f"  💡 စည်းမျဉ်း: Ping < 200ms = အကောင်းဆုံး ✅  |  >400ms = ပြောင်းသင့် ❌")
    print()

def scan(keys):
    logo()
    print(f"{C.B}📊 ဆာဗာများကို စမ်းသပ်နေသည်...{C.N}\n")
    res = []
    total = min(len(keys), 15)
    for i in range(total):
        k = keys[i]
        h, p = get_host(k["key"])
        ms = ping(h, p) if h else 9999
        res.append({"name":k["name"],"key":k["key"],"ms":ms})
        print(f"  [{i+1}/{total}] ပြီးပြီ", end="\r")
    print("\n")
    res.sort(key=lambda x:x["ms"])
    return res

def show_best(results, keys):
    logo()
    line()
    print(f"{C.G}🏆 အကောင်းဆုံး ဆာဗာ{C.N}\n")
    best = None
    for r in results:
        if r["ms"] < 9999:
            best = r
            break
    if not best:
        print(f"{C.R}❌ မည်သည့်ဆာဗာမျှ မတုံ့ပြန်ပါ{C.N}")
        return
    
    fl = flag(best["name"])
    print(f"  နိုင်ငံ   : {fl}")
    print(f"  အမည်     : {best['name'][:40]}")
    print(f"  မြန်နှုန်း : {ping_str(best['ms'])}")
    print()
    print(f"{C.B}🔑 VPN Key (အောက်ကကို ကူးယူပါ){C.N}")
    print(f"  {C.W}{best['key']}{C.N}")
    print()
    if copy(best["key"]):
        print(f"{C.G}✅ ကီးကို ကလစ်ဘုတ်သို့ ကူးယူပြီးပါပြီ!{C.N}")
        print(f"{C.B}💡 V2RayNG/NekoBox ထဲမှာ → + → Import from Clipboard နှိပ်ပါ{C.N}")
    network_tip()
    line()

def show_list(results):
    logo()
    print(f"{C.B}📋 ဆာဗာအားလုံးစာရင်း{C.N}\n")
    print(f"  နိုင်ငံ    Ping       အမည်")
    line()
    for i, r in enumerate(results, 1):
        fl = flag(r["name"])
        print(f"  {i:02d} {fl}  {ping_str(r['ms']):<22} {r['name'][:30]}")
    network_tip()

def main():
    keys = get_keys()
    if not keys:
        print(f"{C.R}❌ ကီးမရပါ{C.N}")
        input("ပြန်ရန် Enter...")
        return
    results = scan(keys)
    
    while True:
        logo()
        print(f"{C.B}📋 မီနူး{C.N}\n")
        print(f"  {C.G}[1]{C.N} 🏆 အကောင်းဆုံး ဆာဗာကို ချက်ချင်းရွေးပါ")
        print(f"  {C.G}[2]{C.N} 📋 ဆာဗာအားလုံးစာရင်း ကြည့်ပါ")
        print(f"  {C.G}[3]{C.N} 📱 ကွန်ရက်အလိုက် အကြံပြုချက်")
        print(f"  {C.G}[4]{C.N} 🔄 အသစ်ပြန်ရှာပါ")
        print(f"  {C.R}[0]{C.N} ❌ ထွက်ပါ")
        print()
        sel = input(f"ရွေးချယ်ပါ → ").strip()
        
        if sel == "1":
            show_best(results, keys)
            input("\nပြန်ရန် Enter...")
        elif sel == "2":
            show_list(results)
            input("\nပြန်ရန် Enter...")
        elif sel == "3":
            logo()
            network_tip()
            input("ပြန်ရန် Enter...")
        elif sel == "4":
            keys = get_keys()
            if keys: results = scan(keys)
        elif sel == "0":
            print(f"{C.G}👋 ပျော်ရွှင်ဖွယ်ရှိပါစေ!{C.N}")
            break

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{C.G}👋 ပြီးပါပြီ{C.N}")
    except Exception as e: print(f"{C.R}အမှား: {e}{C.N}")
        
