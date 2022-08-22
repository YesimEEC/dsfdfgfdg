#!/bin/bash
sudo apt update -y
sudo apt install -y build-essential libtool autoconf wget python3-pip
sudo apt install -y gcc-10 g++-10
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 100 --slave /usr/bin/g++ g++ /usr/bin/g++-10
sudo apt-get install -y cppcheck
sudo apt-get install git wget libncurses-dev flex bison gperf python3 python3-pip python3-setuptools python3-serial python3-cryptography python3-future python3-pyparsing python3-pyelftools cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0
sudo apt-get install gawk gperf grep gettext python python-dev automake bison flex texinfo help2man libtool libtool-bin make
pip install -r requirements.txt
pre-commit install

if [ ! -f /opt/esp/tools/xtensa-esp32-elf/bin/xtensa-esp32-elf-gcc ]
then
    sudo chmod -R 777 /opt/
    cd /opt/
    mkdir esp
    cd esp
    git clone -b v4.4.1 --recursive https://github.com/espressif/esp-idf.git
    mkdir tools
    cd tools
    git clone https://github.com/espressif/crosstool-NG.git
    cd crosstool-NG
    git checkout esp-2021r2-patch3
    git submodule update --init
    ./bootstrap && ./configure --enable-local && make
    ./ct-ng xtensa-esp32-elf
    ./ct-ng build
    cd /opt/esp/tools/crosstool-NG/builds
    chmod -R u+w xtensa-esp32-elf
    mv xtensa-esp32-elf /opt/esp/tools
    cd ..
    cd ..
    rm -rf crosstool-NG
fi

