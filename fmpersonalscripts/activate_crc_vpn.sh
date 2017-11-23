#!/usr/bin/env bash
## Connect to University of IDAHO vpn

# Check if already connected
if ! ifconfig | grep -q tun0; then
    ( sudo openvpn --config "$HOME/data/vpn_certs/schaack-crc.ovpn" ) &
    # Wait for the VPN to fully activate
    sleep 8
fi
