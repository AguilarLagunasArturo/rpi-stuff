# RPI

## Setup
Stuff I usually install.

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
