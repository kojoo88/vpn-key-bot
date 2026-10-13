#!/usr/bin/env python3
# VPN Key Generator — Premium Edition v5.3
import urllib.request
import urllib.error
import json
import base64
import os
import sys
import socket
import time
from datetime import datetime

os.environ["TERM"] = "xterm-256color"
VERSION = "5.3 ✨ PREMIUM"
FAV_FILE = os.path.expanduser("~/.vpn_favorites.txt")

class Colors:
    P = "\033[95m"
    C = "\033[96m"
    G = "\033[92m"
    Y = "\033[93m"
    R = "\033[91m"
    W = "\033[97m"
    D = "\033[90m"
    rst = "\033[0m"

API_LIST = {
    "1": ("Shadowmere JSON", "https://shadowmere.xyz/api/sub/", "json"),
    "2": ("Shadowmere Base64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    "3": ("VLESS List", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Splitted-By-Protocol/vless.txt", "txt")
}

# မြန်မာနိုင်ငံနှင့် နီးစပ်ရာ နိုင်ငံများ (ဦးစားပေးအစီအစဉ်)
NEARBY_COUNTRIES = [
    "singapore", "malaysia", "thailand", "vietnam", 
    "indonesia", "philippines", "hong kong", "hongkong", 
    "japan", "korea", "india", "australia"
]

def clear(): os.system("clear")
C = Colors()

def header():
    clear()
    fav_count = len(load_favorites())
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{C.P}╔══════════════════════════════════════════════════╗{C.rst}")
    print(f"{C.P}║{C.rst}{C.Y}  ✨ VPN KEY GENERATOR PREMIUM v{VERSION.split()[1]} ✨{C.rst}{C.P}║{C.rst}")
    print(f"{C.P}╠══════════════════════════════════════════════════╣{C.rst}")
    print(f"{C.P}║{C.rst}  {C.C}📡 Status:{C.rst} Online ✅  |  {C.C}⭐ Favorites:{C.rst} {fav_count}  {C.D}{now}{C.rst}{C.P}║{C.rst}")
    print(f"{C.P}╚══════════════════════════════════════════════════╝{C.rst}\n")

def divider(title=""):
    print(f"{C.C}─── {title} {'─'*(50-len(title))}{C.rst}" if title else f"{C.D}─"*52+C.rst)

def load_favorites():
    if not os.path.exists(FAV_FILE): return []
    try:
        with open(FAV_FILE,"r",encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except: return []

def save_favorite(name, key, ping="", uptime=""):
    favs = load_favorites()
    entry = f"{name}|{key}|{ping}|{uptime}"
    if entry not in favs:
        try:
            with open(FAV_FILE,"w",encoding="utf-8") as f:
                f.write("\n".join(favs+[entry]))
            return True
        except: return False
    return False

def copy_to_clipboard(text):
    try:
        with open("/dev/clipboard","w") as f: f.write(text)
        return True
    except: return False

def get_uptime_percent(ping_ms):
    if ping_ms < 100:
        return 100, f"{C.G}⚡ 100%{C.rst}"
    elif ping_ms < 150:
        return 90, f"{C.G}⚡ 90%{C.rst}"
    elif ping_ms < 200:
        return 75, f"{C.Y}⚡ 75%{C.rst}"
    elif ping_ms < 300:
        return 50, f"{C.Y}⚡ 50%{C.rst}"
    else:
        return 25, f"{C.R}⚡ 25%{C.rst}"

def test_ping(host, port=443, timeout=2):
    try:
        ip = socket.gethostbyname(host)
        start = time.time()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, int(port)))
        s.close()
        ms = round((time.time() - start) * 1000)
        if ms < 100:
            return ms, f"{C.G}🟢 {ms}ms{C.rst}"
        elif ms < 250:
            return ms, f"{C.Y}🟡 {ms}ms{C.rst}"
        else:
            return ms, f"{C.R}🔴 {ms}ms{C.rst}"
    except:
        return 9999, f"{C.R}❌ Timeout{C.rst}"

def extract_host_port(key):
    try:
        if "://" in key:
            import urllib.parse
            parsed = urllib.parse.urlparse(key)
            return parsed.hostname or "", parsed.port or 443
    except: pass
    try:
        if "@" in key and ":" in key.split("@")[-1]:
            part = key.split("@")[-1]
            h, p = part.split(":")
            return h.strip(), p.strip()
    except: pass
    return "", ""

def get_flag_emoji(name):
    name = name.lower()
    flags = {
        "singapore": "🇸🇬", "malaysia": "🇲🇾", "thailand": "🇹🇭",
        "vietnam": "🇻🇳", "indonesia": "🇮🇩", "philippines": "🇵🇭",
        "hongkong": "🇭🇰", "hong kong": "🇭🇰", "japan": "🇯🇵",
        "korea": "🇰🇷", "india": "🇮🇳", "australia": "🇦🇺",
        "germany": "🇩🇪", "finland": "🇫🇮", "usa": "🇺🇸",
        "united states": "🇺🇸", "uk": "🇬🇧", "russia": "🇷🇺"
    }
    for k, v in flags.items():
        if k in name: return v
    return "🌐"

def get_country_priority(name):
    """နိုင်ငံအပေါ်မူတည်ပြီး ဦးစားပေးအမှတ်ပေး (နီးလေ ပိုကောင်းလေ)"""
    name = name.lower()
    for idx, country in enumerate(NEARBY_COUNTRIES):
        if country in name:
            return 100 - (idx * 5)  # စင်ကာပူ = 100, မလေးရှား = 95, ထိုင်း = 90...
    return 30  # ဝေးတဲ့နိုင်ငံများ

def calculate_score(ping_ms, country_priority, uptime_pct):
    """အကိုက်ညီဆုံးဖြစ်အောင် အမှတ်တွက်ပေးတယ် — အမှတ်များလေ ပိုကောင်းလေ"""
    ping_score = max(0, 100 - ping_ms // 2)  # Ping နည်းလေ အမှတ်များလေ
    total = int((country_priority * 0.5) + (ping_score * 0.35) + (uptime_pct * 0.15))
    return total

def build_share_text(name, key, ping_info="", uptime_pct="", fetched_time=""):
    ping_clean = ping_info.replace(C.G,"").replace(C.Y,"").replace(C.R,"").replace(C.rst,"")
    uptime_clean = uptime_pct.replace(C.G,"").replace(C.Y,"").replace(C.R,"").replace(C.rst,"")
    flag = get_flag_emoji(name)
    return f"""{flag} VPN Server — {name}
⚡ အခြေအနေ: {uptime_clean}
📶 Ping: {ping_clean}
🕒 ရယူချိန်: {fetched_time}

🔑 Key:
{key}

✨ VPN Key Generator Premium
#VPN #FreeVPN #InternetFreedom"""

def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            content = r.read().decode().strip()
            try:
                data = json.loads(content)
                if isinstance(data, list): return data
            except: pass
            lines = content.splitlines()
            res = []
            for line in lines:
                line = line.strip()
                if line:
                    try: res.append(json.loads(line))
                    except: pass
            return res if res else None
    except Exception as e:
        print(f"  {C.R}❌ JSON: {str(e)[:40]}{C.rst}")
        return None

def fetch_b64(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return [l.strip() for l in base64.b64decode(r.read()).decode().splitlines() if l.strip()]
    except Exception as e:
        print(f"  {C.R}❌ Base64: {str(e)[:40]}{C.rst}")
        return None

def fetch_txt(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return [l.strip() for l in r.read().decode().splitlines() if l.strip() and not l.startswith("#")]
    except Exception as e:
        print(f"  {C.R}❌ TXT: {str(e)[:40]}{C.rst}")
        return None

def parse_key_info(key):
    if not key or len(key)<10: return None, None
    name = "Server"
    if "#" in key:
        try:
            import urllib.parse
            name = urllib.parse.unquote(key.split("#")[-1])
        except: pass
    if key.startswith("vless://") or key.startswith("ss://"):
        return name, key
    return None, None

def get_all_keys():
    all_keys = []
    for sid in ["1","2","3"]:
        name, url, dtype = API_LIST[sid]
        data = {"json":fetch_json,"b64":fetch_b64,"txt":fetch_txt}[dtype](url)
        if not data: continue
        if dtype=="json" and isinstance(data,list):
            for item in data:
                if isinstance(item,dict):
                    key = item.get("url") or item.get("link") or ""
                    n = item.get("name") or item.get("remarks") or "Server"
                    if key and (key.startswith("vless://") or key.startswith("ss://")):
                        all_keys.append({"name":n,"key":key,"source":name})
        elif dtype in ["b64","txt"] and isinstance(data,list):
            for k in data:
                n, vk = parse_key_info(k)
                if vk: all_keys.append({"name":n,"key":vk,"source":name})
    return all_keys

def show_key_detail(item, ping_ms, ping_str):
    fetched_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uptime_pct_val, uptime_pct_str = get_uptime_percent(ping_ms)
    flag = get_flag_emoji(item['name'])
    
    while True:
        header()
        divider(f"{flag} {item['name']}")
        print(f"  {C.C}📍 အရင်းအမြစ်:{C.rst} {item['source']}")
        print(f"  {C.Y}⚡ အခြေအနေ:{C.rst} {uptime_pct_str}")
        print(f"  {C.Y}📶 Ping:{C.rst} {ping_str}")
        print(f"  {C.D}🕒 ရယူချိန်:{C.rst} {fetched_time}")
        divider()
        print(f"  {C.G}🔑 Key:{C.rst}\n{C.W}{item['key']}{C.rst}")
        divider()
        share_text = build_share_text(item['name'], item['key'], ping_str, uptime_pct_str, fetched_time)
        print(f"\n  {C.C}[1]{C.rst} Key ကူးယူပါ")
        print(f"  {C.C}[2]{C.rst} Share ဖို့ အကုန်ကူးယူပါ")
        print(f"  {C.C}[F]{C.rst} အကြိုက်ဆုံးထဲသိမ်းပါ")
        print(f"  {C.C}[Q]{C.rst} ပြန်သွားမည်")
        sel = input("  ▶ ရွေးပါ : ").strip().upper()
        if sel=="1":
            copy_to_clipboard(item['key'])
            print(f"  {C.G}✅ Key ကူးယူပြီးပါပြီ!{C.rst}\n"); input("  Enter...")
        elif sel=="2":
            copy_to_clipboard(share_text)
            print(f"  {C.G}✅ Share အကုန်ကူးယူပြီးပါပြီ! Telegram/Facebook/TikTok မှာ Paste လုပ်ပါ{C.rst}\n"); input("  Enter...")
        elif sel=="F":
            save_favorite(item['name'], item['key'], ping_str, fetched_time)
            print(f"  {C.G}✅ အကြိုက်ဆုံးထဲ သိမ်းပြီးပါပြီ{C.rst}\n"); input("  Enter...")
        elif sel=="Q":
            break

def find_best_key():
    header()
    print(f"  {C.Y}🔍 အမြန်ဆုံး Server ကို ရှာဖွေနေသည်...{C.rst}\n")
    all_keys = get_all_keys()
    if not all_keys:
        input(f"  {C.R}မရပါ။ Enter...{C.rst}"); return
    
    print(f"  {C.C}စုစုပေါင်း Key {len(all_keys)} လုံး တွေ့ရှိခဲ့သည် ✅{C.rst}")
    print(f"  {C.Y}⏳ တစ်ခုချင်းစီ စမ်းသပ်နေသည်...{C.rst}\n")
    
    best_key = None
    best_ping = 9999
    
    for i, item in enumerate(all_keys, 1):
        host, port = extract_host_port(item['key'])
        if not host: continue
        flag = get_flag_emoji(item['name'])
        sys.stdout.write(f"  {flag} {i}/{len(all_keys)} — {item['name'][:20]}...")
        sys.stdout.flush()
        ping_ms, ping_str = test_ping(host, port, timeout=1.5)
        if ping_ms < best_ping:
            best_ping = ping_ms
            best_key = item.copy()
            best_key["ping_ms"] = ping_ms
            best_key["ping_str"] = ping_str
            _, uptime_str = get_uptime_percent(ping_ms)
            sys.stdout.write(f"  {C.G}✅ အသစ်အကောင်းဆုံး! {uptime_str}  {ping_str}{C.rst}\n")
        else:
            sys.stdout.write(f"  {ping_str}\n")
    
    if not best_key:
        input(f"\n  {C.R}အလုပ်လုပ်နိုင်တဲ့ Server မတွေ့ပါ။ Enter...{C.rst}"); return
    
    print(f"\n{C.G}══════════════════════════════════════════════════{C.rst}")
    print(f"{C.G}🏆 အမြန်ဆုံး Server ကို တွေ့ရှိခဲ့သည်!{C.rst}")
    print(f"{C.G}══════════════════════════════════════════════════{C.rst}\n")
    
    show_key_detail(best_key, best_key["ping_ms"], best_key["ping_str"])

def find_best_for_me():
    header()
    print(f"  {C.Y}🎯 သင့်အတွက် အသင့်တော်ဆုံး Server ကို ရှာဖွေနေသည်...{C.rst}")
    print(f"  {C.D}📍 မြန်မာနိုင်ငံမှ အနီးဆုံး + အမြန်ဆုံးကို ရွေးချင်နေသည်...{C.rst}\n")
    
    all_keys = get_all_keys()
    if not all_keys:
        input(f"  {C.R}မရပါ။ Enter...{C.rst}"); return
    
    print(f"  {C.C}စုစုပေါင်း Key {len(all_keys)} လုံး ကို စစ်ဆေးနေသည် ✅{C.rst}")
    print(f"  {C.Y}⏳ အကဲဖြတ်နေသည်... (တည်နေရာ + အမြန်နှုန်း + တည်ငြိမ်မှု){C.rst}\n")
    
    scored_keys = []
    
    for i, item in enumerate(all_keys, 1):
        host, port = extract_host_port(item['key'])
        if not host: continue
        flag = get_flag_emoji(item['name'])
        sys.stdout.write(f"  {flag} {i}/{len(all_keys)} — {item['name'][:20]}...စစ်ဆေးနေသည်")
        sys.stdout.flush()
        
        ping_ms, ping_str = test_ping(host, port, timeout=1.5)
        uptime_pct, _ = get_uptime_percent(ping_ms)
        country_priority = get_country_priority(item['name'])
        score = calculate_score(ping_ms, country_priority, uptime_pct)
        
        scored_keys.append({
            **item,
            "ping_ms": ping_ms,
            "ping_str": ping_str,
            "uptime_pct": uptime_pct,
            "country_priority": country_priority,
            "score": score
        })
        
        sys.stdout.write(f"  အမှတ် {score}/100 ✅\n")
    
    if not scored_keys:
        input(f"\n  {C.R}အသင့်တော်ဆုံး Server မတွေ့ပါ။ Enter...{C.rst}"); return
    
    # အမှတ်အများဆုံးကို ရွေးမယ်
    scored_keys.sort(key=lambda x: x["score"], reverse=True)
    best = scored_keys[0]
    
    print(f"\n{C.G}╔══════════════════════════════════════════════════╗{C.rst}")
    print(f"{C.G}║{C.rst}  🎯 သင့်အတွက် အသင့်တော်ဆုံး Server ကို တွေ့ရှိခဲ့သည်!{C.G}║{C.rst}")
    print(f"{C.G}╚══════════════════════════════════════════════════╝{C.rst}")
    print(f"\n  {C.Y}📌 အကဲဖြတ်ချက်:{C.rst}")
    print(f"     • တည်နေရာ နီးစပ်မှု  : {C.G}{best['country_priority']}{C.rst}/100")
    print(f"     • တုံ့ပြန်မှု မြန်နှုန်း  : {best['ping_str']}")
    print(f"     • အွန်လိုင်း တည်ငြိမ်မှု: {C.G}{best['uptime_pct']}%{C.rst}")
    print(f"     ═══════════════════════════════")
    print(f"     {C.G}စုစုပေါင်း အကိုက်ညီမှု အမှတ်: {best['score']}/100{C.rst}\n")
    
    show_key_detail(best, best["ping_ms"], best["ping_str"])

def find_browse_keys():
    header()
    print(f"  {C.Y}🔍 ဒေတာရှာဖွေနေသည်...{C.rst}\n")
    all_keys = []; sources = []
    for sid in ["1","2","3"]:
        name, url, dtype = API_LIST[sid]
        print(f"  ⬜ {name}...", end="", flush=True)
        data = {"json":fetch_json,"b64":fetch_b64,"txt":fetch_txt}[dtype](url)
        print(f" {C.G}✅{C.rst}" if data else f" {C.R}❌{C.rst}")
        if data: sources.append((name,data,dtype))
    if not sources:
        input(f"\n  {C.R}မရပါ။ Enter နှိပ်ပါ...{C.rst}"); return
    for sname, data, dtype in sources:
        cnt=0
        if dtype=="json" and isinstance(data,list):
            for item in data:
                if isinstance(item,dict):
                    key = item.get("url") or item.get("link") or ""
                    n = item.get("name") or item.get("remarks") or f"Server {cnt+1}"
                    if key and (key.startswith("vless://") or key.startswith("ss://")):
                        all_keys.append({"name":n,"key":key,"source":sname}); cnt+=1
        elif dtype in ["b64","txt"] and isinstance(data,list):
            for k in data:
                n, vk = parse_key_info(k)
                if vk: all_keys.append({"name":n,"key":vk,"source":sname}); cnt+=1
        print(f"     → {sname}: Key {cnt} လုံး")
    if not all_keys:
        input(f"\n  {C.R}Key မတွေ့ပါ။ Enter...{C.rst}"); return
    print(f"\n  {C.G}စုစုပေါင်း Key {len(all_keys)} လုံး ✅{C.rst}\n")
    idx=0
    while True:
        item=all_keys[idx]
        fetched_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        flag = get_flag_emoji(item['name'])
        header()
        divider(f"{flag} Key #{idx+1}/{len(all_keys)}")
        host, port = extract_host_port(item['key'])
        print(f"  {C.G}နာမည်:{C.rst} {item['name']}")
        print(f"  {C.C}အရင်းအမြစ်:{C.rst} {item['source']}")
        print(f"  {C.Y}📶 Ping:{C.rst} {C.D}⏳ စမ်းနေသည်...{C.rst}", end="\r", flush=True)
        ping_ms, ping_str = test_ping(host, port) if host else (0, f"{C.D}မရနိုင်ပါ{C.rst}")
        _, uptime_str = get_uptime_percent(ping_ms)
        print(f"  {C.Y}⚡ အခြေအနေ:{C.rst} {uptime_str}    ")
        print(f"  {C.Y}📶 Ping:{C.rst} {ping_str}")
        print(f"  {C.D}🕒 ရယူချိန်:{C.rst} {fetched_time}")
        divider()
        print(f"  {C.Y}🔑 Key:{C.rst}\n{C.W}{item['key']}{C.rst}")
        divider()
        share_text = build_share_text(item['name'], item['key'], ping_str, uptime_str, fetched_time)
        print(f"\n  {C.C}[1]{C.rst} Key ကူး   {C.C}[2]{C.rst} Share ကူး   {C.C}[F]{C.rst}သိမ်း")
        print(f"  {C.C}[←]ယခင်  {C.C}[→]နောက်  {C.C}[Q]{C.rst}ပြန်")
        sel = input("  ▶ : ").strip().upper()
        if sel=="1":
            copy_to_clipboard(item['key'])
            print(f"  {C.G}✅ Key ကူးယူပြီး{C.rst}\n"); input("  Enter...")
        elif sel=="2":
            copy_to_clipboard(share_text)
            print(f"  {C.G}✅ Share အကုန်ကူးယူပြီး! Telegram/Facebook/TikTok မှာ Paste လုပ်ပါ{C.rst}\n"); input("  Enter...")
        elif sel=="F":
            save_favorite(item['name'], item['key'], ping_str, fetched_time)
            print(f"  {C.G}✅ သိမ်းပြီး{C.rst}\n"); input("  Enter...")
        elif sel=="B" or sel=="P" or sel=="":
            if idx>0: idx-=1
        elif sel=="N":
            if idx+1<len(all_keys): idx+=1
        elif sel=="Q":
            break

def favorites_menu():
    while True:
        header()
        favs=load_favorites()
        print(f"  {C.Y}⭐ အကြိုက်ဆုံးများ{C.rst}\n")
        divider()
        if not favs:
            print(f"  {C.D}မရှိသေးပါ။ Key ရတဲ့အခါ [F] နှိပ်ပါ။{C.rst}")
        else:
            for i,e in enumerate(favs,1):
                parts = e.split("|",3)
                n = parts[0] if len(parts)>0 else "Server"
                k = parts[1] if len(parts)>1 else ""
                p = parts[2] if len(parts)>2 else ""
                t = parts[3] if len(parts)>3 else ""
                flag = get_flag_emoji(n)
                print(f"  {C.C}[{i}]{C.rst} {flag} {n}")
                if p: print(f"      📶 {p}")
                if t: print(f"      🕒 {t}")
                print(f"      {C.W}{k}{C.rst}")
                share_text = build_share_text(n, k, p, "", t)
                print(f"      {C.C}[1]Key ကူး  [2]Share ကူး{C.rst}")
                act = input(f"      ▶ : ").strip()
                if act=="1":
                    copy_to_clipboard(k)
                    print(f"        {C.G}✅ Key ကူးယူပြီး{C.rst}")
                elif act=="2":
                    copy_to_clipboard(share_text)
                    print(f"        {C.G}✅ Share အကုန်ကူးယူပြီး{C.rst}")
        divider()
        print(f"  {C.C}[Q]{C.rst}ပြန်  {C.C}[A]{C.rst}အားလုံးဖျက်")
        sel=input("  ▶ : ").strip().upper()
        if sel=="Q": break
        elif sel=="A" and input(f"  {C.R}ဖျက်မှာလား? y/n:{C.rst}").lower()=="y":
            os.path.exists(FAV_FILE) and os.remove(FAV_FILE); break

def main_menu():
    while True:
        header()
        print(f"  {C.Y}📂 ပင်မမီနူး{C.rst}\n")
        divider()
        print(f"  {C.G}🎯 [M] ကျွန်ုပ်အတွက် အသင့်တော်ဆုံး — အကြံပြု{C.rst}")
        print(f"  {C.G}🏆 [0] အမြန်ဆုံးကိုသာ ရွေးမည်{C.rst}")
        print(f"  {C.C}📋 [B] အားလုံးကို ကြည့်ပြီး ကိုယ်တိုင်ရွေးမည်{C.rst}\n")
        print(f"  {C.C}[1]{C.rst} Shadowmere JSON")
        print(f"  {C.C}[2]{C.rst} Shadowmere Base64")
        print(f"  {C.C}[3]{C.rst} VLESS List")
        print(f"  {C.C}[4]{C.rst} ⭐ အကြိုက်ဆုံးများ\n")
        print(f"  {C.R}[9]{C.rst} ထွက်မည်")
        divider()
        ch=input("  ▶ ရွေးပါ : ").strip().upper()
        if ch=="M": find_best_for_me()
        elif ch=="0": find_best_key()
        elif ch=="B": find_browse_keys()
        elif ch=="9": clear(); print(f"\n  {C.C}👋 ကျေးဇူးတင်ပါတယ်။{C.rst}\n"); sys.exit(0)
        elif ch=="4": favorites_menu()
        elif ch in API_LIST:
            name,url,dtype = API_LIST[ch]
            header(); print(f"  {C.Y}{name} မှ ဒေတာရယူနေသည်...{C.rst}\n")
            data = {"json":fetch_json,"b64":fetch_b64,"txt":fetch_txt}[dtype](url)
            if not data: input(f"  {C.R}မရပါ။ Enter...{C.rst}"); continue
            items=[]
            if dtype=="json" and isinstance(data,list):
                for item in data:
        
