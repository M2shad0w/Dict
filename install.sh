#!/bin/bash
wget https://raw.githubusercontent.com/m2shad0w/Dict/master/dict.py -O dict
echo "are you sure to install these files? y|Y|yes|Yes"
read ANS
case $ANS in    
y|Y|yes|Yes) 
	echo "please input suder's passwd "
	read passwd
	echo $passwd |sudo -S mv ./dict /usr/local/bin/dict
	sudo chmod +x /usr/local/bin/dict
	echo "enjoy it ~~ !"
        ;;
n|N|no|No) 
        exit 0
        ;;
esac
