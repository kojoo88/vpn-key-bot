#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, base64, os, socket, time, json, sys
from datetime import datetime

VERSION = "🌏 ALL-SOURCES EDITION v8.5"
FAV_FILE = os.path.expanduser("~/.vpn_eternal.json")
FACEBOOK_LINK = "https://www.facebook.com/share/18jrazYpmS/"

class C:
    G = "\033[38;5;220m"
    D = "\033[38;5;159m"
    E = "\033[38;5;49m"
    R = "\033[38;5;196m"
    S = "\033[38;5;45m"
    W = "\033[38;5;255m"
    A = "\033[38;5;172m"
    N = "\033[38;5;234m"
    M = "\033[38;5;201m"
    RESET = "\033[0m"
    B = "\033[1m"

def clear(): os.system("clear")

def title_banner():
    clear()
    print(f"""{C.M}{C.B}
╔═══════════════════════════════════════════════════════════════════╗
║     🚀  {C.B}ALL-SOURCES EDITION v8.5{C.RESET}{C.M}                              ║
║   ⚡ VLESS / SS / VMESS / TROJAN — Fast VPN Key Finder             ║
╚═══════════════════════════════════════════════════════════════════╝{C.RESET}""")
    print(f"  🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  📘 {C.S}Facebook:{C.RESET} {FACEBOOK_LINK}\n")

SOURCES = [
    ("Shadowmere API", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("V2Ray Seeker All", "https://raw.githubusercontent.com/v2ray-seeker/v2rayseeker/main/sub.txt", "txt"),
    ("Free V2Ray All", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/all.txt", "txt"),
    ("SaeedDev V2Ray", "https://raw.githubusercontent.com/SaeedDev94/V2ray/main/all.txt", "txt"),
    ("Hossaini V2Ray", "https://raw.githubusercontent.com/hossaini/v2ray/main/sub.txt", "txt"),
    ("Awesome VPN Daily", "https://raw.githubusercontent.com/awesome-vpn/awesome-vpn/master/all", "txt"),
    ("Free V2Ray SG 🇸🇬", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/singapore.txt", "txt"),
    ("Free V2Ray MY 🇲🇾", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/malaysia.txt", "txt"),
    ("Free V2Ray TH 🇹🇭", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/thailand.txt", "txt"),
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
    if t=="b64":
        try: content = base64.b64decode(content).decode("utf-8", errors="ignore")
        except: pass
    for line in content.splitlines():
        line = line.strip()
        if not line: continue
        proto = None
        if line.startswith("vless://"): proto="VLESS"
        elif line.startswith("ss://"): proto="SS"
        elif line.startswith("vmess://"): proto="VMESS"
        elif line.startswith("trojan://"): proto="TROJAN"
        if not proto: continue
        name = line.split("#")[-1] if "#" in line else f"{proto} Server"
        try:
            from urllib.parse import unquote
            name = unquote(name)
        except: pass
        keys.append({"name":name,"key":line,"proto":proto})
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
        return round((time.time()-t0)*1000)
    except: return 9999

def flag(name):
    n = name.lower()
    if "singapore" in n or "sg " in n: return "🇸🇬 SG"
    if "malaysia" in n or "my " in n: return "🇲🇾 MY"
    if "thai" in n or "th " in n: return "🇹🇭 TH"
    if "hongkong" in n or "hk " in n: return "🇭🇰 HK"
    if "japan" in n or "jp " in n: return "🇯🇵 JP"
    if "korea" in n or "kr " in n: return "🇰🇷 KR"
    if "vietnam" in n or "vn " in n: return "🇻🇳 VN"
    if "uk" in n or "gb" in n or "london" in n: return "🇬🇧 GB"
    if "finland" in n or "fi " in n: return "🇫🇮 FI"
    if "russia" in n or "ru " in n: return "🇷🇺 RU"
    if "us " in n or "usa" in n: return "🇺🇸 US"
    if "de " in n or "frankfurt" in n: return "🇩🇪 DE"
    if "canada" in n or "ca " in n: return "🇨🇦 CA"
    if "denmark" in n or "dk " in n: return "🇩🇰 DK"
    if "netherlands" in n or "nl " in n or "amsterdam" in n: return "🇳🇱 NL"
    if "france" in n or "fr " in n or "paris" in n: return "🇫🇷 FR"
    if "india" in n or "in " in n: return "🇮🇳 IN"
    return "🌐 --"

def rank(ms):
    if ms == 9999: return f"{C.R}✖ OFFLINE{C.RESET}"
    ms = int(ms)
    if ms < 60: return f"{C.G}👑 S-TIER {C.E}{ms}ms{C.RESET}"
    if ms < 100: return f"{C.D}💎 A-TIER {C.S}{ms}ms{C.RESET}"
    if ms < 180: return f"{C.W}⭐ B-TIER {C.A}{ms}ms{C.RESET}"
    if ms < 300: return f"{C.A}⚡ C-TIER {ms}ms{C.RESET}"
    return f"{C.N}⚠ D-TIER {C.R}{ms}ms{C.RESET}"

def load_keys_silent():
    all_keys = []
    seen = set()
    success = 0
    for name, url, t in SOURCES:
        c = fetch((name, url, t))
        if c:
            ks = parse(c, t)
            for k in ks:
                if k["key"] not in seen:
                    seen.add(k["key"])
                    all_keys.append(k)
            success += 1
    return all_keys, success

def scan_best(keys, limit=30):
    title_banner()
    print(f"  {C.S}⚡ စကင်န်ဖတ်နေသည်... ကျေးဇူးပြု၍ စောင့်ပါ{C.RESET}\n")
    res = []
    total = min(len(keys), limit)
    for i in range(total):
        k = keys[i]
        h,p = get_host(k["key"])
        ms = ping(h,p) if h else 9999
        res.append({"name":k["name"],"key":k["key"],"proto":k["proto"],"ms":ms})
        pct = int((i+1)/total*100)
        bar = "█"*int(pct/5)+"░"*(20-int(pct/5))
        print(f"\r  [{bar}] {pct:>3}%", end="", flush=True)
    print("\n")
    res.sort(key=lambda x:x["ms"])
    return [r for r in res if int(r["ms"]) < 500]

def show_and_copy(data, title_text, count=5):
    if not data:
        print(f"  {C.R}မတွေ့ပါ။ ပြန်ကြိုးစားပါ။{C.RESET}\n")
        input(f"  ပြန်ရန် Enter...")
        return
    
    top = data[:count]
    print(f"  {C.M}{C.B}╔════════════════════════════════════════════════════════╗{C.RESET}")
    print(f"  {C.M}{C.B}║  ✅ {title_text} — အကောင်းဆုံး {count} ခု{C.RESET}{' '*(32-len(title_text))}{C.M}║{C.RESET}")
    print(f"  {C.M}{C.B}╚════════════════════════════════════════════════════════╝{C.RESET}\n")
    
    for idx, r in enumerate(top, 1):
        proto_icon = {"VLESS":"🟦","SS":"🟩","VMESS":"🟧","TROJAN":"🟪"}.get(r["proto"],"⬜")
        print(f"  {C.B}▸ ဆာဗာ {idx}/{count}{C.RESET}")
        print(f"    {C.W}နိုင်ငံ:{C.RESET} {flag(r['name'])}   {C.W}အမြန်နှုန်း:{C.RESET} {rank(r['ms'])}")
        print(f"    {C.W}အမည်:{C.RESET} {r['name'][:50]}")
        print(f"    {C.W}ပရိုတိုကော:{C.RESET} {proto_icon} {r['proto']}")
        print(f"    {C.W}ကီး:{C.RESET}")
        print(f"    {C.S}{r['key']}{C.RESET}\n")
    
    all_keys_text = "\n".join([r["key"] for r in top])
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", all_keys_text])
        print(f"  {C.E}✅ ကီးအားလုံး ကလစ်ဘုတ်သို့ ကူးယူပြီးပါပြီ!{C.RESET}\n")
    except:
        print(f"  {C.A}⚠️ အထက်က ကီးများကို ကိုယ်တိုင်ကူးယူပါ{C.RESET}\n")
    
    usage_guide_short()
    input(f"  ပင်မမီနူးသို့ ပြန်ရန် Enter...")

def usage_guide_short():
    print(f"  {C.M}📘 VLESS Key သုံးနည်း{C.RESET}")
    print(f"  ────────────────────────────────────────────────")
    print(f"  ၁။ V2RayNG / NekoBox ကိုဖွင့်ပါ")
    print(f"  ၂။ ညာဘက်အပေါ် + → Import from Clipboard")
    print(f"  ၃။ ဆာဗာကိုနှိပ်ပြီး Connect လုပ်ပါ ✅")
    print(f"  📘 အသေးစိတ်: {FACEBOOK_LINK}")
    print(f"  ────────────────────────────────────────────────\n")

def fav_menu():
    while True:
        title_banner()
        if not os.path.exists(FAV_FILE):
            favs = []
        else:
            try: favs = json.load(open(FAV_FILE))
            except: favs = []
        
        print(f"  {C.M}{C.B}⭐ အကြိုက်ဆုံးဆာဗာများ{C.RESET} ({len(favs)} ခု)\n")
        if not favs:
            print(f"  {C.A}အကြိုက်ဆုံး မရှိသေးပါ။ ကီးရပါက သိမ်းထားနိုင်ပါတယ်။{C.RESET}\n")
        else:
            for i, f in enumerate(favs, 1):
                print(f"  [{i}] {flag(f['name'])} | {f['name'][:40]}")
            print(f"  နံပါတ်ထည့်ပါ = ကီးကူးယူမည်")
        print(f"  [0] ပင်မမီနူးသို့ ပြန်မည်\n")
        sel = input(f"  {C.S}ရွေးချယ်ပါ → {C.RESET}").strip()
        if sel == "0": break
        if sel.isdigit() and favs:
            idx = int(sel)-1
            if 0 <= idx < len(favs):
                print(f"\n  {favs[idx]['key']}\n")
                try:
                    import subprocess
                    subprocess.run(["termux-clipboard-set", favs[idx]["key"]])
                    print(f"  {C.E}✅ ကူးယူပြီးပါပြီ!{C.RESET}\n")
                except: pass
                input(f"  ပြန်ရန် Enter...")

def main_menu(all_keys):
    vless = [k for k in all_keys if k["proto"]=="VLESS"]
    ss = [k for k in all_keys if k["proto"]=="SS"]
    vmess = [k for k in all_keys if k["proto"]=="VMESS"]
    trojan = [k for k in all_keys if k["proto"]=="TROJAN"]
    
    while True:
        title_banner()
        print(f"  {C.M}{C.B}📊 စာရင်းအင်း{C.RESET}")
        print(f"  ┌────────────┬──────────────────────────────┐")
        print(f"  │  🟦 VLESS  │  {len(vless):>4} ခု                     │")
        print(f"  │  🟩 SS     │  {len(ss):>4} ခု                     │")
        print(f"  │  🟧 VMESS  │  {len(vmess):>4} ခု                     │")
        print(f"  │  🟪 TROJAN │  {len(trojan):>4} ခု                     │")
        print(f"  │  📦 စုစုပေါင်း │  {len(all_keys):>4} ခု                     │")
        print(f"  └────────────┴──────────────────────────────┘\n")
        
        print(f"  {C.M}{C.B}🎯 ပင်မမီနူး{C.RESET}")
        print(f"  ┌──────────────────────────────────────────────────────┐")
        print(f"  │  [1] ⚡ VLESS  အမြန်ဆုံး ၅ ခု  │  [2] 🟩 SS  အမြန်ဆုံး ၅ ခု     │")
        print(f"  │  [3] 🏆 အားလုံး  အမြန်ဆုံး ၅ ခု  │  [4] 🇸🇬 အာရှဆာဗာများသာ       │")
        print(f"  │  [5] ⭐ အကြိုက်ဆုံးဆာဗာများ      │  [6] 🔄 ကီးအသစ်ပြန်ဖတ်မည်     │")
        print(f"  │  [0] ✖ ပရိုဂရမ်မှထွက်မည်      │                          │")
        print(f"  └──────────────────────────────────────────────────────┘\n")
        
        sel = input(f"  {C.S}{C.B}ရွေးချယ်ပါ → {C.RESET}").strip()
        
        if sel == "1":
            if not vless:
                print(f"  {C.A}VLESS ကီးမရှိပါ။ [6] ကိုနှိပ်ပြီး ပြန်ဖတ်ပါ။{C.RESET}\n")
                time.sleep(1.5)
                continue
            data = scan_best(vless)
            show_and_copy(data, "🟦 VLESS အမြန်ဆုံး", 5)
        
        elif sel == "2":
            if not ss:
                print(f"  {C.A}SS ကီးမရှိပါ။ [6] ကိုနှိပ်ပြီး ပြန်ဖတ်ပါ။{C.RESET}\n")
                time.sleep(1.5)
                continue
            data = scan_best(ss)
            show_and_copy(data, "🟩 SS အမြန်ဆုံး", 5)
        
        elif sel == "3":
            if not all_keys:
                print(f"  {C.A}ကီးမရှိပါ။ [6] ကိုနှိပ်ပြီး ပြန်ဖတ်ပါ။{C.RESET}\n")
                time.sleep(1.5)
                continue
            data = scan_best(all_keys)
            show_and_copy(data, "🏆 အားလုံးထဲမှ အမြန်ဆုံး", 5)
        
        elif sel == "4":
            if not all_keys:
                print(f"  {C.A}ကီးမရှိပါ။ [6] ကိုနှိပ်ပြီး ပြန်ဖတ်ပါ။{C.RESET}\n")
                time.sleep(1.5)
                continue
            asia_flags = ["🇸🇬", "🇲🇾", "🇹🇭", "🇭🇰", "🇯🇵", "🇰🇷", "🇻🇳", "🇮🇳"]
            asia = [k for k in all_keys if any(a in flag(k["name"]) for a in asia_flags)]
            if not asia:
                print(f"  {C.A}အာရှဆာဗာ မတွေ့ပါ။ အားလုံးကိုပြပါမည်။{C.RESET}\n")
                asia = all_keys
            data = scan_best(asia)
            show_and_copy(data, "🇸🇬 အာရှဆာဗာများ အမြန်ဆုံး", 5)
        
        elif sel == "5":
            fav_menu()
        
        elif sel == "6":
            title_banner()
            print(f"  {C.S}🔄 ကီးအသစ်ပြန်ဖတ်နေသည်...{C.RESET}\n")
            all_keys, _ = load_keys_silent()
            vless = [k for k in all_keys if k["proto"]=="VLESS"]
            ss = [k for k in all_keys if k["proto"]=="SS"]
            vmess = [k for k in all_keys if k["proto"]=="VMESS"]
            trojan = [k for k in all_keys if k["proto"]=="TROJAN"]
            print(f"  {C.E}✅ အသစ်ဖတ်ပြီးပါပြီ! စုစုပေါင်း: {len(all_keys)} ခု{C.RESET}\n")
            time.sleep(1.2)
        
        elif sel == "0":
            title_banner()
            print(f"  {C.M}{C.B}✨ ကျေးဇူးပါ! အကောင်းဆုံးဆာဗာရှာနိုင်ပါစေ ✨{C.RESET}")
            print(f"  📘 Facebook: {FACEBOOK_LINK}\n")
            sys.exit(0)
        
        else:
            print(f"  {C.R}မှားနေပါတယ် 0-6 ကြားသာထည့်ပါ{C.RESET}\n")
            time.sleep(1)

if __name__ == "__main__":
    try:
        title_banner()
        print(f"  {C.S}🔄 ကီးများကို နောက်ခံမှ ရယူနေသည်...{C.RESET}\n")
        all_keys, _ = load_keys_silent()
        time.sleep(0.5)
        main_menu(all_keys)
    except KeyboardInterrupt:
        title_banner()
        print(f"  {C.M}👑 ပရိုဂရမ်မှ ထွက်ပါပြီ{C.RESET}\n")
    except Exception as e:
        print(f"\n  {C.R}အမှား: {e}{C.RESET}\n")
        input(f"  ဆက်ရန် Enter...")
