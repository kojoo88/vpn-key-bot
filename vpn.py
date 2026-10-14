#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, base64, os, socket, time, json, sys
from datetime import datetime

VERSION = "🚀 ALL-SOURCES EDITION | ULTRA PREMIUM v8.6"
FAV_FILE = os.path.expanduser("~/.vpn_premium.json")
FACEBOOK_LINK = "https://www.facebook.com/share/18jrazYpmS/"

class C:
    P = "\033[38;5;201m"   # ပန်းရောင် Premium
    G = "\033[38;5;46m"    # အစိမ်းရောင်
    B = "\033[38;5;39m"    # အပြာရောင်
    Y = "\033[38;5;226m"   # အဝါရောင်
    O = "\033[38;5;208m"   # လိမ္မော်ရောင်
    R = "\033[38;5;196m"   # အနီရောင်
    W = "\033[38;5;255m"   # အဖြူရောင်
    GR = "\033[38;5;245m"  # မီးခိုးရောင်
    RESET = "\033[0m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDER = "\033[4m"

def clear(): os.system("clear")

def separator(char="═", length=62):
    return f"{C.P}{C.BOLD}{char * length}{C.RESET}"

def premium_header():
    clear()
    print(f"""
{C.P}{C.BOLD}
╔══════════════════════════════════════════════════════════════╗
║   {C.W}🚀  U L T R A   P R E M I U M   E D I T I O N{C.P}              ║
║   {C.BOLD}{VERSION}{C.P}          ║
╠══════════════════════════════════════════════════════════════╣
║   {C.ITALIC}⚡ Fast VPN Key Finder • VLESS / SS / VMESS / TROJAN{C.P}          ║
╚══════════════════════════════════════════════════════════════╝{C.RESET}""")
    now = datetime.now()
    print(f"  {C.G}📅 ရက်စွဲ:{C.RESET} {now.strftime('%Y-%m-%d')}   {C.G}⏰ အချိန်:{C.RESET} {now.strftime('%H:%M:%S')}")
    print(f"  {C.B}📘 Facebook အကူအညီ:{C.RESET} {C.UNDER}{FACEBOOK_LINK}{C.RESET}")
    print(f"  {separator('-', 62)}\n")

SOURCES = [
    ("Shadowmere API", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("V2Ray Seeker All", "https://raw.githubusercontent.com/v2ray-seeker/v2rayseeker/main/sub.txt", "txt"),
    ("Free V2Ray All", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/all.txt", "txt"),
    ("SaeedDev V2Ray", "https://raw.githubusercontent.com/SaeedDev94/V2ray/main/all.txt", "txt"),
    ("Hossaini V2Ray", "https://raw.githubusercontent.com/hossaini/v2ray/main/sub.txt", "txt"),
    ("Awesome VPN Daily", "https://raw.githubusercontent.com/awesome-vpn/awesome-vpn/master/all", "txt"),
    ("Free V2Ray 🇸🇬 SG", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/singapore.txt", "txt"),
    ("Free V2Ray 🇲🇾 MY", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/malaysia.txt", "txt"),
    ("Free V2Ray 🇹🇭 TH", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/thailand.txt", "txt"),
    ("Epodonios VLESS", "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/vless.txt", "txt"),
    ("Epodonios SS", "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/ss.txt", "txt"),
    ("MatinGhanbari VLESS", "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/vless.txt", "txt"),
    ("MatinGhanbari SS", "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/ss.txt", "txt"),
    ("Argh73 Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
    ("V2Ray Pool All", "https://raw.githubusercontent.com/v2ray-pool/v2ray-pool/main/sub.txt", "txt"),
    ("IRCF Space", "https://raw.githubusercontent.com/ircfspace/ircf.github.io/main/configs.txt", "txt"),
    ("V2RayNG Free", "https://raw.githubusercontent.com/v2ray-ng/free/main/sub.txt", "txt"),
]

def fetch(src):
    try:
        r = urllib.request.Request(src[1], headers={"User-Agent":"Mozilla/5.0"})
        return urllib.request.urlopen(r, timeout=15).read().decode("utf-8", errors="ignore")
    except: return None

def parse(content, t):
    keys = []
    if not content: return keys
    if t == "b64":
        try: content = base64.b64decode(content).decode("utf-8", errors="ignore")
        except: pass
    for line in content.splitlines():
        line = line.strip()
        if not line: continue
        proto = None
        if line.startswith("vless://"): proto = "VLESS"
        elif line.startswith("ss://"): proto = "SS"
        elif line.startswith("vmess://"): proto = "VMESS"
        elif line.startswith("trojan://"): proto = "TROJAN"
        if not proto: continue
        name = line.split("#")[-1] if "#" in line else f"{proto} Server"
        try:
            from urllib.parse import unquote
            name = unquote(name)
        except: pass
        keys.append({"name": name, "key": line, "proto": proto})
    return keys

def get_host(k):
    try:
        from urllib.parse import urlparse
        u = urlparse(k)
        return u.hostname or "", u.port or 443
    except: return "", 443

def ping(host, port=443):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.8)
        t0 = time.time()
        s.connect((host, int(port)))
        return round((time.time() - t0) * 1000)
    except: return 9999

def flag(name):
    n = name.lower()
    if "singapore" in n or "sg " in n: return "🇸🇬 စင်ကာပူ"
    if "malaysia" in n or "my " in n: return "🇲🇾 မလေးရှား"
    if "thai" in n or "th " in n: return "🇹🇭 ထိုင်း"
    if "hongkong" in n or "hk " in n: return "🇭🇰 ဟောင်ကောင်"
    if "japan" in n or "jp " in n: return "🇯🇵 ဂျပန်"
    if "korea" in n or "kr " in n: return "🇰🇷 ကိုရီးယား"
    if "vietnam" in n or "vn " in n: return "🇻🇳 ဗီယက်နမ်"
    if "uk" in n or "gb" in n or "london" in n: return "🇬🇧 ယူကေ"
    if "finland" in n or "fi " in n: return "🇫🇮 ဖင်လန်"
    if "russia" in n or "ru " in n: return "🇷🇺 ရုရှား"
    if "us " in n or "usa" in n: return "🇺🇸 အမေရိက"
    if "de " in n or "frankfurt" in n: return "🇩🇪 ဂျာမနီ"
    if "canada" in n or "ca " in n: return "🇨🇦 ကနေဒါ"
    if "netherlands" in n or "nl " in n or "amsterdam" in n: return "🇳🇱 နယ်သာလန်"
    if "france" in n or "fr " in n or "paris" in n: return "🇫🇷 ပြင်သစ်"
    if "india" in n or "in " in n: return "🇮🇳 အိန္ဒိယ"
    return "🌐 အခြား"

def tier_label(ms):
    if ms == 9999: return f"{C.R}❌ အော့ဖ်လိုင်း{C.RESET}"
    if ms < 60: return f"{C.G}👑 ELITE {ms}ms{C.RESET}"
    if ms < 100: return f"{C.B}💎 PREMIUM {ms}ms{C.RESET}"
    if ms < 180: return f"{C.Y}⭐ FAST {ms}ms{C.RESET}"
    if ms < 300: return f"{C.O}⚡ NORMAL {ms}ms{C.RESET}"
    return f"{C.GR}⚠️ SLOW {ms}ms{C.RESET}"

def load_keys_silent():
    all_keys = []
    seen = set()
    for name, url, t in SOURCES:
        c = fetch((name, url, t))
        if c:
            ks = parse(c, t)
            for k in ks:
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
        h, p = get_host(k["key"])
        ms = ping(h, p) if h else 9999
        results.append({"name": k["name"], "key": k["key"], "proto": k["proto"], "ms": ms})
        percent = int((i + 1) / total * 100)
        bar = "█" * int(percent / 5) + "░" * (20 - int(percent / 5))
        print(f"  {C.B}[{bar}] {percent:>3}%{C.RESET}", end="\r", flush=True)
    print("\n")
    results.sort(key=lambda x: x["ms"])
    return [r for r in results if int(r["ms"]) < 500]

def display_results(data, title, count=5):
    if not data:
        print(f"  {C.R}❌ မတွေ့ပါ။ ပြန်ကြိုးစားပါ။{C.RESET}\n")
        input(f"  ပင်မမီနူးသို့ ပြန်ရန် {C.Y}Enter{C.RESET} နှိပ်ပါ...")
        return
    
    top5 = data[:count]
    proto_icon = {"VLESS": "🟦", "SS": "🟩", "VMESS": "🟧", "TROJAN": "🟪"}
    
    print(f"  {C.P}{C.BOLD}╔════════════════════════════════════════════════════════════╗{C.RESET}")
    print(f"  {C.P}{C.BOLD}║ ✅ {title}{' '*(56-len(title))}{C.P}║{C.RESET}")
    print(f"  {C.P}{C.BOLD}╚════════════════════════════════════════════════════════════╝{C.RESET}\n")
    
    for idx, item in enumerate(top5, 1):
        icon = proto_icon.get(item["proto"], "⬜")
        print(f"  {C.Y}{C.BOLD}┌── ဆာဗာ {idx}/{count} ────────────────────────────────────────┐{C.RESET}")
        print(f"  {C.Y}{C.BOLD}│{C.RESET}  {C.W}🌏 နိုင်ငံ:{C.RESET} {flag(item['name'])}")
        print(f"  {C.Y}{C.BOLD}│{C.RESET}  {C.W}🚀 အမြန်နှုန်း:{C.RESET} {tier_label(item['ms'])}")
        print(f"  {C.Y}{C.BOLD}│{C.RESET}  {C.W}🏷️ အမည်:{C.RESET} {item['name'][:55]}")
        print(f"  {C.Y}{C.BOLD}│{C.RESET}  {C.W}📦 ပရိုတိုကော:{C.RESET} {icon} {item['proto']}")
        print(f"  {C.Y}{C.BOLD}│{C.RESET}  {C.W}🔑 ကီး:{C.RESET}")
        print(f"  {C.Y}{C.BOLD}│{C.RESET}  {C.G}{item['key']}{C.RESET}")
        print(f"  {C.Y}{C.BOLD}└─────────────────────────────────────────────────────────────┘{C.RESET}\n")
    
    all_keys_text = "\n".join([k["key"] for k in top5])
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", all_keys_text])
        print(f"  {C.G}✅ ကီးအားလုံး ကလစ်ဘုတ်သို့ ကူးယူပြီးပါပြီ!{C.RESET}\n")
    except:
        print(f"  {C.O}⚠️ အထက်က ကီးများကို ကိုယ်တိုင်ကူးယူပါ{C.RESET}\n")
    
    print(f"  {separator('-', 62)}")
    print(f"  {C.P}📖 VLESS Key သုံးနည်း လမ်းညွှန်{C.RESET}")
    print(f"  {C.G}၁။{C.RESET} V2RayNG / NekoBox ကိုဖွင့်ပါ")
    print(f"  {C.G}၂။{C.RESET} ညာဘက်အပေါ် {C.Y}+{C.RESET} ကိုနှိပ်ပါ")
    print(f"  {C.G}၃။{C.RESET} \"{C.B}Import from Clipboard{C.RESET}\" ကိုရွေးပါ")
    print(f"  {C.G}၄။{C.RESET} ဆာဗာကိုနှိပ်ပြီး {C.G}Connect ✅{C.RESET} လုပ်ပါ")
    print(f"  {C.P}📘 အသေးစိတ်: {FACEBOOK_LINK}{C.RESET}")
    print(f"  {separator('-', 62)}\n")
    
    input(f"  ပင်မမီနူးသို့ ပြန်ရန် {C.Y}Enter{C.RESET} နှိပ်ပါ...")

def favorites_menu():
    while True:
        premium_header()
        if not os.path.exists(FAV_FILE):
            favs = []
        else:
            try: favs = json.load(open(FAV_FILE))
            except: favs = []
        
        print(f"  {C.P}{C.BOLD}⭐ အကြိုက်ဆုံးဆာဗာများ  ({len(favs)} ခု){C.RESET}\n")
        
        if not favs:
            print(f"  {C.O}⚠️ အကြိုက်ဆုံး မရှိသေးပါ။ ကီးရပါက သိမ်းထားနိုင်ပါတယ်။{C.RESET}\n")
        else:
            proto_icon = {"VLESS": "🟦", "SS": "🟩", "VMESS": "🟧", "TROJAN": "🟪"}
            for i, f in enumerate(favs, 1):
                icon = proto_icon.get(f["proto"], "⬜")
                print(f"  {C.BOLD}[{i}]{C.RESET} {flag(f['name'])} {icon} {f['name'][:45]}")
            print(f"\n  {C.Y}နံပါတ်ထည့်ပါ = ကီးကူးယူမည်{C.RESET}")
        
        print(f"  {C.BOLD}[0]{C.RESET} ပင်မမီနူးသို့ ပြန်မည်\n")
        sel = input(f"  {C.P}{C.BOLD}ရွေးချယ်ပါ → {C.RESET}").strip()
        
        if sel == "0": break
        if sel.isdigit() and favs:
            idx = int(sel) - 1
            if 0 <= idx < len(favs):
                print(f"\n  {C.G}{favs[idx]['key']}{C.RESET}\n")
                try:
                    import subprocess
                    subprocess.run(["termux-clipboard-set", favs[idx]["key"]])
                    print(f"  {C.G}✅ ကူးယူပြီးပါပြီ!{C.RESET}\n")
                except: pass
                input(f"  ပြန်ရန် {C.Y}Enter{C.RESET}...")

def main_menu(all_keys):
    vless = [k for k in all_keys if k["proto"] == "VLESS"]
    ss = [k for k in all_keys if k["proto"] == "SS"]
    vmess = [k for k in all_keys if k["proto"] == "VMESS"]
    trojan = [k for k in all_keys if k["proto"] == "TROJAN"]
    
    while True:
        premium_header()
        
        print(f"  {C.P}{C.BOLD}📊 စာရင်းအင်း{C.RESET}")
        print(f"  ╔════════════════════════════════╗")
        print(f"  ║  🟦 VLESS   {C.BOLD}{len(vless):>4}{C.RESET} ခု                ║")
        print(f"  ║  🟩 SS      {C.BOLD}{len(ss):>4}{C.RESET} ခု                ║")
        print(f"  ║  🟧 VMESS   {C.BOLD}{len(vmess):>4}{C.RESET} ခု                ║")
        print(f"  ║  🟪 TROJAN  {C.BOLD}{len(trojan):>4}{C.RESET} ခု                ║")
        print(f"  ║  📦 စုစုပေါင်း {C.BOLD}{len(all_keys):>4}{C.RESET} ခု                ║")
        print(f"  ╚════════════════════════════════╝\n")
        
        print(f"  {C.P}{C.BOLD}🎯 ပင်မမီနူး{C.RESET}")
        print(f"  ╔════════════════════════════════════════════════╗")
        print(f"  ║  {C.BOLD}[1]{C.RESET} 🟦 VLESS  အမြန်ဆုံး ၅ ခု    {C.BOLD}[2]{C.RESET} 🟩 SS      အမြန်ဆုံး ၅ ခု   ║")
        print(f"  ║  {C.BOLD}[3]{C.RESET} 🏆 အားလုံး  အမြန်ဆုံး ၅ ခု    {C.BOLD}[4]{C.RESET} 🇸🇬 အာရှဆာဗာများသာ       ║")
        print(f"  ║  {C.BOLD}[5]{C.RESET} ⭐ အကြိုက်ဆုံးဆာဗာများ      {C.BOLD}[6]{C.RESET} 🔄 ကီးအသစ်ပြန်ဖတ်မည်     ║")
        print(f"  ║  {C.BOLD}[0]{C.RESET} ❌ ပရိုဂရမ်မှထွက်မည်                          ║")
        print(f"  ╚════════════════════════════════════════════════╝\n")
        
        sel = input(f"  {C.P}{C.BOLD}ရွေးချယ်ပါ → {C.RESET}").strip()
        
        if sel == "1":
            if not vless:
                print(f"  {C.O}⚠️ VLESS ကီးမရှိပါ။ [6] ကိုနှိပ်ပြီး ပြန်ဖတ်ပါ။{C.RESET}\n")
                time.sleep(1.5)
                continue
            data = scan_and_sort(vless)
            display_results(data, "🟦 VLESS အမြန်ဆုံး ဆာဗာများ", 5)
        
        elif sel == "2":
            if not ss:
                print(f"  {C.O}⚠️ SS ကီးမရှိပါ။ [6] ကိုနှိပ်ပြီး ပြန်ဖတ်ပါ။{C.RESET}\n")
                time.sleep(1.5)
                continue
            data = scan_and_sort(ss)
            display_results(data, "🟩 SS အမြန်ဆုံး ဆာဗာများ", 5)
        
        elif sel == "3":
            if not all_keys:
                print(f"  {C.O}⚠️ ကီးမရှိပါ။ [6] ကိုနှိပ်ပြီး ပြန်ဖတ်ပါ။{C.RESET}\n")
                time.sleep(1.5)
                continue
            data = scan_and_sort(all_keys)
            display_results(data, "🏆 အားလုံးထဲမှ အမြန်ဆုံး ဆာဗာများ", 5)
        
        elif sel == "4":
            if not all_keys:
                print(f"  {C.O}⚠️ ကီးမရှိပါ။ [6] ကိုနှိပ်ပြီး ပြန်ဖတ်ပါ။{C.RESET}\n")
                time.sleep(1.5)
                continue
            asia_flags = ["🇸🇬", "🇲🇾", "🇹🇭", "🇭🇰", "🇯🇵", "🇰🇷", "🇻🇳", "🇮🇳"]
            asia = [k for k in all_keys if any(a in flag(k["name"]) for a in asia_flags)]
            if not asia:
                print(f"  {C.O}⚠️ အာရှဆာဗာ မတွေ့ပါ။ အားလုံးကိုပြပါမည်။{C.RESET}\n")
                asia = all_keys
            data = scan_and_sort(asia)
            display_results(data, "🇸🇬 အာရှဆာဗာများ အမြန်ဆုံး", 5)
        
        elif sel == "5":
            favorites_menu()
        
        elif sel == "6":
            premium_header()
            print(f"  {C.Y}🔄 ကီးအသစ်ပြန်ဖတ်နေသည်...{C.RESET}\n")
            all_keys = load_keys_silent()
            vless = [k for k in all_keys if k["proto"] == "VLESS"]
            ss = [k for k in all_keys if k["proto"] == "SS"]
            vmess = [k for k in all_keys if k["proto"] == "VMESS"]
            trojan = [k for k in all_keys if k["proto"] == "TROJAN"]
            print(f"  {C.G}✅ အသစ်ဖတ်ပြီးပါပြီ! စုစုပေါင်း: {len(all_keys)} ခု{C.RESET}\n")
            time.sleep(1.2)
        
        elif sel == "0":
            premium_header()
            print(f"  {C.P}{C.BOLD}✨ ကျေးဇူးပါ! အကောင်းဆုံးဆာဗာရှာနိုင်ပါစေ ✨{C.RESET}")
            print(f"  {C.B}📘 Facebook: {FACEBOOK_LINK}{C.RESET}\n")
            sys.exit(0)
        
        else:
            print(f"  {C.R}❌ မှားနေပါတယ် 0-6 ကြားသာထည့်ပါ{C.RESET}\n")
            time.sleep(1)

if __name__ == "__main__":
    try:
        premium_header()
        print(f"  {C.Y}⚡ ကီးများကို နောက်ခံမှ ရယူနေသည်...{C.RESET}\n")
        all_keys = load_keys_silent()
        time.sleep(0.5)
        main_menu(all_keys)
    except KeyboardInterrupt:
        premium_header()
        print(f"  {C.P}👑 ပရိုဂရမ်မှ ထွက်ပါပြီ{C.RESET}\n")
    except Exception as e:
        print(f"\n  {C.R}❌ အမှား: {e}{C.RESET}\n")
        input(f"  ဆက်ရန် {C.Y}Enter{C.RESET}...")
    
