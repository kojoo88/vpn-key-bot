#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import base64
import socket
import time
import os
import subprocess
import sys

# ================== COLORS ==================
BLK = "\033[38;5;234m"
BLU = "\033[38;5;117m"
CYN = "\033[38;5;80m"
GRN = "\033[38;5;114m"
YEL = "\033[38;5;221m"
ORG = "\033[38;5;215m"
RED = "\033[38;5;209m"
PUR = "\033[38;5;141m"
WHT = "\033[38;5;255m"
RST = "\033[0m"

def clear():
    os.system("clear")

# ================== PING TEST ==================
def extract_ip_port(url):
    try:
        if url.startswith("vless://"):
            body = url[8:]
        elif url.startswith("ss://"):
            body = url[5:]
        else:
            return None, None
        if "#" in body:
            body = body.split("#")[0]
        if "@" in body:
            host_port = body.split("@")[-1]
        else:
            host_port = body
        if ":" in host_port:
            parts = host_port.rsplit(":", 1)
            host = parts[0].split("/")[0]
            port = int(parts[1].split("/")[0])
            return host, port
        return None, None
    except:
        return None, None

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
        return False, 999, "No Response", 0

def get_country(text):
    codes = ["SG", "US", "JP", "KR", "HK", "TW", "UK", "DE", "NL", "CA", "AU", "IN", "TH", "MY", "FR", "IT", "ES", "BR"]
    for c in codes:
        if c in text.upper():
            return c
    return "??"

def parse_keys(content, fmt):
    keys = []
    if not content:
        return keys
    try:
        if fmt == "b64":
            content = base64.b64decode(content).decode("utf-8", errors="ignore")
        lines = content.splitlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith(("vless://", "ss://")):
                proto = "VLESS" if line.startswith("vless://") else "SS"
                ip, port = extract_ip_port(line)
                keys.append({
                    "country": get_country(line),
                    "protocol": proto,
                    "url": line,
                    "ip": ip,
                    "port": port
                })
    except:
        pass
    return keys

def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        with urllib.request.urlopen(req) as r:
            return r.read().decode("utf-8", errors="ignore")
    except:
        return None

# ================== MAIN MENU ==================
def main():
    vless = []
    ss = []
    SOURCES = [
        ("Shadowmere Plain", "https://shadowmere.xyz/api/sub/", "txt"),
        ("Shadowmere B64", "https://shadowmere.xyz/api/b64sub/", "b64"),
        ("Epodon VLESS", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Splitted-By-Protocol/vless.txt", "txt"),
        ("Epodon SS", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/ss.txt", "txt"),
    ]
    
    while True:
        clear()
        print(PUR + "="*60 + RST)
        print(PUR + "|   🚀 VPN KEY FINDER - REAL PING         |" + RST)
        print(PUR + "-"*60 + RST)
        print(f"  [1] Load Sources from Internet")
        print(f"  [2] Paste & Scan Your Own Keys")
        print(f"  [3] Show VLESS + Real Ping")
        print(f"  [4] Show SS + Real Ping")
        print(f"  [5] Find Fastest Server")
        print(PUR + "-"*60 + RST)
        print(f"  [0] Exit")
        print(PUR + "="*60 + RST)
        
        choice = input("\n  ရွေးပါ -> ")
        
        if choice == "0":
            print("\n  Bye! 👋\n")
            break
        
        elif choice == "1":
            vless = []
            ss = []
            clear()
            print(PUR + "="*60 + RST)
            print(PUR + "|        LOADING SOURCES...               |" + RST)
            print(PUR + "-"*60 + RST)
            ok_count = 0
            for name, url, fmt in SOURCES:
                print(f"  ⏳ {name}...", end=" ")
                content = fetch_url(url)
                if content:
                    keys = parse_keys(content, fmt)
                    for k in keys:
                        if k["protocol"] == "VLESS":
                            vless.append(k)
                        else:
                            ss.append(k)
                    print(f"{GRN}OK {len(keys)} keys{RST}")
                    ok_count += 1
                else:
                    print(f"{YEL}SKIP (no internet){RST}")
            print(PUR + "-"*60 + RST)
            print(f"  ✅ ရရှိခဲ့: VLESS={len(vless)}  SS={len(ss)}")
            if ok_count == 0:
                print(f"  {YEL}⚠️  လင့်ခ်မဖွင့်နိုင်ပါက Option [2] ကိုသုံးပါ{RST}")
            input("\n  ဆက်ရန် Enter...")
        
        elif choice == "2":
            clear()
            print(PUR + "="*60 + RST)
            print(PUR + "|         ကီးကို ကူးထည့်ပါ               |" + RST)
            print(PUR + "-"*60 + RST)
            print("  ဘရောက်ဆာက ကူးလာတဲ့ ကီးတွေကို ဒီမှာ ကူးထည့်ပါ")
            print("  ပြီးရင် အလွတ် line မှာ ENTER နှစ်ခုနှိပ်ပါ\n")
            lines = []
            while True:
                try:
                    l = input()
                    if not l:
                        break
                    lines.append(l)
                except:
                    break
            content = "\n".join(lines)
            keys = parse_keys(content, "txt") + parse_keys(content, "b64")
            for k in keys:
                if k["protocol"] == "VLESS":
                    vless.append(k)
                else:
                    ss.append(k)
            print(f"\n  {GRN}✅ စုစုပေါင်း {len(keys)} ခုကို တွေ့ရှိခဲ့သည်!{RST}")
            input("  ဆက်ရန် Enter...")
        
        elif choice == "3" or choice == "4":
            target = vless if choice == "3" else ss
            label = "VLESS" if choice == "3" else "SS"
            if not target:
                print(f"\n  {YEL}⚠️  အရင် [1] သို့မဟုတ် [2] ဖြင့် ကီးရယူပါ{RST}")
                time.sleep(1.5)
                continue
            clear()
            print(PUR + "="*70 + RST)
            print(PUR + f"|   {label} SERVERS - REAL PING{' '*(48-len(label))}|" + RST)
            print(PUR + "-"*70 + RST)
            results = []
            total = len(target)
            for i, k in enumerate(target, 1):
                print(f"  စစ်ဆေးနေ: {i}/{total}", end="\r")
                ok, ms, lvl, sc = ping_server(k["ip"], k["port"])
                if ok and sc > 0:
                    k["ms"] = ms
                    k["lvl"] = lvl
                    k["sc"] = sc
                    results.append(k)
            results.sort(key=lambda x: x["ms"])
            print(f"\n  {GRN}✅ အလုပ်လုပ်သူ {len(results)} ခု တွေ့ရှိခဲ့{RST}")
            print(PUR + "="*70 + RST)
            for idx, s in enumerate(results[:15], 1):
                stars = "*"*s["sc"] + "-"*(5-s["sc"])
                print(f"\n{PUR}[{idx}] {s['country']}  Ping: {CYN}{s['ms']}ms{RST}  {stars}  {GRN}{s['lvl']}{RST}")
                print(f"  🔑 {WHT}{s['url']}{RST}")
                print(PUR + "-"*70 + RST)
            input("\n  ပြန်ရန် Enter...")
        
        elif choice == "5":
            all_keys = vless + ss
            if not all_keys:
                print(f"\n  {YEL}⚠️  အရင်ကီးရယူပါ{RST}")
                time.sleep(1.5)
                continue
            clear()
            print(PUR + "="*70 + RST)
            print(PUR + "|      🏆 အမြန်ဆုံးကို ရှာဖွေနေ...          |" + RST)
            print(PUR + "-"*70 + RST)
            results = []
            total = len(all_keys)
            for i, k in enumerate(all_keys, 1):
                print(f"  စစ်ဆေးနေ: {i}/{total}", end="\r")
                ok, ms, lvl, sc = ping_server(k["ip"], k["port"])
                if ok and sc > 0:
                    k["ms"] = ms
                    k["lvl"] = lvl
                    k["sc"] = sc
                    results.append(k)
            results.sort(key=lambda x: x["ms"])
            if results:
                best = results[0]
                stars = "*"*best["sc"] + "-"*(5-best["sc"])
                clear()
                print(PUR + "="*70 + RST)
                print(PUR + "|       🏆 အမြန်ဆုံးဆာဗာ တွေ့ပြီ!           |" + RST)
                print(PUR + "-"*70 + RST)
                print(f"\n  နိုင်ငံ : {best['country']}")
                print(f"  အမျိုးအစား: {best['protocol']}")
                print(f"  Ping   : {GRN}{best['ms']}ms{RST}  {stars}")
                print(f"  အရှိနှုန်း: {GRN}{best['lvl']}{RST}")
                print(f"\n  🔑 ကီး:")
                print(f"  {WHT}{best['url']}{RST}")
                print(PUR + "="*70 + RST)
            else:
                print(f"\n  {RED}❌ အလုပ်လုပ်သူ မတွေ့ပါ{RST}")
            input("\n  ပြန်ရန် Enter...")
        
        else:
            print(f"\n  {RED}မှားနေတယ်၊ ပြန်ရွေးပါ{RST}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Bye!\n")
        sys.exit(0)
