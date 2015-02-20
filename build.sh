#!/bin/bash

rm -rf ~/temp/DigitalFreedomWithRaspberryPI
mkdir ~/temp/DigitalFreedomWithRaspberryPI
python -m markdown README.md > ~/temp/DigitalFreedomWithRaspberryPI/index.html
python -m markdown web.md > ~/temp/DigitalFreedomWithRaspberryPI/web.html
python -m markdown introduction.md > ~/temp/DigitalFreedomWithRaspberryPI/introduction.html
python -m markdown LICENSE.md > ~/temp/DigitalFreedomWithRaspberryPI/LICENSE.html
python -m markdown setup.md > ~/temp/DigitalFreedomWithRaspberryPI/setup.html