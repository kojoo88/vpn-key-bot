#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import base64
import socket
import time
import os
import sys
from datetime import datetime

# ================== COLORS ==================
CYN = "\033[38;5;80m"
GRN = "\033[38;5;114m"
YEL = "\033[38;5;221m"
RED = "\033[38;5;209m"
PUR = "\033[38;5;141m"
WHT = "\033[38;5;255m"
BLD = "\033[1m"
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
            return True, ms, "⚡ အမြန်ဆုံး", 5
        elif ms < 150:
            return True, ms, "✅ ကောင်းမွန်", 4
        elif ms < 250:
            return True, ms, "⚠️  အလယ်အလတ်", 3
        elif ms < 400:
            return True, ms, "🐢 နှေးကွေး", 2
        else:
            return True, ms, "🐌 အလွန်နှေး", 1
    except:
        return False, 999, "❌ ဆက်မရ", 0

def get_country(text):
    codes = {
        "SG": "🇸🇬 စင်ကာပူ",
        "US": "🇺🇸 အမေရိက",
        "JP": "🇯🇵 ဂျပန်",
        "KR": "🇰🇷 ကိုရီးယား",
        "HK": "🇭🇰 ဟောင်ကောင်",
        "TW": "🇹🇭 ထိုင်ဝမ်",
        "UK": "🇬🇧 ဗြိတိန်",
        "DE": "🇩🇪 ဂျာမနီ",
        "NL": "🇳🇱 နယ်သာလန်",
        "CA": "🇨🇦 ကနေဒါ",
        "AU": "🇦🇺 ဩစတြေးလျ",
        "IN": "🇮🇳 အိန္ဒိယ",
        "TH": "🇹🇭 ထိုင်း",
        "MY": "🇲🇾 မလေးရှား",
        "FR": "🇫🇷 ပြင်သစ်",
        "IT": "🇮🇹 အီတလီ",
        "ES": "🇪🇸 စပိန်",
        "BR": "🇧🇷 ဘရာဇီး",
        "FI": "🇫🇮 ဖင်လန်",
        "SE": "🇸🇪 ဆွီဒင်",
        "PL": "🇵🇱 ပိုလန်",
        "CH": "🇨🇭 ဆွစ်ဇာလန်",
        "IE": "🇮🇪 အိုင်ယာလန်",
        "AT": "🇦🇹 သြစတြီးယား",
        "BE": "🇧🇪 ဘယ်လ်ဂျီယံ",
        "DK": "🇩🇰 ဒိန်းမတ်",
        "NO": "🇳🇴 နော်ဝေ",
        "NZ": "🇳🇿 နယူးဇီလန်",
        "ZA": "🇿🇦 တောင်အာဖရိက",
        "RU": "🇷🇺 ရုရှား"
    }
    text_upper = text.upper()
    for code, name in codes.items():
        if code in text_upper:
            return name
    return "🌍 အခြား"

# ================== MAIN ==================
def main():
    while True:
        clear()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(PUR + "="*60 + RST)
        print(PUR + f"|   🚀 SHADOWMERE B64 - KEY FINDER        |" + RST)
        print(PUR + f"|   📅 စတင်ချိန်: {now}{' '*(32-len(now))}|" + RST)
        print(PUR + "="*60 + RST)
        print(f"  [1] 📋 ကီးအားလုံးကို ကြည့်မည်")
        print(f"  [2] ⚡ Ping တိုင်းပြီး အမြန်ဆုံးရှာမည်")
        print(f"  [0] ❌ ထွက်မည်")
        print(PUR + "="*60 + RST)
        
        choice = input("\n  ရွေးပါ -> ")
        
        if choice == "0":
            print("\n  👋 ပြန်လာတော့မယ်! ဘယ်အချိန်မဆိုပြန်လာခဲ့နော်\n")
            break
        
        elif choice == "1" or choice == "2":
            clear()
            print(f"{CYN}⏳ လင့်ခ်ဖွင့်နေသည်...{RST}")
            try:
                req = urllib.request.Request(B64_URL, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=20) as r:
                    b64_content = r.read().decode("utf-8", errors="ignore")
            except Exception as e:
                print(f"{RED}❌ လင့်ခ်မဖွင့်နိုင်ပါ: {e}{RST}")
                print(f"{YEL}💡 အကြံပြုချက်- ဘရောက်ဆာမှာ ဒီလင့်ခ်ကိုဖွင့်ပါ\n{B64_URL}{RST}")
                input("  ပြန်ရန် Enter...")
                continue
            
            load_time = datetime.now().strftime("%H:%M:%S")
            print(f"{GRN}✅ ဒေတာရရှိပြီ!  ရယူချိန်: {load_time}{RST}")
            
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
                print(f"  📅 ရယူချိန်: {load_time}")
                print(f"  📊 စုစုပေါင်း ဆာဗာ: {len(keys)} ခု")
                print(PUR + "-"*70 + RST)
                
                for idx, s in enumerate(keys, 1):
                    print(f"\n{PUR}[{idx}] {s['country']}{RST}")
                    print(f"{GRN}🔑 ကီးကို အောက်ကနေ ကူးယူပါ 👇{RST}")
                    print(f"{WHT}{s['url']}{RST}")
                    print(PUR + "-"*70 + RST)
                
                input("\n  ပြီးပါပြီ။ ပြန်ရန် Enter...")
            
            else:
                clear()
                print(PUR + "="*70 + RST)
                print(PUR + "|       ⚡ Ping တိုင်းနေသည်...              |" + RST)
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
                success_rate = int((len(results) / total) * 100) if total > 0 else 0
                
                print(f"\n\n{PUR}📊 အကျဉ်းချုပ်:{RST}")
                print(f"  စုစုပေါင်း: {total} ခု")
                print(f"  အလုပ်လုပ်သူ: {GRN}{len(results)} ခု{WHT}")
                print(f"  အလုပ်လုပ်နှုန်း: {GRN}{success_rate}%{WHT}")
                if results:
                    print(f"  🏆 အမြန်ဆုံး Ping: {GRN}{results[0]['ms']}ms{RST} — {results[0]['country']}")
                print(PUR + "="*70 + RST)
                
                if results:
                    # အမြန်ဆုံးကို အထူးပြု
                    best = results[0]
                    stars = "⭐" * best["sc"] + "☆" * (5 - best["sc"])
                    print(f"\n{BLD}{GRN}🏆 အမြန်ဆုံး ဆာဗာ (အကြံပြုအသုံးပြုရန်){RST}")
                    print(f"{PUR}{'='*70}{RST}")
                    print(f"  နိုင်ငံ: {best['country']}")
                    print(f"  Ping:   {CYN}{best['ms']}ms{RST}")
                    print(f"  အရှိန်: {stars}")
                    print(f"  အဆင့်: {GRN}{best['lvl']}{RST}")
                    print(f"\n  {GRN}🔑 ကီးကို အောက်ကနေ ကူးယူပါ 👇{RST}")
                    print(f"  {WHT}{best['url']}{RST}")
                    print(PUR + "-"*70 + RST)
                    
                    # ကျန်တွေ
                    print(f"\n{PUR}📋 အခြားဆာဗာများ{RST}")
                    for idx, s in enumerate(results[1:15], 2):
                        stars = "★" * s["sc"] + "☆" * (5 - s["sc"])
                        print(f"\n{PUR}[{idx}] {s['country']}{RST}  |  Ping: {CYN}{s['ms']}ms{RST}  |  {stars}  {s['lvl']}")
                        print(f"{WHT}{s['url']}{RST}")
                        print(PUR + "-"*70 + RST)
                else:
                    print(f"{RED}❌ အလုပ်လုပ်နိုင်သောဆာဗာ မတွေ့ပါ{RST}")
                
                input("\n  ပြီးပါပြီ။ ပြန်ရန် Enter...")
        
        else:
            print(f"\n{RED}မှားနေတယ်၊ 0, 1, 2 သာရွေးပါ{RST}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("\n\n  👋 ပြန်လာတော့မယ်!\n")
        sys.exit(0)
            
