#!/usr/bin/env python3
import urllib.request, urllib.error, json, base64, os, sys, socket, time

os.environ["TERM"] = "xterm-256color"

VERSION = "3.5 ✨"
FAV_FILE = os.path.expanduser("~/.vpn_favorites.txt")

API_LIST = {
    "1": ("Shadowmere JSON", "https://shadowmere.xyz/api/sub/", "json"),
    "2": ("Shadowmere Base64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    "3": ("VLESS List", "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/vless.txt", "txt")
}

def clear(): os.system("clear")

# ==========================================
#        📋 ကလစ်ဘုတ် ကူးယူခြင်း
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
#        ⭐ အကြိုက်ဆုံးများ စနစ်
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
#        ⚡ Ping စစ်ဆေးခြင်း
# ==========================================
def test_ping(host, port, timeout=2):
    try:
        if not host or not port: return 9999, "⚠️ စမ်းသပ်၍မရ"
        port = int(port)
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        ms = round((time.time() - start) * 1000)
        if result == 0:
            if ms < 100: return ms, "🟢 အလွန်ကောင်း {}ms".format(ms)
            elif ms < 200: return ms, "🟡 ကောင်းသည် {}ms".format(ms)
            else: return ms, "🔴 နှေးသည် {}ms".format(ms)
        return 9999, "❌ မရနိုင်ပါ"
    except: return 9999, "⚠️ စမ်းသပ်၍မရ"

# ==========================================
#        📥 ဒေတာ ရယူခြင်း
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
            return base64.b64decode(r.read().decode()).splitlines()
    except: return None

def fetch_txt(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            content = r.read().decode().strip()
            try: return [l.strip() for l in base64.b64decode(content).decode('utf-8').splitlines() if l.strip() and not l.startswith('#')]
            except: return [l.strip() for l in content.splitlines() if l.strip() and not l.startswith('#')]
    except: return None

# ==========================================
#        🔑 Key ဖန်တီးခြင်း
# ==========================================
def make_ss_key(s):
    try:
        host = s.get("serverAddress", s.get("server", ""))
        port = s.get("serverPort", s.get("port", s.get("server_port", "")))
        method = s.get("method", "")
        password = s.get("password", "")
        info = "{}:{}".format(method, password)
        b64 = base64.b64encode(info.encode()).decode().rstrip("=")
        name = s.get("remarks", s.get("name", "Server"))
        return "ss://{}@{}#{}".format(b64, host+":"+str(port), name)
    except: return "❌ အမှား"

def extract_host_port(link):
    try:
        if link.startswith("ss://"):
            part = link.split("//")[1].split("@")[1].split("#")[0]
            h, p = part.split(":")
            return h, int(p)
        elif "://" in link:
            after = link.split("//")[1]
            if "@" in after: after = after.split("@")[1]
            if ":" in after and "?" in after:
                h = after.split(":")[0]
                p = after.split(":")[1].split("?")[0]
                return h, int(p)
            elif ":" in after:
                hp = after.split("/")[0]
                if ":" in hp:
                    h, p = hp.split(":")
                    return h, int(p)
                return hp, 443
            else: return after.split("/")[0], 443
    except: return None, None
    return None, None

# ==========================================
#        ⏳ Loading
# ==========================================
def loading(text="ဒေတာရယူနေသည်"):
    print("\n  ⏳ {}".format(text), end="", flush=True)
    for _ in range(4):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print(" ✅")

# ==========================================
#        🎦 Header
# ==========================================
def header():
    clear()
    p, c, y, rst = "\033[95m", "\033[96m", "\033[93m", "\033[0m"
    print("{}╔════════════════════════════════════════════════════════════════╗{}".format(p, rst))
    print("{}║{}    ✨ {}V P N   K E Y   G E N E R A T O R{}  v{} ✨        {}║{}".format(p, rst, c, rst, VERSION, p, rst))
    print("{}║{}     ⭐ အကြိုက်ဆုံးများ  📋 ကူးယူခြင်း  ⚡ အမြန်ဆုံးရွေးချယ်  🔍 စစ်ဆေးမှု   {}║{}".format(p, rst, p, rst))
    print("{}╚════════════════════════════════════════════════════════════════╝{}".format(p, rst))
    print("{}┌────────────────────────────────────────────────────────────────────┐{}".format(c, rst))
    print("{}│{}  📡 Status: Online ✅     ⭐ Favorites: {} လုံး     ⚡ Ping Test: အသင့်တော်ဆုံး{}│{}".format(c, rst, len(load_favorites()), c, rst))
    print("{}└────────────────────────────────────────────────────────────────────┘{}".format(c, rst))
    print("{}{}{}".format(y, "─" * 68, rst))
    print()

# ==========================================
#        ⭐ အကြိုက်ဆုံးများ မီနူး
# ==========================================
def favorites_menu():
    while True:
        header()
        favs = load_favorites()
        print("  ⭐ အကြိုက်ဆုံး Server များ")
        print("  ──────────────────────────────────────────────────")
        if not favs:
            print("  😔 အကြိုက်ဆုံးမရှိသေးပါ။ Server မီနူးမှာ F နှိပ်ပြီး သိမ်းဆည်းပါ")
        else:
            for i, entry in enumerate(favs, 1):
                if "|" in entry:
                    name, key = entry.split("|", 1)
                    print("  [{}] ⭐ {}".format(i, name))
                    print("      🔑 {}...".format(key[:55]))
                    print()
        print("  ──────────────────────────────────────────────────")
        print("  [C] မီနူးသို့ပြန်ရန်    [A] အားလုံးဖျက်မည်")
        ch = input("  ▸ ရွေးချယ်မှု : ").strip().lower()
        if ch == "c": return
        elif ch == "a":
            if input("  အားလုံးဖျက်မှာလား? (y/n): ").lower() == "y":
                os.remove(FAV_FILE)
                print("  ✅ ဖျက်ပြီးပါပြီ")

# ==========================================
#        ⚡ အမြန်ဆုံး ရှာဖွေခြင်း
# ==========================================
def show_fastest(data, api_type):
    header()
    print("  ⚡ အမြန်ဆုံး Server ကို ရှာဖွေနေသည်...")
    best_ms, best_name, best_key = 9999, None, None
    items = data[:10] if len(data) > 10 else data

    for idx, item in enumerate(items, 1):
        if api_type == "json":
            host = item.get("serverAddress", item.get("server", ""))
            port = item.get("serverPort", item.get("port", item.get("server_port", "")))
            name = item.get("remarks", item.get("name", "Server {}".format(idx)))
            key = make_ss_key(item)
        else:
            key = item
            host, port = extract_host_port(item)
            name = "Server {}".format(idx)
        ms, _ = test_ping(host, port, timeout=1.5)
        if ms < best_ms and ms < 9999:
            best_ms, best_name, best_key = ms, name, key

    clear()
    print("\033[95m╔══════════════════════════════════════════════════════════╗\033[0m")
    if best_name:
        print("\033[96m  🏆 အမြန်ဆုံး Server: {}  •  {}ms\033[0m".format(best_name, best_ms))
        print("\033[95m╚══════════════════════════════════════════════════════════╝\033[0m")
        print("\n  📍 {}".format(best_name))
        print("  ⚡ 🟢 အလွန်ကောင်း {}ms".format(best_ms))
        print("  🔑 {}".format(best_key))
        if copy_to_clipboard(best_key):
            print("  ✅ ကလစ်ဘုတ်ကူးယူပြီးပါပြီ!")
        if save_favorite(best_name, best_key):
            print("  ⭐ အကြိုက်ဆုံးထဲ သိမ်းဆည်းပြီးပါပြီ!")
    else:
        print("\033[91m  ❌ အမြန်ဆုံးမတွေ့ပါ\033[0m")
    input("\n  Enter နှိပ်ပါ...")

# ==========================================
#        📋 ရလဒ်များ ပြသခြင်း
# ==========================================
def show_results(results, api_type):
    clear()
    print("\033[95m╔══════════════════════════════════════════════════════════╗\033[0m")
    print("\033[96m  📌 စုစုပေါင်း {} လုံး\033[0m".format(len(results)))
    print("\033[95m╚══════════════════════════════════════════════════════════╝\033[0m")

    for idx, item in enumerate(results, 1):
        if api_type == "json":
            host = item.get("serverAddress", item.get("server", ""))
            port = item.get("serverPort", item.get("port", item.get("server_port", "")))
            name = item.get("remarks", item.get("name", "Server {}".format(idx)))
            key = make_ss_key(item)
        else:
            key = item
            host, port = extract_host_port(item)
            name = "Server {}".format(idx)

        ms, status = test_ping(host, port)
        print("\n  ┌─────────────────────────────────────────────┐")
        print("  │ [{}] 📍 {}".format(idx, name))
        print("  │ ⚡ {}".format(status))
        print("  ├─────────────────────────────────────────────┤")
        print("  │ 🔑 {}".format(key))
        print("  └─────────────────────────────────────────────┘")
        print("  │  [C] ကူးယူ  [F] အကြိုက်ဆုံးသိမ်း  [N] နောက်တစ်ခု  [Q] ပြန်")

        ch = input("  ▸ ရွေးချယ်မှု : ").strip().lower()
        if ch == "c":
            if copy_to_clipboard(key): print("  ✅ ကူးယူပြီးပါပြီ!")
            else: print("  ⚠️ ကူးယူ၍မရပါ၊ ကိုယ်တိုင်ကူးပါ")
        elif ch == "f":
            if save_favorite(name, key): print("  ⭐ သိမ်းဆည်းပြီးပါပြီ!")
            else: print("  ⚠️ ရှိပြီးသားဖြစ်နေပါသည်")
        elif ch == "q":
            return

# ==========================================
#        🌍 နိုင်ငံ ရွေးချယ်ခြင်း
# ==========================================
def country_menu(data, api_type):
    while True:
        header()
        print("  🌍 နိုင်ငံ/ဒေသ ရွေးချယ်ပါ")
        print("  ──────────────────────────────────────────────────")
        print("  [1] 🌏 အားလုံး      [A] ⚡ အမြန်ဆုံးရွေးမည်")
        print("  [2] 🇺🇸 US   [3] 🇸🇬 SG   [4] 🇭🇰 HK")
        print("  [5] 🇯🇵 JP   [6] 🇰🇷 KR   [7] 🇿🇦 ZA")
        print("  ──────────────────────────────────────────────────")
        print("  [8] 🔙 မီနူးပြန်    [0] ❌ ထွက်")
        ch = input("  ▸ ရွေးချယ်မှု : ").strip().lower()

        if ch == "0":
            clear()
            print("\n  👋 ကျေးဇူးတင်ပါတယ်!\n")
            sys.exit(0)
        if ch == "8": return
        if ch == "a":
            show_fastest(data, api_type)
            continue
        if not data:
            input("\n  ❌ ဒေတာမရှိပါ။ Enter...")
            continue

        filters = {
            "1": "", "2": "us", "3": "sg singapore", "4": "hk hong kong",
            "5": "jp japan", "6": "kr korea", "7": "za south africa"
        }
        if ch not in filters: continue
        kw = filters[ch]
        results = []
        if api_type == "json":
            for s in data:
                rmk = str(s.get("remarks", s.get("name", ""))).lower()
                if not kw or any(k in rmk for k in kw.split()):
                    results.append(s)
        else:
            results = data if not kw else [l for l in data if any(k in l.lower() for k in kw.split())]
        show_results(results, api_type)

# ==========================================
#        📂 ပင်မ မီနူး
# ==========================================
def main_menu():
    while True:
        header()
        print("  📂 အရင်းအမြစ် ရွေးချယ်ပါ")
        print("  ──────────────────────────────────────────────────")
        for k, v in API_LIST.items():
            print("  [{}] {}".format(k, v[0]))
        print("  [4] ⭐ အကြိုက်ဆုံးများ")
        print("  ──────────────────────────────────────────────────")
        print("  [0] ❌ ပရိုဂရမ်မှ ထွက်ရန်")
        ch = input("  ▸ ရွေးချယ်မှု : ").strip()

        if ch == "0":
            clear()
            print("\n  👋 အသုံးပြုမှုအတွက် ကျေးဇူးတင်ပါတယ်!\n")
            sys.exit(0)
        if ch == "4":
            favorites_menu()
            continue
        if ch not in API_LIST: continue

        name, url, dtype = API_LIST[ch]
        header()
        loading("{} မှ ဒေတာရယူနေသည်".format(name))

        data = None
        if dtype == "json": data = fetch_json(url)
        elif dtype == "b64": data = fetch_b64(url)
        elif dtype == "txt": data = fetch_txt(url)

        if not data:
            input("\n  ❌ ဒေတာရယူ၍မရပါ။ Enter နှိပ်ပါ...")
            continue
        country_menu(data, dtype)

# ==========================================
#        🚀 ပရိုဂရမ် စတင်ခြင်း
# ==========================================
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        clear()
        print("\n\n  👋 ပရိုဂရမ်မှ ထွက်လိုက်ပါပြီ။\n")
        sys.exit(0)
            
