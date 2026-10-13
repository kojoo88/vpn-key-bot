#!/usr/bin/env python3
import urllib.request, json, base64, os, sys

API_URL = "https://shadowmere.xyz/api/sub/"
VERSION = "1.0"

def clear():
    os.system("clear")

def get_data():
    try:
        r = urllib.request.Request(
            API_URL,
            headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
        )
        with urllib.request.urlopen(r, timeout=15) as res:
            return json.loads(res.read().decode())
    except Exception as e:
        return []

def make_key(s):
    try:
        info = f"{s['method']}:{s['password']}"
        b64 = base64.b64encode(info.encode()).decode().rstrip("=")
        return f"ss://{b64}@{s['server']}:{s['server_port']}#{s['remarks']}"
    except:
        return "❌ မထုတ်နိုင်ပါ"

def print_header():
    clear()
    print("╔════════════════════════════════════════════╗")
    print("║      🔑  VPN KEY GENERATOR TOOL            ║")
    print("║        github.com/kojoo88/vpn-key-bot      ║")
    print("║             Version " + VERSION + "                        ║")
    print("╚════════════════════════════════════════════╝")
    print()
    print("*" * 48)
    print()

def main():
    data = get_data()
    
    while True:
        print_header()
        if not data:
            print("  ⚠️  ဆာဗာဒေတာ ရယူ၍မရပါ။ ကွန်နက်ရှင်စစ်ဆေးပါ။")
            print()
        print("  [ နိုင်ငံရွေးချယ်ရန် ]")
        print()
        print("  [ 1 ]  📋 ALL  —  နိုင်ငံအားလုံး")
        print("  [ 2 ]  🇺🇸 USA  —  အမေရိကန်")
        print("  [ 3 ]  🇸🇬 SGP  —  စင်ကာပူ")
        print("  [ 4 ]  🇭🇰 HKG  —  ဟောင်ကောင်")
        print("  [ 5 ]  🇯🇵 JPN  —  ဂျပန်")
        print("  [ 6 ]  🇰🇷 KOR  —  ကိုရီးယား")
        print("  [ 7 ]  🇿🇦 ZAF  —  တောင်အာဖရိက")
        print("  [ 0 ]  ❌ EXIT —  ပရိုဂရမ်မှထွက်ရန်")
        print()
        print("*" * 48)
        choice = input("  ➤ ရွေးချယ်မှု: ").strip()
        
        if choice == "0":
            print_header()
            print("  ✅ အသုံးပြုသည့်အတွက် ကျေးဇူးတင်ပါသည်!")
            print("  👋 ပရိုဂရမ်မှ ထွက်လိုက်ပါပြီ။")
            print()
            sys.exit(0)
        
        filtered = []
        title = ""
        
        if choice == "1":
            filtered = data
            title = "📋 နိုင်ငံအားလုံး"
        elif choice == "2":
            filtered = [s for s in data if "us" in s.get("remarks","").lower()]
            title = "🇺🇸 United States"
        elif choice == "3":
            filtered = [s for s in data if any(v in s.get("remarks","").lower() for v in ["sg", "singapore"])]
            title = "🇸🇬 Singapore"
        elif choice == "4":
            filtered = [s for s in data if any(v in s.get("remarks","").lower() for v in ["hk", "hong"])]
            title = "🇭🇰 Hong Kong"
        elif choice == "5":
            filtered = [s for s in data if any(v in s.get("remarks","").lower() for v in ["jp", "japan"])]
            title = "🇯🇵 Japan"
        elif choice == "6":
            filtered = [s for s in data if any(v in s.get("remarks","").lower() for v in ["kr", "korea"])]
            title = "🇰🇷 Korea"
        elif choice == "7":
            filtered = [s for s in data if any(v in s.get("remarks","").lower() for v in ["za", "south africa"])]
            title = "🇿🇦 South Africa"
        else:
            print_header()
            print("  ❌ မှားယွင်းသောရွေးချယ်မှု။ ထပ်မံကြိုးစားပါ။")
            input("\n  ပြန်မီနူးသို့ရန် Enter နှိပ်ပါ...")
            continue
        
        print_header()
        print(f"  📌 {title}")
        print(f"  🔄 စုစုပေါင်း: {len(filtered)} Server")
        print()
        if not filtered:
            print("  ⚠️  ဤနိုင်ငံအတွက် Server မတွေ့ပါ။")
        else:
            print("  ─" * 24)
            for idx, srv in enumerate(filtered, 1):
                name = srv.get("remarks", f"Server {idx}")
                key = make_key(srv)
                print(f"  [{idx}] {name}")
                print(f"      {key}")
                print()
            print("  ─" * 24)
        input("\n  မီနူးသို့ပြန်ရန် Enter နှိပ်ပါ...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("\n\n  ⚠️  ပရိုဂရမ်မှ ထွက်လိုက်ပါသည်။")
        sys.exit(0)
        
