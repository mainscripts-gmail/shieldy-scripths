"""
SHIELDY SCRIPTS - MALWARE SCANNER v1.0
Usage: python scanner.py path/to/script.lua
"""
import re
import sys
import hashlib

DANGEROUS_PATTERNS = [
    (r"\.ROBLOSECURITY", "ACCOUNT THEFT: Reads Roblox login cookie"),
    (r"getrenv\s*\(", "HIGH RISK: Accesses memory of other running scripts"),
    (r"gethui\s*\(", "HIGH RISK: Hijacks UI elements from other scripts"),
    (r"HttpPost|HttpService:PostAsync", "DATA EXFILTRATION: Sends information to external servers"),
    (r"writefile\s*\(|readfile\s*\(", "FILE ACCESS: Reads/writes files to your system"),
    (r"\\x[0-9a-fA-F]{2}", "OBFUSCATED CODE: Hidden source — almost always malicious"),
    (r"discord\.com/api/webhooks", "DATA EXFILTRATION: Sends data via Discord webhook"),
    (r"getfenv\s*\(|setfenv\s*\(", "ENVIRONMENT MANIPULATION: Can hide malicious behavior"),
]

def scan_script(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    
    print(f"🔍 Scanning: {file_path}")
    print(f"📏 Size: {len(source)} characters")
    print(f"🔑 SHA-256 Hash: {hashlib.sha256(source.encode()).hexdigest()}\n")
    
    issues = []
    for pattern, description in DANGEROUS_PATTERNS:
        if re.search(pattern, source):
            issues.append(f"❌ {description}")
    
    if not issues:
        print("✅ CLEAN — Eligible for approval (still do a manual source review!)")
        return True
    else:
        print("⛔ SECURITY ISSUES DETECTED:")
        for issue in issues: print(issue)
        print("\n❌ SCRIPT REJECTED — Do NOT add to the approved database")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scanner.py script.lua")
        sys.exit(1)
    scan_script(sys.argv[1])
