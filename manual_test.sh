source venv/bin/activate
cd ./ivport_v2/
python init_ivport.py
cd ..
i2cdetect -y 1
vcgencmd get_camera
python -c 'from ivport_v2 import ivport; iv = ivport.IVPort(ivport.TYPE_QUAD2); iv.camera_change(1)'
raspistill -o /media/usb0/testimg.jpg
if [ ! -f /media/usb0/testimg.jpg ]; then
	rm /media/usb0/testimg.jpg
fi
