#!/usr/bin/env python3
# VPN Key Generator — Premium Edition
import urllib.request
import urllib.error
import json
import base64
import os
import sys

os.environ["TERM"] = "xterm-256color"
VERSION = "4.8 ✨ PREMIUM"
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

def clear(): os.system("clear")
C = Colors()

def header():
    clear()
    fav_count = len(load_favorites())
    print(f"{C.P}╔════════════════════════════════════════╗{C.rst}")
    print(f"{C.P}║{C.rst}{C.Y}  ✨ VPN KEY GENERATOR PREMIUM v{VERSION.split()[1]} ✨{C.rst}{C.P}║{C.rst}")
    print(f"{C.P}╠════════════════════════════════════════╣{C.rst}")
    print(f"{C.P}║{C.rst}  {C.C}📡 Status:{C.rst} Online ✅  |  {C.C}⭐ Favorites:{C.rst} {fav_count}{C.P}║{C.rst}")
    print(f"{C.P}╚════════════════════════════════════════╝{C.rst}\n")

def divider(title=""):
    print(f"{C.C}─── {title} {'─'*(40-len(title))}{C.rst}" if title else f"{C.D}─"*45+C.rst)

def load_favorites():
    if not os.path.exists(FAV_FILE): return []
    try:
        with open(FAV_FILE,"r",encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except: return []

def save_favorite(name, key):
    favs = load_favorites()
    entry = f"{name}|{key}"
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

def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as response:
            content = response.read().decode().strip()
            try:
                data = json.loads(content)
                if isinstance(data, list): return data
            except: pass
            lines = content.splitlines()
            result = []
            for line in lines:
                line = line.strip()
                if line:
                    try: result.append(json.loads(line))
                    except: pass
            return result if result else None
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

def find_best_key():
    header()
    print(f"  {C.Y}🔍 ရှာဖွေနေသည်...{C.rst}\n")
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
        header(); divider(f"Key #{idx+1}/{len(all_keys)}")
        print(f"  {C.G}နာမည်:{C.rst} {item['name']}")
        print(f"  {C.C}အရင်းအမြစ်:{C.rst} {item['source']}")
        divider(); print(f"  {C.Y}Key:{C.rst}\n{C.W}{item['key']}{C.rst}"); divider()
        if copy_to_clipboard(item['key']): print(f"  {C.G}✅ ကူးယူပြီးပါပြီ{C.rst}")
        else: print(f"  {C.Y}အပေါ်က Key ကို ကူးယူပါ{C.rst}")
        print(f"\n  {C.C}[F]{C.rst}သိမ်း  {C.C}[N]{C.rst}နောက်တစ်ခု  {C.C}[P]{C.rst}ယခင်  {C.C}[Q]{C.rst}ပြန်")
        c = input("  ▶ : ").strip().upper()
        if c=="F": save_favorite(item['name'],item['key']); print(f"  {C.G}✅ သိမ်းပြီး{C.rst}\n"); input("  Enter...")
        elif c=="N" and idx+1<len(all_keys): idx+=1
        elif c=="P" and idx>0: idx-=1
        elif c=="Q": break

def favorites_menu():
    while True:
        header(); favs=load_favorites(); print(f"  {C.Y}⭐ အကြိုက်ဆုံးများ{C.rst}\n"); divider()
        if not favs: print(f"  {C.D}မရှိသေးပါ။ Key ရတဲ့အခါ [F] နှိပ်ပါ။{C.rst}")
        else:
            for i,e in enumerate(favs,1):
                if "|" in e: n,k=e.split("|",1); print(f"  {C.C}[{i}]{C.rst} {n}"); print(f"      {C.W}{k}{C.rst}"); copy_to_clipboard(k) and print(f"      {C.G}✅ ကူးယူပြီး{C.rst}")
        divider(); print(f"  {C.C}[Q]{C.rst}ပြန်  {C.C}[A]{C.rst}အားလုံးဖျက်")
        sel=input("  ▶ : ").strip().upper()
        if sel=="Q": break
        elif sel=="A" and input(f"  {C.R}ဖျက်မှာလား? y/n:{C.rst}").lower()=="y":
            os.path.exists(FAV_FILE) and os.remove(FAV_FILE); break

def main_menu():
    while True:
        header()
        print(f"  {C.Y}📂 ပင်မမီနူး{C.rst}\n"); divider()
        print(f"  {C.G}⭐ [0] အကောင်းဆုံး Key ရှာမည် — အကြံပြု{C.rst}\n")
        print(f"  {C.C}[1]{C.rst} Shadowmere JSON")
        print(f"  {C.C}[2]{C.rst} Shadowmere Base64")
        print(f"  {C.C}[3]{C.rst} VLESS List")
        print(f"  {C.C}[4]{C.rst} ⭐ အကြိုက်ဆုံးများ\n")
        print(f"  {C.R}[9]{C.rst} ထွက်မည်")
        divider()
        ch=input("  ▶ ရွေးပါ : ").strip()
        if ch=="0": find_best_key()
        elif ch=="9": clear(); print(f"\n  {C.C}👋 ကျေးဇူးတင်ပါတယ်။{C.rst}\n"); sys.exit(0)
        elif ch=="4": favorites_menu()
        elif ch in API_LIST:
            name,url,dtype=API_LIST[ch]
            header(); print(f"  {C.Y}{name} မှ ဒေတာရယူနေသည်...{C.rst}\n")
            data = {"json":fetch_json,"b64":fetch_b64,"txt":fetch_txt}[dtype](url)
            if not data: input(f"  {C.R}မရပါ။ Enter...{C.rst}"); continue
            items=[]
            if dtype=="json" and isinstance(data,list):
                for item in data:
                    if isinstance(item,dict):
                        key=item.get("url") or item.get("link") or ""
                        n=item.get("name") or item.get("remarks") or "Server"
                        if key and (key.startswith("vless://") or key.startswith("ss://")): items.append({"name":n,"key":key})
            elif dtype in ["b64","txt"] and isinstance(data,list):
                for k in data:
                    n,vk=parse_key_info(k)
                    if vk: items.append({"name":n,"key":vk})
            if not items: input(f"  {C.R}Key မတွေ့ပါ။ အခြားရွေးပါ။ Enter...{C.rst}"); continue
            for i,x in enumerate(items,1): print(f"  {C.C}[{i}]{C.rst} {x['name']}")
            sel=input(f"\n  ▶ နံပါတ်ရွေးပါ [Q]ပြန် : ").strip().upper()
            if sel=="Q": continue
            try:
                idx=int(sel)-1
                if 0<=idx<len(items):
                    it=items[idx]; header(); divider(it['name'])
                    print(f"  {C.G}Key:{C.rst}\n{C.W}{it['key']}{C.rst}"); divider()
                    copy_to_clipboard(it['key']) and print(f"  {C.G}✅ ကူးယူပြီး{C.rst}")
                    while True:
                        a=input(f"  {C.C}[F]{C.rst}သိမ်း  {C.C}[Q]{C.rst}ပြန် : ").strip().upper()
                        if a=="F": save_favorite(it['name'],it['key']); print(f"  {C.G}✅ သိမ်းပြီး{C.rst}\n"); input("  Enter...")
                        elif a=="Q": break
            except: pass

if __name__=="__main__":
    try: main_menu()
    except KeyboardInterrupt: clear(); print(f"\n  {C.C}👋 ပြီးပါပြီ။{C.rst}\n"); sys.exit(0)
    
