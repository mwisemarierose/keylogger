#!/usr/bin/env python3
"""
Simple, safe detector for classroom use.

Usage:
  python3 detector.py

Requirements:
  pip install psutil
"""

import psutil
import platform
import os
import sys
from datetime import datetime

SUSPICIOUS_KEYWORDS = [
    "keylog", "keylogger", "key-log", "pynput", "keyboard", "keyspy", "klg", "hook"
]

def stamp():
    return datetime.utcnow().isoformat() + "Z"

def scan_processes():
    findings = []
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'username']):
        try:
            info = proc.info
            cmdline = " ".join(info.get('cmdline') or [])
            name = info.get('name') or ""
            exe = info.get('exe') or ""
            lower_blob = " ".join([name, cmdline, exe]).lower()

            for kw in SUSPICIOUS_KEYWORDS:
                if kw in lower_blob:
                    findings.append({
                        "pid": info['pid'],
                        "name": name,
                        "username": info.get('username'),
                        "reason": f"keyword match: '{kw}' in cmdline/name/exe",
                        "cmdline": cmdline
                    })
                    break

            # Heuristic: Python processes that import pynput/keyboard are suspicious to investigate
            if "python" in name.lower() or "python" in cmdline.lower():
                # If module name appears in cmdline, flag it
                for mod in ("pynput", "keyboard", "pyHook"):
                    if mod in lower_blob:
                        findings.append({
                            "pid": info['pid'],
                            "name": name,
                            "username": info.get('username'),
                            "reason": f"python process referencing module '{mod}'",
                            "cmdline": cmdline
                        })
                        break

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return findings

def linux_input_scan():
    findings = []
    if platform.system() != "Linux":
        return findings
    # list /dev/input/* and who has them open (best-effort)
    try:
        input_devices = [d for d in os.listdir("/dev") if d.startswith("input")]
        # check open files of processes for /dev/input
        for proc in psutil.process_iter(['pid', 'name', 'open_files']):
            try:
                ofs = proc.info.get('open_files') or []
                for f in ofs:
                    if "/dev/input" in f.path:
                        findings.append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "reason": f"opened input device: {f.path}"
                        })
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception:
        pass
    return findings

def report(findings):
    print("="*60)
    print("KEYLOGGER DETECTOR REPORT")
    print("Time (UTC):", stamp())
    print("="*60)
    if not findings:
        print("No suspicious findings from quick heuristics. This is not a guarantee.")
        print("Consider deeper EDR / manual inspection for production/real investigations.")
        return

    for f in findings:
        print(f"- PID: {f.get('pid')}  Name: {f.get('name')}  Reason: {f.get('reason')}")
        if 'cmdline' in f:
            print(f"  cmdline: {f['cmdline']}")
    print("="*60)
    print("Notes:")
    print("- These heuristics catch obvious misconfigurations and test/demo loggers.")
    print("- They will miss stealthy, compiled, or kernel-level loggers.")
    print("- For Windows, combine with Sysinternals (Autoruns, Process Explorer) and EDR logs.")
    print("- For macOS, check Accessibility permissions and TCC logs; for Linux, check /dev/input access.")
    print("="*60)

def main():
    print("Running quick detector heuristics (classroom demo).")
    findings = scan_processes()
    findings += linux_input_scan()
    report(findings)

if __name__ == "__main__":
    main()
