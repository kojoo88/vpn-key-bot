#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, base64, os, socket, time, json, sys
from datetime import datetime

VERSION = "🏆 ETERNAL SUPREME v8.0"
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
╔═════════════════════════════════════╗
║     {C.B}🏆 ETERNAL SUPREME v8.0 🏆{C.RESET}{C.G}     ║
║   Beyond stars, beyond time ✨       ║
╚═════════════════════════════════════╝{C.RESET}""")
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

SOURCES = [
    ("Shadowmere API","https://shadowmere.xyz/api/b64sub/","b64"),
    ("Epodonios VLESS","https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/vless.txt","txt"),
    ("Epodonios SS","https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/ss.txt","txt"),
    ("MatinGhanbari VLESS","https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/vless.txt","txt"),
    ("MatinGhanbari SS","https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/ss.txt","txt"),
    ("Argh73 Vault","https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt","txt"),
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
        if not proto: continue
        name = line.split("#")[-1] if "#" in line else f"{proto} Server"
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
        s.connect((host, port))
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
    return "🌐 --"

def rank(ms):
    if ms==9999: return f"{C.R}✖ OFFLINE{C.RESET}"
    if ms<60: return f"{C.G}👑 S-TIER {C.E}●{ms}ms{C.RESET}"
    if ms<100: return f"{C.D}💎 A-TIER {C.S}●{ms}ms{C.RESET}"
    if ms<180: return f"{C.W}⭐ B-TIER {C.A}●{ms}ms{C.RESET}"
    return f"{C.N}⚡ C-TIER {C.R}●{ms}ms{C.RESET}"

def load_keys():
    all_keys = []
    seen = set()
    title()
    print(f"  {C.S}📡 ကီးများရယူနေသည်...{C.RESET}\n")
    for name, url, t in SOURCES:
        print(f"  ▸ {name}...", end=" ")
        c = fetch((name,url,t))
        if c:
            ks = parse(c, t)
            cnt=0
            for k in ks:
                if k["key"] not in seen:
                    seen.add(k["key"])
                    all_keys.append(k)
                    cnt+=1
            print(f"{C.E}✓ {cnt} ခု{C.RESET}")
        else:
            print(f"{C.R}✖ မရရှိ{C.RESET}")
    print(f"\n  {C.G}✨ စုစုပေါင်း: {len(all_keys)} ခု အဆင်သင့်{C.RESET}\n")
    time.sleep(1)
    return all_keys

def scan_best(keys, limit=15):
    title()
    print(f"  {C.S}⚡ အကောင်းဆုံးများကို ရွေးချယ်နေသည်...{C.RESET}\n")
    res = []
    total = min(len(keys), limit)
    for i in range(total):
        k = keys[i]
        h,p = get_host(k["key"])
        ms = ping(h,p) if h else 9999
        res.append({"name":k["name"],"key":k["key"],"proto":k["proto"],"ms":ms})
        pct = int((i+1)/total*100)
        bar = "█"*int(pct/5)+"░"*(20-int(pct/5))
        print(f"\r  [{bar}] {pct}%", end="")
    print("\n")
    res.sort(key=lambda x:x["ms"])
    return [r for r in res if r["ms"]<400]

def show_list(data, title_text):
    if not data:
        print(f"  {C.R}မတွေ့ပါ{C.RESET}\n")
        return
    print(f"  {C.G}{title_text}  ({len(data)} ခု){C.RESET}")
    print(f"  ┌──┬─────────┬──────────────────┬─────────────────────────────┐")
    print(f"  │# │ နိုင်ငံ  │ အဆင့်            │ အမည်                        │")
    print(f"  ├──┼─────────┼──────────────────┼─────────────────────────────┤")
    for i,r in enumerate(data,1):
        print(f"  │{i:<2}│ {flag(r['name']):<7} │ {rank(r['ms']):<16} │ {r['name'][:28]:<28} │")
    print(f"  └──┴─────────┴──────────────────┴─────────────────────────────┘\n")

def copy_top(data, n=3):
    if not data: return
    top = data[:n]
    keys_text = "\n".join([r["key"] for r in top])
    print(f"  {C.G}💎 အကောင်းဆုံး {len(top)} ခု ကီးများ{C.RESET}")
    print("  "+"═"*65)
    for r in top:
        print(f"  နိုင်ငံ: {flag(r['name'])}  အဆင့်: {rank(r['name'])}")
        print(f"  ကီး: {r['key'][:60]}...")
        print()
    ok = copy_t(keys_text)
    if ok:
        print(f"  {C.E}✓ ကလစ်ဘုတ်သို့ ကူးယူပြီးပါပြီ!{C.RESET}")
    else:
        print(f"  {C.A}⚠️ အထက်က ကီးကို ကိုယ်တိုင်ကူးပါ{C.RESET}")
    print()
    return top

def fav_menu():
    while True:
        title()
        favs = load_fav()
        if not favs:
            print(f"  {C.A}အကြိုက်ဆုံး မရှိသေးပါ{C.RESET}\n")
        else:
            print(f"  {C.G}⭐ အကြိုက်ဆုံး ({len(favs)} ခု){C.RESET}")
            print(f"  ┌──┬─────────┬──────────────────────────────┬──────────────┐")
            print(f"  │# │ နိုင်ငံ  │ အမည်                        │ သိမ်းခဲ့စဉ်   │")
            print(f"  ├──┼─────────┼──────────────────────────────┼──────────────┤")
            for i,f in enumerate(favs,1):
                print(f"  │{i:<2}│ {flag(f['name']):<7} │ {f['name'][:30]:<30} │ {f['saved_at']:<12} │")
            print(f"  └──┴─────────┴──────────────────────────────┴──────────────┘")
            print(f"  နံပါတ်ထည့်ပါ = ကီးကူးယူမည်")
        print(f"  0 = ပင်မမီနူး")
        sel = input(f"\n  {C.S}ရွေးချယ်ပါ → {C.RESET}").strip()
        if sel=="0": break
        if sel.isdigit() and favs:
            idx = int(sel)-1
            if 0<=idx<len(favs):
                copy_t(favs[idx]["key"])
                print(f"  {C.E}✓ ကူးယူပြီးပါပြီ!{C.RESET}\n")
                time.sleep(1)

def main():
    all_keys = load_keys()
    vless = [k for k in all_keys if k["proto"]=="VLESS"]
    ss = [k for k in all_keys if k["proto"]=="SS"]
    
    while True:
        title()
        print(f"  🟦 VLESS: {len(vless)}  │  🟩 SS: {len(ss)}")
        print(f"\n  {C.G}ပင်မမီနူး{C.RESET}")
        print(f"  ───────────────────────────────")
        print(f"  [1] ⚡ အကောင်းဆုံး VLESS ရှာမည်")
        print(f"  [2] 🟩 အကောင်းဆုံး SS ရှာမည်")
        print(f"  [3] 🏆 အကောင်းဆုံး ၃ ခု")
        print(f"  [4] ⭐ အကြိုက်ဆုံးများ")
        print(f"  [5] 🔄 ကီးအသစ်ပြန်ဖတ်မည်")
        print(f"  [0] ✖ ထွက်မည်")
        sel = input(f"\n  {C.S}ရွေးချယ်ပါ → {C.RESET}").strip()
        
        if sel=="1":
            if not vless:
                print(f"  {C.A}VLESS မရှိပါ{C.RESET}\n")
                time.sleep(1)
                continue
            data = scan_best(vless)
            show_list(data, "⚡ VLESS ရလဒ်များ")
            if data: copy_top(data,3)
            input(f"  ပြန်ရန် Enter...")
        elif sel=="2":
            if not ss:
                print(f"  {C.A}SS မရှိပါ{C.RESET}\n")
                time.sleep(1)
                continue
            data = scan_best(ss)
            show_list(data, "🟩 SS ရလဒ်များ")
            if data: copy_top(data,3)
            input(f"  ပြန်ရန် Enter...")
        elif sel=="3":
            if not all_keys:
                print(f"  {C.A}ကီးမရှိပါ{C.RESET}\n")
                time.sleep(1)
                continue
            data = scan_best(all_keys, 20)
            show_list(data, "🏆 အကောင်းဆုံးအားလုံး")
            if data: copy_top(data,3)
            input(f"  ပြန်ရန် Enter...")
        elif sel=="4":
            fav_menu()
        elif sel=="5":
            all_keys = load_keys()
            vless = [k for k in all_keys if k["proto"]=="VLESS"]
            ss = [k for k in all_keys if k["proto"]=="SS"]
        elif sel=="0":
            title()
            print(f"  {C.G}✨ ကျေးဇူးပါ! ✨{C.RESET}")
            break
        else:
            print(f"  {C.R}မှားနေပါတယ်{C.RESET}\n")
            time.sleep(1)

if __name__=="__main__":
    try: main()
    except KeyboardInterrupt:
        print(f"\n\n  {C.G}👑 ပရိုဂရမ်မှ ထွက်ပါပြီ{C.RESET}\n")
    except Exception as e:
        print(f"\n  {C.R}အမှား: {e}{C.RESET}\n")

