# OSX4VM — Mastered Edition
### Windows Edition 1.0 · OpenCore 1.0.5

> Highly engineered. Optimized kernel. Intelligent boot engine.

OSX4VM is a hand-crafted OpenCore + QEMU/KVM configuration for running macOS on Windows (via WSL2) or native Linux. Built for maximum responsiveness, real Mac-like behavior, and the cleanest possible implementation.

---

## Getting Started

```bash
git clone https://github.com/ltnproject/OSX4VM.git
cd OSX4VM
```

---

## Prerequisites

Before running, make sure the following are in place:

- **Virtualization enabled** in your BIOS (VT-x for Intel, AMD-V/SVM for AMD)
- **WSL2** installed (Windows users) — or a native Linux environment
- **QEMU** and **KVM** installed on your system
- **Python 3** available in your terminal

> Not sure if virtualization is enabled? Check Task Manager → Performance → CPU and look for **Virtualization: Enabled**. If it shows Disabled, enter your BIOS and enable it before continuing.

---

## Setup Guide

### 1 — Fetch macOS Installer

Download the official macOS Recovery image directly from Apple's servers. Supports **macOS Tahoe (26)** and earlier.

```bash
python3 fetch_macos.py
```

### 2 — Create Virtual Disk

Create a high-performance QCOW2 virtual disk. 64 GB minimum, **128 GB recommended**.

```bash
qemu-img create -f qcow2 mac_hdd.qcow2 128G
```

### 3 — Initialize Boot Engine

Launch the boot engine. It automatically detects your hardware, verifies KVM health, and optimizes memory mapping.

```bash
chmod +x boot.sh && ./boot.sh
```

### 4 — Install macOS

Once OpenCore loads:

1. Select **macOS Base System**
2. Open **Disk Utility** and format your virtual drive as **APFS**
3. Close Disk Utility and proceed with the installation
4. Reboot when prompted — you're done

---

## What's Included

| Component | Description |
|---|---|
| `OpenCore/config.plist` | Hand-tuned OpenCore config with custom ACPI & RTC patches |
| `fetch_macos.py` | Direct Apple CDN fetcher with automated BaseSystem logic |
| `boot.sh` | Diagnostic boot engine with dynamic RAM/core allocation |

---

## Features

- **Advanced ACPI & RTC Patches** — Real Mac-like power behavior
- **Power Management Optimizations** — Tuned for KVM host environments
- **Enhanced WSL2 SMBios Data** — Seamless integration on Windows
- **Real-time KVM Health Check** — Validates your setup before every boot
- **Auto-Hardware Optimization** — Detects and adapts to your host machine
- **Dynamic RAM/Core Allocation** — Maximizes guest performance automatically
- **macOS Tahoe (26) Support** — Always up to date with the latest releases

---

## Configuration

The OpenCore configuration lives at `OpenCore/config.plist`. It includes custom kernel tweaks and resource allocation logic not found in standard repositories. Edit with caution — most users will not need to touch this file.

---

## Platform Support

| Platform | Status |
|---|---|
| Windows + WSL2 | ✅ Fully supported |
| Native Linux (KVM) | ✅ Fully supported |
| macOS host | ❌ Not supported |

---

## Notes

**Is this optimized?**
Yes. This version includes custom kernel tweaks and resource allocation logic not found in standard repositories. Hand-tuned ACPI patches ensure real Mac-like power behavior.

**Which macOS versions are supported?**
All modern macOS versions up to and including Tahoe (26). Select your target version when running `fetch_macos.py`.

---

## License

© 2026 Ltn Project. Privacy and power.

---

*For more detailed information, visit [github.com/ltnproject/OSX4VM](https://github.com/ltnproject/OSX4VM)*
