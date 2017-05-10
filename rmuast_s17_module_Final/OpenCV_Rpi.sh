#!/bin/bash

# Script to 
# Install OpenCV on Raspbian RaspberryPi3

# Update and upgrade the system
sudo apt-get update && sudo apt-get upgrade

# Download all dependencies
apt-get install -y build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk2.0-dev libatlas-base-dev gfortran python2.7-dev python3-dev

# Download the base version of OpenCV in the home folder and unzip it
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.2.0.zip
unzip opencv.zip

# Download the contrib packages in the home folder and unzip them
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.2.0.zip
unzip opencv_contrib.zip

# Download and install pip for both versions of python
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
python3 get-pip.py

# Download  and install imutils for both versions of python
pip install imutils
pip3 install imutils

# Generate a build folder in OpenCV's main folder and create the MakeFiles needed to begin the building process
cd ~/opencv-3.2.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D INSTALL_PYTHON_EXAMPLES=ON -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.2.0/modules -D BUILD_EXAMPLES=ON ..

# Now you are ready to begin the installation of OpenCV