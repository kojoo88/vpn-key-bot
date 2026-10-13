#!/usr/bin/env python3
import urllib.request, urllib.error, json, base64, os, sys, socket, time

VERSION = "2.4"

API_LIST = {
    "1": ("Shadowmere JSON", "https://shadowmere.xyz/api/sub/", "json"),
    "2": ("Shadowmere Base64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    "3": ("VLESS List", "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/vless.txt", "txt")
}

def clear(): os.system("clear")

def test_ping(host, port, timeout=2):
    try:
        if not host:
            return "⚠️ စမ်းသပ်၍မရ"
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, int(port)))
        sock.close()
        ms = round((time.time() - start) * 1000)
        if result == 0:
            return f"✅ အလုပ်လုပ်နေ  {ms}ms"
        else:
            return "❌ မရနိုင်ပါ"
    except Exception:
        return "⚠️ စမ်းသပ်၍မရ"

def fetch_json(url):
    try:
        r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(r, timeout=15) as res:
            return json.loads(res.read().decode())
    except Exception:
        return None

def fetch_b64(url):
    try:
        r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(r, timeout=15) as res:
            data = res.read().decode().strip()
            return base64.b64decode(data).decode().splitlines()
    except Exception:
        return None

def fetch_txt(url):
    try:
        r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(r, timeout=15) as res:
            content = res.read().decode().strip()
            try:
                decoded = base64.b64decode(content).decode('utf-8')
                return [line.strip() for line in decoded.splitlines() if line.strip() and not line.startswith('#')]
            except:
                return [line.strip() for line in content.splitlines() if line.strip() and not line.startswith('#')]
    except Exception:
        return None

def make_ss_key(s):
    try:
        info = f"{s['method']}:{s['password']}"
        b64 = base64.b64encode(info.encode()).decode().rstrip("=")
        return f"ss://{b64}@{s['server']}:{s['server_port']}#{s['remarks']}"
    except:
        return "❌ အမှား"

def extract_host_port(link):
    try:
        if link.startswith("ss://"):
            part = link.split("@")[1].split("#")[0]
            host, port = part.split(":")
            return host, int(port)
        elif "://" in link:
            after = link.split("//")[1]
            if "@" in after:
                after = after.split("@")[1]
            if ":" in after and "?" in after:
                host = after.split(":")[0]
                port = after.split(":")[1].split("?")[0]
                return host, int(port)
            elif ":" in after:
                host, port = after.split(":")
                return host, int(port.split("/")[0])
            else:
                return after.split("/")[0], 443
    except:
        return None, None
    return None, None

def header():
    clear()
    print("\033[92m")
    print("╔══════════════════════════════════════════════════════╗")
    print("║           🔑   V P N   K E Y   T O O L                 ║")
    print(f"║               Version {VERSION}  •  Real Working Only               ║")
    print("╚══════════════════════════════════════════════════════╝")
    print("\033[93m")
    print("  [*] Status    : Online ✅")
    print("  [*] Source    : Shadowmere + VLESS")
    print("  [*] Filter    : Showing only working servers")
    print("\033[90m" + "─" * 54 + "\033[0m")
    print()

def api_menu():
    while True:
        header()
        print("  🔌 API အရင်းအမြစ် ရွေးချယ်ပါ")
        print("  " + "─" * 30)
        for k, v in API_LIST.items():
            print(f"  [{k}] {v[0]}")
        print("  [0]  ❌ ထွက်ရန်")
        print()
        ch = input("  ➤ ရွေးချယ်မှု: ").strip()
        
        if ch == "0":
            clear()
            print("  ✅ ပရိုဂရမ်မှ ထွက်လိုက်ပါပြီ။")
            sys.exit(0)
        if ch in API_LIST:
            return API_LIST[ch]

def country_menu(data, api_type):
    while True:
        header()
        print("  🌍 နိုင်ငံရွေးချယ်ပါ")
        print("  " + "─" * 30)
        print("  [1] အားလုံး      [5] 🇯🇵 JP Japan")
        print("  [2] 🇺🇸 US       [6] 🇰🇷 KR Korea")
        print("  [3] 🇸🇬 SG       [7] 🇿🇦 ZA SA")
        print("  [4] 🇭🇰 HK       [8] 🔙 API ပြန်ရွေးရန်")
        print("  [0] ❌ ထွက်ရန်")
        print()
        ch = input("  ➤ ရွေးချယ်မှု: ").strip()
        
        if ch == "0":
            clear()
            print("  ✅ ပရိုဂရမ်မှ ထွက်လိုက်ပါပြီ။")
            sys.exit(0)
        if ch == "8":
            return
        if not data:
            input("  ❌ ဒေတာမရှိပါ။ ပြန်ကြိုးစားပါ။ Enter...")
            continue
        
        filters = {
            "1": "",
            "2": "us",
            "3": "sg singapore",
            "4": "hk hong",
            "5": "jp japan",
            "6": "kr korea",
            "7": "za south africa"
        }
        
        if ch not in filters:
            continue
        
        kw = filters[ch]
        results = []
        
        if api_type == "json":
            for s in data:
                rmk = s.get("remarks", "").lower()
                if not kw or any(k in rmk for k in kw.split()):
                    results.append(s)
        else:
            if not kw:
                results = data
            else:
                results = [line for line in data if any(k in line.lower() for k in kw.split())]
        
        clear()
        title = {v:k for k,v in filters.items()}.get(kw, "အားလုံး")
        print("\033[92m" + "─" * 55 + "\033[0m")
        print(f"  📌 {title}  —  စစ်ဆေးနေသည်... စောင့်ပါ")
        print("\033[92m" + "─" * 55 + "\033[0m")
        
        working = []
        for idx, item in enumerate(results, 1):
            if api_type == "json":
                host = item.get("server", "")
                port = item.get("server_port", 0)
                name = item.get("remarks", f"Server {idx}")
                key = make_ss_key(item)
            else:
                key = item
                host, port = extract_host_port(item)
                name = f"Server {idx}"
            
            status = test_ping(host, port) if host else "⚠️ စမ်းသပ်၍မရ"
            
            if "✅" in status:
                working.append((idx, name, key, status))
                print(f"\n  🟢 {name}")
                print(f"     {status}")
                print(f"     {key}")
        
        print("\n\033[92m" + "─" * 55 + "\033[0m")
        print(f"  ✅ စုစုပေါင်း: {len(working)} / {len(results)} လုံး အလုပ်လုပ်နေသည်")
        print("\033[92m" + "─" * 55 + "\033[0m")
        input("  မီနူးသို့ပြန်ရန် Enter...")

def main():
    while True:
        name, url, dtype = api_menu()
        header()
        print(f"  🔄 ဒေတာရယူနေသည်...")
        
        data = None
        if dtype == "json":
            data = fetch_json(url)
        elif dtype == "b64":
            data = fetch_b64(url)
        elif dtype == "txt":
            data = fetch_txt(url)
        
        if not data:
            input("  ❌ ဒေတာရယူ၍မရပါ။ လင့်ခ်သေခြင်း သို့မဟုတ် အင်တာနက်ပြဿနာ။ Enter...")
            continue
        
        while True:
            country_menu(data, dtype)
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("\n\n  ✅ ထွက်လိုက်ပါပြီ။")
        sys.exit(0)
    
