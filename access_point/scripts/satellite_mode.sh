#!/bin/bash

###
# Authors: Maël Jeuffrard/Thomas Blein
# Date: May 2025
# Description:
# This script is call by /etc/kinematic/check_mod.py
# It changes ChronoRoot module network configuration to the satellite mode:
# it disable the access point and dhcp/dns server and set the wlan0 network interface as client.
###

LOGFILE=/var/log/automode.log
LIST_SERVICES="dnsmasq hostapd"
NETWORK_CONFIG_FILE=/etc/ChronoRoot/satellite_interface
INTERFACES_FILE=/etc/network/interfaces.d/wlan0
WIFI_INTERFACE="wlan0"

if [ -e $NETWORK_SONFIG_FILE ]; then
  if [ "$(readlink $INTERFACES_FILE)" != "$NETWORK_CONFIG_FILE" ]; then
    ln --symbolic --force $NETWORK_CONFIG_FILE $INTERFACES_FILE
    if [ $? == 1 ]; then
      echo $(date +%Y-%m-%d/%H:%M:%S) "Can not create symlink"
    fi
    ifdown $WIFI_INTERFACE && ifup $WIFI_INTERFACE
  fi
else
  echo $(date +%Y-%m-%d/%H:%M:%S) "$NETWORK_CONFIG_FILE do not exist"
fi

for srv in $LIST_SERVICES; do
  systemctl is-active $srv -q
  if [ $? != 0 ]; then
    echo $(date +%Y-%m-%d/%H:%M:%S) "$srv is already stopped"
  else
    systemctl stop $srv
    if [ $? == 1 ]; then
      echo $(date +%Y-%m-%d/%H:%M:%S) "Can not stop $srv"
    fi
    systemctl disable $srv
    if [ $? == 1 ]; then
      echo $(date +%Y-%m-%d/%H:%M:%S) "Can not disable $srv"
    fi
  fi
done
