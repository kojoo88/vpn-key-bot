#!/usr/bin/env python3
import urllib.request, base64, socket, time, os, datetime, random, sys

# COLORS
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
RST = "\033[0m"

# ================== ADMIN LINK ==================
ADMIN_LINK = "https://www.facebook.com/share/19TVQNTUGZ/"
# =================================================

def clear(): os.system("clear")

def open_admin_link():
    """Admin စာမျက်နှာကို တိုက်ရိုက်ဖွင့်ပေးမယ်"""
    clear()
    print(PUR + "="*50 + RST)
    print(PUR + "|" + RST + "   📘 Admin Page ဖွင့်နေသည်...    " + PUR + "|" + RST)
    print(PUR + "="*50 + RST)
    print(f"\n  🔗 လင့်ခ်- {CYN}{ADMIN_LINK}{RST}")
    print(f"\n  🌐 ဘရောက်ဇာတွင် တိုက်ရိုက်ဖွင့်နေသည်...")
    print(f"  {YEL}မဖွင့်လှစ်ပါက အပေါ်ကလင့်ခ်ကို ကူးယူဖွင့်ပါ{RST}\n")
    
    # Termux/Android တွင် တိုက်ရိုက်ဖွင့်ရန်
    try:
        import subprocess
        subprocess.run(['am', 'start', '-a', 'android.intent.action.VIEW', '-d', ADMIN_LINK], check=False)
    except:
        try:
            os.system(f"termux-open-url '{ADMIN_LINK}'")
        except:
            pass
    
    input(f"{CYN}ပြန်ရန် Enter နှိပ်ပါ...{RST}")

# SOURCES
SOURCES = [
    ("V2Nodes", "https://www.v2nodes.com/subscriptions/country/all/?key=72BEE427C23A1AF", "b64"),
    ("Shadowmere B64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("Shadowmere Plain", "https://shadowmere.xyz/api/sub/", "txt"),
    ("V2Ray-Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
    ("Epodon VLESS", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Splitted-By-Protocol/vless.txt", "txt"),
    ("Epodon SS", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/ss.txt", "txt"),
]

FAV_FILE = "favorites.txt"
favorites = []

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

def get_net():
    try:
        import subprocess
        r = subprocess.run(['ip','link'], capture_output=True, text=True, timeout=3)
        return "WiFi" if 'wlan' in r.stdout.lower() or 'wlp' in r.stdout.lower() else "Mobile Data"
    except: return "Unknown"

def get_country_flag(name):
    flags = {"SG": "SG", "US": "US", "JP": "JP", "KR": "KR", "HK": "HK",
             "TW": "TW", "UK": "UK", "GB": "GB", "DE": "DE", "NL": "NL",
             "CA": "CA", "AU": "AU", "IN": "IN", "TH": "TH", "MY": "MY"}
    for code in flags.keys():
        if code in name.upper():
            return code
    return "??"

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
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
        if ms < 40: return True, ms, "Very Fast", 5
        if ms < 70: return True, ms, "Excellent", 5
        if ms < 100: return True, ms, "Good", 4
        if ms < 180: return True, ms, "Normal", 3
        if ms < 300: return True, ms, "Slow", 2
        return True, ms, "Too Slow", 1
    except: return False, 9999, "Offline", 0

def load_all():
    vless, ss = [], []
    print("\n" + PUR + "="*50 + RST)
    print(PUR + "|" + RST + "  Loading sources..." + " "*34 + PUR + "|" + RST)
    print(PUR + "-"*50 + RST)
    success_count = 0
    for idx, (name, url, fmt) in enumerate(SOURCES, 1):
        print(f"  [{idx}/{len(SOURCES)}] {name:<22}", end=" ")
        text = fetch(url)
        if text:
            keys = parse(text, fmt)
            v_count = sum(1 for k in keys if k["type"]=="VLESS")
            s_count = sum(1 for k in keys if k["type"]=="SS")
            if v_count + s_count > 0:
                print(f"{GRN}OK{RST}  VLESS:{v_count}  SS:{s_count}")
                vless.extend([k for k in keys if k["type"]=="VLESS"])
                ss.extend([k for k in keys if k["type"]=="SS"])
                success_count += 1
            else:
                print(f"{YEL}No keys found{RST}")
        else:
            print(f"{RED}Failed to connect{RST}")
    print(PUR + "="*50 + RST)
    print(f"{GRN}Loaded {success_count}/{len(SOURCES)} sources successfully{RST}")
    load_favorites()
    return vless, ss

def scan_and_show(keys, title, count=10):
    if not keys:
        print(f"\n{YEL}Load sources first using [1]!{RST}")
        time.sleep(1.5)
        return
    results = []
    print(f"\n{PUR}{title}{RST}\n")
    total = len(keys)
    for i, k in enumerate(keys, 1):
        pct = int(i/total*100)
        print(f"  Scanning... {pct}%", end="\r")
        ok, ms, lvl, sc = ping_test(k["url"])
        if ok and sc > 0:
            k.update({"ms":ms,"lvl":lvl,"sc":sc})
            results.append(k)
    results.sort(key=lambda x:x["ms"])
    top = results[:count]
    print("\n\n")
    for idx, s in enumerate(top, 1):
        stars = "*"*s["sc"] + "o"*(5-s["sc"])
        print(f"  {s['flag']} [{idx}] {BD}{s['name']}{RST}")
        print(f"     Ping: {CYN}{s['ms']}ms{RST}  Level: {s['lvl']}  {stars}")
        print(f"     {s['url'][:65]}...")
        print()
    input(f"{CYN}Press Enter to continue...{RST}")

def best_for_me(all_keys):
    if not all_keys:
        print(f"\n{YEL}Load sources first using [1]!{RST}")
        time.sleep(1.5)
        return
    print(f"\n{PUR}Finding best server for your {get_net()}...{RST}\n")
    results = []
    for k in all_keys:
        ok, ms, lvl, sc = ping_test(k["url"])
        if ok and sc > 0:
            k.update({"ms":ms,"lvl":lvl,"sc":sc})
            results.append(k)
    results.sort(key=lambda x:(x["ms"], -x["sc"]))
    if results:
        best = results[0]
        clear()
        print(PUR + "="*50 + RST)
        print(PUR + "|" + RST + "    ✅ BEST SERVER FOR YOU    " + PUR + "|" + RST)
        print(PUR + "-"*50 + RST)
        print(f"  Network: {CYN}{get_net()}{RST}")
        print(f"  Country: {best['flag']}")
        print(f"  Name   : {BD}{best['name']}{RST}")
        print(f"  Ping   : {GRN}{best['ms']} ms{RST}")
        print(f"  Level  : {best['lvl']}")
        print()
        print(f"  FULL KEY:")
        print(f"  {best['url']}")
        print(PUR + "="*50 + RST)
        print(f"  [S] Save to Favorites   [X] Back")
        ch = input("\nChoose -> ").upper()
        if ch == "S":
            if best["url"] not in favorites:
                favorites.append(best["url"])
                save_favorites()
                print(f"{PINK}Saved to favorites! ❤️{RST}")
            else:
                print(f"{YEL}Already in favorites{RST}")
            time.sleep(1.5)
    else:
        print(f"{RED}No working server found{RST}")
        time.sleep(1.5)

def show_favorites():
    clear()
    print(f"{PINK}❤️  My Favorites ({len(favorites)}){RST}\n")
    if not favorites:
        print(f"{DIM}Empty. Scan servers and save with [S]{RST}")
    else:
        for i, url in enumerate(favorites, 1):
            name = url.split("#")[-1][:40] if "#" in url else f"Server {i}"
            print(f"  [{i}] {name}")
            print(f"      {url[:60]}...")
            print()
    input(f"{CYN}Press Enter to go back...{RST}")

def main():
    vless, ss = [], []
    while True:
        clear()
        total = len(vless) + len(ss)
        print(PUR + "="*50 + RST)
        print(PUR + "|" + RST + "   VPN Key Finder - Full Edition   " + PUR + "|" + RST)
        print(PUR + "-"*50 + RST)
        print(PUR + "|" + RST + f"  Network: {get_net()}" + " "*30 + PUR + "|" + RST)
        print(PUR + "|" + RST + f"  VLESS: {BLU}{len(vless)}{RST}   SS: {ORG}{len(ss)}{RST}   Total: {WHT}{total}{RST}" + " "*12 + PUR + "|" + RST)
        print(PUR + "-"*50 + RST)
        print(PUR + "|" + RST + "      MAIN MENU" + " "*34 + PUR + "|" + RST)
        print(PUR + "-"*50 + RST)
        print(PUR + "|" + RST + "  [1] Load All Sources" + " "*32 + PUR + "|" + RST)
        print(PUR + "|" + RST + "  [2] VLESS - Top 10 Fastest" + " "*28 + PUR + "|" + RST)
        print(PUR + "|" + RST + "  [3] SS - Top 10 Fastest" + " "*32 + PUR + "|" + RST)
        print(PUR + "|" + RST + "  [4] 🏆 Best Server For My Network" + " "*22 + PUR + "|" + RST)
        print(PUR + "|" + RST + "  [5] ❤️  My Favorites" + " "*34 + PUR + "|" + RST)
        print(PUR + "|" + RST + "  [6] 📘 Admin ဆီဆက်သွယ်ရန်" + " "*26 + PUR + "|" + RST)
        print(PUR + "|" + RST + "  [0] Exit" + " "*42 + PUR + "|" + RST)
        print(PUR + "="*50 + RST)
        ch = input("\nChoose -> ")
        
        if ch == "0":
            clear()
            print(f"\n{GRN}Goodbye! 👋{RST}\n")
            break
        elif ch == "1":
            vless, ss = load_all()
            input(f"\n{CYN}Press Enter to return to menu...{RST}")
        elif ch == "2":
            scan_and_show(vless, "VLESS Servers - Fastest First", 10)
        elif ch == "3":
            scan_and_show(ss, "SS Servers - Fastest First", 10)
        elif ch == "4":
            best_for_me(vless + ss)
        elif ch == "5":
            show_favorites()
        elif ch == "6":
            open_admin_link()
        else:
            print(f"\n{RED}Invalid choice! Try again{RST}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("\n\nExited.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}Error: {e}{RST}")
        input("Press Enter to exit...")
