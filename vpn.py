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

def copy_to_clipboard(text):
    try:
        if os.name == "posix":
            with os.popen("xclip -selection clipboard", "w") as p:
                p.write(text)
        return True
    except:
        return False

def load_favorites():
    if not os.path.exists(FAV_FILE):
        return []
    try:
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def save_favorite(name, key):
    favs = load_favorites()
    entry = f"{name}|{key}"
    if entry not in favs:
        favs.append(entry)
        with open(FAV_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(favs))
        return True
    return False

def remove_favorite(name):
    favs = load_favorites()
    new_favs = [f for f in favs if not f.startswith(f"{name}|")]
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(new_favs))

def test_ping(host, port, timeout=2):
    try:
        if not host or not port:
            return 9999, "⚠️ စမ်းသပ်၍မရ"
        port = int(port)
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        ms = round((time.time() - start) * 1000)
        if result == 0:
            if ms < 100:
                return ms, f"🟢 အလွန်ကောင်း  {ms}ms"
            elif ms < 200:
                return ms, f"🟡 ကောင်းသည်   {ms}ms"
            else:
                return ms, f"🔴 နှေးသည်   {ms}ms"
        else:
            return 9999, "❌ မရနိုင်ပါ"
    except Exception:
        return 9999, "⚠️ စမ်းသပ်၍မရ"

def fetch_json(url):
    try:
        r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(r, timeout=15) as res:
            return json.loads(res.read().decode())
    except Exception:
        return None

def fetch_b64(url):
    try:
        r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(r, timeout=15) as res:
            data = res.read().decode().strip()
            return base64.b64decode(data).decode().splitlines()
    except Exception:
        return None

def fetch_txt(url):
    try:
        r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(r, timeout=15) as res:
            content = res.read().decode().strip()
            try:
                decoded = base64.b64decode(content).decode('utf-8')
                return [line.strip() for line in decoded.splitlines() if line.strip() and not line.startswith('#')]
            except:
                return [line.strip() for line in content.splitlines() if line.strip() and not line.startswith('#')]
    except Exception:
        return None

def make_ss_key(s):
    try:
        host = s.get("serverAddress", s.get("server", ""))
        port = s.get("serverPort", s.get("port", s.get("server_port", "")))
        method = s.get("method", "")
        password = s.get("password", "")
        info = f"{method}:{password}"
        b64 = base64.b64encode(info.encode()).decode().rstrip("=")
        remarks = s.get("remarks", s.get("name", "Server"))
        return f"ss://{b64}@{host}:{port}#{remarks}"
    except Exception as e:
        return f"❌ အမှား"

def extract_host_port(link):
    try:
        if link.startswith("ss://"):
            part = link.split("@")[1].split("#")[0]
            host, port = part.split(":")
            return host, int(port)
        elif "://" in link:
            after = link.split("//")[1]
            if "@" in after:
                after = after.split("@")[1]
            if ":" in after and "?" in after:
                host = after.split(":")[0]
                port = after.split(":")[1].split("?")[0]
                return host, int(port)
            elif ":" in after:
                host_part = after.split("/")[0]
                if ":" in host_part:
                    host, port = host_part.split(":")
                    return host, int(port)
                return host_part, 443
            else:
                return after.split("/")[0], 443
    except:
        return None, None
    return None, None

def loading(text="ဒေတာရယူနေသည်"):
    print(f"\n  ⏳ {text}", end="", flush=True)
    for _ in range(4):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print(" ✅")

def header():
    clear()
    p = "\033[95m"
    c = "\033[96m"
    y = "\033[93m"
    rst = "\033[0m"
    print(f"{p}╔══════════════════════════════════════════════════════════════════╗{rst}")
    print(f"{p}║{rst}    ✨ {c}V P N   K E Y   G E N E R A T O R{rst}  v{VERSION} ✨        {p}║{rst}")
    print(f"{p}║{rst}     ⭐ အကြိုက်ဆုံးများ  📋 ကူးယူခြင်း  ⚡ အမြန်ဆုံးရွေးချယ်  🔍 စစ်ဆေးမှု   {p}║{rst}")
    print(f"{p}╚══════════════════════════════════════════════════════════════════╝{rst}")
    print(f"{c}┌────────────────────────────────────────────────────────────────────┐{rst}")
    print(f"{c}│{rst}  📡 Status: Online ✅     ⭐ Favorites: {len(load_favorites())} လုံး     ⚡ Ping Test: အသင့်တော်ဆုံး{c}│{rst}")
    print(f"{c}└────────────────────────────────────────────────────────────────────┘{rst}")
    print(f"{y}{'─' * 68}{rst}")
    print()

def favorites_menu():
    while True:
        header()
        favs = load_favorites()
        print("  ⭐ အကြိုက်ဆုံး Server များ")
        print("  " + "─" * 50)
        if not favs:
            print("  😔 အကြိုက်ဆုံးမရှိသေးပါ။ Server မီနူးမှာ F နှိပ်ပြီး သိမ်းဆည်းပါ")
        else:
            for i, entry in enumerate(favs, 1):
                if "|" in entry:
                    name, key = entry.split("|", 1)
                    print(f"  [{i}] ⭐ {name}")
                    print(f"      🔑 {key[:50]}...")
                    print()
        print("  ╭────────────────────────────────────────────────────╮")
        print("  │  [C] မီနူးသို့ပြန်ရန်   [R] အားလုံးဖျက်မည်         │")
        print("  ╰────────────────────────────────────────────────────╯")
        ch = input("  ▸ ရွေးချယ်မှု : ").strip().lower()
        if ch == "c":
            return
        elif ch == "r":
            if input("  အားလုံးဖျက်မှာလား? (y/n): ").lower() == "y":
                os.remove(FAV_FILE)
                print("  ✅ ဖျက်ပြီးပါပြီ")
        elif ch.isdigit():
            idx = int(ch) - 1
            if 0 <= idx < len(favs):
                name, key = favs[idx].split("|", 1)
                print(f"\n  📍 {name}")
                print(f"  🔑 {key}")
                copy_to_clipboard(key)
                print("  ✅ ကလစ်ဘုတ်ကူးယူပြီးပါပြီ!")
                input("  Enter နှိပ်ပါ...")

def api_menu():
    while True:
        header()
        print("  📂 အရင်းအမြစ် ရွေးချယ်ပါ")
        print("  " + "─" * 50)
        print("  ╭────────────────────────────────────────────────────╮")
        print("  │   [1] 🌐 Shadowmere JSON API                        │")
        print("  │   [2] 🔐 Shadowmere Base64 API                      │")
        print("  │   [3] 📋 VLESS Config List                          │")
        print("  │   [4] ⭐ အကြိုက်ဆုံးများ                              │")
        print("  ╰────────────────────────────────────────────────────╯")
        print("  │   [0] ❌ ပရိုဂရမ်မှ ထွက်ရန်                           │")
        print("  ╰────────────────────────────────────────────────────╯")
        print()
        ch = input("  ▸ ရွေးချယ်မှု : ").strip()
        if ch == "0":
            clear()
            print("\n  👋 အသုံးပြုမှုအတွက် ကျေးဇူးတင်ပါတယ်!\n")
            sys.exit(0)
        elif ch == "4":
            favorites_menu()
        elif ch in API_LIST:
            return API_LIST[ch]

def country_menu(data, api_type):
    while True:
        header()
        print("  🌍 နိုင်ငံ/ဒေသ ရွေးချယ်ပါ")
        print("  " + "─" * 50)
        print("  ╭────────────────────────────────────────────────────╮")
        print("  │   [1] 🌏 အားလုံး          [A] ⚡ အမြန်ဆုံးရွေးမည်     │")
        print("  │   [2] 🇺🇸 US  [3] 🇸🇬 SG  [4] 🇭🇰 HK               │")
        print("  │   [5] 🇯🇵 JP  [6] 🇰🇷 KR  [7] 🇿🇦 ZA               │")
        print("  ╰────────────────────────────────────────────────────╯")
        print("  │   [8] 🔙 မီနူးပြန်  [0] ❌ ထွက်                    │")
        print("  ╰────────────────────────────────────────────────────╯")
        print()
        ch = input("  ▸ ရွေးချယ်မှု : ").strip().lower()
        if ch == "0":
            clear()
            print("\n  👋 ကျေးဇူးတင်ပါတယ်!\n")
            sys.exit(0)
        if ch == "8":
            return
        if ch == "a":
            show_fastest(data, api_type)
            continue
        if not data:
            input("\n  ❌ ဒေတာမရှိပါ။ Enter...")
            continue
        filters = {"1": "", "2": "us", "3": "sg singapore", "4": "hk hong", "5": "jp japan", "6": "kr korea", "7": "za south africa"}
        if ch not in filters:
            continue
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

def show_fastest(data, api_type):
    header()
    print("  ⚡ အမြန်ဆုံး Server ကို ရှာဖွေနေသည်...")
    best_ms = 9999
    best_item = None
    best_key = None
    best_name = None
    items = data[:10] if len(data) > 10 else data
    for idx, item in enumerate(items, 1):
        if api_type == "json":
            host = item.get("serverAddress", item.get("server", ""))
            port = item.get("serverPort", item.get("port", item.get("server_port", "")))
            name = item.get("remarks", item.get("name", f"Server {idx}"))
            key = make_ss_key(item)
        else:
            key = item
            host, port = extract_host_port(item)
            name = f"Server {idx}"
        ms, _ = test_ping(host, port, timeout=1.5)
        if ms < best_ms and ms < 9999:
            best_ms = ms
            best_item = item
            best_key = key
            best_name = name
    clear()
    print("\033[95m╔══════════════════════════════════════════════════════════╗\033[0m")
    if best_item:
        print(f"\033[96m  🏆 အမြန်ဆုံး Server : {best_name}  •  {best_ms}ms\033[0m")
        print("\033[95m╚══════════════════════════════════════════════════════════╝\033[0m")
        print(f"\n  📍 {best_name}")
        print(f"  ⚡ 🟢 အလွန်ကောင်း  {best_ms}ms")
        print(f"  🔑 {best_key}")
        copy_to_clipboard(best_key)
        print("\n  ✅ အလိုအလျောက် ကူးယူပြီးပါပြီ!")
        if save_favorite(best_name, best_key):
            print("  ⭐ အကြိုက်ဆုံးထဲ သိမ်းဆည်းပြီးပါပြီ!")
    else:
        print("\033[91m  ❌ အမြန်ဆုံးမတွေ့ပါ\033[0m")
    input("\n  မီနူးသို့ပြန်ရန် Enter...")

def show_results(results, api_type):
    clear()
    print("\033[95m╔══════════════════════════════════════════════════════════╗\033[0m")
    print(f"\033[96m  📌 စုစုပေါင်း {len(results)} လုံး\033[0m")
    print("\033[95m╚══════════════════════════════════════════════════════════╝\033[0m")
    for idx, item in enumerate(results, 1):
        if api_type == "json":
            host = item.get("serverAddress", item.get("server", ""))
            port = item.get("serverPort", item.get("port", item.get("server_port", "")))
            name = item.get("remarks", item.get("name", f"Server {idx}"))
            key = make_ss_key(item)
        else:
            key = item
            host, port = extract_host_port(item)
            name = f"Server {idx}"
        ms, status = test_ping(host, port)
        print(f"\n  ┌─────────────────────────────────────────────┐")
        print(f"  │ [{idx}] 📍 {name}")
        print(f"  │ ⚡ {status}")
        print(f"  ├─────────────────────────────────────────────┤")
        print(f"  │ 🔑 {key}")
        print(f"  └─────────────────────────────────────────────┘")
        print("  │  [C] ကူးယူ  [F] အကြိုက်ဆုံးသိမ်း  [N] နောက်တစ်ခု")
        ch = input("  ▸ ရွေးချယ်မှု : ").strip().lower()
        if ch == "c":
            if copy_to_clipboard(key):
                print("  ✅ ကူးယူပြီးပါပြီ!")
            else:
                print("  ⚠️ ကူးယူ၍မရပါ၊ ကိုယ်တိုင်ကူးပါ")
        elif ch == "f":
            if save_favorite(name, key):
                print("  ⭐ သိမ်းဆည်းပြီးပါပြီ!")
            else:
                print("  ⚠️ ရှိပြီးသားဖြစ်နေပါသည်")
    input("\n  မီနူးသို့ပြန်ရန် Enter...")

def main():
    while True:
        name, url, dtype = api_menu()
        header()
        loading("ဒေတာရယူနေသည်")
        data = None
        if dtype == "json":
            data = fetch_json(url)
        elif dtype == "b64":
            data = fetch_b64(url)
        elif dtype == "txt":
            data = fetch_txt(url)
        if not data:
            input("\n  ❌ ဒေတာရယူ၍မရပါ။ Enter...")
            continue
        while True:
            country_menu(data, dtype)
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("\n\n  👋 ပရိုဂရမ်မှ ထွက်လိုက်ပါပြီ။\n")
        sys.exit(0)
                
