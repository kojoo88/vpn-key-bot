#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

# ================== REAL PING TEST ==================
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
    codes = ["SG", "US", "JP", "KR", "HK", "TW", "UK", "DE", "NL", "CA", "AU", "IN", "TH", "MY", "FR", "IT", "ES", "BR", "FI", "SE", "PL", "CH", "IE", "NL", "AT", "BE", "DK", "NO"]
    text_upper = text.upper()
    for c in codes:
        if c in text_upper:
            return c
    return "??"

# ================== DECODE & PARSE ==================
def decode_b64_data(b64_text):
    try:
        decoded = base64.b64decode(b64_text).decode("utf-8", errors="ignore")
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
        return keys
    except Exception as e:
        print(f"{RED}Decode Error: {e}{RST}")
        return []

# ================== MAIN ==================
def main():
    clear()
    print(PUR + "="*60 + RST)
    print(PUR + "|    🚀 SHADOWMERE B64 - VPN KEY FINDER   |" + RST)
    print(PUR + "="*60 + RST)
    
    print(f"\n{CYN}📋 လမ်းညွှန်:{RST}")
    print(f"  1. ဘရောက်ဆာဖွင့် → https://shadowmere.xyz/api/b64sub/ ကိုသွားပါ")
    print(f"  2. စာသားအားလုံး ကူးယူပါ")
    print(f"  3. ဒီမှာ Paste လုပ်ပါ → ပြီးရင် Enter နှစ်ခုနှိပ်ပါ\n")
    
    print(f"{PUR}▼ B64 စာသားကို ဒီမှာ ကူးထည့်ပါ ▼{RST}")
    lines = []
    while True:
        try:
            l = input()
            if not l:
                break
            lines.append(l)
        except:
            break
    
    b64_text = "".join(lines).strip()
    if not b64_text:
        print(f"\n{RED}❌ စာသားမရှိပါ။ ပြန်စပါ။{RST}")
        time.sleep(1.5)
        return
    
    print(f"\n{GRN}⏳ ကုဒ်ဖွင့်နေသည်...{RST}")
    keys = decode_b64_data(b64_text)
    
    if not keys:
        print(f"{RED}❌ ကီးမတွေ့ပါ။ စာသားမှန်ကန်မှုစစ်ပါ။{RST}")
        input(f"\n ပြန်ရန် Enter...")
        return
    
    print(f"{GRN}✅ စုစုပေါင်း {len(keys)} ခု တွေ့ရှိခဲ့သည်!{RST}")
    input(f" ဆက်ရန် Enter...")
    
    # Test ping and sort
    clear()
    print(PUR + "="*70 + RST)
    print(PUR + "|       📡 တကယ့် Ping တိုင်းနေသည်...         |" + RST)
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
        print(f"\n{PUR}[{idx}] {s['country']}{RST}  |  IP: {CYN}{s.get('ip', 'N/A')}{RST}")
        print(f"      Ping: {CYN}{s['ms']}ms{RST}  |  {stars}  {GRN}{s['lvl']}{RST}")
        print(f"      Port: {s.get('port', 'N/A')}")
        print(f"{WHT}{s['url']}{RST}")
        print(PUR + "-"*70 + RST)
    
    input(f"\n  ပြီးပါပြီ။ Exit ရန် Enter...")

if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        clear()
        print(f"\n\n  {GRN}ပြီးပါပြီ။ Bye! 👋{RST}\n")
        sys.exit(0)
            
