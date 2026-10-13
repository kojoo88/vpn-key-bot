#!/usr/bin/env python3
import urllib.request, urllib.error, json, base64, os, sys

VERSION = "2.2"

API_LIST = {
    "1": ("Shadowmere JSON", "https://shadowmere.xyz/api/sub/", "json"),
    "2": ("Shadowmere Base64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    "3": ("VLESS List", "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/vless.txt", "txt")
}

def clear(): os.system("clear")

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

def header():
    clear()
    print("─" * 50)
    print(f"     🔑 VPN KEY TOOL  v{VERSION}")
    print("─" * 50)
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
        print("─" * 55)
        print(f"  📌 {title}  —  စုစုပေါင်း {len(results)} လုံး")
        print("─" * 55)
        
        if not results:
            print("  ❌ ဤနိုင်ငံအတွက် မတွေ့ပါ")
        else:
            for idx, item in enumerate(results, 1):
                if api_type == "json":
                    name = item.get("remarks", f"Server {idx}")
                    key = make_ss_key(item)
                    print(f"\n  {idx}. {name}")
                    print(f"     {key}")
                else:
                    print(f"\n  {idx}. {item}")
        
        print("\n" + "─" * 55)
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
            input("  ❌ ဒေတာရယူ၍မရပါ။ လင့်ခ်သေခြင်း သို့မဟုတ် အင်တာနက်ပြဿနာဖြစ်နိုင်ပါသည်။ Enter...")
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
                
