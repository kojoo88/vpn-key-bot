#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════╗
# ║     🌍 ULTIMATE VPN KEY FINDER — Smart Filter Edition     ║
# ║   Auto-Scan • Smart Filter • Quality Score • Auto-Save   ║
# ╚══════════════════════════════════════════════════════════╝
import urllib.request, base64, os, socket, time, datetime

# ─── Theme Colors ───
BLU = "\033[94m"
CYN = "\033[96m"
GRN = "\033[92m"
YEL = "\033[93m"
RED = "\033[91m"
MAG = "\033[95m"
BLD = "\033[1m"
RST = "\033[0m"

# ─── Data Files ───
SAVE_VLESS = "best_vless.txt"
SAVE_SS    = "best_ss.txt"

# ─── Country List ───
COUNTRIES = {
    "1": ("🇯🇵 Japan",     ["JP", "Japan", "Tokyo"]),
    "2": ("🇰🇷 Korea",     ["KR", "Korea", "Seoul"]),
    "3": ("🇸🇬 Singapore", ["SG", "Singapore", "Sin"]),
    "4": ("🇭🇰 Hong Kong", ["HK", "HongKong", "Hong"]),
    "5": ("🇺🇸 USA",       ["US", "USA", "United States", "Los Angeles", "New York"]),
    "6": ("🇹🇭 Thailand",  ["TH", "Thailand", "Bangkok"]),
    "7": ("🌐 All Countries", []),
}

def clear(): os.system("clear")
def line(char="═", n=58): return char * n

def header(subtitle=""):
    clear()
    print(f"{CYN}{BLD}╔{line()}╗{RST}")
    print(f"{CYN}{BLD}║{RST}  🌍 {MAG}{BLD}ULTIMATE VPN KEY FINDER{RST}", end="")
    print(f"{' '*(26-len(subtitle))}{CYN}{BLD}║{RST}")
    if subtitle:
        print(f"{CYN}{BLD}║{RST}  {subtitle}{' '*(56-len(subtitle))}{CYN}{BLD}║{RST}")
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
        if ms < 100:   return f"{GRN}🌟 {ms}ms  EXCELLENT{RST}", ms, 5
        elif ms < 150: return f"{GRN}✅ {ms}ms    GREAT{RST}", ms, 4
        elif ms < 250: return f"{YEL}⚡ {ms}ms     GOOD{RST}", ms, 3
        elif ms < 400: return f"{YEL}📍 {ms}ms     FAIR{RST}", ms, 2
        else:           return f"{RED}⚠️ {ms}ms     SLOW{RST}", ms, 1
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
        return unquote(line.split("#")[-1])[:40].strip()
    except:
        return line.split("#")[-1][:40].strip() or "Unknown Server"

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
                            "key": line, "ping": "--", "ms": 9999, "score": 0})
            elif line.startswith("ss://"):
                keys.append({"proto": "SS", "name": name, "country": country, 
                            "key": line, "ping": "--", "ms": 9999, "score": 0})
    except: pass
    return keys

def save_results(proto, country_label, results, mode_label):
    try:
        fname = SAVE_VLESS if proto == "VLESS" else SAVE_SS
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(f"{'═'*60}\n")
            f.write(f"  🏆 {mode_label} — {proto} SERVERS — {country_label}\n")
            f.write(f"  📅 Updated: {now}\n")
            f.write(f"{'═'*60}\n\n")
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
        print(f"    🔄 {name:<15}", end=" ")
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
    
    print(f"\n  ✅ Server list refreshed!  VLESS: {GRN}{len(vless_list)}{RST}  |  SS: {GRN}{len(ss_list)}{RST}\n")
    footer()
    input("  Back → Enter")
    return vless_list, ss_list

def country_filter_menu(proto):
    header(f"🌍 SELECT COUNTRY — {proto}")
    for k, v in COUNTRIES.items():
        print(f"   [{k}] {v[0]}")
    print(f"\n   [0] Cancel")
    footer()
    c = input(f"\n  {MAG}Choose Country → {RST}").strip()
    
    if c == "0": return None, None
    if c in COUNTRIES:
        country_label = COUNTRIES[c][0]
        keywords = COUNTRIES[c][1]
        return country_label, keywords
    return None, None

def filter_menu():
    header("📊 SELECT FILTER MODE")
    print(f"   [1] ⚡ FASTEST Top 10       — အမြန်ဆုံး 10 ခု")
    print(f"   [2] 🟢 STABLE & GOOD        — တည်ငြိမ်+ကောင်းမွန် (250ms အောက်)")
    print(f"   [3] 📊 SHOW ALL + QUALITY   — အကုန်ပြပြီး အဆင့်သတ်မှတ်ပေး")
    print(f"\n   [0] Cancel")
    footer()
    c = input(f"\n  {MAG}Choose Filter → {RST}").strip()
    
    if c == "1": return "fastest", "⚡ FASTEST Top 10"
    elif c == "2": return "stable", "🟢 STABLE & GOOD"
    elif c == "3": return "all", "📊 SHOW ALL + QUALITY"
    return None, None

def scan_and_filter(proto, all_keys, country_label, keywords, filter_mode, mode_label):
    header(f"🔍 SCANNING {proto} — {country_label}")
    
    servers = [k for k in all_keys if k["proto"] == proto]
    if keywords:
        servers = [s for s in servers if any(kw.upper() in s["name"].upper() for kw in keywords)]
    
    total = len(servers)
    if total == 0:
        print(f"\n  {YEL}⚠️ No servers found for this country{RST}\n")
        footer()
        input("  Back → Enter")
        return
    
    print(f"  ⚠️  {YEL}IMPORTANT: First time using VPN? Please connect to the fastest server first!{RST}\n")
    print(f"  📦 Total: {BLU}{total}{RST} servers")
    print(f"  🔄 Testing connection & quality...\n")
    
    alive = []
    start_time = time.time()
    
    for idx, svr in enumerate(servers, 1):
        print(f"    [{idx}/{total}] {svr['country']} {svr['name'][:22]:<22}", end="\r")
        try:
            from urllib.parse import urlparse
            p = urlparse(svr["key"])
            ping_str, ms, score = ping_test(p.hostname, p.port)
            if ping_str:
                svr["ping"] = ping_str
                svr["ms"] = ms
                svr["score"] = score
                alive.append(svr.copy())
        except: pass
    
    elapsed = int(time.time() - start_time)
    alive_sorted = sorted(alive, key=lambda x: x["ms"])
    
    # Apply filters
    if filter_mode == "fastest":
        results = alive_sorted[:10]
    elif filter_mode == "stable":
        results = [s for s in alive_sorted if s["ms"] <= 250]
    else:  # all
        results = alive_sorted
    
    header(f"🏆 {mode_label}")
    print(f"  ⚠️  {YEL}IMPORTANT: First time using VPN? Please connect to the fastest server first!{RST}\n")
    print(f"  📊 Scanned: {BLU}{total}{RST} | ✅ Online: {GRN}{len(alive)}{RST} | ✅ Passed: {MAG}{len(results)}{RST} | ⏱️ {elapsed}s\n")
    
    if not results:
        print(f"  {RED}😢 No matching servers found{RST}")
        if filter_mode == "stable":
            print(f"  {YEL}  Try 'Show All' to see all available servers{RST}\n")
        footer()
        input("  Back → Enter")
        return
    
    for idx, svr in enumerate(results, 1):
        stars = "⭐" * svr["score"]
        print(f"  {BLU}{BLD}[{idx:02d}]{RST}  {svr['ping']}  {stars}")
        print(f"       {svr['country']}  {MAG}{svr['name']}{RST}")
        print(f"       {svr['key']}\n")
    
    ok, fname, stamp = save_results(proto, country_label, results, mode_label)
    if ok:
        print(f"  💾 {GRN}✓ Saved to: {fname}{RST}")
        print(f"  📅 Time: {stamp}\n")
    footer()

def view_saved(proto):
    content, fname, mtime = load_saved_data(proto)
    header(f"📂 SAVED {proto} — Results")
    print(f"  ⚠️  {YEL}IMPORTANT: First time using VPN? Please connect to the fastest server first!{RST}\n")
    if not content:
        print(f"  {YEL}⚠️ No saved data yet!{RST}")
        print(f"  First run: Scan & Filter\n")
    else:
        print(f"  📄 File: {fname}\n")
        print(content)
    footer()

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
        print(f"    🔄 {name:<15}", end=" ")
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
    
    print(f"\n  ✅ Ready!  VLESS: {GRN}{len(vless_list)}{RST}  |  SS: {GRN}{len(ss_list)}{RST}\n")
    footer()
    time.sleep(1.5)
    return vless_list, ss_list

def main():
    vless_data, ss_data = boot_loader()
    
    while True:
        header("MAIN MENU")
        print(f"  🟦 {BLU}VLESS SERVERS{RST}        🟧 {YEL}SS SERVERS{RST}")
        print(f"  {line('-',16)}        {line('-',16)}")
        print(f"   [1] 🌍 Scan VLESS        [4] 🌍 Scan SS")
        print(f"   [2] 📂 View Saved VLESS   [5] 📂 View Saved SS")
        print(f"   [3] 🔄 Refresh List      [0] ❌ Exit")
        print(f"  {line('-',40)}")
        footer()
        
        choice = input(f"\n  {MAG}Your choice → {RST}").strip()
        
        if choice == "0":
            header("GOODBYE! 👋")
            print(f"\n  Thank you for using Ultimate VPN Key Finder!")
            print(f"  💡 Your best servers are always auto-saved\n")
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
            vless_data, ss_data = load_all_sources()
        elif choice == "4":
            country_label, keywords = country_filter_menu("SS")
            if country_label:
                filter_mode, mode_label = filter_menu()
                if filter_mode:
                    scan_and_filter("SS", ss_data, country_label, keywords, filter_mode, mode_label)
            input(f"\n  {MAG}Back → Menu{RST}")
        elif choice == "5":
            view_saved("SS")
            input(f"\n  {MAG}Back → Menu{RST}")
        else:
            print(f"\n  {RED}⚠️ Invalid choice!{RST}")
            time.sleep(1)

if __name__ == "__main__":
    main()
