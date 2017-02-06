#!/bin/bash
# https://www.raspberrypi.org/documentation/linux/software/python.md
echo "Run sudo raspi-config? [y/N]:"
read runraspi

if [ "$runraspi" = "y" ]
then
    echo "*** execute:  sudo raspi-config ***"
    echo "Perform the following configuration tasks:"
    echo "*** Expand the root filesystem ***"
    echo "*** Set/Verify: Advanced Options->Device Tree->Yes ***"
    echo "*** Set/Verify: Advanced Options->I2C->Yes ***"
    echo "*** Select Yes when asked to reboot ***"
    echo " "
    echo "*** Press enter/return to open raspi-config:"

    # wait for user to press enter
    read

    # open the raspi-config application
    sudo raspi-config

    read
fi


echo "******* apt-get update ******"
sudo apt-get update
echo "******* apt-get python3 ******"
sudo apt-get --yes --force-yes install python3
echo "******* Installing pip *******"
sudo apt-get --yes --force-yes install python3-pip
echo "******* Installing RPi.GPIO *******"
sudo apt-get --yes --force-yes install python3-rpi.gpio
echo "******* Installing i2c-tools *******"
sudo apt-get --yes --force-yes install i2c-tools
echo "******* Installing python3-smbus *******"
sudo apt-get --yes --force-yes install python3-smbus
echo "******* Installing git *******"
sudo apt-get --yes --force-yes install git
echo "******* add pi to i2c user *******"
sudo adduser pi i2c
echo "******* pip install requirements *******"
sudo pip install -r requirements.txt


