#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import os
import socket
import time
from datetime import datetime

VERSION = "5.9 ⚡ MIRRORS"

class Colors:
    C = "\033[96m"
    G = "\033[92m"
    Y = "\033[93m"
    R = "\033[91m"
    W = "\033[97m"
    RESET = "\033[0m"

def clear(): os.system("clear")
def header():
    clear()
    print(f"{Colors.C}{'='*55}{Colors.RESET}")
    print(f"{Colors.C}⚡ VPN KEY FINDER  —  {VERSION}{Colors.RESET}")
    print(f"{Colors.C}{'='*55}{Colors.RESET}")
    print()

# Mirror အသစ်များ — ကွန်ရက်အလိုက် ကွဲပြားစွာသုံးမည်
SOURCE_LINKS = [
    # Mirror 1 — jsdelivr (GitHub CDN, မြန်မာတွင် ပိုမိုဝင်လွယ်)
    "https://cdn.jsdelivr.net/gh/ymyuuu/ymyuuu.github.io@main/vless.txt",
    # Mirror 2 — ghproxy
    "https://ghproxy.com/https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt",
    # Mirror 3 — ပုံမှန် GitHub
    "https://raw.githubusercontent.com/ircfspace/worker/main/dist/subscribe.txt",
    # Mirror 4 — အခြားအရင်းအမြစ်
    "https://cdn.jsdelivr.net/gh/aiboboxx/v2rayfree@main/v2.md",
]

def fetch_from_source(url):
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Android; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0",
                "Cache-Control": "no-cache"
            }
        )
        with urllib.request.urlopen(req, timeout=25) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        return f"ERROR_HTTP:{e.code}"
    except urllib.error.URLError as e:
        return f"ERROR_NETWORK:{str(e)[:40]}"
    except Exception as e:
        return f"ERROR:{str(e)[:40]}"

def parse_keys(text):
    keys = []
    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("vless://") or line.startswith("ss://") or line.startswith("vmess://"):
            name = "VPN Server"
            if "#" in line:
                try:
                    from urllib.parse import unquote
                    name = unquote(line.split("#")[-1])
                except:
                    name = line.split("#")[-1][:40]
            keys.append({"name": name, "key": line})
    return keys

def get_all_keys():
    all_keys = []
    print("  🔍 ဆာဗာများကို ရှာဖွေနေသည်...")
    print()
    
    for idx, url in enumerate(SOURCE_LINKS, 1):
        short_url = url[:55] + "..." if len(url) > 55 else url
        print(f"  [{idx}/{len(SOURCE_LINKS)}] ဖတ်နေသည်: {short_url}")
        
        result = fetch_from_source(url)
        
        if result.startswith("ERROR"):
            print(f"      {Colors.R}❌ မအောင်မြင်ပါ: {result}{Colors.RESET}")
            print(f"      {Colors.Y}💡 နောက်အရင်းအမြစ်သို့ ပြောင်းနေသည်...{Colors.RESET}")
            print()
            continue
        
        keys = parse_keys(result)
        if keys:
            all_keys.extend(keys)
            print(f"      {Colors.G}✅ အောင်မြင်သည်! ကီး {len(keys)} ခု တွေ့ရှိခဲ့သည်{Colors.RESET}")
            print()
            # တစ်ခုအောင်မြင်ပြီးသားဆို ရပ်တန့်မည်
            if len(all_keys) >= 3:
                break
        else:
            print(f"      {Colors.Y}⚠️ အကြောင်းအရာမတွေ့ပါ{Colors.RESET}")
            print()
    
    # တူညီသောကီးများကို ဖယ်ရှားမည်
    seen = set()
    unique_keys = []
    for item in all_keys:
        if item["key"] not in seen:
            seen.add(item["key"])
            unique_keys.append(item)
    
    return unique_keys

def extract_host(key):
    try:
        from urllib.parse import urlparse
        u = urlparse(key)
        return u.hostname or "", u.port or 443
    except:
        return "", 443

def ping_test(host, port=443, timeout=0.5):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        start = time.time()
        s.connect((host, int(port)))
        s.close()
        return round((time.time() - start) * 1000)
    except:
        return 9999

def copy_to_clipboard(text):
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", text])
        return True
    except:
        return False

def show_result(item, ms=0):
    print(f"\n{Colors.G}{'─'*55}{Colors.RESET}")
    print(f"  📌 အမည်: {item['name']}")
    if ms > 0:
        if ms < 200:
            status = f"{Colors.G}{ms}ms  အမြန်{Colors.RESET}"
        elif ms < 400:
            status = f"{Colors.Y}{ms}ms  အတန်းအစား{Colors.RESET}"
        else:
            status = f"{Colors.R}{ms}ms  နှေး{Colors.RESET}"
        print(f"  📶 မြန်နှုန်း: {status}")
    print(f"  🔑 ကီး:")
    print(f"  {Colors.W}{item['key']}{Colors.RESET}")
    print(f"{Colors.G}{'─'*55}{Colors.RESET}")
    
    if copy_to_clipboard(item["key"]):
        print(f"  ✅ ကီးကို ကူးယူပြီးပါပြီ! အသုံးပြုရန် VPN အက်ပ်ထဲတွင် ကူးထည့်ပါ။")
    else:
        print(f"  ⚠️ အထက်ကကီးကို ကိုယ်တိုင်ကူးယူပါ")
    print()

def main():
    header()
    keys = get_all_keys()
    
    if not keys:
        print(f"  {Colors.R}❌ မည်သည့်ကီးကိုမျှ မတွေ့ပါ{Colors.RESET}")
        print()
        print(f"  {Colors.Y}💡 ဖြေရှင်းနည်းများ:{Colors.RESET}")
        print(f"     ၁။ WiFi မှ မိုဘိုင်းဒေတာသို့ ပြောင်းပါ")
        print(f"     ၂။ VPN သို့မဟုတ် ပရောက်စီကို ပိတ်ပါ")
        print(f"     ၃။ အင်တာနက် ချိတ်ဆက်မှုကို စစ်ဆေးပါ")
        print(f"     ၄။ ပြန်လည်စတင်ပါ")
        print()
        input("  ထွက်ရန် Enter နှိပ်ပါ...")
        return
    
    print(f"  ✅ စုစုပေါင်း ထူးခြားသော ကီး {len(keys)} ခု အဆင်သင့်ဖြစ်နေသည်")
    print(f"  📋 အကောင်းဆုံးဆာဗာကို ရွေးချယ်နေသည်...\n")
    
    best_ms = 9999
    best_item = None
    
    for idx, item in enumerate(keys[:10], 1):
        host, port = extract_host(item["key"])
        if not host:
            continue
        ms = ping_test(host, port)
        if ms == 9999:
            print(f"  [{idx}] {item['name'][:35]:<38} → {Colors.R}မတုံ့ပြန်ပါ{Colors.RESET}")
            continue
        
        if ms < 200:
            tag = f"{Colors.G} ← အကောင်းဆုံး!{Colors.RESET}"
        elif ms < best_ms:
            tag = f" အသစ်ပိုမြန်သည်"
        else:
            tag = ""
        
        print(f"  [{idx}] {item['name'][:35]:<38} → {ms}ms{tag}")
        
        if ms < best_ms:
            best_ms = ms
            best_item = item
            if ms < 100:
                break
    
    print()
    if best_item:
        show_result(best_item, best_ms)
    else:
        print(f"  {Colors.Y}⚠️ မည်သည့်ဆာဗာမျှ မတုံ့ပြန်ပါ{Colors.RESET}")
        print(f"  သို့သော် အောက်ပါကီးကို သင်ကိုယ်တိုင် အသုံးပြုနိုင်ပါသည်-")
        show_result(keys[0])
    
    input("  ပြီးဆုံးရန် Enter နှိပ်ပါ...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  👋 ပျော်ရွှင်ဖွယ်ရှိပါစေ!")
    except Exception as e:
        print(f"\n  {Colors.R}အမှားအယွင်း: {str(e)}{Colors.RESET}")
        input("  ထွက်ရန် Enter နှိပ်ပါ...")
        
