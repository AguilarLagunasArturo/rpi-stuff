# RPI
This is the greatest RPI setup of all time.

## Setup
Stuff I usually install.

### Python3 modules
``` bash
pip install numpy
pip install cv-recon
pip install Flask
pip install matplotlib
sudo apt install python3-smbus # mpu6050
```
### OpenCV
``` bash
# Compilers
sudo apt install python3 cmake gcc g++ 

# Python3 support
sudo apt install python3-dev python3-numpy 

# GTK3 support
sudo apt install libavcodec-dev libavformat-dev libswscale-dev 
sudo apt install libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev
sudo apt install libgtk-3-dev 

# Others
sudo apt install libpng-dev
sudo apt install libjpeg-dev
sudo apt install libopenexr-dev
sudo apt install libtiff-dev
sudo apt install libwebp-dev

# Download
cd /opt
sudo mkdir ocv
cd ocv
sudo wget https://github.com/opencv/opencv/archive/refs/tags/4.5.2.tar.gz
sudo tar -xvf 4.5.2.tar.gz

# Build
cd opencv-4.5.2
mkdir build
cd build
sudo cmake ../

sudo make
sudo make install
```

### Others
``` bash
sudo apt install htop
sudo apt install neofetch
sudo apt install x11vnc
```

### Services
``` bash
# sudo x11vnc -storepasswd some-passwd /etc/x11vnc.pwd
# sudo chown user:user-group /etc/x11vnc.pwd
# sudo cp x11vnc.service /etc/systemd/system/
# sudo systemctl enable x11vnc

[Unit]
Description=VNC Server for X11
Requires=display-manager.service
After=syslog.target network-online.target
Wants=syslog.target network-online.target

[Service]
User=your-user
Group=your-user-group
ExecStart=/usr/bin/x11vnc -display :0 -rfbauth /etc/x11vnc.pwd -shared -forever
ExecStop=/usr/bin/x11vnc -R stop
Restart=on-failure
RestartSec=2

[Install]
WantedBy=multi-user.target
```
