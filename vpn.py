#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import base64
import socket
import time
import os
import subprocess
import sys

# ================== အရောင်များ ==================
BLK = "\033[38;5;234m"
BLU = "\033[38;5;117m"
CYN = "\033[38;5;80m"
GRN = "\033[38;5;114m"
YEL = "\033[38;5;221m"
ORG = "\033[38;5;215m"
RED = "\033[38;5;209m"
PUR = "\033[38;5;141m"
PINK = "\033[38;5;212m"
LIME = "\033[38;5;156m"
WHT = "\033[38;5;255m"
DIM = "\033[2m"
BD = "\033[1m"
RST = "\033[0m"

# ================== ADMIN LINK ==================
ADMIN_LINK = "https://www.facebook.com/share/19TVQNTUGZ/"
# =================================================

def clear():
    os.system("clear")

def open_admin_link():
    clear()
    print(PUR + "="*50 + RST)
    print(PUR + "|" + RST + "      📘 Admin ဆီဆက်သွယ်ရန်       " + PUR + "|" + RST)
    print(PUR + "="*50 + RST)
    print(f"\n  🔘 Facebook စာမျက်နှာ လင့်ခ်-")
    print(f"\n  {CYN}{ADMIN_LINK}{RST}")
    print(f"\n  {'─'*50}")
    print(f"  💡 အသုံးပြုနည်း-")
    print(f"     ၁။ အပေါ်က လင့်ခ်ကို နှိပ်ပြီး ကူးယူပါ")
    print(f"     ၂။ သင့်ဖုန်းရဲ့ ဘရောက်ဇာထဲမှာ ကူးထည့်ဖွင့်ပါ")
    print(f"  {'─'*50}\n")
    input(f"{CYN}ပြန်ရန် Enter နှိပ်ပါ...{RST}")

# ================== ရင်းမြစ်များ ==================
SOURCES = [
    ("V2Nodes", "https://www.v2nodes.com/subscriptions/country/all/?key=72BEE427C23A1AF", "b64"),
    ("Shadowmere B64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("Shadowmere Plain", "https://shadowmere.xyz/api/sub/", "txt"),
    ("V2Ray-Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
    ("Epodon VLESS", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Splitted-By-Protocol/vless.txt", "txt"),
    ("Epodon SS", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/ss.txt", "txt"),
    ("Free V2Ray", "https://raw.githubusercontent.com/freefq/free/master/v2", "b64"),
]

FAV_FILE = "favorites.txt"
favorites = []

def load_favorites():
    global favorites
    favorites = []
    if os.path.exists(FAV_FILE):
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            favorites = [l.strip() for l in f if l.strip()]

def save_favorites():
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        for url in favorites:
            f.write(url + "\n")

def get_net():
    try:
        result = subprocess.run(['ip','link'], capture_output=True, text=True, timeout=3)
        return "WiFi" if 'wlan' in result.stdout.lower() or 'wlp' in result.stdout.lower() else "Mobile Data"
    except:
        return "Unknown"

def get_country_flag(name):
    flags = {"SG": "🇸🇬", "US": "🇺🇸", "JP": "🇯🇵", "KR": "🇰🇷", "HK": "🇭🇰",
             "TW": "🇹🇼", "UK": "🇬🇧", "GB": "🇬🇧", "DE": "🇩🇪", "NL": "🇳🇱",
             "CA": "🇨🇦", "AU": "🇦🇺", "IN": "🇮🇳", "TH": "🇹🇭", "MY": "🇲🇲"}
    for code in flags.keys():
        if code in name.upper():
            return flags[code] + " " + code
    return "🌐 ?? "

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf-8", errors="ignore")
    except:
        return None

def parse(content, fmt):
    keys = []
    if not content:
        return keys
    try:
        if fmt == "b64":
            content = base64.b64decode(content).decode("utf-8", errors="ignore")
        lines = content.splitlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith(("vless://", "ss://")):
                protocol = "VLESS" if line.startswith("vless://") else "SS"
                name = f"{protocol}-{line[:30]}..."
                keys.append({"name": name, "url": line, "protocol": protocol})
    except:
        pass
    return keys

def ping_test(url):
    try:
        host = "8.8.8.8"
        port = 53
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        start = time.time()
        s.connect((host, port))
        ms = int((time.time() - start) * 1000)
        s.close()
        if ms < 100:
            return True, ms, "Fast", 5
        elif ms < 200:
            return True, ms, "Normal", 4
        elif ms < 300:
            return True, ms, "Medium", 3
        elif ms < 500:
            return True, ms, "Slow", 2
        else:
            return True, ms, "Very Slow", 1
    except:
        return False, 999, "Offline", 0

def load_all():
    all_keys = []
    vless = []
    ss = []
    clear()
    print(PUR + "="*50 + RST)
    print(PUR + "|" + RST + "    🔄 ရင်းမြစ်များကို ဖတ်နေသည်...    " + PUR + "|" + RST)
    print(PUR + "-"*50 + RST)
    success_count = 0
    for idx, (name, url, fmt) in enumerate(SOURCES, 1):
        print(f"  [{idx}/{len(SOURCES)}] {name:<25}", end=" ")
        content = fetch(url)
        if content:
            keys = parse(content, fmt)
            for k in keys:
                if k["protocol"] == "VLESS":
                    vless.append(k)
                else:
                    ss.append(k)
            all_keys.extend(keys)
            print(f"{GRN}✅ {len(keys)} ခု ရှိသည်{RST}")
            success_count += 1
        else:
            print(f"{RED}❌ မဖတ်နိုင်ပါ{RST}")
    print(PUR + "="*50 + RST)
    print(f"{GRN}✅ စုစုပေါင်း {success_count}/{len(SOURCES)} ရင်းမြစ် ဖတ်ပြီး{WHT}")
    print(f"   VLESS: {len(vless)} ခု  |  SS: {len(ss)} ခု{WHT}")
    load_favorites()
    input(f"\n{CYN}ဆက်ရန် Enter နှိပ်ပါ...{RST}")
    return vless, ss

def scan_and_show(keys, title, count=20):
    if not keys:
        print(f"\n{YEL}⚠️  အရင်ဆုံး [1] Load Sources ကို နှိပ်ပါ!{RST}")
        time.sleep(1.5)
        return
    results = []
    clear()
    print(PUR + "="*60 + RST)
    print(PUR + f"|   📊 {title}{' '*(50-len(title))}|" + RST)
    print(PUR + "-"*60 + RST)
    total = len(keys)
    for i, k in enumerate(keys, 1):
        pct = int(i/total*100)
        print(f"  🔄 စစ်ဆေးနေသည်... {pct}%", end="\r")
        ok, ms, lvl, sc = ping_test(k["url"])
        if ok and sc > 0:
            k["ms"] = ms
            k["lvl"] = lvl
            k["sc"] = sc
            results.append(k)
    
    results.sort(key=lambda x: x["ms"])
    top = results[:count]
    
    # ============== ဖိုင်ထဲ အပြည့်အဝသိမ်းမယ် ==============
    with open("all_keys.txt", "w", encoding="utf-8") as f:
        f.write("="*70 + "\n")
        f.write(f"  {title} - အပြည့်အစုံစာရင်း\n")
        f.write("="*70 + "\n\n")
        f.write(f"စုစုပေါင်းဆာဗာ: {len(results)} ခု  |  ပြသမှု: ထိပ်ဆုံး {len(top)} ခု\n")
        f.write("="*70 + "\n\n")
        for idx, s in enumerate(top, 1):
            flag = get_country_flag(s["name"])
            f.write(f"[{idx}] {flag} {s['name']}\n")
            f.write(f"     Ping: {s['ms']}ms  |  အရှိန်အဆင့်: {s['lvl']}\n")
            f.write(f"     🔑 KEY: {s['url']}\n")
            f.write("-"*70 + "\n")
    # ==========================================================
    
    # မျက်နှာပြင်မှာ အကျဉ်းပဲပြမယ်
    print(f"\n{GRN}✅ စစ်ဆေးပြီးစီးပါပြီ! စုစုပေါင်း {len(results)} ခု တွေ့ရှိ{WHT}")
    print(f"{CYN}📋 အပြည့်အစုံကို 'all_keys.txt' ဖိုင်ထဲ သိမ်းပြီးပါပြီ{WHT}")
    print(f"   ကြည့်ရန်- cat all_keys.txt\n")
    print(PUR + "-"*60 + RST)
    
    for idx, s in enumerate(top, 1):
        flag = get_country_flag(s["name"])
        stars = "★"*s["sc"] + "☆"*(5-s["sc"])
        print(f"  [{idx}] {flag}")
        print(f"      Ping: {CYN}{s['ms']:>4}ms{RST}  |  အရှိန်: {stars}  {GRN}{s['lvl']}{RST}")
        print(f"      ဖိုင်ထဲမှာ အပြည့်အဝကြည့်ပါ → all_keys.txt\n")
    
    print(PUR + "="*60 + RST)
    input(f"{CYN}ပြန်ရန် Enter နှိပ်ပါ...{RST}")

def best_for_me(all_keys):
    if not all_keys:
        print(f"\n{YEL}⚠️  အရင်ဆုံး [1] Load Sources ကို နှိပ်ပါ!{RST}")
        time.sleep(1.5)
        return
    clear()
    print(PUR + "="*60 + RST)
    print(PUR + "|    🏆 သင့်လိုင်းနှင့် အကိုက်ညီဆုံး ရှာဖွေနေသည်...    |" + RST)
    print(PUR + "-"*60 + RST)
    
    results = []
    total = len(all_keys)
    for i, k in enumerate(all_keys, 1):
        pct = int(i/total*100)
        print(f"  🔄 စစ်ဆေးနေသည်... {pct}%", end="\r")
        ok, ms, lvl, sc = ping_test(k["url"])
        if ok and sc > 0:
            k["ms"] = ms
            k["lvl"] = lvl
            k["sc"] = sc
            results.append(k)
    
    results.sort(key=lambda x: x["ms"])
    if results:
        best = results[0]
        flag = get_country_flag(best["name"])
        
        # အကောင်းဆုံးကီးကို သီးခြားဖိုင်ထဲသိမ်းမယ်
        with open("best_key.txt", "w", encoding="utf-8") as f:
            f.write("="*70 + "\n")
            f.write("  🏆 အကောင်းဆုံးဆာဗာ - သင့်လိုင်းနှင့် အကိုက်ညီဆုံး\n")
            f.write("="*70 + "\n\n")
            f.write(f"ဆာဗာအမည်: {best['name']}\n")
            f.write(f"တိုင်းပြည်: {flag}\n")
            f.write(f"Ping: {best['ms']}ms\n")
            f.write(f"အရှိန်အဆင့်: {best['lvl']}\n")
            f.write(f"ရှာဖွေချိန်: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n" + "="*70 + "\n")
            f.write(f"🔑 VPN KEY:\n{best['url']}\n")
        
        clear()
        print(PUR + "="*60 + RST)
        print(PUR + "|        🏆 အကောင်းဆုံးဆာဗာ တွေ့ရှိပါသည်!         |" + RST)
        print(PUR + "-"*60 + RST)
        print(f"\n  {BD}{flag}{RST}")
        print(f"  အမည်: {best['name']}")
        print(f"  Ping: {GRN}{best['ms']}ms{RST}")
        print(f"  အရှိန်အဆင့်: {GRN}{best['lvl']}{RST}")
        print(f"\n  {PINK}📋 ကီးအပြည့်အစုံကို 'best_key.txt' ဖိုင်ထဲ သိမ်းပြီးပါပြီ{RST}")
        print(f"   ကြည့်ရန်- cat best_key.txt")
        print(f"\n  {'─'*60}")
        choice = input(f"\n  {CYN}[S] အကြိုက်ဆုံးထဲသိမ်းမယ်  |  [X] ပြန်မယ်{RST}  → ").upper()
        if choice == "S":
            if best["url"] not in favorites:
                favorites.append(best["url"])
                save_favorites()
                print(f"\n{GRN}✅ အကြိုက်ဆုံးထဲ သိမ်းပြီးပါပြီ! ❤️{RST}")
            else:
                print(f"\n{YEL}⚠️  အရင်ကတည်းက ရှိပြီးသားဖြစ်ပါတယ်{RST}")
        time.sleep(1.5)
    else:
        print(f"\n{RED}❌ အလုပ်လုပ်နိုင်တဲ့ဆာဗာ မတွေ့ပါ{RST}")
        time.sleep(1.5)

def show_favorites():
    clear()
    print(PUR + "="*60 + RST)
    print(PUR + "|        ❤️  အကြိုက်ဆုံး ကီးများစာရင်း        |" + RST)
    print(PUR + "-"*60 + RST)
    if not favorites:
        print(f"\n  {DIM}အကြိုက်ဆုံးထဲ ဘာမှမရှိသေးပါ{RST}")
    else:
        print(f"  စုစုပေါင်း: {len(favorites)} ခု\n")
        for idx, url in enumerate(favorites, 1):
            short = url[:50] + "..." if len(url) > 50 else url
            print(f"  [{idx}] {short}")
            print(f"      အပြည့်အဝကြည့်ရန်- cat favorites.txt\n")
    input(f"{CYN}ပြန်ရန် Enter နှိပ်ပါ...{RST}")

def main():
    vless, ss = [], []
    while True:
        clear()
        net_type = get_net()
        total_keys = len(vless) + len(ss)
        print(PUR + "="*60 + RST)
        print(PUR + "|     🚀 VPN Key Finder - Premium Edition     |" + RST)
        print(PUR + "-"*60 + RST)
        print(f"  📡 လိုင်းအမျိုးအစား: {CYN}{net_type}{RST}")
        print(f"  🔑 ရရှိပြီးသားကီး: {GRN}{total_keys}{RST} ခု")
        print(PUR + "-"*60 + RST)
        print(f"  [1] 🔄 ရင်းမြစ်များအားလုံးကို ဖတ်ရန်")
        print(f"  [2] 🟦 VLESS ဆာဗာများ ကြည့်ရန်")
        print(f"  [3] 🟪 SS ဆာဗာများ ကြည့်ရန်")
        print(f"  [4] 🏆 အကောင်းဆုံးဆာဗာ ရှာရန်")
        print(f"  [5] ❤️  အကြိုက်ဆုံးများ ကြည့်ရန်")
        print(f"  [6] 📘 Admin ဆီဆက်သွယ်ရန်")
        print(PUR + "-"*60 + RST)
        print(f"  [0] ❌ ပိတ်ရန်")
        print(PUR + "="*60 + RST)
        choice = input(f"\n  ရွေးချယ်ပါ → ")
        
        if choice == "0":
            clear()
            print(f"\n  {GRN}Goodbye! 👋{RST}\n")
            break
        elif choice == "1":
            vless, ss = load_all()
        elif choice == "2":
            scan_and_show(vless, "VLESS ဆာဗာများ - အလျင်စဥ်", 20)
        elif choice == "3":
            scan_and_show(ss, "SS ဆာဗာများ - အလျင်စဥ်", 20)
        elif choice == "4":
            best_for_me(vless + ss)
        elif choice == "5":
            show_favorites()
        elif choice == "6":
            open_admin_link()
        else:
            print(f"\n  {RED}⚠️  ရွေးချယ်မှုမှားနေပါတယ်{RST}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print(f"\n\n  {GRN}ပရိုဂရမ်မှ ထွက်သွားပါပြီ{RST}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n  {RED}အမှားအယွင်း: {e}{RST}")
        input(f"  ပြန်ရန် Enter နှိပ်ပါ...")
    
