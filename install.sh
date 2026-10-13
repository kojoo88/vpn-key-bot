#!/data/data/com.termux/files/usr/bin/bash
pkg update -y && pkg install python -y
pip install requests
cd ~
if [ ! -d "vpn-key-bot" ]; then
    git clone https://github.com/kojoo88/vpn-key-bot.git
fi
cd ~/vpn-key-bot
git pull
chmod +x vpn.py
if ! grep -q "alias vpn" ~/.bashrc; then
    echo "alias vpn='cd ~/vpn-key-bot && python vpn.py'" >> ~/.bashrc
fi
clear
echo "✅ ပြီးပါပြီ! ဖွင့်ရန်: vpn"
