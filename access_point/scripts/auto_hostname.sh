#!/bin/bash
### BEGIN INIT INFO
# Provides:          Nom du script
# Required-Start:    $local_fs $network
# Required-Stop:     $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Automatic set hostname according to MAC
# Description:       Automatic set hostname according to the MAC address and name set in the module_info.csv file
### END INIT INFO

MODULE_INFO=/etc/ChronoRoot/module_info.csv
MAC_ADD=$(cat /sys/class/net/wlan0/address)
HOSTNAME=$(grep -i "$MAC_ADD" $MODULE_INFO | cut -d, -f2)

if [ ! $HOSTNAME -eq "" ]; then
  if [ $(hostname) -eq $HOSTNAME]; then
    hostnamectl set-hostname $HOSTNAME
  fi
fi
