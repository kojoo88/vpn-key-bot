#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import base64
import os
import socket
import time
import json
from datetime import datetime

VERSION = "LUXURY PREMIUM 2.0 👑"
FAV_FILE = os.path.expanduser("~/.vpn_favorites.json")

# ==================================================
# 🎨 ပရီမီယံ အရောင်နှင့် ဒီဇိုင်း
# ==================================================
class Colors:
    GOLD = "\033[38;5;226m"
    GOLD_DARK = "\033[38;5;214m"
    SILVER = "\033[38;5;250m"
    CYAN = "\033[38;5;45m"
    TEAL = "\033[38;5;37m"
    EMERALD = "\033[38;5;41m"
    LIME = "\033[38;5;118m"
    ORANGE = "\033[38;5;208m"
    RED_SOFT = "\033[38;5;196m"
    PURPLE = "\033[38;5;147m"
    PINK = "\033[38;5;213m"
    DIM = "\033[38;5;245m"
    BG_DARK = "\033[48;5;234m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"

def clear(): os.system("clear")

def separator(char="━", length=52):
    return f"{Colors.GOLD_DARK}{char * length}{Colors.RESET}"

def separator_light():
    return f"{Colors.DIM}─" * 52 + Colors.RESET

# ==================================================
# 👑 လိုဂိုနှင့် Header
# ==================================================
def show_logo():
    clear()
    print(f"""
{Colors.GOLD}    ╔══════════════════════════════════════════════════╗
{Colors.GOLD}    ║{Colors.RESET}        {Colors.GOLD}👑 VPN KEY FINDER{Colors.RESET}  {Colors.PURPLE}— PREMIUM EDITION{Colors.RESET}          {Colors.GOLD}║
{Colors.GOLD}    ║{Colors.RESET}           {Colors.DIM}Fast • Stable • Premium Quality{Colors.RESET}               {Colors.GOLD}║
{Colors.GOLD}    ╚══════════════════════════════════════════════════╝{Colors.RESET}
{Colors.CYAN}    ● Version  : {Colors.SILVER}{VERSION}{Colors.RESET}
{Colors.CYAN}    ● Updated  : {Colors.SILVER}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}
{Colors.RESET}""")
    print()

def show_header(title):
    show_logo()
    print(f"{Colors.GOLD}    ┌{'─' * 50}┐{Colors.RESET}")
    print(f"{Colors.GOLD}    │{Colors.RESET}  {Colors.BOLD}{Colors.GOLD}{title}{Colors.RESET}")
    print(f"{Colors.GOLD}    └{'─' * 50}┘{Colors.RESET}\n")

# ==================================================
# ⭐ အကြိုက်ဆုံးများ
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
        "proto": item.get("proto", "unknown"),
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M")
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
# 📋 အရင်းအမြစ်များ
# ==================================================
SOURCES = [
    {"name": "Shadowmere", "url": "https://shadowmere.xyz/api/b64sub/", "type": "b64"},
    {"name": "Epodonios VLESS", "url": "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/vless.txt", "type": "txt"},
    {"name": "Epodonios SS", "url": "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/ss.txt", "type": "txt"},
    {"name": "MatinGhanbari VLESS", "url": "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/vless.txt", "type": "txt"},
    {"name": "MatinGhanbari SS", "url": "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/ss.txt", "type": "txt"},
    {"name": "Argh73 All", "url": "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "type": "txt"}
]

# ==================================================
# 📥 ဒေတာဖတ်ခြင်း
# ==================================================
def fetch_source(src):
    try:
        req = urllib.request.Request(src["url"], headers={"User-Agent": "Mozilla/5.0 (Android; Mobile)"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", errors="ignore")
    except:
        return None

def parse_configs(content, src_type):
    keys = []
    if not content: return keys
    if src_type == "b64":
        try: content = base64.b64decode(content).decode("utf-8", errors="ignore")
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
                name = unquote(line.split("#")[-1])[:45]
            except:
                name = line.split("#")[-1][:45]
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

def ping_result(ms):
    if ms == 9999: return f"{Colors.RED_SOFT}✖ Offline{Colors.RESET}"
    if ms < 100: return f"{Colors.LIME}● {ms}ms  Excellent{Colors.RESET}"
    if ms < 200: return f"{Colors.EMERALD}● {ms}ms  Good{Colors.RESET}"
    if ms < 350: return f"{Colors.ORANGE}● {ms}ms  Fair{Colors.RESET}"
    return f"{Colors.RED_SOFT}● {ms}ms  Slow{Colors.RESET}"

# ==================================================
# 🔍 ကီးများရယူခြင်း
# ==================================================
def load_all_keys():
    all_keys = []
    seen = set()
    
    show_header("📡  ကီးများရယူနေသည်")
    print(f"  {Colors.DIM}အရင်းအမြစ်များကို ချိတ်ဆက်နေသည်...{Colors.RESET}\n")
    
    for idx, src in enumerate(SOURCES, 1):
        print(f"  {Colors.CYAN}[{idx}/{len(SOURCES)}]{Colors.RESET}  {Colors.SILVER}{src['name']:<20}{Colors.RESET}", end=" ")
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
            print(f"{Colors.ORANGE}— ကျော်သွား{Colors.RESET}")
    
    print()
    if len(all_keys) == 0:
        print(f"  {Colors.RED_SOFT}✖ ကီးမရရှိပါ။ နောက်မှတစ်ခါပြန်ကြိုးစားပါ။{Colors.RESET}")
    else:
        print(f"  {Colors.GOLD}👑 စုစုပေါင်း ကီး {len(all_keys)} ခု အဆင်သင့်ဖြစ်ပါပြီ။{Colors.RESET}")
    time.sleep(1.5)
    return all_keys

def find_best_servers(keys, limit=15):
    show_header("⚡  လိုင်းကောင်းဆာဗာများကို ရွေးချယ်နေသည်")
    print(f"  {Colors.DIM}Ping စစ်ဆေးနေသည်... စက္ကန့်အနည်းငယ် စောင့်ပါ။{Colors.RESET}\n")
    
    results = []
    total = min(len(keys), limit)
    
    for i in range(total):
        k = keys[i]
        host, port = get_host(k["key"])
        ms = ping_server(host, port) if host else 9999
        results.append({"name": k["name"], "key": k["key"], "proto": k["proto"], "ms": ms})
        percent = int((i+1)/total*100)
        bar = "█" * int(percent/5)
        print(f"  {Colors.CYAN}တိုးတက်မှု: [{bar}{' '*(20-int(percent/5))}] {percent}%{Colors.RESET}", end="\r")
    
    print("\n\n")
    good = [r for r in results if r["ms"] < 400]
    good.sort(key=lambda x: x["ms"])
    return good

# ==================================================
# 📋 ပြသခြင်းများ
# ==================================================
def show_server_list(good_keys, title="ရလဒ်များ"):
    if not good_keys:
        print(f"  {Colors.ORANGE}⚠️ လိုင်းကောင်းဆာဗာ မတွေ့ပါ။ ပြန်စကင်န်ဖတ်ကြည့်ပါ။{Colors.RESET}\n")
        return None
    
    print(f"  {Colors.GOLD}🏆 {title}  (အရေအတွက်: {len(good_keys)}){Colors.RESET}\n")
    print(f"  {Colors.CYAN}┌─────┬──────────┬────────┬──────────────────────┐{Colors.RESET}")
    print(f"  {Colors.CYAN}│{Colors.RESET} {Colors.GOLD}နံပါတ်{Colors.RESET} │ {Colors.GOLD}နိုင်ငံ{Colors.RESET}   │ {Colors.GOLD}Ping{Colors.RESET}     │ {Colors.GOLD}အမည်{Colors.RESET:<22} {Colors.CYAN}│{Colors.RESET}")
    print(f"  {Colors.CYAN}├─────┼──────────┼────────┼──────────────────────┤{Colors.RESET}")
    
    for i, r in enumerate(good_keys, 1):
        flag = get_country_flag(r["name"])
        ms_text = f"{r['ms']}ms" if r['ms'] != 9999 else "—"
        print(f"  {Colors.CYAN}│{Colors.RESET}  {Colors.SILVER}{i:<3}{Colors.RESET} │ {flag:<8} │ {ping_result(r['ms']):<20}{Colors.RESET} │ {r['name'][:22]:<22} {Colors.CYAN}│{Colors.RESET}")
    
    print(f"  {Colors.CYAN}└─────┴──────────┴────────┴──────────────────────┘{Colors.RESET}\n")
    return good_keys

def copy_and_show_keys(server_list, limit=3):
    if not server_list: return
    top = server_list[:limit]
    
    print(f"  {Colors.GOLD}📌 အကောင်းဆုံး {len(top)} ခု၏ ကီးများ{Colors.RESET}")
    print(separator_light())
    
    all_keys_text = "\n\n".join([r["key"] for r in top])
    print(all_keys_text)
    
    print(separator_light())
    copied = copy_text(all_keys_text)
    
    if copied:
        print(f"  {Colors.EMERALD}✓ ကီးများကို ကလစ်ဘုတ်သို့ ကူးယူပြီးပါပြီ!{Colors.RESET}")
        print(f"  {Colors.CYAN}💡 V2RayNG / NekoBox → + → Import from Clipboard{Colors.RESET}")
    else:
        print(f"  {Colors.ORANGE}⚠️ အထက်ကကီးကို ကိုယ်တိုင်ကူးယူပါ။{Colors.RESET}")
    print()
    return top

def show_favorites_menu():
    while True:
        favs = load_favorites()
        show_header("⭐  အကြိုက်ဆုံးဆာဗာများ")
        
        if not favs:
            print(f"  {Colors.ORANGE}⚠️ အကြိုက်ဆုံး မသိမ်းရသေးပါ။{Colors.RESET}\n")
        else:
            print(f"  {Colors.GOLD}စုစုပေါင်း: {len(favs)} ခု{Colors.RESET}\n")
            for i, f in enumerate(favs, 1):
                flag = get_country_flag(f["name"])
                print(f"  {Colors.CYAN}[{i}]{Colors.RESET} {flag}  {Colors.SILVER}{f['name'][:35]}{Colors.RESET}")
                print(f"      {Colors.DIM}💾 {f['saved_at']}{Colors.RESET}")
                print(f"      {Colors.DIM}{f['key'][:55]}...{Colors.RESET}")
                print()
        
        print(f"  {Colors.GOLD}နံပါတ်ထည့်ပါ = ကီးကူးယူမည်    {Colors.RED_SOFT}[0] = ပြန်သွားရန်{Colors.RESET}\n")
        sel = input(f"  {Colors.CYAN}ရွေးချယ်ပါ → {Colors.RESET}").strip()
        
        if sel == "0": break
        if sel.isdigit() and favs:
            idx = int(sel) - 1
            if 0 <= idx < len(favs):
                copy_text(favs[idx]["key"])
                print(f"  {Colors.EMERALD}✓ ကီးကူးယူပြီးပါပြီ!{Colors.RESET}\n")
                time.sleep(1)

def network_tips():
    show_header("📱  ကွန်ရက်အကြံပြုချက်")
    print(f"  {Colors.GOLD}ကွန်ရက်အလိုက် အကောင်းဆုံးနိုင်ငံ{Colors.RESET}\n")
    print(f"  {Colors.CYAN}MPT     {Colors.RESET}→ 🇸🇬 SG  စင်ကာပူ   သို့မဟုတ်  🇹🇭 TH  ထိုင်း")
    print(f"  {Colors.CYAN}Ooredoo {Colors.RESET}→ 🇸🇬 SG  စင်ကာပူ   သို့မဟုတ်  🇲🇾 MY  မလေးရှား")
    print(f"  {Colors.CYAN}Telenor {Colors.RESET}→ 🇸🇬 SG  စင်ကာပူ   သို့မဟုတ်  🇲🇾 MY  မလေးရှား")
    print(f"  {Colors.CYAN}Mytel   {Colors.RESET}→ 🇹🇭 TH  ထိုင်း     သို့မဟုတ်  🇻🇳 VN  ဗီယက်နမ်")
    print(f"  {Colors.CYAN}WiFi    {Colors.RESET}→ 🇸🇬 SG  စင်ကာပူ   အမြဲပိုမိုမြန်ဆန်တယ်")
    print()
    print(f"  {Colors.DIM}စည်းမျဉ်း: Ping < 200ms = အကောင်းဆုံး   |   200-400ms = အတန်းအစား   |   >400ms = ပြောင်းသင့်{Colors.RESET}\n")
    input(f"  {Colors.CYAN}ပြန်ရန် Enter...{Colors.RESET}")

# ==================================================
# 🏠 ပင်မမီနူး
# ==================================================
def main():
    all_keys = load_all_keys()
    vless_keys = [k for k in all_keys if k["proto"] == "VLESS"]
    ss_keys = [k for k in all_keys if k["proto"] == "SS"]
    vmess_keys = [k for k in all_keys if k["proto"] == "VMESS"]
    
    while True:
        show_logo()
        print(f"  {Colors.GOLD}👑 ပင်မမီနူး{Colors.RESET}\n")
        print(f"  {Colors.CYAN}┌──────────────────────────────────────────────┐{Colors.RESET}")
        print(f"  {Colors.CYAN}│{Colors.RESET}  🟦 VLESS: {Colors.GOLD}{len(vless_keys):<4}{Colors.RESET}  🟩 SS: {Colors.GOLD}{len(ss_keys):<4}{Colors.RESET}  🟧 VMESS: {Colors.GOLD}{len(vmess_keys):<4}{Colors.RESET}       {Colors.CYAN}│{Colors.RESET}")
        print(f"  {Colors.CYAN}├──────────────────────────────────────────────┤{Colors.RESET}")
        print(f"  {Colors.CYAN}│{Colors.RESET}  {Colors.GOLD}[1]{Colors.RESET}  ⚡ အကောင်းဆုံး VLESS ကို ရှာမည်                {Colors.CYAN}│{Colors.RESET}")
        print(f"  {Colors.CYAN}│{Colors.RESET}  {Colors.GOLD}[2]{Colors.RESET}  🟩 အကောင်းဆုံး SS ကို ရှာမည်                  {Colors.CYAN}│{Colors.RESET}")
        print(f"  {Colors.CYAN}│{Colors.RESET}  {Colors.GOLD}[3]{Colors.RESET}  🏆 အားလုံးထဲမှ အကောင်းဆုံး ၃ ခု              {Colors.CYAN}│{Colors.RESET}")
        print(f"  {Colors.CYAN}│{Colors.RESET}  {Colors.GOLD}[4]{Colors.RESET}  ⭐ အကြိုက်ဆုံးဆာဗာများ                     {Colors.CYAN}│{Colors.RESET}")
        print(f"  {Colors.CYAN}│{Colors.RESET}  {Colors.GOLD}[5]{Colors.RESET}  📱 ကွန်ရက်အကြံပြုချက်                       {Colors.CYAN}│{Colors.RESET}")
        print(f"  {Colors.CYAN}│{Colors.RESET}  {Colors.GOLD}[6]{Colors.RESET}  🔄 ကီးအသစ်ပြန်ဖတ်မည်                     {Colors.CYAN}│{Colors.RESET}")
        print(f"  {Colors.CYAN}│{Colors.RESET}  {Colors.RED_SOFT}[0]{Colors.RESET}  ❌ ထွက်ပါ                                {Colors.CYAN}│{Colors.RESET}")
        print(f"  {Colors.CYAN}└──────────────────────────────────────────────┘{Colors.RESET}\n")
        
        sel = input(f"  {Colors.GOLD}ရွေးချယ်ပါ → {Colors.RESET}").strip()
        
        if sel == "1":
            if not vless_keys:
                print(f"  {Colors.ORANGE}⚠️ VLESS ကီးမရှိပါ။ အခြားအမျိုးအစားကို ကြည့်ပါ။{Colors.RESET}\n")
                time.sleep(1.5)
                continue
            good = find_best_servers(vless_keys)
            show_server_list(good, "VLESS ဆာဗာများ")
            if good:
                copy_and_show_keys(good)
                if input(f"  {Colors.CYAN}အကောင်းဆုံးကို အကြိုက်ဆုံးထဲသိမ်းမလား? (y/n) → {Colors.RESET}").strip().lower() == "y":
                    save_favorite(good[0])
                    print(f"  {Colors.EMERALD}✓ သိမ်းပြီးပါပြီ! ⭐{Colors.RESET}\n")
            input(f"  {Colors.CYAN}ပြန်ရန် Enter...{Colors.RESET}")
        
        elif sel == "2":
            if not ss_keys:
                print(f"  {Colors.ORANGE}⚠️ SS ကီးမရှိပါ။ အခြားအမျိုးအစားကို ကြည့်ပါ။{Colors.RESET}\n")
                time.sleep(1.5)
                continue
            good = find_best_servers(ss_keys)
            show_server_list(good, "SS ဆာဗာများ")
            if good:
                copy_and_show_keys(good)
                if input(f"  {Colors.CYAN}အကောင်းဆုံးကို အကြိုက်ဆုံးထဲသိမ်းမလား? (y/n) → {Colors.RESET}").strip().lower() == "y":
                    save_favorite(good[0])
                    print(f"  {Colors.EMERALD}✓ သိမ်းပြီးပါပြီ! ⭐{Colors.RESET}\n")
            input(f"  {Colors.CYAN}ပြန်ရန် Enter...{Colors.RESET}")
        
        elif sel == "3":
            if not all_keys:
                print(f"  {Colors.ORANGE}⚠️ ကီးမရှိပါ။ အရင်ဖတ်ပါ။{Colors.RESET}\n")
                time.sleep(1.5)
                continue
            good = find_best_servers(all_keys, limit=20)
            show_server_list(good, "အားလုံးမှ အကောင်းဆုံး")
            if good:
                copy_and_show_keys(good, limit=3)
            input(f"  {Colors.CYAN}ပြန်ရန် Enter...{Colors.RESET}")
        
        elif sel == "4":
            show_favorites_menu()
        
        elif sel == "5":
            network_tips()
        
        elif sel == "6":
            all_keys = load_all_keys()
            vless_keys = [k for k in all_keys if k["proto"] == "VLESS"]
            ss_keys = [k for k in all_keys if k["proto"] == "SS"]
            vmess_keys = [k for k in all_keys if k["proto"] == "VMESS"]
        
        elif sel == "0":
            show_logo()
            print(f"  {Colors.GOLD}👑 အသုံးပြုတာကျေးဇူးတင်ပါတယ်!{Colors.RESET}")
            print(f"  {Colors.CYAN}      ပျော်ရွှင်ဖွယ်အသုံးပြုမှုဖြစ်ပါစေ။{Colors.RESET}\n")
            break
        
        else:
            print(f"  {Colors.RED_SOFT}✖ ရွေးချယ်မှုမှားနေပါသည်။ 0-6 ကြားသာထည့်ပါ။{Colors.RESET}\n")
            time.sleep(1.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {Colors.GOLD}👑 ပရိုဂရမ်မှ ထွက်သွားပါပြီ{Colors.RESET}\n")
    except Exception as e:
        print(f"\n  {Colors.RED_SOFT}အမှားအယွင်း: {str(e)}{Colors.RESET}\n")
        input(f"  ဆက်ရန် Enter...")
    
