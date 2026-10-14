#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, base64, os, socket, time, json, sys
from datetime import datetime

VERSION = "🌏 ALL-SOURCES EDITION v8.3"
FAV_FILE = os.path.expanduser("~/.vpn_eternal.json")

class C:
    G = "\033[38;5;220m"
    D = "\033[38;5;159m"
    E = "\033[38;5;49m"
    R = "\033[38;5;196m"
    S = "\033[38;5;45m"
    W = "\033[38;5;255m"
    A = "\033[38;5;172m"
    N = "\033[38;5;234m"
    RESET = "\033[0m"
    B = "\033[1m"

def clear(): os.system("clear")
def title():
    clear()
    print(f"""{C.G}
╔═════════════════════════════════════════╗
║     {C.B}🌏 ALL-SOURCES EDITION v8.3 🌏{C.RESET}{C.G}     ║
║   ပိုမိုမြန်ဆန်သောဆာဗာများ ရှာဖွေခြင်း       ║
╚═════════════════════════════════════════╝{C.RESET}""")
    print(f"  🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

def load_fav():
    if os.path.exists(FAV_FILE):
        try: return json.load(open(FAV_FILE))
        except: return []
    return []

def save_fav(item):
    favs = load_fav()
    if any(f["key"]==item["key"] for f in favs): return False
    favs.insert(0, {"name":item["name"],"key":item["key"],"saved_at":datetime.now().strftime("%Y-%m-%d %H:%M")})
    json.dump(favs, open(FAV_FILE,"w"), ensure_ascii=False, indent=2)
    return True

def copy_t(text):
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", text])
        return True
    except: return False

# ==================================================
# 🌏 အရင်းအမြစ်အားလုံး — စုစုပေါင်း 28 ခု
# ==================================================
SOURCES = [
    # ⭐ အဓိက အကောင်းဆုံး အရင်းအမြစ်များ
    ("Shadowmere API", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("V2Ray Seeker All", "https://raw.githubusercontent.com/v2ray-seeker/v2rayseeker/main/sub.txt", "txt"),
    ("Free V2Ray All", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/all.txt", "txt"),
    ("SaeedDev V2Ray", "https://raw.githubusercontent.com/SaeedDev94/V2ray/main/all.txt", "txt"),
    ("Hossaini V2Ray", "https://raw.githubusercontent.com/hossaini/v2ray/main/sub.txt", "txt"),
    ("Awesome VPN Daily", "https://raw.githubusercontent.com/awesome-vpn/awesome-vpn/master/all", "txt"),
    ("Free Nodes V2Ray", "https://raw.githubusercontent.com/free-nodes/v2rayfree/main/v202607312", "txt"),
    
    # 🇸🇬 အာရှ သီးသန့် (မြန်မာအတွက် အမြန်ဆုံး)
    ("Free V2Ray SG 🇸🇬", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/singapore.txt", "txt"),
    ("Free V2Ray MY 🇲🇾", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/malaysia.txt", "txt"),
    ("Free V2Ray TH 🇹🇭", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/thailand.txt", "txt"),
    ("V2Ray Pool SG 🇸🇬", "https://raw.githubusercontent.com/v2ray-pool/v2ray-pool/main/sg.txt", "txt"),
    
    # 🔹 ပရိုတိုကော သီးသန့် — VLESS
    ("Epodonios VLESS", "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/vless.txt", "txt"),
    ("MatinGhanbari VLESS", "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/vless.txt", "txt"),
    ("VLESS Hub", "https://raw.githubusercontent.com/ircfspace/vlesshub/main/vless.txt", "txt"),
    ("Config Collector VLESS", "https://raw.githubusercontent.com/tahmaseb73/configs-collector-v2ray/refs/heads/main/data/sub/protocols/vless.txt", "txt"),
    
    # 🔹 ပရိုတိုကော သီးသန့် — SS
    ("Epodonios SS", "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/ss.txt", "txt"),
    ("MatinGhanbari SS", "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/ss.txt", "txt"),
    ("V2Ray Seeker SS", "https://raw.githubusercontent.com/v2ray-seeker/v2rayseeker/main/ss.txt", "txt"),
    ("Free V2Ray SS", "https://raw.githubusercontent.com/Free-V2Ray/Free-V2Ray/main/ss.txt", "txt"),
    
    # 🔹 အခြား အရင်းအမြစ်ကောင်းများ
    ("Argh73 Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
    ("V2Ray Pool All", "https://raw.githubusercontent.com/v2ray-pool/v2ray-pool/main/sub.txt", "txt"),
    ("IRCF Space", "https://raw.githubusercontent.com/ircfspace/ircf.github.io/main/configs.txt", "txt"),
    ("V2RayNG Free", "https://raw.githubusercontent.com/v2ray-ng/free/main/sub.txt", "txt"),
    ("Config Collector All", "https://raw.githubusercontent.com/tahmaseb73/configs-collector-v2ray/refs/heads/main/data/sub/splitted/mixed_19.txt", "txt"),
    ("TGParse Mixed", "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/splitted/ss", "txt"),
    ("MorpheusAdam Configs", "https://raw.githubusercontent.com/morpheusadam/v2ray-config/main/subs/all.txt", "txt"),
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
    if "singapore" in n or "sg " in n or "sg-" in n: return "🇸🇬 SG"
    if "malaysia" in n or "my " in n or "my-" in n: return "🇲🇾 MY"
    if "thai" in n or "th " in n or "th-" in n: return "🇹🇭 TH"
    if "hongkong" in n or "hk " in n or "hk-" in n: return "🇭🇰 HK"
    if "japan" in n or "jp " in n or "jp-" in n: return "🇯🇵 JP"
    if "korea" in n or "kr " in n or "kr-" in n: return "🇰🇷 KR"
    if "vietnam" in n or "vn " in n: return "🇻🇳 VN"
    if "uk" in n or "gb" in n or "london" in n or "united kingdom" in n: return "🇬🇧 GB"
    if "finland" in n or "fi " in n: return "🇫🇮 FI"
    if "russia" in n or "ru " in n: return "🇷🇺 RU"
    if "united states" in n or "us " in n or "usa" in n: return "🇺🇸 US"
    if "germany" in n or "de " in n or "frankfurt" in n: return "🇩🇪 DE"
    if "canada" in n or "ca " in n: return "🇨🇦 CA"
    if "denmark" in n or "dk " in n: return "🇩🇰 DK"
    if "netherlands" in n or "nl " in n or "amsterdam" in n: return "🇳🇱 NL"
    if "france" in n or "fr " in n or "paris" in n: return "🇫🇷 FR"
    if "india" in n or "in " in n: return "🇮🇳 IN"
    if "brazil" in n or "br " in n: return "🇧🇷 BR"
    return "🌐 --"

def rank(ms):
    if ms == 9999: return f"{C.R}✖ OFFLINE{C.RESET}"
    ms = int(ms)
    if ms < 60: return f"{C.G}👑 S-TIER {C.E}●{ms}ms{C.RESET}"
    if ms < 100: return f"{C.D}💎 A-TIER {C.S}●{ms}ms{C.RESET}"
    if ms < 180: return f"{C.W}⭐ B-TIER {C.A}●{ms}ms{C.RESET}"
    if ms < 300: return f"{C.A}⚡ C-TIER {C.A}●{ms}ms{C.RESET}"
    return f"{C.N}⚠ D-TIER {C.R}●{ms}ms{C.RESET}"

def load_keys():
    all_keys = []
    seen = set()
    title()
    print(f"  {C.S}📡 အရင်းအမြစ် {len(SOURCES)} ခုမှ ကီးများရယူနေသည်...{C.RESET}\n")
    success = 0
    for idx, (name, url, t) in enumerate(SOURCES, 1):
        print(f"  [{idx:02d}/{len(SOURCES)}] ▸ {name[:25]:<25}...", end=" ", flush=True)
        c = fetch((name, url, t))
        if c:
            ks = parse(c, t)
            cnt=0
            for k in ks:
                if k["key"] not in seen:
                    seen.add(k["key"])
                    all_keys.append(k)
                    cnt+=1
            print(f"{C.E}✓ {cnt:>3d} ခု{C.RESET}")
            success += 1
        else:
            print(f"{C.R}✖ မရရှိ{C.RESET}")
        time.sleep(0.1)
    print(f"\n  {C.G}✨ အလုပ်လုပ်သောအရင်းအမြစ်: {success}/{len(SOURCES)}  │  စုစုပေါင်းကီး: {len(all_keys)} ခု{C.RESET}\n")
    time.sleep(1)
    return all_keys

def scan_best(keys, limit=25):
    title()
    print(f"  {C.S}⚡ အကောင်းဆုံးများကို စကင်န်ဖတ်နေသည်... ကျေးဇူးပြု၍ စောင့်ပါ{C.RESET}\n")
    res = []
    total = min(len(keys), limit)
    for i in range(total):
        k = keys[i]
        h,p = get_host(k["key"])
        ms = ping(h,p) if h else 9999
        res.append({"name":k["name"],"key":k["key"],"proto":k["proto"],"ms":ms})
        pct = int((i+1)/total*100)
        bar = "█"*int(pct/5)+"░"*(20-int(pct/5))
        print(f"\r  [{bar}] {pct:>3}%  ({i+1}/{total})", end="", flush=True)
    print("\n")
    res.sort(key=lambda x:x["ms"])
    return [r for r in res if int(r["ms"]) < 500]

def show_list(data, title_text):
    if not data:
        print(f"  {C.R}မတွေ့ပါ။ ပြန်ကြိုးစားပါ။{C.RESET}\n")
        return
    print(f"  {C.G}{title_text}  ({len(data)} ခု){C.RESET}")
    print(f"  ┌──┬─────────┬──────────────────┬──────────────────────────────────────────────────────┐")
    print(f"  │# │ နိုင်ငံ  │ အဆင့်            │ အမည်                                                │")
    print(f"  ├──┼─────────┼──────────────────┼──────────────────────────────────────────────────────┤")
    for i,r in enumerate(data,1):
        print(f"  │{i:<2}│ {flag(r['name']):<7} │ {rank(r['ms']):<16} │ {r['name'][:52]:<52} │")
    print(f"  └──┴─────────┴──────────────────┴──────────────────────────────────────────────────────┘\n")

def copy_top(data, n=3):
    if not data: return
    top = data[:n]
    keys_text = "\n".join([r["key"] for r in top])
    
    print(f"\n{C.G}{'═'*75}{C.RESET}")
    print(f"{C.G}💎 အကောင်းဆုံး {len(top)} ခု — ကီးအပြည့်အစုံ{C.RESET}")
    print(f"{C.G}{'═'*75}{C.RESET}\n")
    
    for idx, r in enumerate(top, 1):
        print(f"{C.S}┌── ကီး {idx}/{len(top)} ─────────────────────────────────────────────{C.RESET}")
        print(f"  {C.W}နိုင်ငံ:{C.RESET} {flag(r['name'])}   {C.W}အဆင့်:{C.RESET} {rank(r['ms'])}")
        print(f"  {C.W}အမည်:{C.RESET} {r['name']}")
        print(f"  {C.W}ပရိုတိုကော:{C.RESET} {r['proto']}")
        print(f"  {C.W}ကီး:{C.RESET}")
        print(f"  {r['key']}")
        print()
    
    ok = copy_t(keys_text)
    print(f"{C.G}{'═'*75}{C.RESET}")
    if ok:
        print(f"  {C.E}✅ ကလစ်ဘုတ်သို့ အကုန်ကူးယူပြီးပါပြီ!{C.RESET}")
        print(f"  {C.S}💡 V2RayNG / NekoBox → + → Import from Clipboard{C.RESET}")
    else:
        print(f"  {C.A}⚠️ အထက်က ကီးများကို ကိုယ်တိုင်အပြည့်အဝကူးယူပါ{C.RESET}")
    print()
    return top

def fav_menu():
    while True:
        title()
        favs = load_fav()
        if not favs:
            print(f"  {C.A}အကြိုက်ဆုံး မရှိသေးပါ။ ကီးတစ်ခုရွေးပြီး သိမ်းထားနိုင်ပါတယ်။{C.RESET}\n")
        else:
            print(f"  {C.G}⭐ အကြိုက်ဆုံး ({len(favs)} ခု){C.RESET}")
            print(f"  ┌──┬─────────┬───────────────────────────────────────────────────────┬──────────────┐")
            print(f"  │# │ နိုင်ငံ  │ အမည်                                                │ သိမ်းခဲ့စဉ်   │")
            print(f"  ├──┼─────────┼───────────────────────────────────────────────────────┼──────────────┤")
            for i,f in enumerate(favs,1):
                print(f"  │{i:<2}│ {flag(f['name']):<7} │ {f['name'][:55]:<55} │ {f['saved_at']:<12} │")
            print(f"  └──┴─────────┴───────────────────────────────────────────────────────┴──────────────┘")
            print(f"  နံပါတ်ထည့်ပါ = ကီးအပြည့်အစုံကူးယူမည်")
        print(f"  0 = ပင်မမီနူး")
        sel = input(f"\n  {C.S}ရွေးချယ်ပါ → {C.RESET}").strip()
        if sel=="0": break
        if sel.isdigit() and favs:
            idx = int(sel)-1
            if 0<=idx<len(favs):
                key_data = favs[idx]["key"]
                copy_t(key_data)
                print(f"\n  {C.G}ကီးအပြည့်အစုံ:{C.RESET}")
                print(f"  {key_data}")
                print(f"\n  {C.E}✅ ကူးယူပြီးပါပြီ!{C.RESET}\n")
                time.sleep(2)

def network_info():
    title()
    print(f"  {C.G}🌏 မြန်မာအတွက် အကောင်းဆုံးနိုင်ငံများ{C.RESET}\n")
    print(f"  ┌────────────┬────────────────────────────────────────────┐")
    print(f"  │ 🇸🇬 SG စင်ကာပူ │ အမြန်ဆုံး  •  80–180ms  •  ပထမရွေးချယ်မှု   │")
    print(f"  │ 🇲🇾 MY မလေးရှား │ အလွန်ကောင်း  •  100–200ms               │")
    print(f"  │ 🇹🇭 TH ထိုင်း   │ ကောင်း  •  120–220ms                   │")
    print(f"  │ 🇭🇰 HK ဟောင်ကောင် │ အတန်းအစား  •  150–250ms               │")
    print(f"  │ 🇯🇵 JP ဂျပန်   │ နှေးနိုင်  •  180–280ms                   │")
    print(f"  │ 🇺🇸 US အမေရိကန် │ အနှေးဆုံး  •  250–400ms+                 │")
    print(f"  └────────────┴────────────────────────────────────────────┘\n")
    print(f"  {C.S}အကောင်းဆုံးအချိန်- မနက်စောစော နှင့် ညနေ 5-7 နာရီအတွင်း{C.RESET}")
    print(f"  {C.A}အရင်းအမြစ် 28 ခုမှ ရှာဖွေနေသည် — မတွေ့ရင် [5] ကိုနှိပ်ပြီး ပြန်ဖတ်ပါ{C.RESET}\n")
    input(f"  ပြန်ရန် Enter...")

def main():
    all_keys = load_keys()
    vless = [k for k in all_keys if k["proto"]=="VLESS"]
    ss = [k for k in all_keys if k["proto"]=="SS"]
    vmess = [k for k in all_keys if k["proto"]=="VMESS"]
    trojan = [k for k in all_keys if k["proto"]=="TROJAN"]
    
    while True:
        title()
        print(f"  🟦 VLESS: {len(vless)}  │  🟩 SS: {len(ss)}  │  🟧 VMESS: {len(vmess)}  │  🟪 TROJAN: {len(trojan)}")
        print(f"\n  {C.G}ပင်မမီနူး{C.RESET}")
        print(f"  ─────────────────────────────────────")
        print(f"  [1] ⚡ အကောင်းဆုံး VLESS ရှာမည်")
        print(f"  [2] 🟩 အကောင်းဆုံး SS ရှာမည်")
        print(f"  [3] 🏆 အားလုံးထဲမှ အကောင်းဆုံး ၅ ခု")
        print(f"  [4] 🇸🇬 အာရှဆာဗာများသာ ရှာမည်")
        print(f"  [5] ⭐ အကြိုက်ဆုံးဆာဗာများ")
        print(f"  [6] 📱 ကွန်ရက်အကြံပြုချက်")
        print(f"  [7] 🔄 ကီးအသစ်ပြန်ဖတ်မည်")
        print(f"  [0] ✖ ပရိုဂရမ်မှထွက်မည်")
        sel = input(f"\n  {C.S}ရွေးချယ်ပါ → {C.RESET}").strip()
        
        if sel=="1":
            if not vless:
                print(f"  {C.A}VLESS ကီးမရှိပါ{C.RESET}\n")
                time.sleep(1)
                continue
            data = scan_best(vless)
            show_list(data, "⚡ VLESS ဆာဗာများ")
            if data: copy_top(data,3)
            input(f"  ပြန်ရန် Enter...")
        
        elif sel=="2":
            if not ss:
                print(f"  {C.A}SS ကီးမရှိပါ{C.RESET}\n")
                time.sleep(1)
                continue
            data = scan_best(ss)
            show_list(data, "🟩 SS ဆာဗာများ")
            if data: copy_top(data,3)
            input(f"  ပြန်ရန် Enter...")
        
        elif sel=="3":
            if not all_keys:
                print(f"  {C.A}ကီးမရှိပါ။ အရင်ပြန်ဖတ်ပါ{C.RESET}\n")
                time.sleep(1)
                continue
            data = scan_best(all_keys, limit=30)
            show_list(data, "🏆 အကောင်းဆုံးအားလုံး")
            if data: copy_top(data,5)
            input(f"  ပြန်ရန် Enter...")
        
        elif sel=="4":
            if not all_keys:
                print(f"  {C.A}ကီးမရှိပါ။ အရင်ပြန်ဖတ်ပါ{C.RESET}\n")
                time.sleep(1)
                continue
            asia = []
            asia_flags = ["🇸🇬", "🇲🇾", "🇹🇭", "🇭🇰", "🇯🇵", "🇰🇷", "🇻🇳", "🇮🇳"]
            for k in all_keys:
                f = flag(k["name"])
                if any(a in f for a in asia_flags):
                    asia.append(k)
            if not asia:
                print(f"  {C.A}အာရှဆာဗာ မတွေ့ပါ။ အားလုံးကိုပြပါမည်။{C.RESET}\n")
                asia = all_keys
            data = scan_best(asia, limit=20)
            show_list(data, "🇸🇬 အာရှဆာဗာများ")
            if data: copy_top(data,3)
            input(f"  ပြန်ရန် Enter...")
        
        elif sel=="5":
            fav_menu()
        
        elif sel=="6":
            network_info()
        
        elif sel=="7":
            all_keys = load_keys()
            vless = [k for k in all_keys if k["proto"]=="VLESS"]
            ss = [k for k in all_keys if k["proto"]=="SS"]
            vmess = [k for k in all_keys if k["proto"]=="VMESS"]
            trojan = [k for k in all_keys if k["proto"]=="TROJAN"]
        
        elif sel=="0":
            title()
            print(f"  {C.G}✨ ကျေးဇူးပါ! အကောင်းဆုံးဆာဗာရှာနိုင်ပါစေ ✨{C.RESET}")
            break
        
        else:
            print(f"  {C.R}မှားနေပါတယ် 0-7 ကြားသာထည့်ပါ{C.RESET}\n")
            time.sleep(1)

if __name__=="__main__":
    try: main()
    except KeyboardInterrupt:
        print(f"\n\n  {C.G}👑 ပရိုဂရမ်မှ ထွက်ပါပြီ{C.RESET}\n")
    except Exception as e:
        print(f"\n  {C.R}အမှား: {e}{C.RESET}\n")
        input(f"  ဆက်ရန် Enter...")
    
