#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, base64, os, re, datetime

G = "\033[92m"
B = "\033[94m"
Y = "\033[93m"
R = "\033[91m"
CY = "\033[96m"
RS = "\033[0m"

FAVORITES_FILE = "favorites.txt"
ALL_KEYS_FILE = "all_keys.txt"

def clear():
    os.system("clear")

SOURCES = [
    ("Shadowmere B64", "https://shadowmere.xyz/api/b64sub/", "b64"),
]

def get_text(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
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
            if line.startswith("vless://"):
                proto = "VLESS"
            elif line.startswith("ss://"):
                proto = "SS"
            elif line.startswith("vmess://"):
                proto = "VMESS"
            elif line.startswith("trojan://"):
                proto = "TROJAN"
            if proto:
                name = "Unknown"
                if "#" in line:
                    name = line.split("#")[-1]
                    try:
                        from urllib.parse import unquote
                        name = unquote(name)
                    except:
                        pass
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                keys.append({
                    "proto": proto,
                    "name": name,
                    "key": line,
                    "added_time": now
                })
    except:
        pass
    return keys

def save_to_file(keys, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("Updated: " + str(datetime.datetime.now()) + "\n")
            f.write("Total Keys: " + str(len(keys)) + "\n\n")
            for k in keys:
                f.write(k["proto"] + " | " + k["name"] + "\n")
                f.write(k["key"] + "\n\n")
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
                    if line.startswith("ss://") or line.startswith("vless://"):
                        favs.append(line)
        except:
            pass
    return favs

def add_favorite(key_line):
    try:
        with open(FAVORITES_FILE, "a", encoding="utf-8") as f:
            f.write(key_line + "\n")
        return True
    except:
        return False

def search_by_country(keys, keyword):
    result = []
    keyword = keyword.upper()
    for k in keys:
        if keyword in k["name"].upper():
            result.append(k)
    return result

def show(keys, title="ကီးများ"):
    if not keys:
        print()
        print(R + "❌ ကီးမတွေ့ပါ" + RS)
        print()
        input("ပြန်ရန် Enter နှိပ်ပါ")
        return
    
    print()
    print(CY + "=== " + title + " (" + str(len(keys)) + " ခု) ===" + RS)
    print()
    for i, k in enumerate(keys[:10], 1):
        print(str(i) + ". " + k["proto"] + " | " + k["name"])
        print("   📅 " + k.get("added_time", "အသိမရှိ"))
        print("   🔑 " + k["key"])
        print()
    
    if len(keys) > 10:
        print(Y + "... နောက်ထပ် " + str(len(keys)-10) + " ခု ရှိပါသည်" + RS)
        print()
    
    input("ပြန်ရန် Enter နှိပ်ပါ")
    print()

def main():
    clear()
    print("=" * 50)
    print("      VPN KEY FINDER")
    print("=" * 50)
    print()
    
    all_keys = []
    seen = set()
    
    print(Y + "ဒေတာဖတ်နေသည်..." + RS)
    print()
    
    for name, url, fmt in SOURCES:
        print(name + " ... ", end="")
        text = get_text(url)
        ks = parse(text, fmt)
        if ks:
            for k in ks:
                if k["key"] not in seen:
                    seen.add(k["key"])
                    all_keys.append(k)
            print(G + "OK — " + str(len(ks)) + " ခု" + RS)
        else:
            print(R + "မရရှိ" + RS)
    
    print()
    print(CY + "စုစုပေါင်း ကီး " + str(len(all_keys)) + " ခု ရရှိပြီးသား" + RS)
    print()
    
    while True:
        print("=" * 50)
        print("📌 မီနူး")
        print("=" * 50)
        print("  1. 📋 ကီးအားလုံးကို ပြပါ")
        print("  2. 📋 VLESS သီးသန့်ပြပါ")
        print("  3. 📋 SS သီးသန့်ပြပါ")
        print("  4. 🔍 နိုင်ငံအလိုက် ရှာပါ")
        print("  5. 💾 ဖိုင်အဖြစ် သိမ်းပါ")
        print("  6. ⭐ အကြိုက်ဆုံးများကို ကြည့်ပါ")
        print("  7. ➕ ကီးတစ်ခုကို အကြိုက်ဆုံးထဲ ထည့်ပါ")
        print("  8. 📡 Subscribe လင့်ခ်ကို ပြပါ")
        print("  0. ❌ ထွက်ပါ")
        print("=" * 50)
        
        choice = input("\nရွေးပါ → ").strip()
        
        if choice == "0":
            print()
            print("👋 ပါသေး...")
            break
        
        elif choice == "1":
            show(all_keys, "ကီးအားလုံး")
        
        elif choice == "2":
            vless_keys = [k for k in all_keys if k["proto"] == "VLESS"]
            show(vless_keys, "VLESS ကီးများ")
        
        elif choice == "3":
            ss_keys = [k for k in all_keys if k["proto"] == "SS"]
            show(ss_keys, "SS ကီးများ")
        
        elif choice == "4":
            keyword = input("ရှာမည့်စာလုံး သို့မဟုတ် နိုင်ငံအမည် ရိုက်ထည့်ပါ → ").strip()
            found = search_by_country(all_keys, keyword)
            show(found, "'" + keyword + "' ဖြင့် ရှာဖွေမှုရလဒ်")
        
        elif choice == "5":
            if save_to_file(all_keys, ALL_KEYS_FILE):
                print()
                print(G + "✅ " + ALL_KEYS_FILE " အဖြစ် သိမ်းဆည်းပြီးသား" + RS)
                print()
            else:
                print()
                print(R + "❌ သိမ်းဆည်း၍မရပါ" + RS)
                print()
            input("ပြန်ရန် Enter နှိပ်ပါ")
        
        elif choice == "6":
            fav_keys = load_favorites()
            print()
            if not fav_keys:
                print(Y + "⭐ အကြိုက်ဆုံး မရှိသေးပါ" + RS)
            else:
                print(CY + "=== အကြိုက်ဆုံး ကီးများ ===" + RS)
                print()
                for i, k in enumerate(fav_keys, 1):
                    print(str(i) + ". " + k)
            print()
            input("ပြန်ရန် Enter နှိပ်ပါ")
        
        elif choice == "7":
            idx_str = input("အကြိုက်ဆုံးထဲ ထည့်မည့် ကီးနံပါတ် → ").strip()
            try:
                idx = int(idx_str) - 1
                if 0 <= idx < len(all_keys):
                    if add_favorite(all_keys[idx]["key"]):
                        print()
                        print(G + "✅ အကြိုက်ဆုံးထဲ ထည့်ပြီးသား" + RS)
                        print()
                    else:
                        print()
                        print(R + "❌ မအောင်မြင်ပါ" + RS)
                        print()
                else:
                    print()
                    print(R + "❌ နံပါတ်မှားနေပါတယ်" + RS)
                    print()
            except:
                print()
                print(R + "❌ သင့်လျော်တဲ့နံပါတ်မဟုတ်ပါ" + RS)
                print()
            input("ပြန်ရန် Enter နှိပ်ပါ")
        
        elif choice == "8":
            print()
            print(CY + "📡 Subscribe လင့်ခ်:" + RS)
            print("https://shadowmere.xyz/api/b64sub/")
            print()
            print(Y + "💡 အသုံးပြုနည်း- V2RayNG/NekoBox → + → Subscribe → URL မှာ ကူးထည့်ပါ" + RS)
            print()
            input("ပြန်ရန် Enter နှိပ်ပါ")
        
        else:
            print()
            print(R + "❌ ရွေးချယ်မှုမှားနေပါတယ်" + RS)
            print()

if __name__ == "__main__":
    main()
        
