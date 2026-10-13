import os
import urllib.request
import urllib.parse
import json
import base64
import time

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_URL = os.environ.get("API_URL")

_server_cache = None
_server_last_check = 0
CACHE_DURATION = 60

def get_servers():
    global _server_cache, _server_last_check
    now = time.time()
    if _server_cache and (now - _server_last_check) < CACHE_DURATION:
        return _server_cache
    try:
        req = urllib.request.Request(
            API_URL,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }
        )
        with urllib.request.urlopen(req, timeout=15) as res:
            data = json.loads(res.read().decode())
        if isinstance(data, list):
            _server_cache = data
            _server_last_check = now
            return data
        return []
    except Exception as e:
        print(f"API Error: {e}")
        return []

def get_updates(offset=None):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        if offset: url += f"?offset={offset}"
        with urllib.request.urlopen(url, timeout=10) as res:
            return json.loads(res.read().decode())
    except:
        return {"result": []}

def send_message(chat_id, text):
    try:
        data = urllib.parse.urlencode({"chat_id": chat_id, "text": text, "parse_mode": "HTML"}).encode()
        req = urllib.request.Request(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data=data)
        with urllib.request.urlopen(req, timeout=10) as res:
            return True
    except:
        return False

def generate_ss_link(server):
    try:
        userinfo = f"{server['method']}:{server['password']}"
        b64 = base64.b64encode(userinfo.encode()).decode().rstrip('=')
        return f"ss://{b64}@{server['server']}:{server['server_port']}#{server['remarks']}"
    except:
        return "❌ ဖော်ပြ၍မရပါ"

def main():
    last_update_id = 0
    print("✅ Bot အလုပ်လုပ်နေပြီ! Telegram မှာ /start ရိုက်ပါ")
    while True:
        updates = get_updates(last_update_id + 1)
        if "result" in updates and updates["result"]:
            for upd in updates["result"]:
                last_update_id = upd["update_id"]
                if "message" not in upd: continue
                msg = upd["message"]
                chat_id = msg["chat"]["id"]
                text = msg.get("text", "").strip().lower()
                
                if text == "/start":
                    send_message(chat_id, """👋 VPN Key Bot မှ ကြိုဆိုပါတယ်!

အမှာစာများ-
/all  - ဆာဗာအားလုံး
/sg   - Singapore 🇸🇬
/hk   - Hong Kong 🇭🇰
/jp   - Japan 🇯🇵
/kr   - Korea 🇰🇷
/us   - United States 🇺🇸
/nl   - Netherlands 🇳🇱
/de   - Germany 🇩🇪
/uk   - United Kingdom 🇬🇧
/za   - South Africa 🇿🇦
/br   - Brazil 🇧🇷
/at   - Austria 🇦🇹
/ca   - Canada 🇨🇦

ss:// လင့်ကို ကော်ပီကူးပြီး Shadowsocks မှာ အသုံးပြုပါ။""")
                
                elif text == "/all":
                    servers = get_servers()
                    if not servers:
                        send_message(chat_id, "❌ ဒေတာရယူ၍မရပါ")
                        continue
                    reply = f"✅ စုစုပေါင်း ဆာဗာ {len(servers)} လုံး\n\n"
                    for s in servers[:12]:
                        reply += f"{s.get('remarks','အမည်မသိ')}\n<code>{generate_ss_link(s)}</code>\n\n"
                    send_message(chat_id, reply)
                
                else:
                    kw_map = {
                        "sg": ["sg", "singapore"], "hk": ["hk", "hong"],
                        "jp": ["jp", "japan"], "kr": ["kr", "korea"],
                        "us": ["us", "united states"], "nl": ["nl", "netherlands"],
                        "de": ["de", "germany"], "uk": ["uk", "united kingdom"],
                        "za": ["za", "south africa", "johannesburg"],
                        "br": ["br", "brazil"], "at": ["at", "austria"],
                        "ca": ["ca", "canada"]
                    }
                    cmd = text.lstrip("/")
                    if cmd in kw_map:
                        servers = get_servers()
                        found = []
                        for s in servers:
                            rem = s.get("remarks", "").lower()
                            for kw in kw_map[cmd]:
                                if kw in rem:
                                    found.append(s)
                                    break
                        if not found:
                            reply = f"❌ {cmd.upper()} ဆာဗာ မတွေ့ပါ"
                        else:
                            reply = f"✅ {cmd.upper()} – စုစုပေါင်း {len(found)} ခု\n\n"
                            for s in found:
                                reply += f"{s['remarks']}\n<code>{generate_ss_link(s)}</code>\n\n"
                        send_message(chat_id, reply)
        time.sleep(2)

if __name__ == "__main__":
    main()
      
