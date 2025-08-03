#!/usr/bin/env python3
"""
WiFi Security Research Toolkit (Home Networks Edition)
=====================================================
Author: SecurityResearch AI
Version: 0.1.0

This toolkit is designed for SECURITY RESEARCHERS who want to explore Wi-Fi
security weaknesses in **controlled home-lab environments** – especially with
regard to iOS clients.

⚠️  IMPORTANT LEGAL NOTICE  ⚠️
------------------------------------------------------------
• You **MUST** own the network or have an explicit *written* authorisation by
  the owner to run *any* active tests.
• The *attack* modules included here are provided **FOR EDUCATIONAL USE ONLY**.
  They purposefully include built-in guard rails that try to detect if you are
  outside an RFC-1918 private range and will refuse to run if so.
• The authors take **NO responsibility** for any misuse.  You are the only
  person liable for the commands you execute.

Core modules delivered in this first version
-------------------------------------------
1.  Network discovery  ("discover" sub-command)
2.  Basic router / client security analysis  ("analyze" sub-command – very
    lightweight placeholder for now)
3.  Attack *simulation* entry-points ("simulate" sub-command)
    – Deauthentication, Evil-Twin, Karma – **place-holders** that explain what
      would happen and how to proceed manually with Scapy / hostapd.
4.  Report generation  ("report" sub-command) – JSON today, PDF upcoming.

Road-map items like the optional Tkinter GUI will land in later commits.
"""
import argparse
import ipaddress
import json
import os
import random
import subprocess
import sys
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# External libraries – imported lazily where possible so the toolkit can still
# print a helpful error instead of crashing if dependencies are missing.

PRIVATE_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
]

###############################################################################
# Utility helpers                                                             #
###############################################################################

def _is_private(ip: str) -> bool:
    """True iff *ip* is inside one of the RFC-1918 private ranges."""
    try:
        addr = ipaddress.ip_address(ip)
        return any(addr in rng for rng in PRIVATE_RANGES)
    except ValueError:
        return False


def _current_ssid() -> str:
    """Return the current Wi-Fi SSID if available (Linux & macOS only)."""
    try:
        if sys.platform.startswith("linux"):
            # nmcli: quick and available on most modern Linux desktops
            ssid = (
                subprocess.check_output(["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"], stderr=subprocess.DEVNULL)
                .decode()
                .split("\n")
            )
            for line in ssid:
                if line.startswith("yes:"):
                    return line.split(":", 1)[1]
        elif sys.platform == "darwin":
            out = (
                subprocess.check_output([
                    "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport",
                    "-I",
                ])
                .decode()
                .split("\n")
            )
            for line in out:
                if " SSID:" in line:
                    return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return "unknown"


def _require_root():
    if os.geteuid() != 0:
        sys.exit("[!] This action requires root privileges – please run with sudo.")


###############################################################################
# Discovery                                                                   #
###############################################################################

def discover_network(interface: str, timeout: int = 5) -> List[Dict]:
    """Active ARP-scan on *interface* returning a list of dicts with
    {ip, mac, vendor}.

    Scapy is used if available, otherwise we fall back to the *arping*
    binary which is slower but good enough.
    """
    _require_root()
    results: List[Dict] = []

    try:
        from scapy.all import ARP, Ether, conf, srp  # type: ignore

        conf.verb = 0
        net = _cidr_for_iface(interface)
        if not net:
            raise RuntimeError("Could not detect network range for interface")

        print(f"[*] Scanning {net} on {interface} …")
        pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=str(net))
        answered = srp(pkt, timeout=timeout)[0]
        for snd, rcv in answered:
            mac = rcv[Ether].src
            ip = rcv[ARP].psrc
            results.append({"ip": ip, "mac": mac, "vendor": _oui_lookup(mac)})
    except ImportError:
        print("[!] scapy not installed – falling back to arping")
        results = _arping_fallback(interface, timeout)

    return results


def _cidr_for_iface(iface: str) -> str:
    """Return *network/mask* for interface (Linux only)."""
    try:
        import netifaces  # type: ignore

        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET not in addrs:
            return ""
        info = addrs[netifaces.AF_INET][0]
        ip = info["addr"]
        mask = info["netmask"]
        network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
        return str(network)
    except Exception:
        return ""


def _arping_fallback(iface: str, timeout: int) -> List[Dict]:
    res = []
    proc = subprocess.run([
        "arping",
        "-c",
        "256",
        "-I",
        iface,
        "255.255.255.255",
    ], capture_output=True, text=True, timeout=timeout + 5)
    for line in proc.stdout.split("\n"):
        if "bytes from" in line and "Unicast" in line:
            # Example: 60 bytes from 192.168.1.10 (aa:bb:cc:dd:ee:ff): index=0 time=1.874 msec
            try:
                parts = line.split()
                ip = parts[3]
                mac = parts[4].strip("()")
                res.append({"ip": ip, "mac": mac, "vendor": _oui_lookup(mac)})
            except Exception:
                continue
    return res


def _oui_lookup(mac: str) -> str:
    prefix = mac.upper().replace(":", "")[:6]
    oui_file = Path(__file__).with_suffix(".oui")  # cached vendor db
    vendor = "?"
    try:
        if oui_file.exists():
            with oui_file.open() as f:
                for l in f:
                    if l.startswith(prefix):
                        vendor = l[7:].strip()
                        break
    except Exception:
        pass
    return vendor

###############################################################################
# Basic security analysis                                                     #
###############################################################################

def analyze_targets(targets: List[Dict]) -> List[Dict]:
    """Very basic port / service check using nmap ‑O for OS detection."""
    findings = []

    try:
        import nmap  # type: ignore
    except ImportError:
        sys.exit("[!] python-nmap library not installed – run: pip install python-nmap")

    nm = nmap.PortScanner()
    for t in targets:
        ip = t["ip"]
        print(f"[*] nmap scanning {ip} …")
        try:
            nm.scan(ip, arguments="-T4 -F -O")  # fast top-100 ports + OS finger
            osmatch = nm[ip]["osmatch"][0]["name"] if nm[ip].has_tcp(22) or nm[ip]["osmatch"] else "unknown"
            open_ports = list(nm[ip]["tcp"].keys()) if "tcp" in nm[ip] else []
            t["os"] = osmatch
            t["open_ports"] = open_ports

            # naive insecurity heuristics
            issues: List[str] = []
            if 23 in open_ports:
                issues.append("Telnet open (unencrypted)")
            if 80 in open_ports and 443 not in open_ports:
                issues.append("HTTP open but HTTPS missing")
            if ip.endswith(".1") and 80 in open_ports:
                issues.append("Likely router with HTTP admin interface")

            t["issues"] = issues
            findings.append(t)
        except Exception as e:
            print(f"[!] nmap failed for {ip}: {e}")
    return findings

###############################################################################
# Attack simulations                                                          #
###############################################################################

def simulate_attack(kind: str, interface: str):
    """Entry-point that calls the corresponding simulation stub."""
    _require_root()

    if kind == "deauth":
        _simulate_deauth(interface)
    elif kind == "evil_twin":
        _simulate_evil_twin(interface)
    elif kind == "karma":
        _simulate_karma(interface)
    elif kind == "awdl_zero_click":
        _simulate_awdl_zero_click(interface)
    else:
        sys.exit("[!] Unknown attack kind – choose from: deauth | evil_twin | karma")


def _ensure_test_environment():
    ssid = _current_ssid()
    gw_ip = _default_gateway()
    if gw_ip and not _is_private(gw_ip):
        sys.exit("[!] Non-private gateway detected – refusing to run outside test network!")
    print(f"[✓] Test environment check: SSID '{ssid}', Gateway {gw_ip}")


def _default_gateway() -> str:
    try:
        import netifaces  # type: ignore

        gws = netifaces.gateways()
        if "default" in gws and netifaces.AF_INET in gws["default"]:
            return gws["default"][netifaces.AF_INET][0]
    except Exception:
        pass
    return ""


def _simulate_deauth(iface: str):
    _ensure_test_environment()
    print(textwrap.dedent(
        f"""
        ------------------------------------------------------------
        DEAUTHENTICATION ATTACK (Simulation)
        ------------------------------------------------------------
        This module would craft 802.11 deauthentication frames and send them
        over interface '{iface}'.  For safety reasons **no frames are sent** in
        simulation mode.

        To run an actual test in your isolated lab you can use:
            from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp
            pkt = RadioTap()/Dot11(addr1=target_mac, addr2=ap_mac, addr3=ap_mac)/Dot11Deauth()
            sendp(pkt, iface="{iface}", count=100, inter=0.1)

        Make sure the interface is in monitor mode (airmon-ng start {iface}).
        """
    ))


def _simulate_evil_twin(iface: str):
    _ensure_test_environment()
    channel = random.choice(range(1, 12))
    print(textwrap.dedent(
        f"""
        ------------------------------------------------------------
        EVIL-TWIN ACCESS-POINT (Simulation)
        ------------------------------------------------------------
        A fake AP would be spawned with *hostapd* on channel {channel} while a
        captive-portal phishing page is served by *dnsmasq* and *lighttpd*.

        Quick reference commands (manual):
          hostapd-wpe config/hostapd.conf
          dnsmasq  --no-dhcp-interface={iface} --dhcp-range=...

        Use Wireshark to verify probe requests from iOS devices.
        """
    ))


def _simulate_karma(iface: str):
    _ensure_test_environment()
    print(textwrap.dedent(
        f"""
        ------------------------------------------------------------
        KARMA ATTACK (Simulation)
        ------------------------------------------------------------
        KARMA listens for probe requests and responds with matching beacons,
        tricking devices into associating. Tools like *MDK4* or *airbase-ng*
        can be used.  In simulation mode we only print this guidance.
        """
    ))


def _simulate_awdl_zero_click(iface: str):
    """Simulated *defensive* monitoring for an iOS/macOS AWDL zero-click RCE.

    Apple Wireless Direct Link (AWDL) is a proprietary IEEE-802.11-based ad-hoc
    protocol used by AirDrop, AirPlay, Sidecar and more. In 2020, Google’s
    Project Zero disclosed a critical heap-overflow (see CVE-2020-3843) that
    allowed *remote* code-execution on iOS *without any user interaction* as
    soon as Wi-Fi was enabled – **a so-called zero-click exploit**.

    This simulation does NOT exploit anything. Instead, it demonstrates how a
    blue-team defender could *passively* monitor raw 802.11 action-frames on
    the AWDL social channel (usually channel 44 / 5 GHz) and flag anomalies
    such as unusually large payloads (> 600 bytes) that could indicate an
    attempted heap-overflow.
    """

    _ensure_test_environment()

    print(textwrap.dedent(
        f"""
        ------------------------------------------------------------
        AWDL ZERO-CLICK MONITOR (Simulation)
        ------------------------------------------------------------
        The interface '{iface}' will be put into *monitor* mode (if not yet)
        and scapy sniffing started for IEEE-802.11 action frames that match
        the AWDL OUI (Apple, 00:17:F2) on the 5 GHz social channel. Suspicious
        frames – e.g. payload length >600 bytes – are logged to STDOUT so you
        can observe potential exploitation attempts in a *controlled* lab.

        Stop the capture with CTRL-C.  No packets will be *transmitted* by
        this module – it is purely passive.
        """
    ))

    try:
        from scapy.all import sniff, Dot11, RadioTap  # type: ignore
    except ImportError:
        print("[!] scapy not installed – passive monitoring unavailable")
        return

    def _awdl_filter(pkt):
        if not pkt.haslayer(Dot11):
            return False
        dot11 = pkt[Dot11]
        # Action frames (type=0, subtype=13) are used by AWDL for service discovery
        if dot11.type == 0 and dot11.subtype == 13:
            # OUI can be found in payload starting at fixed offset within the
            # action frame. A quick & dirty heuristic:
            raw = bytes(pkt[RadioTap].payload)
            return b"\x00\x17\xF2" in raw  # Apple OUI
        return False

    def _process(pkt):
        ts = datetime.utcnow().isoformat() + "Z"
        length = len(pkt)
        if length > 600:
            print(f"[!] {ts} Suspect large AWDL action frame: {length} bytes from {pkt.addr2}")
        else:
            print(f"[+] {ts} AWDL action frame {length}B from {pkt.addr2}")

    print("[*] Sniffing – press CTRL-C to stop …")
    try:
        sniff(iface=iface, prn=_process, lfilter=_awdl_filter, store=False)
    except KeyboardInterrupt:
        print("\n[✓] Capture stopped by user")

###############################################################################
# Report generation                                                           #
###############################################################################

def save_json_report(findings: List[Dict], out_file: str):
    data = {
        "generated": datetime.utcnow().isoformat() + "Z",
        "findings": findings,
    }
    with open(out_file, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[+] JSON report written to {out_file}")

###############################################################################
# CLI                                                                        #
###############################################################################

def build_cli() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="wifi-toolkit",
        description="Wi-Fi Security Research Toolkit – *educational use only*",
    )
    sub = p.add_subparsers(dest="command", required=True)

    # discover
    d = sub.add_parser("discover", help="Discover devices in the local network")
    d.add_argument("-i", "--interface", required=True, help="Network interface to scan (must be in the same LAN)")
    d.add_argument("-t", "--timeout", type=int, default=5, help="ARP timeout in seconds")

    # analyze
    a = sub.add_parser("analyze", help="Run basic security analysis on targets")
    a.add_argument("targets", help="JSON file produced by discover, or comma-separated list of IPs")

    # simulate
    s = sub.add_parser("simulate", help="Run attack simulation stub")
    s.add_argument(
        "kind",
        choices=[
            "deauth",
            "evil_twin",
            "karma",
            "awdl_zero_click",
        ],
        help="Attack kind (including iOS AWDL zero-click monitor)",
    )
    s.add_argument("-i", "--interface", required=True, help="Wireless interface in monitor mode")

    # report
    r = sub.add_parser("report", help="Generate JSON report from findings")
    r.add_argument("findings", help="JSON produced by analyze")
    r.add_argument("-o", "--out", default="report.json", help="Output file")

    return p


def main(argv: List[str] | None = None):
    args = build_cli().parse_args(argv)

    if args.command == "discover":
        devices = discover_network(args.interface, args.timeout)
        out = "discover_" + datetime.utcnow().strftime("%Y%m%dT%H%M%SZ") + ".json"
        save_json_report(devices, out)

    elif args.command == "analyze":
        if os.path.exists(args.targets):
            with open(args.targets) as f:
                targets = json.load(f)
        else:
            targets = [{"ip": ip.strip()} for ip in args.targets.split(",")]
        findings = analyze_targets(targets)
        out = "findings_" + datetime.utcnow().strftime("%Y%m%dT%H%M%SZ") + ".json"
        save_json_report(findings, out)

    elif args.command == "simulate":
        simulate_attack(args.kind, args.interface)

    elif args.command == "report":
        with open(args.findings) as f:
            data = json.load(f)
        # For now we just pretty-print
        print(json.dumps(data, indent=2))
        save_json_report(data["findings"], args.out)


if __name__ == "__main__":
    main()