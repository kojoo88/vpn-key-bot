#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, base64, os, datetime, socket, time

# 🎨 အရောင်များ
G = "\033[92m"
B = "\033[94m"
Y = "\033[93m"
R = "\033[91m"
CY = "\033[96m"
M = "\033[95m"
BD = "\033[1m"
RS = "\033[0m"

FAVORITES_FILE = "favorites.txt"
ALL_KEYS_FILE = "all_keys.txt"

def clear():
    os.system("clear")

# 📡 အရင်းအမြစ်များ
SOURCES = [
    ("Shadowmere B64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("Argh73 Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
]

# ⚡ Ping စစ်ဆေးခြင်း
def check_ping(host, port, timeout=2):
    try:
        start = time.time()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, int(port)))
        ms = int((time.time() - start) * 1000)
        if ms < 150:
            return f"{G}{ms} ms  ✅ အလွန်ကောင်း{RS}", ms, True
        elif ms < 300:
            return f"{Y}{ms} ms  ⚡ ပုံမှန်{RS}", ms, True
        else:
            return f"{B}{ms} ms  📍 နှေး{RS}", ms, True
    except:
        return f"{R}❌ ချိတ်ဆက်မရှိ{RS}", 9999, False

# 🔗 Host နှင့် Port ထုတ်ယူခြင်း
def extract_host_port(key):
    try:
        from urllib.parse import urlparse
        parsed = urlparse(key)
        if parsed.hostname and parsed.port:
            return parsed.hostname, parsed.port
    except:
        pass
    
    try:
        import re
        if "://" in key and "@" in key:
            match = re.search(r"@([^:]+):(\d+)", key)
            if match:
                return match.group(1), int(match.group(2))
    except:
        pass
    return None, None

# 📄 ဒေတာဖတ်ခြင်း
def get_text(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", errors="ignore")
    except:
        return None

# 🔑 ကီးများဖြတ်ထုတ်ခြင်း
def parse(text, fmt):
    keys = []
    if not text:
        return keys
    try:
        if fmt == "b64":
            text = base64.b64decode(text).decode("utf-8", errors="ignore")
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            proto = None
            if line.startswith("vless://"):
                proto = "VLESS"
            elif line.startswith("ss://"):
                proto = "SS"
            elif line.startswith("vmess://"):
                proto = "VMESS"
            elif line.startswith("trojan://"):
                proto = "TROJAN"
            if proto:
                name = "ဆာဗာ"
                if "#" in line:
                    name = line.split("#")[-1]
                    try:
                        from urllib.parse import unquote
                        name = unquote(name)
                    except:
                        pass
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                keys.append({
                    "proto": proto,
                    "name": name,
                    "key": line,
                    "added_time": now,
                    "ping_ms": 9999,
                    "ping_str": "မစစ်ရသေး",
                    "is_alive": False
                })
    except:
        pass
    return keys

# 💾 ဖိုင်သိမ်းခြင်း
def save_to_file(keys, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("Updated: " + str(datetime.datetime.now()) + "\n")
            f.write("Total Keys: " + str(len(keys)) + "\n\n")
            for k in keys:
                status = "✅ အလုပ်လုပ်သည်" if k["is_alive"] else "❌ အလုပ်မလုပ်ပါ"
                f.write(k["proto"] + " | " + k["name"] + " | " + status + "\n")
                f.write(k["key"] + "\n\n")
        return True
    except:
        return False

# ⭐ အကြိုက်ဆုံးများ
def load_favorites():
    favs = []
    if os.path.exists(FAVORITES_FILE):
        try:
            with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and ("://" in line):
                        favs.append(line)
        except:
            pass
    return favs

def add_favorite(key_line):
    try:
        with open(FAVORITES_FILE, "a", encoding="utf-8") as f:
            f.write(key_line + "\n")
        return True
    except:
        return False

# 🔍 ရှာဖွေခြင်း
def search_by_name(keys, keyword):
    result = []
    keyword = keyword.upper()
    for k in keys:
        if keyword in k["name"].upper():
            result.append(k)
    return result

# 📋 ကီးများပြသခြင်း
def show_keys(keys, title="ကီးများ", show_only_alive=False, sort_by_ping=False):
    if show_only_alive:
        keys = [k for k in keys if k["is_alive"]]
    if sort_by_ping:
        keys = sorted(keys, key=lambda x: x["ping_ms"])
    
    if not keys:
        print(f"\n{R}❌ ကီးမတွေ့ရှိပါ{RS}\n")
        input(f"{Y}ပြန်ရန် Enter နှိပ်ပါ → {RS}")
        return
    
    print(f"\n{M}{BD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RS}")
    print(f"{M}{BD}📌  {title}  ({len(keys)} ခု){RS}")
    print(f"{M}{BD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RS}\n")
    
    display_count = min(10, len(keys))
    for i, k in enumerate(keys[:display_count], 1):
        status = f"{G}✅ အလုပ်လုပ်သည်{RS}" if k["is_alive"] else f"{R}❌ စစ်ဆေးရန်လို{RS}"
        print(f"  {BD}{str(i).zfill(2)}{RS} ｜ {k['proto']:7} ｜ {k['name'][:35]}")
        print(f"       ⚡ Ping: {k['ping_str']}  ｜ အခြေအနေ: {status}")
        print(f"       🔑 {CY}{k['key']}{RS}\n")
    
    if len(keys) > display_count:
        print(f"{Y}... နောက်ထပ် {len(keys)-display_count} ခု ကျန်ရှိနေပါသည်{RS}\n")
    
    input(f"{Y}ပြန်ရန် Enter နှိပ်ပါ → {RS}\n")

# 🏆 အနိမ့်ဆုံး Ping ဖြင့် စီခြင်း
def sort_by_best_ping(keys):
    print(f"\n{M}{BD}⚡ အကောင်းဆုံး ဆာဗာများကို ရှာဖွေနေသည်...{RS}\n")
    tested = []
    for i, k in enumerate(keys):
        host, port = extract_host_port(k["key"])
        if host and port:
            print(f"  စစ်ဆေးနေသည်... [{i+1}/{len(keys)}] {k['name'][:25]}", end="\r")
            ping_str, ping_ms, is_alive = check_ping(host, port, timeout=1.5)
            k["ping_str"] = ping_str
            k["ping_ms"] = ping_ms
            k["is_alive"] = is_alive
            if is_alive:
                tested.append(k.copy())
    
    if not tested:
        print(f"\n{R}❌ အလုပ်လုပ်သည့်ဆာဗာ မတွေ့ပါ{RS}\n")
        input(f"{Y}ပြန်ရန် Enter နှိပ်ပါ → {RS}")
        return
    
    tested.sort(key=lambda x: x["ping_ms"])
    show_keys(tested, "🏆 အနိမ့်ဆုံး Ping ရှိ ဆာဗာများ")

# 🚀 အားလုံးကို Ping စစ်ခြင်း
def check_all_pings(keys):
    print(f"\n{M}{BD}⚡ ဆာဗာများကို စစ်ဆေးနေသည်...{RS}\n")
    alive_count = 0
    for i, k in enumerate(keys):
        host, port = extract_host_port(k["key"])
        if host and port:
            print(f"  စစ်ဆေးနေသည်... [{i+1}/{len(keys)}]", end="\r")
            ping_str, ping_ms, is_alive = check_ping(host, port, timeout=1.5)
            k["ping_str"] = ping_str
            k["ping_ms"] = ping_ms
            k["is_alive"] = is_alive
            if is_alive:
                alive_count += 1
    
    print(f"\n\n{G}{BD}✅ စစ်ဆေးမှုပြီးဆုံး — အလုပ်လုပ်သည်: {alive_count} / {len(keys)}{RS}\n")
    input(f"{Y}ပြန်ရန် Enter နှိပ်ပါ → {RS}\n")
    return keys

# 🚀 ပရှိထားပြီးသား ကီးများထဲမှ အလုပ်လုပ်တာကိုသာ ပြခြင်း
def show_alive_only(keys):
    alive_keys = [k for k in keys if k["is_alive"]]
    show_keys(alive_keys, "✅ အလုပ်လုပ်သည့် ကီးများသာ", show_only_alive=False, sort_by_ping=True)

# 📋 အဓိကမီနူး
def main():
    clear()
    print(f"""{M}{BD}
╔══════════════════════════════════════════════════════════════╗
║           🚀  V P N   K E Y   F I N D E R   •  P R O          ║
║     ═══════════════════════════════════════════════════════     ║
║     ✅ နှစ်ခုအရင်းအမြစ်  •  ⚡ Ping စစ်ဆေးမှု  •  🏆 အကောင်းဆုံးရွေး  ║
╚══════════════════════════════════════════════════════════════╝{RS}""")
    
    all_keys = []
    seen = set()
    
    print(f"\n{Y}📡 ဒေတာရင်းမြစ်များမှ ဖတ်နေသည်...{RS}\n")
    
    for name, url, fmt in SOURCES:
        print(f"  ⏳ {name} ကို ဖတ်နေသည်...", end="\r")
        text = get_text(url)
        ks = parse(text, fmt)
        if ks:
            for k in ks:
                if k["key"] not in seen:
                    seen.add(k["key"])
                    all_keys.append(k)
            print(f"  {G}✅ {name} — {len(ks)} ကီး ရရှိ{RS}")
        else:
            print(f"  {R}❌ {name} — မရရှိ{RS}")
    
    print(f"\n{CY}{BD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RS}")
    print(f"{CY}📊 စုစုပေါင်း ကီး အရေအတွက်: {G}{len(all_keys)}{CY} ခု{RS}")
    print(f"{CY}{BD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RS}\n")
    
    # 📌 ပင်မမီနူး
    while True:
        print(f"{M}{BD}📌  ပင်မမီနူး{RS}")
        print(f"{CY}═══════════════════════════════════════════════{RS}")
        print(f"   {BD}[ 1 ]{RS}  📋 ကီးအားလုံးကို ကြည့်ရန်")
        print(f"   {BD}[ 2 ]{RS}  📋 VLESS ကီးများသာ ကြည့်ရန်")
        print(f"   {BD}[ 3 ]{RS}  📋 SS ကီးများသာ ကြည့်ရန်")
        print(f"   {BD}[ 4 ]{RS}  ⚡ Ping နှင့်အတူ အားလုံးကို စစ်ဆေးရန်")
        print(f"   {BD}[ 5 ]{RS}  ✅ အလုပ်လုပ်သည့် ကီးများသာ ပြရန်")
        print(f"   {BD}[ 6 ]{RS}  🏆 အနိမ့်ဆုံး Ping ဖြင့် အကောင်းဆုံးရှာရန်")
        print(f"   {BD}[ 7 ]{RS}  🔍 အမည်/နိုင်ငံအလိုက် ရှာဖွေရန်")
        print(f"   {BD}[ 8 ]{RS}  💾 ဖိုင်အဖြစ် သိမ်းဆည်းရန်")
        print(f"   {BD}[ 9 ]{RS}  ⭐ အကြိုက်ဆုံးများ ကြည့်ရန်")
        print(f"   {BD}[10 ]{RS}  ➕ ကီးတစ်ခုကို အကြိုက်ဆုံးထဲ ထည့်ရန်")
        print(f"   {BD}[ 0 ]{RS}  ❌ ပရိုဂရမ်မှ ထွက်ရန်")
        print(f"{CY}═══════════════════════════════════════════════{RS}")
        
        choice = input(f"\n{B}ရွေးချယ်ပါ → {RS}").strip()
        
        if choice == "0":
            print(f"\n{CY}👋 ကျေးဇူးတင်ပါတယ်! ပြန်လာတန်းမှာ...{RS}\n")
            break
        
        elif choice == "1":
            show_keys(all_keys, "ကီးအားလုံး")
        
        elif choice == "2":
            show_keys([k for k in all_keys if k["proto"] == "VLESS"], "VLESS ကီးများ")
        
        elif choice == "3":
            show_keys([k for k in all_keys if k["proto"] == "SS"], "SS ကီးများ")
        
        elif choice == "4":
            all_keys = check_all_pings(all_keys)
        
        elif choice == "5":
            show_alive_only(all_keys)
        
        elif choice == "6":
            sort_by_best_ping(all_keys)
        
        elif choice == "7":
            keyword = input(f"{B}ရှာမည့် စာလုံး သို့မဟုတ် နိုင်ငံအမည် → {RS}").strip()
            found = search_by_name(all_keys, keyword)
            show_keys(found, f"'{keyword}' ဖြင့် ရှာဖွေမှုရလဒ်")
        
        elif choice == "8":
            if save_to_file(all_keys, ALL_KEYS_FILE):
                print(f"\n{G}✅ {ALL_KEYS_FILE} အဖြစ် သိမ်းဆည်းပြီးသား{RS}\n")
            else:
                print(f"\n{R}❌ သိမ်းဆည်း၍မရပါ{RS}\n")
            input(f"{Y}ပြန်ရန် Enter နှိပ်ပါ → {RS}")
        
        elif choice == "9":
            fav_keys = load_favorites()
            print()
            if not fav_keys:
                print(f"{Y}⭐ အကြိုက်ဆုံး မရှိသေးပါ{RS}\n")
            else:
                print(f"{M}{BD}=== ⭐ အကြိုက်ဆုံး ကီးများ ==={RS}\n")
                for i, k in enumerate(fav_keys, 1):
                    print(f"  {i}. {k}\n")
            input(f"{Y}ပြန်ရန် Enter နှိပ်ပါ → {RS}")
        
        elif choice == "10":
            idx_str = input(f"{B}အကြိုက်ဆုံးထဲ ထည့်မည့် ကီးနံပါတ် → {RS}").strip()
            try:
                idx = int(idx_str) - 1
                if 0 <= idx < len(all_keys):
                    if add_favorite(all_keys[idx]["key"]):
                        print(f"\n{G}✅ အကြိုက်ဆုံးထဲ ထည့်ပြီးသား{RS}\n")
                    else:
                        print(f"\n{R}❌ မအောင်မြင်ပါ{RS}\n")
                else:
                    print(f"\n{R}❌ နံပါတ်မှားနေပါတယ်{RS}\n")
            except:
                print(f"\n{R}❌ သင့်လျော်တဲ့နံပါတ်မဟုတ်ပါ{RS}\n")
            input(f"{Y}ပြန်ရန် Enter နှိပ်ပါ → {RS}")
        
        else:
            print(f"\n{R}❌ ရွေးချယ်မှုမှားနေပါတယ်၊ ထပ်မံကြိုးစားကြည့်ပါ{RS}\n")

if __name__ == "__main__":
    main()
