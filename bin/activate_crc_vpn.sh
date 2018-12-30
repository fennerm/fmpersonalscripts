#!/usr/bin/env bash
## Connect to IBEST vpn

# Check if already connected
if ! ifconfig | grep -q tun0; then
    sudo openvpn --config "/home/fen-arch/data/vpn_certs/schaack-crc.ovpn" || true
    # Wait for the VPN to fully activate
    sleep 8
    sync-dotfiles
fi
