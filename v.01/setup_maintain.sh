#!/bin/bash
#script file used for setting up rpi for digital wastebin
#as well as run daily maintainance 

# MAIN_PY_FILE_NAME="test_new_format" 
# MAIN_PY_FILE="pygame_test.py"

#list of necessary software
SOFTWARE=" python3 python-serial ufw ntp python3-pip chromium-browser "

#time for the computer to sleep
REBOOT_TIME="24:00" 

#quit if there is any error
set -e 

#MAINTAINANCE CODE
if [ -e ~/dwb_installed ]
then
sudo ufw enable
sudo ifconfig wlan0 up
sudo service ntp restart
cd ~/UCI-Digital-Waste-Bin/
git pull
sudo apt-get update
sudo apt-get dist-upgrade -y 
sudo timedatectl set-timezone US/Pacific
sudo ifconfig wlan0 down
shutdown -r ${REBOOT_TIME}

#INITIAL SETUP CODE
else
#change password from default
echo "Please enter password"
passwd
sudo passwd -l root 

#update and install the necessary software
sudo apt-get update
sudo apt-get dist-upgrade -y 
sudo apt-get install ${SOFTWARE}
python3 -m pip install pyserial

#enable firewall
sudo ufw enable 
sudo ufw status

#set the correct timezone to California
sudo timedatectl set-timezone US/Pacific

#disable bluetooth after reboot and rotate the display
echo "dtoverlay=pi3-disable-bt" | sudo tee --append /boot/config.txt
echo "display_rotate=3" | sudo tee --append /boot/config.txt


#enable auto-login
sed -i -e '/autologin-user/s/#//' -e '/autologin-user/s/$/pi' /etc/lightdm/lightdm.conf

#Add to startup file to run python script and the html code at boot as well 
#as disable sleep mode and screensaver for rpi
sudo sed -i -e '/@xscreensaver/s/^/#/' ~/.config/lxsession/LXDE-pi/autostart
echo "@xset s off" | sudo tee --append ~/.config/lxsession/LXDE-pi/autostart
echo "@xset -dpms" | sudo tee --append ~/.config/lxsession/LXDE-pi/autostart
echo "@xset s noblank" | sudo tee --append ~/.config/lxsession/LXDE-pi/autostart
echo "@sed -i 's/\"exited_cleanly\": true/' ~/.config/chromium/Default/Preferences " | sudo tee --append ~/.config/lxsession/LXDE-pi/autostart
echo "@sudo /usr/bin/python3 ~/UCI-Digital-Waste-Bin/v.01/scale_serial.py" | sudo tee --append ~/.config/lxsession/LXDE-pi/autostart
echo "@point-rpi" | sudo tee --append ~/.config/lxsession/LXDE-pi/autostart
echo "@chromium-browser --noerrdialogs --kiosk --incognito --allow-file-access-from-files ~/UCI-Digital-Waste-Bin/v.01/index.html" | sudo tee --append ~/.config/lxsession/LXDE-pi/autostart

#Create symlink for the scale, the number seems to be same for every scale
echo "ACTION==\"add\",SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"0403\", ATTRS{idProduct}==\"6001\", SYMLINK+=\"SCALE\"" >> /etc/udev/rules.d/99-com.rules

echo "Setup done, the system will reboot in 5 seconds"
sleep 5

#touch ~/dwb_installed
sudo reboot
fi