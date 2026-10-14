#!/usr/bin/env python3
# ==========================================================
#    🚀 Ultimate VPN Key Finder — Dream Edition GUI
# ==========================================================
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import urllib.request, base64, socket, time, os, datetime, threading

# 🎨 Color Theme
COLORS = {
    "bg": "#0B0C10",
    "card": "#1F2833",
    "accent": "#66FCF1",
    "blue": "#45A29E",
    "text": "#C5C6C7",
    "white": "#FFFFFF",
    "green": "#2ECC71",
    "yellow": "#F1C40F",
    "red": "#E74C3C",
    "purple": "#9B59B6"
}

# 🌐 YOUR SOURCES - DO NOT CHANGE
SOURCES = [
    ("V2Nodes", "https://www.v2nodes.com/subscriptions/country/all/?key=72BEE427C23A1AF", "b64"),
    ("Shadowmere", "https://shadowmere.xyz/api/b64sub/", "b64"),
    ("V2Ray-Vault", "https://raw.githubusercontent.com/Argh73/V2Ray-Vault/main/data/sub/all_configs.txt", "txt"),
    ("V2Ray-Configs SS", "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Splitted-By-Protocol/ss.txt", "txt"),
]

class VPNKeyFinderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Ultimate VPN Key Finder — Dream Edition ✨")
        self.root.geometry("750x650")
        self.root.resizable(True, True)
        self.root.config(bg=COLORS["bg"])

        self.vless_data = []
        self.ss_data = []
        self.is_scanning = False

        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background=COLORS["bg"])
        style.configure("Card.TFrame", background=COLORS["card"], relief="flat")

        style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"], font=("Segoe UI", 10))
        style.configure("Title.TLabel", background=COLORS["bg"], foreground=COLORS["accent"], font=("Segoe UI", 18, "bold"))
        style.configure("Subtitle.TLabel", background=COLORS["bg"], foreground=COLORS["blue"], font=("Segoe UI", 12))
        style.configure("CardTitle.TLabel", background=COLORS["card"], foreground=COLORS["white"], font=("Segoe UI", 11, "bold"))
        style.configure("CardText.TLabel", background=COLORS["card"], foreground=COLORS["text"], font=("Segoe UI", 10))

        style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=10, relief="flat")
        style.configure("Accent.TButton", background=COLORS["accent"], foreground=COLORS["bg"])
        style.map("Accent.TButton", background=[("active", COLORS["blue"])])

        style.configure("Green.TButton", background=COLORS["green"], foreground="#FFFFFF")
        style.map("Green.TButton", background=[("active", "#27AE60")])

        style.configure("Yellow.TButton", background=COLORS["yellow"], foreground="#2C3E50")
        style.map("Yellow.TButton", background=[("active", "#F39C12")])

        style.configure("Red.TButton", background=COLORS["red"], foreground="#FFFFFF")
        style.map("Red.TButton", background=[("active", "#C0392B")])

        style.configure("TProgressbar", background=COLORS["accent"], troughcolor=COLORS["card"], bordercolor=COLORS["bg"], lightcolor=COLORS["accent"], darkcolor=COLORS["blue"])

    def build_ui(self):
        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = ttk.Label(main_frame, text="🚀 Ultimate VPN Key Finder", style="Title.TLabel")
        title_label.pack(pady=(0, 5))

        subtitle_label = ttk.Label(main_frame, text="Dream Edition ✨", style="Subtitle.TLabel")
        subtitle_label.pack(pady=(0, 20))

        # Info Card
        info_card = ttk.Frame(main_frame, style="Card.TFrame")
        info_card.pack(fill=tk.X, pady=(0, 15))

        self.network_label = ttk.Label(info_card, text="📡 Network: Detecting...", style="CardText.TLabel")
        self.network_label.pack(anchor=tk.W, padx=15, pady=(10, 5))

        self.source_label = ttk.Label(info_card, text="📦 Sources: 4", style="CardText.TLabel")
        self.source_label.pack(anchor=tk.W, padx=15, pady=5)

        self.vless_label = ttk.Label(info_card, text="🟦 VLESS: 0 keys", style="CardText.TLabel")
        self.vless_label.pack(anchor=tk.W, padx=15, pady=5)

        self.ss_label = ttk.Label(info_card, text="🟧 SS: 0 keys", style="CardText.TLabel")
        self.ss_label.pack(anchor=tk.W, padx=15, pady=(5, 10))

        # Button Grid
        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.pack(fill=tk.X, pady=(0, 15))

        self.load_btn = ttk.Button(button_frame, text="🔄 Load All Sources", style="Accent.TButton", command=self.load_sources_thread)
        self.load_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.vless_btn = ttk.Button(button_frame, text="🟦 Test VLESS", style="Green.TButton", command=lambda: self.start_scan("VLESS"), state=tk.DISABLED)
        self.vless_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.ss_btn = ttk.Button(button_frame, text="🟧 Test SS", style="Yellow.TButton", command=lambda: self.start_scan("SS"), state=tk.DISABLED)
        self.ss_btn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.view_btn = ttk.Button(button_frame, text="📄 View Saved", style="Accent.TButton", command=self.view_saved)
        self.view_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.exit_btn = ttk.Button(button_frame, text="❌ Exit", style="Red.TButton", command=self.root.quit)
        self.exit_btn.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, style="TProgressbar", mode="determinate")
        self.progress.pack(fill=tk.X, pady=(0, 15))

        # Result Box
        result_frame = ttk.Frame(main_frame, style="Card.TFrame")
        result_frame.pack(fill=tk.BOTH, expand=True)

        result_title = ttk.Label(result_frame, text="📋 Results", style="CardTitle.TLabel")
        result_title.pack(anchor=tk.W, padx=15, pady=(10, 5))

        self.result_text = scrolledtext.ScrolledText(result_frame, height=15, bg=COLORS["bg"], fg=COLORS["text"], insertbackground=COLORS["accent"], font=("Segoe UI", 9))
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))

        self.detect_network()

    def detect_network(self):
        try:
            import subprocess
            r = subprocess.run(['ip', 'link'], capture_output=True, text=True, timeout=3)
            if 'wlan' in r.stdout.lower() or 'wlp' in r.stdout.lower():
                net = "📡 WiFi"
            else:
                net = "📱 Mobile Data"
        except:
            net = "❓ Unknown"
        self.network_label.config(text=f"📡 Network: {net}")

    def fetch(self, url):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read().decode("utf-8", errors="ignore")
        except:
            return None

    def parse(self, text, fmt):
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
                name = "Server"
                if "#" in line:
                    try:
                        from urllib.parse import unquote
                        name = unquote(line.split("#")[-1])[:38]
                    except:
                        name = line.split("#")[-1][:38]
                if line.startswith("vless://"):
                    keys.append({"type": "VLESS", "name": name, "url": line})
                elif line.startswith("ss://"):
                    keys.append({"type": "SS", "name": name, "url": line})
        except:
            pass
        return keys

    def ping_test(self, url):
        try:
            from urllib.parse import urlparse
            p = urlparse(url)
            host = p.hostname
            port = p.port or 443
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            start = time.time()
            s.connect((host, int(port)))
            ms = int((time.time() - start) * 1000)
            s.close()
            if ms < 80:
                level = "🚀 Fast"
                score = 5
            elif ms < 150:
                level = "✅ Good"
                score = 4
            elif ms < 250:
                level = "⚡ Normal"
                score = 3
            elif ms < 400:
                level = "⚠️ Slow"
                score = 2
            else:
                level = "🐢 Very Slow"
                score = 1
            return True, ms, level, score
        except:
            return False, 9999, "❌ Offline", 0

    def load_sources_thread(self):
        if self.is_scanning:
            return
        self.is_scanning = True
        self.load_btn.config(state=tk.DISABLED)
        self.result_text.delete(1.0, tk.END)
        self.progress.config(maximum=len(SOURCES), value=0)

        def task():
            self.vless_data.clear()
            self.ss_data.clear()
            for name, url, fmt in SOURCES:
                self.result_text.insert(tk.END, f"🔄 Loading {name}...\n")
                self.result_text.update()
                text = self.fetch(url)
                if text:
                    keys = self.parse(text, fmt)
                    v_count = sum(1 for k in keys if k["type"] == "VLESS")
                    s_count = sum(1 for k in keys if k["type"] == "SS")
                    self.result_text.insert(tk.END, f"✅ {name} loaded: VLESS {v_count}, SS {s_count}\n\n")
                    for k in keys:
                        if k["type"] == "VLESS":
                            self.vless_data.append(k)
                        else:
                            self.ss_data.append(k)
                else:
                    self.result_text.insert(tk.END, f"❌ {name} failed\n\n")
                self.progress.step(1)
                self.progress.update()

            self.vless_label.config(text=f"🟦 VLESS: {len(self.vless_data)} keys")
            self.ss_label.config(text=f"🟧 SS: {len(self.ss_data)} keys")
            self.vless_btn.config(state=tk.NORMAL if self.vless_data else tk.DISABLED)
            self.ss_btn.config(state=tk.NORMAL if self.ss_data else tk.DISABLED)
            self.load_btn.config(state=tk.NORMAL)
            self.is_scanning = False

        threading.Thread(target=task, daemon=True).start()

    def start_scan(self, key_type):
        if self.is_scanning:
            return
        keys = self.vless_data if key_type == "VLESS" else self.ss_data
        if not keys:
            messagebox.showwarning("Warning", f"No {key_type} keys found. Load sources first!")
            return

        self.is_scanning = True
        self.vless_btn.config(state=tk.DISABLED)
        self.ss_btn.config(state=tk.DISABLED)
        self.result_text.delete(1.0, tk.END)
        self.progress.config(maximum=len(keys), value=0)

        def task():
            results = []
            for i, k in enumerate(keys, 1):
                self.result_text.insert(tk.END, f"[{i}/{len(keys)}] Testing {k['name'][:35]}...\n")
                self.result_text.update()
                ok, ms, level, score = self.ping_test(k["url"])
                if ok:
                    k["ms"] = ms
                    k["level"] = level
                    k["score"] = score
                    results.append(k)
                self.progress.step(1)
                self.progress.update()

            results.sort(key=lambda x: x["ms"])
            self.result_text.delete(1.0, tk.END)

            if not results:
                self.result_text.insert(tk.END, "❌ No working servers found\n")
            else:
                self.result_text.insert(tk.END, f"🎉 Found {len(results)} working servers\n\n")
                for i, s in enumerate(results, 1):
                    self.result_text.insert(tk.END, f"[{i}] {s['level']}  Ping: {s['ms']}ms  {'⭐' * s['score']}\n")
                    self.result_text.insert(tk.END, f"📌 {s['name']}\n")
                    self.result_text.insert(tk.END, f"🔑 {s['url'][:80]}...\n\n")

                with open("working_keys.txt", "w", encoding="utf-8") as f:
                    f.write("=" * 50 + "\n")
                    f.write("🚀 Ultimate VPN Key Finder — Dream Edition ✨\n")
                    f.write("=" * 50 + "\n")
                    f.write(f"Updated : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Network : {self.network_label.cget('text')}\n")
                    f.write(f"Total   : {len(results)} servers\n")
                    f.write("=" * 50 + "\n\n")
                    for s in results:
                        f.write(f"{s['url']}\n")

                self.result_text.insert(tk.END, f"✅ Saved → working_keys.txt\n")

            self.vless_btn.config(state=tk.NORMAL if self.vless_data else tk.DISABLED)
            self.ss_btn.config(state=tk.NORMAL if self.ss_data else tk.DISABLED)
            self.is_scanning = False

        threading.Thread(target=task, daemon=True).start()

    def view_saved(self):
        if not os.path.exists("working_keys.txt"):
            messagebox.showinfo("Info", "No saved keys found. Run a scan first!")
            return
        with open("working_keys.txt", "r", encoding="utf-8") as f:
            content = f.read()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, content)

if __name__ == "__main__":
    root = tk.Tk()
    app = VPNKeyFinderGUI(root)
    root.mainloop()
        
