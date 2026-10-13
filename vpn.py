#!/usr/bin/env python3
import urllib.request, urllib.error, json, base64, os, sys, socket, time

os.environ["TERM"] = "xterm-256color"

VERSION = "4.0 ✨ PREMIUM"
FAV_FILE = os.path.expanduser("~/.vpn_favorites.txt")

API_LIST = {
    "1": ("Shadowmere JSON", "https://shadowmere.xyz/api/sub/", "json"),
    "2": ("Shadowmere Base64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    "3": ("VLESS List", "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/vless.txt", "txt")
}

def clear(): os.system("clear")

# ==========================================
#        🎨 Premium UI Design
# ==========================================
class Colors:
    P = "\033[95m"   # Purple
    C = "\033[96m"   # Cyan
    G = "\033[92m"   # Green
    Y = "\033[93m"   # Yellow
    R = "\033[91m"   # Red
    B = "\033[94m"   # Blue
    W = "\033[97m"   # White
    D = "\033[90m"   # Dim
    rst = "\033[0m"

def header():
    clear()
    c = Colors()
    print(f"{c.P}╔══════════════════════════════════════════════════════════════════════╗{c.rst}")
    print(f"{c.P}║{c.rst}{c.Y}        ✨  VPN KEY GENERATOR  —  PREMIUM EDITION  v{VERSION.split()[1]}        ✨{c.rst}{c.P}║{c.rst}")
    print(f"{c.P}╠══════════════════════════════════════════════════════════════════════╣{c.rst}")
    print(f"{c.P}║{c.rst}  {c.C}📡 Status:{c.rst} Online ✅  {c.C}│{c.rst}  {c.C}⭐ Favorites:{c.rst} {len(load_favorites())}  {c.C}│{c.rst}  {c.C}⚡ Fast Scan:{c.rst} Auto-Select Best  {c.P}║{c.rst}")
    print(f"{c.P}╚══════════════════════════════════════════════════════════════════════╝{c.rst}")
    print()

def divider(title=""):
    c = Colors()
    if title:
        print(f"{c.C}─── {title} {'─' * (60 - len(title))}{c.rst}")
    else:
        print(f"{c.D}─" * 68 + c.rst)

# ==========================================
#        📋 Clipboard
# ==========================================
def copy_to_clipboard(text):
    try:
        with open("/dev/clipboard", "w") as f:
            f.write(text)
        return True
    except:
        try:
            os.system(f'echo -n "{text}" > /dev/clipboard')
            return True
        except:
            return False

# ==========================================
#        ⭐ Favorites
# ==========================================
def load_favorites():
    if not os.path.exists(FAV_FILE): return []
    try:
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except: return []

def save_favorite(name, key):
    favs = load_favorites()
    entry = f"{name}|{key}"
    if entry not in favs:
        favs.append(entry)
        with open(FAV_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(favs))
        return True
    return False

# ==========================================
#        ⚡ Ping Test
# ==========================================
def test_ping(host, port, timeout=2):
    try:
        if not host or not port: return 9999
        port = int(port)
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.close()
        ms = round((time.time() - start) * 1000)
        return ms
    except: return 9999

# ==========================================
#        📥 Fetch Data
# ==========================================
def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode())
    except: return None

def fetch_b64(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
        return base64.b64decode(r.read()).decode().splitlines()
    except: return None

def fetch_txt(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return [l.strip() for l in r.read().decode().splitlines() if l.strip() and not l.startswith("#")]
    except: return None

# ==========================================
#        🔑 Parse Key Info
# ==========================================
def parse_key_info(key):
    try:
        if key.startswith("ss://"):
            data = key.split("//")[1].split("@")
            if len(data) >= 2:
                hostport = data[1].split("#")[0].split("/")[0]
                host, port = hostport.split(":")
                name = key.split("#")[-1] if "#" in key else "Server"
                return name, host, int(port)
        elif key.startswith("vless://"):
            parts = key.split("?")[0].split("@")
            if len(parts) >= 2:
                hostport = parts[1].split("#")[0]
                if ":" in hostport:
                    host, port = hostport.split(":")
                    name = key.split("#")[-1] if "#" in key else "Server"
                    return name, host, int(port)
        return "Unknown", "", 0
    except: return "Unknown", "", 0

# ==========================================
#        🏆 AUTO BEST — One-Click Best Key
# ==========================================
def find_best_key():
    header()
    c = Colors()
    print(f"  {c.Y}🔍 အကောင်းဆုံး Server ကို ရှာဖွေနေသည်...{c.rst}")
    print(f"  {c.D}─── ဒေတာအရင်းအမြစ်များကို စစ်ဆေးနေသည်...{c.rst}")

    all_keys = []
    sources = []

    # Fetch from all APIs
    name, url, dtype = API_LIST["1"]
    data = fetch_json(url)
    if data: sources.append((name, data, dtype))

    name, url, dtype = API_LIST["2"]
    data = fetch_b64(url)
    if data: sources.append((name, data, dtype))

    name, url, dtype = API_LIST["3"]
    data = fetch_txt(url)
    if data: sources.append((name, data, dtype))

    if not sources:
        print(f"\n  {c.R}❌ ဒေတာရယူ၍မရပါ။ နောက်မှ ထပ်ကြိုးစားကြည့်ပါ။{c.rst}")
        input(f"  {c.D}Enter နှိပ်ပါ...{c.rst}")
        return

    total = 0
    for src_name, data, dtype in sources:
        if dtype == "json" and isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and "name" in item and ("server" in item or "address" in item):
                    host = item.get("server", item.get("address", ""))
                    port = int(item.get("port", 443))
                    key = item.get("url", item.get("link", ""))
                    if key:
                        ms = test_ping(host, port, timeout=1.5)
                        all_keys.append({"name": item["name"], "host": host, "port": port, "key": key, "ping": ms, "source": src_name})
                        total += 1
        elif dtype in ["b64", "txt"] and isinstance(data, list):
            for key in data:
                sname, host, port = parse_key_info(key)
                if host and port:
                    ms = test_ping(host, port, timeout=1.5)
                    all_keys.append({"name": sname, "host": host, "port": port, "key": key, "ping": ms, "source": src_name})
                    total += 1

    print(f"  {c.G}✅ Server {total} လုံးကို စစ်ဆေးပြီးပါပြီ။ အကောင်းဆုံးကို ရွေးချယ်နေသည်...{c.rst}\n")

    # Filter working & sort by ping
    working = [k for k in all_keys if k["ping"] < 9999]
    if not working:
        print(f"  {c.R}❌ အလုပ်လုပ်နိုင်သော Server မတွေ့ပါ။{c.rst}")
        input(f"  {c.D}Enter နှိပ်ပါ...{c.rst}")
        return

    working.sort(key=lambda x: x["ping"])
    best = working[0]

    divider("🏆 အကောင်းဆုံး Server")
    print(f"  {c.G}📍 နာမည်:{c.rst}     {c.W}{best['name']}{c.rst}")
    print(f"  {c.G}🌐 လိပ်စာ:{c.rst}    {best['host']}:{best['port']}")
    print(f"  {c.G}⚡ Ping:{c.rst}       {c.G if best['ping']<150 else c.Y}{best['ping']} ms{c.rst}")
    print(f"  {c.C}📌 အရင်းအမြစ်:{c.rst}  {best['source']}")
    divider()
    print(f"  {c.Y}🔑 Key:{c.rst}")
    print(f"  {c.W}{best['key']}{c.rst}")
    divider()

    while True:
        print(f"  {c.C}[C]{c.rst} ကူးယူရန်   {c.C}[F]{c.rst} အကြိုက်ဆုံးသိမ်းရန်   {c.C}[B]{c.rst} နောက်ထပ်အကောင်းဆုံးကိုကြည့်ရန်   {c.C}[Q]{c.rst} မီနူးသို့ပြန်ရန်")
        sel = input(f"  {c.P}▶ ရွေးချယ်ပါ : {c.rst}").strip().upper()
        if sel == "C":
            if copy_to_clipboard(best["key"]):
                print(f"  {c.G}✅ ကလစ်ဘုတ်သို့ ကူးယူပြီးပါပြီ!{c.rst}\n")
            else:
                print(f"  {c.R}⚠️ ကူးယူ၍မရပါ၊ ကိုယ်တိုင်ကူးယူပါ။{c.rst}\n")
        elif sel == "F":
            if save_favorite(best["name"], best["key"]):
                print(f"  {c.G}✅ အကြိုက်ဆုံးထဲ သိမ်းဆည်းပြီးပါပြီ!{c.rst}\n")
            else:
                print(f"  {c.Y}⚠️ ရှိပြီးသားဖြစ်နေပါသည်။{c.rst}\n")
        elif sel == "B":
            idx = working.index(best) + 1
            if idx < len(working):
                best = working[idx]
                header()
                print(f"  {c.Y}🏆 နောက်ထပ်အကောင်းဆုံး #{idx+1}{c.rst}\n")
                divider("🏆 Server Info")
                print(f"  {c.G}📍 နာမည်:{c.rst}     {c.W}{best['name']}{c.rst}")
                print(f"  {c.G}🌐 လိပ်စာ:{c.rst}    {best['host']}:{best['port']}")
                print(f"  {c.G}⚡ Ping:{c.rst}       {c.G if best['ping']<150 else c.Y}{best['ping']} ms{c.rst}")
                print(f"  {c.C}📌 အရင်းအမြစ်:{c.rst}  {best['source']}")
                divider()
                print(f"  {c.Y}🔑 Key:{c.rst}")
                print(f"  {c.W}{best['key']}{c.rst}")
                divider()
            else:
                print(f"  {c.Y}⚠️ နောက်ထပ် Server မရှိတော့ပါ။{c.rst}\n")
        elif sel == "Q":
            break

# ==========================================
#        ⭐ Favorites Menu
# ==========================================
def favorites_menu():
    while True:
        header()
        favs = load_favorites()
        print(f"  {c.Y}⭐ အကြိုက်ဆုံးများ{c.rst}")
        divider()
        if not favs:
            print(f"  {c.D}အကြိုက်ဆုံးမရှိသေးပါ။ Server များထဲမှာ [F] နှိပ်ပြီး သိမ်းဆည်းပါ။{c.rst}")
        else:
            for i, entry in enumerate(favs, 1):
                if "|" in entry:
                    name, key = entry.split("|", 1)
                    print(f"  {c.C}[{i}]{c.rst} {name}")
                    short_key = key[:45] + "..." if len(key) > 45 else key
                    print(f"      {c.D}{short_key}{c.rst}")
                    print()
        divider()
        print(f"  {c.C}[C]{c.rst} မီနူးသို့ပြန်ရန်   {c.C}[A]{c.rst} အားလုံးဖျက်ရန်")
        sel = input(f"  {c.P}▶ ရွေးချယ်ပါ : {c.rst}").strip().upper()
        if sel == "C": break
        elif sel == "A":
            if input(f"  {c.R}⚠️ အားလုံးဖျက်မှာလား? (y/n): {c.rst}").lower() == "y":
                os.remove(FAV_FILE)
                print(f"  {c.G}✅ အားလုံးဖျက်ပြီးပါပြီ။{c.rst}")

# ==========================================
#        📂 Main Menu
# ==========================================
def main_menu():
    while True:
        header()
        print(f"  {c.Y}📂 ပင်မမီနူး{c.rst}")
        divider()
        print(f"  {c.G}⭐ [0]  အကောင်းဆုံး Key ကို တခါထဲရှာမည်  —  အကြံပြု{c.rst}")
        print()
        print(f"  {c.C}[1]{c.rst} Shadowmere JSON API")
        print(f"  {c.C}[2]{c.rst} Shadowmere Base64 API")
        print(f"  {c.C}[3]{c.rst} VLESS Config List")
        print(f"  {c.C}[4]{c.rst} ⭐ အကြိုက်ဆုံးများ")
        print()
        print(f"  {c.R}[9]{c.rst} ပရိုဂရမ်မှ ထွက်မည်")
        divider()
        choice = input(f"  {c.P}▶ ရွေးချယ်ပါ : {c.rst}").strip()

        if choice == "0":
            find_best_key()
        elif choice == "9":
            clear()
            print(f"\n  {c.C}👋 ကျေးဇူးပြု၍ ပြန်လာပါ။{c.rst}\n")
            sys.exit(0)
        elif choice == "4":
            favorites_menu()
        elif choice in API_LIST:
            name, url, dtype = API_LIST[choice]
            header()
            print(f"  {c.Y}📥 {name} မှ ဒေတာရယူနေသည်...{c.rst}")
            data = None
            if dtype == "json": data = fetch_json(url)
            elif dtype == "b64": data = fetch_b64(url)
            elif dtype == "txt": data = fetch_txt(url)
            if not data:
                print(f"  {c.R}❌ ဒေတာရယူ၍မရပါ။{c.rst}")
                input(f"  {c.D}Enter နှိပ်ပါ...{c.rst}")
                continue
            # Display list
            header()
            print(f"  {c.Y}📋 {name} — ရလဒ်များ{c.rst}")
            divider()
            items = []
            if dtype == "json" and isinstance(data, list):
                items = data
            elif dtype in ["b64", "txt"] and isinstance(data, list):
                for k in data:
                    n, h, p = parse_key_info(k)
                    items.append({"name": n, "server": h, "port": p, "url": k})
            for idx, item in enumerate(items, 1):
                print(f"  {c.C}[{idx}]{c.rst} {item.get('name', 'Server')}")
            divider()
            sel = input(f"  {c.P}▶ နံပါတ်ရွေးပါ သို့မဟုတ် [Q] ပြန်ရန် : {c.rst}").strip().upper()
            if sel == "Q": continue
            try:
                idx = int(sel) - 1
                if 0 <= idx < len(items):
                    item = items[idx]
                    key = item.get("url", item.get("link", ""))
                    header()
                    divider(f"Server #{idx+1}")
                    print(f"  {c.G}📍 နာမည်:{c.rst} {item.get('name','')}")
                    print(f"  {c.G}🔑 Key:{c.rst}")
                    print(f"  {c.W}{key}{c.rst}")
                    divider()
                    while True:
                        print(f"  {c.C}[C]{c.rst} ကူးယူ  {c.C}[F]{c.rst} သိမ်း  {c.C}[Q]{c.rst} ပြန်")
                        act = input(f"  {c.P}▶ : {c.rst}").strip().upper()
                        if act == "C":
                            if copy_to_clipboard(key): print(f"  {c.G}✅ ကူးယူပြီး!{c.rst}")
                            else: print(f"  {c.R}⚠️ ကူးယူ၍မရပါ{c.rst}")
                        elif act == "F":
                            if save_favorite(item.get("name","Server"), key): print(f"  {c.G}✅ သိမ်းပြီး!{c.rst}")
                        elif act == "Q": break
            except: pass

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        clear()
        print(f"\n\n  {c.C}👋 ပရိုဂရမ်မှ ထွက်လိုက်ပါပြီ။{c.rst}\n")
        sys.exit(0)
    
