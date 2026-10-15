#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import base64
import socket
import time
import os
import sys

# ================== COLORS ==================
CYN = "\033[38;5;80m"
GRN = "\033[38;5;114m"
YEL = "\033[38;5;221m"
RED = "\033[38;5;209m"
PUR = "\033[38;5;141m"
WHT = "\033[38;5;255m"
RST = "\033[0m"

def clear():
    os.system("clear")

# ================== CONFIG ==================
B64_URL = "https://shadowmere.xyz/api/b64sub/"

# ================== EXTRACT IP & PORT ==================
def extract_ip_port(url):
    try:
        if url.startswith("ss://"):
            body = url[5:]
        else:
            return None, None
        if "#" in body:
            body = body.split("#")[0]
        if "@" in body:
            host_port = body.split("@")[-1]
        else:
            return None, None
        if ":" in host_port:
            parts = host_port.rsplit(":", 1)
            host = parts[0].split("/")[0]
            port = int(parts[1].split("/")[0])
            return host, port
        return None, None
    except:
        return None, None

# ================== PING TEST ==================
def ping_server(host, port=443, timeout=2):
    if not host:
        return False, 999, "No IP", 0
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        start = time.perf_counter()
        s.connect((host, port))
        ms = int((time.perf_counter() - start) * 1000)
        s.close()
        if ms < 80:
            return True, ms, "Fast", 5
        elif ms < 150:
            return True, ms, "Good", 4
        elif ms < 250:
            return True, ms, "Normal", 3
        elif ms < 400:
            return True, ms, "Slow", 2
        else:
            return True, ms, "VerySlow", 1
    except:
        return False, 999, "Offline", 0

def get_country(text):
    codes = ["SG", "US", "JP", "KR", "HK", "TW", "UK", "DE", "NL", "CA", "AU", "IN", "TH", "MY", "FR", "IT", "ES", "BR", "FI", "SE", "PL", "CH", "IE", "AT", "BE", "DK", "NO", "NZ", "ZA", "RU"]
    text_upper = text.upper()
    for c in codes:
        if c in text_upper:
            return c
    return "??"

# ================== MAIN ==================
def main():
    while True:
        clear()
        print(PUR + "="*60 + RST)
        print(PUR + "|   🚀 SHADOWMERE B64 - KEY FINDER        |" + RST)
        print(PUR + "="*60 + RST)
        print(f"  [1] Load & Show All Keys")
        print(f"  [2] Load + Test Ping + Sort")
        print(f"  [0] Exit")
        print(PUR + "="*60 + RST)
        
        choice = input("\n  ရွေးပါ -> ")
        
        if choice == "0":
            print("\n  Bye! 👋\n")
            break
        
        elif choice == "1" or choice == "2":
            clear()
            print(f"{CYN}⏳ လင့်ခ်ဖွင့်နေသည်...{RST}")
            try:
                req = urllib.request.Request(B64_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
                with urllib.request.urlopen(req) as r:
                    b64_content = r.read().decode("utf-8", errors="ignore")
            except Exception as e:
                print(f"{RED}❌ လင့်ခ်မဖွင့်နိုင်ပါ: {e}{RST}")
                print(f"{YEL}💡 အကြံပြု- ဘရောက်ဆာမှာ {B64_URL} ကိုဖွင့်ပါ{RST}")
                input("  ပြန်ရန် Enter...")
                continue
            
            print(f"{GRN}✅ ဒေတာရရှိပြီ၊ ဖွင့်နေသည်...{RST}")
            
            try:
                decoded = base64.b64decode(b64_content).decode("utf-8", errors="ignore")
            except Exception as e:
                print(f"{RED}❌ ဖွင့်၍မရပါ: {e}{RST}")
                input("  ပြန်ရန် Enter...")
                continue
            
            lines = decoded.splitlines()
            keys = []
            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("ss://"):
                    ip, port = extract_ip_port(line)
                    keys.append({
                        "country": get_country(line),
                        "url": line,
                        "ip": ip,
                        "port": port
                    })
            
            if not keys:
                print(f"{RED}❌ ကီးမတွေ့ပါ{RST}")
                input("  ပြန်ရန် Enter...")
                continue
            
            print(f"{GRN}✅ စုစုပေါင်း {len(keys)} ခု တွေ့ရှိခဲ့သည်!{RST}")
            input("  ဆက်ရန် Enter...")
            
            if choice == "1":
                clear()
                print(PUR + "="*70 + RST)
                print(PUR + "|        📋 ကီးအားလုံးပြသခြင်း             |" + RST)
                print(PUR + "="*70 + RST)
                for idx, s in enumerate(keys, 1):
                    print(f"\n{PUR}[{idx}] {s['country']}{RST}")
                    print(f"{WHT}{s['url']}{RST}")
                    print(PUR + "-"*70 + RST)
                input("\n  ပြီးပါပြီ။ ပြန်ရန် Enter...")
            
            else:
                clear()
                print(PUR + "="*70 + RST)
                print(PUR + "|       📡 Ping တိုင်းနေသည်...              |" + RST)
                print(PUR + "-"*70 + RST)
                results = []
                total = len(keys)
                for i, k in enumerate(keys, 1):
                    print(f"  တိုင်းနေ: {i}/{total}", end="\r")
                    ok, ms, lvl, sc = ping_server(k["ip"], k["port"])
                    if ok and sc > 0:
                        k["ms"] = ms
                        k["lvl"] = lvl
                        k["sc"] = sc
                        results.append(k)
                
                results.sort(key=lambda x: x["ms"])
                print(f"\n\n{GRN}✅ အလုပ်လုပ်သူ {len(results)} ခု တွေ့ရှိခဲ့{RST}")
                print(PUR + "="*70 + RST)
                
                for idx, s in enumerate(results, 1):
                    stars = "*"*s["sc"] + "-"*(5-s["sc"])
                    print(f"\n{PUR}[{idx}] {s['country']}{RST}  |  Ping: {CYN}{s['ms']}ms{RST}  |  {stars}  {GRN}{s['lvl']}{RST}")
                    print(f"{WHT}{s['url']}{RST}")
                    print(PUR + "-"*70 + RST)
                
                input("\n  ပြီးပါပြီ။ ပြန်ရန် Enter...")
        
        else:
            print(f"\n{RED}မှားနေတယ်၊ ပြန်ရွေးပါ{RST}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("\n\n  Bye!\n")
        sys.exit(0)
        
