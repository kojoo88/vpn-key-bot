#!/usr/bin/env python3
import urllib.request, base64, os, socket, time

G = "\033[92m"
Y = "\033[93m"
R = "\033[91m"
RS = "\033[0m"

def clear(): os.system("clear")

def ping_test(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.8)
        start = time.time()
        s.connect((host, int(port)))
        ms = int((time.time() - start) * 1000)
        s.close()
        if ms < 150: return f"{G}{ms}ms ✅{RS}", ms
        elif ms < 300: return f"{Y}{ms}ms ⚡{RS}", ms
        else: return f"{R}{ms}ms 📍{RS}", ms
    except: return None, 9999

def get_text(url):
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return None

def parse_keys(text, fmt):
    keys = []
    if not text: return keys
    try:
        if fmt == "b64":
            text = base64.b64decode(text).decode("utf-8", errors="ignore")
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"): continue
            if line.startswith("vless://"):
                keys.append({"proto": "VLESS", "key": line, "ping": "--ms", "ms": 9999, "alive": False})
            elif line.startswith("ss://"):
                keys.append({"proto": "SS", "key": line, "ping": "--ms", "ms": 9999, "alive": False})
    except: pass
    return keys

def check_alive_and_sort(keys):
    """အရင်အကုန်စစ် → အလုပ်လုပ်တဲ့ဟာပဲရွေး → Ping အနည်းဆုံးအစီအစဉ်စီပြီး ပြန်ပေး"""
    clear()
    total = len(keys)
    print(f"Checking {total} keys...\n")
    alive = []
    
    for i, k in enumerate(keys, 1):
        print(f"  [{i}/{total}] Checking...", end="\r")
        try:
            from urllib.parse import urlparse
            p = urlparse(k["key"])
            ping_str, ms = ping_test(p.hostname, p.port)
            if ping_str:
                k["ping"] = ping_str
                k["ms"] = ms
                k["alive"] = True
                alive.append(k)
        except: pass
    
    alive_sorted = sorted(alive, key=lambda x: x["ms"])
    return alive_sorted, total

def display_results(alive, total):
    clear()
    print(f"{G}✅ Done!{RS}  Working: {len(alive)}/{total}\n")
    if not alive:
        print(f"{R}No working keys found{RS}\n")
        return
    
    print(f"⚡ Fastest first:\n")
    for i, k in enumerate(alive, 1):
        print(f"{i:02d} | {k['ping']} | {k['key']}")
    print()

def main():
    clear()
    print("===== VPN KEY FINDER =====\n")
    
    sources = [
        ("Shadowmere", "https://shadowmere.xyz/api/b64sub/", "b64"),
        ("V2Ray-Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
        ("V2Nodes", "https://www.v2nodes.com/subscriptions/country/all/?key=72BEE427C23A1AF", "b64"),
    ]
    
    all_vless = []
    all_ss = []
    
    print("Loading keys...\n")
    for name, url, fmt in sources:
        text = get_text(url)
        if text:
            keys = parse_keys(text, fmt)
            for k in keys:
                if k["proto"] == "VLESS": all_vless.append(k)
                else: all_ss.append(k)
    
    print(f"VLESS: {len(all_vless)} loaded")
    print(f"SS:    {len(all_ss)} loaded\n")
    input("Ready → Enter")
    
    while True:
        clear()
        print("===== VPN KEY FINDER =====")
        print(f"  VLESS: {len(all_vless)}  |  SS: {len(all_ss)}")
        print()
        print("  1. Check VLESS → Show Working + Ping")
        print("  2. Check SS   → Show Working + Ping")
        print("  0. Exit")
        print("===========================")
        
        c = input("\nChoose → ").strip()
        
        if c == "0":
            print("\n👋 Bye!")
            break
        elif c == "1":
            if not all_vless:
                print(f"\n{R}No VLESS keys{RS}")
                input("Back → Enter")
                continue
            alive, total = check_alive_and_sort(all_vless)
            display_results(alive, total)
            input("Back → Enter")
        elif c == "2":
            if not all_ss:
                print(f"\n{R}No SS keys{RS}")
                input("Back → Enter")
                continue
            alive, total = check_alive_and_sort(all_ss)
            display_results(alive, total)
            input("Back → Enter")
        else:
            print(f"\n{R}Wrong choice{RS}")
            input("OK → Enter")

if __name__ == "__main__":
    main()
        
