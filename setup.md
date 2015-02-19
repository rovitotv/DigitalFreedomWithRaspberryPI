Setup
=====

Hardware
--------

I highly recommend the Raspberry PI 2 because it is the same price as the
Raspberry PI model B but has four cores and 1 GB of RAM.  Same price but six
times the performance with double the RAM not many down sides to the Raspberry
PI 2.  Yes a Raspberry PI model B will work with this book but it will be slow.
As far as flash cards I use a class 10 that is 16 GB of size.

Operating System
----------------

This book uses Raspbian operating system which is the "official" operating 
system for the Raspberry PI.  It is based on Debian Linux "Wheezy" and includes
many packages that will make digital freedom easy obtainable.  

NOOBS
-----

Updating
--------

No matter which version of NOOBS that you use your operating system will
most likely need patching.  Whenever possible you should try and update
your Rasberry PI's operating system at least montly.  Computers are all
about automation so you could setup a cron script and do the update on a
regular basis.  There is a small chance that updating could break your OS
so some people update only after backups.  If you keep your Raspberry PI
behind a firewall with only a select number of ports open your Raspberry
PI is secure.  Sets to update:

sudo apt-get update
sudo apt-get upgrade
sudo rpi-update