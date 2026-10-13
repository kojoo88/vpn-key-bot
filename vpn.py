#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import base64
import os
import socket
import time
from datetime import datetime

VERSION = "5.10 ⚡ DIRECT LINKS"

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

# သင်ပေးလိုက်တဲ့ တိုက်ရိုက်လင့်ခ်သစ်များ
SOURCES = [
    {
        "name": "Shadowmere JSON",
        "url": "https://shadowmere.xyz/api/sub/",
        "type": "json"
    },
    {
        "name": "Shadowmere Base64",
        "url": "https://shadowmere.xyz/api/b64sub/",
        "type": "b64"
    },
    {
        "name": "GitHub VLESS List",
        "url": "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vless.txt",
        "type": "txt"
    }
]

def fetch_url(source):
    print(f"  📥 ဖတ်နေသည်: {source['name']}...")
    try:
        req = urllib.request.Request(
            source["url"],
            headers={
                "User-Agent": "Mozilla/5.0 (Android 14; Mobile; rv:125.0) Gecko/125.0 Firefox/125.0",
                "Accept": "*/*"
            }
        )
        with urllib.request.urlopen(req, timeout=25) as res:
            return res.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        print(f"    ❌ HTTP အမှား: {e.code}")
        return None
    except urllib.error.URLError as e:
        print(f"    ❌ ကွန်ရက်အမှား: {str(e)[:40]}")
        return None
    except Exception as e:
        print(f"    ❌ ဖတ်လို့မရ: {str(e)[:40]}")
        return None

def parse_keys(text, source_type):
    keys = []
    if not text:
        return keys
    
    if source_type == "json":
        try:
            data = __import__("json").loads(text)
            if isinstance(data, list):
                for item in data:
                    key = item.get("url") or item.get("link") or ""
                    name = item.get("name") or item.get("remarks") or "Server"
                    if key and ("vless://" in key or "ss://" in key or "vmess://" in key):
                        keys.append({"name": name, "key": key})
        except Exception as e:
            print(f"    ⚠️ JSON ဖတ်လို့မရ: {str(e)[:30]}")
    
    elif source_type == "b64":
        try:
            decoded = base64.b64decode(text).decode("utf-8", errors="ignore")
            for line in decoded.splitlines():
                line = line.strip()
                if line and ("://" in line):
                    name = "Server"
                    if "#" in line:
                        try:
                            from urllib.parse import unquote
                            name = unquote(line.split("#")[-1])
                        except:
                            name = line.split("#")[-1][:40]
                    keys.append({"name": name, "key": line})
        except Exception as e:
            print(f"    ⚠️ Base64 ဖတ်လို့မရ: {str(e)[:30]}")
    
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

def get_all_keys():
    all_keys = []
    seen = set()
    
    for src in SOURCES:
        text = fetch_url(src)
        if text:
            keys = parse_keys(text, src["type"])
            if keys:
                for k in keys:
                    if k["key"] not in seen:
                        seen.add(k["key"])
                        all_keys.append(k)
                print(f"    ✅ {len(keys)} ခု တွေ့ရှိခဲ့သည်")
            else:
                print(f"    ⚠️ ကီးမတွေ့ပါ")
        print()
    
    return all_keys

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
    print("  🔍 ကီးများကို ရယူနေသည်...")
    print()
    
    keys = get_all_keys()
    
    if not keys:
        print(f"  {Colors.R}❌ မည်သည့်ကီးကိုမျှ မတွေ့ပါ{Colors.RESET}")
        print()
        print(f"  {Colors.Y}💡 စစ်ဆေးပါ:{Colors.RESET}")
        print(f"     • အင်တာနက် ချိတ်ဆက်မှု")
        print(f"     • VPN / ပရောက်စီ ပိတ်ထားခြင်း")
        print(f"     • WiFi ↔ မိုဘိုင်းဒေတာ ပြောင်းကြည့်ပါ")
        input("  ပြန်ရန် Enter နှိပ်ပါ...")
        return
    
    print(f"  ✅ စုစုပေါင်း ထူးခြားသော ကီး {len(keys)} ခု အဆင်သင့်ဖြစ်နေသည်")
    print(f"  📶 အမြန်ဆုံးဆာဗာကို ရွေးချယ်နေသည်...\n")
    
    best_ms = 9999
    best = None
    
    for i, item in enumerate(keys[:15], 1):
        host, port = extract_host(item["key"])
        if not host:
            continue
        ms = ping_test(host, port)
        
        if ms == 9999:
            print(f"  [{i:2d}] ❌ {item['name'][:30]:<32} မတုံ့ပြန်ပါ")
            continue
        
        status = f"{Colors.G}{ms}ms{Colors.RESET}" if ms < 200 else f"{Colors.Y}{ms}ms{Colors.RESET}" if ms < 400 else f"{Colors.R}{ms}ms{Colors.RESET}"
        marker = " ← အကောင်းဆုံး!" if ms < best_ms else ""
        print(f"  [{i:2d}] ✅ {item['name'][:30]:<32} {status}{marker}")
        
        if ms < best_ms:
            best_ms = ms
            best = item
            if ms < 100:
                break
    
    print()
    if best:
        print(f"{Colors.G}{'═'*55}{Colors.RESET}")
        print(f"{Colors.G} 🏆 အကောင်းဆုံးဆာဗာ{Colors.RESET}")
        print(f"  📌 အမည်: {best['name']}")
        print(f"  📶 မြန်နှုန်း: {Colors.G}{best_ms}ms{Colors.RESET}")
        print(f"  🔑 ကီး:")
        print(f"  {Colors.W}{best['key']}{Colors.RESET}")
        print(f"{Colors.G}{'═'*55}{Colors.RESET}")
        
        if copy_key(best["key"]):
            print(f"  ✅ ကီးကို ကူးယူပြီးပါပြီ! VPN အက်ပ်ထဲတွင် ကူးထည့်ပါ။")
        else:
            print(f"  ⚠️ အထက်ကကီးကို ကိုယ်တိုင်ကူးယူပါ")
    else:
        print(f"  {Colors.Y}⚠️ ဆာဗာအားလုံး မတုံ့ပြန်ပါ{Colors.RESET}")
        print(f"  ပထမဆုံးကီးကို ပြပေးမည်-")
        print(f"  🔑 {keys[0]['key']}")
        if copy_key(keys[0]["key"]):
            print(f"  ✅ ကူးယူပြီးပါပြီ!")
    
    input("\n  ပြီးဆုံးရန် Enter နှိပ်ပါ...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  👋 ပျော်ရွှင်ဖွယ်ရှိပါစေ!")
    except Exception as e:
        print(f"\n  {Colors.R}အမှား: {str(e)}{Colors.RESET}")
        input("  ထွက်ရန် Enter နှိပ်ပါ...")
                    
