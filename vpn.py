#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════╗
# ║          🚀 Ultimate VPN Key Finder                      ║
# ║              — Dream Edition ✨                           ║
# ╚══════════════════════════════════════════════════════════╝
import urllib.request, base64, socket, time, os, datetime

# 🎨 COLORS
BLU = "\033[94m"
CYN = "\033[96m"
GRN = "\033[92m"
YEL = "\033[93m"
RED = "\033[91m"
MAG = "\033[95m"
BLD = "\033[1m"
DIM = "\033[2m"
RST = "\033[0m"

def clear(): os.system("clear")
def hline(): return "═" * 58
def stars(n): return "⭐" * n + "☆" * (5-n)

# ==========================================================
# 🌐 YOUR SOURCES - DO NOT CHANGE
# ==========================================================
SOURCES = [
    ("V2Nodes", "https://www.v2nodes.com/subscriptions/country/all/?key=72BEE427C23A1AF", "b64"),
    ("Shadowmere", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("V2Ray-Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
    ("V2Ray-Configs SS", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Splitted-By-Protocol/ss.txt", "txt"),
]

# ==========================================================
# 📡 NETWORK DETECTION
# ==========================================================
def get_network():
    try:
        import subprocess
        r = subprocess.run(['ip','link'], capture_output=True, text=True, timeout=3)
        if 'wlan' in r.stdout.lower() or 'wlp' in r.stdout.lower():
            return f"📡 WiFi"
        return f"📱 Mobile Data"
    except:
        return "❓ Unknown"

# ==========================================================
# 🔄 FETCH & PARSE
# ==========================================================
def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", errors="ignore")
    except:
        return None

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
                    name = unquote(line.split("#")[-1])[:38]
                except:
                    name = line.split("#")[-1][:38]
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
        host = p.hostname
        port = p.port or 443
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        start = time.time()
        s.connect((host, int(port)))
        ms = int((time.time() - start) * 1000)
        s.close()
        if ms < 80:
            level = f"{GRN}🚀 Fast{RST}"
            score = 5
        elif ms < 150:
            level = f"{GRN}✅ Good{RST}"
            score = 4
        elif ms < 250:
            level = f"{YEL}⚡ Normal{RST}"
            score = 3
        elif ms < 400:
            level = f"{YEL}⚠️ Slow{RST}"
            score = 2
        else:
            level = f"{RED}🐢 Very Slow{RST}"
            score = 1
        return True, ms, level, score
    except:
        return False, 9999, f"{RED}❌ Offline{RST}", 0

# ==========================================================
# 📥 LOAD SOURCES
# ==========================================================
def load_sources():
    vless, ss = [], []
    print(f"\n{CYN}🔄 Loading Sources...{RST}\n")
    for name, url, fmt in SOURCES:
        print(f"  {name:<18}", end=" ")
        text = fetch(url)
        if text:
            keys = parse(text, fmt)
            v_count = sum(1 for k in keys if k["type"]=="VLESS")
            s_count = sum(1 for k in keys if k["type"]=="SS")
            print(f"{GRN}✓{RST}  VLESS: {v_count}  SS: {s_count}")
            for k in keys:
                if k["type"]=="VLESS": vless.append(k)
                else: ss.append(k)
        else:
            print(f"{RED}✗ Failed{RST}")
    print()
    return vless, ss

# ==========================================================
# 🔍 SCAN & SHOW
# ==========================================================
def scan_and_show(keys):
    if not keys:
        print(f"\n{RED}⚠️ No keys found. Load sources first!{RST}")
        time.sleep(1.5)
        return
    results = []
    print(f"\n{CYN}🧪 Testing {len(keys)} servers...{RST}\n")
    for i, k in enumerate(keys, 1):
        print(f"  [{i}/{len(keys)}] {k['name'][:35]:<35}", end="\r")
        ok, ms, level, score = ping_test(k["url"])
        if ok:
            k["ms"] = ms
            k["level"] = level
            k["score"] = score
            results.append(k)
    results.sort(key=lambda x: x["ms"])
    print("\n" * 2)
    
    if not results:
        print(f"{RED}❌ No working servers found{RST}")
        time.sleep(2)
        return
    
    print(f"{BLD}{BLU}┌{hline()}┐{RST}")
    print(f"{BLD}{BLU}│{RST}{MAG}{BLD}  🎉 Found {len(results)} Working Servers{' '*(28-len(str(len(results))))}{BLD}{BLU}│{RST}")
    print(f"{BLD}{BLU}├{hline()}┤{RST}")
    
    for i, s in enumerate(results, 1):
        print(f"  [{i}] {s['level']}  Ping: {s['ms']}ms  {stars(s['score'])}")
        print(f"      📌 {BLD}{s['name']}{RST}")
        print(f"      🔑 {s['url'][:75]}...")
        print()
    
    # Save
    with open("working_keys.txt", "w", encoding="utf-8") as f:
        f.write("="*50 + "\n")
        f.write("🚀 Ultimate VPN Key Finder — Dream Edition ✨\n")
        f.write("="*50 + "\n")
        f.write(f"Updated : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Network : {get_network()}\n")
        f.write(f"Total   : {len(results)} servers\n")
        f.write("="*50 + "\n\n")
        for s in results:
            f.write(f"{s['url']}\n")
    
    print(f"{BLD}{BLU}└{hline()}┘{RST}")
    print(f"\n{GRN}✅ Saved → working_keys.txt{RST}")
    input(f"\n{CYN}Press Enter to return...{RST}")

# ==========================================================
# 📄 VIEW SAVED
# ==========================================================
def view_saved():
    clear()
    print(f"{BLD}{MAG}📄 Saved Keys{RST}\n")
    if not os.path.exists("working_keys.txt"):
        print(f"{RED}File not found! Run a scan first.{RST}")
        time.sleep(2)
        return
    with open("working_keys.txt", "r", encoding="utf-8") as f:
        print(f.read())
    input(f"\n{CYN}Press Enter to return...{RST}")

# ==========================================================
# 🏠 MAIN MENU
# ==========================================================
def main():
    vless_data, ss_data = [], []
    while True:
        clear()
        print(f"{BLD}{MAG}╔{hline()}╗{RST}")
        print(f"{BLD}{MAG}║{RST}{BLD}        🚀 Ultimate VPN Key Finder{RST}{' '*(18)}{BLD}{MAG}║{RST}")
        print(f"{BLD}{MAG}║{RST}{DIM}             — Dream Edition ✨{' '*(24)}{BLD}{MAG}║{RST}")
        print(f"{BLD}{MAG}╠{hline()}╣{RST}")
        net = get_network()
        print(f"{BLD}{MAG}║{RST}  📡 Network: {net}{' '*(42-len(net))}{BLD}{MAG}║{RST}")
        print(f"{BLD}{MAG}║{RST}  📦 Sources: {len(SOURCES)}{' '*(44)}{BLD}{MAG}║{RST}")
        print(f"{BLD}{MAG}║{RST}  🟦 VLESS: {len(vless_data)}{' '*(45-len(str(len(vless_data))))}{BLD}{MAG}║{RST}")
        print(f"{BLD}{MAG}║{RST}  🟧 SS:    {len(ss_data)}{' '*(45-len(str(len(ss_data))))}{BLD}{MAG}║{RST}")
        print(f"{BLD}{MAG}╠{hline()}╣{RST}")
        print(f"{BLD}{MAG}║{RST}  {BLD}MENU OPTIONS{RST}{' '*(43)}{BLD}{MAG}║{RST}")
        print(f"{BLD}{MAG}╠{hline()}╣{RST}")
        print(f"{BLD}{MAG}║{RST}  {GRN}[1]{RST} 🔄 Load All Sources{' '*(38)}{BLD}{MAG}║{RST}")
        print(f"{BLD}{MAG}║{RST}  {GRN}[2]{RST} 🟦 Find & Test VLESS Keys{' '*(34)}{BLD}{MAG}║{RST}")
        print(f"{BLD}{MAG}║{RST}  {GRN}[3]{RST} 🟧 Find & Test SS Keys{' '*(38)}{BLD}{MAG}║{RST}")
        print(f"{BLD}{MAG}║{RST}  {GRN}[4]{RST} 📄 View Saved Keys{' '*(39)}{BLD}{MAG}║{RST}")
        print(f"{BLD}{MAG}║{RST}  {RED}[0]{RST} ❌ Exit{' '*(49)}{BLD}{MAG}║{RST}")
        print(f"{BLD}{MAG}╚{hline()}╝{RST}")
        choice = input(f"\n  {BLD}Choose → {RST}").strip()
        
        if choice == "0":
            clear()
            print(f"\n{MAG}✨ Thanks for using Dream Edition ✨{RST}")
            print(f"{CYN}   Stay fast, stay safe! 🚀{RST}\n")
            break
        elif choice == "1":
            vless_data, ss_data = load_sources()
            input(f"\n{CYN}Done! Press Enter...{RST}")
        elif choice == "2":
            if not vless_data:
                print(f"\n{YEL}⚠️ Load sources first!{RST}")
                time.sleep(1.5)
                continue
            scan_and_show(vless_data)
        elif choice == "3":
            if not ss_data:
                print(f"\n{YEL}⚠️ Load sources first!{RST}")
                time.sleep(1.5)
                continue
            scan_and_show(ss_data)
        elif choice == "4":
            view_saved()
        else:
            print(f"\n{RED}Invalid choice!{RST}")
            time.sleep(1)

if __name__ == "__main__":
    main()
