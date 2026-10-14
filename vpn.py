#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import base64
import os
import socket
import time
import json
from datetime import datetime

VERSION = "DIAMOND PREMIUM 3.0 💎"
FAV_FILE = os.path.expanduser("~/.vpn_favorites.json")

# ==================================================
# 💎 DIAMOND PREMIUM — Color Palette
# ==================================================
class Colors:
    DIAMOND = "\033[38;5;159m"
    GOLD = "\033[38;5;220m"
    GOLD_BRIGHT = "\033[38;5;229m"
    PLATINUM = "\033[38;5;252m"
    SILVER = "\033[38;5;248m"
    SAPPHIRE = "\033[38;5;45m"
    EMERALD = "\033[38;5;49m"
    RUBY = "\033[38;5;196m"
    AMBER = "\033[38;5;214m"
    GRAPHITE = "\033[38;5;240m"
    WHITE = "\033[38;5;255m"
    BG_DARK = "\033[48;5;234m"
    BORDER = "\033[38;5;59m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    BLINK = "\033[5m"

def clear(): os.system("clear")

def line():
    return f"{Colors.BORDER}╚{'═' * 50}╝{Colors.RESET}"

def line_top():
    return f"{Colors.BORDER}╔{'═' * 50}╗{Colors.RESET}"

def line_mid():
    return f"{Colors.BORDER}╠{'─' * 50}╣{Colors.RESET}"

# ==================================================
# 💎 DIAMOND LOGO
# ==================================================
def show_logo():
    clear()
    print(f"""
{Colors.BORDER}╔══════════════════════════════════════════════════╗
{Colors.BORDER}║{Colors.RESET}                                                    {Colors.BORDER}║
{Colors.BORDER}║{Colors.RESET}        {Colors.DIAMOND}{Colors.BOLD}💎 VPN KEY FINDER{Colors.RESET}                    {Colors.BORDER}║
{Colors.BORDER}║{Colors.RESET}           {Colors.GOLD}DIAMOND PREMIUM EDITION{Colors.RESET}               {Colors.BORDER}║
{Colors.BORDER}║{Colors.RESET}      {Colors.SAPPHIRE}✦ Fast  •  ✦ Stable  •  ✦ Secure{Colors.RESET}           {Colors.BORDER}║
{Colors.BORDER}║{Colors.RESET}                                                    {Colors.BORDER}║
{Colors.BORDER}╚══════════════════════════════════════════════════╝{Colors.RESET}

{Colors.PLATINUM}┌────────────────────────────────────────────────────┐{Colors.RESET}
{Colors.PLATINUM}│{Colors.RESET} {Colors.SAPPHIRE}📌 Version{Colors.RESET}     : {Colors.GOLD}{VERSION}{Colors.RESET}
{Colors.PLATINUM}│{Colors.RESET} {Colors.SAPPHIRE}🕐 Updated{Colors.RESET}     : {Colors.SILVER}{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}{Colors.RESET}
{Colors.PLATINUM}│{Colors.RESET} {Colors.SAPPHIRE}👑 Status{Colors.RESET}      : {Colors.EMERALD}● ONLINE & READY{Colors.RESET}
{Colors.PLATINUM}└────────────────────────────────────────────────────┘{Colors.RESET}
""")

def show_section(title, icon):
    show_logo()
    print(f"""
{Colors.PLATINUM}┌────────────────────────────────────────────────────┐{Colors.RESET}
{Colors.PLATINUM}│{Colors.RESET}  {icon}  {Colors.BOLD}{Colors.DIAMOND}{title}{Colors.RESET}
{Colors.PLATINUM}└────────────────────────────────────────────────────┘{Colors.RESET}
""")

# ==================================================
# ⭐ Favorites System
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
        return False
    fav_item = {
        "name": item["name"],
        "key": item["key"],
        "proto": item.get("proto", "UNKNOWN"),
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    favs.insert(0, fav_item)
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(favs, f, ensure_ascii=False, indent=2)
    return True

def copy_text(text):
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", text])
        return True
    except:
        return False

# ==================================================
# 📋 Sources
# ==================================================
SOURCES = [
    {"name": "Shadowmere", "url": "https://shadowmere.xyz/api/b64sub/", "type": "b64"},
    {"name": "Epodonios VLESS", "url": "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/vless.txt", "type": "txt"},
    {"name": "Epodonios SS", "url": "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/ss.txt", "type": "txt"},
    {"name": "MatinGhanbari VLESS", "url": "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/vless.txt", "type": "txt"},
    {"name": "MatinGhanbari SS", "url": "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/ss.txt", "type": "txt"},
    {"name": "Argh73 Vault", "url": "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "type": "txt"}
]

# ==================================================
# 📥 Data Fetch & Parse
# ==================================================
def fetch_source(src):
    try:
        req = urllib.request.Request(
            src["url"],
            headers={"User-Agent": "Mozilla/5.0 (Android; Mobile)"}
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", errors="ignore")
    except:
        return None

def parse_configs(content, src_type):
    keys = []
    if not content: return keys
    if src_type == "b64":
        try:
            content = base64.b64decode(content).decode("utf-8", errors="ignore")
        except: pass
    
    for line in content.splitlines():
        line = line.strip()
        if not line: continue
        proto = None
        if line.startswith("vless://"): proto = "VLESS"
        elif line.startswith("ss://"): proto = "SS"
        elif line.startswith("vmess://"): proto = "VMESS"
        if not proto: continue
        
        name = f"{proto} Server"
        if "#" in line:
            try:
                from urllib.parse import unquote
                name = unquote(line.split("#")[-1])[:50]
            except:
                name = line.split("#")[-1][:50]
        keys.append({"name": name, "key": line, "proto": proto})
    return keys

# ==================================================
# 📊 Ping & Country
# ==================================================
def get_host(key):
    try:
        from urllib.parse import urlparse
        u = urlparse(key)
        return u.hostname or "", u.port or 443
    except: return "", 443

def ping_server(host, port=443, timeout=0.8):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        st = time.time()
        s.connect((host, int(port)))
        s.close()
        return round((time.time() - st) * 1000)
    except: return 9999

def get_country_flag(name):
    n = name.lower()
    if "singapore" in n or "sg" in n: return "🇸🇬 SG"
    if "malaysia" in n or "my" in n: return "🇲🇾 MY"
    if "thai" in n or "th" in n: return "🇹🇭 TH"
    if "vietnam" in n or "vn" in n: return "🇻🇳 VN"
    if "hongkong" in n or "hk" in n: return "🇭🇰 HK"
    if "japan" in n or "jp" in n: return "🇯🇵 JP"
    if "korea" in n or "kr" in n: return "🇰🇷 KR"
    if "india" in n or "in" in n: return "🇮🇳 IN"
    if "uk" in n or "gb" in n or "london" in n: return "🇬🇧 UK"
    if "usa" in n or "us" in n: return "🇺🇸 US"
    return "🌐 --"

def ping_badge(ms):
    if ms == 9999: return f"{Colors.RUBY}✖ OFFLINE{Colors.RESET}"
    if ms < 100: return f"{Colors.EMERALD}✦ {ms}ms  EXCELLENT{Colors.RESET}"
    if ms < 200: return f"{Colors.SAPPHIRE}✦ {ms}ms  GOOD{Colors.RESET}"
    if ms < 350: return f"{Colors.AMBER}✦ {ms}ms  FAIR{Colors.RESET}"
    return f"{Colors.RUBY}✦ {ms}ms  SLOW{Colors.RESET}"

# ==================================================
# 🔍 Load & Scan
# ==================================================
def load_all_keys():
    all_keys = []
    seen = set()
    
    show_section("ကီးများရယူနေသည်", "📡")
    print(f"  {Colors.GRAPHITE}အရင်းအမြစ်များကို ချိတ်ဆက်နေသည်...{Colors.RESET}\n")
    
    for idx, src in enumerate(SOURCES, 1):
        print(f"  {Colors.PLATINUM}│{Colors.RESET} {Colors.SAPPHIRE}[{idx}/{len(SOURCES)}]{Colors.RESET}  {Colors.PLATINUM}{src['name']:<22}{Colors.RESET}", end=" ")
        content = fetch_source(src)
        if content:
            keys = parse_configs(content, src["type"])
            new_count = 0
            for k in keys:
                if k["key"] not in seen:
                    seen.add(k["key"])
                    all_keys.append(k)
                    new_count += 1
            print(f"{Colors.EMERALD}✓ +{new_count}{Colors.RESET}")
        else:
            print(f"{Colors.RUBY}✖ FAILED{Colors.RESET}")
    
    print()
    if len(all_keys) == 0:
        print(f"  {Colors.RUBY}✖ ကီးမရရှိပါ။ နောက်မှတစ်ခါပြန်ကြိုးစားပါ။{Colors.RESET}\n")
    else:
        print(f"  {Colors.DIAMOND}💎 စုစုပေါင်း ကီး {Colors.BOLD}{len(all_keys)}{Colors.RESET}{Colors.DIAMOND} ခု အဆင်သင့်ဖြစ်ပါပြီ။{Colors.RESET}\n")
    time.sleep(1.2)
    return all_keys

def find_best(keys, limit=15):
    show_section("လိုင်းကောင်းဆာဗာများကို ရွေးချယ်နေသည်", "⚡")
    print(f"  {Colors.GRAPHITE}Ping စစ်ဆေးနေသည်... စက္ကန့်အနည်းငယ် စောင့်ပါ။{Colors.RESET}\n")
    
    results = []
    total = min(len(keys), limit)
    
    for i in range(total):
        k = keys[i]
        host, port = get_host(k["key"])
        ms = ping_server(host, port) if host else 9999
        results.append({"name": k["name"], "key": k["key"], "proto": k["proto"], "ms": ms})
        pct = int((i+1)/total*100)
        filled = "█" * int(pct/5)
        empty = "░" * (20 - int(pct/5))
        print(f"  {Colors.SAPPHIRE}တိုးတက်မှု: │{filled}{empty}│ {pct}%{Colors.RESET}", end="\r")
    
    print("\n\n")
    good = [r for r in results if r["ms"] < 400]
    good.sort(key=lambda x: x["ms"])
    return good

# ==================================================
# 📋 Display Functions
# ==================================================
def show_results(good, title="ရလဒ်များ"):
    if not good:
        print(f"  {Colors.AMBER}⚠️ လိုင်းကောင်းဆာဗာ မတွေ့ပါ။ ပြန်စကင်န်ဖတ်ကြည့်ပါ။{Colors.RESET}\n")
        return None
    
    print(f"  {Colors.DIAMOND}🏆 {title}  (အရေအတွက်: {len(good)}){Colors.RESET}\n")
    print(f"  {Colors.PLATINUM}┌─────┬──────────┬──────────────────────┬──────────────────────┐{Colors.RESET}")
    print(f"  {Colors.PLATINUM}│{Colors.RESET} {Colors.GOLD}# {Colors.RESET}│ {Colors.GOLD}နိုင်ငံ{Colors.RESET}   │ {Colors.GOLD}Ping{Colors.RESET:<22}      │ {Colors.GOLD}အမည်{Colors.RESET:<22}        {Colors.PLATINUM}│{Colors.RESET}")
    print(f"  {Colors.PLATINUM}├─────┼──────────┼──────────────────────┼──────────────────────┤{Colors.RESET}")
    
    for i, r in enumerate(good, 1):
        flag = get_country_flag(r["name"])
        print(f"  {Colors.PLATINUM}│{Colors.RESET} {Colors.SILVER}{i:<2}{Colors.RESET} │ {flag:<8} │ {ping_badge(r['ms']):<26}{Colors.RESET} │ {r['name'][:22]:<22} {Colors.PLATINUM}│{Colors.RESET}")
    
    print(f"  {Colors.PLATINUM}└─────┴──────────┴──────────────────────┴──────────────────────┘{Colors.RESET}\n")
    return good

def copy_and_display(server_list, limit=3):
    if not server_list: return
    top = server_list[:limit]
    
    print(f"  {Colors.GOLD}📌 အကောင်းဆုံး {len(top)} ခု၏ ကီးများ{Colors.RESET}")
    print(f"  {Colors.PLATINUM}─" * 52 + Colors.RESET + "\n")
    
    all_keys_text = "\n\n".join([r["key"] for r in top])
    print(all_keys_text)
    
    print(f"\n  {Colors.PLATINUM}─" * 52 + Colors.RESET)
    copied = copy_text(all_keys_text)
    
    if copied:
        print(f"  {Colors.EMERALD}✓ ကီးများကို ကလစ်ဘုတ်သို့ ကူးယူပြီးပါပြီ!{Colors.RESET}")
        print(f"  {Colors.SAPPHIRE}💡 V2RayNG / NekoBox → + → Import from Clipboard{Colors.RESET}")
    else:
        print(f"  {Colors.AMBER}⚠️ အထက်ကကီးကို ကိုယ်တိုင်ကူးယူပါ။{Colors.RESET}")
    print()
    return top

def show_favorites():
    while True:
        favs = load_favorites()
        show_section("အကြိုက်ဆုံးဆာဗာများ", "⭐")
        
        if not favs:
            print(f"  {Colors.AMBER}⚠️ အကြိုက်ဆုံး မသိမ်းရသေးပါ။ ကီးတစ်ခုရွေးပြီး သိမ်းထားနိုင်ပါတယ်။{Colors.RESET}\n")
        else:
            print(f"  {Colors.GOLD}💎 စုစုပေါင်း: {len(favs)} ခု{Colors.RESET}\n")
            for i, f in enumerate(favs, 1):
                flag = get_country_flag(f["name"])
                print(f"  {Colors.SAPPHIRE}[{i}]{Colors.RESET} {flag}  {Colors.PLATINUM}{f['name'][:40]}{Colors.RESET}")
                print(f"      {Colors.GRAPHITE}💾 {f['saved_at']}{Colors.RESET}")
                print(f"      {Colors.GRAPHITE}{f['key'][:60]}...{Colors.RESET}\n")
        
        print(f"  {Colors.GOLD}နံပါတ်ထည့်ပါ{Colors.RESET} = ကီးကူးယူမည်    {Colors.RUBY}[0] = ပင်မည်{Colors.RESET}\n")
        sel = input(f"  {Colors.DIAMOND}ရွေးချယ်ပါ → {Colors.RESET}").strip()
        
        if sel == "0": break
        if sel.isdigit() and favs:
            idx = int(sel) - 1
            if 0 <= idx < len(favs):
                copy_text(favs[idx]["key"])
                print(f"  {Colors.EMERALD}✓ ကီးကူးယူပြီးပါပြီ!{Colors.RESET}\n")
                time.sleep(1)

def network_guide():
    show_section("ကွန်ရက်အကြံပြုချက်", "📱")
    print(f"  {Colors.GOLD}ကွန်ရက်အလိုက် အကောင်းဆုံးနိုင်ငံ{Colors.RESET}\n")
    print(f"  {Colors.SAPPHIRE}▸ MPT      {Colors.RESET}→ 🇸🇬 SG  စင်ကာပူ   /   🇹🇭 TH  ထိုင်း")
    print(f"  {Colors.SAPPHIRE}▸ Ooredoo  {Colors.RESET}→ 🇸🇬 SG  စင်ကာပူ   /   🇲🇾 MY  မလေးရှား")
    print(f"  {Colors.SAPPHIRE}▸ Telenor  {Colors.RESET}→ 🇸🇬 SG  စင်ကာပူ   /   🇲🇾 MY  မလေးရှား")
    print(f"  {Colors.SAPPHIRE}▸ Mytel    {Colors.RESET}→ 🇹🇭 TH  ထိုင်း     /   🇻🇳 VN  ဗီယက်နမ်")
    print(f"  {Colors.SAPPHIRE}▸ WiFi     {Colors.RESET}→ 🇸🇬 SG  စင်ကာပူ   အမြဲပိုမိုမြန်ဆန်တယ်")
    print()
    print(f"  {Colors.GRAPHITE}စံနှုန်း: Ping < 100ms = အကောင်းဆုံး  |  100-200ms = ကောင်း  |  200-400ms = အတန်းအစား  |  >400ms = ပြောင်းသင့်{Colors.RESET}\n")
    input(f"  {Colors.SAPPHIRE}ပင်မမီနူးသို့ပြန်ရန် Enter...{Colors.RESET}")

# ==================================================
# 🏠 MAIN MENU
# ==================================================
def main():
    all_keys = load_all_keys()
    vless_keys = [k for k in all_keys if k["proto"] == "VLESS"]
    ss_keys = [k for k in all_keys if k["proto"] == "SS"]
    vmess_keys = [k for k in all_keys if k["proto"] == "VMESS"]
    
    while True:
        show_logo()
        print(f"  {Colors.DIAMOND}💎 ပင်မမီနူး{Colors.RESET}\n")
        print(f"  {Colors.PLATINUM}┌────────────────────────────────────────────────────┐{Colors.RESET}")
        print(f"  {Colors.PLATINUM}│{Colors.RESET}  🟦 VLESS: {Colors.GOLD}{len(vless_keys):<4}{Colors.RESET}  🟩 SS: {Colors.GOLD}{len(ss_keys):<4}{Colors.RESET}  🟧 VMESS: {Colors.GOLD}{len(vmess_keys):<4}{Colors.RESET}        {Colors.PLATINUM}│{Colors.RESET}")
        print(f"  {Colors.PLATINUM}├────────────────────────────────────────────────────┤{Colors.RESET}")
        print(f"  {Colors.PLATINUM}│{Colors.RESET}  {Colors.GOLD}[1]{Colors.RESET}  ⚡ အကောင်းဆုံး VLESS ကို ရှာမည်                     {Colors.PLATINUM}│{Colors.RESET}")
        print(f"  {Colors.PLATINUM}│{Colors.RESET}  {Colors.GOLD}[2]{Colors.RESET}  🟩 အကောင်းဆုံး SS ကို ရှာမည်                       {Colors.PLATINUM}│{Colors.RESET}")
        print(f"  {Colors.PLATINUM}│{Colors.RESET}  {Colors.GOLD}[3]{Colors.RESET}  🏆 အားလုံးထဲမှ အကောင်းဆုံး ၃ ခု                   {Colors.PLATINUM}│{Colors.RESET}")
        print(f"  {Colors.PLATINUM}│{Colors.RESET}  {Colors.GOLD}[4]{Colors.RESET}  ⭐ အကြိုက်ဆုံးဆာဗာများ                            {Colors.PLATINUM}│{Colors.RESET}")
        print(f"  {Colors.PLATINUM}│{Colors.RESET}  {Colors.GOLD}[5]{Colors.RESET}  📱 ကွန်ရက်အကြံပြုချက်                              {Colors.PLATINUM}│{Colors.RESET}")
        print(f"  {Colors.PLATINUM}│{Colors.RESET}  {Colors.GOLD}[6]{Colors.RESET}  🔄 ကီးအသစ်ပြန်ဖတ်မည်                            {Colors.PLATINUM}│{Colors.RESET}")
        print(f"  {Colors.PLATINUM}│{Colors.RESET}  {Colors.RUBY}[0]{Colors.RESET}  ✖ ပရိုဂရမ်မှထွက်မည်                             {Colors.PLATINUM}│{Colors.RESET}")
        print(f"  {Colors.PLATINUM}└────────────────────────────────────────────────────┘{Colors.RESET}\n")
        
        sel = input(f"  {Colors.DIAMOND}ရွေးချယ်ပါ → {Colors.RESET}").strip()
        
        if sel == "1":
            if not vless_keys:
                print(f"  {Colors.AMBER}⚠️ VLESS ကီးမရှိပါ။ အခြားအမျိုးအစားကို ကြည့်ပါ။{Colors.RESET}\n")
                time.sleep(1.5)
                continue
            good = find_best(vless_keys)
            show_results(good, "VLESS ဆာဗာများ")
            if good:
                copy_and_display(good)
                if input(f"  {Colors.SAPPHIRE}အကောင်းဆုံးကို အကြိုက်ဆုံးထဲသိမ်းမလား? (y/n) → {Colors.RESET}").strip().lower() == "y":
                    save_favorite(good[0])
                    print(f"  {Colors.EMERALD}✓ သိမ်းပြီးပါပြီ! ⭐{Colors.RESET}\n")
            input(f"  {Colors.SAPPHIRE}ပင်မမီနူးသို့ပြန်ရန် Enter...{Colors.RESET}")
        
        elif sel == "2":
            if not ss_keys:
                print(f"  {Colors.AMBER}⚠️ SS ကီးမရှိပါ။ အခြားအမျိုးအစားကို ကြည့်ပါ။{Colors.RESET}\n")
                time.sleep(1.5)
                continue
            good = find_best(ss_keys)
            show_results(good, "SS ဆာဗာများ")
            if good:
                copy_and_display(good)
                if input(f"  {Colors.SAPPHIRE}အကောင်းဆုံးကို အကြိုက်ဆုံးထဲသိမ်းမလား? (y/n) → {Colors.RESET}").strip().lower() == "y":
                    save_favorite(good[0])
                    print(f"  {Colors.EMERALD}✓ သိမ်းပြီးပါပြီ! ⭐{Colors.RESET}\n")
            input(f"  {Colors.SAPPHIRE}ပင်မမီနူးသို့ပြန်ရန် Enter...{Colors.RESET}")
        
        elif sel == "3":
            if not all_keys:
                print(f"  {Colors.AMBER}⚠️ ကီးမရှိပါ။ အရင်ဖတ်ပါ။{Colors.RESET}\n")
                time.sleep(1.5)
                continue
            good = find_best(all_keys, limit=20)
            show_results(good, "အားလုံးမှ အကောင်းဆုံး")
            if good:
                copy_and_display(good, limit=3)
            input(f"  {Colors.SAPPHIRE}ပင်မမီနူးသို့ပြန်ရန် Enter...{Colors.RESET}")
        
        elif sel == "4":
            show_favorites()
        
        elif sel == "5":
            network_guide()
        
        elif sel == "6":
            all_keys = load_all_keys()
            vless_keys = [k for k in all_keys if k["proto"] == "VLESS"]
            ss_keys = [k for k in all_keys if k["proto"] == "SS"]
            vmess_keys = [k for k in all_keys if k["proto"] == "VMESS"]
        
        elif sel == "0":
            show_logo()
            print(f"  {Colors.DIAMOND}💎 အသုံးပြုတာကျေးဇူးတင်ပါတယ်!{Colors.RESET}")
            print(f"  {Colors.SAPPHIRE}      ပျော်ရွှင်ဖွယ်အသုံးပြုမှုဖြစ်ပါစေ။{Colors.RESET}\n")
            break
        
        else:
            print(f"  {Colors.RUBY}✖ ရွေးချယ်မှုမှားနေပါသည်။ 0-6 ကြားသာထည့်ပါ။{Colors.RESET}\n")
            time.sleep(1.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {Colors.DIAMOND}💎 ပရိုဂရမ်မှ ထွက်သွားပါပြီ{Colors.RESET}\n")
    except Exception as e:
        print(f"\n  {Colors.RUBY}အမှားအယွင်း: {str(e)}{Colors.RESET}\n")
        input(f"  ဆက်ရန် Enter...")
    
