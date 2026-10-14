#!/usr/bin/env python3
import urllib.request, base64, socket, time, os, datetime, random, sys

# COLORS
BLK = "\033[38;5;234m"
BLU = "\033[38;5;117m"
CYN = "\033[38;5;80m"
GRN = "\033[38;5;114m"
YEL = "\033[38;5;221m"
ORG = "\033[38;5;215m"
RED = "\033[38;5;209m"
PUR = "\033[38;5;141m"
PINK = "\033[38;5;212m"
LIME = "\033[38;5;156m"
WHT = "\033[38;5;255m"
DIM = "\033[2m"
BD  = "\033[1m"
RST = "\033[0m"

def clear(): os.system("clear")

def main():
    clear()
    print(PUR + "="*50 + RST)
    print(PUR + "|" + RST + "    VPN Key Finder - Test OK     " + PUR + "|" + RST)
    print(PUR + "="*50 + RST)
    print(GRN + "  Program အလုပ်လုပ်နေပါတယ်!" + RST)
    print()
    print("  [1] Load Sources")
    print("  [2] VLESS Servers")
    print("  [3] SS Servers")
    print("  [0] Exit")
    print()
    while True:
        ch = input("Choose -> ")
        if ch == "0":
            print(GRN + "  Bye!" + RST)
            break
        else:
            print(YEL + f"  You chose: {ch}" + RST)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(RED + f"Error: {e}" + RST)
        
