#!/bin/sh
#whole thing takes 10-30 minutes
#run as user not root or pip screws up

sudo apt-get update
#sudo apt-get upgrade -y

#pip
sudo apt-get install python3-pip -y

#spacy (takes ~10 minutes on its own)
pip3 install --user spacy
python3 -m spacy.en.download

#pattern:
sudo apt-get install git -y
git clone https://github.com/pattern3/pattern
cp /home/vagrant/pattern/pattern /vagrant -r

#nltk
sudo apt-get install python3-nltk -y
python3 -c "import nltk; nltk.download('wordnet')"

