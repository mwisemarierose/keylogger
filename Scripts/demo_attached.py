#!/usr/bin/env python3
"""
Simple notes app that optionally attaches an internal logger (consented).
This demonstrates how a normal application could be extended to log inputs.
Usage:
  python3 demo_attached_logger.py
Requirements:
  pip install pynput
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from datetime import datetime
import json, os

EXPORT_DIR = "demo_exports"

class DemoApp:
    def __init__(self, root):
        self.root = root
        root.title("Demo Notes App (Classroom)")

        self.log_enabled = tk.BooleanVar(value=False)

        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.text = scrolledtext.ScrolledText(frame, width=60, height=20)
        self.text.pack(fill="both", expand=True)

        bottom = tk.Frame(root)
        bottom.pack(fill="x", padx=10, pady=5)

        self.enable_cb = tk.Checkbutton(bottom, text="Enable internal logging (consent)", var=self.log_enabled)
        self.enable_cb.pack(side="left")

        save_btn = tk.Button(bottom, text="Save Note", command=self.save_note)
        save_btn.pack(side="right")

        self.text.bind("<Key>", self.on_key)

        if not os.path.exists(EXPORT_DIR):
            os.makedirs(EXPORT_DIR, exist_ok=True)

    def on_key(self, event):
        if self.log_enabled.get():
            # Write a small JSON entry for each keypress (for demo only)
            entry = {"ts": datetime.utcnow().isoformat()+"Z", "key": event.keysym, "char": event.char}
            fname = os.path.join(EXPORT_DIR, "demo_log.jsonl")
            with open(fname, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")

    def save_note(self):
        content = self.text.get("1.0", "end-1c")
        fname = os.path.join(EXPORT_DIR, f"note_{int(time.time())}.txt")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Note saved to {fname}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DemoApp(root)
    root.mainloop()
