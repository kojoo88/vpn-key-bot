#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════╗
# ║     🌟 ULTIMATE VPN KEY FINDER — DREAM EDITION           ║
# ║   Smart Scan • Auto-Save • History • Favorites • Share    ║
# ╚══════════════════════════════════════════════════════════╝
import urllib.request, base64, os, socket, time, datetime, json

# ─── 🎨 Theme Colors ───
BLU = "\033[94m"
CYN = "\033[96m"
GRN = "\033[92m"
YEL = "\033[93m"
RED = "\033[91m"
MAG = "\033[95m"
BLD = "\033[1m"
RST = "\033[0m"

# ─── 📁 Data Files ───
SAVE_VLESS = "best_vless.txt"
SAVE_SS    = "best_ss.txt"
FAV_FILE   = "favorites.json"
HIST_FILE  = "history.json"

# ─── 🌍 Country List ───
COUNTRIES = {
    "1": ("🇯🇵 Japan",     ["JP", "Japan", "Tokyo"]),
    "2": ("🇰🇷 Korea",     ["KR", "Korea", "Seoul"]),
    "3": ("🇸🇬 Singapore", ["SG", "Singapore", "Sin"]),
    "4": ("🇭🇰 Hong Kong", ["HK", "HongKong", "Hong"]),
    "5": ("🇺🇸 USA",       ["US", "USA", "United States", "Los Angeles", "New York"]),
    "6": ("🇹🇭 Thailand",  ["TH", "Thailand", "Bangkok"]),
    "7": ("🇲🇲 Best for MM", ["SG", "HK", "JP", "KR"]),
    "8": ("🌐 All Countries", []),
}

def clear(): os.system("clear")
def line(char="═", n=60): return char * n

def header(subtitle=""):
    clear()
    print(f"{CYN}{BLD}╔{line()}╗{RST}")
    print(f"{CYN}{BLD}║{RST}  🌟 {MAG}{BLD}ULTIMATE VPN KEY FINDER{RST}", end="")
    print(f"{' '*(28-len(subtitle))}{CYN}{BLD}║{RST}")
    if subtitle:
        print(f"{CYN}{BLD}║{RST}  {subtitle}{' '*(58-len(subtitle))}{CYN}{BLD}║{RST}")
    print(f"{CYN}{BLD}╠{line()}╣{RST}")

def footer():
    print(f"{CYN}{BLD}╚{line()}╝{RST}")

def ping_test(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.8)
        start = time.time()
        s.connect((host, int(port)))
        ms = int((time.time() - start) * 1000)
        s.close()
        if ms < 80:    return f"{GRN}✨ {ms}ms    PERFECT{RST}", ms, 5
        elif ms < 120: return f"{GRN}🌟 {ms}ms  EXCELLENT{RST}", ms, 5
        elif ms < 180: return f"{GRN}✅ {ms}ms    GREAT{RST}", ms, 4
        elif ms < 250: return f"{YEL}⚡ {ms}ms     GOOD{RST}", ms, 3
        elif ms < 400: return f"{YEL}📍 {ms}ms     FAIR{RST}", ms, 2
        else:          return f"{RED}⚠️ {ms}ms     SLOW{RST}", ms, 1
    except: return None, 9999, 0

def fetch_url(url):
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except: return None

def extract_name(line):
    if "#" not in line: return "Unknown Server"
    try:
        from urllib.parse import unquote
        return unquote(line.split("#")[-1])[:45].strip()
    except:
        return line.split("#")[-1][:45].strip() or "Unknown Server"

def detect_country(name):
    name_upper = name.upper()
    for code, (label, keywords) in COUNTRIES.items():
        for kw in keywords:
            if kw.upper() in name_upper:
                return label
    return "🌍 Other"

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
            country = detect_country(name)
            if line.startswith("vless://"):
                keys.append({"proto": "VLESS", "name": name, "country": country, 
                            "key": line, "ping": "--", "ms": 9999, "score": 0, "time_found": ""})
            elif line.startswith("ss://"):
                keys.append({"proto": "SS", "name": name, "country": country, 
                            "key": line, "ping": "--", "ms": 9999, "score": 0, "time_found": ""})
    except: pass
    return keys

# ═══════════════════════════════════════════════════════════
# 💾 SAVE & LOAD FUNCTIONS
# ═══════════════════════════════════════════════════════════
def save_results(proto, country_label, results, mode_label):
    try:
        fname = SAVE_VLESS if proto == "VLESS" else SAVE_SS
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(f"{line()}\n")
            f.write(f"  🏆 {mode_label}\n")
            f.write(f"  🌍 Region: {country_label}\n")
            f.write(f"  📅 Updated: {now}\n")
            f.write(f"{line()}\n\n")
            for idx, item in enumerate(results, 1):
                stars = "⭐" * item["score"]
                f.write(f"  [{idx}] {item['ping']}  {stars}\n")
                f.write(f"      {item['country']} | {item['name']}\n")
                f.write(f"      {item['key']}\n\n")
        return True, fname, now
    except: return False, "", ""

def load_saved_data(proto):
    fname = SAVE_VLESS if proto == "VLESS" else SAVE_SS
    if not os.path.exists(fname): return None, fname, ""
    try:
        with open(fname, "r", encoding="utf-8") as f:
            return f.read(), fname, os.path.getmtime(fname)
    except: return None, fname, ""

def save_to_history(proto, country_label, results):
    try:
        history = []
        if os.path.exists(HIST_FILE):
            with open(HIST_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "time": now,
            "proto": proto,
            "country": country_label,
            "count": len(results),
            "top_ms": results[0]["ms"] if results else None
        }
        history.insert(0, entry)
        history = history[:50]  # Keep last 50 records
        with open(HIST_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except: pass

def get_favorites():
    if not os.path.exists(FAV_FILE): return []
    try:
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except: return []

def add_favorite(server):
    favs = get_favorites()
    key = server["key"]
    if any(f["key"] == key for f in favs):
        return False, "Already in favorites"
    favs.insert(0, {
        "name": server["name"],
        "country": server["country"],
        "key": key,
        "added": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(favs, f, ensure_ascii=False, indent=2)
    return True, "Added to favorites ❤️"

def remove_favorite(index):
    favs = get_favorites()
    if 0 <= index < len(favs):
        del favs[index]
        with open(FAV_FILE, "w", encoding="utf-8") as f:
            json.dump(favs, f, ensure_ascii=False, indent=2)
        return True, "Removed from favorites"
    return False, "Invalid index"

# ═══════════════════════════════════════════════════════════
# 🔄 LOAD SOURCES
# ═══════════════════════════════════════════════════════════
def load_all_sources():
    header("🔄 REFRESHING SERVER LIST...")
    print(f"  📡 Reconnecting to server lists...\n")
    
    sources = [
        ("Shadowmere",  "https://shadowmere.xyz/api/b64sub/",          "b64"),
        ("V2Ray-Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
        ("V2Nodes",     "https://www.v2nodes.com/subscriptions/country/all/?key=72BEE427C23A1AF", "b64"),
    ]
    
    vless_list = []
    ss_list = []
    
    for name, url, fmt in sources:
        print(f"    🔄 {name:<18}", end=" ")
        text = fetch_url(url)
        if text:
            keys = parse_configs(text, fmt)
            v_cnt = sum(1 for k in keys if k["proto"] == "VLESS")
            s_cnt = sum(1 for k in keys if k["proto"] == "SS")
            print(f"{GRN}✓{RST}  VLESS:{v_cnt}  SS:{s_cnt}")
            for k in keys:
                if k["proto"] == "VLESS": vless_list.append(k)
                else: ss_list.append(k)
        else:
            print(f"{RED}✗{RST}")
    
    print(f"\n  ✅ Server list updated!  VLESS: {GRN}{len(vless_list)}{RST}  |  SS: {GRN}{len(ss_list)}{RST}\n")
    footer()
    input("  Back → Enter")
    return vless_list, ss_list

def boot_loader():
    header("LOADING SERVER SOURCES...")
    print(f"  📡 Connecting to server lists...\n")
    
    sources = [
        ("Shadowmere",  "https://shadowmere.xyz/api/b64sub/",          "b64"),
        ("V2Ray-Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
        ("V2Nodes",     "https://www.v2nodes.com/subscriptions/country/all/?key=72BEE427C23A1AF", "b64"),
    ]
    
    vless_list = []
    ss_list = []
    
    for name, url, fmt in sources:
        print(f"    🔄 {name:<18}", end=" ")
        text = fetch_url(url)
        if text:
            keys = parse_configs(text, fmt)
            v_cnt = sum(1 for k in keys if k["proto"] == "VLESS")
            s_cnt = sum(1 for k in keys if k["proto"] == "SS")
            print(f"{GRN}✓{RST}  VLESS:{v_cnt}  SS:{s_cnt}")
            for k in keys:
                if k["proto"] == "VLESS": vless_list.append(k)
                else: ss_list.append(k)
        else:
            print(f"{RED}✗{RST}")
    
    print(f"\n  ✅ Welcome!  VLESS: {GRN}{len(vless_list)}{RST}  |  SS: {GRN}{len(ss_list)}{RST}\n")
    footer()
    time.sleep(1.5)
    return vless_list, ss_list

# ═══════════════════════════════════════════════════════════
# 🌍 MENUS
# ═══════════════════════════════════════════════════════════
def country_filter_menu(proto):
    header(f"🌍 SELECT COUNTRY — {proto}")
    for k, v in COUNTRIES.items():
        print(f"   [{k}] {v[0]}")
    print(f"\n   [0] Cancel")
    footer()
    c = input(f"\n  {MAG}Choose Country → {RST}").strip()
    
    if c == "0": return None, None
    if c in COUNTRIES:
        return COUNTRIES[c][0], COUNTRIES[c][1]
    return None, None

def filter_menu():
    header("📊 SELECT SCAN MODE")
    print(f"   [1] ⚡ FASTEST Top 10       — အမြန်ဆုံး 10 ခု")
    print(f"   [2] 🟢 STABLE & GOOD        — တည်ငြိမ်+ကောင်း (250ms အောက်)")
    print(f"   [3] 📊 SHOW ALL + QUALITY   — အကုန်ပြပြီး အဆင့်သတ်မှတ်")
    print(f"   [4] 🎯 BEST FOR ME          — မြန်မာအတွက် အကောင်းဆုံး")
    print(f"\n   [0] Cancel")
    footer()
    c = input(f"\n  {MAG}Choose Mode → {RST}").strip()
    
    if c == "1": return "fastest", "⚡ FASTEST Top 10"
    elif c == "2": return "stable", "🟢 STABLE & GOOD"
    elif c == "3": return "all", "📊 SHOW ALL + QUALITY"
    elif c == "4": return "bestforme", "🎯 BEST FOR ME (Myanmar)"
    return None, None

def favorites_menu():
    header("❤️ MY FAVORITES")
    favs = get_favorites()
    if not favs:
        print(f"\n  {YEL}⚠️ No favorites yet!{RST}")
        print(f"  Scan any server and add to favorites ❤️\n")
    else:
        for idx, item in enumerate(favs, 1):
            print(f"  [{idx}] ❤️ {item['country']} | {item['name']}")
            print(f"      {item['key']}\n")
        print(f"  [del#] Remove from favorites (e.g. del1)")
    print(f"  [0] Back")
    footer()
    c = input(f"\n  {MAG}Action → {RST}").strip().lower()
    if c == "0": return
    if c.startswith("del"):
        try:
            idx = int(c[3:]) - 1
            ok, msg = remove_favorite(idx)
            print(f"  {GRN}✓ {msg}{RST}\n")
        except:
            print(f"  {RED}⚠️ Invalid command{RST}\n")
        time.sleep(1.5)

def history_menu():
    header("📈 SCAN HISTORY")
    if not os.path.exists(HIST_FILE):
        print(f"\n  {YEL}⚠️ No history yet!{RST}")
        print(f"  Run a scan first to record history\n")
    else:
        with open(HIST_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
        if not history:
            print(f"\n  {YEL}⚠️ No history yet!{RST}\n")
        else:
            print(f"  {'Time':<18} {'Proto':<6} {'Region':<20} {'Found':<6} {'Best':<8}")
            print(f"  {line('-',58)}")
            for item in history[:15]:
                print(f"  {item['time']:<18} {item['proto']:<6} {item['country'][:18]:<20} {item['count']:<6} {item['top_ms']}ms")
            print(f"\n  Showing last 15 of {len(history)} records\n")
    print(f"  [0] Back")
    footer()
    input(f"\n  {MAG}Press Enter → Back{RST}")

# ═══════════════════════════════════════════════════════════
# 🔍 SCAN & DISPLAY
# ═══════════════════════════════════════════════════════════
def scan_and_filter(proto, all_keys, country_label, keywords, filter_mode, mode_label):
    header(f"🔍 SCANNING {proto} — {country_label}")
    
    servers = [k for k in all_keys if k["proto"] == proto]
    if keywords:
        servers = [s for s in servers if any(kw.upper() in s["name"].upper() for kw in keywords)]
    
    total = len(servers)
    if total == 0:
        print(f"\n  {YEL}⚠️ No servers found for this region{RST}\n")
        footer()
        input("  Back → Enter")
        return
    
    print(f"  ⚠️  {YEL}IMPORTANT: First time using VPN? Connect to the fastest server first!{RST}\n")
    print(f"  📦 Total: {BLU}{total}{RST} servers")
    print(f"  🔄 Testing connection speed & quality...\n")
    
    alive = []
    start_time = time.time()
    
    for idx, svr in enumerate(servers, 1):
        print(f"    [{idx}/{total}] {svr['country']} {svr['name'][:24]:<24}", end="\r")
        try:
            from urllib.parse import urlparse
            p = urlparse(svr["key"])
            ping_str, ms, score = ping_test(p.hostname, p.port)
            if ping_str:
                svr["ping"] = ping_str
                svr["ms"] = ms
                svr["score"] = score
                svr["time_found"] = datetime.datetime.now().strftime("%H:%M")
                alive.append(svr.copy())
        except: pass
    
    elapsed = int(time.time() - start_time)
    alive_sorted = sorted(alive, key=lambda x: x["ms"])
    
    # Apply filters
    if filter_mode == "fastest":
        results = alive_sorted[:10]
    elif filter_mode == "stable":
        results = [s for s in alive_sorted if s["ms"] <= 250]
    elif filter_mode == "bestforme":
        results = [s for s in alive_sorted if s["ms"] <= 300][:10]
    else:
        results = alive_sorted
    
    # Save history
    save_to_history(proto, country_label, results)
    
    header(f"🏆 {mode_label}")
    print(f"  ⚠️  {YEL}IMPORTANT: First time using VPN? Connect to the fastest server first!{RST}\n")
    print(f"  📊 Scanned: {BLU}{total}{RST} | ✅ Online: {GRN}{len(alive)}{RST} | ✅ Selected: {MAG}{len(results)}{RST} | ⏱️ {elapsed}s\n")
    
    if not results:
        print(f"  {RED}😢 No matching servers found{RST}\n")
        footer()
        input("  Back → Enter")
        return
    
    for idx, svr in enumerate(results, 1):
        stars = "⭐" * svr["score"]
        print(f"  {BLU}{BLD}[{idx:02d}]{RST}  {svr['ping']}  {stars}")
        print(f"       {svr['country']}  {MAG}{svr['name']}{RST}")
        print(f"       {svr['key']}")
        print(f"       💡 [f{idx}] = Add to Favorites ❤️\n")
    
    print(f"  💾 Auto-saved to file")
    print(f"  ➕ To add: type f1, f2, etc.  |  [0] Done\n")
    footer()
    
    # Interactive: add to favorites
    while True:
        cmd = input(f"  {MAG}Action → {RST}").strip().lower()
        if cmd == "0": break
        if cmd.startswith("f") and cmd[1:].isdigit():
            try:
                idx = int(cmd[1:]) - 1
                if 0 <= idx < len(results):
                    ok, msg = add_favorite(results[idx])
                    print(f"  {GRN}✓ {msg}{RST}\n")
                else:
                    print(f"  {RED}⚠️ Invalid number{RST}\n")
            except:
                print(f"  {RED}⚠️ Try again{RST}\n")
    
    # Save results to file
    ok, fname, stamp = save_results(proto, country_label, results, mode_label)
    if ok:
        print(f"\n  💾 {GRN}✓ Saved to: {fname}{RST}")
        print(f"  📅 Time: {stamp}{RST}")
    print()
    footer()

def view_saved(proto):
    content, fname, mtime = load_saved_data(proto)
    header(f"📂 SAVED {proto} — Results")
    print(f"  ⚠️  {YEL}IMPORTANT: First time using VPN? Connect to the fastest server first!{RST}\n")
    if not content:
        print(f"  {YEL}⚠️ No saved data yet!{RST}")
        print(f"  First run: Scan & Filter\n")
    else:
        print(f"  📄 File: {fname}\n")
        print(content)
    footer()

# ═══════════════════════════════════════════════════════════
# 🏠 MAIN MENU
# ═══════════════════════════════════════════════════════════
def main():
    vless_data, ss_data = boot_loader()
    
    while True:
        header("MAIN MENU")
        print(f"  🟦 {BLU}VLESS SERVERS{RST}        🟧 {YEL}SS SERVERS{RST}")
        print(f"  {line('-',16)}        {line('-',16)}")
        print(f"   [1] 🌍 Scan VLESS        [5] 🌍 Scan SS")
        print(f"   [2] 📂 View Saved VLESS   [6] 📂 View Saved SS")
        print(f"  ═══ EXTRA FEATURES ═══")
        print(f"   [3] ❤️  My Favorites      [7] 📈 Scan History")
        print(f"   [4] 🔄 Refresh List       [0] ❌ Exit")
        print(f"  {line('-',40)}")
        footer()
        
        choice = input(f"\n  {MAG}Your choice → {RST}").strip()
        
        if choice == "0":
            header("GOODBYE! 👋")
            print(f"\n  Thank you for using 🌟 Ultimate VPN Key Finder — Dream Edition!")
            print(f"  💡 Your best servers are always auto-saved")
            print(f"  ❤️  Favorites & History keep your best connections safe\n")
            footer()
            break
        elif choice == "1":
            country_label, keywords = country_filter_menu("VLESS")
            if country_label:
                filter_mode, mode_label = filter_menu()
                if filter_mode:
                    scan_and_filter("VLESS", vless_data, country_label, keywords, filter_mode, mode_label)
            input(f"\n  {MAG}Back → Menu{RST}")
        elif choice == "2":
            view_saved("VLESS")
            input(f"\n  {MAG}Back → Menu{RST}")
        elif choice == "3":
            favorites_menu()
        elif choice == "4":
            vless_data, ss_data = load_all_sources()
        elif choice == "5":
            country_label, keywords = country_filter_menu("SS")
            if country_label:
                filter_mode, mode_label = filter_menu()
                if filter_mode:
                    scan_and_filter("SS", ss_data, country_label, keywords, filter_mode, mode_label)
            input(f"\n  {MAG}Back → Menu{RST}")
        elif choice == "6":
            view_saved("SS")
            input(f"\n  {MAG}Back → Menu{RST}")
        elif choice == "7":
            history_menu()
        else:
            print(f"\n  {RED}⚠️ Invalid choice!{RST}")
            time.sleep(1)

if __name__ == "__main__":
    main()
        
