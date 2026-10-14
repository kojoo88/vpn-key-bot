#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, base64, os

G = "\033[92m"
B = "\033[94m"
Y = "\033[93m"
R = "\033[91m"
CY = "\033[96m"
RS = "\033[0m"

def clear():
    os.system("clear")

# ✅ အလုပ်လုပ်နေတဲ့ နှစ်ခုသာ
SOURCES = [
    ("Shadowmere B64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("Argh73 Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
]

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
            if line.startswith("vless://"):
                proto = "VLESS"
            elif line.startswith("ss://"):
                proto = "SS"
            elif line.startswith("vmess://"):
                proto = "VMESS"
            elif line.startswith("trojan://"):
                proto = "TROJAN"
            if proto:
                name = "Server"
                if "#" in line:
                    name = line.split("#")[-1]
                    try:
                        from urllib.parse import unquote
                        name = unquote(name)
                    except:
                        pass
                keys.append({"proto": proto, "name": name, "key": line})
    except:
        pass
    return keys

def main():
    clear()
    print(CY + "🚀 VPN KEY FINDER" + RS)
    print("=" * 50 + "\n")
    
    all_keys = []
    seen = set()
    
    print(Y + "🔍 စစ်ဆေးနေသည်..." + RS + "\n")
    
    for name, url, fmt in SOURCES:
        print("  → " + name + " ...", end="\r")
        text = get_text(url)
        ks = parse(text, fmt)
        if ks:
            for k in ks:
                if k["key"] not in seen:
                    seen.add(k["key"])
                    all_keys.append(k)
            print("  " + G + "✅ " + name + " — " + str(len(ks)) + " keys" + RS)
        else:
            print("  " + R + "❌ " + name + " — မရရှိ" + RS)
    
    print("\n" + G + "✅ စုစုပေါင်း ကီး " + str(len(all_keys)) + " ခု ရရှိပြီးသား" + RS + "\n")
    
    while True:
        print(B + "📌 မီနူး" + RS)
        print("  1. အားလုံးပြပါ")
        print("  2. VLESS သီးသန့်ပြပါ")
        print("  3. SS သီးသန့်ပြပါ")
        print("  4. Subscribe လင့်ခ်များပြပါ")
        print("  0. ထွက်ပါ")
        
        choice = input("\nရွေးပါ → ").strip()
        
        if choice == "0":
            print(CY + "👋 ပါသေး..." + RS)
            break
        elif choice == "1":
            show(all_keys)
        elif choice == "2":
            show([k for k in all_keys if k["proto"] == "VLESS"])
        elif choice == "3":
            show([k for k in all_keys if k["proto"] == "SS"])
        elif choice == "4":
            print("\n" + G + "✅ Subscribe လင့်ခ်များ" + RS)
            for name, url, _ in SOURCES:
                print("  " + name + ": " + url)
            input("\nပြန်ရန် Enter နှိပ်ပါ")
        else:
            print(R + "❌ မှားနေပါတယ်" + RS + "\n")

def show(keys):
    if not keys:
        print(R + "❌ မတွေ့ပါ" + RS + "\n")
        return
    print("\n" + G + "✅ ကီး " + str(len(keys)) + " ခု" + RS + "\n")
    for i, k in enumerate(keys[:10], 1):
        print("  " + str(i) + ". " + k["proto"] + " | " + k["name"][:40])
        print("     " + k["key"] + "\n")
    if len(keys) > 10:
        print("... နောက်ထပ် " + str(len(keys)-10) + " ခု ရှိပါသည်\n")
    input("ပြန်ရန် Enter နှိပ်ပါ\n")

if __name__ == "__main__":
    main()
    
