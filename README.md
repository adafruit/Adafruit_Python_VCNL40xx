DEPRECATED LIBRARY Adafruit Python VCNL40xx
===================

This library has been deprecated!

we are now only using our circuitpython sensor libraries in python, they work great and are easier to maintain

we are leaving the code up for historical/research purposes but archiving the repository.

check out this guide for using the vcnl4010 with python!
https://learn.adafruit.com/using-vcnl4010-proximity-sensor

##

Python code to use the VCNL4000 &amp; VCNL4010 proximity sensors with the Raspberry Pi &amp; BeagleBone Black.

## Installation

To install the library from source (recommended) run the following commands on a Raspberry Pi or other Debian-based OS system:

    sudo apt-get install git build-essential python-dev
    cd ~
    git clone https://github.com/adafruit/Adafruit_Python_VCNL40xx.git
    cd Adafruit_Python_VCNL40xx
    sudo python setup.py install

Alternatively you can install from pip with:

    sudo pip install adafruit-vcnl40xx

Note that the pip install method **won't** install the example code.
