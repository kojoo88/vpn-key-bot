#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import base64
import os
import socket
import time
import json
from datetime import datetime

VERSION = "ULTIMATE PRO 2.0 ⚡"
FAV_FILE = os.path.expanduser("~/.vpn_favorites.json")

class C:
    G = "\033[92m"
    B = "\033[94m"
    Y = "\033[93m"
    R = "\033[91m"
    W = "\033[97m"
    M = "\033[95m"
    N = "\033[0m"

def clear(): os.system("clear")
def line(): print(f"{C.B}{'═'*60}{C.N}")

def logo():
    clear()
    line()
    print(f"{C.G}⚡ VPN KEY FINDER — ULTIMATE PRO  {VERSION}{C.N}")
    line()
    print()

# ==================================================
# 📂 အရင်းအမြစ် — Shadowmere တစ်ခုတည်း
# ==================================================
SOURCE_URL = "https://shadowmere.xyz/api/b64sub/"

# ==================================================
# ⭐ အကြိုက်ဆုံးဆာဗာ စီမံခန့်ခွဲမှု
# ==================================================
def load_favorites():
    if os.path.exists(FAV_FILE):
        try:
            with open(FAV_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_favorites(favs):
    try:
        with open(FAV_FILE, "w", encoding="utf-8") as f:
            json.dump(favs, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def add_favorite(item):
    favs = load_favorites()
    exists = any(f["key"] == item["key"] for f in favs)
    if exists:
        return False, "ရှိပြီးသားဖြစ်နေပါတယ်"
    fav_item = {
        "name": item["name"],
        "key": item["key"],
        "proto": item.get("proto", "unknown"),
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    favs.insert(0, fav_item)
    save_favorites(favs)
    return True, "အကြိုက်ဆုံးထဲ ထည့်ပြီးပါပြီ ⭐"

def remove_favorite(index):
    favs = load_favorites()
    if 0 <= index < len(favs):
        favs.pop(index)
        save_favorites(favs)
        return True, "ဖယ်ရှားပြီးပါပြီ"
    return False, "မမှန်ကန်ပါ"

# ==================================================
# 📥 ဒေတာဖတ်ခြင်း
# ==================================================
def fetch_source():
    print(f"{C.B}📥 Shadowmere မှ ကီးများရယူနေသည်...{C.N}")
    try:
        req = urllib.request.Request(
            SOURCE_URL,
            headers={"User-Agent": "Mozilla/5.0 (Android; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0"}
        )
        with urllib.request.urlopen(req, timeout=20) as res:
            content = res.read().decode("utf-8", errors="ignore")
        content = base64.b64decode(content).decode("utf-8", errors="ignore")
        print(f"{C.G}✅ ဒေတာဖတ်ပြီးပါပြီ{C.N}\n")
        return content
    except Exception as e:
        print(f"{C.R}❌ မအောင်မြင်: {str(e)}{C.N}")
        return None

def parse_keys(content):
    vless_keys = []
    ss_keys = []
    seen_vless = set()
    seen_ss = set()
    
    for line in content.splitlines():
        line = line.strip()
        if not line: continue
        
        name = "Server"
        if "#" in line:
            try:
                from urllib.parse import unquote
                name = unquote(line.split("#")[-1])[:45]
            except:
                name = line.split("#")[-1][:45]
        
        if line.startswith("vless://") and line not in seen_vless:
            seen_vless.add(line)
            vless_keys.append({"name": name, "key": line, "proto": "vless"})
        elif line.startswith("ss://") and line not in seen_ss:
            seen_ss.add(line)
            ss_keys.append({"name": name, "key": line, "proto": "ss"})
    
    return vless_keys, ss_keys

# ==================================================
# 📊 စမ်းသပ်မှုများ
# ==================================================
def get_host(key):
    try:
        from urllib.parse import urlparse
        u = urlparse(key)
        return u.hostname or "", u.port or 443
    except:
        return "", 443

def ping_server(host, port=443, timeout=0.6):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        st = time.time()
        s.connect((host, int(port)))
        s.close()
        return round((time.time()-st)*1000)
    except:
        return 9999

def speed_test(host, port=443):
    """ရိုးရှင်းတဲ့ ဒေါင်းလုဒ်အမြန်နှုန်း အကဲဖြတ်ချက်"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        st = time.time()
        s.connect((host, int(port)))
        # အသေးစားဒေတာပို့ပြီး အချိန်တိုင်းတာ
        s.send(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\nConnection: close\r\n\r\n")
        data = s.recv(1024)
        s.close()
        elapsed = time.time() - st
        # 1KB / အချိန် = kbps အကြမ်းဖက်တန်ဖိုး
        speed_kbps = round((len(data) / 1024) / elapsed * 8) if elapsed > 0 else 0
        return speed_kbps
    except:
        return 0

def flag(n):
    n = n.lower()
    if "singapore" in n or "sg" in n: return "🇸🇬 SG"
    if "malaysia" in n or "my" in n: return "🇲🇾 MY"
    if "thai" in n or "th" in n: return "🇹🇭 TH"
    if "vietnam" in n or "vn" in n: return "🇻🇳 VN"
    if "hongkong" in n or "hk" in n: return "🇭🇰 HK"
    if "japan" in n or "jp" in n: return "🇯🇵 JP"
    if "korea" in n or "kr" in n: return "🇰🇷 KR"
    if "india" in n or "in" in n: return "🇮🇳 IN"
    if "uk" in n or "gb" in n or "london" in n: return "🇬🇧 UK"
    if "germany" in n or "de" in n or "frankfurt" in n: return "🇩🇪 DE"
    if "canada" in n or "ca" in n: return "🇨🇦 CA"
    if "japan" in n or "jp" in n or "tokyo" in n: return "🇯🇵 JP"
    return "🌐 --"

def ping_str(ms):
    if ms == 9999: return f"{C.R}❌ မတုံ့ပြန်{C.N}"
    if ms < 100: return f"{C.G}✅ {ms}ms  အလွန်မြန်{C.N}"
    if ms < 200: return f"{C.G}✅ {ms}ms  ကောင်း{C.N}"
    if ms < 350: return f"{C.Y}⚠️ {ms}ms  အတန်းအစား{C.N}"
    return f"{C.R}❌ {ms}ms  နှေး{C.N}"

def speed_str(kbps):
    if kbps == 0: return f"{C.R}— မစမ်းနိုင်{C.N}"
    if kbps > 500: return f"{C.G}🔥 {kbps} kbps  အမြန်{C.N}"
    if kbps > 200: return f"{C.G}✅ {kbps} kbps  ကောင်း{C.N}"
    if kbps > 50: return f"{C.Y}⚠️ {kbps} kbps  နှေး{C.N}"
    return f"{C.R}🐢 {kbps} kbps  နှေးလွန်း{C.N}"

def copy_text(text):
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", text])
        return True
    except:
        return False

def network_tips():
    print(f"\n{C.B}📱 ကွန်ရက်အလိုက် အကြံပြုချက်{C.N}")
    print(f"  MPT     → 🇸🇬 SG စင်ကာပူ  သို့မဟုတ်  🇹🇭 TH ထိုင်း")
    print(f"  Ooredoo → 🇸🇬 SG စင်ကာပူ  သို့မဟုတ်  🇲🇾 MY မလေးရှား")
    print(f"  Telenor → 🇸🇬 SG စင်ကာပူ  သို့မဟုတ်  🇲🇾 MY မလေးရှား")
    print(f"  Mytel   → 🇹🇭 TH ထိုင်း    သို့မဟုတ်  🇻🇳 VN ဗီယက်နမ်")
    print(f"  WiFi    → 🇸🇬 SG စင်ကာပူ  အမြဲပိုမိုမြန်ဆန်တယ်")
    print(f"  💡 စည်းမျဉ်း: Ping < 200ms = အကောင်းဆုံး ✅  |  Speed > 200kbps = ကောင်းမွန် ✅")
    print()

# ==================================================
# 🔍 စကင်န်နှင့် အဆင့်အတန်းသတ်မှတ်ခြင်း
# ==================================================
def scan_servers(keys, limit=15):
    logo()
    print(f"{C.B}📊 ဆာဗာများကို စမ်းသပ်နေသည်...{C.N}")
    print(f"{C.Y}⏳ စက္ကန့်အနည်းငယ် စောင့်ပါ...{C.N}\n")
    
    results = []
    total = min(len(keys), limit)
    
    for i in range(total):
        k = keys[i]
        host, port = get_host(k["key"])
        ms = ping_server(host, port) if host else 9999
        spd = speed_test(host, port) if host and ms < 9999 else 0
        
        score = 0
        if ms < 9999:
            score += max(0, 500 - ms)
            score += spd * 0.1
        
        results.append({
            "name": k["name"],
            "key": k["key"],
            "proto": k["proto"],
            "ms": ms,
            "speed": spd,
            "score": score,
            "host": host
        })
        print(f"  [{i+1}/{total}] ပြီးပြီ", end="\r")
    
    print("\n\n")
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

# ==================================================
# 📋 ပြသခြင်းများ
# ==================================================
def show_top3(results):
    logo()
    print(f"{C.G}🏆 အကောင်းဆုံး ဆာဗာ ၃ ခု{C.N}\n")
    print(f"  #   နိုင်ငံ    Ping          အမြန်နှုန်း       အမည်")
    line()
    
    top3 = [r for r in results if r["ms"] < 9999][:3]
    
    if not top3:
        print(f"  {C.R}❌ မည်သည့်ဆာဗာမျှ မတုံ့ပြန်ပါ{C.N}")
        return []
    
    for i, r in enumerate(top3, 1):
        fl = flag(r["name"])
        print(f"  {i}   {fl}   {ping_str(r['ms']):<22} {speed_str(r['speed']):<18} {r['name'][:30]}")
    
    print()
    all_keys = "\n".join([r["key"] for r in top3])
    if copy_text(all_keys):
        print(f"{C.G}✅ ၃ ခုစလုံး ကလစ်ဘုတ်သို့ ကူးယူပြီးပါပြီ!{C.N}")
    else:
        print(f"{C.Y}⚠️ အထက်ကကီးများကို ကိုယ်တိုင်ကူးယူပါ{C.N}")
    
    return top3

def show_best_single(results):
    logo()
    print(f"{C.G}🏆 အကောင်းဆုံး ဆာဗာ{C.N}\n")
    
    best = None
    for r in results:
        if r["ms"] < 9999:
            best = r
            break
    
    if not best:
        print(f"{C.R}❌ မည်သည့်ဆာဗာမျှ မတုံ့ပြန်ပါ{C.N}")
        return None
    
    fl = flag(best["name"])
    print(f"  ပရိုတိုကော : {C.G}{best['proto'].upper()}{C.N}")
    print(f"  နိုင်ငံ    : {fl}")
    print(f"  အမည်      : {best['name'][:45]}")
    print(f"  📶 Ping     : {ping_str(best['ms'])}")
    print(f"  ⚡ အမြန်နှုန်း: {speed_str(best['speed'])}")
    print()
    print(f"{C.B}🔑 VPN Key{C.N}")
    print(f"  {C.W}{best['key']}{C.N}")
    print()
    
    if copy_text(best["key"]):
        print(f"{C.G}✅ ကီးကို ကလစ်ဘုတ်သို့ ကူးယူပြီးပါပြီ!{C.N}")
    
    print(f"\n  {C.M}[A] အကြိုက်ဆုံးထဲသို့ထည့်မလား  |  [Enter] ပြန်မယ်{C.N}")
    choice = input(f"ရွေးချယ်ပါ → ").strip().upper()
    if choice == "A":
        ok, msg = add_favorite(best)
        print(f"  {C.G if ok else C.Y}{msg}{C.N}")
        time.sleep(1)
    
    network_tips()
    return best

def show_all_list(results):
    logo()
    print(f"{C.B}📋 ဆာဗာအားလုံးစာရင်း (အကောင်းဆုံးအစီအစဉ်){C.N}\n")
    print(f"  #    နိုင်ငံ   ပရိုတိုကော   Ping          အမြန်နှုန်း")
    line()
    
    for i, r in enumerate(results, 1):
        fl = flag(r["name"])
        print(f"  {i:02d}   {fl}   {r['proto'].upper():<6}    {ping_str(r['ms']):<22} {speed_str(r['speed'])}")
    
    network_tips()

def show_favorites():
    while True:
        favs = load_favorites()
        logo()
        print(f"{C.M}⭐ အကြိုက်ဆုံးဆာဗာများ  (စုစုပေါင်း: {len(favs)} ခု){C.N}\n")
        
        if not favs:
            print(f"{C.Y}အကြိုက်ဆုံး မသိမ်းရသေးပါ{C.N}")
        else:
            for i, f in enumerate(favs, 1):
                print(f"  [{i}] {flag(f['name'])}  {f['name'][:35]}  |  {f['proto'].upper()}")
                print(f"      💾 သိမ်းဆည်းခဲ့သည်: {f['saved_at']}")
                print(f"      🔑 {f['key'][:60]}...")
                print()
        
        print(f"  {C.G}[C] ကီးကူးယူရန် နံပါတ်ထည့်ပါ  |  [D] ဖယ်ရန်  |  [0] ပြန်သွားရန်{C.N}")
        sel = input(f"ရွေးချယ်ပါ → ").strip()
        
        if sel == "0":
            break
        elif sel.isdigit():
            idx = int(sel) - 1
            if 0 <= idx < len(favs):
                copy_text(favs[idx]["key"])
                print(f"  {C.G}✅ ကီးကူးယူပြီးပါပြီ!{C.N}")
                time.sleep(1)
        elif sel.upper().startswith("D"):
            num = ''.join(filter(str.isdigit, sel))
            if num:
                idx = int(num) - 1
                ok, msg = remove_favorite(idx)
                print(f"  {C.G if ok else C.R}{msg}{C.N}")
                time.sleep(1)

# ==================================================
# 🎯 ပင်မမီနူးများ
# ==================================================
def run_protocol_menu(protocol_name, keys):
    while True:
        logo()
        print(f"{C.G}{protocol_name} မီနူး  (စုစုပေါင်း: {len(keys)} ခု){C.N}\n")
        print(f"  {C.G}[1]{C.N} 🏆 အကောင်းဆုံးတစ်ခုကို ရွေးပါ (Ping + Speed စစ်ဆေးပြီး){C.N}")
        print(f"  {C.G}[2]{C.N} 🥇🥈🥉 အကောင်းဆုံး ၃ ခုကို တစ်ပြိုင်နက်ကူးပါ{C.N}")
        print(f"  {C.G}[3]{C.N} 📋 အားလုံးစာရင်းကို ကြည့်ပါ{C.N}")
        print(f"  {C.G}[4]{C.N} ⭐ အကြိုက်ဆုံးဆာဗာများ{C.N}")
        print(f"  {C.G}[5]{C.N} 🔄 ပြန်လည်စကင်န်ဖတ်ပါ{C.N}")
        print(f"  {C.R}[0]{C.N} ← ပင်မမီနူးသို့ ပြန်သွားရန်{C.N}")
        print()
        
        sel = input(f"ရွေးချယ်ပါ → ").strip()
        
        if sel == "1":
            results = scan_servers(keys)
            show_best_single(results)
            input(f"\nပြန်ရန် Enter...")
        elif sel == "2":
            results = scan_servers(keys)
            show_top3(results)
            input(f"\nပြန်ရန် Enter...")
        elif sel == "3":
            results = scan_servers(keys, limit=20)
            show_all_list(results)
            input(f"\nပြန်ရန် Enter...")
        elif sel == "4":
            show_favorites()
        elif sel == "5":
            results = scan_servers(keys)
            input(f"ပြီးပါပြီ။ ပြန်ရန် Enter...")
        elif sel == "0":
            break

# ==================================================
# 🏠 ပင်မမီနူး
# ==================================================
def main():
    content = fetch_source()
    if not content:
        input(f"ထွက်ရန် Enter...")
        return
    
    vless_keys, ss_keys = parse_keys(content)
    
    while True:
        logo()
        print(f"{C.B}📋 ပင်မမီနူး{C.N}\n")
        print(f"  🟦 VLESS ကီးများ: {C.G}{len(vless_keys)}{C.N} ခု")
        print(f"  🟩 SS ကီးများ   : {C.G}{len(ss_keys)}{C.N} ခု")
        print()
        print(f"  {C.G}[1]{C.N} 🟦 VLESS ဆာဗာများကို ကြည့်မည်")
        print(f"  {C.G}[2]{C.N} 🟩 SS (Shadowsocks) ဆာဗာများကို ကြည့်မည်")
        print(f"  {C.G}[3]{C.N} ⭐ အကြိုက်ဆုံးဆာဗာများ")
        print(f"  {C.G}[4]{C.N} 📱 ကွန်ရက်အလိုက် အကြံပြုချက်")
        print(f"  {C.G}[5]{C.N} 🔄 အသစ်ပြန်လည်ဖတ်ရန်")
        print(f"  {C.R}[0]{C.N} ❌ ထွက်ပါ")
        print()
        
        sel = input(f"ရွေးချယ်ပါ → ").strip()
        
        if sel == "1":
            if vless_keys:
                run_protocol_menu("🟦 VLESS", vless_keys)
            else:
                print(f"{C.Y}⚠️ VLESS ကီးများမရှိပါ{C.N}")
                time.sleep(1)
        elif sel == "2":
            if ss_keys:
                run_protocol_menu("🟩 SS", ss_keys)
            else:
                print(f"{C.Y}⚠️ SS ကီးများမရှိပါ{C.N}")
                time.sleep(1)
        elif sel == "3":
            show_favorites()
        elif sel == "4":
            logo()
            network_tips()
            input(f"ပြန်ရန် Enter...")
        elif sel == "5":
            content = fetch_source()
            if content:
                vless_keys, ss_keys = parse_keys(content)
        elif sel == "0":
            print(f"{C.G}👋 ပျော်ရွှင်ဖွယ်ရှိပါစေ!{C.N}")
            break
        else:
            print(f"{C.R}❌ ရွေးချယ်မှုမှားနေပါသည်! 0-5 ကြားသာထည့်ပါ{C.N}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{C.G}👋 ပြီးပါပြီ{C.N}")
    except Exception as e:
        print(f"\n{C.R}အမှားအယွင်း: {str(e)}{C.N}")
        input(f"ဆက်ရန် Enter...")
    
