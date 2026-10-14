#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, base64, os, socket, time, datetime

G = "\033[92m"
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

SOURCES = [
    ("Shadowmere B64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("Argh73 Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
]

def check_ping(host, port, timeout=0.8):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        start = time.time()
        s.connect((host, int(port)))
        ms = int((time.time() - start) * 1000)
        s.close()
        if ms < 150:
            return f"{G}{ms}ms ✅ ကောင်း{RS}", ms, True
        elif ms < 300:
            return f"{Y}{ms}ms ⚡ ပုံမှန်{RS}", ms, True
        else:
            return f"{CY}{ms}ms 📍 နှေး{RS}", ms, True
    except:
        return None, 9999, False

def extract_host_port(key):
    try:
        from urllib.parse import urlparse
        p = urlparse(key)
        if p.hostname and p.port:
            return p.hostname, p.port
    except:
        pass
    try:
        import re
        m = re.search(r"@([^:]+):(\d+)", key)
        if m:
            return m.group(1), int(m.group(2))
    except:
        pass
    return None, None

def get_text(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.read().decode("utf-8", errors="ignore")
    except:
        return None

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
            if line.startswith("vless://"): proto = "VLESS"
            elif line.startswith("ss://"): proto = "SS"
            elif line.startswith("vmess://"): proto = "VMESS"
            elif line.startswith("trojan://"): proto = "TROJAN"
            if proto:
                name = "ဆာဗာ"
                if "#" in line:
                    name = line.split("#")[-1]
                    try:
                        from urllib.parse import unquote
                        name = unquote(name)
                    except:
                        pass
                keys.append({
                    "proto": proto,
                    "name": name,
                    "key": line,
                    "ping_ms": 9999,
                    "ping_str": "--",
                    "is_alive": False
                })
    except:
        pass
    return keys

def get_proto_file(proto):
    return f"alive_{proto.lower()}.txt"

def save_alive_by_proto(proto, keys):
    try:
        with open(get_proto_file(proto), "w", encoding="utf-8") as f:
            f.write(f"Protocol: {proto}\n")
            f.write("Updated: " + str(datetime.datetime.now()) + "\n")
            f.write("Total Alive: " + str(len(keys)) + "\n\n")
            for k in keys:
                f.write(f"{k['name']} | {k.get('ping_str', '--')}\n")
                f.write(k["key"] + "\n\n")
        return True
    except:
        return False

def load_alive_by_proto(proto):
    keys = []
    fname = get_proto_file(proto)
    if not os.path.exists(fname):
        return keys
    try:
        with open(fname, "r", encoding="utf-8") as f:
            lines = f.readlines()
        current_key = None
        for line in lines:
            line = line.strip()
            if not line or line.startswith("Protocol:") or line.startswith("Updated:") or line.startswith("Total Alive:"):
                continue
            if "://" in line:
                if current_key:
                    keys.append(current_key)
                current_key = {
                    "proto": proto,
                    "name": "Saved Server",
                    "key": line,
                    "ping_ms": 9999,
                    "ping_str": "--",
                    "is_alive": False
                }
            elif "|" in line and current_key:
                parts = line.split(" | ", 1)
                if len(parts) >= 1:
                    current_key["name"] = parts[0]
        if current_key:
            keys.append(current_key)
    except:
        pass
    return keys

def save_to_file(keys, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("Updated: " + str(datetime.datetime.now()) + "\n")
            f.write("Total: " + str(len(keys)) + "\n\n")
            for k in keys:
                f.write(k["proto"] + " | " + k["name"] + "\n" + k["key"] + "\n\n")
        return True
    except:
        return False

def load_favorites():
    favs = []
    if os.path.exists(FAVORITES_FILE):
        try:
            with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if "://" in line:
                        favs.append(line)
        except:
            pass
    return favs

def add_favorite(line):
    try:
        with open(FAVORITES_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        return True
    except:
        return False

def search_name(keys, kw):
    kw = kw.upper()
    return [k for k in keys if kw in k["name"].upper()]

def show(keys, title="ကီးများ", limit=20):
    if not keys:
        print(f"\n{R}မတွေ့ပါ{RS}\n")
        input("ပြန်ရန် Enter")
        return
    print(f"\n{M}{BD}=== {title} ({len(keys)}) ==={RS}\n")
    display_count = min(limit, len(keys))
    for i, k in enumerate(keys[:display_count], 1):
        status = f"{G}✅အလုပ်လုပ်{RS}" if k.get("is_alive") else f"{R}❌မစစ်ရသေး{RS}"
        print(f"{i:02d} | {k['proto']:6} | {k['name'][:35]}")
        print(f"    ⚡{k.get('ping_str', '--')}  {status}")
        print(f"    🔑{k['key']}\n")
    if len(keys) > display_count:
        print(f"{Y}...နောက်ထပ် {len(keys)-display_count} ခု{RS}\n")
    input("ပြန်ရန် Enter")

def copy_key(key_text):
    try:
        import subprocess
        subprocess.run(["termux-clipboard-set"], input=key_text.encode('utf-8'))
        print(f"{G}✅ ကီးကို ကူးယူပြီးပါပြီ!{RS}\n")
    except:
        print(f"{Y}⚠️ Termux မဟုတ်ပါက ကိုယ်တိုင်ကူးပါ:{RS}\n{key_text}\n")
    input("ပြန်ရန် Enter")

def scan_by_proto(all_keys, proto):
    keys = [k for k in all_keys if k["proto"] == proto]
    if not keys:
        print(f"\n{R}{proto} ကီးမရှိပါ{RS}\n")
        input("ပြန်ရန် Enter")
        return []
    
    print(f"\n{M}{BD}⚡ {proto} ကီးများကို စစ်ဆေးနေသည်...{RS}")
    print(f"{Y}စုစုပေါင်း {len(keys)} ခု{RS}\n")
    
    alive = []
    for i, k in enumerate(keys, 1):
        print(f"  [{i}/{len(keys)}] {k['name'][:22]}", end="\r")
        host, port = extract_host_port(k["key"])
        if not host or not port:
            continue
        ping_str, ms, is_alive = check_ping(host, port)
        if is_alive:
            k["ping_str"] = ping_str
            k["ping_ms"] = ms
            k["is_alive"] = True
            alive.append(k.copy())
    
    print(f"\n\n{G}{BD}✅ {proto} စစ်ပြီးဆုံး{RS}")
    print(f"   အလုပ်လုပ်သည်: {G}{len(alive)}{RS} / {len(keys)} ခု")
    
    if save_alive_by_proto(proto, alive):
        print(f"   {G}✅ သိမ်းဆည်းပြီးသား{RS}")
    print()
    input("ပြန်ရန် Enter")
    return alive

def rescan_saved(proto):
    keys = load_alive_by_proto(proto)
    if not keys:
        print(f"\n{Y}⚠️  {proto} သိမ်းထားတာမရှိသေးပါ{RS}\n")
        input("ပြန်ရန် Enter")
        return []
    
    print(f"\n{M}{BD}⚡ သိမ်းပြီးသား {proto} ကီးများကို ပြန်စစ်နေသည်...{RS}")
    print(f"{Y}စုစုပေါင်း {len(keys)} ခု{RS}\n")
    
    updated = []
    for i, k in enumerate(keys, 1):
        print(f"  [{i}/{len(keys)}] {k['name'][:22]}", end="\r")
        host, port = extract_host_port(k["key"])
        if not host or not port:
            continue
        ping_str, ms, is_alive = check_ping(host, port)
        if is_alive:
            k["ping_str"] = ping_str
            k["ping_ms"] = ms
            k["is_alive"] = True
            updated.append(k.copy())
    
    print(f"\n\n{G}{BD}✅ ပြန်စစ်ပြီး{RS}")
    print(f"   အလုပ်လုပ်ဆဲ: {G}{len(updated)}{RS} / {len(keys)} ခု")
    
    if save_alive_by_proto(proto, updated):
        print(f"   {G}✅ အသစ်ပြန်သိမ်းပြီး{RS}")
    print()
    input("ပြန်ရန် Enter")
    return updated

def show_best(keys, proto):
    if not keys:
        keys = load_alive_by_proto(proto)
    if not keys:
        print(f"\n{R}❌ ပထမဆုံး စစ်ဆေးပေးပါ{RS}\n")
        input("ပြန်ရန် Enter")
        return
    sorted_keys = sorted(keys, key=lambda x: x["ping_ms"])
    print(f"\n{M}{BD}🏆 {proto} — အကောင်းဆုံး 10 ခု{RS}\n")
    for i, k in enumerate(sorted_keys[:10], 1):
        print(f"{i:02d}. {k['name'][:35]}")
        print(f"    ⚡ {k['ping_str']}")
        print(f"    🔑 {k['key']}")
        print()
    input("ပြန်ရန် Enter")

# 🔑 ကီးစီမံခန့်ခွဲမှု မီနူး
def key_management_menu(all_keys):
    while True:
        print(f"\n{M}{BD}🔑 ကီးစီမံခန့်ခွဲမှု{RS}")
        print("════════════════════════════════")
        print(" [1] 📋 ကီးအားလုံးကို ကြည့်ရန်")
        print(" [2] 🔍 နာမည်/နိုင်ငံဖြင့် ရှာဖွေရန်")
        print(" [3] ⚡ VLESS ကီးများသာ ကြည့်ရန်")
        print(" [4] 📡 SS ကီးများသာ ကြည့်ရန်")
        print(" [5] ⭐ အကြိုက်ဆုံး ကီးများကို ကြည့်ရန်")
        print(" [6] 💾 ကီးတစ်ခုကို အကြိုက်ဆုံးထဲ သိမ်းရန်")
        print(" [7] 📋 အကြိုက်ဆုံးမှ ကူးယူရန်")
        print(" [8] 📤 ဖိုင်အဖြစ် အားလုံးထုတ်ယူရန်")
        print(" [0] ⬅️ ပင်မမီနူးသို့ ပြန်ရန်")
        print("════════════════════════════════")
        
        c = input(f"\nရွေးချယ်ပါ → {RS}").strip()
        
        if c == "0":
            break
        elif c == "1":
            show(all_keys, "ကီးအားလုံး")
        elif c == "2":
            kw = input("ရှာဖွေမည့် စာလုံး/နိုင်ငံအမည် → ").strip()
            result = search_name(all_keys, kw)
            show(result, f"'{kw}' ဖြင့်ရှာဖွေမှု")
        elif c == "3":
            vless = [k for k in all_keys if k["proto"] == "VLESS"]
            show(vless, "VLESS ကီးများ")
        elif c == "4":
            ss = [k for k in all_keys if k["proto"] == "SS"]
            show(ss, "SS ကီးများ")
        elif c == "5":
            favs = load_favorites()
            if not favs:
                print(f"\n{Y}⚠️  အကြိုက်ဆုံး မရှိသေးပါ{RS}\n")
            else:
                print(f"\n{M}{BD}⭐ အကြိုက်ဆုံး ကီးများ ({len(favs)}){RS}\n")
                for i, line in enumerate(favs, 1):
                    print(f"{i}. {line[:60]}...")
                    print(f"   🔑 {line}")
                    print()
            input("ပြန်ရန် Enter")
        elif c == "6":
            n = input("အကြိုက်ဆုံးထဲ သိမ်းမည့် ကီးနံပါတ် → ").strip()
            try:
                idx = int(n) - 1
                if 0 <= idx < len(all_keys):
                    if add_favorite(all_keys[idx]["key"]):
                        print(f"\n{G}✅ အကြိုက်ဆုံးထဲ ထည့်ပြီးပါပြီ!{RS}\n")
                    else:
                        print(f"\n{R}❌ မအောင်မြင်ပါ{RS}\n")
                else:
                    print(f"\n{R}နံပါတ်မှားနေတယ်{RS}\n")
            except:
                print(f"\n{R}မှားနေတယ်{RS}\n")
            input("ပြန်ရန် Enter")
        elif c == "7":
            favs = load_favorites()
            if not favs:
                print(f"\n{Y}⚠️  အကြိုက်ဆုံး မရှိသေးပါ{RS}\n")
                input("ပြန်ရန် Enter")
                continue
            print(f"\n{M}{BD}အကြိုက်ဆုံး ကီးများ:{RS}\n")
            for i, line in enumerate(favs, 1):
                print(f" [{i}] {line[:50]}...")
            sel = input("\nကူးယူမည့် နံပါတ် → ").strip()
            try:
                idx = int(sel) - 1
                if 0 <= idx < len(favs):
                    copy_key(favs[idx])
            except:
                print(f"\n{R}မှားနေတယ်{RS}\n")
                input("ပြန်ရန် Enter")
        elif c == "8":
            if save_to_file(all_keys, ALL_KEYS_FILE):
                print(f"\n{G}✅ ဖိုင်အဖြစ် သိမ်းပြီးပါပြီ! ဖိုင်နာမည်: {ALL_KEYS_FILE}{RS}\n")
            else:
                print(f"\n{R}❌ မအောင်မြင်ပါ{RS}\n")
            input("ပြန်ရန် Enter")
        else:
            print(f"\n{R}မှားနေတယ်{RS}\n")

def main():
    clear()
    print(f"""{M}{BD}
╔══════════════════════════════════════════╗
║     🚀 VPN KEY FINDER • PROTO SEPARATED     ║
║     ✅ VLESS / SS / VMESS / TROJAN          ║
║     ✅ အမျိုးအစားခွဲ • သီးခြားစီစစ်          ║
║     ✅ 🔑 ကီးစီမံခန့်ခွဲမှု မီနူးအသစ်         ║
╚══════════════════════════════════════════╝{RS}""")
    
    all_keys = []
    seen = set()
    
    print(f"\n{Y}ဒေတာဖတ်နေသည်...{RS}\n")
    for name, url, fmt in SOURCES:
        print(f"  {name}...", end=" ")
        text = get_text(url)
        ks = parse(text, fmt)
        if ks:
            for k in ks:
                if k["key"] not in seen:
                    seen.add(k["key"])
                    all_keys.append(k)
            print(f"{G}OK {len(ks)} ခု{RS}")
        else:
            print(f"{R}မရ{RS}")
    
    vless_keys = [k for k in all_keys if k["proto"] == "VLESS"]
    ss_keys = [k for k in all_keys if k["proto"] == "SS"]
    vmess_keys = [k for k in all_keys if k["proto"] == "VMESS"]
    trojan_keys = [k for k in all_keys if k["proto"] == "TROJAN"]
    
    print(f"\n{CY}📊 စုစုပေါင်း ကီးအရေအတွက်:{RS}")
    print(f"   VLESS: {G}{len(vless_keys)}{RS} ခု")
    print(f"   SS:    {G}{len(ss_keys)}{RS} ခု")
    print(f"   VMESS: {G}{len(vmess_keys)}{RS} ခု")
    print(f"   TROJAN:{G}{len(trojan_keys)}{RS} ခု")
    print()
    
    while True:
        print(f"{M}{BD}📌 ပင်မမီနူး{RS}")
        print("════════════════════════════")
        print("  VLESS ကီးများအတွက်")
        print("   [1] 📋 VLESS အားလုံးကို ကြည့်ရန်")
        print("   [2] ⚡ VLESS အသစ်စစ်ပြီး သိမ်းရန်")
        print("   [3] 🔄 VLESS သိမ်းပြီးသားကို ပြန်စစ်ရန်")
        print("   [4] 🏆 VLESS အကောင်းဆုံး ပြရန်")
        print()
        print("  SS ကီးများအတွက်")
        print("   [5] 📋 SS အားလုံးကို ကြည့်ရန်")
        print("   [6] ⚡ SS အသစ်စစ်ပြီး သိမ်းရန်")
        print("   [7] 🔄 SS သိမ်းပြီးသားကို ပြန်စစ်ရန်")
        print("   [8] 🏆 SS အကောင်းဆုံး ပြရန်")
        print()
        print("  🔑 ကီးစီမံခန့်ခွဲမှု")
        print("   [9] 🔑 ကီးများကို စီမံရန် ⬅️ အသစ်!")
        print()
        print("  အခြား")
        print("   [0] ❌ ထွက်ရန်")
        print("════════════════════════════")
        
        c = input(f"\nရွေးချယ်ပါ → {RS}").strip()
        
        if c == "0":
            print("\n👋 ပါသေး")
            break
        elif c == "1":
            show(vless_keys, "VLESS ကီးအားလုံး")
        elif c == "2":
            _ = scan_by_proto(all_keys, "VLESS")
        elif c == "3":
            _ = rescan_saved("VLESS")
        elif c == "4":
            show_best([], "VLESS")
        elif c == "5":
            show(ss_keys, "SS ကီးအားလုံး")
        elif c == "6":
            _ = scan_by_proto(all_keys, "SS")
        elif c == "7":
            _ = rescan_saved("SS")
        elif c == "8":
            show_best([], "SS")
        elif c == "9":
            key_management_menu(all_keys)
        else:
            print(f"\n{R}မှားနေတယ်{RS}\n")

if __name__ == "__main__":
    main()
