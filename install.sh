#!/data/data/com.termux/files/usr/bin/bash
pkg update -y && pkg upgrade -y
pkg install python git -y
pip install -r requirements.txt
cd ~/vpn-key-bot 2>/dev/null || git clone https://github.com/kojoo88/vpn-key-bot.git ~/vpn-key-bot
cd ~/vpn-key-bot
git pull
echo "alias vpn='cd ~/vpn-key-bot && python bot.py'" >> ~/.bashrc
clear
echo "✅ VPN Key Bot တပ်ဆင်ပြီးပါပြီ!"
echo "👉 ဖွင့်ရန်: vpn"
echo "💡 မရသေးရင်: source ~/.bashrc"
