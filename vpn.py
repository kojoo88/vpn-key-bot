#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import base64
import os
import socket
import time
import json
from datetime import datetime

VERSION = "FAST FILTER 1.0 ⚡"
FAV_FILE = os.path.expanduser("~/.vpn_favorites.json")

class C:
    G = "\033[92m"
    B = "\033[94m"
    Y = "\033[93m"
    R = "\033[91m"
    W = "\033[97m"
    M = "\033[95m"
    N = "\033[0m"

def clear(): os.system("clear")
def line(): print(f"{C.B}{'═'*60}{C.N}")

def logo():
    clear()
    line()
    print(f"{C.G}⚡ FAST FILTER — လိုင်းကောင်းဆာဗာသီးသန့်  {VERSION}{C.N}")
    line()
    print()

# ==================================================
# ⚡ စစ်ထုတ်မှု စံနှုန်းများ
# ==================================================
GOOD_PING_MAX = 200        # ms အောက်သာ ကောင်းတယ်
GOOD_SPEED_MIN = 200       # kbps အထက်သာ ကောင်းတယ်
PRIORITY_COUNTRIES = ["🇸🇬", "🇲🇾", "🇹🇭", "🇻🇳", "🇭🇰"]  # ဦးစားပေးနိုင်ငံ

# ==================================================
# 📂 အရင်းအမြစ်များ
# ==================================================
SOURCES = [
    {"name": "Shadowmere", "url": "https://shadowmere.xyz/api/b64sub/", "type": "b64"},
    {"name": "Epodonios SS", "url": "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/ss.txt", "type": "txt"},
    {"name": "Epodonios VLESS", "url": "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/vless.txt", "type": "txt"},
    {"name": "MatinGhanbari SS", "url": "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/ss.txt", "type": "txt"},
    {"name": "MatinGhanbari VLESS", "url": "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/vless.txt", "type": "txt"},
]

# ==================================================
# ⭐ အကြိုက်ဆုံး စီမံခန့်ခွဲမှု
# ==================================================
def load_favorites():
    if os.path.exists(FAV_FILE):
        try:
            with open(FAV_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []
    return []

def save_favorite(item):
    favs = load_favorites()
    if any(f["key"] == item["key"] for f in favs):
        return False, "ရှိပြီးသား"
    fav_item = {"name": item["name"], "key": item["key"], "proto": item["proto"], "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M")}
    favs.insert(0, fav_item)
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(favs, f, ensure_ascii=False, indent=2)
    return True, "⭐ အကြိုက်ဆုံးထဲ သိမ်းပြီးပါပြီ"

# ==================================================
# 📥 ဖတ်ခြင်း
# ==================================================
def fetch(src):
    try:
        req = urllib.request.Request(src["url"], headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as r:
            return r.read().decode("utf-8", errors="ignore")
    except: return None

def parse(content, src_type):
    keys = []
    if not content: return []
    if src_type == "b64":
        try: content = base64.b64decode(content).decode("utf-8", errors="ignore")
        except: pass
    for line in content.splitlines():
        line = line.strip()
        if not line: continue
        proto = None
        if line.startswith("vless://"): proto = "vless"
        elif line.startswith("ss://"): proto = "ss"
        if not proto: continue
        name = "Server"
        if "#" in line:
            try:
                from urllib.parse import unquote
                name = unquote(line.split("#")[-1])[:40]
            except: name = line.split("#")[-1][:40]
        keys.append({"name": name, "key": line, "proto": proto})
    return keys

# ==================================================
# 📊 စမ်းသပ်ခြင်း
# ==================================================
def get_host(key):
    try:
        from urllib.parse import urlparse
        u = urlparse(key)
        return u.hostname or "", u.port or 443
    except: return "", 443

def ping_test(host, port=443, t=0.6):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(t)
        st = time.time()
        s.connect((host, int(port)))
        s.close()
        return round((time.time()-st)*1000)
    except: return 9999

def speed_test(host, port=443):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        st = time.time()
        s.connect((host, int(port)))
        s.send(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\nConnection: close\r\n\r\n")
        data = s.recv(1024)
        s.close()
        elapsed = time.time() - st
        return round((len(data) / 1024) / elapsed * 8) if elapsed > 0 else 0
    except: return 0

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
    if ms < 350: return f"{C.Y}⚠️ {ms}ms  အတန်းအစား{C.N}"
    return f"{C.R}❌ {ms}ms  နှေး{C.N}"

def speed_str(kbps):
    if kbps == 0: return f"{C.R}— မစမ်းနိုင်{C.N}"
    if kbps > 500: return f"{C.G}🔥 {kbps} kbps  အမြန်{C.N}"
    if kbps > 200: return f"{C.G}✅ {kbps} kbps  ကောင်း{C.N}"
    if kbps > 50: return f"{C.Y}⚠️ {kbps} kbps  နှေး{C.N}"
    return f"{C.R}🐢 {kbps} kbps  နှေးလွန်း{C.N}"

def copy_text(text):
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", text])
        return True
    except: return False

# ==================================================
# 🔍 စစ်ထုတ်ခြင်း — အဓိကအပိုင်း
# ==================================================
def is_good_server(r):
    fl = flag(r["name"])
    in_priority = any(p in fl for p in PRIORITY_COUNTRIES)
    good_ping = r["ms"] < GOOD_PING_MAX
    good_speed = r["speed"] > GOOD_SPEED_MIN
    return in_priority and good_ping and good_speed

def scan_and_filter(keys, limit=20):
    logo()
    print(f"{C.B}📊 လိုင်းကောင်းဆာဗာများကို ရှာဖွေနေသည်...{C.N}")
    print(f"{C.G}စံနှုန်း: Ping < {GOOD_PING_MAX}ms  +  Speed > {GOOD_SPEED_MIN}kbps  +  အနီးအနားနိုင်ငံ{C.N}\n")
    
    results = []
    total = min(len(keys), limit)
    for i in range(total):
        k = keys[i]
        h, p = get_host(k["key"])
        ms = ping_test(h, p) if h else 9999
        spd = speed_test(h, p) if h and ms < 9999 else 0
        results.append({"name": k["name"], "key": k["key"], "proto": k["proto"], "ms": ms, "speed": spd})
        print(f"  [{i+1}/{total}] စမ်းသပ်နေသည်", end="\r")
    print("\n\n")
    
    good = [r for r in results if is_good_server(r)]
    good.sort(key=lambda x: (x["ms"], -x["speed"]))
    return good, results

# ==================================================
# 📋 ပြသခြင်း
# ==================================================
def show_good_only(good, all_results):
    logo()
    print(f"{C.G}🏆 လိုင်းကောင်းဆာဗာများသာ  (စံနှုန်းကိုက်ညီသူ: {len(good)}/{len(all_results)}){C.N}\n")
    
    if not good:
        print(f"{C.Y}⚠️ ယခုအချိန်တွင် စံနှုန်းပြည့်မီသောဆာဗာ မတွေ့သေးပါ{C.N}")
        print(f"   ပြန်စကင်န်ဖတ်ကြည့်ပါ သို့မဟုတ် စံနှုန်းကို ပြောင်းကြည့်ပါ\n")
        return None
    
    print(f"  #   နိုင်ငံ   ပရိုတို   Ping          အမြန်နှုန်း       အမည်")
    line()
    for i, r in enumerate(good, 1):
        fl = flag(r["name"])
        print(f"  {i}   {fl}   {r['proto'].upper():<6}   {ping_str(r['ms']):<22} {speed_str(r['speed']):<18} {r['name'][:28]}")
    
    print(f"\n{C.G}✅ အကောင်းဆုံးကီး {len(good)} ခု တွေ့ရှိခဲ့သည်{C.N}")
    
    if good:
        top_keys = "\n".join([r["key"] for r in good[:3]])
        if copy_text(top_keys):
            print(f"{C.G}✅ အကောင်းဆုံး ၃ ခုကို ကလစ်ဘုတ်သို့ ကူးယူပြီးပါပြီ!{C.N}")
            print(f"   V2RayNG → + → Import from Clipboard နှိပ်ပါ")
        
        print(f"\n{C.M}[1] ပထမဆုံးကီးကို အကြိုက်ဆုံးထဲသိမ်းမည်  [0] ပြန်မယ်{C.N}")
        sel = input(f"ရွေးချယ်ပါ → ").strip()
        if sel == "1":
            ok, msg = save_favorite(good[0])
            print(f"  {C.G if ok else C.Y}{msg}{C.N}")
            time.sleep(1)
    
    return good

def show_favorites():
    while True:
        favs = load_favorites()
        logo()
        print(f"{C.M}⭐ အကြိုက်ဆုံးဆာဗာများ  (စုစုပေါင်း: {len(favs)} ခု){C.N}\n")
        if not favs:
            print(f"{C.Y}အကြိုက်ဆုံး မသိမ်းရသေးပါ{C.N}")
        else:
            for i, f in enumerate(favs, 1):
                fl = flag(f["name"])
                print(f"  [{i}] {fl}  {f['name'][:35]}  |  {f['proto'].upper()}")
                print(f"      🔑 {f['key'][:55]}...")
                print(f"      💾 {f['saved_at']}\n")
        print(f"  {C.G}နံပါတ်ထည့်ပါ = ကီးကူးယူမည်   [0] = ပြန်သွားရန်{C.N}")
        sel = input(f"ရွေးချယ်ပါ → ").strip()
        if sel == "0": break
        if sel.isdigit():
            idx = int(sel) - 1
            if 0 <= idx < len(favs):
                copy_text(favs[idx]["key"])
                print(f"  {C.G}✅ ကီးကူးယူပြီးပါပြီ!{C.N}")
                time.sleep(1)

# ==================================================
# 🏠 ပင်မမီနူး
# ==================================================
def main():
    all_keys = []
    for src in SOURCES:
        print(f"ဖတ်နေသည်: {src['name']}...", end=" ")
        txt = fetch(src)
        if txt:
            ks = parse(txt, src["type"])
            all_keys.extend(ks)
            print(f"{C.G}+{len(ks)}{C.N}")
        else:
            print(f"{C.R}မရှိ{C.N}")
    
    seen = set()
    unique_keys = []
    for k in all_keys:
        if k["key"] not in seen:
            seen.add(k["key"])
            unique_keys.append(k)
    print(f"\n{C.B}စုစုပေါင်း ကီး {len(unique_keys)} ခု အဆင်သင့်{C.N}\n")
    
    while True:
        logo()
        print(f"{C.B}📋 ပင်မမီနူး{C.N}\n")
        print(f"  {C.G}[1]{C.N} ⚡ လိုင်းကောင်းဆာဗာများကို ရှာမည် (အကောင်းဆုံးသာ)")
        print(f"  {C.G}[2]{C.N} ⭐ အကြိုက်ဆုံးဆာဗာများ")
        print(f"  {C.G}[3]{C.N} 🔄 ကီးအသစ်ပြန်ဖတ်မည်")
        print(f"  {C.R}[0]{C.N} ❌ ထွက်ပါ")
        print()
        sel = input(f"ရွေးချယ်ပါ → ").strip()
        
        if sel == "1":
            good, all_res = scan_and_filter(unique_keys)
            show_good_only(good, all_res)
            input(f"\nပြန်ရန် Enter...")
        elif sel == "2":
            show_favorites()
        elif sel == "3":
            all_keys = []
            for src in SOURCES:
                txt = fetch(src)
                if txt: all_keys.extend(parse(txt, src["type"]))
            seen = set(); unique_keys = []
            for k in all_keys:
                if k["key"] not in seen: seen.add(k["key"]); unique_keys.append(k)
            print(f"{C.G}✅ ကီးအသစ်များ ဖတ်ပြီးပါပြီ (စုစုပေါင်း: {len(unique_keys)}){C.N}")
            time.sleep(1)
        elif sel == "0":
            print(f"{C.G}👋 ပျော်ရွှင်ဖွယ်ရှိပါစေ!{C.N}")
            break

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{C.G}👋 ပြီးပါပြီ{C.N}")
    except Exception as e: print(f"\n{C.R}အမှား: {e}{C.N}")
