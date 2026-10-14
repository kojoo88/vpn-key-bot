#!/usr/bin/env python3
# ==========================================================
#    🚀 VPN Key Finder
#    Sources: Only your 4 links
# ==========================================================
import urllib.request, base64, socket, time, os, datetime

# Colors
BLU = "\033[94m"
GRN = "\033[92m"
YEL = "\033[93m"
RED = "\033[91m"
RST = "\033[0m"

def clear(): os.system("clear")
def line(): return "=" * 50

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
# 📡 Network Detection
# ==========================================================
def get_network_type():
    try:
        import subprocess
        result = subprocess.run(['ip', 'link'], capture_output=True, text=True, timeout=3)
        if 'wlan' in result.stdout.lower() or 'wlp' in result.stdout.lower():
            return "WiFi"
        else:
            return "Mobile Data"
    except:
        return "Unknown"

# ==========================================================
# 🔄 Fetch & Parse
# ==========================================================
def fetch(url):
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Android; Mobile)"}
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  {RED}✗{RST} Failed: {str(e)[:40]}")
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
                    name = unquote(line.split("#")[-1])[:35]
                except:
                    name = line.split("#")[-1][:35]
            if line.startswith("vless://"):
                keys.append({"type": "VLESS", "name": name, "url": line})
            elif line.startswith("ss://"):
                keys.append({"type": "SS", "name": name, "url": line})
    except Exception as e:
        print(f"  Parse error: {e}")
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
        if ms < 100:
            rating = f"{GRN}Excellent{RST} 🚀"
        elif ms < 200:
            rating = f"{GRN}Good{RST} ✅"
        elif ms < 350:
            rating = f"{YEL}Fair{RST} ⚡"
        else:
            rating = f"{RED}Slow{RST} 🐢"
        return True, ms, rating
    except:
        return False, 9999, "Unreachable ❌"

# ==========================================================
# 📥 Load All Keys
# ==========================================================
def load_all():
    all_vless = []
    all_ss = []
    print(f"\n{BLU}🔄 Loading {len(SOURCES)} sources...{RST}\n")
    for name, url, fmt in SOURCES:
        print(f"  {name:<20}", end=" ")
        text = fetch(url)
        if text:
            keys = parse(text, fmt)
            v = sum(1 for k in keys if k["type"] == "VLESS")
            s = sum(1 for k in keys if k["type"] == "SS")
            print(f"{GRN}✓{RST}  VLESS: {v}  SS: {s}")
            for k in keys:
                if k["type"] == "VLESS":
                    all_vless.append(k)
                else:
                    all_ss.append(k)
        else:
            print(f"{RED}✗ Failed{RST}")
    print()
    return all_vless, all_ss

# ==========================================================
# 🔍 Scan & Show
# ==========================================================
def show_results(keys):
    if not keys:
        print(f"{RED}No keys found!{RST}")
        return
    
    results = []
    print(f"\n{BLU}Testing {len(keys)} servers...{RST}\n")
    
    for i, k in enumerate(keys, 1):
        print(f"  [{i}/{len(keys)}] {k['name'][:35]:<35}", end="\r")
        ok, ms, rating = ping_test(k["url"])
        if ok:
            k["ms"] = ms
            k["rating"] = rating
            results.append(k)
    
    results.sort(key=lambda x: x["ms"])
    
    print(f"\n\n{line()}")
    print(f"  🎉 Found {len(results)} working servers")
    print(f"{line()}\n")
    
    for i, k in enumerate(results, 1):
        print(f"  [{i}] {k['rating']}  Ping: {k['ms']}ms")
        print(f"      📌 {k['name']}")
        print(f"      🔑 {k['url']}\n")
    
    with open("working_keys.txt", "w", encoding="utf-8") as f:
        f.write(f"Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Network: {get_network_type()}\n")
        f.write(f"Total working: {len(results)}\n\n")
        for k in results:
            f.write(f"{k['url']}\n")
    
    print(f"{GRN}✅ Saved to: working_keys.txt{RST}")
    input("\nPress Enter to go back...")

# ==========================================================
# 📋 MAIN MENU
# ==========================================================
def main():
    vless_data, ss_data = [], []
    network = get_network_type()
    
    while True:
        clear()
        print(f"{BLU}{line()}{RST}")
        print(f"  🚀 VPN Key Finder")
        print(f"{BLU}{line()}{RST}")
        print(f"  📡 Network: {network}")
        print(f"  📦 Sources: {len(SOURCES)}")
        if vless_data or ss_data:
            print(f"  🟦 VLESS: {len(vless_data)} keys")
            print(f"  🟧 SS:    {len(ss_data)} keys")
        print(f"{BLU}{line()}{RST}\n")
        
        print("  [1] 🔄 Load All Sources")
        print("  [2] 🟦 Find & Test VLESS Keys")
        print("  [3] 🟧 Find & Test SS Keys")
        print("  [4] 📄 View Saved Keys")
        print("  [0] ❌ Exit")
        print()
        
        choice = input("  Choose → ").strip()
        
        if choice == "0":
            print("\n  👋 Goodbye! ✨\n")
            break
        
        elif choice == "1":
            vless_data, ss_data = load_all()
            input("\n  Done! Press Enter...")
        
        elif choice == "2":
            if not vless_data:
                print(f"\n  {YEL}⚠️ Load sources first (Option 1){RST}")
                time.sleep(1.5)
                continue
            show_results(vless_data)
        
        elif choice == "3":
            if not ss_data:
                print(f"\n  {YEL}⚠️ Load sources first (Option 1){RST}")
                time.sleep(1.5)
                continue
            show_results(ss_data)
        
        elif choice == "4":
            if os.path.exists("working_keys.txt"):
                clear()
                print(f"{BLU}📄 working_keys.txt{RST}\n")
                with open("working_keys.txt", "r", encoding="utf-8") as f:
                    print(f.read())
                input("\nPress Enter...")
            else:
                print(f"\n  {RED}No saved file yet. Run a scan first!{RST}")
                time.sleep(1.5)
        
        else:
            print(f"\n  {RED}Invalid choice{RST}")
            time.sleep(1)

if __name__ == "__main__":
    main()
        
