#!/usr/bin/env python3
import urllib.request, json, base64, os

API_URL = "https://shadowmere.xyz/api/sub/"

def clear(): os.system("clear")

def get_data():
    try:
        r = urllib.request.Request(
            API_URL,
            headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
        )
        with urllib.request.urlopen(r, timeout=15) as res:
            return json.loads(res.read().decode())
    except:
        return []

def make_key(s):
    try:
        info = f"{s['method']}:{s['password']}"
        b64 = base64.b64encode(info.encode()).decode().rstrip("=")
        return f"ss://{b64}@{s['server']}:{s['server_port']}#{s['remarks']}"
    except:
        return "❌ အမှား"

def main():
    data = get_data()
    while True:
        clear()
        print("=" * 40)
        print("        🔑 VPN KEY TOOL")
        print("=" * 40)
        print()
        print("  နိုင်ငံရွေးရန်")
        print("  ───────────────────────")
        print("  1 = ALL  အားလုံး")
        print("  2 = 🇺🇸 US")
        print("  3 = 🇸🇬 Singapore")
        print("  4 = 🇭🇰 Hong Kong")
        print("  5 = 🇯🇵 Japan")
        print("  6 = 🇰🇷 Korea")
        print("  7 = 🇿🇦 South Africa")
        print("  0 = ထွက်ရန်")
        print()
        ch = input("👉 ရွေးပါ: ").strip()
        
        if ch == "0":
            print("👋 ပြီးပါပြီ")
            return
        
        filtered = []
        title = ""
        
        if ch == "1":
            filtered = data
            title = "အားလုံး"
        elif ch == "2":
            filtered = [s for s in data if "us" in s.get("remarks","").lower()]
            title = "🇺🇸 US"
        elif ch == "3":
            filtered = [s for s in data if any(v in s.get("remarks","").lower() for v in ["sg", "singapore"])]
            title = "🇸🇬 Singapore"
        elif ch == "4":
            filtered = [s for s in data if any(v in s.get("remarks","").lower() for v in ["hk", "hong"])]
            title = "🇭🇰 Hong Kong"
        elif ch == "5":
            filtered = [s for s in data if any(v in s.get("remarks","").lower() for v in ["jp", "japan"])]
            title = "🇯🇵 Japan"
        elif ch == "6":
            filtered = [s for s in data if any(v in s.get("remarks","").lower() for v in ["kr", "korea"])]
            title = "🇰🇷 Korea"
        elif ch == "7":
            filtered = [s for s in data if any(v in s.get("remarks","").lower() for v in ["za", "south africa"])]
            title = "🇿🇦 South Africa"
        
        clear()
        print(f"📌 {title}  ({len(filtered)} လုံး)")
        print("─" * 45)
        for i, s in enumerate(filtered, 1):
            print(f"{i}. {s['remarks']}")
            print(f"   {make_key(s)}\n")
        print("─" * 45)
        input("\nပြန်ရန် Enter...")

if __name__ == "__main__":
    main()
