#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════╗
# ║     🚀 ULTIMATE VPN KEY FINDER — Smart Edition           ║
# ║   Auto-Scan • Fastest Top 10 • Smart Save • Quick View    ║
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

def clear(): os.system("clear")

def line(char="═", n=58): return char * n

def header(subtitle=""):
    clear()
    print(f"{CYN}{BLD}╔{line()}╗{RST}")
    print(f"{CYN}{BLD}║{RST}  🚀 {MAG}{BLD}ULTIMATE VPN KEY FINDER{RST}", end="")
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
        if ms < 100:   return f"{GRN}🌟 {ms}ms  EXCELLENT{RST}", ms
        elif ms < 150: return f"{GRN}✅ {ms}ms    GREAT{RST}", ms
        elif ms < 250: return f"{YEL}⚡ {ms}ms     GOOD{RST}", ms
        elif ms < 400: return f"{YEL}📍 {ms}ms     FAIR{RST}", ms
        else:           return f"{RED}⚠️ {ms}ms     SLOW{RST}", ms
    except: return None, 9999

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
        return unquote(line.split("#")[-1])[:35].strip()
    except:
        return line.split("#")[-1][:35].strip() or "Unknown Server"

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
                keys.append({"proto": "VLESS", "name": name, "key": line, "ping": "--", "ms": 9999})
            elif line.startswith("ss://"):
                keys.append({"proto": "SS", "name": name, "key": line, "ping": "--", "ms": 9999})
    except: pass
    return keys

def save_top10(proto, top10):
    try:
        fname = SAVE_VLESS if proto == "VLESS" else SAVE_SS
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(f"{'═'*60}\n")
            f.write(f"  🏆 TOP 10 FASTEST {proto} SERVERS\n")
            f.write(f"  📅 Updated: {now}\n")
            f.write(f"{'═'*60}\n\n")
            for idx, item in enumerate(top10, 1):
                f.write(f"  [{idx}] {item['ping']} | {item['name']}\n")
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

def scan_and_pick_best(proto, all_keys):
    header(f"🔍 SCANNING {proto} SERVERS...")
    servers = [k for k in all_keys if k["proto"] == proto]
    total = len(servers)
    
    if total == 0:
        print(f"\n  {RED}⚠️ No {proto} servers available right now{RST}\n")
        footer()
        input("  Back → Enter")
        return None
    
    print(f"  📦 Total: {BLU}{total}{RST} servers")
    print(f"  🔄 Testing connection speed...\n")
    
    alive = []
    start_time = time.time()
    
    for idx, svr in enumerate(servers, 1):
        print(f"    [{idx}/{total}] {svr['name'][:28]:<28}", end="\r")
        try:
            from urllib.parse import urlparse
            p = urlparse(svr["key"])
            ping_str, ms = ping_test(p.hostname, p.port)
            if ping_str:
                svr["ping"] = ping_str
                svr["ms"] = ms
                alive.append(svr.copy())
        except: pass
    
    elapsed = int(time.time() - start_time)
    top10 = sorted(alive, key=lambda x: x["ms"])[:10]
    
    header(f"🏆 TOP 10 FASTEST {proto} SERVERS")
    print(f"  📊 Scanned: {BLU}{total}{RST} | ✅ Online: {GRN}{len(alive)}{RST} | ⏱️ Done in {elapsed}s\n")
    
    if not top10:
        print(f"  {RED}😢 No working servers found{RST}")
        print(f"  {YEL}  Check your internet or try again later{RST}\n")
        footer()
        input("  Back → Enter")
        return None
    
    for idx, svr in enumerate(top10, 1):
        print(f"  {BLU}{BLD}[{idx:02d}]{RST}  {svr['ping']}")
        print(f"       {MAG}{svr['name']}{RST}")
        print(f"       {svr['key']}\n")
    
    ok, fname, stamp = save_top10(proto, top10)
    if ok:
        print(f"  💾 {GRN}✓ Saved to: {fname}{RST}")
        print(f"  📅 Time: {stamp}\n")
    footer()
    return top10

def view_saved(proto):
    content, fname, mtime = load_saved_data(proto)
    header(f"📂 SAVED {proto} — Top 10 Fastest")
    if not content:
        print(f"\n  {YEL}⚠️ No saved data yet!{RST}")
        print(f"  First run: [1] Scan & Find Best\n")
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
        print(f"   [1] 🔍 Scan & Best      [3] 🔍 Scan & Best")
        print(f"   [2] 📂 View Saved       [4] 📂 View Saved")
        print(f"  {line('-',40)}")
        print(f"   [0] ❌ Exit")
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
            scan_and_pick_best("VLESS", vless_data)
            input(f"\n  {MAG}Back to Menu → Enter{RST}")
        elif choice == "2":
            view_saved("VLESS")
            input(f"\n  {MAG}Back to Menu → Enter{RST}")
        elif choice == "3":
            scan_and_pick_best("SS", ss_data)
            input(f"\n  {MAG}Back to Menu → Enter{RST}")
        elif choice == "4":
            view_saved("SS")
            input(f"\n  {MAG}Back to Menu → Enter{RST}")
        else:
            print(f"\n  {RED}⚠️ Invalid choice! Try again{RST}")
            time.sleep(1)

if __name__ == "__main__":
    main()
    
