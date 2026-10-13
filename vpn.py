#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import os
import socket
import time
from datetime import datetime

VERSION = "5.8 ⚡ SIMPLE"

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
    print(f"{Colors.C}{'='*50}{Colors.RESET}")
    print(f"{Colors.C} VPN KEY FINDER — {VERSION}{Colors.RESET}")
    print(f"{Colors.C}{'='*50}{Colors.RESET}")
    print()

def get_links():
    links = []
    print("  📥 ကီးများကို ရယူနေသည်...")
    
    urls = [
        "https://raw.githubusercontent.com/ymyuuu/ymyuuu.github.io/main/vless.txt",
        "https://raw.githubusercontent.com/ircfspace/cfworker/main/dist/subscribe.txt",
        "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt"
    ]
    
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as res:
                text = res.read().decode("utf-8", errors="ignore")
                for line in text.splitlines():
                    line = line.strip()
                    if line.startswith("vless://") or line.startswith("ss://"):
                        name = "Server"
                        if "#" in line:
                            try:
                                from urllib.parse import unquote
                                name = unquote(line.split("#")[-1])
                            except:
                                name = line.split("#")[-1][:30]
                        links.append({"name": name, "key": line})
                print(f"  ✅ အောင်မြင်သည်: {url[:40]}...")
                if len(links) > 5:
                    break
        except Exception as e:
            print(f"  ❌ မအောင်မြင်ပါ: {str(e)[:30]}")
        if len(links) > 5:
            break
    
    return links

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

def main():
    header()
    keys = get_links()
    
    if not keys:
        print(f"\n  {Colors.R}❌ ကီးမတွေ့ပါ{Colors.RESET}")
        print(f"  {Colors.Y}💡 WiFi မှ မိုဘိုင်းဒေတာသို့ ပြောင်းကြည့်ပါ{Colors.RESET}")
        input("  ပိတ်ရန် Enter နှိပ်ပါ...")
        return
    
    print(f"\n  ✅ စုစုပေါင်း {len(keys)} ခု တွေ့ရှိခဲ့သည်\n")
    best_ms = 9999
    best = None
    
    for i, item in enumerate(keys, 1):
        host, port = extract_host(item["key"])
        ms = ping_test(host, port) if host else 9999
        status = f"{Colors.G}{ms}ms{Colors.RESET}" if ms < 300 else f"{Colors.Y}{ms}ms{Colors.RESET}" if ms < 600 else f"{Colors.R}{ms}ms{Colors.RESET}"
        print(f"  [{i}] {item['name'][:35]:<40} → {status}")
        if ms < best_ms:
            best_ms = ms
            best = item
    
    if best:
        print(f"\n{Colors.G}{'='*50}{Colors.RESET}")
        print(f"{Colors.G} ✅ အကောင်းဆုံးရွေးချယ်မှု{Colors.RESET}")
        print(f"  📶 မြန်နှုန်း: {Colors.G}{best_ms}ms{Colors.RESET}")
        print(f"  🔑 ကီး:")
        print(f"  {Colors.W}{best['key']}{Colors.RESET}")
        print(f"{Colors.G}{'='*50}{Colors.RESET}")
        
        if copy_key(best["key"]):
            print(f"  {Colors.G}✅ ကီးကို ကူးယူပြီးပါပြီ!{Colors.RESET}")
        else:
            print(f"  ⚠️ အထက်ကကီးကို ကိုယ်တိုင်ကူးယူပါ")
    
    input("\n  ပိတ်ရန် Enter နှိပ်ပါ...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n  ပျော်ရွှင်ဖွယ်ရှိပါစေ!")
        
