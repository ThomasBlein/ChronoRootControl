#!/bin/bash

###
# Authors: Maël Jeuffrard/Thomas Blein
# Date: May 2025
# Description:
# This script is called by /etc/ChronoRoot/check_mod.py
# It changes ChronoRoot module network configuration to access_point mode:
# it enables the access point and dhcp/dns server
###

LOGFILE=/var/log/automode.log
LIST_SERVICES="dnsmasq hostapd"
NETWORK_CONFIG_FILE=/etc/ChronoRoot/access_point_interface
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
  if [ $? == 0 ]; then
    echo $(date +%Y-%m-%d/%H:%M:%S) "$srv is already started"
  else
    systemctl enable $srv
    if [ $? == 1 ]; then
      echo $(date +%Y-%m-%d/%H:%M:%S) "Can not enable $srv"
    fi
    systemctl stop $srv && systemctl start $srv
    if [ $? == 1 ]; then
      echo $(date +%Y-%m-%d/%H:%M:%S) "Can not start $srv"
    fi
  fi
done
