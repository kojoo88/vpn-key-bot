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
        return urllib.request.urlopen(
            urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
            timeout=10
        ).read().decode("utf-8", errors="ignore")
    except: return None

def parse_keys(text, fmt):
    keys = []
    if not text: return keys
    if fmt == "b64": text = base64.b64decode(text).decode("utf-8", errors="ignore")
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"): continue
        if line.startswith("vless://"):
            keys.append({"proto": "VLESS", "key": line, "ping": "--ms", "ms": 9999})
        elif line.startswith("ss://"):
            keys.append({"proto": "SS", "key": line, "ping": "--ms", "ms": 9999})
    return keys

def show_and_check(keys):
    clear()
    print(f"Total: {len(keys)} keys\n")
    working = []
    for i, k in enumerate(keys, 1):
        try:
            from urllib.parse import urlparse
            p = urlparse(k["key"])
            ping_str, ms = ping_test(p.hostname, p.port)
            if ping_str:
                k["ping"] = ping_str
                k["ms"] = ms
                working.append(k)
            print(f"{i:02d} | {k['ping']} | {k['key']}")
        except:
            print(f"{i:02d} | ❌ | {k['key']}")
    print(f"\n{G}✅ Working: {len(working)}/{len(keys)}{RS}")
    return working

def main():
    clear()
    print("Loading keys...\n")
    all_keys = []
    for url, fmt in [
        ("https://shadowmere.xyz/api/b64sub/", "b64"),
        ("https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
    ]:
        ks = parse_keys(get_text(url), fmt)
        if ks: all_keys.extend(ks)
    
    vless = [k for k in all_keys if k["proto"] == "VLESS"]
    ss = [k for k in all_keys if k["proto"] == "SS"]
    
    while True:
        clear()
        print("==== VPN KEY FINDER ====")
        print("  1. VLESS + Ping")
        print("  2. SS + Ping")
        print("  0. Exit")
        print("========================")
        
        c = input("\nChoose → ").strip()
        
        if c == "0":
            print("\nBye!")
            break
        elif c == "1":
            if not vless:
                print(f"\n{R}No VLESS keys found{RS}")
                input("Back → Enter")
                continue
            show_and_check(vless)
            input("\nBack → Enter")
        elif c == "2":
            if not ss:
                print(f"\n{R}No SS keys found{RS}")
                input("Back → Enter")
                continue
            show_and_check(ss)
            input("\nBack → Enter")
        else:
            print(f"\n{R}Wrong choice{RS}")
            input("OK → Enter")

if __name__ == "__main__":
    main()
    
