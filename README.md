# Keylogger Classroom Project — README

**Purpose:**
This repository contains three safe, consent-first classroom tools for your Infosec lab:

1. **Consented keystroke recorder** (`scripts/consented_recorder.py`) — records keystrokes only after typed consent, periodically exports data, writes a final export and ZIP when stopped.
2. **Controlled demo app** (`scripts/demo_attached_logger.py`) — a simple Tkinter notes application that can optionally enable internal logging (consent checkbox). Demonstrates how logging can be attached to a normal app.
3. **Defensive detector** (`scripts/detector.py`) — heuristics-based local detector that scans for suspicious processes, modules, and (on Linux) processes that access `/dev/input/*`.

> **Ethics & legal notice:** Only run these tools in a lab environment, on machines you own, or where you have written consent from the owner and all participants. Do **not** deploy or use outside of approved coursework. Keep all exported logs confidential and delete when the lab is complete.

---

## Project layout

```
keylogger-classroom-project/
├─ .venv/                        # virtual environment (created by setup)
├─ requirements.txt              # pip requirements (pynput, psutil)
├─ README.md                     # this file
├─ CONSENT.txt                   # consent template
├─ setup.sh                      # helper: create venv & install (macOS / Linux)
├─ setup.ps1                     # helper: create venv & install (Windows PowerShell)
├─ scripts/
│  ├─ consented_recorder.py      # consent-first global key recorder (pynput)
│  ├─ demo_attached_logger.py    # Tkinter demo app with optional internal logging
│  └─ detector.py                # heuristics-based local detector (psutil)
└─ exports/                      # output folder created by scripts for logs & zips
   ├─ recorder_exports/          # consented recorder writes here
   └─ demo_exports/              # demo app writes here
```

---

## Requirements

* Python 3.8+ recommended.
* pip

Python packages (see `requirements.txt`):

```
pynput>=1.7.6
psutil>=5.9.0
```

**System packages:**

* `tkinter` is required by the demo app. It is bundled with many Python installs; on Debian/Ubuntu you may need `sudo apt install python3-tk`.
* On macOS, global keystroke capture requires granting Accessibility permission to Terminal or Python.

---

## Quick setup (create venv & install dependencies)

### Linux / macOS (one line)

```bash
cd keylogger-classroom-project
python3 -m venv .venv && source .venv/bin/activate && python -m pip install --upgrade pip && pip install -r requirements.txt
```

If your Python executable is `python` instead of `python3`, replace accordingly.

### Windows PowerShell (one line)

```powershell
cd keylogger-classroom-project
python -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install --upgrade pip; pip install -r requirements.txt
```

If PowerShell blocks activation, allow it temporarily for the session:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

---

## Activate the virtual environment

* macOS / Linux:

```bash
source .venv/bin/activate
```

* Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, `python` and `pip` will point to the virtual environment.

---

## Running the tools

Open a terminal, activate the venv, then run the scripts from the `scripts/` folder.

### 1) Run the defensive detector

```bash
cd scripts
python detector.py
```

* Prints a heuristics-based report of suspicious processes or device access.
* Good to run first to create a baseline.

### 2) Run the controlled demo app (notes app with optional logger)

```bash
cd scripts
python demo_attached_logger.py
```

* UI: a simple notes editor. Use the checkbox "Enable internal logging (consent)" to start logging to `exports/demo_exports/demo_log.jsonl`.
* Save notes with the "Save Note" button.
* Use this to teach how an application can be extended to log input.

### 3) Run the consented keystroke recorder

```bash
cd scripts
python consented_recorder.py
```

* The script asks for explicit typed consent. Type `I CONSENT` (exactly) to proceed.
* Records key presses/releases via `pynput` and stores entries with timestamps.
* Writes periodic partial exports (every `EXPORT_INTERVAL` seconds) to `exports/recorder_exports/`.
* Press **ESC** to stop; the script writes a final JSON export and packages exports into a ZIP archive.

---

## Troubleshooting & notes

* **macOS Accessibility:** macOS blocks global input capture until you allow Accessibility permission for Terminal/Python in System Settings → Security & Privacy → Privacy → Accessibility.

* **Anti-virus / EDR:** Programs that use low-level input hooks (like `pynput`) may trigger AV/EDR alerts even when used for legitimate classroom work. Use isolated VMs and coordinate with your lab/IT.

* **tkinter on Linux:** If `demo_attached_logger.py` fails to start due to missing Tk support, install your distro's `python3-tk` package.

* **Permissions on Linux for `/dev/input`:** the detector’s check for processes opening `/dev/input/*` usually requires root to see detailed open file handles. That part is optional and purely educational.

* **Data handling:** Treat export files as sensitive. Keep them on lab machines and delete after the exercise.

---

## Extending the project (ideas)

* Improve the detector to check startup autoruns (Windows Registry, Task Scheduler) in a read-only fashion.
* Add a GUI for the detector with alerts and exportable reports.
* Add secure handling for exported logs (encrypt with a classroom shared key) to practice secure telemetry handling.

---

