#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, base64, os, socket, time, datetime

G = "\033[92m"
Y = "\033[93m"
R = "\033[91m"
CY = "\033[96m"
M = "\033[95m"
BD = "\033[1m"
RS = "\033[0m"

FAVORITES_FILE = "favorites.txt"
ALL_KEYS_FILE = "all_keys.txt"

def clear_screen():
    os.system("clear")

SOURCES = [
    ("Shadowmere B64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("Argh73 Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
]

def check_ping(host, port, timeout=0.8):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        start = time.time()
        s.connect((host, int(port)))
        ms = int((time.time() - start) * 1000)
        s.close()
        if ms < 150:
            return f"{G}{ms}ms ✅ Good{RS}", ms, True
        elif ms < 300:
            return f"{Y}{ms}ms ⚡ Normal{RS}", ms, True
        else:
            return f"{CY}{ms}ms 📍 Slow{RS}", ms, True
    except:
        return None, 9999, False

def extract_host_port(key):
    try:
        from urllib.parse import urlparse
        p = urlparse(key)
        if p.hostname and p.port:
            return p.hostname, p.port
    except:
        pass
    try:
        import re
        m = re.search(r"@([^:]+):(\d+)", key)
        if m:
            return m.group(1), int(m.group(2))
    except:
        pass
    return None, None

def get_text(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.read().decode("utf-8", errors="ignore")
    except:
        return None

def parse(text, fmt):
    keys = []
    if not text:
        return keys
    try:
        if fmt == "b64":
            text = base64.b64decode(text).decode("utf-8", errors="ignore")
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            proto = None
            if line.startswith("vless://"): proto = "VLESS"
            elif line.startswith("ss://"): proto = "SS"
            elif line.startswith("vmess://"): proto = "VMESS"
            elif line.startswith("trojan://"): proto = "TROJAN"
            if proto:
                name = "Server"
                if "#" in line:
                    name = line.split("#")[-1]
                    try:
                        from urllib.parse import unquote
                        name = unquote(name)
                    except:
                        pass
                keys.append({
                    "proto": proto,
                    "name": name,
                    "key": line,
                    "ping_ms": "--",
                    "ping_str": "--",
                    "is_alive": False
                })
    except:
        pass
    return keys

def get_proto_file(proto):
    return f"alive_{proto.lower()}.txt"

def save_alive_by_proto(proto, keys):
    try:
        with open(get_proto_file(proto), "w", encoding="utf-8") as f:
            f.write(f"Protocol: {proto}\n")
            f.write("Updated: " + str(datetime.datetime.now()) + "\n")
            f.write("Total Alive: " + str(len(keys)) + "\n\n")
            for k in keys:
                f.write(f"{k['name']} | {k.get('ping_str', '--')}\n")
                f.write(k["key"] + "\n\n")
        return True
    except:
        return False

def load_alive_by_proto(proto):
    keys = []
    fname = get_proto_file(proto)
    if not os.path.exists(fname):
        return keys
    try:
        with open(fname, "r", encoding="utf-8") as f:
            lines = f.readlines()
        current_key = None
        for line in lines:
            line = line.strip()
            if not line or line.startswith("Protocol:") or line.startswith("Updated:") or line.startswith("Total Alive:"):
                continue
            if "://" in line:
                if current_key:
                    keys.append(current_key)
                current_key = {
                    "proto": proto,
                    "name": "Saved Server",
                    "key": line,
                    "ping_ms": "--",
                    "ping_str": "--",
                    "is_alive": False
                }
            elif "|" in line and current_key:
                parts = line.split(" | ", 1)
                if len(parts) >= 1:
                    current_key["name"] = parts[0]
        if current_key:
            keys.append(current_key)
    except:
        pass
    return keys

def save_to_file(keys, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("Updated: " + str(datetime.datetime.now()) + "\n")
            f.write("Total: " + str(len(keys)) + "\n\n")
            for k in keys:
                f.write(f"{k['proto']} | {k['name']} | {k.get('ping_str', '--')}\n")
                f.write(f"{k['key']}\n\n")
        return True
    except:
        return False

def load_favorites():
    favs = []
    if os.path.exists(FAVORITES_FILE):
        try:
            with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if "://" in line:
                        favs.append(line)
        except:
            pass
    return favs

def add_favorite(line):
    try:
        with open(FAVORITES_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        return True
    except:
        return False

def search_name(keys, kw):
    kw = kw.upper()
    return [k for k in keys if kw in k["name"].upper()]

def show(keys, title="Keys", limit=20):
    clear_screen()
    if not keys:
        print(f"\n{R}No keys found{RS}\n")
        input("Press Enter to go back")
        return
    print(f"\n{M}{BD}=== {title} ({len(keys)}) ==={RS}\n")
    display_count = min(limit, len(keys))
    for i, k in enumerate(keys[:display_count], 1):
        status = f"{G}✅ Working{RS}" if k.get("is_alive") else f"{R}❌ Not checked{RS}"
        print(f"{i:02d} | {k['proto']:6} | {k['name'][:40]}")
        print(f"    ⚡ Ping: {k.get('ping_str', '--')}  {status}")
        print(f"    🔑 Key: {k['key']}\n")
    if len(keys) > display_count:
        print(f"{Y}...and {len(keys)-display_count} more{RS}\n")
    input("Press Enter to go back")

def copy_key(key_text):
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set"], input=key_text.encode('utf-8'))
        print(f"{G}✅ Key copied to clipboard!{RS}\n")
    except:
        print(f"{Y}⚠️ Copy manually:{RS}\n{key_text}\n")
    input("Press Enter to go back")

def scan_by_proto(all_keys, proto):
    clear_screen()
    keys = [k for k in all_keys if k["proto"] == proto]
    if not keys:
        print(f"\n{R}No {proto} keys found{RS}\n")
        input("Press Enter to go back")
        return []
    
    print(f"\n{M}{BD}⚡ Checking {proto} keys...{RS}")
    print(f"{Y}Total: {len(keys)} keys{RS}\n")
    
    alive = []
    for i, k in enumerate(keys, 1):
        print(f"  [{i}/{len(keys)}] {k['name'][:25]}", end="\r")
        host, port = extract_host_port(k["key"])
        if not host or not port:
            continue
        ping_str, ms, is_alive = check_ping(host, port)
        if is_alive:
            k["ping_str"] = ping_str
            k["ping_ms"] = ms
            k["is_alive"] = True
            alive.append(k.copy())
    
    print(f"\n\n{G}{BD}✅ {proto} check complete{RS}")
    print(f"   Working: {G}{len(alive)}{RS} / {len(keys)}")
    
    if save_alive_by_proto(proto, alive):
        print(f"   {G}✅ Saved successfully{RS}")
    print()
    input("Press Enter to go back")
    return alive

def rescan_saved(proto):
    clear_screen()
    keys = load_alive_by_proto(proto)
    if not keys:
        print(f"\n{Y}⚠️ No saved {proto} keys yet{RS}\n")
        input("Press Enter to go back")
        return []
    
    print(f"\n{M}{BD}⚡ Re-checking saved {proto} keys...{RS}")
    print(f"{Y}Total: {len(keys)} keys{RS}\n")
    
    updated = []
    for i, k in enumerate(keys, 1):
        print(f"  [{i}/{len(keys)}] {k['name'][:25]}", end="\r")
        host, port = extract_host_port(k["key"])
        if not host or not port:
            continue
        ping_str, ms, is_alive = check_ping(host, port)
        if is_alive:
            k["ping_str"] = ping_str
            k["ping_ms"] = ms
            k["is_alive"] = True
            updated.append(k.copy())
    
    print(f"\n\n{G}{BD}✅ Re-check complete{RS}")
    print(f"   Still working: {G}{len(updated)}{RS} / {len(keys)}")
    
    if save_alive_by_proto(proto, updated):
        print(f"   {G}✅ Updated and saved{RS}")
    print()
    input("Press Enter to go back")
    return updated

def show_best(keys, proto):
    clear_screen()
    if not keys:
        keys = load_alive_by_proto(proto)
    if not keys:
        print(f"\n{R}❌ Please scan first{RS}\n")
        input("Press Enter to go back")
        return
    sorted_keys = sorted(keys, key=lambda x: x["ping_ms"] if x["ping_ms"] != "--" else 9999)
    print(f"\n{M}{BD}🏆 Best 10 {proto} Keys (Lowest Ping){RS}\n")
    for i, k in enumerate(sorted_keys[:10], 1):
        print(f"{i:02d}. {k['name'][:45]}")
        print(f"    ⚡ Ping: {k['ping_str']}")
        print(f"    🔑 Key: {k['key']}")
        print()
    input("Press Enter to go back")

def key_management_menu(all_keys):
    while True:
        clear_screen()
        print(f"\n{M}{BD}🔑 Key Management{RS}")
        print("================================")
        print(" [1] 📋 View All Keys")
        print(" [2] 🔍 Search by Name/Country")
        print(" [3] ⚡ View Only VLESS Keys")
        print(" [4] 📡 View Only SS Keys")
        print(" [5] ⭐ View Favorites")
        print(" [6] 💾 Save Key to Favorites")
        print(" [7] 📋 Copy from Favorites")
        print(" [8] 📤 Export All to File")
        print(" [0] ⬅️ Back to Main Menu")
        print("================================")
        
        c = input(f"\nSelect option → {RS}").strip()
        
        if c == "0":
            break
        elif c == "1":
            show(all_keys, "All Keys")
        elif c == "2":
            clear_screen()
            kw = input("Enter keyword/country → ").strip()
            result = search_name(all_keys, kw)
            show(result, f"Search: '{kw}'")
        elif c == "3":
            vless = [k for k in all_keys if k["proto"] == "VLESS"]
            show(vless, "VLESS Keys")
        elif c == "4":
            ss_list = [k for k in all_keys if k["proto"] == "SS"]
            show(ss_list, "SS Keys")
        elif c == "5":
            clear_screen()
            favs = load_favorites()
            if not favs:
                print(f"\n{Y}⚠️ No favorites yet{RS}\n")
            else:
                print(f"\n{M}{BD}⭐ Favorites ({len(favs)}){RS}\n")
                for i, line in enumerate(favs, 1):
                    print(f"{i}. {line[:60]}...")
                    print(f"   🔑 {line}")
                    print()
            input("Press Enter to go back")
        elif c == "6":
            clear_screen()
            n = input("Key number to favorite → ").strip()
            try:
                idx = int(n) - 1
                if 0 <= idx < len(all_keys):
                    if add_favorite(all_keys[idx]["key"]):
                        print(f"\n{G}✅ Added to favorites!{RS}\n")
                    else:
                        print(f"\n{R}❌ Failed{RS}\n")
                else:
                    print(f"\n{R}Invalid number{RS}\n")
            except:
                print(f"\n{R}Invalid input{RS}\n")
            input("Press Enter to go back")
        elif c == "7":
            clear_screen()
            favs = load_favorites()
            if not favs:
                print(f"\n{Y}⚠️ No favorites yet{RS}\n")
                input("Press Enter to go back")
                continue
            print(f"\n{M}{BD}Favorites:{RS}\n")
            for i, line in enumerate(favs, 1):
                print(f" [{i}] {line[:50]}...")
            sel = input("\nNumber to copy → ").strip()
            try:
                idx = int(sel) - 1
                if 0 <= idx < len(favs):
                    copy_key(favs[idx])
            except:
                print(f"\n{R}Invalid input{RS}\n")
                input("Press Enter to go back")
        elif c == "8":
            if save_to_file(all_keys, ALL_KEYS_FILE):
                print(f"\n{G}✅ Saved to file: {ALL_KEYS_FILE}{RS}\n")
            else:
                print(f"\n{R}❌ Failed to save{RS}\n")
            input("Press Enter to go back")
        else:
            print(f"\n{R}Invalid option{RS}\n")

def main():
    clear_screen()
    print(f"""{M}{BD}
=========================================
     🚀 VPN KEY FINDER
     ✅ VLESS / SS Separated
     ✅ Ping + Key Displayed Together
     ✅ Screen Clears Automatically
========================================={RS}""")
    
    all_keys = []
    seen = set()
    
    print(f"\n{Y}Loading data...{RS}\n")
    for name, url, fmt in SOURCES:
        print(f"  {name}...", end=" ")
        text = get_text(url)
        ks = parse(text, fmt)
        if ks:
            for k in ks:
                if k["key"] not in seen:
                    seen.add(k["key"])
                    all_keys.append(k)
            print(f"{G}OK {len(ks)} keys{RS}")
        else:
            print(f"{R}Failed{RS}")
    
    vless_keys = [k for k in all_keys if k["proto"] == "VLESS"]
    ss_keys = [k for k in all_keys if k["proto"] == "SS"]
    
    print(f"\n{CY}📊 Total Keys:{RS}")
    print(f"   VLESS: {G}{len(vless_keys)}{RS}")
    print(f"   SS:    {G}{len(ss_keys)}{RS}")
    print()
    
    while True:
        clear_screen()
        print(f"{M}{BD}📌 MAIN MENU{RS}")
        print("================================")
        print("  🟦 VLESS Keys")
        print("   [1] 📋 View All VLESS")
        print("   [2] ⚡ Scan & Save VLESS")
        print("   [3] 🔄 Rescan Saved VLESS")
        print("   [4] 🏆 Best VLESS (Lowest Ping)")
        print()
        print("  🟧 SS Keys")
        print("   [5] 📋 View All SS")
        print("   [6] ⚡ Scan & Save SS")
        print("   [7] 🔄 Rescan Saved SS")
        print("   [8] 🏆 Best SS (Lowest Ping)")
        print()
        print("  🔑 Management")
        print("   [9] 🔑 Key Management Menu")
        print()
        print("   [0] ❌ Exit")
        print("================================")
        
        c = input(f"\nSelect option → {RS}").strip()
        
        if c == "0":
            clear_screen()
            print("\n👋 Goodbye!")
            break
        elif c == "1":
            show(vless_keys, "VLESS Keys")
        elif c == "2":
            _ = scan_by_proto(all_keys, "VLESS")
        elif c == "3":
            _ = rescan_saved("VLESS")
        elif c == "4":
            show_best([], "VLESS")
        elif c == "5":
            show(ss_keys, "SS Keys")
        elif c == "6":
            _ = scan_by_proto(all_keys, "SS")
        elif c == "7":
            _ = rescan_saved("SS")
        elif c == "8":
            show_best([], "SS")
        elif c == "9":
            key_management_menu(all_keys)
        else:
            print(f"\n{R}Invalid option{RS}\n")
            input("Press Enter to continue")

if __name__ == "__main__":
    main()
            
