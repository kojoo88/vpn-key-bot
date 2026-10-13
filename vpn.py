#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import base64
import os
import socket
import time
from datetime import datetime

VERSION = "PREMIUM 1.0 ⚡"

class Theme:
    PRI = "\033[38;5;117m"
    SEC = "\033[38;5;245m"
    ACC = "\033[38;5;149m"
    SUC = "\033[38;5;114m"
    INF = "\033[38;5;81m"
    WAR = "\033[38;5;221m"
    ERR = "\033[38;5;203m"
    BLD = "\033[1m"
    BRI = "\033[38;5;255m"
    RES = "\033[0m"

def clear(): os.system("clear")

def logo():
    clear()
    print(f"{Theme.PRI}{'╔'+'═'*58+'╗'}{Theme.RES}")
    print(f"{Theme.PRI}║{Theme.RES}{Theme.BRI}{' '*15}⚡ VPN KEY FINDER PREMIUM ⚡{' '*15}{Theme.RES}{Theme.PRI}║{Theme.RES}")
    print(f"{Theme.PRI}║{Theme.RES}{Theme.SEC}{' '*22}Version {VERSION}{' '*22}{Theme.RES}{Theme.PRI}║{Theme.RES}")
    print(f"{Theme.PRI}{'╚'+'═'*58+'╝'}{Theme.RES}")
    print()

SOURCES = [
    {"name": "Shadowmere JSON",   "url": "https://shadowmere.xyz/api/sub/",        "type": "json"},
    {"name": "Shadowmere Base64", "url": "https://shadowmere.xyz/api/b64sub/",     "type": "b64"},
    {"name": "GitHub VLESS List",  "url": "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vless.txt", "type": "txt"}
]

def fetch_url(source):
    try:
        req = urllib.request.Request(
            source["url"],
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=25) as res:
            return res.read().decode("utf-8", errors="ignore")
    except:
        return None

def parse_keys(text, source_type):
    keys = []
    if not text: return keys
    if source_type == "json":
        try:
            import json
            data = json.loads(text)
            if isinstance(data, list):
                for item in data:
                    key = item.get("url") or item.get("link") or ""
                    name = item.get("name") or item.get("remarks") or "Server"
                    if key and "://" in key:
                        keys.append({"name": name, "key": key})
        except: pass
    elif source_type == "b64":
        try:
            decoded = base64.b64decode(text).decode("utf-8", errors="ignore")
            for line in decoded.splitlines():
                line = line.strip()
                if line and "://" in line:
                    name = "Server"
                    if "#" in line:
                        try:
                            from urllib.parse import unquote
                            name = unquote(line.split("#")[-1])
                        except:
                            name = line.split("#")[-1][:40]
                    keys.append({"name": name, "key": line})
        except: pass
    elif source_type == "txt":
        for line in text.splitlines():
            line = line.strip()
            if line and ("vless://" in line or "ss://" in line or "vmess://" in line):
                name = "Server"
                if "#" in line:
                    try:
                        from urllib.parse import unquote
                        name = unquote(line.split("#")[-1])
                    except:
                        name = line.split("#")[-1][:40]
                keys.append({"name": name, "key": line})
    return keys

def load_sources():
    all_keys = []
    seen = set()
    logo()
    print(f"{Theme.INF}📡 အရင်းအမြစ်များကို ဖတ်နေသည်...{Theme.RES}\n")
    for idx, src in enumerate(SOURCES, 1):
        print(f"  {Theme.INF}[{idx}/{len(SOURCES)}]{Theme.RES} {src['name']:<22}", end=" ")
        text = fetch_url(src)
        if text:
            keys = parse_keys(text, src["type"])
            if keys:
                for k in keys:
                    if k["key"] not in seen:
                        seen.add(k["key"])
                        all_keys.append(k)
                print(f"{Theme.SUC}✅ +{len(keys)} keys  |  Total: {len(all_keys)}{Theme.RES}")
            else:
                print(f"{Theme.WAR}⚠️ အကြောင်းအရာမတွေ့{Theme.RES}")
        else:
            print(f"{Theme.ERR}❌ ချိတ်ဆက်မှုမအောင်မြင်{Theme.RES}")
    print(f"\n{Theme.SUC}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Theme.RES}")
    print(f"{Theme.SUC}✅ စုစုပေါင်း ကီး {len(all_keys)} ခု အဆင်သင့်ဖြစ်နေပါပြီ{Theme.RES}")
    return all_keys

def extract_host(key):
    try:
        from urllib.parse import urlparse
        u = urlparse(key)
        return u.hostname or "", u.port or 443
    except:
        return "", 443

def ping_test(host, port=443, timeout=0.55):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        st = time.time()
        s.connect((host, int(port)))
        s.close()
        return round((time.time() - st) * 1000)
    except:
        return 9999

def copy_key(text):
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", text])
        return True
    except:
        return False

def progress_bar(current, total, width=30):
    pct = int((current / total) * 100)
    filled = int(width * current / total)
    bar = f"{Theme.INF}{'█'*filled}{Theme.SEC}{'░'*(width-filled)}{Theme.RES}"
    return f"{bar} {pct}%"

def ping_bar(ms):
    if ms == 9999:
        return f"{Theme.ERR}မတုံ့ပြန်နိုင်{Theme.RES}"
    if ms < 100:
        s = Theme.SUC
        b = "█"*5
    elif ms < 200:
        s = "\033[38;5;148m"
        b = "█"*4 + "░"
    elif ms < 350:
        s = Theme.WAR
        b = "█"*3 + "░"*2
    elif ms < 500:
        s = "\033[38;5;215m"
        b = "█"*2 + "░"*3
    else:
        s = Theme.ERR
        b = "█"*1 + "░"*4
    return f"{s}{b}{Theme.RES}  {s}{ms:>4}ms{Theme.RES}"

def get_flag(name):
    n = name.lower()
    fl = "🌐"
    if "singapore" in n or "sg" in n: fl = "🇸🇬"
    elif "malaysia" in n or "my" in n: fl = "🇲🇾"
    elif "thai" in n or "th" in n: fl = "🇹🇭"
    elif "vietnam" in n or "vn" in n: fl = "🇻🇳"
    elif "hongkong" in n or "hk" in n: fl = "🇭🇰"
    elif "japan" in n or "jp" in n: fl = "🇯🇵"
    elif "korea" in n or "kr" in n: fl = "🇰🇷"
    elif "india" in n or "in" in n: fl = "🇮🇳"
    elif "indonesia" in n or "id" in n: fl = "🇮🇩"
    elif "canada" in n: fl = "🇨🇦"
    elif "germany" in n or "de" in n: fl = "🇩🇪"
    elif "united kingdom" in n or "uk" in n or "gb" in n: fl = "🇬🇧"
    elif "france" in n or "fr" in n: fl = "🇫🇷"
    return fl

def scan_all(keys):
    logo()
    print(f"{Theme.INF}📊 ဆာဗာအားလုံးကို စမ်းသပ်နေသည်...{Theme.RES}\n")
    results = []
    total = min(len(keys), 25)
    for i in range(total):
        item = keys[i]
        host, port = extract_host(item["key"])
        ms = ping_test(host, port) if host else 9999
        results.append({"name": item["name"], "key": item["key"], "ms": ms, "host": host})
        print(f"  [{i+1:02d}/{total}] {progress_bar(i+1, total, 25)}", end="\r")
    print("\n")
    results.sort(key=lambda x: x["ms"])
    return results

def show_top(results, count=10):
    logo()
    print(f"{Theme.BLD}{Theme.INF}🏆 အမြန်ဆုံး ဆာဗာများ (Top {count}){Theme.RES}\n")
    print(f"  {'#':<4} {'တည်းချက်':<5} {'Ping':<16} {'တည်နေရာ/အမည်'}")
    print(f"  {'─'*60}")
    display = [r for r in results if r["ms"] < 9999][:count]
    if not display:
        print(f"  {Theme.WAR}မည်သည့်ဆာဗာမျှ မတုံ့ပြန်ပါ{Theme.RES}")
        return None
    for idx, r in enumerate(display, 1):
        flag = get_flag(r["name"])
        bar = ping_bar(r["ms"])
        name = r["name"][:38]
        print(f"  {Theme.BLD}{idx:<2d}{Theme.RES}   {bar:<16} {flag} {name}")
    return display[0]

def show_best(best, total_tested, total_keys, results):
    logo()
    print(f"{Theme.SUC}🏆 အကောင်းဆုံး ဆာဗာ ရွေးချယ်ပြီးပါပြီ{Theme.RES}\n")
    print(f"{Theme.INF}📊 စာရင်းအင်းအချက်အလက်များ{Theme.RES}")
    print(f"  စုစုပေါင်းကီးရရှိမှု : {Theme.BLD}{total_keys}{Theme.RES} ခု")
    print(f"  စမ်းသပ်ပြီးဆာဗာ    : {Theme.BLD}{total_tested}{Theme.RES} ခု")
    success = sum(1 for r in results if r["ms"] < 9999)
    rate = (success / total_tested * 100) if total_tested else 0
    print(f"  အလုပ်လုပ်ဆောင်နှုန်း : {Theme.BLD}{rate:.1f}%{Theme.RES}")
    print()
    print(f"{Theme.INF}📍 ဆာဗာအချက်အလက်{Theme.RES}")
    print(f"  အမည် : {Theme.BLD}{get_flag(best['name'])} {best['name']}{Theme.RES}")
    print(f"  Ping  : {ping_bar(best['ms'])}")
    print()
    print(f"{Theme.INF}🔑 VPN Key{Theme.RES}")
    print(f"  {Theme.BRI}{best['key']}{Theme.RES}")
    print()
    if copy_key(best["key"]):
        print(f"{Theme.SUC}✅ ကီးကို ကလစ်ဘုတ်သို့ ကူးယူပြီးပါပြီ!{Theme.RES}")
    else:
        print(f"{Theme.WAR}⚠️ အထက်ကကီးကို ကိုယ်တိုင်ကူးယူပါ{Theme.RES}")
    print(f"\n{Theme.SEC}{'═'*60}{Theme.RES}")

def menu():
    keys = load_sources()
    if not keys:
        input(f"\n{Theme.INF}ပြန်ရန် Enter နှိပ်ပါ...{Theme.RES}")
        return
    results = scan_all(keys)
    while True:
        logo()
        print(f"{Theme.BLD}{Theme.INF}📋 အဓိက မီနူး{Theme.RES}\n")
        print(f"  [1] 🏆 အကောင်းဆုံး ဆာဗာကို ချက်ချင်းရွေးပါ")
        print(f"  [2] 📊 အမြန်ဆုံး 10 ခုကို ကြည့်ပါ")
        print(f"  [3] 📋 ဆာဗာအားလုံးစာရင်း")
        print(f"  [4] 🔄 ပြန်လည်စကင်န်ဖတ်ပါ")
        print(f"  [0] ❌ ထွက်ပါ")
        print()
        sel = input(f"{Theme.INF}ရွေးချယ်ပါ → {Theme.RES}").strip()
        if sel == "1":
            best = show_top(results, 1)
            if best: show_best(best, len(results), len(keys), results)
            input(f"\n{Theme.INF}ပြန်ရန် Enter နှိပ်ပါ...{Theme.RES}")
        elif sel == "2":
            show_top(results, 10)
            input(f"\n{Theme.INF}ပြန်ရန် Enter နှိပ်ပါ...{Theme.RES}")
        elif sel == "3":
            logo()
            print(f"{Theme.INF}📋 ဆာဗာအားလုံးစာရင်း{Theme.RES}\n")
            for i, r in enumerate(results, 1):
                flag = get_flag(r["name"])
                bar = ping_bar(r["ms"])
                print(f"  [{i:02d}] {flag} {r['name'][:35]:<38} {bar}")
            input(f"\n{Theme.INF}ပြန်ရန် Enter နှိပ်ပါ...{Theme.RES}")
        elif sel == "4":
            keys = load_sources()
            if keys: results = scan_all(keys)
        elif sel == "0":
            print(f"{Theme.SUC}👋 ကောင်းသောနေ့လည်ခင်းဖြစ်ပါစေ!{Theme.RES}")
            break

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(f"\n{Theme.SUC}👋 ပျော်ရွှင်ဖွယ်ရှိပါစေ!{Theme.RES}")
    except Exception as e:
        print(f"\n{Theme.ERR}အမှားအယွင်း: {str(e)}{Theme.RES}")
        input(f"ဆက်ရန် Enter...")
