#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, urllib.error, base64, os, socket, time, json, sys
from datetime import datetime

VERSION = "🚀 ALL-SOURCES EDITION v8.7"
FAV_FILE = os.path.expanduser("~/.vpn_premium.json")
FACEBOOK_LINK = "https://www.facebook.com/share/18jrazYpmS/"

class C:
    P = "\033[38;5;201m"
    G = "\033[38;5;46m"
    B = "\033[38;5;39m"
    Y = "\033[38;5;226m"
    O = "\033[38;5;208m"
    R = "\033[38;5;196m"
    W = "\033[38;5;255m"
    GR = "\033[38;5;245m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

def clear(): os.system("clear")

def premium_header():
    clear()
    print(f"""
{C.P}{C.BOLD}
╔══════════════════════════════════════════════════════════════╗
║   🚀  U L T R A   P R E M I U M   E D I T I O N              ║
║   {VERSION:^60}║
╠══════════════════════════════════════════════════════════════╣
║   ⚡ Fast VPN Key Finder • VLESS / SS / VMESS / TROJAN        ║
╚══════════════════════════════════════════════════════════════╝{C.RESET}""")
    now = datetime.now()
    print(f"  {C.G}📅 ရက်စွဲ:{C.RESET} {now.strftime('%Y-%m-%d')}   {C.G}⏰ အချိန်:{C.RESET} {now.strftime('%H:%M:%S')}")
    print(f"  {C.B}📘 Facebook:{C.RESET} {FACEBOOK_LINK}\n")

# ==============================================================
# 🔗 အရင်းအမြစ်အားလုံး — အရင်ဟာတွေ + အသစ်တွေ အားလုံးပါ
# ==============================================================
SOURCES = [
    # ⭐ အဓိက အရင်းအမြစ်များ
    ("Shadowmere B64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("Shadowmere RAW", "https://shadowmere.xyz/api/sub/", "txt"),
    ("V2Ray Seeker ALL", "https://raw.githubusercontent.com/v2ray-seeker/v2rayseeker/main/sub.txt", "txt"),
    ("V2Ray Seeker B64", "https://raw.githubusercontent.com/v2ray-seeker/v2rayseeker/main/sub.b64", "b64"),
    ("Free V2Ray ALL", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/all.txt", "txt"),
    ("SaeedDev V2Ray", "https://raw.githubusercontent.com/SaeedDev94/V2ray/main/all.txt", "txt"),
    ("Hossaini V2Ray", "https://raw.githubusercontent.com/hossaini/v2ray/main/sub.txt", "txt"),
    ("Awesome VPN Daily", "https://raw.githubusercontent.com/awesome-vpn/awesome-vpn/master/all", "txt"),
    ("Argh73 Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
    ("V2Ray Pool ALL", "https://raw.githubusercontent.com/v2ray-pool/v2ray-pool/main/sub.txt", "txt"),
    ("V2RayNG Free", "https://raw.githubusercontent.com/v2ray-ng/free/main/sub.txt", "txt"),
    ("IRCF Space", "https://raw.githubusercontent.com/ircfspace/ircf.github.io/main/configs.txt", "txt"),
    ("Config Collector ALL", "https://raw.githubusercontent.com/tahmaseb73/configs-collector-v2ray/refs/heads/main/data/sub/splitted/mixed_19.txt", "txt"),
    ("TGParse Mixed", "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/splitted/mixed", "txt"),
    ("MorpheusAdam", "https://raw.githubusercontent.com/morpheusadam/v2ray-config/main/subs/all.txt", "txt"),
    
    # 🟦 VLESS သီးသန့်
    ("Epodonios VLESS", "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/vless.txt", "txt"),
    ("MatinGhanbari VLESS", "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/vless.txt", "txt"),
    ("VLESS Hub", "https://raw.githubusercontent.com/ircfspace/vlesshub/main/vless.txt", "txt"),
    ("Config Collector VLESS", "https://raw.githubusercontent.com/tahmaseb73/configs-collector-v2ray/refs/heads/main/data/sub/protocols/vless.txt", "txt"),
    ("Free V2Ray VLESS", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/vless.txt", "txt"),
    ("V2Ray Seeker VLESS", "https://raw.githubusercontent.com/v2ray-seeker/v2rayseeker/main/vless.txt", "txt"),
    
    # 🟩 SS သီးသန့်
    ("Epodonios SS", "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/ss.txt", "txt"),
    ("MatinGhanbari SS", "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/ss.txt", "txt"),
    ("V2Ray Seeker SS", "https://raw.githubusercontent.com/v2ray-seeker/v2rayseeker/main/ss.txt", "txt"),
    ("Free V2Ray SS", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/ss.txt", "txt"),
    
    # 🟧 VMESS သီးသန့်
    ("Epodonios VMESS", "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/vmess.txt", "txt"),
    ("MatinGhanbari VMESS", "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/vmess.txt", "txt"),
    ("Free V2Ray VMESS", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/vmess.txt", "txt"),
    
    # 🟪 TROJAN သီးသန့်
    ("Epodonios TROJAN", "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/trojan.txt", "txt"),
    ("MatinGhanbari TROJAN", "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/trojan.txt", "txt"),
    
    # 🌍 နိုင်ငံအလိုက်
    ("🇸🇬 Singapore", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/singapore.txt", "txt"),
    ("🇲🇾 Malaysia", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/malaysia.txt", "txt"),
    ("🇹🇭 Thailand", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/thailand.txt", "txt"),
    ("🇭🇰 HongKong", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/hongkong.txt", "txt"),
    ("🇯🇵 Japan", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/japan.txt", "txt"),
    ("🇰🇷 Korea", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/korea.txt", "txt"),
    ("🇻🇳 Vietnam", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/vietnam.txt", "txt"),
    ("🇮🇳 India", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/india.txt", "txt"),
    ("🇺🇸 USA", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/usa.txt", "txt"),
    ("🇬🇧 UK", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/uk.txt", "txt"),
    ("🇩🇪 Germany", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/germany.txt", "txt"),
]

def fetch_content(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except:
        return None

def parse_configs(content, fmt):
    configs = []
    if not content: return configs
    try:
        if fmt == "b64":
            content = base64.b64decode(content).decode("utf-8", errors="ignore")
        lines = content.strip().splitlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"): continue
            proto = ""
            if line.startswith("vless://"): proto = "VLESS"
            elif line.startswith("ss://"): proto = "SS"
            elif line.startswith("vmess://"): proto = "VMESS"
            elif line.startswith("trojan://"): proto = "TROJAN"
            if proto:
                name = ""
                if "#" in line:
                    name = line.split("#")[-1]
                    from urllib.parse import unquote
                    name = unquote(name)
                configs.append({"name": name[:60], "key": line, "proto": proto})
    except:
        pass
    return configs

def get_hostname(key):
    try:
        if "://" not in key: return "", ""
        rest = key.split("://", 1)[1]
        if "@" in rest: rest = rest.split("@", 1)[1]
        if ":" in rest:
            host, port = rest.rsplit(":", 1)
            if "?" in port: port = port.split("?")[0]
            return host, port
    except: pass
    return "", ""

def ping_server(host, port=443, timeout=1):
    if not host: return 9999
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        start = time.time()
        s.connect((host, int(port) if port else 443))
        s.close()
        return round((time.time() - start) * 1000)
    except: return 9999

def flag_display(name):
    nl = name.lower()
    if "singapore" in nl or "sg" in nl: return "🇸🇬 စင်ကာပူ"
    if "malaysia" in nl or "my" in nl: return "🇲🇾 မလေးရှား"
    if "thailand" in nl or "th" in nl: return "🇹🇭 ထိုင်း"
    if "hongkong" in nl or "hk" in nl: return "🇭🇰 ဟောင်ကောင်"
    if "japan" in nl or "jp" in nl: return "🇯🇵 ဂျပန်"
    if "korea" in nl or "kr" in nl: return "🇰🇷 ကိုရီးယား"
    if "vietnam" in nl or "vn" in nl: return "🇻🇳 ဗီယက်နမ်"
    if "india" in nl or "in " in nl: return "🇮🇳 အိန္ဒိယ"
    if "united states" in nl or "usa" in nl or "us" in nl: return "🇺🇸 အမေရိက"
    if "uk" in nl or "london" in nl or "gb" in nl: return "🇬🇧 ယူကေ"
    if "germany" in nl or "de" in nl: return "🇩🇪 ဂျာမနီ"
    return "🌐 အခြား"

def tier_text(ms):
    if ms == 9999: return f"{C.R}❌ အော့ဖ်လိုင်း{C.RESET}"
    if ms < 60: return f"{C.G}👑 ELITE  {ms}ms{C.RESET}"
    if ms < 100: return f"{C.B}💎 PREMIUM {ms}ms{C.RESET}"
    if ms < 180: return f"{C.Y}⭐ FAST    {ms}ms{C.RESET}"
    if ms < 300: return f"{C.O}⚡ NORMAL  {ms}ms{C.RESET}"
    return f"{C.GR}⚠️ SLOW    {ms}ms{C.RESET}"

def load_all_keys_silent():
    all_keys = []
    seen = set()
    for name, url, fmt in SOURCES:
        content = fetch_content(url)
        if content:
            keys = parse_configs(content, fmt)
            for k in keys:
                if k["key"] not in seen:
                    seen.add(k["key"])
                    all_keys.append(k)
    return all_keys

def scan_and_sort(keys, limit=30):
    premium_header()
    print(f"  {C.Y}⚡ စကင်န်ဖတ်နေသည်... ကျေးဇူးပြု၍ စောင့်ပါ{C.RESET}\n")
    results = []
    total = min(len(keys), limit)
    for i in range(total):
        k = keys[i]
        host, port = get_hostname(k["key"])
        ms = ping_server(host, port)
        results.append({"name": k["name"], "key": k["key"], "proto": k["proto"], "ms": ms})
        pct = int((i + 1) / total * 100)
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        print(f"  {C.B}[{bar}] {pct:>3}%{C.RESET}", end="\r")
    print("\n")
    results.sort(key=lambda x: x["ms"])
    return [r for r in results if r["ms"] < 500]

def show_result_list(data, title, count=5):
    if not data:
        print(f"  {C.R}❌ မတွေ့ပါ။ ပြန်ကြိုးစားပါ။{C.RESET}\n")
        input(f"  ပြန်ရန် {C.Y}Enter{C.RESET}")
        return
    top = data[:count]
    pi = {"VLESS": "🟦", "SS": "🟩", "VMESS": "🟧", "TROJAN": "🟪"}
    
    print(f"  {C.P}{C.BOLD}╔════════════════════════════════════════════════════════╗{C.RESET}")
    print(f"  {C.P}{C.BOLD}║ ✅ {title}{' '*(56-len(title))}{C.P}║{C.RESET}")
    print(f"  {C.P}{C.BOLD}╚════════════════════════════════════════════════════════╝{C.RESET}\n")
    
    for idx, item in enumerate(top, 1):
        icon = pi.get(item["proto"], "⬜")
        print(f"  {C.Y}{C.BOLD}─── ဆာဗာ {idx}/{count} ──────────────────────────────────────{C.RESET}")
        print(f"  🌏 နိုင်ငံ   : {flag_display(item['name'])}")
        print(f"  🚀 အမြန်နှုန်း: {tier_text(item['ms'])}")
        print(f"  🏷️ အမည်    : {item['name'][:50]}")
        print(f"  📦 ပရိုတိုကော: {icon} {item['proto']}")
        print(f"  🔑 ကီး     :")
        print(f"  {C.G}{item['key']}{C.RESET}\n")
    
    all_text = "\n".join([x["key"] for x in top])
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", all_text])
        print(f"  {C.G}✅ ကီးအားလုံး ကလစ်ဘုတ်သို့ ကူးယူပြီးပါပြီ!{C.RESET}\n")
    except:
        pass
    
    print(f"  {C.P}📖 အသုံးပြုနည်း{C.RESET}")
    print(f"  ───────────────────────────────────────────────")
    print(f"  ၁။ V2RayNG / NekoBox ဖွင့်ပါ → + → Import from Clipboard")
    print(f"  ၂။ ဆာဗာကိုရွေးပြီး Connect လုပ်ပါ ✅")
    print(f"  📘 အကူအညီ: {FACEBOOK_LINK}")
    print(f"  ───────────────────────────────────────────────\n")
    input(f"  ပင်မမီနူးသို့ ပြန်ရန် {C.Y}Enter{C.RESET}")

def fav_menu():
    while True:
        premium_header()
        favs = []
        if os.path.exists(FAV_FILE):
            try: favs = json.load(open(FAV_FILE))
            except: pass
        print(f"  {C.P}{C.BOLD}⭐ အကြိုက်ဆုံးဆာဗာများ  ({len(favs)} ခု){C.RESET}\n")
        if not favs:
            print(f"  {C.O}⚠️ မရှိသေးပါ။ ကီးရပါက သိမ်းထားနိုင်ပါတယ်။{C.RESET}\n")
        else:
            pi = {"VLESS": "🟦", "SS": "🟩", "VMESS": "🟧", "TROJAN": "🟪"}
            for i, f in enumerate(favs, 1):
                print(f"  [{i}] {flag_display(f.get('name',''))} {pi.get(f.get('proto',''),'⬜')} {f.get('name','')[:45]}")
            print(f"\n  နံပါတ်ရိုက်ပါ = ကီးကူးယူမည်")
        print(f"  [0] ပင်မမီနူးသို့ ပြန်မည်\n")
        sel = input(f"  {C.P}{C.BOLD}ရွေးချယ်ပါ → {C.RESET}").strip()
        if sel == "0": break
        if sel.isdigit() and favs:
            idx = int(sel) - 1
            if 0 <= idx < len(favs):
                print(f"\n  {C.G}{favs[idx]['key']}{C.RESET}\n")
                try:
                    import subprocess
                    subprocess.run(["termux-clipboard-set", favs[idx]["key"]])
                    print(f"  ✅ ကူးယူပြီးပါပြီ!\n")
                except: pass
                input(f"  ပြန်ရန် Enter")

def main_loop(all_keys):
    vless = [k for k in all_keys if k["proto"] == "VLESS"]
    ss = [k for k in all_keys if k["proto"] == "SS"]
    vmess = [k for k in all_keys if k["proto"] == "VMESS"]
    trojan = [k for k in all_keys if k["proto"] == "TROJAN"]
    
    while True:
        premium_header()
        print(f"  {C.P}{C.BOLD}📊 စာရင်းအင်း{C.RESET}")
        print(f"  ╔════════════════════════════╗")
        print(f"  ║  🟦 VLESS   {len(vless):>4} ခု           ║")
        print(f"  ║  🟩 SS      {len(ss):>4} ခု           ║")
        print(f"  ║  🟧 VMESS   {len(vmess):>4} ခု           ║")
        print(f"  ║  🟪 TROJAN  {len(trojan):>4} ခု           ║")
        print(f"  ║  📦 စုစုပေါင်း {len(all_keys):>4} ခု           ║")
        print(f"  ╚════════════════════════════╝\n")
        
        print(f"  {C.P}{C.BOLD}🎯 ပင်မမီနူး{C.RESET}")
        print(f"  ╔════════════════════════════════════════╗")
        print(f"  ║  [1] 🟦 VLESS  အမြန်ဆုံး ၅ ခု  [2] 🟩 SS    အမြန်ဆုံး ၅ ခု ║")
        print(f"  ║  [3] 🏆 အားလုံး အမြန်ဆုံး ၅ ခု  [4] 🇸🇬 အာရှဆာဗာများသာ  ║")
        print(f"  ║  [5] ⭐ အကြိုက်ဆုံးဆာဗာများ     [6] 🔄 ကီးအသစ်ပြန်ဖတ်မည် ║")
        print(f"  ║  [0] ❌ ပရိုဂရမ်မှထွက်မည်                      ║")
        print(f"  ╚════════════════════════════════════════╝\n")
        
        sel = input(f"  {C.P}{C.BOLD}ရွေးချယ်ပါ → {C.RESET}").strip()
        
        if sel == "1":
            if not vless:
                print(f"  {C.O}⚠️ VLESS မရှိပါ။ [6] နှိပ်ပြီး ပြန်ဖတ်ပါ။{C.RESET}\n")
                time.sleep(1.5)
                continue
            data = scan_and_sort(vless)
            show_result_list(data, "🟦 VLESS အမြန်ဆုံး", 5)
        
        elif sel == "2":
            if not ss:
                print(f"  {C.O}⚠️ SS မရှိပါ။ [6] နှိပ်ပြီး ပြန်ဖတ်ပါ။{C.RESET}\n")
                time.sleep(1.5)
                continue
            data = scan_and_sort(ss)
            show_result_list(data, "🟩 SS အမြန်ဆုံး", 5)
        
        elif sel == "3":
            if not all_keys:
                print(f"  {C.O}⚠️ ကီးမရှိပါ။ [6] နှိပ်ပြီး ပြန်ဖတ်ပါ။{C.RESET}\n")
                time.sleep(1.5)
                continue
            data = scan_and_sort(all_keys)
            show_result_list(data, "🏆 အားလုံးထဲမှ အမြန်ဆုံး", 5)
        
        elif sel == "4":
            if not all_keys:
                print(f"  {C.O}⚠️ ကီးမရှိပါ။ [6] နှိပ်ပြီး ပြန်ဖတ်ပါ။{C.RESET}\n")
                time.sleep(1.5)
                continue
            asia_names = ["singapore", "malaysia", "thailand", "hongkong", "japan", "korea", "vietnam", "india"]
            asia = [k for k in all_keys if any(a in k["name"].lower() for a in asia_names)]
            if not asia:
                print(f"  {C.O}⚠️ အာရှဆာဗာ မတွေ့ပါ။ အားလုံးကိုပြပါမည်။{C.RESET}\n")
                asia = all_keys
            data = scan_and_sort(asia)
            show_result_list(data, "🇸🇬 အာရှဆာဗာများ အမြန်ဆုံး", 5)
        
        elif sel == "5":
            fav_menu()
        
        elif sel == "6":
            premium_header()
            print(f"  {C.Y}🔄 ကီးအသစ်ပြန်ဖတ်နေသည်...{C.RESET}\n")
            all_keys = load_all_keys_silent()
            vless = [k for k in all_keys if k["proto"] == "VLESS"]
            ss = [k for k in all_keys if k["proto"] == "SS"]
            vmess = [k for k in all_keys if k["proto"] == "VMESS"]
            trojan = [k for k in all_keys if k["proto"] == "TROJAN"]
            print(f"  {C.G}✅ အသစ်ဖတ်ပြီးပါပြီ! စုစုပေါင်း: {len(all_keys)} ခု{C.RESET}\n")
            time.sleep(1.2)
        
        elif sel == "0":
            premium_header()
            print(f"  {C.P}✨ ကျေးဇူးပါ! အကောင်းဆုံးဆာဗာရှာနိုင်ပါစေ ✨{C.RESET}")
            print(f"  📘 Facebook: {FACEBOOK_LINK}\n")
            sys.exit(0)
        
        else:
            print(f"  {C.R}❌ မှားနေပါတယ် 0-6 ကြားသာရွေးပါ{C.RESET}\n")
            time.sleep(1)

if __name__ == "__main__":
    try:
        premium_header()
        print(f"  {C.Y}⚡ ကီးများကို နောက်ခံမှ ရယူနေသည်...{C.RESET}\n")
        all_keys = load_all_keys_silent()
        time.sleep(0.5)
        main_loop(all_keys)
    except KeyboardInterrupt:
        premium_header()
        print(f"  {C.P}👑 ပရိုဂရမ်မှ ထွက်ပါပြီ{C.RESET}\n")
    except Exception as e:
        print(f"\n  {C.R}❌ အမှား: {e}{C.RESET}\n")
        input(f"  ဆက်ရန် {C.Y}Enter{C.RESET}")
    
