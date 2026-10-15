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

FAV_FILE = "favorites.txt"
KEYS_FILE = "saved_keys.txt"

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
            return code, name
    return "??", "🌍 အခြား"

# ================== FAVORITES ==================
def load_favorites():
    if not os.path.exists(FAV_FILE):
        return []
    try:
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def save_favorite(url):
    favs = load_favorites()
    if url not in favs:
        favs.append(url)
        with open(FAV_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(favs))
        return True
    return False

def remove_favorite(url):
    favs = load_favorites()
    if url in favs:
        favs.remove(url)
        with open(FAV_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(favs))
        return True
    return False

# ================== SAVE TO FILE ==================
def save_keys_to_file(keys):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(KEYS_FILE, "w", encoding="utf-8") as f:
            f.write(f"ရယူချိန်: {timestamp}\n")
            f.write(f"စုစုပေါင်း: {len(keys)} ခု\n")
            f.write("="*60 + "\n")
            for idx, k in enumerate(keys, 1):
                f.write(f"\n[{idx}] {k['country']}\n")
                f.write(f"{k['url']}\n")
        return True
    except:
        return False

# ================== LOAD KEYS ==================
def load_keys_from_url():
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
        return None, None
    
    load_time = datetime.now().strftime("%H:%M:%S")
    print(f"{GRN}✅ ဒေတာရရှိပြီ!  ရယူချိန်: {load_time}{RST}")
    
    try:
        decoded = base64.b64decode(b64_content).decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"{RED}❌ ဖွင့်၍မရပါ: {e}{RST}")
        input("  ပြန်ရန် Enter...")
        return None, None
    
    lines = decoded.splitlines()
    keys = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("ss://"):
            code, name = get_country(line)
            ip, port = extract_ip_port(line)
            keys.append({
                "code": code,
                "country": name,
                "url": line,
                "ip": ip,
                "port": port
            })
    
    if not keys:
        print(f"{RED}❌ ကီးမတွေ့ပါ{RST}")
        input("  ပြန်ရန် Enter...")
        return None, None
    
    print(f"{GRN}✅ စုစုပေါင်း {len(keys)} ခု တွေ့ရှိခဲ့သည်!{RST}")
    input("  ဆက်ရန် Enter...")
    return keys, load_time

# ================== DISPLAY KEYS ==================
def display_key(s, idx=None, show_fav_btn=False):
    idx_str = f"[{idx}]" if idx else ""
    stars = "⭐" * s.get("sc", 0) + "☆" * (5 - s.get("sc", 0))
    ping_str = f"  Ping: {CYN}{s['ms']}ms{RST}" if "ms" in s else ""
    lvl_str = f"  |  {stars}  {s.get('lvl', '')}" if "lvl" in s else ""
    
    print(f"\n{PUR}{idx_str} {s['country']}{ping_str}{lvl_str}{RST}")
    print(f"{GRN}🔑 ကီးကို အောက်ကနေ ကူးယူပါ 👇{RST}")
    print(f"{WHT}{s['url']}{RST}")
    
    if show_fav_btn:
        favs = load_favorites()
        is_fav = s['url'] in favs
        if is_fav:
            print(f"{YEL}❤️  အကြိုက်ဆုံးဖြစ်နေသည် | ဖယ်ရှားလိုပါက 'U+နံပါတ်' ရိုက်ပါ{RST}")
        else:
            print(f"{GRN}🤍 အကြိုက်ဆုံးထဲထည့်လိုပါက 'F+နံပါတ်' ရိုက်ပါ (ဥပမာ: F1){RST}")
    print(PUR + "-"*70 + RST)

# ================== MAIN MENU ==================
def main():
    keys = []
    load_time = ""
    
    while True:
        clear()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(PUR + "="*60 + RST)
        print(PUR + f"|   🚀 SHADOWMERE B64 - KEY FINDER        |" + RST)
        print(PUR + f"|   📅 စတင်ချိန်: {now}{' '*(32-len(now))}|" + RST)
        print(PUR + "="*60 + RST)
        print(f"  [1] 📋 ကီးအားလုံးကို ကြည့်မည်")
        print(f"  [2] ⚡ Ping တိုင်းပြီး အမြန်ဆုံးရှာမည်")
        print(f"  [3] 🔍 နိုင်ငံအလိုက် ရှာဖွေမည်")
        print(f"  [4] ⭐ အကြိုက်ဆုံး ဆာဗာများ")
        print(f"  [5] 💾 ကီးများကို ဖိုင်အဖြစ် သိမ်းမည်")
        print(f"  [6] 📱 အက်ပ်ထဲသို့ ထည့်သွင်းနည်း")
        print(f"  [7] 🔄 အလိုအလျောက် ပြန်လည်စစ်ဆေးမည်")
        print(f"  [0] ❌ ထွက်မည်")
        print(PUR + "="*60 + RST)
        
        choice = input("\n  ရွေးပါ -> ").strip()
        
        if choice == "0":
            print("\n  👋 ပြန်လာတော့မယ်! ဘယ်အချိန်မဆိုပြန်လာခဲ့နော်\n")
            break
        
        elif choice == "1":
            result = load_keys_from_url()
            if result[0] is None:
                continue
            keys, load_time = result
            
            clear()
            print(PUR + "="*70 + RST)
            print(PUR + "|        📋 ကီးအားလုံးပြသခြင်း             |" + RST)
            print(PUR + "="*70 + RST)
            print(f"  📅 ရယူချိန်: {load_time}")
            print(f"  📊 စုစုပေါင်း ဆာဗာ: {len(keys)} ခု")
            print(PUR + "-"*70 + RST)
            
            for idx, s in enumerate(keys, 1):
                display_key(s, idx, show_fav_btn=True)
            
            input("\n  ပြီးပါပြီ။ ပြန်ရန် Enter...")
        
        elif choice == "2":
            result = load_keys_from_url()
            if result[0] is None:
                continue
            keys, load_time = result
            
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
                    display_key(s, idx, show_fav_btn=True)
            else:
                print(f"{RED}❌ အလုပ်လုပ်နိုင်သောဆာဗာ မတွေ့ပါ{RST}")
            
            input("\n  ပြီးပါပြီ။ ပြန်ရန် Enter...")
        
        elif choice == "3":
            if not keys:
                print(f"{YEL}⚠️  အရင် [1] သို့မဟုတ် [2] ဖြင့် ကီးရယူပါ{RST}")
                time.sleep(1.5)
                continue
            
            clear()
            print(PUR + "="*60 + RST)
            print(PUR + "|        🔍 နိုင်ငံအလိုက် ရှာဖွေခြင်း       |" + RST)
            print(PUR + "="*60 + RST)
            print(f"  ရရှိနိုင်သောနိုင်ငံကုဒ်များ- SG, US, JP, KR, HK, TH, MY, IN...")
            code_input = input("\n  နိုင်ငံကုဒ်ထည့်ပါ (ဥပမာ- SG) -> ").strip().upper()
            
            filtered = [k for k in keys if k["code"] == code_input]
            
            if not filtered:
                print(f"{RED}❌ ထိုနိုင်ငံမှ ဆာဗာမတွေ့ပါ{RST}")
            else:
                print(f"{GRN}✅ {code_input} မှ {len(filtered)} ခု တွေ့ရှိခဲ့{RST}")
                print(PUR + "-"*70 + RST)
                for idx, s in enumerate(filtered, 1):
                    display_key(s, idx, show_fav_btn=True)
            
            input("\n  ပြန်ရန် Enter...")
        
        elif choice == "4":
            clear()
            print(PUR + "="*60 + RST)
            print(PUR + "|          ⭐ အကြိုက်ဆုံး ဆာဗာများ          |" + RST)
            print(PUR + "="*60 + RST)
            
            favs = load_favorites()
            if not favs:
                print(f"{YEL}❤️  အကြိုက်ဆုံး မရှိသေးပါ{RST}")
                print(f"  ကီးကြည့်နေစဉ် 'F1', 'F2' စသည်ဖြင့် ထည့်ပါ")
            else:
                print(f"{GRN}❤️  စုစုပေါင်း {len(favs)} ခု သိမ်းဆည်းထားသည်{RST}")
                print(PUR + "-"*70 + RST)
                for idx, url in enumerate(favs, 1):
                    print(f"\n{PUR}[{idx}]{RST}")
                    print(f"{WHT}{url}{RST}")
                    print(f"{YEL}ဖယ်ရှားလိုပါက 'U{idx}' ရိုက်ပါ{RST}")
                    print(PUR + "-"*70 + RST)
            
            input("\n  ပြန်ရန် Enter...")
        
        elif choice == "5":
            if not keys:
                print(f"{YEL}⚠️  အရင်ကီးရယူပါ{RST}")
                time.sleep(1.5)
                continue
            
            clear()
            print(PUR + "="*60 + RST)
            print(PUR + "|          💾 ဖိုင်အဖြစ် သိမ်းဆည်းခြင်း      |" + RST)
            print(PUR + "="*60 + RST)
            
            if save_keys_to_file(keys):
                print(f"{GRN}✅ အောင်မြင်စွာသိမ်းဆည်းပြီးပါပြီ!{RST}")
                print(f"  ဖိုင်နာမည်: {KEYS_FILE}")
                print(f"  ကြည့်လိုပါက: cat {KEYS_FILE}")
            else:
                print(f"{RED}❌ သိမ်းဆည်း၍မရပါ{RST}")
            
            input("\n  ပြန်ရန် Enter...")
        
        elif choice == "6":
            clear()
            print(PUR + "="*70 + RST)
            print(PUR + "|          📱 အက်ပ်ထဲသို့ ထည့်သွင်းနည်း      |" + RST)
            print(PUR + "="*70 + RST)
            print(f"""
{CYN}အက်ပ်ရွေးချယ်မှုများ:{RST}

📱 Android:
  • NekoBox
  • V2RayNG
  • Clash Meta

🍎 iOS:
  • Streisand
  • Shadowrocket

{CYN}ထည့်သွင်းနည်း (အက်ပ်အားလုံးအတွက် အလားတူ):{RST}

  အဆင့် ၁။ အက်ပ်ကိုဖွင့်ပါ
  အဆင့် ၂။ + သင်္ကေတ သို့မဟုတ် Add ခလုတ်ကိုနှိပ်ပါ
  အဆင့် ၃။ ကီးကို ကူးထည့်ပါ
  အဆင့် ၄။ ✅ သိမ်းပါ
  အဆင့် ၅။ ဆာဗာကိုရွေးပြီး ချိတ်ဆက်ပါ

{CYN}အမြန်နည်းလမ်း (အက်ပ်အားလုံးတွင်အလုပ်လုပ်သည်):{RST}
  ကီးကို ကူးယူပါ → အက်ပ်ထဲမှာ Paste လုပ်ပါ → ပြီးပါပြီ!
            """)
            input("\n  ပြန်ရန် Enter...")
        
        elif choice == "7":
            clear()
            print(PUR + "="*60 + RST)
            print(PUR + "|       🔄 အလိုအလျောက် ပြန်လည်စစ်ဆေးခြင်း    |" + RST)
            print(PUR + "="*60 + RST)
            print(f"  မိနစ်မည်မျှတိုင်း ပြန်စစ်မလား?")
            mins = input(f"  အချိန် (မိနစ်) ရိုက်ပါ -> ").strip()
            try:
                mins = int(mins)
                if mins < 1:
                    print(f"{RED}❌ အနည်းဆုံး ၁ မိနစ်ထည့်ပါ{RST}")
                    time.sleep(1.5)
                    continue
            except:
                print(f"{RED}❌ ဂဏန်းသာထည့်ပါ{RST}")
                time.sleep(1.5)
                continue
            
            print(f"{GRN}✅ {mins} မိနစ်တိုင်း ပြန်ဖတ်မည်...{RST}")
            print(f"{YEL}ရပ်တန့်လိုပါက Ctrl + C ကိုနှိပ်ပါ{RST}\n")
            
            try:
                while True:
                    next_time = datetime.now().strftime("%H:%M:%S")
                    print(f"{CYN}⏰ {next_time} — ဒေတာပြန်ဖတ်နေသည်...{RST}")
                    result = load_keys_from_url()
                    if result[0]:
                        keys, load_time = result
                        print(f"{GRN}✅ {len(keys)} ခု ရရှိပြီးပါပြီ{RST}")
                    print(f"{YEL}{mins} မိနစ်စောင့်နေသည်...{RST}\n")
                    time.sleep(mins * 60)
            except KeyboardInterrupt:
                print(f"\n{GRN}✅ ရပ်တန့်လိုက်ပါပြီ{RST}")
                input("  ပြန်ရန် Enter...")
        
        else:
            # Favorites add/remove
            if choice.upper().startswith("F") and choice[1:].isdigit():
                idx = int(choice[1:]) - 1
                if 0 <= idx < len(keys):
                    url = keys[idx]['url']
                    if save_favorite(url):
                        print(f"{GRN}✅ အကြိုက်ဆုံးထဲထည့်ပြီးပါပြီ!{RST}")
                    else:
                        print(f"{YEL}⚠️  အရင်ကတည်းက ရှိပြီးသားဖြစ်နေသည်{RST}")
                else:
                    print(f"{RED}❌ နံပါတ်မှားနေသည်{RST}")
                time.sleep(1.2)
            
            elif choice.upper().startswith("U") and choice[1:].isdigit():
                idx = int(choice[1:]) - 1
                favs = load_favorites()
                if 0 <= idx < len(favs):
                    if remove_favorite(favs[idx]):
                        print(f"{GRN}✅ အကြိုက်ဆုံးမှဖယ်ရှားပြီးပါပြီ{RST}")
                else:
                    print(f"{RED}❌ နံပါတ်မှားနေသည်{RST}")
                time.sleep(1.2)
            
            else:
                print(f"\n{RED}မှားနေတယ်၊ 0-7 သာရွေးပါ{RST}")
                time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("\n\n  👋 ပြန်လာတော့မယ်!\n")
        sys.exit(0)
        
