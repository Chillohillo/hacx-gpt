#!/usr/bin/env python3
"""
WiFi Security Demonstration GUI
MBA AI Study Project - Professional Presentation Interface

This GUI provides a visual interface for demonstrating WiFi security risks
and attack vectors in an educational context.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import json
import os
from datetime import datetime
from typing import Dict, List

class WiFiDemoGUI:
    """Main GUI application for WiFi security demonstration"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("iOS WiFi Security Demonstration - MBA AI Study Project")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')
        
        # Demo state
        self.demo_running = False
        self.current_target = None
        self.attack_log = []
        
        # Create main notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_network_tab()
        self.create_attack_tab()
        self.create_exploit_tab()
        self.create_monitoring_tab()
        self.create_report_tab()
        
        # Start demo timer
        self.start_demo_timer()
        
    def create_dashboard_tab(self):
        """Create main dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Title
        title_label = tk.Label(dashboard_frame, 
                              text="iOS WiFi Security Demonstration",
                              font=("Arial", 20, "bold"),
                              fg='#00ff00',
                              bg='#2b2b2b')
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(dashboard_frame,
                                 text="MBA AI Study Project - Educational Purpose Only",
                                 font=("Arial", 12),
                                 fg='#cccccc',
                                 bg='#2b2b2b')
        subtitle_label.pack(pady=5)
        
        # Demo controls
        control_frame = tk.Frame(dashboard_frame, bg='#2b2b2b')
        control_frame.pack(pady=20)
        
        self.start_button = tk.Button(control_frame,
                                     text="Start Full Demo",
                                     command=self.start_full_demo,
                                     font=("Arial", 14, "bold"),
                                     bg='#00ff00',
                                     fg='black',
                                     width=15,
                                     height=2)
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = tk.Button(control_frame,
                                    text="Stop Demo",
                                    command=self.stop_demo,
                                    font=("Arial", 14, "bold"),
                                    bg='#ff0000',
                                    fg='white',
                                    width=15,
                                    height=2,
                                    state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        # Status display
        status_frame = tk.Frame(dashboard_frame, bg='#2b2b2b')
        status_frame.pack(pady=20, fill='both', expand=True)
        
        self.status_text = scrolledtext.ScrolledText(status_frame,
                                                    height=15,
                                                    font=("Consolas", 10),
                                                    bg='#1e1e1e',
                                                    fg='#00ff00',
                                                    insertbackground='#00ff00')
        self.status_text.pack(fill='both', expand=True, padx=10)
        
        # Demo progress
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(dashboard_frame,
                                           variable=self.progress_var,
                                           maximum=100)
        self.progress_bar.pack(fill='x', padx=10, pady=10)
        
    def create_network_tab(self):
        """Create network reconnaissance tab"""
        network_frame = ttk.Frame(self.notebook)
        self.notebook.add(network_frame, text="Network Reconnaissance")
        
        # Network scan controls
        scan_frame = tk.Frame(network_frame, bg='#2b2b2b')
        scan_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(scan_frame,
                 text="Scan Network",
                 command=self.scan_network,
                 bg='#0066cc',
                 fg='white',
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Device list
        device_frame = tk.Frame(network_frame, bg='#2b2b2b')
        device_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for devices
        columns = ('IP', 'MAC', 'Hostname', 'OS', 'Vulnerabilities')
        self.device_tree = ttk.Treeview(device_frame, columns=columns, show='headings')
        
        for col in columns:
            self.device_tree.heading(col, text=col)
            self.device_tree.column(col, width=150)
        
        self.device_tree.pack(fill='both', expand=True)
        
        # Device details
        detail_frame = tk.Frame(network_frame, bg='#2b2b2b')
        detail_frame.pack(fill='x', padx=10, pady=10)
        
        self.device_detail_text = scrolledtext.ScrolledText(detail_frame,
                                                           height=8,
                                                           font=("Consolas", 10),
                                                           bg='#1e1e1e',
                                                           fg='#00ff00')
        self.device_detail_text.pack(fill='both', expand=True)
        
        # Bind selection event
        self.device_tree.bind('<<TreeviewSelect>>', self.on_device_select)
        
    def create_attack_tab(self):
        """Create attack vectors tab"""
        attack_frame = ttk.Frame(self.notebook)
        self.notebook.add(attack_frame, text="Attack Vectors")
        
        # Attack selection
        attack_select_frame = tk.Frame(attack_frame, bg='#2b2b2b')
        attack_select_frame.pack(fill='x', padx=10, pady=10)
        
        attacks = [
            "WiFi Deauthentication",
            "Evil Twin Access Point", 
            "Karma Attack",
            "ARP Spoofing",
            "DNS Poisoning",
            "SSL Stripping",
            "Session Hijacking"
        ]
        
        self.attack_var = tk.StringVar(value=attacks[0])
        attack_menu = ttk.OptionMenu(attack_select_frame, self.attack_var, attacks[0], *attacks)
        attack_menu.pack(side=tk.LEFT, padx=5)
        
        tk.Button(attack_select_frame,
                 text="Execute Attack",
                 command=self.execute_attack,
                 bg='#cc0000',
                 fg='white',
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Attack log
        attack_log_frame = tk.Frame(attack_frame, bg='#2b2b2b')
        attack_log_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.attack_log_text = scrolledtext.ScrolledText(attack_log_frame,
                                                        font=("Consolas", 10),
                                                        bg='#1e1e1e',
                                                        fg='#ff6600')
        self.attack_log_text.pack(fill='both', expand=True)
        
    def create_exploit_tab(self):
        """Create exploit demonstration tab"""
        exploit_frame = ttk.Frame(self.notebook)
        self.notebook.add(exploit_frame, text="iOS Exploits")
        
        # Exploit selection
        exploit_select_frame = tk.Frame(exploit_frame, bg='#2b2b2b')
        exploit_select_frame.pack(fill='x', padx=10, pady=10)
        
        exploits = [
            "Kernel Exploit Chain (CVE-2023-32434)",
            "WebKit Exploit (CVE-2023-41990)",
            "Zero-Click Exploit",
            "Sandbox Escape",
            "Privilege Escalation"
        ]
        
        self.exploit_var = tk.StringVar(value=exploits[0])
        exploit_menu = ttk.OptionMenu(exploit_select_frame, self.exploit_var, exploits[0], *exploits)
        exploit_menu.pack(side=tk.LEFT, padx=5)
        
        tk.Button(exploit_select_frame,
                 text="Execute Exploit",
                 command=self.execute_exploit,
                 bg='#cc0000',
                 fg='white',
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Exploit details
        exploit_detail_frame = tk.Frame(exploit_frame, bg='#2b2b2b')
        exploit_detail_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.exploit_detail_text = scrolledtext.ScrolledText(exploit_detail_frame,
                                                            font=("Consolas", 10),
                                                            bg='#1e1e1e',
                                                            fg='#ff0066')
        self.exploit_detail_text.pack(fill='both', expand=True)
        
    def create_monitoring_tab(self):
        """Create monitoring demonstration tab"""
        monitoring_frame = ttk.Frame(self.notebook)
        self.notebook.add(monitoring_frame, text="Device Monitoring")
        
        # Monitoring controls
        monitor_control_frame = tk.Frame(monitoring_frame, bg='#2b2b2b')
        monitor_control_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(monitor_control_frame,
                 text="Start Monitoring",
                 command=self.start_monitoring,
                 bg='#0066cc',
                 fg='white',
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(monitor_control_frame,
                 text="Stop Monitoring",
                 command=self.stop_monitoring,
                 bg='#cc6600',
                 fg='white',
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Monitoring modules
        module_frame = tk.Frame(monitoring_frame, bg='#2b2b2b')
        module_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        modules = [
            "Screen Recording",
            "Keylogging",
            "Location Tracking",
            "Call Monitoring",
            "Message Interception",
            "App Usage Tracking",
            "Network Traffic Analysis",
            "File System Monitoring",
            "Camera Access",
            "Microphone Access"
        ]
        
        self.module_vars = {}
        for i, module in enumerate(modules):
            var = tk.BooleanVar(value=True)
            self.module_vars[module] = var
            tk.Checkbutton(module_frame,
                          text=module,
                          variable=var,
                          bg='#2b2b2b',
                          fg='#00ff00',
                          selectcolor='#1e1e1e',
                          font=("Arial", 10)).grid(row=i//2, column=i%2, sticky='w', padx=10, pady=5)
        
        # Monitoring log
        monitor_log_frame = tk.Frame(monitoring_frame, bg='#2b2b2b')
        monitor_log_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.monitor_log_text = scrolledtext.ScrolledText(monitor_log_frame,
                                                         font=("Consolas", 10),
                                                         bg='#1e1e1e',
                                                         fg='#00ccff')
        self.monitor_log_text.pack(fill='both', expand=True)
        
    def create_report_tab(self):
        """Create final report tab"""
        report_frame = ttk.Frame(self.notebook)
        self.notebook.add(report_frame, text="Final Report")
        
        # Report controls
        report_control_frame = tk.Frame(report_frame, bg='#2b2b2b')
        report_control_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(report_control_frame,
                 text="Generate Report",
                 command=self.generate_report,
                 bg='#00cc00',
                 fg='black',
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(report_control_frame,
                 text="Save Report",
                 command=self.save_report,
                 bg='#0066cc',
                 fg='white',
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Report display
        report_display_frame = tk.Frame(report_frame, bg='#2b2b2b')
        report_display_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.report_text = scrolledtext.ScrolledText(report_display_frame,
                                                    font=("Consolas", 10),
                                                    bg='#1e1e1e',
                                                    fg='#ffffff')
        self.report_text.pack(fill='both', expand=True)
        
    def start_demo_timer(self):
        """Start demo timer for progress updates"""
        def update_timer():
            if self.demo_running:
                current_time = time.time()
                elapsed = current_time - self.demo_start_time
                progress = min((elapsed / self.demo_duration) * 100, 100)
                self.progress_var.set(progress)
                
                if progress >= 100:
                    self.demo_running = False
                    self.stop_demo()
                else:
                    self.root.after(100, update_timer)
        
        self.demo_start_time = 0
        self.demo_duration = 300  # 5 minutes
        
    def start_full_demo(self):
        """Start the full demonstration"""
        self.demo_running = True
        self.demo_start_time = time.time()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Start demo in separate thread
        demo_thread = threading.Thread(target=self.run_demo_sequence)
        demo_thread.daemon = True
        demo_thread.start()
        
    def run_demo_sequence(self):
        """Run the complete demo sequence"""
        phases = [
            ("Network Reconnaissance", self.simulate_network_scan),
            ("Target Selection", self.simulate_target_selection),
            ("WiFi Attacks", self.simulate_wifi_attacks),
            ("MITM Attacks", self.simulate_mitm_attacks),
            ("iOS Exploits", self.simulate_ios_exploits),
            ("Persistence", self.simulate_persistence),
            ("Monitoring", self.simulate_monitoring),
            ("Report Generation", self.simulate_report_generation)
        ]
        
        for phase_name, phase_func in phases:
            if not self.demo_running:
                break
                
            self.log_status(f"Starting Phase: {phase_name}")
            phase_func()
            time.sleep(2)
            
    def simulate_network_scan(self):
        """Simulate network scanning"""
        self.log_status("Scanning network for devices...")
        time.sleep(1)
        
        # Add demo devices to treeview
        demo_devices = [
            ("192.168.1.100", "AA:BB:CC:DD:EE:01", "iPhone-13-Pro", "iOS 18.6", "CVE-2023-32434, CVE-2023-41990"),
            ("192.168.1.101", "AA:BB:CC:DD:EE:02", "MacBook-Pro-M2", "macOS 14.0", "CVE-2023-38606"),
            ("192.168.1.102", "AA:BB:CC:DD:EE:03", "iPad-Air-5th", "iOS 18.6", "CVE-2023-41990, CVE-2024-23225")
        ]
        
        for device in demo_devices:
            self.device_tree.insert('', 'end', values=device)
            time.sleep(0.5)
            
        self.log_status(f"Found {len(demo_devices)} devices on network")
        
    def simulate_target_selection(self):
        """Simulate target selection"""
        self.log_status("Analyzing potential targets...")
        time.sleep(1)
        
        # Select iPhone as target
        self.current_target = {
            "ip": "192.168.1.100",
            "hostname": "iPhone-13-Pro",
            "os": "iOS 18.6",
            "vulnerabilities": ["CVE-2023-32434", "CVE-2023-41990"]
        }
        
        self.log_status(f"Selected target: {self.current_target['hostname']} ({self.current_target['ip']})")
        self.log_status(f"OS Version: {self.current_target['os']}")
        self.log_status(f"Vulnerabilities: {', '.join(self.current_target['vulnerabilities'])}")
        
    def simulate_wifi_attacks(self):
        """Simulate WiFi attacks"""
        self.log_status("Executing WiFi attack vectors...")
        
        attacks = [
            "WiFi Deauthentication Attack",
            "Evil Twin Access Point Creation",
            "Karma Attack (Probe Response)"
        ]
        
        for attack in attacks:
            self.log_status(f"  [-] {attack}")
            self.attack_log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {attack}\n")
            self.attack_log_text.see(tk.END)
            time.sleep(0.8)
            
    def simulate_mitm_attacks(self):
        """Simulate MITM attacks"""
        self.log_status("Executing Man-in-the-Middle attacks...")
        
        mitm_attacks = [
            "ARP Spoofing",
            "DNS Cache Poisoning",
            "SSL/TLS Stripping",
            "Session Hijacking"
        ]
        
        for attack in mitm_attacks:
            self.log_status(f"  [-] {attack}")
            self.attack_log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {attack}\n")
            self.attack_log_text.see(tk.END)
            time.sleep(0.8)
            
    def simulate_ios_exploits(self):
        """Simulate iOS exploits"""
        self.log_status("Executing iOS-specific exploits...")
        
        exploits = [
            "Kernel Exploit Chain (CVE-2023-32434)",
            "WebKit Exploit (CVE-2023-41990)",
            "Zero-Click Exploit via iMessage"
        ]
        
        for exploit in exploits:
            self.log_status(f"  [-] {exploit}")
            self.exploit_detail_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {exploit}\n")
            self.exploit_detail_text.see(tk.END)
            time.sleep(1)
            
    def simulate_persistence(self):
        """Simulate persistence installation"""
        self.log_status("Installing persistence mechanisms...")
        
        persistence_methods = [
            "LaunchDaemon Installation",
            "LoginHook Configuration",
            "Kernel Module Loading",
            "Firmware Modification"
        ]
        
        for method in persistence_methods:
            self.log_status(f"  [-] {method}")
            time.sleep(0.8)
            
    def simulate_monitoring(self):
        """Simulate device monitoring"""
        self.log_status("Starting comprehensive device monitoring...")
        
        monitoring_modules = [
            "Screen Recording",
            "Keylogging",
            "Location Tracking",
            "Call Monitoring",
            "Message Interception"
        ]
        
        for module in monitoring_modules:
            self.log_status(f"  [-] Activating {module}")
            self.monitor_log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {module} active\n")
            self.monitor_log_text.see(tk.END)
            time.sleep(0.5)
            
    def simulate_report_generation(self):
        """Simulate report generation"""
        self.log_status("Generating final demonstration report...")
        time.sleep(1)
        self.generate_report()
        
    def stop_demo(self):
        """Stop the demonstration"""
        self.demo_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.log_status("Demonstration stopped")
        
    def scan_network(self):
        """Scan network for devices"""
        self.device_tree.delete(*self.device_tree.get_children())
        self.simulate_network_scan()
        
    def on_device_select(self, event):
        """Handle device selection"""
        selection = self.device_tree.selection()
        if selection:
            item = self.device_tree.item(selection[0])
            values = item['values']
            
            detail_text = f"""
Device Details:
==============
IP Address: {values[0]}
MAC Address: {values[1]}
Hostname: {values[2]}
Operating System: {values[3]}
Vulnerabilities: {values[4]}

Services Detected:
- SSH (Port 22)
- HTTP (Port 80)
- HTTPS (Port 443)
- iMessage (Port 5223)
- FaceTime (Port 5228)

Risk Assessment:
- High risk device
- Multiple critical vulnerabilities
- Potential for complete compromise
- Suitable for demonstration
"""
            self.device_detail_text.delete(1.0, tk.END)
            self.device_detail_text.insert(1.0, detail_text)
            
    def execute_attack(self):
        """Execute selected attack"""
        attack = self.attack_var.get()
        self.log_status(f"Executing: {attack}")
        self.attack_log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {attack} executed\n")
        self.attack_log_text.see(tk.END)
        
    def execute_exploit(self):
        """Execute selected exploit"""
        exploit = self.exploit_var.get()
        self.log_status(f"Executing: {exploit}")
        self.exploit_detail_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {exploit} executed\n")
        self.exploit_detail_text.see(tk.END)
        
    def start_monitoring(self):
        """Start device monitoring"""
        active_modules = [module for module, var in self.module_vars.items() if var.get()]
        self.log_status(f"Starting monitoring with {len(active_modules)} modules")
        
        for module in active_modules:
            self.monitor_log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {module} started\n")
            self.monitor_log_text.see(tk.END)
            
    def stop_monitoring(self):
        """Stop device monitoring"""
        self.log_status("Stopping device monitoring")
        self.monitor_log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring stopped\n")
        self.monitor_log_text.see(tk.END)
        
    def generate_report(self):
        """Generate demonstration report"""
        report = f"""
iOS WiFi Security Demonstration Report
=====================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Target Device:
- Hostname: {self.current_target['hostname'] if self.current_target else 'N/A'}
- IP Address: {self.current_target['ip'] if self.current_target else 'N/A'}
- OS Version: {self.current_target['os'] if self.current_target else 'N/A'}

Attack Vectors Demonstrated:
1. WiFi Deauthentication Attack
2. Evil Twin Access Point
3. Karma Attack (Probe Response)
4. ARP Spoofing
5. DNS Cache Poisoning
6. SSL/TLS Stripping
7. Session Hijacking

iOS Exploits Demonstrated:
1. Kernel Exploit Chain (CVE-2023-32434)
2. WebKit Exploit (CVE-2023-41990)
3. Zero-Click Exploit via iMessage
4. Sandbox Escape
5. Privilege Escalation

Persistence Methods:
1. LaunchDaemon Installation
2. LoginHook Configuration
3. Kernel Module Loading
4. Firmware Modification

Monitoring Capabilities:
1. Screen Recording
2. Keylogging
3. Location Tracking
4. Call Monitoring
5. Message Interception
6. App Usage Tracking
7. Network Traffic Analysis
8. File System Monitoring
9. Camera Access
10. Microphone Access

Security Implications:
- Complete device compromise without user interaction
- Persistent access across reboots and updates
- Comprehensive surveillance capabilities
- Bypass of all iOS security measures
- Access to sensitive personal data
- Ability to monitor children's devices
- Potential for identity theft
- Complete privacy violation

Recommended Countermeasures:
1. Use VPN on all untrusted networks
2. Keep devices updated to latest iOS version
3. Enable two-factor authentication
4. Use firewall and network monitoring
5. Regular security audits
6. Educate family members about risks
7. Monitor device behavior for anomalies
8. Use enterprise security solutions

Conclusion:
This demonstration shows the critical importance of securing home WiFi networks
and the severe risks associated with admin access in untrusted environments.
The ability to compromise iOS devices without user interaction highlights the
need for comprehensive security measures and user education.
"""
        
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report)
        
    def save_report(self):
        """Save report to file"""
        report_content = self.report_text.get(1.0, tk.END)
        filename = f"wifi_demo_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write(report_content)
            messagebox.showinfo("Success", f"Report saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")
            
    def log_status(self, message):
        """Log status message"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()

def main():
    """Main function"""
    root = tk.Tk()
    app = WiFiDemoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()