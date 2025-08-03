#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WiFi Security Toolkit - GUI Module
Version 1.0 - Educational and Research Purposes Only

Graphical user interface for the WiFi security research toolkit.
Provides visual network mapping, real-time monitoring, and interactive analysis.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import json
from datetime import datetime
import os

# Try to import matplotlib for network visualization
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import matplotlib.patches as patches
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

class WiFiSecurityGUI:
    """Main GUI application for WiFi security toolkit."""
    
    def __init__(self, network_discovery, security_analyzer, attack_simulator, 
                 report_generator, safety_validator):
        self.network_discovery = network_discovery
        self.security_analyzer = security_analyzer
        self.attack_simulator = attack_simulator
        self.report_generator = report_generator
        self.safety_validator = safety_validator
        
        # GUI state
        self.scanning = False
        self.devices = {}
        self.access_points = {}
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("WiFi Security Research Toolkit")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2b2b2b')
        
        # Configure style
        self.setup_styles()
        
        # Create GUI components
        self.create_widgets()
        
        # Status
        self.update_status("Ready - WiFi Security Toolkit Loaded")
    
    def setup_styles(self):
        """Configure ttk styles for dark theme."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', 
                       foreground='#00ff41', 
                       background='#2b2b2b',
                       font=('Courier', 16, 'bold'))
        
        style.configure('Header.TLabel',
                       foreground='#ffffff',
                       background='#2b2b2b',
                       font=('Courier', 12, 'bold'))
        
        style.configure('Info.TLabel',
                       foreground='#cccccc',
                       background='#2b2b2b',
                       font=('Courier', 10))
        
        style.configure('Custom.TButton',
                       foreground='#ffffff',
                       background='#404040',
                       font=('Courier', 10))
        
        style.configure('Danger.TButton',
                       foreground='#ffffff',
                       background='#cc0000',
                       font=('Courier', 10, 'bold'))
    
    def create_widgets(self):
        """Create and arrange GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="WiFi Security Research Toolkit",
                               style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_discovery_tab()
        self.create_analysis_tab()
        self.create_attack_tab()
        self.create_visualization_tab()
        self.create_reports_tab()
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_discovery_tab(self):
        """Create network discovery tab."""
        discovery_frame = ttk.Frame(self.notebook)
        self.notebook.add(discovery_frame, text="Network Discovery")
        
        # Control panel
        control_frame = ttk.LabelFrame(discovery_frame, text="Discovery Controls")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Network range input
        ttk.Label(control_frame, text="Target Range:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.range_var = tk.StringVar(value="192.168.1.0/24")
        range_entry = ttk.Entry(control_frame, textvariable=self.range_var, width=20)
        range_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # WiFi scan duration
        ttk.Label(control_frame, text="WiFi Scan Duration:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.duration_var = tk.IntVar(value=30)
        duration_spin = ttk.Spinbox(control_frame, from_=10, to=300, textvariable=self.duration_var, width=10)
        duration_spin.grid(row=0, column=3, padx=5, pady=5)
        
        # Buttons
        ttk.Button(control_frame, text="Discover Devices", 
                  command=self.start_device_discovery).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(control_frame, text="Scan WiFi", 
                  command=self.start_wifi_scan).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(control_frame, text="Full Scan", 
                  command=self.start_full_scan).grid(row=1, column=2, padx=5, pady=5)
        ttk.Button(control_frame, text="Stop Scan", 
                  command=self.stop_scan).grid(row=1, column=3, padx=5, pady=5)
        
        # Results area
        results_frame = ttk.LabelFrame(discovery_frame, text="Discovery Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create treeview for devices
        self.device_tree = ttk.Treeview(results_frame, columns=('IP', 'MAC', 'Vendor', 'OS', 'Vulnerabilities'), show='tree headings')
        self.device_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Configure columns
        self.device_tree.heading('#0', text='Type')
        self.device_tree.heading('IP', text='IP Address')
        self.device_tree.heading('MAC', text='MAC Address')
        self.device_tree.heading('Vendor', text='Vendor')
        self.device_tree.heading('OS', text='OS Info')
        self.device_tree.heading('Vulnerabilities', text='Vulnerabilities')
        
        # Scrollbar for treeview
        tree_scroll = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.device_tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.device_tree.configure(yscrollcommand=tree_scroll.set)
    
    def create_analysis_tab(self):
        """Create security analysis tab."""
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="Security Analysis")
        
        # Analysis controls
        control_frame = ttk.LabelFrame(analysis_frame, text="Analysis Controls")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Analyze All Devices", 
                  command=self.analyze_all_devices).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(control_frame, text="Analyze Selected", 
                  command=self.analyze_selected).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(control_frame, text="Export Analysis", 
                  command=self.export_analysis).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Analysis results
        results_frame = ttk.LabelFrame(analysis_frame, text="Vulnerability Analysis")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create text widget for analysis results
        self.analysis_text = scrolledtext.ScrolledText(results_frame, 
                                                      wrap=tk.WORD, 
                                                      font=('Courier', 10),
                                                      bg='#1e1e1e',
                                                      fg='#ffffff',
                                                      insertbackground='#ffffff')
        self.analysis_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_attack_tab(self):
        """Create attack simulation tab."""
        attack_frame = ttk.Frame(self.notebook)
        self.notebook.add(attack_frame, text="Attack Simulation")
        
        # Warning label
        warning_label = ttk.Label(attack_frame, 
                                 text="⚠️ EDUCATIONAL USE ONLY - AUTHORIZED ENVIRONMENTS ONLY ⚠️",
                                 style='Header.TLabel')
        warning_label.pack(pady=10)
        
        # Environment status
        self.env_status_label = ttk.Label(attack_frame, text="Environment Status: Checking...", style='Info.TLabel')
        self.env_status_label.pack(pady=5)
        
        # Attack controls
        control_frame = ttk.LabelFrame(attack_frame, text="Attack Simulation Controls")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Deauth attack
        deauth_frame = ttk.LabelFrame(control_frame, text="Deauthentication Attack")
        deauth_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(deauth_frame, text="Target BSSID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.deauth_bssid_var = tk.StringVar()
        ttk.Entry(deauth_frame, textvariable=self.deauth_bssid_var, width=20).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(deauth_frame, text="Client MAC (optional):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.deauth_client_var = tk.StringVar()
        ttk.Entry(deauth_frame, textvariable=self.deauth_client_var, width=20).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Button(deauth_frame, text="Simulate Deauth", 
                  command=self.simulate_deauth, style='Danger.TButton').grid(row=2, column=0, columnspan=2, pady=5)
        
        # Evil Twin attack
        eviltwin_frame = ttk.LabelFrame(control_frame, text="Evil Twin Attack")
        eviltwin_frame.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(eviltwin_frame, text="Target SSID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.eviltwin_ssid_var = tk.StringVar()
        ttk.Entry(eviltwin_frame, textvariable=self.eviltwin_ssid_var, width=20).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Button(eviltwin_frame, text="Simulate Evil Twin", 
                  command=self.simulate_eviltwin, style='Danger.TButton').grid(row=1, column=0, columnspan=2, pady=5)
        
        # Karma attack
        karma_frame = ttk.LabelFrame(control_frame, text="Karma Attack")
        karma_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Button(karma_frame, text="Simulate Karma Attack", 
                  command=self.simulate_karma, style='Danger.TButton').pack(pady=5)
        
        # Attack log
        log_frame = ttk.LabelFrame(attack_frame, text="Attack Simulation Log")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.attack_log = scrolledtext.ScrolledText(log_frame, 
                                                   wrap=tk.WORD, 
                                                   font=('Courier', 10),
                                                   bg='#1e1e1e',
                                                   fg='#00ff41',
                                                   insertbackground='#ffffff')
        self.attack_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Check environment status
        self.check_environment_status()
    
    def create_visualization_tab(self):
        """Create network visualization tab."""
        viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(viz_frame, text="Network Visualization")
        
        if not MATPLOTLIB_AVAILABLE:
            ttk.Label(viz_frame, 
                     text="Matplotlib not available - install matplotlib for network visualization",
                     style='Header.TLabel').pack(expand=True)
            return
        
        # Visualization controls
        control_frame = ttk.LabelFrame(viz_frame, text="Visualization Controls")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Update Network Map", 
                  command=self.update_network_map).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(control_frame, text="Show Vulnerability Heatmap", 
                  command=self.show_vulnerability_heatmap).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(control_frame, text="Export Visualization", 
                  command=self.export_visualization).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(12, 8), dpi=100, facecolor='#2b2b2b')
        self.ax = self.fig.add_subplot(111, facecolor='#1e1e1e')
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initialize empty plot
        self.ax.set_title("Network Topology", color='white', fontsize=14)
        self.ax.set_facecolor('#1e1e1e')
        self.fig.patch.set_facecolor('#2b2b2b')
        self.canvas.draw()
    
    def create_reports_tab(self):
        """Create reports generation tab."""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="Reports")
        
        # Report controls
        control_frame = ttk.LabelFrame(reports_frame, text="Report Generation")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Generate JSON Report", 
                  command=self.generate_json_report).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(control_frame, text="Generate PDF Report", 
                  command=self.generate_pdf_report).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(control_frame, text="Export Raw Data", 
                  command=self.export_raw_data).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Report preview
        preview_frame = ttk.LabelFrame(reports_frame, text="Report Preview")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.report_preview = scrolledtext.ScrolledText(preview_frame, 
                                                       wrap=tk.WORD, 
                                                       font=('Courier', 10),
                                                       bg='#1e1e1e',
                                                       fg='#ffffff',
                                                       insertbackground='#ffffff')
        self.report_preview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_status_bar(self, parent):
        """Create status bar."""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(5, 0))
        
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, style='Info.TLabel')
        self.status_label.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(side=tk.RIGHT, padx=(10, 0))
    
    def update_status(self, message):
        """Update status bar message."""
        self.status_var.set(f"Status: {message}")
        self.root.update_idletasks()
    
    def start_progress(self):
        """Start progress bar animation."""
        self.progress.start(10)
    
    def stop_progress(self):
        """Stop progress bar animation."""
        self.progress.stop()
    
    def check_environment_status(self):
        """Check and update environment authorization status."""
        def check():
            authorized = self.safety_validator.validate_environment()
            if authorized:
                self.env_status_label.config(text="Environment Status: ✅ AUTHORIZED TEST ENVIRONMENT")
            else:
                self.env_status_label.config(text="Environment Status: ❌ NOT AUTHORIZED - ATTACKS DISABLED")
        
        threading.Thread(target=check, daemon=True).start()
    
    def start_device_discovery(self):
        """Start device discovery in background thread."""
        if self.scanning:
            messagebox.showwarning("Scan in Progress", "A scan is already running. Please wait for it to complete.")
            return
        
        def discover():
            self.scanning = True
            self.start_progress()
            self.update_status("Discovering network devices...")
            
            try:
                target_range = self.range_var.get()
                self.devices = self.network_discovery.discover_devices(target_range)
                
                # Identify iOS devices
                ios_devices = self.network_discovery.identify_ios_devices()
                
                # Update GUI on main thread
                self.root.after(0, self.update_device_tree)
                self.root.after(0, self.update_status, f"Discovered {len(self.devices)} devices ({len(ios_devices)} iOS)")
                
            except Exception as e:
                self.root.after(0, self.update_status, f"Discovery error: {e}")
                messagebox.showerror("Discovery Error", f"Failed to discover devices: {e}")
            finally:
                self.scanning = False
                self.stop_progress()
        
        threading.Thread(target=discover, daemon=True).start()
    
    def start_wifi_scan(self):
        """Start WiFi scanning in background thread."""
        if self.scanning:
            messagebox.showwarning("Scan in Progress", "A scan is already running. Please wait for it to complete.")
            return
        
        def scan():
            self.scanning = True
            self.start_progress()
            duration = self.duration_var.get()
            self.update_status(f"Scanning WiFi networks for {duration} seconds...")
            
            try:
                self.access_points = self.network_discovery.scan_wifi_networks(duration)
                
                # Update GUI on main thread
                self.root.after(0, self.update_device_tree)
                self.root.after(0, self.update_status, f"Found {len(self.access_points)} access points")
                
            except Exception as e:
                self.root.after(0, self.update_status, f"WiFi scan error: {e}")
                messagebox.showerror("Scan Error", f"Failed to scan WiFi: {e}")
            finally:
                self.scanning = False
                self.stop_progress()
        
        threading.Thread(target=scan, daemon=True).start()
    
    def start_full_scan(self):
        """Start full network and WiFi scan."""
        if self.scanning:
            messagebox.showwarning("Scan in Progress", "A scan is already running. Please wait for it to complete.")
            return
        
        def full_scan():
            self.scanning = True
            self.start_progress()
            self.update_status("Starting full network scan...")
            
            try:
                # Device discovery
                target_range = self.range_var.get()
                self.devices = self.network_discovery.discover_devices(target_range)
                self.root.after(0, self.update_status, f"Discovered {len(self.devices)} devices, starting WiFi scan...")
                
                # WiFi scan
                duration = self.duration_var.get()
                self.access_points = self.network_discovery.scan_wifi_networks(duration)
                
                # Update GUI
                self.root.after(0, self.update_device_tree)
                self.root.after(0, self.update_status, 
                               f"Full scan complete: {len(self.devices)} devices, {len(self.access_points)} APs")
                
            except Exception as e:
                self.root.after(0, self.update_status, f"Full scan error: {e}")
                messagebox.showerror("Scan Error", f"Full scan failed: {e}")
            finally:
                self.scanning = False
                self.stop_progress()
        
        threading.Thread(target=full_scan, daemon=True).start()
    
    def stop_scan(self):
        """Stop current scanning operation."""
        if self.scanning:
            self.network_discovery.scanning = False
            self.scanning = False
            self.stop_progress()
            self.update_status("Scan stopped by user")
    
    def update_device_tree(self):
        """Update the device tree view with discovered devices and APs."""
        # Clear existing items
        for item in self.device_tree.get_children():
            self.device_tree.delete(item)
        
        # Add devices
        if self.devices:
            devices_node = self.device_tree.insert('', 'end', text='Network Devices', values=('', '', '', '', ''))
            for mac, device in self.devices.items():
                vuln_count = len(device.vulnerabilities)
                self.device_tree.insert(devices_node, 'end', text='Device',
                                       values=(device.ip or 'Unknown', mac, device.vendor, 
                                              device.os_info or 'Unknown', str(vuln_count)))
        
        # Add access points
        if self.access_points:
            aps_node = self.device_tree.insert('', 'end', text='WiFi Access Points', values=('', '', '', '', ''))
            for bssid, ap in self.access_points.items():
                vuln_count = len(ap.vulnerabilities)
                self.device_tree.insert(aps_node, 'end', text='Access Point',
                                       values=(ap.ssid, bssid, f'Ch {ap.channel}', 
                                              ap.encryption, str(vuln_count)))
        
        # Expand all nodes
        for item in self.device_tree.get_children():
            self.device_tree.item(item, open=True)
    
    def analyze_all_devices(self):
        """Analyze security of all discovered devices."""
        if not self.devices and not self.access_points:
            messagebox.showwarning("No Data", "No devices or access points to analyze. Please run a scan first.")
            return
        
        def analyze():
            self.start_progress()
            self.update_status("Analyzing device security...")
            
            try:
                analysis_results = []
                
                # Analyze devices
                for device in self.devices.values():
                    self.security_analyzer.analyze_device_security(device)
                    if device.vulnerabilities:
                        analysis_results.append(f"Device {device.ip} ({device.mac}):")
                        for vuln in device.vulnerabilities:
                            analysis_results.append(f"  - {vuln['type']}: {vuln['description']} ({vuln['severity']})")
                        analysis_results.append("")
                
                # Analyze access points (already done during discovery)
                for ap in self.access_points.values():
                    if ap.vulnerabilities:
                        analysis_results.append(f"Access Point {ap.ssid} ({ap.bssid}):")
                        for vuln in ap.vulnerabilities:
                            analysis_results.append(f"  - {vuln['type']}: {vuln['description']} ({vuln['severity']})")
                        analysis_results.append("")
                
                # Update analysis display
                analysis_text = "\n".join(analysis_results) if analysis_results else "No vulnerabilities found."
                self.root.after(0, self.display_analysis_results, analysis_text)
                self.root.after(0, self.update_device_tree)  # Refresh vulnerability counts
                self.root.after(0, self.update_status, "Security analysis completed")
                
            except Exception as e:
                self.root.after(0, self.update_status, f"Analysis error: {e}")
                messagebox.showerror("Analysis Error", f"Security analysis failed: {e}")
            finally:
                self.stop_progress()
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def display_analysis_results(self, results):
        """Display analysis results in the text widget."""
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(1.0, results)
    
    def analyze_selected(self):
        """Analyze security of selected device/AP."""
        selection = self.device_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device or access point to analyze.")
            return
        
        # Get selected item details
        item = self.device_tree.item(selection[0])
        values = item['values']
        
        if not values or not values[1]:  # No MAC/BSSID
            messagebox.showwarning("Invalid Selection", "Please select a specific device or access point.")
            return
        
        # Find and analyze the selected item
        mac_or_bssid = values[1]
        
        if mac_or_bssid in self.devices:
            device = self.devices[mac_or_bssid]
            self.security_analyzer.analyze_device_security(device)
            results = f"Analysis for Device {device.ip} ({device.mac}):\n\n"
            if device.vulnerabilities:
                for vuln in device.vulnerabilities:
                    results += f"- {vuln['type']}: {vuln['description']} ({vuln['severity']})\n"
            else:
                results += "No vulnerabilities found."
        
        elif mac_or_bssid in self.access_points:
            ap = self.access_points[mac_or_bssid]
            results = f"Analysis for Access Point {ap.ssid} ({ap.bssid}):\n\n"
            if ap.vulnerabilities:
                for vuln in ap.vulnerabilities:
                    results += f"- {vuln['type']}: {vuln['description']} ({vuln['severity']})\n"
            else:
                results += "No vulnerabilities found."
        
        else:
            messagebox.showerror("Error", "Selected item not found in scan results.")
            return
        
        self.display_analysis_results(results)
        self.update_device_tree()  # Refresh vulnerability counts
    
    def simulate_deauth(self):
        """Simulate deauthentication attack."""
        if not self.safety_validator.authorized:
            messagebox.showerror("Not Authorized", 
                               "Attack simulations require authorized test environment!")
            return
        
        target_bssid = self.deauth_bssid_var.get().strip()
        if not target_bssid:
            messagebox.showwarning("Missing Target", "Please enter a target BSSID.")
            return
        
        client_mac = self.deauth_client_var.get().strip() or None
        
        def attack():
            try:
                result = self.attack_simulator.simulate_deauth_attack(target_bssid, client_mac)
                log_message = f"[{datetime.now().strftime('%H:%M:%S')}] Deauth simulation: {result}\n"
                self.root.after(0, self.append_attack_log, log_message)
            except Exception as e:
                error_message = f"[{datetime.now().strftime('%H:%M:%S')}] Deauth error: {e}\n"
                self.root.after(0, self.append_attack_log, error_message)
        
        threading.Thread(target=attack, daemon=True).start()
    
    def simulate_eviltwin(self):
        """Simulate evil twin attack."""
        if not self.safety_validator.authorized:
            messagebox.showerror("Not Authorized", 
                               "Attack simulations require authorized test environment!")
            return
        
        target_ssid = self.eviltwin_ssid_var.get().strip()
        if not target_ssid:
            messagebox.showwarning("Missing Target", "Please enter a target SSID.")
            return
        
        def attack():
            try:
                result = self.attack_simulator.simulate_evil_twin(target_ssid)
                log_message = f"[{datetime.now().strftime('%H:%M:%S')}] Evil Twin simulation: {result}\n"
                self.root.after(0, self.append_attack_log, log_message)
            except Exception as e:
                error_message = f"[{datetime.now().strftime('%H:%M:%S')}] Evil Twin error: {e}\n"
                self.root.after(0, self.append_attack_log, error_message)
        
        threading.Thread(target=attack, daemon=True).start()
    
    def simulate_karma(self):
        """Simulate karma attack."""
        if not self.safety_validator.authorized:
            messagebox.showerror("Not Authorized", 
                               "Attack simulations require authorized test environment!")
            return
        
        def attack():
            try:
                probe_requests = ['TestNetwork', 'HomeWiFi', 'CoffeeShop', 'FreeWiFi']
                result = self.attack_simulator.simulate_karma_attack(probe_requests)
                log_message = f"[{datetime.now().strftime('%H:%M:%S')}] Karma simulation: {result}\n"
                self.root.after(0, self.append_attack_log, log_message)
            except Exception as e:
                error_message = f"[{datetime.now().strftime('%H:%M:%S')}] Karma error: {e}\n"
                self.root.after(0, self.append_attack_log, error_message)
        
        threading.Thread(target=attack, daemon=True).start()
    
    def append_attack_log(self, message):
        """Append message to attack log."""
        self.attack_log.insert(tk.END, message)
        self.attack_log.see(tk.END)
    
    def update_network_map(self):
        """Update network visualization map."""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        self.ax.clear()
        self.ax.set_title("Network Topology", color='white', fontsize=14)
        self.ax.set_facecolor('#1e1e1e')
        
        if not self.devices and not self.access_points:
            self.ax.text(0.5, 0.5, 'No network data available\nRun a scan to populate the map', 
                        ha='center', va='center', transform=self.ax.transAxes, 
                        color='white', fontsize=12)
            self.canvas.draw()
            return
        
        # Create network layout
        positions = {}
        colors = []
        labels = []
        
        # Position devices in a circle
        device_count = len(self.devices)
        ap_count = len(self.access_points)
        total_count = device_count + ap_count
        
        if total_count == 0:
            self.canvas.draw()
            return
        
        # Position access points in center
        ap_positions = []
        if ap_count > 0:
            for i, (bssid, ap) in enumerate(self.access_points.items()):
                angle = 2 * np.pi * i / max(ap_count, 1)
                x = 0.3 * np.cos(angle)
                y = 0.3 * np.sin(angle)
                positions[bssid] = (x, y)
                ap_positions.append((x, y))
                colors.append('red' if ap.vulnerabilities else 'orange')
                labels.append(f"AP: {ap.ssid[:10]}")
        
        # Position devices around the edge
        for i, (mac, device) in enumerate(self.devices.items()):
            angle = 2 * np.pi * i / max(device_count, 1)
            x = 0.8 * np.cos(angle)
            y = 0.8 * np.sin(angle)
            positions[mac] = (x, y)
            
            if device.vulnerabilities:
                colors.append('red')
            elif device.os_info and 'ios' in device.os_info.lower():
                colors.append('blue')
            else:
                colors.append('green')
            
            label = device.hostname[:10] if device.hostname else device.ip
            labels.append(f"Device: {label}")
        
        # Draw nodes
        if positions:
            x_coords = [pos[0] for pos in positions.values()]
            y_coords = [pos[1] for pos in positions.values()]
            
            scatter = self.ax.scatter(x_coords, y_coords, c=colors, s=100, alpha=0.7)
            
            # Add labels
            for i, (key, pos) in enumerate(positions.items()):
                self.ax.annotate(labels[i], pos, xytext=(5, 5), 
                               textcoords='offset points', 
                               fontsize=8, color='white')
        
        # Draw connections from devices to nearest AP
        if ap_positions and positions:
            for mac, device_pos in positions.items():
                if mac not in self.access_points:  # It's a device
                    # Find nearest AP
                    if ap_positions:
                        nearest_ap = min(ap_positions, 
                                       key=lambda ap_pos: np.sqrt((device_pos[0] - ap_pos[0])**2 + 
                                                                 (device_pos[1] - ap_pos[1])**2))
                        self.ax.plot([device_pos[0], nearest_ap[0]], 
                                   [device_pos[1], nearest_ap[1]], 
                                   'gray', alpha=0.3, linewidth=0.5)
        
        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=8, label='Secure Device'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=8, label='iOS Device'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=8, label='Secure AP'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Vulnerable')
        ]
        self.ax.legend(handles=legend_elements, loc='upper right', 
                      facecolor='#2b2b2b', edgecolor='white', labelcolor='white')
        
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        
        self.canvas.draw()
    
    def show_vulnerability_heatmap(self):
        """Show vulnerability heatmap."""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        # Create vulnerability data
        vuln_data = {}
        
        for device in self.devices.values():
            vuln_data[f"Device {device.ip}"] = len(device.vulnerabilities)
        
        for ap in self.access_points.values():
            vuln_data[f"AP {ap.ssid}"] = len(ap.vulnerabilities)
        
        if not vuln_data:
            messagebox.showinfo("No Data", "No vulnerability data available.")
            return
        
        # Create heatmap
        self.ax.clear()
        self.ax.set_title("Vulnerability Heatmap", color='white', fontsize=14)
        
        names = list(vuln_data.keys())
        values = list(vuln_data.values())
        
        if values:
            bars = self.ax.bar(range(len(names)), values, 
                              color=['red' if v > 2 else 'orange' if v > 0 else 'green' for v in values])
            
            self.ax.set_xticks(range(len(names)))
            self.ax.set_xticklabels([name[:15] for name in names], rotation=45, ha='right', color='white')
            self.ax.set_ylabel('Vulnerability Count', color='white')
            self.ax.tick_params(colors='white')
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                if value > 0:
                    self.ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                               str(value), ha='center', va='bottom', color='white')
        
        self.ax.set_facecolor('#1e1e1e')
        self.fig.tight_layout()
        self.canvas.draw()
    
    def export_visualization(self):
        """Export current visualization."""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.fig.savefig(filename, facecolor='#2b2b2b', dpi=300, bbox_inches='tight')
                messagebox.showinfo("Export Complete", f"Visualization exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export visualization: {e}")
    
    def generate_json_report(self):
        """Generate JSON report."""
        if not self.devices and not self.access_points:
            messagebox.showwarning("No Data", "No scan data available for report generation.")
            return
        
        try:
            filepath = self.report_generator.generate_json_report(
                self.devices, self.access_points, []
            )
            
            # Show preview
            with open(filepath, 'r') as f:
                content = f.read()
            
            self.report_preview.delete(1.0, tk.END)
            self.report_preview.insert(1.0, content)
            
            messagebox.showinfo("Report Generated", f"JSON report saved to: {filepath}")
            
        except Exception as e:
            messagebox.showerror("Report Error", f"Failed to generate JSON report: {e}")
    
    def generate_pdf_report(self):
        """Generate PDF report."""
        if not self.devices and not self.access_points:
            messagebox.showwarning("No Data", "No scan data available for report generation.")
            return
        
        try:
            filepath = self.report_generator.generate_pdf_report(self.devices, self.access_points)
            
            if filepath:
                messagebox.showinfo("Report Generated", f"PDF report saved to: {filepath}")
            else:
                messagebox.showwarning("PDF Not Available", 
                                     "PDF generation requires reportlab library.")
            
        except Exception as e:
            messagebox.showerror("Report Error", f"Failed to generate PDF report: {e}")
    
    def export_raw_data(self):
        """Export raw scan data."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                raw_data = {
                    "devices": {mac: device.to_dict() for mac, device in self.devices.items()},
                    "access_points": {bssid: ap.to_dict() for bssid, ap in self.access_points.items()},
                    "export_time": datetime.now().isoformat()
                }
                
                with open(filename, 'w') as f:
                    json.dump(raw_data, f, indent=2)
                
                messagebox.showinfo("Export Complete", f"Raw data exported to {filename}")
                
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export raw data: {e}")
    
    def export_analysis(self):
        """Export analysis results."""
        content = self.analysis_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("No Analysis", "No analysis results to export.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(f"WiFi Security Analysis Report\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(content)
                
                messagebox.showinfo("Export Complete", f"Analysis exported to {filename}")
                
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export analysis: {e}")
    
    def run(self):
        """Start the GUI application."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()

if __name__ == "__main__":
    # This would normally be imported and used by the main toolkit
    print("WiFi Security GUI Module - Import this module from the main toolkit")