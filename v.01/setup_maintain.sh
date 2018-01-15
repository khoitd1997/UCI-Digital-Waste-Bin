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
if [ -e ${HOME}/${USER}/dwb_installed ]
then
chromium-browser index.html --allow-file-access-from-files
sudo ifconfig wlan0 up
sudo service ntp restart
sudo ufw enable
sudo apt-get update
sudo apt-get dist-upgrade -y 
sudo timedatectl set-timezone US/Pacific
sudo ifconfig wlan0 down
shutdown -r ${REBOOT_TIME}

#launch the scale and html code
chromium-browser ${HOME}/${USER}/{MAIN_PY_FILE_NAME}/index.html --allow-file-access-from-files --noerrdialogs --kiosk

python3 scale_serial.py

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

#Create symlink for the scale, the number seems to be same for every scale
echo "ACTION==\"add\",SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"0403\", ATTRS{idProduct}==\"6001\", SYMLINK+=\"SCALE\"" >> /etc/udev/rules.d/99-com.rules

echo "Setup done, the system will reboot in 5 seconds"
sleep 5

#touch ${HOME}/dwb_installed
sudo reboot
fi