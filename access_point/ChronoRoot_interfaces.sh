#!/bin/bash

# Create the directory to handle the ChronoRoot specific files
mkdir -p /etc/ChronoRoot

# Deploy the modules_info.csv file if present
if [ -f modules_info.csv ]; then
  cp modules_info.csv /etc/ChronoRoot
  # Deploy the auto hostname script
  cp ./scripts/auto_hostname.sh /etc/init.d/auto_hostname.sh
  chown root:root /etc/init.d/auto_hostname.sh
  chmod 755 /etc/init.d/auto_hostname.sh
fi

# Setup the access point configuration #
#######################################

# install the required packages and disable the services
apt install -y dnsmasq hostapd netfilter-persistent
systemctl stop dnsmasq
systemctl disable dnsmasq
systemctl unmask hostapd
systemctl disable hostapd

# DHCP configuration through dnsmasq
cp ./conf/dnsmasq.conf /etc/dnsmasq.d/10_dhcp_configuration.conf
chown root:root /etc/dnsmasq.d/10_dhcp_configuration.conf
chmod 644 /etc/dnsmasq.d/10_dhcp_configuration.conf

# Wifi configuration as server (hostapd)
# If a personalised conf file exist use it or fallback on the default
if [ -f ./conf/hostapd.conf ]; then
  cp ./conf/hostapd.conf /etc/hostapd/hostapd.conf
else
  cp ./conf/hostapd.default.conf /etc/hostapd/hostapd.conf
fi
chown root:root /etc/hostapd/hostapd.conf
chmod 644 /etc/hostapd/hostapd.conf

# Enable packet forwarding for IPV4 in the kernel and firewall
cp ./conf/ipv4.ip_forward.conf /etc/sysctl.d/50_ipv4.ip_forward.conf
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
netfilter-persistent save

# Deploy the different network configuration if access_point or satellite
cp ./conf/access_point_interface /etc/ChronoRoot/
cp ./conf/satellite_interface /etc/ChronoRoot/
# Wifi configuration as client (wpa supplicant)
# If a personalised conf file exist use it or fallback on the default
if [ -f ./conf/chronoroot_wpa_supplicant.conf ]; then
  cp ./conf/chronoroot_wpa_supplicant.conf /etc/ChronoRoot/chronoroot_wpa_supplicant.conf
else
  cp ./conf/chronoroot_wpa_supplicant.default.conf /etc/ChronoRoot/chronoroot_wpa_supplicant.conf
fi
# Deploy the scripts for status change
cp ./scripts/access_point_mode.sh /etc/ChronoRoot/
cp ./scripts/satellite_mode.sh /etc/ChronoRoot/
cp ./scripts/check_mode.py /etc/ChronoRoot/
# Set the right
chown -R root:root /etc/ChronoRoot/*
chmod 644 /etc/ChronoRoot/*
chmod 600 /etc/ChronoRoot/chronoroot_wpa_supplicant.conf
chmod +x /etc/ChronoRoot/*.sh
chmod +x /etc/ChronoRoot/*.py

# Setup jumper status check service
cp ./conf/check_mod.service /etc/systemd/system/
chown root:root /etc/systemd/system/check_mod.service
chmod 644 /etc/systemd/system/check_mod.service
systemctl daemon-reload
# systemctl enable check_mod.service

# Deploy the fixed IP configuration based on modules_info.csv if present
if [ -f /etc/ChronoRoot/modules_info.csv ]; then
  tail -n+2 /etc/ChronoRoot/modules_info.csv |
    sed "s/^/dhcp-host=/" \
      >/etc/dnsmasq.d/50_chronoroot_modules.conf
fi
