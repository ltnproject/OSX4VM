#!/usr/bin/env bash

# OSX4VM - Masterful Unified Boot Engine (Personal Edition)
# ---------------------------------------------------------
# Engineered for peak performance and stability on Windows/WSL2

# --- Color Scheme ---
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}OSX4VM Masterful Boot Engine${NC}"
echo -e "---------------------------------"

# --- Diagnostic Layer ---
echo -n "[*] Checking KVM availability... "
if [ -e /dev/kvm ]; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}ERROR: KVM not found. Enable Virtualization in BIOS/Windows Features.${NC}"
    exit 1
fi

echo -n "[*] Detecting environment... "
if grep -qi "microsoft" /proc/version; then
    ENV_TYPE="WSL2"
    echo -e "${BLUE}WSL2${NC}"
else
    ENV_TYPE="Native"
    echo -e "${BLUE}Native Linux${NC}"
fi

# --- Hardware Intelligence ---
RAM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
RAM_GB=$((RAM_KB / 1024 / 1024))
CORES=$(nproc)

# Intelligent Resource Allocation
ALLOCATED_RAM=$((RAM_GB / 2))
[ $ALLOCATED_RAM -lt 4 ] && ALLOCATED_RAM=4
[ $ALLOCATED_RAM -gt 16 ] && ALLOCATED_RAM=16

ALLOCATED_CORES=$((CORES / 2))
[ $ALLOCATED_CORES -lt 2 ] && ALLOCATED_CORES=2

echo -e "[*] Host: ${RAM_GB}GB RAM, ${CORES} Cores detected."
echo -e "[*] Allocating: ${ALLOCATED_RAM}GB RAM, ${ALLOCATED_CORES} Cores to macOS."

# --- CPU Optimization ---
if grep -qi "intel" /proc/cpuinfo; then
    CPU_VENDOR="GenuineIntel"
    CPU_TYPE="Haswell-noTSX"
elif grep -qi "amd" /proc/cpuinfo; then
    CPU_VENDOR="AuthenticAMD"
    CPU_TYPE="Penryn"
fi

# --- QEMU Configuration ---
if [ "$ENV_TYPE" == "WSL2" ]; then
    DISPLAY="-device virtio-vga,id=video0,max_outputs=1"
    NET="-netdev user,id=net0,hostfwd=tcp::2222-:22 -device virtio-net-pci,netdev=net0"
else
    DISPLAY="-device vmware-svga"
    NET="-netdev user,id=net0 -device virtio-net-pci,netdev=net0"
fi

ARGS=(
    -enable-kvm
    -m "${ALLOCATED_RAM}G"
    -cpu "$CPU_TYPE",kvm=on,vendor="$CPU_VENDOR",+invtsc,vmware-cpuid-freq=on
    -machine q35
    -smp "$ALLOCATED_CORES",cores="$ALLOCATED_CORES",sockets=1
    -device qemu-xhci,id=xhci
    -device usb-kbd,bus=xhci.0
    -device usb-tablet,bus=xhci.0
    -device isa-applesmc,osk="ourhardworkbythesewordsguardedpleasedontsteal(c)AppleComputerInc"
    -drive if=pflash,format=raw,readonly=on,file="./OVMF_CODE_4M.fd"
    -drive if=pflash,format=raw,file="./OVMF_VARS.fd"
    -smbios type=2
    -device ich9-intel-hda -device hda-duplex
    -drive id=OpenCore,if=none,snapshot=on,format=qcow2,file="./OpenCore/OpenCore.qcow2"
    -device ide-hd,bus=sata.2,drive=OpenCore
    -drive id=MacHDD,if=none,file="./mac_hdd.qcow2",format=qcow2
    -device ide-hd,bus=sata.3,drive=MacHDD
    $NET
    $DISPLAY
    -monitor stdio
)

echo -e "${GREEN}[+] Personal Engine Initialized. Launching macOS...${NC}"
qemu-system-x86_64 "${ARGS[@]}"
