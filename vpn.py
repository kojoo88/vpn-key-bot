#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import base64
import os
import socket
import time

VERSION = "SPLIT PRO 1.0 ⚡"

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
    print(f"{C.G}⚡ VPN KEY FINDER — VLESS + SS SPLIT  {VERSION}{C.N}")
    line()
    print()

# ==================================================
# 📂 VLESS သီးသန့် အရင်းအမြစ်များ
# ==================================================
VLESS_SOURCES = [
    {
        "name": "Epodonios VLESS",
        "url": "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/vless.txt",
        "type": "txt"
    },
    {
        "name": "MatinGhanbari VLESS",
        "url": "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/vless.txt",
        "type": "txt"
    },
    {
        "name": "Shadowmere Base64",
        "url": "https://shadowmere.xyz/api/b64sub/",
        "type": "b64"
    }
]

# ==================================================
# 📂 SS (Shadowsocks) သီးသန့် အရင်းအမြစ်များ
# ==================================================
SS_SOURCES = [
    {
        "name": "Epodonios SS",
        "url": "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/ss.txt",
        "type": "txt"
    },
    {
        "name": "MatinGhanbari SS",
        "url": "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/ss.txt",
        "type": "txt"
    }
]

def fetch_url(source):
    try:
        req = urllib.request.Request(
            source["url"],
            headers={"User-Agent": "Mozilla/5.0 (Android; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0"}
        )
        with urllib.request.urlopen(req, timeout=12) as res:
            return res.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return None

def parse_text(text, source_type, protocol_filter=None):
    keys = []
    if not text: return keys
    
    if source_type == "b64":
        try:
            text = base64.b64decode(text).decode("utf-8", errors="ignore")
        except:
            pass
    
    for line in text.splitlines():
        line = line.strip()
        if not line: continue
        
        proto = None
        if line.startswith("vless://"): proto = "vless"
        elif line.startswith("ss://"): proto = "ss"
        elif line.startswith("vmess://"): proto = "vmess"
        
        if not proto: continue
        if protocol_filter and proto != protocol_filter: continue
        
        name = f"{proto.upper()} Server"
        if "#" in line:
            try:
                from urllib.parse import unquote
                name = unquote(line.split("#")[-1])[:40]
            except:
                name = line.split("#")[-1][:40]
        
        keys.append({"proto": proto, "name": name, "key": line})
    return keys

def load_from_sources(sources, protocol_name, protocol_filter=None):
    all_keys = []
    seen = set()
    print(f"{C.B}📡 {protocol_name} ကီးများရယူနေသည်...{C.N}\n")
    
    for i, src in enumerate(sources, 1):
        print(f"  [{i}/{len(sources)}] {src['name']:<25}", end=" ")
        text = fetch_url(src["url"])
        if text:
            ks = parse_text(text, src["type"], protocol_filter)
            if ks:
                for k in ks:
                    if k["key"] not in seen:
                        seen.add(k["key"])
                        all_keys.append(k)
                print(f"{C.G}✅ +{len(ks)}  (စုစုပေါင်း: {len(all_keys)}){C.N}")
            else:
                print(f"{C.Y}⚠️ ကီးမတွေ့{C.N}")
        else:
            print(f"{C.R}❌ မအောင်မြင်{C.N}")
    print()
    return all_keys

def get_host(key):
    try:
        from urllib.parse import urlparse
        u = urlparse(key)
        return u.hostname or "", u.port or 443
    except:
        return "", 443

def ping_server(host, port=443, t=0.5):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(t)
        st = time.time()
        s.connect((host, int(port)))
        s.close()
        return round((time.time()-st)*1000)
    except:
        return 9999

def copy_to_clipboard(text):
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", text])
        return True
    except:
        return False

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

def ping_display(ms):
    if ms == 9999: return f"{C.R}❌ မတုံ့ပြန်{C.N}"
    if ms < 100: return f"{C.G}✅ {ms}ms  အလွန်မြန်{C.N}"
    if ms < 200: return f"{C.G}✅ {ms}ms  ကောင်း{C.N}"
    if ms < 400: return f"{C.Y}⚠️ {ms}ms  အတန်းအစား{C.N}"
    return f"{C.R}❌ {ms}ms  နှေး{C.N}"

def network_tips():
    print(f"\n{C.B}📱 ကွန်ရက်အလိုက် အကြံပြုချက်{C.N}")
    print(f"  MPT     → 🇸🇬 SG သို့မဟုတ် 🇹🇭 TH")
    print(f"  Ooredoo → 🇸🇬 SG သို့မဟုတ် 🇲🇾 MY")
    print(f"  Telenor → 🇸🇬 SG သို့မဟုတ် 🇲🇾 MY")
    print(f"  Mytel   → 🇹🇭 TH သို့မဟုတ် 🇻🇳 VN")
    print(f"  WiFi    → 🇸🇬 SG အကောင်းဆုံး")
    print(f"  💡 Ping < 200ms = အကောင်းဆုံး ✅  |  >400ms = ပြောင်းသင့် ❌")
    print()

def scan_keys(keys):
    logo()
    print(f"{C.B}📊 ဆာဗာများကို စမ်းသပ်နေသည်...{C.N}\n")
    res = []
    total = min(len(keys), 15)
    for i in range(total):
        k = keys[i]
        h, p = get_host(k["key"])
        ms = ping_server(h, p) if h else 9999
        res.append({"name": k["name"], "key": k["key"], "ms": ms, "proto": k["proto"]})
        print(f"  [{i+1}/{total}] ပြီးပြီ", end="\r")
    print("\n")
    res.sort(key=lambda x: x["ms"])
    return res

def show_best_result(results, total_keys):
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
    print(f"  ပရိုတိုကော : {C.G}{best['proto'].upper()}{C.N}")
    print(f"  နိုင်ငံ    : {fl}")
    print(f"  အမည်      : {best['name'][:40]}")
    print(f"  မြန်နှုန်း  : {ping_display(best['ms'])}")
    print()
    print(f"{C.B}🔑 VPN Key (အောက်ကကို ကူးယူပါ){C.N}")
    print(f"  {C.W}{best['key']}{C.N}")
    print()
    
    if copy_to_clipboard(best["key"]):
        print(f"{C.G}✅ ကီးကို ကလစ်ဘုတ်သို့ ကူးယူပြီးပါပြီ!{C.N}")
        print(f"{C.B}💡 V2RayNG/NekoBox → + → Import from Clipboard နှိပ်ပါ{C.N}")
    
    network_tips()
    line()

def show_all_list(results):
    logo()
    print(f"{C.B}📋 ဆာဗာအားလုံးစာရင်း{C.N}\n")
    print(f"  #    နိုင်ငံ    ပရိုတိုကော    Ping           အမည်")
    line()
    for i, r in enumerate(results, 1):
        fl = flag(r["name"])
        print(f"  {i:02d}  {fl}   {r['proto'].upper():<6}    {ping_display(r['ms']):<22} {r['name'][:28]}")
    network_tips()

def vless_menu():
    logo()
    keys = load_from_sources(VLESS_SOURCES, "VLESS", protocol_filter="vless")
    if not keys:
        input(f"{C.R}ပြန်ရန် Enter...{C.N}")
        return
    results = scan_keys(keys)
    
    while True:
        logo()
        print(f"{C.G}🟦 VLESS မီနူး  (စုစုပေါင်း: {len(keys)} ခု){C.N}\n")
        print(f"  {C.G}[1]{C.N} 🏆 အကောင်းဆုံး VLESS ကို ချက်ချင်းရွေးပါ")
        print(f"  {C.G}[2]{C.N} 📋 VLESS အားလုံးစာရင်း")
        print(f"  {C.G}[3]{C.N} 🔄 VLESS ကို ပြန်လည်စကင်န်ဖတ်ပါ")
        print(f"  {C.R}[0]{C.N} ← ပင်မမီနူးသို့ ပြန်သွားရန်")
        print()
        sel = input(f"ရွေးချယ်ပါ → ").strip()
        
        if sel == "1":
            show_best_result(results, len(keys))
            input(f"\nပြန်ရန် Enter...")
        elif sel == "2":
            show_all_list(results)
            input(f"\nပြန်ရန် Enter...")
        elif sel == "3":
            keys = load_from_sources(VLESS_SOURCES, "VLESS", "vless")
            if keys: results = scan_keys(keys)
        elif sel == "0":
            break

def ss_menu():
    logo()
    keys = load_from_sources(SS_SOURCES, "SS (Shadowsocks)", protocol_filter="ss")
    if not keys:
        input(f"{C.R}ပြန်ရန် Enter...{C.N}")
        return
    results = scan_keys(keys)
    
    while True:
        logo()
        print(f"{C.G}🟩 SS (Shadowsocks) မီနူး  (စုစုပေါင်း: {len(keys)} ခု){C.N}\n")
        print(f"  {C.G}[1]{C.N} 🏆 အကောင်းဆုံး SS ကို ချက်ချင်းရွေးပါ")
        print(f"  {C.G}[2]{C.N} 📋 SS အားလုံးစာရင်း")
        print(f"  {C.G}[3]{C.N} 🔄 SS ကို ပြန်လည်စကင်န်ဖတ်ပါ")
        print(f"  {C.R}[0]{C.N} ← ပင်မမီနူးသို့ ပြန်သွားရန်")
        print()
        sel = input(f"ရွေးချယ်ပါ → ").strip()
        
        if sel == "1":
            show_best_result(results, len(keys))
            input(f"\nပြန်ရန် Enter...")
        elif sel == "2":
            show_all_list(results)
            input(f"\nပြန်ရန် Enter...")
        elif sel == "3":
            keys = load_from_sources(SS_SOURCES, "SS", "ss")
            if keys: results = scan_keys(keys)
        elif sel == "0":
            break

def main_menu():
    while True:
        logo()
        print(f"{C.B}📋 ပင်မမီနူး{C.N}\n")
        print(f"  {C.G}[1]{C.N} 🟦 VLESS ဆာဗာများ")
        print(f"  {C.G}[2]{C.N} 🟩 SS (Shadowsocks) ဆာဗာများ")
        print(f"  {C.G}[3]{C.N} 📱 ကွန်ရက်အလိုက် အကြံပြုချက်")
        print(f"  {C.R}[0]{C.N} ❌ ထွက်ပါ")
        print()
        sel = input(f"ရွေးချယ်ပါ → ").strip()
        
        if sel == "1":
            vless_menu()
        elif sel == "2":
            ss_menu()
        elif sel == "3":
            logo()
            network_tips()
            input(f"ပြန်ရန် Enter...")
        elif sel == "0":
            print(f"{C.G}👋 ပျော်ရွှင်ဖွယ်ရှိပါစေ!{C.N}")
            break
        else:
            print(f"{C.R}❌ ရွေးချယ်မှုမှားနေပါသည်! 0-3 ကြားသာထည့်ပါ{C.N}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{C.G}👋 ပြီးပါပြီ{C.N}")
    except Exception as e:
        print(f"\n{C.R}အမှားအယွင်း: {str(e)}{C.N}")
        input(f"ဆက်ရန် Enter...")
    
