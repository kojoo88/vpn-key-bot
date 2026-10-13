#!/usr/bin/env python3
# VPN Key Generator — Premium Edition v4.6
# ပြင်ဆင်ချက်: အရင်းအမြစ်များကို ပိုမိုခိုင်မာအောင်ပြုပြင်၊ အမှားစစ်ဆေးမှုတိုးမြှင့်

import urllib.request
import urllib.error
import json
import base64
import os
import sys

os.environ["TERM"] = "xterm-256color"

VERSION = "4.6 ✨ PREMIUM"
FAV_FILE = os.path.expanduser("~/.vpn_favorites.txt")

# ✅ အရင်းအမြစ်များကို အသစ်ပြင်ဆင်ထားတယ်
API_LIST = {
    "1": ("Shadowmere JSON", "https://shadowmere.xyz/api/sub/", "json"),
    "2": ("Shadowmere Base64", "https://shadowmere.xyz/api/b64sub/", "b64"),
    "3": ("VLESS List", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vless.txt", "txt")
}


def clear():
    os.system("clear")


class Colors:
    P = "\033[95m"
    C = "\033[96m"
    G = "\033[92m"
    Y = "\033[93m"
    R = "\033[91m"
    W = "\033[97m"
    D = "\033[90m"
    rst = "\033[0m"


c = Colors()


def header():
    clear()
    fav_count = len(load_favorites())
    print(f"{c.P}╔══════════════════════════════════════════════════════════════════════╗{c.rst}")
    print(f"{c.P}║{c.rst}{c.Y}    ✨  VPN KEY GENERATOR — PREMIUM EDITION  v{VERSION.split()[1]}   ✨{c.rst}{c.P}║{c.rst}")
    print(f"{c.P}╠══════════════════════════════════════════════════════════════════════╣{c.rst}")
    print(f"{c.P}║{c.rst}  {c.C}📡 Status:{c.rst} Online ✅  {c.C}│{c.rst}  {c.C}⭐ Favorites:{c.rst} {fav_count}  {c.C}│{c.rst}  {c.C}⚡ Updated  {c.P}║{c.rst}")
    print(f"{c.P}╚══════════════════════════════════════════════════════════════════════╝{c.rst}")
    print()


def divider(title=""):
    if title:
        print(f"{c.C}─── {title} {'─' * (60 - len(title))}{c.rst}")
    else:
        print(f"{c.D}─" * 68 + c.rst)


def copy_to_clipboard(text):
    try:
        with open("/dev/clipboard", "w") as f:
            f.write(text)
        return True
    except Exception:
        return False


def load_favorites():
    if not os.path.exists(FAV_FILE):
        return []
    try:
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception:
        return []


def save_favorite(name, key):
    favs = load_favorites()
    entry = f"{name}|{key}"
    if entry not in favs:
        favs.append(entry)
        try:
            with open(FAV_FILE, "w", encoding="utf-8") as f:
                f.write("\n".join(favs))
            return True
        except Exception:
            return False
    return False


# ✅ JSON ဒေတာကို ပိုမိုကောင်းမွန်အောင်ဖတ်မယ်
def fetch_json(url):
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }
        )
        with urllib.request.urlopen(req, timeout=20) as response:
            data = response.read().decode()
            json_data = json.loads(data)
            
            # ဖွဲ့စည်းပုံအမျိုးမျိုးကို ကိုင်တွယ်မယ်
            if isinstance(json_data, dict):
                for key in ["data", "servers", "list", "subs"]:
                    if key in json_data and isinstance(json_data[key], list):
                        return json_data[key]
            
            if isinstance(json_data, list):
                return json_data
            
            return None
    except json.JSONDecodeError:
        print(f"  {c.R}❌ JSON ဖွဲ့စည်းပုံမှားနေတယ်{c.rst}")
        return None
    except Exception as e:
        print(f"  {c.R}❌ အမှား: {str(e)[:45]}{c.rst}")
        return None


def fetch_b64(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as response:
            decoded = base64.b64decode(response.read()).decode()
            lines = [line.strip() for line in decoded.splitlines() if line.strip()]
            return lines if lines else None
    except Exception as e:
        print(f"  {c.R}❌ Base64: {str(e)[:45]}{c.rst}")
        return None


def fetch_txt(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as response:
            content = response.read().decode()
            lines = [
                line.strip() for line in content.splitlines()
                if line.strip() and not line.startswith("#")
            ]
            return lines if lines else None
    except Exception as e:
        print(f"  {c.R}❌ TXT: {str(e)[:45]}{c.rst}")
        return None


# ✅ Key ကို အမှန်တကယ်ထုတ်ပေးမယ်
def parse_key_info(key):
    if not key or len(key) < 10:
        return None, None

    name = "Unknown Server"
    
    if "#" in key:
        try:
            name_part = key.split("#")[-1]
            import urllib.parse
            name = urllib.parse.unquote(name_part)
        except:
            name = "Server"
    
    if key.startswith("vless://"):
        return name, key
    elif key.startswith("ss://"):
        return name, key
    
    return None, None


def find_best_key():
    header()
    print(f"  {c.Y}🔍 အရင်းအမြစ်များမှ ဒေတာရယူနေသည်...{c.rst}\n")

    all_keys = []
    sources = []

    for source_id in ["1", "2", "3"]:
        name, url, data_type = API_LIST[source_id]
        print(f"  ⬜ {name}...", end="", flush=True)

        data = None
        if data_type == "json":
            data = fetch_json(url)
        elif data_type == "b64":
            data = fetch_b64(url)
        elif data_type == "txt":
            data = fetch_txt(url)

        if data:
            print(f" {c.G}✅ ရရှိ{c.rst}")
            sources.append((name, data, data_type))
        else:
            print(f" {c.R}❌ မရရှိ{c.rst}")

    if not sources:
        print(f"\n  {c.R}❌ မည်သည့်အရင်းအမြစ်မှ ဒေတာမရရှိပါ။{c.rst}")
        print(f"  {c.Y}💡 အကြံပြု: Option 2 ကို အရင်သုံးကြည့်ပါ (Base64 သည်းသာအလုပ်လုပ်တတ်သည်){c.rst}")
        input(f"  {c.D}Enter နှိပ်ပါ...{c.rst}")
        return

    print(f"\n  {c.G}✅ အရင်းအမြစ် {len(sources)} ခု အလုပ်လုပ်နေသည်။{c.rst}")
    print(f"  {c.Y}⚡ VPN Key များကို စုဆောင်းနေသည်...{c.rst}\n")

    for source_name, data, data_type in sources:
        count = 0
        
        if data_type == "json" and isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    key = item.get("url") or item.get("link") or item.get("server") or ""
                    name = item.get("name") or item.get("remarks") or f"Server {count+1}"
                    
                    if key and (key.startswith("vless://") or key.startswith("ss://")):
                        all_keys.append({"name": name, "key": key, "source": source_name})
                        count += 1

        elif data_type in ["b64", "txt"] and isinstance(data, list):
            for key in data:
                name, valid_key = parse_key_info(key)
                if valid_key:
                    all_keys.append({"name": name, "key": valid_key, "source": source_name})
                    count += 1
        
        print(f"     → {source_name}: Key {count} လုံး တွေ့ရှိခဲ့သည်{c.rst}")

    if not all_keys:
        print(f"\n  {c.R}❌ မည်သည့် VPN Key မျှမတွေ့ပါ။{c.rst}")
        print(f"  {c.Y}💡 အကြံပြု: အချိန်နည်းနည်းစောင့်ပြီး ပြန်ကြိုးစားပါ သို့မဟုတ် Option 2 ကိုသုံးပါ။{c.rst}")
        input(f"  {c.D}Enter နှိပ်ပါ...{c.rst}")
        return

    print(f"\n  {c.G}✅ စုစုပေါင်း Key {len(all_keys)} လုံး ရရှိခဲ့သည်။{c.rst}\n")

    current_index = 0
    while True:
        item = all_keys[current_index]
        header()

        divider(f"🔑 Key #{current_index + 1} / {len(all_keys)}")
        print(f"  {c.G}📍 နာမည်:{c.rst}   {item['name']}")
        print(f"  {c.C}📌 အရင်းအမြစ်:{c.rst} {item['source']}")
        divider()

        print(f"  {c.Y}🔑 VPN Key (အပြည့်အဝ):{c.rst}")
        print(f"{c.W}{item['key']}{c.rst}")
        divider()

        if copy_to_clipboard(item["key"]):
            print(f"  {c.G}✅ ကူးယူပြီးပါပြီ! ✅{c.rst}")
        else:
            print(f"  {c.Y}⚠️ အပေါ်က Key ကို ကိုယ်တိုင်ကူးယူပါ{c.rst}")
        divider()

        print(f"  {c.C}[F]{c.rst} သိမ်းမည်  ", end="")
        if current_index + 1 < len(all_keys):
            print(f"{c.C}[N]{c.rst} နောက်တစ်ခု  ", end="")
        if current_index > 0:
            print(f"{c.C}[P]{c.rst} ယခင်တစ်ခု  ", end="")
        print(f"{c.C}[Q]{c.rst} မီနူးသို့ပြန်")

        choice = input(f"  {c.P}▶ ရွေးချယ်ပါ : {c.rst}").strip().upper()

        if choice == "F":
            if save_favorite(item["name"], item["key"]):
                print(f"  {c.G}✅ သိမ်းပြီးပါပြီ!{c.rst}\n")
            else:
                print(f"  {c.Y}⚠️ ရှိပြီးသား{c.rst}\n")
            input(f"  {c.D}Enter...{c.rst}")
        elif choice == "N" and current_index + 1 < len(all_keys):
            current_index += 1
        elif choice == "P" and current_index > 0:
            current_index -= 1
        elif choice == "Q":
            break


def favorites_menu():
    while True:
        header()
        favorites = load_favorites()
        print(f"  {c.Y}⭐ အကြိုက်ဆုံးများ{c.rst}")
        divider()

        if not favorites:
            print(f"  {c.D}အကြိုက်ဆုံး မရှိသေးပါ။ Key ရတဲ့အခါ [F] နှိပ်ပါ။{c.rst}")
        else:
            for idx, entry in enumerate(favorites, 1):
                if "|" in entry:
                    name, key = entry.split("|", 1)
                    print(f"  {c.C}[{idx}]{c.rst} {name}")
                    print(f"      {c.W}{key}{c.rst}")
                    if copy_to_clipboard(key):
                        print(f"      {c.G}✅ ကူးယူပြီး{c.rst}")
                    print()

        divider()
        print(f"  {c.C}[Q]{c.rst} ပြန်မည်   {c.C}[A]{c.rst} အားလုံးဖျက်မည်")
        sel = input(f"  {c.P}▶ : {c.rst}").strip().upper()
        if sel == "Q":
            break
        elif sel == "A":
            if input(f"  {c.R}ဖျက်မှာလား? y/n: {c.rst}").lower() == "y":
                if os.path.exists(FAV_FILE):
                    os.remove(FAV_FILE)
                    print(f"  {c.G}✅ ဖျက်ပြီး{c.rst}")
                input(f"  {c.D}Enter...{c.rst}")
                break


def main_menu():
    while True:
        header()
        print(f"  {c.Y}📂 ပင်မမီနူး{c.rst}")
        divider()
        print(f"  {c.G}⭐ [0]  အကောင်းဆုံး Key ကို ရှာမည် — အကြံပြု{c.rst}")
        print()
        print(f"  {c.C}[1]{c.rst} Shadowmere JSON")
        print(f"  {c.C}[2]{c.rst} Shadowmere Base64  ← အရင်စမ်းကြည့်ပါ")
        print(f"  {c.C}[3]{c.rst} VLESS List")
        print(f"  {c.C}[4]{c.rst} ⭐ အကြိုက်ဆုံးများ")
        print()
        print(f"  {c.R}[9]{c.rst} ထွက်မည်")
        divider()

        choice = input(f"  {c.P}▶ ရွေးချယ်ပါ : {c.rst}").strip()

        if choice == "0":
            find_best_key()
        elif choice == "9":
            clear()
            print(f"\n  {c.C}👋 ကျေးဇူးပြု၍ ပြန်လာပါ။{c.rst}\n")
            sys.exit(0)
        elif choice == "4":
            favorites_menu()
        elif choice in API_LIST:
            name, url, data_type = API_LIST[choice]
            header()
            print(f"  {c.Y}📥 {name} မှ ဒေတာရယူနေသည်...{c.rst}")

            data = None
            if data_type == "json":
                data = fetch_json(url)
            elif data_type == "b64":
                data = fetch_b64(url)
            elif data_type == "txt":
                data = fetch_txt(url)

            if not data:
                print(f"  {c.R}❌ ဒေတာမရပါ။{c.rst}")
                input(f"  {c.D}Enter...{c.rst}")
                continue

            header()
            print(f"  {c.Y}📋 {name} — ရလဒ်များ{c.rst}")
            divider()

            items = []
            if data_type == "json" and isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        key = item.get("url") or item.get("link") or ""
                        sname = item.get("name") or item.get("remarks") or f"Server {len(items)+1}"
                        if key and (key.startswith("vless://") or key.startswith("ss://")):
                            items.append({"name": sname, "key": key})
            elif data_type in ["b64", "txt"] and isinstance(data, list):
                for key in data:
                    sname, full_key = parse_key_info(key)
                    if full_key:
                        items.append({"name": sname, "key": full_key})

            if not items:
                print(f"  {c.R}❌ Key မတွေ့ပါ။{c.rst}")
                print(f"  {c.Y}💡 အကြံပြု: အခြားအရင်းအမြစ်ကို စမ်းကြည့်ပါ။{c.rst}")
                input(f"  {c.D}Enter...{c.rst}")
                continue

            print(f"  {c.G}✅ Server {len(items)} ခု တွေ့ရှိခဲ့သည်။{c.rst}\n")
            for idx, item in enumerate(items, 1):
                print(f"  {c.C}[{idx}]{c.rst} {item['name']}")
            divider()

            sel = input(f"  {c.P}▶ နံပါတ်ရွေးပါ သို့မဟုတ် [Q] ပြန်ရန် : {c.rst}").strip().upper()
            if sel == "Q":
                continue

            try:
                idx = int(sel) - 1
                if 0 <= idx < len(items):
                    item = items[idx]
                    key = item["key"]
                    sname = item["name"]
                    header()
                    divider(f"Server #{idx+1}")
                    print(f"  {c.G}📍 နာမည်:{c.rst} {sname}")
                    print(f"  {c.G}🔑 VPN Key:{c.rst}")
                    print(f"{c.W}{key}{c.rst}")
                    divider()

                    if copy_to_clipboard(key):
                        print(f"  {c.G}✅ ကူးယူပြီးပါပြီ!{c.rst}")
                    else:
                        print(f"  {c.Y}⚠️ ကိုယ်တိုင်ကူးယူပါ{c.rst}")
                    divider()

                    while True:
                        print(f"  {c.C}[F]{c.rst} သိမ်းမည်   {c.C}[Q]{c.rst} ပြန်မည်")
                        act = input(f"  {c.P}▶ : {c.rst}").strip().upper()
                        if act == "F":
                            if save_favorite(sname, key):
                                print(f"  {c.G}✅ သိမ်းပြီး!{c.rst}")
                            input(f"  {c.D}Enter...{c.rst}")
                        elif act == "Q":
                            break
            except ValueError:
                pass


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        clear()
        print(f"\n\n  {c.C}👋 ထွက်လိုက်ပါပြီ။{c.rst}\n")
        sys.exit(0)
    except Exception as e:
        clear()
        print(f"\n  {c.R}❌ အမှား: {str(e)}{c.rst}")
        input(f"  {c.D}Enter...{c.rst}")
        
