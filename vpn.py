#!/usr/bin/env python3
# Ultimate VPN Key Finder - Dream Edition v4.0 (Fixed)
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

def clear(): os.system("clear")
def h(): return "-" * 60

# SOURCES
SOURCES = [
    ("V2Nodes", "https://www.v2nodes.com/subscriptions/country/all/?key=72BEE427C23A1AF", "b64"),
    ("Shadowmere", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("Shadowmere API", "https://shadowmere.xyz/api/sub/", "txt"),
    ("V2Ray-Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
    ("V2Ray-Configs VLESS", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Splitted-By-Protocol/vless.txt", "txt"),
    ("V2Ray-Configs SS", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Splitted-By-Protocol/ss.txt", "txt"),
]

FAV_FILE = "favorites.txt"
HIST_FILE = "history.txt"
favorites = []
history = []

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

def add_history(key):
    global history
    entry = datetime.datetime.now().strftime("%H:%M") + "|" + key["name"] + "|" + key["url"]
    history.insert(0, entry)
    history = history[:50]
    with open(HIST_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(history))

def get_net():
    try:
        import subprocess
        r = subprocess.run(['ip','link'], capture_output=True, text=True, timeout=3)
        return "WiFi" if 'wlan' in r.stdout.lower() or 'wlp' in r.stdout.lower() else "Mobile Data"
    except: return "Unknown"

def get_country_flag(name):
    flags = {
        "SG": "SG", "US": "US", "JP": "JP", "KR": "KR", "HK": "HK",
        "TW": "TW", "UK": "UK", "GB": "GB", "DE": "DE", "NL": "NL",
        "CA": "CA", "AU": "AU", "IN": "IN", "TH": "TH", "MY": "MY"
    }
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
        if ms < 40: return True, ms, "Very Fast", 5, "S", "DIA"
        if ms < 70: return True, ms, "Excellent", 5, "A", "STAR"
        if ms < 100: return True, ms, "Good", 4, "B", "OK"
        if ms < 180: return True, ms, "Normal", 3, "C", "NORM"
        if ms < 300: return True, ms, "Slow", 2, "D", "SLOW"
        return True, ms, "Too Slow", 1, "F", "X"
    except: return False, 9999, "Offline", 0, "X", "X"

def load_all():
    vless, ss = [], []
    print("\n" + PUR + "="*60 + RST)
    print(PUR + "|" + RST + "  Loading sources..." + " "*44 + PUR + "|" + RST)
    print(PUR + "-"*60 + RST)
    success_count = 0
    for idx, (name, url, fmt) in enumerate(SOURCES, 1):
        print(PUR + "|" + RST + f"  [{idx}/{len(SOURCES)}] {name:<24}", end=" ")
        text = fetch(url)
        if text:
            keys = parse(text, fmt)
            v_count = sum(1 for k in keys if k["type"]=="VLESS")
            s_count = sum(1 for k in keys if k["type"]=="SS")
            total = v_count + s_count
            if total > 0:
                print(GRN + "OK" + RST + f"  VLESS:{v_count:>4}  SS:{s_count:>4}  Total:{total:>4}")
                vless.extend([k for k in keys if k["type"]=="VLESS"])
                ss.extend([k for k in keys if k["type"]=="SS"])
                success_count += 1
            else:
                print(YEL + "No keys found" + RST)
        else:
            print(RED + "Failed" + RST)
    print(PUR + "="*60 + RST)
    print(f"\n{GRN}Loaded {success_count}/{len(SOURCES)} sources{RST}")
    load_favorites()
    return vless, ss

def show_card(s, idx=None, show_url=True):
    stars = "*"*s["sc"] + "o"*(5-s["sc"])
    idx_str = f"[{idx:02d}] " if idx else ""
    print(f"  {s['flag']} {idx_str}{BD}{s['name']}{RST}")
    print(f"     Level: {s['rank']} Class  {s['icon']} {s['lvl']}  {stars}")
    print(f"     Ping : {CYN}{s['ms']}{RST} ms")
    if show_url:
        print(f"     Key  : {s['url'][:75]}...")
    print()

def save_results(results, filename="results.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("="*60 + "\n")
        f.write("VPN Key Finder - Results\n")
        f.write("="*60 + "\n")
        f.write(f"Updated : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Network : {get_net()}\n")
        f.write(f"Total   : {len(results)} servers\n")
        f.write("="*60 + "\n\n")
        for s in results:
            f.write(f"# {s['flag']} {s['name']} | Ping: {s['ms']}ms | {s['rank']}\n")
            f.write(f"{s['url']}\n\n")
    print(f"{GRN}Saved to {filename}{RST}")

def scan(keys, title, min_score=0, max_ping=9999, sort_by="ping"):
    if not keys:
        print(f"\n{YEL}Load sources first [1]{RST}")
        time.sleep(1.5)
        return []
    results = []
    print(f"\n{PUR}{title}{RST}\n")
    total = len(keys)
    for i, k in enumerate(keys, 1):
        pct = int(i/total*100)
        bar = "#"*(pct//5) + "-"*(20 - pct//5)
        print(f"  Progress: [{bar}] {pct:>3}%  ({i}/{total})", end="\r")
        ok, ms, lvl, sc, rank, icon = ping_test(k["url"])
        if ok and sc >= min_score and ms <= max_ping:
            k.update({"ms":ms,"lvl":lvl,"sc":sc,"rank":rank,"icon":icon})
            results.append(k)
    if sort_by == "ping":
        results.sort(key=lambda x:x["ms"])
    elif sort_by == "score":
        results.sort(key=lambda x:(-x["sc"], x["ms"]))
    elif sort_by == "name":
        results.sort(key=lambda x:x["name"])
    print("\n\n")
    return results

def show_top_n(keys, proto, n=10):
    results = scan(keys, f"Finding best {n} {proto} servers...", sort_by="ping")
    if not results: return
    top = results[:n]
    print(f"{PUR}Top {n} {proto} Servers{RST}\n")
    for i, s in enumerate(top, 1):
        show_card(s, i)
    save_results(top, f"top{n}_{proto}.txt")
    input(f"\n{CYN}Press Enter to go back...{RST}")

def manage_favorites(all_keys):
    while True:
        clear()
        print(f"{PINK}Favorites ({len(favorites)} items){RST}\n")
        if not favorites:
            print(f"{DIM}Empty. Scan and save keys.{RST}")
        else:
            for i, url in enumerate(favorites, 1):
                preview = url.split("#")[-1][:35] if "#" in url else f"Server {i}"
                flag = get_country_flag(preview)
                print(f"  [{i}] {flag} {preview}")
                print(f"      {url[:65]}...")
                print()
        print(PUR + "-"*30 + RST)
        print("  [A] Export all to file")
        print("  [C] Copy selected")
        print("  [D] Delete one")
        print("  [R] Clear all")
        print("  [X] Back")
        ch = input("\nChoose -> ").upper()
        if ch == "X": break
        elif ch == "A" and favorites:
            with open("my_favorites.txt", "w", encoding="utf-8") as f:
                f.write("="*50 + "\n")
                f.write("My Favorite VPN Keys\n")
                f.write("="*50 + "\n\n")
                f.write("\n\n".join(favorites))
            print(f"{GRN}Saved to my_favorites.txt{RST}")
            time.sleep(1.5)
        elif ch == "C" and favorites:
            try:
                idx = int(input("Number -> ")) - 1
                if 0 <= idx < len(favorites):
                    print("\nKey:")
                    print(f"  {favorites[idx]}")
                    input(f"\n{CYN}Press Enter...{RST}")
            except: print(f"{RED}Invalid input{RST}")
        elif ch == "D" and favorites:
            try:
                idx = int(input("Delete number -> ")) - 1
                if 0 <= idx < len(favorites):
                    favorites.pop(idx)
                    save_favorites()
                    print(f"{RED}Deleted{RST}")
                    time.sleep(1)
            except: print(f"{RED}Invalid input{RST}")
        elif ch == "R":
            if input("Clear all? (Y/N) -> ").upper() == "Y":
                favorites.clear()
                save_favorites()
                print(f"{RED}Cleared{RST}")
                time.sleep(1)

def instant_best(all_keys):
    results = scan(all_keys, "Finding best server for you...", min_score=3, sort_by="score")
    if not results: return
    best = results[0]
    clear()
    print(PUR + "="*60 + RST)
    print(PUR + "|" + RST + "        BEST SERVER FOR YOU" + " "*26 + PUR + "|" + RST)
    print(PUR + "-"*60 + RST)
    show_card(best)
    print(PUR + "-"*60 + RST)
    print(PUR + "|" + RST + "  [S] Save   [C] Copy Key   [X] Back" + " "*24 + PUR + "|" + RST)
    print(PUR + "="*60 + RST)
    ch = input("\nChoose -> ").upper()
    if ch == "S":
        if best["url"] not in favorites:
            favorites.append(best["url"])
            save_favorites()
            add_history(best)
            print(f"{PINK}Saved!{RST}")
        else:
            print(f"{YEL}Already saved{RST}")
        time.sleep(1)
    elif ch == "C":
        print("\nFull Key:")
        print(f"  {best['url']}")
        input(f"\n{CYN}Press Enter...{RST}")

def search_by_country(all_keys):
    clear()
    print(f"{CYN}Search by Country{RST}\n")
    print("  SG=Singapore  US=USA  JP=Japan  HK=HongKong")
    print("  KR=Korea   TW=Taiwan UK=UK     TH=Thailand")
    print("  Leave empty and Enter for ALL servers")
    code = input("\nCountry code -> ").upper().strip()
    filtered = all_keys
    if code:
        filtered = [k for k in all_keys if code in k["name"].upper()]
        if not filtered:
            print(f"{RED}No servers found for {code}{RST}")
            time.sleep(2)
            return
    results = scan(filtered, f"Checking {len(filtered)} servers...", sort_by="ping")
    if not results: return
    print(f"{GRN}Found {len(results)} working servers{RST}\n")
    show_count = min(len(results), 15)
    for i, s in enumerate(results[:show_count], 1):
        show_card(s, i)
    if len(results) > show_count:
        print(f"{DIM}... and {len(results) - show_count} more in file{RST}\n")
    save_results(results, f"country_{code or 'all'}.txt")
    input(f"\n{CYN}Press Enter...{RST}")

def share_menu():
    clear()
    print(f"{PUR}Share Tools{RST}\n")
    if not os.path.exists("results.txt"):
        print(f"{YEL}Run a scan first{RST}")
        time.sleep(2)
        return
    with open("results.txt", "r", encoding="utf-8") as f:
        content = f.read()
    print("  [1] Telegram")
    print("  [2] Facebook")
    print("  [3] WhatsApp")
    print("  [4] Daily Update")
    print("  [5] Keys only")
    print("  [0] Back")
    ch = input("\nChoose -> ")
    output = ""
    today = datetime.date.today()
    if ch == "1":
        output = f"VPN Keys - {today}\nNetwork: {get_net()}\n\n{content}\n\n#VPN #Free"
    elif ch == "2":
        output = f"Free VPN Keys - {today}\n\n{content}\n\n#VPN #FreeInternet"
    elif ch == "3":
        output = f"VPN Keys {today}\n\n{content}"
    elif ch == "4":
        output = f"Daily VPN Update - {today}\n\n{content}"
    elif ch == "5":
        lines = [l for l in content.split("\n") if l.strip() and not l.startswith("=") and not l.startswith("#") and "VPN Key" not in l and "Updated" not in l and "Network" not in l and "Total" not in l]
        output = "\n".join(lines)
    elif ch == "0":
        return
    else:
        print(f"{RED}Invalid choice{RST}")
        time.sleep(1)
        return
    with open("share_ready.txt", "w", encoding="utf-8") as f:
        f.write(output)
    print(f"\n{GRN}Saved to share_ready.txt{RST}")
    print("-"*50)
    print(output)
    print("-"*50)
    input(f"\n{CYN}Press Enter...{RST}")

def random_pick(all_keys):
    if not all_keys:
        print(f"\n{YEL}Load sources first [1]{RST}")
        time.sleep(1.5)
        return
    clear()
    print(f"{PUR}Random Picker{RST}\n")
    print(f"  From {len(all_keys)} total keys...")
    time.sleep(1)
    for _ in range(5):
        temp = random.choice(all_keys)
        print(f"  -> {temp['flag']} {temp['name'][:30]}", end="\r")
        time.sleep(0.15)
    picked = random.choice(all_keys)
    print("\n\n")
    ok, ms, lvl, sc, rank, icon = ping_test(picked["url"])
    picked.update({"ms":ms,"lvl":lvl,"sc":sc,"rank":rank,"icon":icon})
    print(PUR + "="*60 + RST)
    print(PUR + "|" + RST + "        YOUR LUCKY PICK" + " "*30 + PUR + "|" + RST)
    print(PUR + "-"*60 + RST)
    show_card(picked)
    print(PUR + "-"*60 + RST)
    print(PUR + "|" + RST + "  [R] Pick Again   [S] Save   [C] Copy   [X] Back" + " "*18 + PUR + "|" + RST)
    print(PUR + "="*60 + RST)
    ch = input("\nChoose -> ").upper()
    if ch == "R":
        random_pick(all_keys)
    elif ch == "S":
        if picked["url"] not in favorites:
            favorites.append(picked["url"])
            save_favorites()
            print(f"{PINK}Saved!{RST}")
        else:
            print(f"{YEL}Already saved{RST}")
        time.sleep(1)
    elif ch == "C":
        print(f"\n{picked['url']}")
        input(f"\n{CYN}Press Enter...{RST}")

def show_stats(vless, ss):
    clear()
    total = len(vless) + len(ss)
    today = datetime.date.today()
    now = datetime.datetime.now()
    print(f"{PUR}Statistics{RST}\n")
    print(f"  Date    : {today}")
    print(f"  Time    : {now.strftime('%H:%M:%S')}")
    print(f"  Network : {CYN}{get_net()}{RST}")
    print(f"  Sources : {GRN}{len(SOURCES)}{RST}")
    print(f"  VLESS   : {BLU}{len(vless):>4}{RST}  {round(len(vless)/total*100,1) if total else 0}%")
    print(f"  SS      : {ORG}{len(ss):>4}{RST}  {round(len(ss)/total*100,1) if total else 0}%")
    print(f"  Total   : {WHT}{total:>4}{RST}")
    print(f"  Favorites: {PINK}{len(favorites):>4}{RST}")
    print(f"  History : {len(history):>4}")
    print(f"\n{PUR}Files:{RST}")
    for f in ["results.txt", "favorites.txt", "history.txt"]:
        exists = f"{GRN}Exists{RST}" if os.path.exists(f) else f"{DIM}Not found{RST}"
        size = f"({os.path.getsize(f)} bytes)" if os.path.exists(f) else ""
        print(f"  {f:<20} {exists} {size}")
    input(f"\n{CYN}Press Enter...{RST}")

def cleanup_menu():
    while True:
        clear()
        print(f"{PUR}Cleanup Tools{RST}\n")
        print("  [1] Delete all result files")
        print("  [2] Clear history")
        print("  [3] Clear favorites")
        print("  [4] Clear daily files")
        print("  [0] Back")
        ch = input("\nChoose -> ")
        if ch == "0": break
        elif ch == "1":
            files = ["results.txt", "share_ready.txt", "share_key.txt", "my_favorites.txt"]
            cnt = 0
            for f in files:
                if os.path.exists(f):
                    os.remove(f)
                    cnt += 1
            print(f"{GRN}Deleted {cnt} files{RST}")
            time.sleep(1.5)
        elif ch == "2":
            if os.path.exists(HIST_FILE):
                os.remove(HIST_FILE)
                history.clear()
                print(f"{GRN}History cleared{RST}")
            else:
                print(f"{YEL}No history{RST}")
            time.sleep(1.5)
        elif ch == "3":
            if input("Clear all favorites? (Y/N) -> ").upper() == "Y":
                favorites.clear()
                save_favorites()
                print(f"{GRN}Cleared{RST}")
            time.sleep(1.5)
        elif ch == "4":
            cnt = 0
            for f in os.listdir("."):
                if f.startswith("daily_") or f.endswith("_servers.txt") or f.endswith("_keys.txt"):
                    os.remove(f)
                    cnt += 1
            print(f"{GRN}Cleaned {cnt} files{RST}")
            time.sleep(1.5)

def main():
    vless, ss = [], []
    while True:
        clear()
        net = get_net()
        total_keys = len(vless) + len(ss)
        print(PUR + "="*60 + RST)
        print(PUR + "|" + RST + "   VPN Key Finder - Dream Edition v4.0" + " "*24 + PUR + "|" + RST)
        print(PUR + "-"*60 + RST)
        print(PUR + "|" + RST + f"  Network : {net}" + " "*(52-len(net)) + PUR + "|" + RST)
        print(PUR + "|" + RST + f"  Sources : {len(SOURCES)}" + " "*52 + PUR + "|" + RST)
        print(PUR + "|" + RST + f"  VLESS   : {BLU}{len(vless)}{RST}" + " "*(53-len(str(len(vless)))) + PUR + "|" + RST)
        print(PUR + "|" + RST + f"  SS      : {ORG}{len(ss)}{RST}" + " "*(53-len(str(len(ss)))) + PUR + "|" + RST)
        print(PUR + "|" + RST + f"  Total   : {WHT}{total_keys}{RST}" + " "*(53-len(str(total_keys))) + PUR + "|" + RST)
        print(PUR + "|" + RST + f"  Favorites: {PINK}{len(favorites)}{RST}" + " "*(53-len(str(len(favorites)))) + PUR + "|" + RST)
        print(PUR + "-"*60 + RST)
        print(PUR + "|" + RST + "  MAIN MENU" + " "*47 + PUR + "|" + RST)
        print(PUR + "-"*60 + RST)
        print(PUR + "|" + RST + "  [01]  Load All Sources" + " "*38 + PUR + "|" + RST)
        print(PUR + "|" + RST + "  [02]  VLESS Top 15" + " "*42 + PUR + "|" + RST)
        print(PUR + "|" + RST + "  [03]  SS Top 15" + " "*46 + PUR + "|" + RST)
        print(PUR + "|" + RST + "  [04]  Best For My Network" + " "*34 + PUR + "|" + RST)
        print(PUR + "|" + RST + "  [05]  Random Pick" + " "*40 + PUR + "|" + RST)
        print(PUR + "|" + RST + "  [06]  Search By Country" + " "*36 + PUR + "|" + RST)
        print(PUR + "|" + RST + "  [07]  Manage Favorites" + " "*36 + PUR + "|" + RST)
        print(PUR + "|" + RST + "  [08]  Share Tools" + " "*40 + PUR + "|" + RST)
        print(PUR + "|" + RST + "  [09]  Statistics" + " "*42 + PUR + "|" + RST)
        print(PUR + "|" + RST + "  [10]  Cleanup" + " "*44 + PUR + "|" + RST)
        print(PUR + "|" + RST + "  [00]  Exit" + " "*50 + PUR + "|" + RST)
        print(PUR + "="*60 + RST)
        ch = input("\nChoose -> ").strip().zfill(2)
        
        if ch == "00":
            clear()
            print("\n" + PUR + "Thanks for using! Goodbye." + RST + "\n")
            break
        elif ch == "01":
            vless, ss = load_all()
            input(f"\n{CYN}Press Enter...{RST}")
        elif ch == "02":
            show_top_n(vless, "VLESS", 15)
        elif ch == "03":
            show_top_n(ss, "SS", 15)
  
