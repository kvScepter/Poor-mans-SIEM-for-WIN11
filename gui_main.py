import customtkinter as ctk
import threading
import json
import winreg
from datetime import datetime
from log_monitor import monitor_events
from network_monitor import monitor_network

# Modernit väriteemat
ACCENT_BLUE = "#3b8ed0"
BG_DARK = "#1a1a1a"
CARD_BG = "#242424"
TEXT_DIM = "#a0a0a0"

class SIEMModernGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SIEM Ultimate Dashboard")
        self.geometry("1200x800")
        ctk.set_appearance_mode("dark")
        
        self.load_config()
        self.log_count = 0
        self.net_count = 0

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. MODERNI SIVUPALKKI
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#121212")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="SIEM", font=ctk.CTkFont(family="Inter", size=28, weight="bold"), text_color=ACCENT_BLUE)
        self.logo_label.pack(pady=(40, 10))
        
        self.btn_events = self.create_nav_button("📊 Event Log", lambda: self.tabs.set("Event Log"))
        self.btn_network = self.create_nav_button("📡 Network Traffic", lambda: self.tabs.set("Network Traffic"))
        self.btn_forensics = self.create_nav_button("🔍 Forensics", lambda: self.tabs.set("Forensics"))
        self.btn_settings = self.create_nav_button("⚙️ Settings", lambda: self.tabs.set("Settings"))

        # Statistiikkakortti
        self.stat_card = ctk.CTkFrame(self.sidebar, fg_color=CARD_BG, corner_radius=12)
        self.stat_card.pack(pady=40, padx=20, fill="x")
        self.log_stat = ctk.CTkLabel(self.stat_card, text=f"Events: {self.log_count}", font=ctk.CTkFont(size=13))
        self.log_stat.pack(pady=10)

        # 2. PÄÄSISÄLTÖ
        self.container = ctk.CTkFrame(self, fg_color=BG_DARK, corner_radius=0)
        self.container.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        
        self.tabs = ctk.CTkTabview(self.container, fg_color="transparent", segmented_button_fg_color=CARD_BG)
        self.tabs.pack(fill="both", expand=True)
        
        self.tab_log = self.tabs.add("Event Log")
        self.tab_net = self.tabs.add("Network Traffic")
        self.tab_forensic = self.tabs.add("Forensics")
        self.tab_set = self.tabs.add("Settings")

        # Lokilaatikot
        self.log_box = self.create_log_view(self.tab_log)
        self.net_box = self.create_log_view(self.tab_net)

        # --- FORENSICS TAB ---
        self.setup_forensics_ui()

        # --- SETTINGS TAB ---
        self.setup_settings_ui()

        self.start_monitoring()

    def create_nav_button(self, text, command):
        btn = ctk.CTkButton(self.sidebar, text=text, command=command, fg_color="transparent", 
                            text_color="white", hover_color=CARD_BG, anchor="w", height=45)
        btn.pack(fill="x", padx=15, pady=2)
        return btn

    def create_log_view(self, parent):
        box = ctk.CTkTextbox(parent, font=("Consolas", 12), fg_color="#000000", border_width=1, border_color="#333333", corner_radius=8)
        box.pack(fill="both", expand=True, padx=5, pady=5)
        return box

    def setup_forensics_ui(self):
        """Luo Forensics-näkymän Win+R historialle."""
        frame = ctk.CTkFrame(self.tab_forensic, fg_color="transparent")
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text="Windows Run (Win+R) Command History", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ctk.CTkLabel(frame, text="Most recently used commands from the Run dialog.", text_color=TEXT_DIM).pack(anchor="w", pady=(0, 10))
        
        self.history_box = ctk.CTkTextbox(frame, height=300, fg_color="#000000", border_width=1, border_color="#333333")
        self.history_box.pack(fill="x", pady=10)
        
        refresh_btn = ctk.CTkButton(frame, text="Scan Run History", fg_color=ACCENT_BLUE, command=self.scan_history)
        refresh_btn.pack(pady=10)

    def scan_history(self):
        """Lukee Win+R historian rekisteristä ja näyttää sen käyttöliittymässä."""
        self.history_box.delete("0.0", "end")
        path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_READ)
            mru_list, _ = winreg.QueryValueEx(key, "MRUList")
            for letter in mru_list:
                cmd_value, _ = winreg.QueryValueEx(key, letter)
                clean_cmd = cmd_value.split('\\')[0]
                self.history_box.insert("end", f"• {clean_cmd}\n")
            winreg.CloseKey(key)
        except Exception:
            self.history_box.insert("end", "Error: Run history not found or disabled.")

    def setup_settings_ui(self):
        frame = ctk.CTkFrame(self.tab_set, fg_color="transparent")
        frame.pack(pady=40, padx=40, fill="both", expand=True)
        ctk.CTkLabel(frame, text="Whitelist Management", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        self.list_display = ctk.CTkTextbox(frame, height=120, fg_color=CARD_BG)
        self.list_display.pack(fill="x", pady=10)
        self.refresh_list()
        self.entry = ctk.CTkEntry(frame, placeholder_text="e.g. spotify.exe", height=40)
        self.entry.pack(fill="x", pady=10)
        ctk.CTkButton(frame, text="Add to Whitelist", fg_color=ACCENT_BLUE, command=self.add_to_list).pack(fill="x")

    def add_to_list(self):
        new = self.entry.get().strip()
        if new and new not in self.config['whitelist_processes']:
            self.config['whitelist_processes'].append(new)
            with open('config.json', 'w') as f: json.dump(self.config, f, indent=4)
            self.refresh_list()
            self.entry.delete(0, 'end')

    def refresh_list(self):
        self.list_display.delete("0.0", "end")
        self.list_display.insert("0.0", ", ".join(self.config['whitelist_processes']))

    def load_config(self):
        with open('config.json', 'r') as f: self.config = json.load(f)

    def update_display(self, tag, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{ts}] {msg}\n"
        if "SECURITY" in tag:
            self.log_box.insert("end", formatted)
            self.log_box.see("end")
            self.log_count += 1
            self.log_stat.configure(text=f"Events: {self.log_count}")
        else:
            self.net_box.insert("end", formatted)
            self.net_box.see("end")
            self.net_count += 1

    def start_monitoring(self):
        def cb(t, m): self.after(0, self.update_display, t, m)
        threading.Thread(target=monitor_events, args=(self.config, cb), daemon=True).start()
        threading.Thread(target=monitor_network, args=(self.config, cb), daemon=True).start()

if __name__ == "__main__":
    app = SIEMModernGUI()
    app.mainloop()
