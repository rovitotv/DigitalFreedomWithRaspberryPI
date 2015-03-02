# Setup

## Hardware

I highly recommend the Raspberry Pi 2 because it is the same price as the
Raspberry PI model B but has four cores and 1 GB of RAM.  Same price but six
times the performance with double the RAM not many down sides to the Raspberry
PI 2.  Yes a Raspberry PI model B will work with this guide but it will be slow.
As far as flash cards I use a class 10 that is 16 GB of size.  If you plan on 
using Raspberry Pi 1 model B then you could purchase two of them
and run one as a web server and one as an email server to divide the load
between the two Raspberry Pi systems.  Experimentation is required to see what
fits your needs best, I currently run both my email server and web server on
a single Raspberry Pi 2 and it seems to handle the load.

## Raspberry Pi Setup

For install setup the Raspberry Pi with a keyboard, video device, and
Ethernet cable.  After install of the operating system the video device can
be removed.  

## Operating System

This book uses Raspbian operating system which is the "official" operating 
system for the Raspberry PI.  It is based on Debian Linux "Wheezy" and includes
many packages that will make digital freedom easily obtainable. 

## NOOBS

NOOBS is "New Out Of the Box Software" and is a easy operating system install
manager for the Raspberry Pi.  Basically you download to your Mac, Windows, or
Linux computer then unzip then drag to your flash card (inside of the root
directory of the flash card).  Then you put the flash card into your
Raspberry Pi and boot.  On boot up a user is given a choice of operating
systems to install but for this guide you want Raspbian.  NOOBS does make it
easy to install and experiment with other operating system.  The 
[raspberrypi.org](http://www.raspberrypi.org/help/noobs-setup/) web site has
a great video and step by step instructions.  

## Installation of Raspbian

After NOOBS boots up select Raspbian then the system will boot.  At this point
a user has a few choices and will come to the Raspbian configuration screen
with a blue background. rasp-config.  Select "Configure the keyboard layout"
and choose generic 101 key PC.  Then select other select english/US.  Use the
default keyboard layout.  TODO: Need to work on this section.  Most likely have
to perform an install again and take pictures along the way.  Install with no
x-server or just boot to console.  We don't need a x-server because our 
Raspberry Pi will be in the corner staying busy processing email and hosting
our personal blog.  

## Updating

No matter which version of NOOBS that you use your operating system will
most likely need patching.  Whenever possible you should try and update
your Raspberry PI's operating system at least monthly.  Computers are all
about automation so you could setup a cron script and do the update on a
regular basis.  There is a small chance that updating could break your OS
so some people update only after backups.  If you keep your Raspberry PI
behind a firewall with only a select number of ports open your Raspberry
Pi is secure.  Sets to update:

```bash
sudo apt-get update
sudo apt-get upgrade
sudo rpi-update
sudo reboot
```

# Host and Domain Names

For email to work properly the host and domain names must be set properly. By
default Raspbian installs with a host name of `raspberrypi` which I am guessing
is not your host name.  For email I use the host name `mail` and use `www` for
web.  To set the host name use the command below:

```bash
sudo nano /etc/hostname
```

Then change the host name to mail.  Next edit the following file:

```bash
sudo nano /etc/hosts
```

Then add the following two lines, assuming your Raspberry Pi's IP address is
192.168.1.2.

```bash
192.168.1.2 mail.rovitotv.org mail
192.168.1.2 www.rovitotv.org www
```
***Change the domain name from rovitotv.org to your domain name***

After the changes you can verify the changes with the following commands:

```bash
$ hostname --short
mail

$ hostname --domain
rovitotv.org

$ hostname --fqdn
mail.rovitotv.org

$ hostname --ip-address
192.168.1.2
```

The `$` signifies the prompt and the following line is the expected output, but
remember to change your domain name as needed.


