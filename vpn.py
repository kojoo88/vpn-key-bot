#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════╗
# ║      🚀 Ultimate VPN Key Finder — Dream Edition ✨        ║
# ║   + Speed Test + Auto Network Detection                   ║
# ╚══════════════════════════════════════════════════════════╝
import urllib.request, base64, os, socket, time, datetime, json

# 🎨 Colors
BLU = "\033[94m"
CYN = "\033[96m"
GRN = "\033[92m"
YEL = "\033[93m"
RED = "\033[91m"
MAG = "\033[95m"
BLD = "\033[1m"
RST = "\033[0m"

# 📁 Files
SAVE_VLESS = "best_vless.txt"
SAVE_SS = "best_ss.txt"
FAV_FILE = "favorites.json"

# 🌍 Countries
COUNTRIES = {
    "1": ("🇯🇵 Japan", ["JP", "Japan", "Tokyo"]),
    "2": ("🇰🇷 Korea", ["KR", "Korea", "Seoul"]),
    "3": ("🇸🇬 Singapore", ["SG", "Singapore", "Sin"]),
    "4": ("🇭🇰 Hong Kong", ["HK", "HongKong", "Hong"]),
    "5": ("🇺🇸 USA", ["US", "USA", "United States"]),
    "6": ("🇹🇭 Thailand", ["TH", "Thailand", "Bangkok"]),
    "7": ("🇲🇲 Best for MM", ["SG", "HK", "JP", "KR"]),
    "8": ("🌐 All Countries", []),
}

network_type = "📡 Unknown"

def clear(): os.system("clear")
def line(n=58): return "═" * n

def header(title=""):
    clear()
    print(f"{CYN}{BLD}╔{line()}╗{RST}")
    print(f"{CYN}{BLD}║{RST}  🚀 {MAG}{BLD}VPN Key Finder — Dream Edition{RST}", end="")
    print(f"{' '*(20-len(title))}{CYN}{BLD}║{RST}")
    if title:
        print(f"{CYN}{BLD}║{RST}  {title}{' '*(56-len(title))}{CYN}{BLD}║{RST}")
    print(f"{CYN}{BLD}╠{line()}╣{RST}")

def footer():
    print(f"{CYN}{BLD}╚{line()}╝{RST}")

# 📱 Auto Detect Network Type
def detect_network():
    global network_type
    try:
        import subprocess
        result = subprocess.run(['ip', 'route'], capture_output=True, text=True, timeout=3)
        stdout = result.stdout.lower()
        if 'wlan' in stdout or 'wlp' in stdout:
            network_type = "📶 WiFi"
        else:
            network_type = "📱 Mobile Data"
    except:
        network_type = "📡 Unknown"
    return network_type

# ⚡ Ping + Speed Test
def test_server(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.8)
        start = time.time()
        s.connect((host, int(port)))
        ms = int((time.time() - start) * 1000)
        
        # Simple speed test: send & receive small data
        try:
            s.send(b"ping")
            s.settimeout(0.5)
            t1 = time.time()
            s.recv(1024)
            t2 = time.time()
            latency = (t2 - t1) * 1000
            if latency < 20:
                speed_level = "🚀 Fast"
                speed_score = 5
            elif latency < 50:
                speed_level = "⚡ Good"
                speed_score = 4
            elif latency < 100:
                speed_level = "📶 Normal"
                speed_score = 3
            elif latency < 200:
                speed_level = "🐢 Slow"
                speed_score = 2
            else:
                speed_level = "⚠️ Very Slow"
                speed_score = 1
        except:
            speed_level = "⚡ Checked"
            speed_score = 3
            
        s.close()
        
        # Ping rating
        if ms < 80:
            ping_str = f"{GRN}✨ {ms}ms{RST}"
            score = 5
        elif ms < 150:
            ping_str = f"{GRN}✅ {ms}ms{RST}"
            score = 4
        elif ms < 250:
            ping_str = f"{YEL}⚡ {ms}ms{RST}"
            score = 3
        elif ms < 400:
            ping_str = f"{YEL}⚠️ {ms}ms{RST}"
            score = 2
        else:
            ping_str = f"{RED}❌ {ms}ms{RST}"
            score = 1
            
        stars = "⭐" * score
        return ping_str, ms, score, stars, speed_level, speed_score
    except:
        return None, 9999, 0, "", "", 0

def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", errors="ignore")
    except:
        return None

def extract_name(line):
    if "#" not in line: return "Server"
    try:
        from urllib.parse import unquote
        return unquote(line.split("#")[-1])[:40].strip()
    except:
        return line.split("#")[-1][:40].strip() or "Server"

def parse_configs(text, fmt):
    keys = []
    if not text: return keys
    try:
        if fmt == "b64":
            text = base64.b64decode(text).decode("utf-8", errors="ignore")
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"): continue
            name = extract_name(line)
            if line.startswith("vless://"):
                keys.append({"proto": "VLESS", "name": name, "key": line, "ping": "--", "ms": 9999, "score": 0, "speed": "--"})
            elif line.startswith("ss://"):
                keys.append({"proto": "SS", "name": name, "key": line, "ping": "--", "ms": 9999, "score": 0, "speed": "--"})
    except: pass
    return keys

def save_results(proto, results):
    fname = SAVE_VLESS if proto == "VLESS" else SAVE_SS
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"Updated: {now}\n")
        f.write(f"Network: {network_type}\n\n")
        for i, s in enumerate(results, 1):
            stars = "⭐" * s["score"]
            f.write(f"{i}. {s['ping']}  {s['speed']}  {stars} {s['name']}\n{s['key']}\n\n")
    return fname

def get_favorites():
    if not os.path.exists(FAV_FILE): return []
    try:
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except: return []

def add_favorite(server):
    favs = get_favorites()
    if any(f["key"] == server["key"] for f in favs):
        return False, "ရှိပြီးသားပါ ❤️"
    favs.insert(0, {"name": server["name"], "key": server["key"], "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(favs, f, ensure_ascii=False, indent=2)
    return True, "အကြိုက်ထဲထည့်ပြီး ✅"

def load_sources():
    sources = [
        ("Pojie-VLESS", "https://pojiezhiyuanjun.github.io/freev2/vless.txt", "txt"),
        ("Pojie-SS", "https://pojiezhiyuanjun.github.io/freev2/ss.txt", "txt"),
        ("Pojie-All", "https://pojiezhiyuanjun.github.io/freev2/all.txt", "txt"),
        ("V2Ray-Vault-All", "https://raw.gitmirror.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
        ("Freefq", "https://raw.gitmirror.com/freefq/free/master/v2", "b64"),
    ]
    vless, ss = [], []
    for name, url, fmt in sources:
        text = fetch_url(url)
        if text:
            keys = parse_configs(text, fmt)
            for k in keys:
                if k["proto"] == "VLESS": vless.append(k)
                else: ss.append(k)
    return vless, ss

def country_menu():
    header("🌍 နိုင်ငံရွေးပါ")
    for k, v in COUNTRIES.items():
        print(f"  [{k}] {v[0]}")
    print("  [0] ပယ်ဖျက်")
    footer()
    c = input("ရွေးပါ → ").strip()
    if c == "0": return None, None
    if c in COUNTRIES:
        return COUNTRIES[c][0], COUNTRIES[c][1]
    return None, None

def filter_menu():
    header("📊 ရွေးချယ်မှု")
    print("  [1] ⚡ အမြန်ဆုံး 10 ခု")
    print("  [2] 🟢 တည်ငြိမ်သူများ (250ms အောက်)")
    print("  [3] 📊 အားလုံးပြပါ")
    print("  [0] ပယ်ဖျက်")
    footer()
    c = input("ရွေးပါ → ").strip()
    if c == "1": return "fastest"
    if c == "2": return "stable"
    if c == "3": return "all"
    return None

def scan(proto, all_keys, keywords, fmode):
    header("စစ်ဆေးနေသည်...")
    servers = [k for k in all_keys if k["proto"] == proto]
    if keywords:
        servers = [s for s in servers if any(kw.upper() in s["name"].upper() for kw in keywords)]
    total = len(servers)
    if total == 0:
        print("ဆာဗာမတွေ့ပါ")
        footer()
        input()
        return
    print(f"စုစုပေါင်း: {total} လုံး")
    alive = []
    for i, s in enumerate(servers, 1):
        print(f"စစ်ဆေးနေသည်... {i}/{total}", end="\r")
        try:
            from urllib.parse import urlparse
            p = urlparse(s["key"])
            ping_str, ms, score, stars, speed_level, speed_score = test_server(p.hostname, p.port)
            if ping_str:
                s["ping"] = ping_str
                s["ms"] = ms
                s["score"] = score
                s["speed"] = speed_level
                alive.append(s)
        except: pass
    alive.sort(key=lambda x: x["ms"])
    if fmode == "fastest": results = alive[:10]
    elif fmode == "stable": results = [s for s in alive if s["ms"] <= 250]
    else: results = alive
    header("🏆 ရလဒ်များ")
    if not results:
        print("ကိုက်ညီသည့်ဆာဗာမရှိပါ")
        footer()
        input()
        return
    for i, s in enumerate(results, 1):
        stars = "⭐" * s["score"]
        print(f"[{i}] {s['ping']}  {s['speed']}  {stars}")
        print(f"    {s['name']}")
        print(f"    {s['key']}")
        print(f"    f{i}=အကြိုက်ထည့်  c{i}=ကူးယူ\n")
    fname = save_results(proto, results)
    print(f"ဖိုင်ထဲသိမ်းပြီး → {fname}\n")
    footer()
    while True:
        cmd = input("လုပ်ဆောင်ပါ (0=ပြန်) → ").strip().lower()
        if cmd == "0": break
        if cmd.startswith("f") and cmd[1:].isdigit():
            idx = int(cmd[1:]) - 1
            if 0 <= idx < len(results):
                ok, msg = add_favorite(results[idx])
                print(f"  {msg}\n")
        if cmd.startswith("c") and cmd[1:].isdigit():
            idx = int(cmd[1:]) - 1
            if 0 <= idx < len(results):
                print(f"\n📋 ကူးယူပါ:\n{results[idx]['key']}\n")

def favorites_menu():
    header("❤️ အကြိုက်ဆုံးများ")
    favs = get_favorites()
    if not favs:
        print("\nအကြိုက်မရှိသေးပါ။ စကင်န်တစ်ခုလုပ်ပြီး f1,f2... နဲ့ထည့်ပါ ❤️\n")
    else:
        for i, fv in enumerate(favs, 1):
            print(f"[{i}] ❤️ {fv['name']}")
            print(f"    {fv['key']}\n")
    print("[0] ပြန်")
    footer()
    input()

def main():
    detect_network()
    vless_data, ss_data = load_sources()
    while True:
        header("ပင်မမီနူး")
        print(f"📡 လက်ရှိလိုင်း: {network_type}")
        print(f"🟦 VLESS: {len(vless_data)}  🟧 SS: {len(ss_data)}")
        print()
        print(" [1] 🌍 VLESS ရှာမည်")
        print(" [2] 📂 VLESS ရလဒ်များကြည့်မည်")
        print(" [3] ❤️ အကြိုက်ဆုံးများ")
        print(" [4] 🔄 စာရင်းအသစ်ပြန်ဖတ်မည်")
        print(" [5] 🌐 SS ရှာမည်")
        print(" [6] 📂 SS ရလဒ်များကြည့်မည်")
        print(" [0] ❌ ပိတ်မည်")
        footer()
        c = input("ရွေးပါ → ").strip()
        
        if c == "0":
            print("\n👋 ဘေးကင်းစွာပြန်လာကြပါ။ ကံကောင်းပါစေ! ✨\n")
            break
        elif c == "1":
            cl, kw = country_menu()
            if cl:
                fm = filter_menu()
                if fm: scan("VLESS", vless_data, kw, fm)
            input()
        elif c == "2":
            header("📂 VLESS ရလဒ်များ")
            if os.path.exists(SAVE_VLESS):
                with open(SAVE_VLESS, "r", encoding="utf-8") as f:
                    print(f.read())
            else:
                print("ဖိုင်မရှိသေးပါ")
            footer()
            input()
        elif c == "3":
            favorites_menu()
        elif c == "4":
            print("စာရင်းအသစ်ဖတ်နေသည်...")
            vless_data, ss_data = load_sources()
            print(f"✅ ပြီးပြီ! VLESS: {len(vless_data)}  SS: {len(ss_data)}")
            time.sleep(1)
        elif c == "5":
            cl, kw = country_menu()
            if cl:
                fm = filter_menu()
                if fm: scan("SS", ss_data, kw, fm)
            input()
        elif c == "6":
            header("📂 SS ရလဒ်များ")
            if os.path.exists(SAVE_SS):
                with open(SAVE_SS, "r", encoding="utf-8") as f:
                    print(f.read())
            else:
                print("ဖိုင်မရှိသေးပါ")
            footer()
            input()

if __name__ == "__main__":
    main()
    
