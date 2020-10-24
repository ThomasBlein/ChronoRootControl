=======================
ChronoRoot module setup
=======================

We assume you have some basic Linux knowledge in order to follow this procedure.

Download the image
==================

The latest Raspberry Pi OS version can always be downloaded from the `Raspberry Pi
Downloads page <https://www.raspberrypi.org/downloads/raspberry-pi-os>`_.
It’s recommended to download the *Minimal image based on Debian Buster*.

Writing an image to the SD card
===============================

You can follow `installing operating system images
<https://www.raspberrypi.org/documentation/installation/installing-images/README.md>`_
instructions from the Raspberry Pi web site.

Before plugging the SD Card in your Raspberry Pi you may have to make some changes.

*If you plan to  plug a keyboard and a screen to your rPi and don't want to access it
remotely by ssh you can skip this step.*

Insert the SD card into your computer’s card reader.
The SD card should mount automatically. You have to make several changes.

Enable ssh
++++++++++

Create an empty file named **ssh** inside  /boot the boot directory

You will be able to ssh to your Raspberry Pi module.

`ssh pi@IP`

The default password for *pi* user is *raspberry*

First boot
==========

Plug the SD Card you prepared in your Raspberry Pi. The first boot may take up
to 120 seconds. This is normal and is caused by the image expanding the filesystem
to the whole SD card. DO NOT REBOOT before the system is up and running.

ssh to your Raspberry Pi module (ssh pi) and become root (sudo su)

  * define a strong password for the root user
  * run `apt update && apt full-upgrade -y` in order to have everything up to date
  * run `rpi-update` to update firmwares
  * run raspi-config
    + activate camera (Choose "5 Interfacing Options", then "P1 Camera" and "Yes")
    + enable I2C (Chose "5 Interfacing Options", then "P5 I2C". Choose "Yes")
    + disable "Wait for Network at Boot” option
    + enable VNC
    + *enable "ssh" (optional "5 Interfacing Options", then "P2 SSH". Choose "Yes")*
    + setup your locale and timezone
    + allocate 256 MB for the GPU (this can also be done by setting "gpu_mem=255" in /boot/config.txt file)
  * uncomment the line starting with "hdmi_safe" in /boot/config.txt file

You can now reboot your rPi safely.

Installation on Raspberry Pi
============================

Install system dependencies : ::

    sudo apt install git python3 python3-pip python3-rpi.gpio i2c-tools


Install virtualenv on the system : ::

    sudo pip3 install virtualenv


Clone project from repository : ::

    mkdir -p /srv/ChronoRootrobot
    cd /srv/ChronoRootrobot

    git clone git@github.com:ThomasBlein/ChronoRootControl

    #create virtualenv for your project
    virtualenv -p /usr/bin/python3 .

    # activate
    source bin/activate

Install python requirements in project virtualenv : ::

    pip3 install -r requirements.txt

The user that will run the application need to be allowed to run the `date`
command via `sudo`.


After boot
==========

You have to activate `IVport mutiplexing module
<https://ivmech.com/magaza/en/development-modules-c-4/ivport-v2-raspberry-pi-camera-module-v2-multiplexer-p-107>`_
and make sure the wiring is good.

::

    $# cd ivport_v2
    $# python init_ivport.py
    $# i2cdetect -y 1
        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- --
    10: 10 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    60: -- -- -- -- 64 -- -- -- -- -- -- -- -- -- -- --
    70: 70 -- -- -- -- -- -- --

    $# vcgencmd get_camera
    supported=1 detected=1


Optional : Configure WiFi wireless access point
===============================================

If you want to be able to access to your *ChronoRoot module* by wifi you should
setup Raspberry Pi as a routed wireless access point.

Otherwise you'll be able to access the web server over the network.

In order to configure your *ChronoRoot module* as a wireless access point you can
follow instructions from `Setting up a Raspberry Pi as a routed wireless access point
<https://www.raspberrypi.org/documentation/configuration/wireless/access-point-routed.md>`_.


Install the web app and configure the server
============================================

Install necessary packages :

::

  apt install nginx-full uwsgi uwsgi-plugin-python3
  pip install uwsgitop

You'll find chronoroot.conf and uwisgi.ini files in *server* folder of this project.
Copy **uwisgi.ini** to **/etc/uwsgi/apps-available/** folder and **chronoroot.conf**
to **/etc/nginx/sites-available/** folder.

Be sure that you have "include /etc/nginx/sites-enabled/\*.conf;" line in /etc/nginx/nginx.conf file.

You'll have to adapt the content of those files to fit to your setup.

To enable nginx virtualhosts

::

  ln -s /etc/nginx/sites-available/chronoroot.conf /etc/nginx/sites-enabled/
  rm /etc/nginx/sites-enabled/default*
  sudo service nginx reload

You should now be able to connect to your rPi in your browser.

App configuration
=============

The default configuration is in `default_config.py` file. To apply local
modification please modify the `config.py` file.

Config.WORKING_DIR
    a string, the path to the folder containing the experiments.
Config.CAMS
    a list of cameras and name
Config.IR_GPIO
    an int, The GPIO controlling the IR (infra red) switch
Config.IR_WARM_UP
    an int, the delay for IR warm up in seconds


Launch the app
==============

The app is composed by two components. Flask web App & an
`uwisgi mule <https://uwsgi-docs.readthedocs.io/en/latest/Mules.html>`_.
uwsgi and nginx daemons should be up & running on each module.
