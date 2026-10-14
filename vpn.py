#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════╗
# ║          🚀 Ultimate VPN Key Finder                      ║
# ║     — Dream Edition ✨ Super Deluxe Ultimate v4.0        ║
# ║              💎 အပြည့်စုံဆုံးဗားရှင်း 💎                   ║
# ╚══════════════════════════════════════════════════════════╝
import urllib.request, base64, socket, time, os, datetime, random, sys

# 🎨 COLOR THEME
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
BD  = "\033[1m"
BOLD = "\033[1m"
RST = "\033[0m"

def clear(): os.system("clear")
def h(): return "─" * 60

# 🌐 YOUR SOURCES - DO NOT CHANGE
SOURCES = [
    ("V2Nodes", "https://www.v2nodes.com/subscriptions/country/all/?key=72BEE427C23A1AF", "b64"),
    ("Shadowmere", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("Shadowmere API", "https://shadowmere.xyz/api/sub/", "txt"),
    ("V2Ray-Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
    ("V2Ray-Configs VLESS", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Splitted-By-Protocol/vless.txt", "txt"),
    ("V2Ray-Configs SS", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Splitted-By-Protocol/ss.txt", "txt"),
]

# 💾 DATA FILES
FAV_FILE = "favorites.txt"
HIST_FILE = "history.txt"
TODAY_FILE = f"daily_{datetime.date.today()}.txt"
favorites = []
history = []

# 📂 LOAD/SAVE DATA
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

def add_history(key):
    global history
    entry = f"{datetime.datetime.now().strftime('%H:%M')}|{key['name']}|{key['url']}"
    history.insert(0, entry)
    history = history[:50]
    with open(HIST_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(history))

# 📡 NETWORK
def get_net():
    try:
        import subprocess
        r = subprocess.run(['ip','link'], capture_output=True, text=True, timeout=3)
        return "📡 WiFi" if 'wlan' in r.stdout.lower() or 'wlp' in r.stdout.lower() else "📱 Mobile Data"
    except: return "❓ Unknown"

# 🌍 COUNTRY & FLAG
def get_country_flag(name):
    flags = {
        "SG": "🇸🇬", "SIN": "🇸🇬", "SINGAPORE": "🇸🇬",
        "US": "🇺🇸", "USA": "🇺🇸", "UNITED STATES": "🇺🇸",
        "JP": "🇯🇵", "JAPAN": "🇯🇵",
        "KR": "🇰🇷", "KOREA": "🇰🇷", "SK": "🇰🇷",
        "HK": "🇭🇰", "HONGKONG": "🇭🇰",
        "TW": "🇹🇼", "TAIWAN": "🇹🇼",
        "UK": "🇬🇧", "GB": "🇬🇧", "ENGLAND": "🇬🇧",
        "DE": "🇩🇪", "GERMANY": "🇩🇪",
        "NL": "🇳🇱", "NETHERLANDS": "🇳🇱",
        "CA": "🇨🇦", "CANADA": "🇨🇦",
        "AU": "🇦🇺", "AUSTRALIA": "🇦🇺",
        "IN": "🇮🇳", "INDIA": "🇮🇳",
        "RU": "🇷🇺", "RUSSIA": "🇷🇺",
        "CN": "🇨🇳", "CHINA": "🇨🇳",
        "TH": "🇹🇭", "THAILAND": "🇹🇭",
        "MY": "🇲🇾", "MALAYSIA": "🇲🇾",
        "VN": "🇻🇳", "VIETNAM": "🇻🇳",
        "ID": "🇮🇩", "INDONESIA": "🇮🇩",
        "PH": "🇵🇭", "PHILIPPINES": "🇵🇭",
        "BR": "🇧🇷", "BRAZIL": "🇧🇷",
        "FR": "🇫🇷", "FRANCE": "🇫🇷",
        "IT": "🇮🇹", "ITALY": "🇮🇹",
        "ES": "🇪🇸", "SPAIN": "🇪🇸",
        "CH": "🇨🇭", "SWITZERLAND": "🇨🇭",
        "SE": "🇸🇪", "SWEDEN": "🇸🇪",
        "NO": "🇳🇴", "NORWAY": "🇳🇴",
        "DK": "🇩🇰", "DENMARK": "🇩🇰",
        "FI": "🇫🇮", "FINLAND": "🇫🇮",
        "NZ": "🇳🇿", "NEW ZEALAND": "🇳🇿",
        "MX": "🇲🇽", "MEXICO": "🇲🇽",
        "ZA": "🇿🇦", "SOUTH AFRICA": "🇿🇦",
    }
    name_upper = name.upper()
    for code, flag in flags.items():
        if code in name_upper: return flag
    return "🌐"

# 🔄 FETCH & PARSE
def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36"})
        with urllib.request.urlopen(req, timeout=25) as r:
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
            if not line or line.startswith("#") or len(line) < 10: continue
            name = "Server"
            if "#" in line:
                try:
                    from urllib.parse import unquote
                    name = unquote(line.split("#")[-1])[:45]
                except: name = line.split("#")[-1][:45]
            flag = get_country_flag(name)
            if line.startswith("vless://"):
                keys.append({"type": "VLESS", "name": name, "url": line, "flag": flag})
            elif line.startswith("ss://"):
                keys.append({"type": "SS", "name": name, "url": line, "flag": flag})
    except: pass
    return keys

def ping_test(url):
    try:
        from urllib.parse import urlparse
        p = urlparse(url)
        host = p.hostname
        port = p.port or 443
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.2)
        st = time.time()
        s.connect((host, port))
        ms = int((time.time() - st)*1000)
        s.close()
        if ms < 40: return True, ms, f"{PINK}⚡ အလွန်မြန်{RST}", 5, "S", "💎"
        if ms < 70: return True, ms, f"{GRN}🚀 အလွန်ကောင်း{RST}", 5, "A", "🌟"
        if ms < 100: return True, ms, f"{GRN}✅ ကောင်းမွန်{RST}", 4, "B", "✨"
        if ms < 180: return True, ms, f"{YEL}⚡ ပုံမှန်{RST}", 3, "C", "🔸"
        if ms < 300: return True, ms, f"{ORG}⚠️ အတော်နှေး{RST}", 2, "D", "🐢"
        return True, ms, f"{RED}🐢 နှေးနေ{RS}", 1, "F", "❌"
    except: return False, 9999, f"{RED}❌ အော့ဖ်လိုင်း{RST}", 0, "X", "❌"

# 📥 LOAD ALL SOURCES
def load_all():
    vless, ss = [], []
    print(f"\n{PUR}╭{h()}╮{RST}")
    print(f"{PUR}│{RST}  {BD}🔄 Sources ဖတ်နေသည်...{RST}{' '*(44)}{PUR}│{RST}")
    print(f"{PUR}├{h()}┤{RST}")
    success_count = 0
    for idx, (name, url, fmt) in enumerate(SOURCES, 1):
        print(f"{PUR}│{RST}  [{idx}/{len(SOURCES)}] {name:<24}", end=" ")
        text = fetch(url)
        if text:
            keys = parse(text, fmt)
            v = sum(1 for k in keys if k["type"]=="VLESS")
            s = sum(1 for k in keys if k["type"]=="SS")
            total = v + s
            if total > 0:
                print(f"{GRN}✓{RST} VLESS:{v:>4}  SS:{s:>4}  စုစုပေါင်း:{total:>4}")
                vless.extend([k for k in keys if k["type"]=="VLESS"])
                ss.extend([k for k in keys if k["type"]=="SS"])
                success_count += 1
            else:
                print(f"{YEL}⚠️  ကီးမတွေ့{RST}")
        else:
            print(f"{RED}✗ မရနိုင်ပါ{RST}")
    print(f"{PUR}╰{h()}╯{RST}")
    print(f"\n{GRN}✅ ရင်းမြစ် {success_count}/{len(SOURCES)} ခု အောင်မြင်စွာဖတ်ပြီး{RS}")
    load_favorites()
    return vless, ss

# 📋 SHOW SERVER CARD
def show_card(s, idx=None, show_url=True):
    stars = "⭐"*s["sc"] + "☆"*(5-s["sc"])
    idx_str = f"[{idx:02d}] " if idx else ""
    print(f"  {s['flag']} {idx_str}{BD}{s['name']}{RST}")
    print(f"     ├─ အဆင့်  : {s['rank']} Class  {s['icon']} {s['lvl']}  {stars}")
    print(f"     ├─ Ping   : {CYN}{s['ms']}{RST} ms")
    if show_url:
        print(f"     └─ ကီး    : {s['url'][:75]}...")
    print()

# 💾 SAVE RESULTS
def save_results(results, filename="results.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("═"*60+"\n")
        f.write("🚀 Ultimate VPN Key Finder — Dream Edition ✨ v4.0\n")
        f.write("═"*60+"\n")
        f.write(f"ဖန်တီးချိန် : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"လိုင်းအမျိုးအစား: {get_net()}\n")
        f.write(f"စုစုပေါင်း   : {len(results)} ဆာဗာ\n")
        f.write("═"*60+"\n\n")
        for s in results:
            f.write(f"# {s['flag']} {s['name']} | Ping: {s['ms']}ms | {s['rank']}\n")
            f.write(f"{s['url']}\n\n")
    print(f"{GRN}✅ {filename} ထဲသိမ်းပြီးပါပြီ{RST}")

# 🔍 SCAN & FILTER
def scan(keys, title, min_score=0, max_ping=9999, sort_by="ping"):
    if not keys:
        print(f"\n{YEL}⚠️ အရင် [1] ကိုနှိပ်ပြီး Sources ဖတ်ပါ{RST}")
        time.sleep(1.5)
        return []
    results = []
    print(f"\n{PUR}🔍 {title}{RST}\n")
    total = len(keys)
    for i, k in enumerate(keys, 1):
        pct = int(i/total*100)
        bar = "█"*(pct//5) + "░"*(20 - pct//5)
        print(f"  တိုးတက်မှု: [{bar}] {pct:>3}%  ({i}/{total})", end="\r")
        ok, ms, lvl, sc, rank, icon = ping_test(k["url"])
        if ok and sc >= min_score and ms <= max_ping:
            k.update({"ms":ms,"lvl":lvl,"sc":sc,"rank":rank,"icon":icon})
            results.append(k)
    if sort_by == "ping":
        results.sort(key=lambda x:x["ms"])
    elif sort_by == "score":
        results.sort(key=lambda x:(-x["sc"], x["ms"]))
    elif sort_by == "name":
        results.sort(key=lambda x:x["name"])
    print("\n\n")
    return results

# 🏆 TOP N FASTEST
def show_top_n(keys, proto, n=10):
    results = scan(keys, f"{proto} အကောင်းဆုံး {n} လုံးကိုရှာဖွေနေသည်...", sort_by="ping")
    if not results: return
    top = results[:n]
    print(f"{PUR}🏆 {proto} အမြန်ဆုံး Top {n}{RST}\n")
    for i, s in enumerate(top, 1):
        show_card(s, i)
    save_results(top, f"top{n}_{proto}.txt")
    input(f"\n{CYN}ပြန်ရန် Enter နှိပ်ပါ...{RST}")

# 💖 FAVORITES SYSTEM
def manage_favorites(all_keys):
    while True:
        clear()
        print(f"{PINK}💖 အကြိုက်ဆုံးများ ({len(favorites)} ခု){RST}\n")
        if not favorites:
            print(f"{DIM}မရှိသေးပါ။ စကင်လုပ်ပြီးရင် [S] နှိပ်ပြီးသိမ်းနိုင်ပါတယ်{RST}")
        else:
            for i, url in enumerate(favorites, 1):
                preview = url.split("#")[-1][:35] if "#" in url else f"Server {i}"
                flag = get_country_flag(preview)
                print(f"  [{i}] {flag} {preview}")
                print(f"      {url[:65]}...")
                print()
        print(f"{PUR}─"*30 + f"{RST}")
        print(f"  [A] အားလုံးကို ဖိုင်တစ်ခုထဲကူးယူရန်")
        print(f"  [C] အရွေးချယ်ထားသည့်တစ်ခုကို ကူးယူရန်")
        print(f"  [D] တစ်ခုကိုဖျက်ရန်")
        print(f"  [R] အားလုံးကိုဖျက်ရန်")
        print(f"  [X] ပြန်သွားရန်")
        ch = input(f"\n  ရွေးပါ → ").upper()
        if ch == "X": break
        elif ch == "A" and favorites:
            with open("my_favorites.txt", "w", encoding="utf-8") as f:
                f.write("═"*50+"\n")
                f.write("💖 ကျွန်ုပ့်အကြိုက်ဆုံး VPN Keys များ\n")
                f.write("═"*50+"\n\n")
                f.write("\n\n".join(favorites))
            print(f"{GRN}✅ my_favorites.txt ထဲသိမ်းပြီးပါပြီ{RST}")
            time.sleep(1.5)
        elif ch == "C" and favorites:
            try:
                idx = int(input(f"နံပါတ်ရိုက်ထည့်ပါ → ")) - 1
                if 0 <= idx < len(favorites):
                    print(f"\n🔑 ကီးအပြည့်အစုံ-")
                    print(f"  {favorites[idx]}")
                    input(f"\n{CYN}ပြန်ရန် Enter နှိပ်ပါ...{RST}")
            except: print(f"{RED}မှားနေပါတယ်{RST}")
        elif ch == "D" and favorites:
            try:
                idx = int(input(f"ဖျက်မည့်နံပါတ် → ")) - 1
                if 0 <= idx < len(favorites):
                    favorites.pop(idx)
                    save_favorites()
                    print(f"{RED}🗑️ ဖျက်ပြီးပါပြီ{RST}")
                    time.sleep(1)
            except: print(f"{RED}မှားနေပါတယ်{RST}")
        elif ch == "R":
            if input(f"အားလုံးဖျက်မှာလား? (Y/N) → ").upper() == "Y":
                favorites.clear()
                save_favorites()
                print(f"{RED}🗑️ အားလုံးဖျက်ပြီးပါပြီ{RST}")
                time.sleep(1)

# ⚡ INSTANT BEST ONE
def instant_best(all_keys):
    results = scan(all_keys, "အကောင်းဆုံးကိုရှာဖွေနေသည်...", min_score=3, sort_by="score")
    if not results: return
    best = results[0]
    clear()
    print(f"{PUR}╔{h()}╗{RST}")
    print(f"{PUR}║{RST}        🏆 သင့်အတွက် အကောင်းဆုံးကီး{PUR}║{RST}")
    print(f"{PUR}╠{h()}┤{RST}")
    show_card(best)
    print(f"{PUR}╠{h()}╣{RST}")
    print(f"{PUR}║{RST}  [S] 💖 အကြိုက်ဆုံးသိမ်းမည်    [C] 📋 ကီးကူးယူမည်{PUR}║{RST}")
    print(f"{PUR}║{RST}  [မျှဝေရမျှဝေရန်ပြင်ဆင်မည််ပြင်ဆင်မည်] 📤 မျှဝေရန်ပြင်ဆင်မည်    [X] 🔙 
    ပြန်သွားမည်{PUR}║{RST}")
    print(f"{PUR}╚{h()}╝{RST}")
    ch = input(f"\n  ရွေးပါ → ").upper()
    if ch == "S":
        if best["url"] not in favorites:
            favorites.append(best["url"])
            save_favorites()
            add_history(best)
            print(f"{PINK}💖 သိမ်းဆည်းပြီးပါပြီ!{RST}")
        else:
            print(f"{YEL}ဒါ သိမ်းပြီးသားဖြစ်နေပါတယ်{RST}")
        time.sleep(1)
    elif ch == "C":
        print(f"\n📋 ကီးအပြည့်အစုံ-")
        print(f"  {best['url']}")
        input(f"\n{CYN}ပြန်ရန် Enter နှိပ်ပါ...{RST}")
    elif ch == "T":
        share_single(best)

# 🌏 SEARCH BY COUNTRY
def search_by_country(all_keys):
    clear()
    print(f"{CYN}🌏 နိုင်ငံအလိုက် ရှာဖွေခြင်း{RST}\n")
    print(f"  SG 🇸🇬 စင်ကာပူ   US 🇺🇸 အမေရိကန်   JP 🇯🇵 ဂျပန်")
    print(f"  HK 🇭🇰 ဟောင်ကောင်  KR 🇰🇷 ကိုရီးယား   TW 🇹🇼 ထိုင်ဝမ်")
    print(f"  UK 🇬🇧 ဗြိတိန်    DE 🇩🇪 ဂျာမနီ    MY 🇲🇾 မလေးရှား")
    print(f"  TH 🇹🇭 ထိုင်းနိုင်ငံ  VN 🇻🇳 ဗီယက်နမ်  IN 🇮🇳 အိန္ဒိယ")
    print(f"  -- အားလုံးကိုကြည့်လိုရင် ဘာမှမရိုက်ဘဲ Enter နှိပ်ပါ --")
    code = input(f"\n  နိုင်ငံကုဒ်ရိုက်ထည့်ပါ → ").upper().strip()
    filtered = all_keys
    if code:
        filtered = [k for k in all_keys if code in k["name"].upper()]
        if not filtered:
            print(f"{RED}❌ {code} နိုင်ငံမှ ဆာဗာမတွေ့ပါ{RST}")
            time.sleep(2)
            return
    results = scan(filtered, f"ဆာဗာ {len(filtered)} လုံးကိုစစ်ဆေးနေသည်...", sort_by="ping")
    if not results: return
    print(f"{GRN}✅ {code or 'အားလုံး'} ဆာဗာ {len(results)} လုံးအလုပ်လုပ်နေ{RS}\n")
    show_count = min(len(results), 15)
    for i, s in enumerate(results[:show_count], 1):
        show_card(s, i)
    if len(results) > show_count:
        print(f"{DIM}... နောက်ထပ် {len(results) - show_count} လုံးရှိပါသည်၊ ဖိုင်ထဲတွင်အပြည့်အစုံကြည့်ပါ{RST}\n")
    save_results(results, f"country_{code or 'all'}.txt")
    input(f"\n{CYN}ပြန်ရန် Enter နှိပ်ပါ...{RST}")

# 📤 SHARE TOOLS
def share_single(key):
    clear()
    name = key["name"][:25]
    print(f"{PUR}📤 မျှဝေရန် ပြင်ဆင်ခြင်း — {name}{RST}\n")
    print(f"  [1] Telegram ဖော်မတ်")
    print(f"  [2] Facebook ဖော်မတ်")
    print(f"  [3] WhatsApp ဖော်မတ်")
    print(f"  [4] Instagram / Story")
    print(f"  [5] ကိုယ်ပိုင်မက်ဆေ့ချ်ထည့်ရန်")
    print(f"  [0] ပြန်ရန်")
    ch = input(f"\n  ရွေးပါ → ")
    output = ""
    if ch == "1":
        output = f"🚀 VPN Key — Dream Edition ✨\n\n🌍 {key['flag']} {key['name']}\n⚡ Ping: {key.get('ms','?')}ms\n🔑 {key['url']}\n\n✨ #VPN #FreeInternet #{datetime.date.today()}"
    elif ch == "2":
        output = f"✨ VPN Key မျှဝေခြင်း ✨\n\n🌍 {key['flag']} {key['name']}\n⚡ အမြန်နှုန်း: {key.get('ms','စစ်ဆေးပါ')}ms\n🔑 ကီး- {key['url']}\n\n#VPN #အခမဲ့အင်တာနက် #DreamEdition"
    elif ch == "3":
        output = f"✨ VPN Key ✨\n\n{key['flag']} {key['name']}\nPing: {key.get('ms','?')}ms\n\n{key['url']}"
    elif ch == "4":
        output = f"🌍 {key['flag']} {key['name']}\n⚡ Ping: {key.get('ms','?')}ms\n\n🔑 ကီးကို ကူးယူပြီး V2Ray/Clash အက်ပ်ထဲထည့်ပါ ✨\n\n#VPN #Free"
    elif ch == "5":
        msg = input(f"ကိုယ်ပိုင်မက်ဆေ့ချ် → ")
        output = f"{msg}\n\n{key['flag']} {key['name']}\n{key['url']}"
    elif ch == "0":
        return
    else:
        print(f"{RED}မှားနေပါတယ်{RST}")
        time.sleep(1)
        return
    print(f"\n{GRN}✅ အဆင်သင့်ဖြစ်ပါပြီ၊ ကူးယူပြီးမျှဝေနိုင်ပါတယ်!{RST}\n")
    print(f"─"*50)
    print(output)
    print(f"─"*50)
    with open("share_key.txt", "w", encoding="utf-8") as f:
        f.write(output)
    input(f"\n{CYN}ပြန်ရန် Enter နှိပ်ပါ...{RST}")

def share_menu():
    clear()
    print(f"{PUR}📤 လူမှုမီဒီယာ မျှဝေကိရိယာ{RST}\n")
    if not os.path.exists("results.txt"):
        print(f"{YEL}⚠️ အရင်စကင်တစ်ခုလုပ်ပါမှ မျှဝေနိုင်မည်{RST}")
        time.sleep(2)
        return
    with open("results.txt", "r", encoding="utf-8") as f:
        content = f.read()
    print(f"  [1] Telegram အုပ်စု/ချန်နယ်")
    print(f"  [2] Facebook ပို့စ်/မက်ဆေ့ချ်")
    print(f"  [3] WhatsApp အုပ်စု")
    print(f"  [4] နေ့စဉ် Update ဖော်မတ်")
    print(f"  [5] သန့်ရှင်းသော ကီးများသာ")
    print(f"  [0] ပြန်ရန်")
    ch = input(f"\n  ရွေးပါ → ")
    output = ""
    if ch == "1":
        output = f"🚀 နေ့စဉ် VPN Keys — Dream Edition ✨\n📅 ရက်စွဲ: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n📡 လိုင်း: {get_net()}\n\n{content}\n\n✨ #VPN #Free #DreamEdition #DailyUpdate"
    elif ch == "2":
        output = f"✨ အခမဲ့ VPN Keys များ ✨\n\nဒီနေ့အတွက် အကောင်းဆုံးဆာဗာများ စုစည်းပေးထားပါတယ်👇\n\n{content}\n\n#VPN #အခမဲ့အင်တာနက် #မျှဝေပါ #DreamEdition"
    elif ch == "3":
        output = f"✨ VPN Keys ✨\n\n{content}"
    elif ch == "4":
        today = datetime.date.today()
        output = f"📅 {today} — နေ့စဉ် VPN Keys ✨\n\n{content}\n\n💎 နေ့စဉ်အသစ်များရယူရန် ကျွန်ုပ်တို့အားလိုက်နာပါ!"
    elif ch == "5":
        lines = [l for l in content.split("\n") if l.strip() and not l.startswith("═") and not l.startswith("#") and "🚀" not in l and "ဖန်တီးချိန်" not in l and "လိုင်းအမျိုးအစား" not in l and "စုစုပေါင်း" not in l]
        output = "\n".join(lines)
    elif ch == "0":
        return
    else:
        print(f"{RED}မှားနေပါတယ်{RST}")
        time.sleep(1)
        return
    with open("share_ready.txt", "w", encoding="utf-8") as f:
        f.write(output)
    print(f"\n{GRN}✅ share_ready.txt ထဲသိမ်းပြီးပါပြီ{RST}")
    print(f"အကြောင်းအရာ-")
    print(f"═"*50)
    print(output)
    print(f"═"*50)
    input(f"\n{CYN}ပြန်ရန် Enter နှိပ်ပါ...{RST}")

# 🎲 RANDOM PICK
def random_pick(all_keys):
    if not all_keys:
        print(f"\n{YEL}⚠️ အရင် Sources ဖတ်ပါ{RST}")
        time.sleep(1.5)
        return
    clear()
    print(f"{PUR}🎲 ကျပန်းရွေးချယ်ခြင်း{RST}\n")
    print(f"  စုစုပေါင်း {len(all_keys)} ကီးထဲမှ ကျပန်းရွေးနေသည်...")
    time.sleep(1)
    for _ in range(5):
        temp = random.choice(all_keys)
        print(f"  → {temp['flag']} {temp['name'][:30]}", end="\r")
        time.sleep(0.15)
    picked = random.choice(all_keys)
    print("\n\n")
    ok, ms, lvl, sc, rank, icon = ping_test(picked["url"])
    picked.update({"ms":ms,"lvl":lvl,"sc":sc,"rank":rank,"icon":icon})
    print(f"{PUR}╔{h()}╗{RST}")
    print(f"{PUR}║{RST}        🎲 ကံကောင်းစွာရွေးချယ်လိုက်သည်!{PUR}║{RST}")
    print(f"{PUR}╠{h()}┤{RST}")
    show_card(picked)
    print(f"{PUR}╠{h()}╣{RST}")
    print(f"{PUR}║{RST}  [R] 🔄 တစ်ခါထပ်ရွေးမည်    [S] 💖 သိမ်းဆည်းမည်{PUR}║{RST}")
    print(f"{PUR}║{RST}  [C] 📋 ကီးကူးယူမည်      [X] 🔙 ပြန်သွားမည်{PUR}║{RST}")
    print(f"{PUR}╚{h()}╝{RST}")
    ch = input(f"\n  ရွေးပါ → ").upper()
    if ch == "R":
        random_pick(all_keys)
    elif ch == "S":
        if picked["url"] not in favorites:
            favorites.append(picked["url"])
            save_favorites()
            print(f"{PINK}💖 သိမ်းဆည်းပြီးပါပြီ!{RST}")
        else:
            print(f"{YEL}ဒါ သိမ်းပြီးသား{RST}")
        time.sleep(1)
    elif ch == "C":
        print(f"\n🔑 {picked['url']}")
        input(f"\n{CYN}ပြန်ရန် Enter နှိပ်ပါ...{RST}")

# 📊 DETAILED STATS
def show_stats(vless, ss):
    clear()
    total = len(vless) + len(ss)
    today = datetime.date.today()
    now = datetime.datetime.now()
    print(f"{PUR}📊 စာရင်းအင်းအချက်အလက်များ{RST}\n")
    print(f"  📅 နေ့ရက်       : {today}")
    print(f"  ⏰ အချိန်        : {now.strftime('%H:%M:%S')}")
    print(f"  📡 လိုင်းအမျိုးအစား : {CYN}{get_net()}{RST}")
    print(f"  📦 ရင်းမြစ်အရေအတွက်: {GRN}{len(SOURCES)}{RST} ခု")
    print(f"  🟦 VLESS Keys    : {BLU}{len(vless):>4}{RST} ခု  {BD}{round(len(vless)/total*100,1) if total else 0}%{RST}")
    print(f"  🟧 SS Keys       : {ORG}{len(ss):>4}{RST} ခု  {BD}{round(len(ss)/total*100,1) if total else 0}%{RST}")
    print(f"  ✨ စုစုပေါင်း Keys  : {WHT}{total:>4}{RST} ခု")
    print(f"  💖 အကြိုက်ဆုံးသိမ်းထား: {PINK}{len(favorites):>4}{RST} ခု")
    print(f"  📜 မှတ်တမ်းများ    : {len(history):>4} ခု")
    print(f"\n{PUR}📁 ဖိုင်များစာရင်း{RST}")
    for f in ["results.txt", "working_keys.txt", "favorites.txt", "history.txt"]:
        exists = f"{GRN}✓ ရှိသည်{RST}" if os.path.exists(f) else f"{DIM}မရှိသေးပါ{RST}"
        size = f"({os.path.getsize(f)} bytes)" if os.path.exists(f) else ""
        print(f"  {f:<20} {exists} {size}")
    input(f"\n{CYN}ပြန်ရန် Enter နှိပ်ပါ...{RST}")

# 🧹 CLEANUP TOOLS
def cleanup_menu():
    while True:
        clear()
        print(f"{PUR}🧹 သန့်ရှင်းရေးကိရိယာ{RST}\n")
        print(f"  [1] သိမ်းဆည်းထားသည့်ဖိုင်အားလုံးကို ဖျက်မည်")
        print(f"  [2] မှတ်တမ်းများကို ဖျက်မည်")
        print(f"  [3] အကြိုက်ဆုံးများကို သန့်ရှင်းမည်")
        print(f"  [4] ယနေ့ဖိုင်များကို သန့်ရှင်းမည်")
        print(f"  [0] ပြန်ရန်")
        ch = input(f"\n  ရွေးပါ → ")
        if ch == "0": break
        elif ch == "1":
            files = ["results.txt", "working_keys.txt", "share_ready.txt", "share_key.txt", "my_favorites.txt"]
            cnt = 0
            for f in files:
                if os.path.exists(f):
                    os.remove(f)
                    cnt += 1
            print(f"{GRN}✅ ဖိုင် {cnt} ခု ဖျက်ပြီးပါပြီ{RST}")
            time.sleep(1.5)
        elif ch == "2":
            if os.path.exists(HIST_FILE):
                os.remove(HIST_FILE)
                history.clear()
                print(f"{GRN}✅ မှတ်တမ်းဖျက်ပြီးပါပြီ{RST}")
            else:
                print(f"{YEL}မှတ်တမ်းမရှိသေးပါ{RST}")
            time.sleep(1.5)
        elif ch == "3":
            if input(f"အကြိုက်ဆုံးအားလုံးဖျက်မှာလား? (Y/N) → ").upper() == "Y":
                favorites.clear()
                save_favorites()
                print(f"{GRN}✅ သန့်ရှင်းပြီးပါပြီ{RST}")
            time.sleep(1.5)
        elif ch == "4":
            cnt = 0
            for f in os.listdir("."):
                if f.startswith("daily_") or f.endswith("_servers.txt") or f.endswith("_keys.txt"):
                    os.remove(f)
                    cnt += 1
            print(f"{GRN}✅ ဖိုင် {cnt} ခု သန့်ရှင်းပြီးပါပြီ{RST}")
            time.sleep(1.5)

# 🏠 MAIN MENU
def main():
    vless, ss = [], []
    while True:
        clear()
        net = get_net()
        total_keys = len(vless) + len(ss)
        print(f"{PUR}╭{h()}╮{RST}")
        print(f"{PUR}│{RST}   {BD}{WHT}🚀 Ultimate VPN Key Finder{RST}{' '*(28)}{PUR}│{RST}")
        print(f"{PUR}│{RST}     {DIM}— Dream Edition ✨ v4.0 Ultimate{' '*(32)}{PUR}│{RST}")
        print(f"{PUR}├{h()}┤{RST}")
        print(f"{PUR}│{RST}  📡 လိုင်းအမျိုးအစား : {net}{' '*(46-len(net))}{PUR}│{RST}")
        print(f"{PUR}│{RST}  📦 ရင်းမြစ်      : {len(SOURCES)}{' '*(48)}{PUR}│{RST}")
        print(f"{PUR}│{RST}  🟦 VLESS       : {BLU}{len(vless)}{RST}{' '*(49-len(str(len(vless))))}{PUR}│{RST}")
        print(f"{PUR}│{RST}  🟧 SS          : {ORG}{len(ss)}{RST}{' '*(49-len(str(len(ss))))}{PUR}│{RST}")
        print(f"{PUR}│{RST}  ✨ စုစုပေါင်း    : {WHT}{total_keys}{RST}{' '*(49-len(str(total_keys)))}{PUR}│{RST}")
        print(f"{PUR}│{RST}  💖 အကြိုက်ဆုံး    : {PINK}{len(favorites)}{RST}{' '*(49-len(str(len(favorites))))}{PUR}│{RST}")
        print(f"{PUR}├{h()}┤{RST}")
        print(f"{PUR}│{RST}  {BD}🔥 အဓိကလုပ်ဆောင်ချက်များ{RST}{' '*(36)}{PUR}│{RST}")
        print(f"{PUR}├{h()}┤{RST}")
        print(f"{PUR}│{RST}  {GRN}[ 01 ]{RST}  🔄 အားလုံးဖတ်ရန်{' '*(44)}{PUR}│{RST}")
        print(f"{PUR}│{RST}  {BLU}[ 02 ]{RST}  🟦 VLESS အမြန်ဆုံး Top 15{' '*(36)}{PUR}│{RST}")
        print(f"{PUR}│{RST}  {ORG}[ 03 ]{RST}  🟧 SS အမြန်ဆုံး Top 15{' '*(40)}{PUR}│{RST}")
        print(f"{PUR}│{RST}  {CYN}[ 04 ]{RST}  ⚡ ကျွန်ုပ့်လိုင်းအတွက် အကောင်းဆုံးတစ်ခု{' '*(24)}{PUR}│{RST}")
        print(f"{PUR}│{RST}  {LIME}[ 05 ]{RST}  🎲 ကျပန်းကီးတစ်လုံးရွေးရန်{' '*(34)}{PUR}│{RST}")
        print(f"{PUR}│{RST}  {YEL}[ 06 ]{RST}  🌏 နိုင်ငံအလိုက်ရှာဖွေရန်{' '*(36)}{PUR}│{RST}")
        print(f"{PUR}│{RST}  {PINK}[ 07 ]{RST}  💖 အကြိုက်ဆုံးများ စီမံရန်{' '*(34)}{PUR}│{RST}")
        print(f"{PUR}│{RST}  {PUR}[ 08 ]{RST}  📤 လူမှုမီဒီယာ မျှဝေကိရိယာ{' '*(30)}{PUR}│{RST}")
        print(f"{PUR}│{RST}  {WHT}[ 09 ]{RST}  📊 အသေးစိတ်စာရင်းအင်းကြည့်ရန်{' '*(30)}{PUR}│{RST}")
        print(f"{PUR}│{RST}  {PUR}[ 10 ]{RST}  🧹 ဖိုင်များသန့်ရှင်းရေး{' '*(38)}{PUR}│{RST}")
        print(f"{PUR}│{RST}  {RED}[ 00 ]{RST}  ❌ ပရိုဂရမ်မှထွက်ရန်{' '*(42)}{PUR}│{RST}")
        print(f"{PUR}╰{h()}╯{RST}")
        ch = input(f"\n  {BD}ရွေးချယ်ပါ → {RST}").strip().zfill(2)
        
        if ch == "00":
            clear()
            print(f"\n{PUR}✨ အသုံးပြုသည့်အတွက်ကျေးဇူးတင်ပါတယ် ✨{RST}")
            print(f"{CYN}   မြန်မြန်ဆန်ဆန် ဘေးကင်းစွာသုံးစွဲပါ 🚀{RST}")
            print(f"{DIM}   — Dream Edition Ultimate v4.0 —{RST}\n")
            break
        elif ch == "01":
            vless, ss = load_all()
            input(f"\n{CYN}ပြီးပါပြီ။ Enter နှိပ်ပါ...{RST}")
        elif ch == "02":
            show_top_n(vless, "VLESS", 15)
        elif ch == "03":
            show_top_n(ss, "SS", 15)
        elif ch == "04":
            all_keys = vless + ss
            instant_best(all_keys)
        elif ch == "05":
            all_keys = vless + ss
            random_pick(all_keys)
        elif ch == "06":
            all_keys = vless + ss
            search_by_country(all_keys)
        elif ch == "07":
            manage_favorites(vless + ss)
        elif ch == "08":
            share_menu()
        elif ch == "09":
            show_stats(vless, ss)
        elif ch == "10":
            cleanup_menu()
        else:
            print(f"\n{RED}မှားနေပါတယ်၊ ပြန်ရွေးပါ{RST}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print(f"\n\n{PUR}✨ ပရိုဂရမ်မှထွက်သွားပါပြီ ✨{RST}\n")
        sys.exit(0)
    
