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
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )
        with urllib.request.urlopen(req) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:40]}")
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
                keys.append({"proto": "VLESS", "key": line, "ping": "--ms", "ms": 9999})
            elif line.startswith("ss://"):
                keys.append({"proto": "SS", "key": line, "ping": "--ms", "ms": 9999})
    except Exception as e:
        print(f"   Parse error: {e}")
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
            print(f"{i:02d} | ❌ | {k['key'][:60]}...")
    print(f"\n{G}✅ Working: {len(working)}/{len(keys)}{RS}")
    return working

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
    
    print("Loading from sources...\n")
    for name, url, fmt in sources:
        print(f"🔄 {name}...", end=" ", flush=True)
        text = get_text(url)
        if text:
            keys = parse_keys(text, fmt)
            vless_count = sum(1 for k in keys if k["proto"] == "VLESS")
            ss_count = sum(1 for k in keys if k["proto"] == "SS")
            print(f"{G}OK ✓{RS}  VLESS:{vless_count}  SS:{ss_count}")
            for k in keys:
                if k["proto"] == "VLESS":
                    all_vless.append(k)
                else:
                    all_ss.append(k)
        else:
            print(f"{R}SKIP ✗{RS}")
    
    print(f"\n{Y}─── Summary ───{RS}")
    print(f"VLESS: {G}{len(all_vless)}{RS} keys")
    print(f"SS:    {G}{len(all_ss)}{RS} keys\n")
    
    if len(all_vless) == 0 and len(all_ss) == 0:
        print(f"{R}⚠️  No keys found from any source{RS}")
        input("Press Enter to exit")
        return
    
    while True:
        clear()
        print("===== VPN KEY FINDER =====")
        print(f"  VLESS: {len(all_vless)} keys")
        print(f"  SS:    {len(all_ss)} keys")
        print()
        print("  1. Show VLESS + Ping")
        print("  2. Show SS + Ping")
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
            show_and_check(all_vless)
            input("\nBack → Enter")
        elif c == "2":
            if not all_ss:
                print(f"\n{R}No SS keys{RS}")
                input("Back → Enter")
                continue
            show_and_check(all_ss)
            input("\nBack → Enter")
        else:
            print(f"\n{R}Wrong choice{RS}")
            input("OK → Enter")

if __name__ == "__main__":
    main()
    
