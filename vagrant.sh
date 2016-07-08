#!/bin/sh

echo HELLO WORLD >> ~/TESTTEST
echo "HELLO WORLD"

sudo apt-get update
#sudo apt-get upgrade -y

#install nltk
#sudo apt-get install python3-setuptools python-setuptools
#sudo easy_install pip3
#sudo apt-get install python3-minimal
#
#sudo apt-get install python3-setuptools
#sudo easy_install3 pip
#
#wget https://bootstrap.pypa.io/get-pip.py

sudo apt-get install python3-pip -y
pip3 install --user nltk
#pip3 install --user spacy

sudo apt-get install git -y
git clone https://github.com/pattern3/pattern -o ~/pattern3
cp ~/pattern3/pattern /vagrant -r

