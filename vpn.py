#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import json
import os
import socket
import time
from datetime import datetime

ဗားရှင်း = "5.4 ⚡ အမြန်"
ဖိုင်လမ်းကြောင်း = os.path.join(os.path.expanduser("~"), "vpn-key-bot", "သိမ်းထားများ.txt")

class အရောင်များ:
    အပြာ = "\033[96m"
    အစိမ်း = "\033[92m"
    အဝါ = "\033[93m"
    အနီ = "\033[91m"
    အဖြူ = "\033[97m"
    ပုံမှန် = "\033[0m"
အရောင် = အရောင်များ()

ဦးစားပေးနိုင်ငံများ = ["singapore", "malaysia", "thailand", "vietnam", "hong", "japan", "korea"]

def ဖန်သားပြင်ရှင်း():
    os.system("clear")

def ခေါင်းစဉ်():
    ဖန်သားပြင်ရှင်း()
    print(f"{အရောင်အပြာ}{'='*42}{အရောင်ပုံမှန်}")
    print(f"{အရောင်အပြာ}⚡ VPN ကီးရှာစက် — {ဗားရှင်း}{အရောင်ပုံမှန်}")
    print(f"{အရောင်အပြာ}{'='*42}{အရောင်ပုံမှန်}\n")

def အလံ(အမည်):
    စာ = အမည်.lower()
    if "singapore" in စာ: return "🇸🇬"
    if "malaysia" in စာ: return "🇲🇾"
    if "thailand" in စာ: return "🇹🇭"
    if "vietnam" in စာ: return "🇻🇳"
    if "hong" in စာ: return "🇭🇰"
    if "japan" in စာ: return "🇯🇵"
    if "korea" in စာ: return "🇰🇷"
    return "🌐"

def pingစစ်(host, port=443, စောင့်ချိန်=0.3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(စောင့်ချိန်)
        စ = time.time()
        s.connect((host, int(port)))
        s.close()
        return round((time.time() - စ) * 1000)
    except:
        return 9999

def အချက်အလက်ရယူ(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as res:
            return json.loads(res.read().decode())
    except:
        return None

def ကီးများရယူ():
    ကီးစာရင်း = []
    ဒေတာ = အချက်အလက်ရယူ("https://shadowmere.xyz/api/sub/")
    if ဒေတာ and isinstance(ဒေတာ, list):
        for x in ဒေတာ:
            ကီး = x.get("url") or x.get("link") or ""
            အမည် = x.get("name") or "ဆာဗာ"
            if ကီး and ("vless://" in ကီး or "ss://" in ကီး):
                ဦးစားပေး = 99
                for i, နိုင်ငံ in enumerate(ဦးစားပေးနိုင်ငံများ):
                    if နိုင်ငံ in အမည်.lower():
                        ဦးစားပေး = i
                        break
                ကီးစာရင်း.append({"အမည်":အမည်, "ကီး":ကီး, "ဦးစားပေး":ဦးစားပေး})
    ကီးစာရင်း.sort(key=lambda x: x["ဦးစားပေး"])
    return ကီးစာရင်း[:15]

def hostထုတ်(ကီး):
    try:
        if "://" in ကီး:
            from urllib.parse import urlparse
            return urlparse(ကီး).hostname or ""
    except:
        return ""

def ကူးယူ(စာသား):
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", စာသား])
        return True
    except:
        return False

def အကောင်းဆုံးရှာ():
    ခေါင်းစဉ်()
    print("  🔍 အကောင်းဆုံးဆာဗာကို ရှာဖွေနေသည်...")
    print("  📍 ဦးစားပေး → စင်ကာပူ > မလေးရှား > ထိုင်း > ဗီယက်နမ် > ဟောင်ကောင်း > ဂျပန် > ကိုရီးယား\n")
    
    ကီးများ = ကီးများရယူ()
    if not ကီးများ:
        print(f"  {အရောင်အနီ}❌ ကီးမရှိပါ{အရောင်ပုံမှန်}")
        input("  ရှေ့ဆက်ရန် Enter နှိပ်ပါ...")
        return
    
    အကောင်းဆုံးms = 9999
    အကောင်းဆုံး = None
    
    for i, ပစ္စည်း in enumerate(ကီးများ, 1):
        လိပ်စာ = hostထုတ်(ပစ္စည်း["ကီး"])
        if not လိပ်စာ:
            continue
        ms = pingစစ်(လိပ်စာ)
        ပြသမှု = f"{အရောင်အစိမ်း}{ms}ms{အရောင်ပုံမှန်}" if ms < 200 else f"{အရောင်အနီ}{ms}ms{အရောင်ပုံမှန်}"
        print(f"  {အလံ(ပစ္စည်း['အမည်'])} {i}. {ပစ္စည်း['အမည်'][:25]:<28} → {ပြသမှု}")
        
        if ms < အကောင်းဆုံးms:
            အကောင်းဆုံးms = ms
            အကောင်းဆုံး = ပစ္စည်း
            if ms < 80:
                break
    
    if not အကောင်းဆုံး:
        print(f"\n  {အရောင်အနီ}❌ မည်သည့်ဆာဗာမှ အကျဉ်းမတုံ့ပြန်ပါ{အရောင်ပုံမှန်}")
        return
    
    အချိန် = datetime.now().strftime("%H:%M:%S")
    print(f"\n{အရောင်အစိမ်း}{'='*42}{အရောင်ပုံမှန်}")
    print(f"{အရောင်အစိမ်း} ✅ အကောင်းဆုံး - {အလံ(အကောင်းဆုံး['အမည်'])} {အကောင်းဆုံး['အမည်']}{အရောင်ပုံမှန်}")
    print(f" 📶 မြန်နှုန်း: {အရောင်အစိမ်း}{အကောင်းဆုံးms}ms{အရောင်ပုံမှန်}  🕐 အချိန်: {အချိန်}")
    print(f"{အရောင်အစိမ်း}{'='*42}{အရောင်ပုံမှန်}")
    print(f"\n  🔑 ကီး:\n  {အရောင်အဖြူ}{အကောင်းဆုံး['ကီး']}{အရောင်ပုံမှန်}\n")
    
    if ကူးယူ(အကောင်းဆုံး["ကီး"]):
        print(f"  {အရောင်အစိမ်း}✅ ကီးကို ကူးယူပြီးပါပြီ!{အရောင်ပုံမှန်}")
    else:
        print(f"  ⚠️ အထက်ကကီးကို ကိုယ်တိုင်ကူးယူပါ")
    
    input("\n  ပိတ်ရန် Enter နှိပ်ပါ...")

def မီနူး():
    while True:
        ခေါင်းစဉ်()
        print("  ⚡ [F] အကောင်းဆုံးကို ချက်ချင်းရှာမည်")
        print("  🚪 [X] ပိတ်မည်\n")
        ရွေးချယ်မှု = input("  ရွေးချယ်ပါ: ").strip().upper()
        if ရွေးချယ်မှု == "F":
            အကောင်းဆုံးရှာ()
        elif ရွေးချယ်မှု == "X":
            print("  👋 ပျော်ရွှင်ဖွယ်ရှိပါစေ!")
            break

if __name__ == "__main__":
    try:
        မီနူး()
    except KeyboardInterrupt:
        print("\n  👋 ပျော်ရွှင်ဖွယ်ရှိပါစေ!")
