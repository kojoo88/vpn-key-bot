#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════╗
# ║          🚀 Ultimate VPN Key Finder                      ║
# ║              — Dream Edition ✨ v2.0                      ║
# ╚══════════════════════════════════════════════════════════╝
import urllib.request, base64, socket, time, os, datetime, sys

# 🎨 COLOR THEME
BLK = "\033[38;5;234m"
BLU = "\033[38;5;117m"
CYN = "\033[38;5;80m"
GRN = "\033[38;5;114m"
YEL = "\033[38;5;221m"
ORG = "\033[38;5;215m"
RED = "\033[38;5;209m"
PUR = "\033[38;5;141m"
WHT = "\033[38;5;255m"
DIM = "\033[2m"
BD  = "\033[1m"
RST = "\033[0m"

def clear(): os.system("clear")
def h(): return "─" * 54

# 🌐 YOUR SOURCES - DO NOT CHANGE
SOURCES = [
    ("V2Nodes", "https://www.v2nodes.com/subscriptions/country/all/?key=72BEE427C23A1AF", "b64"),
    ("Shadowmere", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("V2Ray-Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
    ("V2Ray-Configs SS", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Splitted-By-Protocol/ss.txt", "txt"),
]

# 📡 NETWORK
def get_net():
    try:
        import subprocess
        r = subprocess.run(['ip','link'], capture_output=True, text=True, timeout=3)
        return "📡 WiFi" if 'wlan' in r.stdout.lower() or 'wlp' in r.stdout.lower() else "📱 Mobile Data"
    except: return "❓ Unknown"

# 🔄 FETCH & PARSE
def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", errors="ignore")
    except: return None

def parse(text, fmt):
    keys = []
    if not text: return keys
    try:
        if fmt == "b64":
            text = base64.b64decode(text).decode("utf-8", errors="ignore")
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"): continue
            name = "Server"
            if "#" in line:
                try:
                    from urllib.parse import unquote
                    name = unquote(line.split("#")[-1])[:36]
                except: name = line.split("#")[-1][:36]
            if line.startswith("vless://"):
                keys.append({"type": "VLESS", "name": name, "url": line})
            elif line.startswith("ss://"):
                keys.append({"type": "SS", "name": name, "url": line})
    except: pass
    return keys

def ping_test(url):
    try:
        from urllib.parse import urlparse
        p = urlparse(url)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        st = time.time()
        s.connect((p.hostname, p.port or 443))
        ms = int((time.time() - st)*1000)
        s.close()
        if ms < 80: return True, ms, f"{GRN}🚀 အမြန်ဆန်{RST}", 5
        if ms < 150: return True, ms, f"{GRN}✅ ကောင်းမွန်{RST}", 4
        if ms < 250: return True, ms, f"{YEL}⚡ ပုံမှန်{RST}", 3
        if ms < 400: return True, ms, f"{ORG}⚠️ နှေး{RST}", 2
        return True, ms, f"{RED}🐢 နှေးနေ{RS}", 1
    except: return False, 9999, f"{RED}❌ အော့ဖ်လိုင်း{RST}", 0

# 📥 LOAD SOURCES
def load_all():
    vless, ss = [], []
    print(f"\n{PUR}╭{h()}╮{RST}")
    print(f"{PUR}│{RST}  {BD}🔄 Sources ဖတ်နေသည်...{RST}{' '*(36)}{PUR}│{RST}")
    print(f"{PUR}├{h()}┤{RST}")
    for name, url, fmt in SOURCES:
        print(f"{PUR}│{RST}  {name:<20}", end=" ")
        text = fetch(url)
        if text:
            keys = parse(text, fmt)
            v = sum(1 for k in keys if k["type"]=="VLESS")
            s = sum(1 for k in keys if k["type"]=="SS")
            print(f"{GRN}✓{RST} VLESS:{v:>3}  SS:{s:>3}")
            vless.extend([k for k in keys if k["type"]=="VLESS"])
            ss.extend([k for k in keys if k["type"]=="SS"])
        else:
            print(f"{RED}✗ မရနိုင်ပါ{RST}")
    print(f"{PUR}╰{h()}╯{RST}")
    return vless, ss

# 🔍 SCAN & SORT
def scan_all(keys, label, sort_by="ping"):
    if not keys:
        print(f"\n{YEL}⚠️ အရင် Sources ဖတ်ပါ [1] ကိုနှိပ်ပါ{RST}")
        time.sleep(1.5)
        return []
    results = []
    print(f"\n{PUR}🔍 {label} စစ်ဆေးနေသည်...{RST}\n")
    for i, k in enumerate(keys, 1):
        print(f"  [{i}/{len(keys)}] {k['name'][:35]:<35}", end="\r")
        ok, ms, lvl, sc = ping_test(k["url"])
        if ok:
            k.update({"ms":ms,"lvl":lvl,"sc":sc})
            results.append(k)
    if sort_by == "ping":
        results.sort(key=lambda x:x["ms"])
    elif sort_by == "stars":
        results.sort(key=lambda x:(-x["sc"], x["ms"]))
    print("\n\n")
    return results

# 📋 DISPLAY RESULTS
def show_results(results, title):
    if not results:
        print(f"{RED}❌ အလုပ်လုပ်သော Server မတွေ့ပါ{RST}")
        time.sleep(2)
        return
    print(f"{GRN}🎉 {title}: {len(results)} လုံးတွေ့ရှိ{RST}\n")
    for i, s in enumerate(results, 1):
        stars = "⭐"*s["sc"] + "☆"*(5-s["sc"])
        print(f"  {BD}[{i}]{RST} {s['lvl']}  Ping: {s['ms']:>4}ms  {stars}")
        print(f"      📌 {s['name']}")
        print(f"      🔑 {s['url'][:75]}...")
        print()
    save_results(results)

# 💾 SAVE
def save_results(results):
    with open("working_keys.txt", "w", encoding="utf-8") as f:
        f.write("="*50+"\n")
        f.write("🚀 Ultimate VPN Key Finder — Dream Edition ✨\n")
        f.write("="*50+"\n")
        f.write(f"Updated : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Network : {get_net()}\n")
        f.write(f"Total   : {len(results)} servers\n")
        f.write("="*50+"\n\n")
        for s in results: f.write(f"{s['url']}\n")
    print(f"{GRN}✅ working_keys.txt ထဲသိမ်းပြီးပါပြီ{RST}")

# 📄 VIEW SAVED
def view_file():
    clear()
    print(f"{PUR}📄 သိမ်းဆည်းထားသော Keys{RS}\n")
    if not os.path.exists("working_keys.txt"):
        print(f"{RED}ဖိုင်မရှိသေးပါ။ အရင်စကင်လုပ်ပါ{RST}")
        time.sleep(2)
        return
    with open("working_keys.txt", "r", encoding="utf-8") as f:
        print(f.read())
    input(f"\n{CYN}ပြန်ရန် Enter နှိပ်ပါ...{RST}")

# 🌟 FIND BEST FOR MY NETWORK
def find_best_match(keys):
    if not keys:
        print(f"\n{YEL}⚠️ အရင် Sources ဖတ်ပါ{RST}")
        time.sleep(1.5)
        return
    results = scan_all(keys, "အကောင်းဆုံးရှာဖွေခြင်း", sort_by="stars")
    if results:
        best = results[0]
        print(f"\n{PUR}╔{h()}╗{RST}")
        print(f"{PUR}║{RST}  🏆 သင့်လိုင်းအတွက် အကောင်းဆုံး Server{PUR}║{RST}")
        print(f"{PUR}╠{h()}┤{RST}")
        stars = "⭐"*best["sc"] + "☆"*(5-best["sc"])
        print(f"{PUR}║{RST}  အဆင့်  : {stars}{' '*(35)}{PUR}║{RST}")
        print(f"{PUR}║{RST}  Ping   : {best['ms']}ms{' '*(38-len(str(best['ms'])))}{PUR}║{RST}")
        print(f"{PUR}║{RST}  နာမည် : {best['name'][:40]}{' '*(42-len(best['name'][:40]))}{PUR}║{RST}")
        print(f"{PUR}║{RST}  ကီး    : {best['url'][:50]}...{' '*(4)}{PUR}║{RST}")
        print(f"{PUR}╚{h()}╝{RST}")
        print(f"\n🔑 ကီးအပြည့်အစုံ-")
        print(f"  {best['url']}\n")
        save_results([best])
    input(f"\n{CYN}ပြန်ရန် Enter နှိပ်ပါ...{RST}")

# 📊 SHOW STATS
def show_stats(vless, ss):
    clear()
    total = len(vless) + len(ss)
    print(f"{PUR}📊 အချက်အလက်အကျဉ်း{RST}\n")
    print(f"  စုစုပေါင်း Sources : {GRN}{len(SOURCES)}{RST} ခု")
    print(f"  VLESS Keys         : {BLU}{len(vless)}{RST} ခု")
    print(f"  SS Keys            : {ORG}{len(ss)}{RST} ခု")
    print(f"  စုစုပေါင်း Keys   : {WHT}{total}{RST} ခု")
    print(f"  လက်ရှိလိုင်းအမျိုးအစား: {CYN}{get_net()}{RST}")
    print(f"  နောက်ဆုံးဖတ်ချိန်   : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    input(f"\n{CYN}ပြန်ရန် Enter နှိပ်ပါ...{RST}")

# 🏠 MAIN MENU
def main():
    vless, ss = [], []
    while True:
        clear()
        net = get_net()
        print(f"{PUR}╭{h()}╮{RST}")
        print(f"{PUR}│{RST}   {BD}{WHT}🚀 Ultimate VPN Key Finder{RST}{' '*(24)}{PUR}│{RST}")
        print(f"{PUR}│{RST}      {DIM}— Dream Edition ✨ v2.0{' '*(30)}{PUR}│{RST}")
        print(f"{PUR}├{h()}┤{RST}")
        print(f"{PUR}│{RST}  📡 လိုင်းအမျိုးအစား : {net}{' '*(42-len(net))}{PUR}│{RST}")
        print(f"{PUR}│{RST}  📦 ရင်းမြစ်အရေအတွက်: {len(SOURCES)}{' '*(44)}{PUR}│{RST}")
        print(f"{PUR}│{RST}  🟦 VLESS Keys    : {BLU}{len(vless)}{RST}{' '*(45-len(str(len(vless))))}{PUR}│{RST}")
        print(f"{PUR}│{RST}  🟧 SS Keys       : {ORG}{len(ss)}{RST}{' '*(45-len(str(len(ss))))}{PUR}│{RST}")
        print(f"{PUR}├{h()}┤{RST}")
        print(f"{PUR}│{RST}  {BD}📌 ခလုတ်များကိုရွေးပါ{RST}{' '*(38)}{PUR}│{RST}")
        print(f"{PUR}├{h()}┤{RST}")
        print(f"{PUR}│{RST}  {GRN}[ 1 ]{RST}  🔄 အရင်းမြစ်အားလုံးဖတ်ရန်{' '*(36)}{PUR}│{RST}")
        print(f"{PUR}│{RST}  {BLU}[ 2 ]{RST}  🟦 VLESS Keys စစ်ပြီးအမြန်ဆုံးရန်{' '*(28)}{PUR}│{RST}")
        print(f"{PUR}│{RST}  {ORG}[ 3 ]{RST}  🟧 SS Keys စစ်ပြီးအမြန်ဆုံးရန်{' '*(32)}{PUR}│{RST}")
        print(f"{PUR}│{RST}  {CYN}[ 4 ]{RST}  🏆 ကျွန်ုပ့်လိုင်းနှင့်အကိုက်ညီဆုံးရှာရန်{' '*(22)}{PUR}│{RST}")
        print(f"{PUR}│{RST}  {YEL}[ 5 ]{RST}  📊 အချက်အလက်ကြည့်ရန်{' '*(36)}{PUR}│{RST}")
        print(f"{PUR}│{RST}  {PUR}[ 6 ]{RST}  📄 သိမ်းထားသော Keys ကြည့်ရန်{' '*(30)}{PUR}│{RST}")
        print(f"{PUR}│{RST}  {RED}[ 0 ]{RST}  ❌ ပရိုဂရမ်မှထွက်ရန်{' '*(38)}{PUR}│{RST}")
        print(f"{PUR}╰{h()}╯{RST}")
        ch = input(f"\n  {BD}ရွေးချယ်ပါ → {RST}").strip()
        
        if ch == "0":
            clear()
            print(f"\n{PUR}✨ အသုံးပြုသည့်အတွက်ကျေးဇူးတင်ပါတယ် ✨{RST}")
            print(f"{CYN}   မြန်မြန်ဆန်ဆန် ဘေးကင်းစွာသုံးစွဲပါ 🚀{RST}\n")
            break
        elif ch == "1":
            vless, ss = load_all()
            input(f"\n{CYN}ပြီးပါပြီ။ Enter နှိပ်ပါ...{RST}")
        elif ch == "2":
            results = scan_all(vless, "VLESS Keys")
            show_results(results, "VLESS အကောင်းဆုံးများ")
            input(f"\n{CYN}ပြန်ရန် Enter နှိပ်ပါ...{RST}")
        elif ch == "3":
            results = scan_all(ss, "SS Keys")
            show_results(results, "SS အကောင်းဆုံးများ")
            input(f"\n{CYN}ပြန်ရန် Enter နှိပ်ပါ...{RST}")
        elif ch == "4":
            all_keys = vless + ss
            find_best_match(all_keys)
        elif ch == "5":
            show_stats(vless, ss)
        elif ch == "6":
            view_file()
        else:
            print(f"\n{RED}မှားနေပါတယ်၊ ပြန်ရွေးပါ{RST}")
            time.sleep(1)

if __name__ == "__main__":
    main()
                    
