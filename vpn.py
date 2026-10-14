#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import base64
import os
import socket
import time
import json
from datetime import datetime

VERSION = "PREMIUM SIMPLE 1.0 ⚡"
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
def line(): print(f"{C.B}{'═'*55}{C.N}")

def logo():
    clear()
    line()
    print(f"{C.G}⚡ VPN KEY FINDER — PREMIUM EDITION  {VERSION}{C.N}")
    line()
    print()

# ==================================================
# 📋 အရင်းအမြစ်များ (အလုပ်လုပ်နေသမျှကိုသာ ထည့်ထားသည်)
# ==================================================
SOURCES = [
    {
        "name": "Shadowmere",
        "url": "https://shadowmere.xyz/api/b64sub/",
        "type": "b64"
    },
    {
        "name": "Epodonios VLESS",
        "url": "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/vless.txt",
        "type": "txt"
    },
    {
        "name": "Epodonios SS",
        "url": "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/Splitted-By-Protocol/ss.txt",
        "type": "txt"
    },
    {
        "name": "MatinGhanbari VLESS",
        "url": "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/vless.txt",
        "type": "txt"
    },
    {
        "name": "MatinGhanbari SS",
        "url": "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/ss.txt",
        "type": "txt"
    },
    {
        "name": "Argh73 All",
        "url": "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt",
        "type": "txt"
    }
]

# ==================================================
# ⭐ အကြိုက်ဆုံးများ
# ==================================================
def load_favorites():
    if os.path.exists(FAV_FILE):
        try:
            with open(FAV_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_favorite(item):
    favs = load_favorites()
    if any(f["key"] == item["key"] for f in favs):
        return False
    fav_item = {
        "name": item["name"],
        "key": item["key"],
        "proto": item.get("proto", "unknown"),
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    favs.insert(0, fav_item)
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(favs, f, ensure_ascii=False, indent=2)
    return True

def copy_text(text):
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set", text])
        return True
    except:
        return False

# ==================================================
# 📥 ဒေတာဖတ်ခြင်း
# ==================================================
def fetch_source(src):
    try:
        req = urllib.request.Request(
            src["url"],
            headers={"User-Agent": "Mozilla/5.0 (Android; Mobile)"}
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  {C.Y}⚠️ {src['name']}: မအောင်မြင်{C.N}")
        return None

def parse_configs(content, src_type):
    keys = []
    if not content:
        return keys
    
    if src_type == "b64":
        try:
            content = base64.b64decode(content).decode("utf-8", errors="ignore")
        except:
            pass
    
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        
        proto = None
        if line.startswith("vless://"):
            proto = "vless"
        elif line.startswith("ss://"):
            proto = "ss"
        elif line.startswith("vmess://"):
            proto = "vmess"
        
        if not proto:
            continue
        
        name = f"{proto.upper()} Server"
        if "#" in line:
            try:
                from urllib.parse import unquote
                name = unquote(line.split("#")[-1])[:45]
            except:
                name = line.split("#")[-1][:45]
        
        keys.append({"name": name, "key": line, "proto": proto})
    
    return keys

# ==================================================
# 📊 စမ်းသပ်ခြင်း
# ==================================================
def get_host(key):
    try:
        from urllib.parse import urlparse
        u = urlparse(key)
        return u.hostname or "", u.port or 443
    except:
        return "", 443

def ping_server(host, port=443, timeout=0.8):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        st = time.time()
        s.connect((host, int(port)))
        s.close()
        return round((time.time() - st) * 1000)
    except:
        return 9999

def get_country_flag(name):
    n = name.lower()
    if "singapore" in n or "sg" in n: return "🇸🇬 SG"
    if "malaysia" in n or "my" in n: return "🇲🇾 MY"
    if "thai" in n or "th" in n: return "🇹🇭 TH"
    if "vietnam" in n or "vn" in n: return "🇻🇳 VN"
    if "hongkong" in n or "hk" in n: return "🇭🇰 HK"
    if "japan" in n or "jp" in n: return "🇯🇵 JP"
    if "korea" in n or "kr" in n: return "🇰🇷 KR"
    if "india" in n or "in" in n: return "🇮🇳 IN"
    if "uk" in n or "gb" in n or "london" in n: return "🇬🇧 UK"
    if "usa" in n or "us" in n or "united states" in n: return "🇺🇸 US"
    return "🌐 --"

def ping_result(ms):
    if ms == 9999: return f"{C.R}❌ မတုံ့ပြန်{C.N}"
    if ms < 100: return f"{C.G}✅ {ms}ms  အလွန်မြန်{C.N}"
    if ms < 200: return f"{C.G}✅ {ms}ms  ကောင်း{C.N}"
    if ms < 350: return f"{C.Y}⚠️ {ms}ms  အတန်းအစား{C.N}"
    return f"{C.R}❌ {ms}ms  နှေး{C.N}"

# ==================================================
# 🔍 အဓိကလုပ်ဆောင်ချက် — ကီးရှာဖွေခြင်း
# ==================================================
def load_all_keys():
    all_keys = []
    seen = set()
    
    logo()
    print(f"{C.B}📡 အရင်းအမြစ်များမှ ကီးများရယူနေသည်...{C.N}\n")
    
    for src in SOURCES:
        print(f"  🔍 {src['name']}...", end=" ")
        content = fetch_source(src)
        if content:
            keys = parse_configs(content, src["type"])
            new_count = 0
            for k in keys:
                if k["key"] not in seen:
                    seen.add(k["key"])
                    all_keys.append(k)
                    new_count += 1
            print(f"{C.G}✅ +{new_count}  (စုစုပေါင်း: {len(all_keys)}){C.N}")
        else:
            print(f"{C.Y}ကျော်သွား{C.N}")
    
    print()
    if len(all_keys) == 0:
        print(f"{C.R}❌ ကီးမရရှိသေးပါ။ နောက်မှတစ်ခါပြန်ကြိုးစားပါ။{C.N}")
    else:
        print(f"{C.G}✅ စုစုပေါင်း ကီး {len(all_keys)} ခု အဆင်သင့်ဖြစ်ပါပြီ!{C.N}")
    time.sleep(1)
    return all_keys

def find_best_servers(keys, limit=15):
    if not keys:
        return []
    
    logo()
    print(f"{C.B}⚡ လိုင်းကောင်းဆာဗာများကို ရွေးချယ်နေသည်...{C.N}\n")
    
    results = []
    total = min(len(keys), limit)
    
    for i in range(total):
        k = keys[i]
        host, port = get_host(k["key"])
        ms = ping_server(host, port) if host else 9999
        
        results.append({
            "name": k["name"],
            "key": k["key"],
            "proto": k["proto"],
            "ms": ms
        })
        print(f"  [{i+1}/{total}] စမ်းသပ်ပြီး", end="\r")
    
    print("\n\n")
    
    good = [r for r in results if r["ms"] < 400]
    good.sort(key=lambda x: x["ms"])
    
    return good

# ==================================================
# 📋 ပြသခြင်းများ
# ==================================================
def show_best_list(good_keys, title="ဆာဗာများ"):
    if not good_keys:
        print(f"{C.Y}⚠️ လိုင်းကောင်းဆာဗာ မတွေ့ပါ။ ပြန်စကင်န်ဖတ်ကြည့်ပါ။{C.N}")
        return None
    
    print(f"{C.G}🏆 အကောင်းဆုံး {title}  (အရေအတွက်: {len(good_keys)}){C.N}\n")
    print(f"  #   နိုင်ငံ   ပရိုတို   Ping          အမည်")
    line()
    
    for i, r in enumerate(good_keys, 1):
        flag = get_country_flag(r["name"])
        print(f"  {i}   {flag}   {r['proto'].upper():<6}   {ping_result(r['ms']):<25} {r['name'][:30]}")
    
    return good_keys

def show_detail_and_copy(server_list, limit=3):
    if not server_list:
        return
    
    top = server_list[:limit]
    
    print(f"\n{C.G}📌 အကောင်းဆုံး {len(top)} ခု၏ ကီးများ{C.N}")
    line()
    
    all_keys_text = "\n\n".join([r["key"] for r in top])
    print(all_keys_text)
    line()
    
    if len(top) == 1:
        copied = copy_text(top[0]["key"])
    else:
        copied = copy_text(all_keys_text)
    
    if copied:
        print(f"{C.G}✅ ကီးများကို ကလစ်ဘုတ်သို့ ကူးယူပြီးပါပြီ!{C.N}")
        print(f"{C.B}💡 V2RayNG / NekoBox → + → Import from Clipboard နှိပ်ပါ{C.N}")
    else:
        print(f"{C.Y}⚠️ ကူးယူ၍မရပါ။ အထက်ကကီးကို ကိုယ်တိုင်ကူးယူပါ။{C.N}")
    
    return top

def show_favorites_menu():
    while True:
        favs = load_favorites()
        logo()
        print(f"{C.M}⭐ အကြိုက်ဆုံးဆာဗာများ  (စုစုပေါင်း: {len(favs)} ခု){C.N}\n")
        
        if not favs:
            print(f"{C.Y}အကြိုက်ဆုံး မသိမ်းရသေးပါ။ ကီးတစ်ခုရွေးပြီး သိမ်းထားနိုင်ပါတယ်။{C.N}")
        else:
            for i, f in enumerate(favs, 1):
                flag = get_country_flag(f["name"])
                print(f"  [{i}] {flag}  {f['name'][:35]}  |  {f['proto'].upper()}")
                print(f"      💾 သိမ်းဆည်းခဲ့သည်: {f['saved_at']}")
                print(f"      🔑 {f['key'][:50]}...")
                print()
            
            print(f"  {C.G}နံပါတ်ထည့်ပါ = ကီးကူးယူမည်{C.N}")
        
        print(f"  {C.R}[0] = ပင်မမီနူးသို့ ပြန်သွားရန်{C.N}")
        sel = input(f"\nရွေးချယ်ပါ → ").strip()
        
        if sel == "0":
            break
        elif sel.isdigit() and favs:
            idx = int(sel) - 1
            if 0 <= idx < len(favs):
                copy_text(favs[idx]["key"])
                print(f"  {C.G}✅ ကီးကူးယူပြီးပါပြီ!{C.N}")
                time.sleep(1)

def network_tips():
    logo()
    print(f"{C.B}📱 ကွန်ရက်အလိုက် အကောင်းဆုံးနိုင်ငံ{C.N}\n")
    print(f"  MPT     → 🇸🇬 SG စင်ကာပူ  သို့မဟုတ်  🇹🇭 TH ထိုင်း")
    print(f"  Ooredoo → 🇸🇬 SG စင်ကာပူ  သို့မဟုတ်  🇲🇾 MY မလေးရှား")
    print(f"  Telenor → 🇸🇬 SG စင်ကာပူ  သို့မဟုတ်  🇲🇾 MY မလေးရှား")
    print(f"  Mytel   → 🇹🇭 TH ထိုင်း    သို့မဟုတ်  🇻🇳 VN ဗီယက်နမ်")
    print(f"  WiFi    → 🇸🇬 SG စင်ကာပူ  အမြဲပိုမိုမြန်ဆန်တယ်")
    print(f"\n  💡 စည်းမျဉ်း: Ping < 200ms = အကောင်းဆုံး ✅  |  200-400ms = အတန်းအစား ⚠️  |  >400ms = ပြောင်းသင့် ❌")
    print()
    input(f"ပြန်ရန် Enter...")

# ==================================================
# 🏠 ပင်မမီနူး
# ==================================================
def main():
    all_keys = load_all_keys()
    vless_keys = [k for k in all_keys if k["proto"] == "vless"]
    ss_keys = [k for k in all_keys if k["proto"] == "ss"]
    vmess_keys = [k for k in all_keys if k["proto"] == "vmess"]
    
    while True:
        logo()
        print(f"{C.B}📋 ပင်မမီနူး{C.N}\n")
        print(f"  🟦 VLESS: {C.G}{len(vless_keys)}{C.N} ခု   🟩 SS: {C.G}{len(ss_keys)}{C.N} ခု   🟧 VMess: {C.G}{len(vmess_keys)}{C.N} ခု")
        print()
        print(f"  {C.G}[1]{C.N} ⚡ အကောင်းဆုံး VLESS ကို ရှာမည်")
        print(f"  {C.G}[2]{C.N} 🟩 အကောင်းဆုံး SS ကို ရှာမည်")
        print(f"  {C.G}[3]{C.N} 🏆 အားလုံးထဲမှ အကောင်းဆုံး ၃ ခု")
        print(f"  {C.G}[4]{C.N} ⭐ အကြိုက်ဆုံးဆာဗာများ")
        print(f"  {C.G}[5]{C.N} 📱 ကွန်ရက်အကြံပြုချက်")
        print(f"  {C.G}[6]{C.N} 🔄 ကီးအသစ်ပြန်ဖတ်မည်")
        print(f"  {C.R}[0]{C.N} ❌ ထွက်ပါ")
        print()
        
        sel = input(f"ရွေးချယ်ပါ → ").strip()
        
        if sel == "1":
            if not vless_keys:
                print(f"{C.Y}⚠️ VLESS ကီးမရှိပါ။ အခြားအမျိုးအစားကို ကြည့်ပါ။{C.N}")
                time.sleep(1)
                continue
            good = find_best_servers(vless_keys)
            show_best_list(good, "VLESS ဆာဗာများ")
            if good:
                show_detail_and_copy(good)
                if input(f"\nအကောင်းဆုံးကို အကြိုက်ဆုံးထဲသိမ်းမလား? (y/n) → ").strip().lower() == "y":
                    save_favorite(good[0])
                    print(f"{C.G}✅ သိမ်းပြီးပါပြီ! ⭐{C.N}")
            input(f"\nပြန်ရန် Enter...")
        
        elif sel == "2":
            if not ss_keys:
                print(f"{C.Y}⚠️ SS ကီးမရှိပါ။ အခြားအမျိုးအစားကို ကြည့်ပါ။{C.N}")
                time.sleep(1)
                continue
            good = find_best_servers(ss_keys)
            show_best_list(good, "SS ဆာဗာများ")
            if good:
                show_detail_and_copy(good)
                if input(f"\nအကောင်းဆုံးကို အကြိုက်ဆုံးထဲသိမ်းမလား? (y/n) → ").strip().lower() == "y":
                    save_favorite(good[0])
                    print(f"{C.G}✅ သိမ်းပြီးပါပြီ! ⭐{C.N}")
            input(f"\nပြန်ရန် Enter...")
        
        elif sel == "3":
            if not all_keys:
                print(f"{C.Y}⚠️ ကီးမရှိပါ။ အရင်ဖတ်ပါ။{C.N}")
                time.sleep(1)
                continue
            good = find_best_servers(all_keys, limit=20)
            show_best_list(good, "အားလုံးမှ အကောင်းဆုံး")
            if good:
                show_detail_and_copy(good, limit=3)
            input(f"\nပြန်ရန် Enter...")
        
        elif sel == "4":
            show_favorites_menu()
        
        elif sel == "5":
            network_tips()
        
        elif sel == "6":
            all_keys = load_all_keys()
            vless_keys = [k for k in all_keys if k["proto"] == "vless"]
            ss_keys = [k for k in all_keys if k["proto"] == "ss"]
            vmess_keys = [k for k in all_keys if k["proto"] == "vmess"]
        
        elif sel == "0":
            print(f"{C.G}👋 အသုံးပြုတာကျေးဇူးတင်ပါတယ်! ပျော်ရွှင်ဖွယ်ရှိပါစေ။{C.N}")
            break
        
        else:
            print(f"{C.R}❌ ရွေးချယ်မှုမှားနေပါသည်။ 0-6 ကြားသာထည့်ပါ။{C.N}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{C.G}👋 ပရိုဂရမ်မှ ထွက်သွားပါပြီ{C.N}")
    except Exception as e:
        print(f"\n{C.R}အမှားအယွင်း: {str(e)}{C.N}")
        input(f"ဆက်ရန် Enter...")
    
