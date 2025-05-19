=======================
ChronoRoot module setup
=======================

We assume you have some basic Linux knowledge in order to follow this procedure.

Prepare PiOS on a SD card
=========================

Use `rpi-imager` to install and configure a Raspberry Pi OS compatible for ChronoRoot.

You will found instructions on installing `rpi-imager` on your computer on the `Raspberry Pi OS<https://www.raspberrypi.com/software/>`_ web page.

Execute rpi-imager and on the first screen:

* Select your raspberry pi model
* Select "Raspberry Pi OS (Legacy, 32-bit) Lite (`Bullseye` version)"" available in 'Raspberry Pi OS (other)' sub-menu.
* Select the SD card to flash

Press "continue". On the second screen, select "Adjust setup" and adjust parameters allowing to connect remotely to the raspberry pi:

* On "General" tab

  * Define user and password
  * configure Wifi
  * Define local (timezone and keyboard)

* On "Services" tab:
  
  * Activate ssh

Press "Save". Process to flash the SD card.


First boot of the Raspberry Pi
==============================

Insert the SD card in the Raspberry Pi, plug the Raspberry Pi and let it boot. It may take several minutes on first boot (5-10 minutes): it will wait for potential network connexion before boot and expand the file system on the full SD card.
DO NOT REBOOT before the system is up and running.

You can plug a screen to the Raspberry Pi to follow its progress. 

Connect to the fully booted Raspberry Pi through ssh using the credential you set during the configuration.

Setup Raspberry Pi hardware
===========================

We will use `raspi-config` to configure the different hardware options:

- Enable legacy camera interfaces
- Enable I2C interfaces and automatic loading of the I2C kernel module
- Deactivate Network at boot
- Set 256Mo of memory for the GPU

You can use the interactive interface of `raspi-config` or use the following commands:

::

    sudo raspi-config nonint do_legacy 0
    sudo raspi-config nonint do_i2c 0
    sudo raspi-config nonint do_boot_wait 0
    sudo raspi-config nonint do_memory_split 256


Reboot the Raspberry Pi to take into account the new hardware configuration

::

    sudo reboot

Setup the Raspberry Pi base packages
====================================

Update the system and install required packages


::

    sudo apt update
    sudo apt upgrade -y
    sudo apt install -y \
        git i2c-tools libffi-dev \
        python3 python3-pip python3-rpi.gpio python3-venv \
        nginx-full uwsgi uwsgi-plugin-python3 \
        libtiff-dev libjpeg-dev libopenjp2-7-dev zlib1g-dev \
        libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev \
        tk8.6-dev python3-tk libharfbuzz-dev libfribidi-dev \
        libxcb1-dev


Install ChronoRootControler application
=======================================

Create the directory structure for `ChronoRootControl` application

::

    sudo mkdir /srv/ChronoRootData
    sudo mkdir /srv/ChronoRootControl
    sudo chmod a+rw /srv/ChronoRootData
    sudo chmod a+rw /srv/ChronoRootControl

Install `ChronoRootControl` application from GitHub and setup the virtual environment

::

    cd /srv/ChronoRootControl
    git clone https://github.com/ThomasBlein/ChronoRootControl.git .
    chmod a+rw /srv/ChronoRootControl/log
    python3 -m venv /srv/ChronoRootControl/venv
    source /srv/ChronoRootControl/venv/bin/activate
    CFLAGS="-fcommon" pip install -r requirements.txt

Setup and restart `uwsgi` to use `ChronoRootControl`

::

    sudo cp \
        /srv/ChronoRootControl/server/uwsgi.ini \
        /etc/uwsgi/apps-available/ChronoRootControl.ini
    cd /etc/uwsgi/apps-enabled/
    sudo ln -s ../apps-available/ChronoRootControl.ini .
    sudo systemctl restart uwsgi

Setup and restart `nginx` as web-proxy


::

    sudo cp \
        /srv/ChronoRootControl/server/nginx.conf \
        /etc/nginx/sites-available/chronorootcontrol.conf
    sudo rm /etc/nginx/sites-enabled/default
    cd /etc/nginx/sites-enabled/
    sudo ln -s ../sites-available/chronorootcontrol.conf .
    sudo systemctl restart nginx

Automatic mounting of USB disk
==============================

To automaticly mount first USB drive on /media/usb0. Create the `/media/usb0` directory and add an entry to the /etc/fstab file.
The automounting work at startup of the module:

::

    sudo mkdir /media/usb0
    sudo chmod a+rw /media/usb0
    echo '/dev/sda1	/media/usb0	vfat	defaults,auto,users,rw,nofail,noatime	0	0' \
        | sudo tee -a /etc/fstab
