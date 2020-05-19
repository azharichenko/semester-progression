sudo apt-get update -y
sudo apt-get install python3-dev
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py
sudo rm get-pip.py
sudo pip3 install pipenv font_hanken_grotesk font_roboto
sudo apt-get install python3-numpy python3-pil -y
