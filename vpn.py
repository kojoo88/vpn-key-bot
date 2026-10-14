#!/usr/bin/env python3
import urllib.request, base64, os

G = "\033[92m"
R = "\033[91m"
Y = "\033[93m"
RS = "\033[0m"

def clear(): os.system("clear")

def test_link(url, name):
    print(f"Testing {name}... ", end="", flush=True)
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )
        with urllib.request.urlopen(req) as r:
            text = r.read().decode("utf-8", errors="ignore")
        print(f"{G}OK ✓{RS}")
        return text
    except Exception as e:
        print(f"{R}FAIL ✗{RS}")
        return None

def extract_keys(text, fmt):
    keys = []
    if not text: return keys
    try:
        if fmt == "b64":
            text = base64.b64decode(text).decode("utf-8", errors="ignore")
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("vless://"):
                keys.append(("VLESS", line))
            elif line.startswith("ss://"):
                keys.append(("SS", line))
    except: pass
    return keys

def main():
    clear()
    print("===== VPN KEY CHECKER =====\n")
    
    sources = [
        ("Shadowmere", "https://shadowmere.xyz/api/b64sub/", "b64"),
        ("V2Ray-Vault", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Splitted-By-Protocol/vless.txt", "txt"),
        ("SS-Configs", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Splitted-By-Protocol/ss.txt", "txt"),
    ]
    
    all_vless = []
    all_ss = []
    
    for name, url, fmt in sources:
        text = test_link(url, name)
        if text:
            keys = extract_keys(text, fmt)
            vless_count = sum(1 for t,_ in keys if t=="VLESS")
            ss_count = sum(1 for t,_ in keys if t=="SS")
            print(f"   → VLESS: {vless_count}, SS: {ss_count}\n")
            for t,k in keys:
                if t=="VLESS": all_vless.append(k)
                else: all_ss.append(k)
        else:
            print(f"   → Could not load\n")
    
    print(f"{Y}Summary:{RS} VLESS: {len(all_vless)}, SS: {len(all_ss)}\n")
    
    if len(all_vless)==0 and len(all_ss)==0:
        print(f"{R}No keys found from any source{RS}")
        print("\nPossible reasons:")
        print("• Internet connection")
        print("• Links are blocked in your network")
        print("• API source is down")
        input("\nPress Enter to exit")
        return
    
    while True:
        clear()
        print("===== VPN KEY FINDER =====")
        print(f"  VLESS: {len(all_vless)} keys")
        print(f"  SS:    {len(all_ss)} keys")
        print()
        print("  1 = Show VLESS")
        print("  2 = Show SS")
        print("  0 = Exit")
        print("===========================")
        
        c = input("\nChoose → ").strip()
        
        if c == "0":
            print("\nBye!")
            break
        elif c == "1" and all_vless:
            clear()
            print(f"VLESS Keys ({len(all_vless)}):\n")
            for i, k in enumerate(all_vless[:20], 1):
                print(f"{i}. {k}")
            if len(all_vless) > 20:
                print(f"\n... and {len(all_vless)-20} more")
            input("\nBack → Enter")
        elif c == "2" and all_ss:
            clear()
            print(f"SS Keys ({len(all_ss)}):\n")
            for i, k in enumerate(all_ss[:20], 1):
                print(f"{i}. {k}")
            if len(all_ss) > 20:
                print(f"\n... and {len(all_ss)-20} more")
            input("\nBack → Enter")
        else:
            print(f"\n{R}No keys or wrong choice{RS}")
            input("OK → Enter")

if __name__ == "__main__":
    main()
        
