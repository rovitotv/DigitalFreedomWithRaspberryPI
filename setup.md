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
a single Raspberry Pi 2 and it seems to handle the load.  In addition to the
Raspberry Pi 2 I have a Netgear Wireless-G Router model WGR614.  The router
lets me open/close Internet ports and acts as a firewall for my network.  Most
people already own a device similar to this

## Raspberry Pi Setup

For install setup the Raspberry Pi with a keyboard, video device, and
Ethernet cable.  After install of the operating system the video device can
be removed.  

## The Raspbian Operating System

This book uses Raspbian operating system which is the "official" operating
system for the Raspberry PI.  It is based on Debian Linux "Jessie" and includes
many packages that will make digital freedom easily obtainable. Raspbian uses
Debian because it offers a strong foundation on which to build a Linux
distribution.  Debian (and by inheritance Raspbian) provide a large number of
pre-compiled packages which are called `.deb` files.  The creators of Debian
created a set of tools called `apt-get` which let you easily download and
automatically install these packages on your system making software management
easy.  Raspbian consists of over 35,000 packages which have been optimized for
best performance on the Raspberry Pi.  In most of this guide packages will be
installed this makes sure the compilation of complicated code bases is done
correctly and optimized for the Raspberry Pi.  One issue with compiling code
directly on the Raspberry Pi is the amount of time it can consume since the
Raspberry Pi doesn't have the  fastest processor.  Using packages is faster and
often the executables are optimized.

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

The `$` signifies the prompt and the line after the prompt is the expected 
output, but remember to change your domain name as needed.

# Assign Static IP Address

In some cases a static IP address is needed.  An IP address is like your house
address and tells the host computer where to look for your Raspberry Pi on the
network.  By default Raspbian is setup to receive a dynamic IP via dynamic host
control protocol (DHCP) usually by your home router.  However this dynamic IP
address can change whenever your remove the Raspberry Pi from the network or
turn it off.  Having a static IP is not essential but it will make  repeated
access to the Raspberry Pi via secure shell (SSH) much simpler since the
Raspberry Pi will always have the same address.  The configuration changes
have to be made to a file `/etc/network/interfaces`.  By default 
`/etc/network/interfaces` looks like the following:

```bash
auto lo

iface lo inet loopback
iface eth0 inet dhcp

allow-hotplug wlan0
iface wlan0 inet manual
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp
```

The line `iface eht0 inet dhcp` implies that the system is currently configured
to receive an IP address with DHCP.  Before we change the network interface
configuration file one must have a good understanding of the network the
Raspberry Pi is using.  Use the command `ifconfig` to see the current 
network configuration supplied by DHCP.  The output should look like the 
following:

```bash
rovitotv@mail:~$ ifconfig
eth0      Link encap:Ethernet  HWaddr b8:27:eb:83:ce:6b  
          inet addr:192.168.1.92  Bcast:192.168.1.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:887 errors:0 dropped:0 overruns:0 frame:0
          TX packets:888 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:87514 (85.4 KiB)  TX bytes:121447 (118.6 KiB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:194 errors:0 dropped:0 overruns:0 frame:0
          TX packets:194 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:15751 (15.3 KiB)  TX bytes:15751 (15.3 KiB)

```

This depicts your network configuration, the part you want is after eth0

```bash
eth0      Link encap:Ethernet  HWaddr b8:27:eb:83:ce:6b  
          inet addr:192.168.1.92  Bcast:192.168.1.255  Mask:255.255.255.0
```

The three most important variables are

* inet addr: 192.168.1.92
* Bcast: 192.168.1.255
* Mask: 255.255.255.0

A gateway address which is usually the IP address of your router might also
be required.  Finally edit the configuration file `/etc/network/interfaces`
so it resembles the following:

```bash
rovitotv@mail:/tmp$ cat /etc/network/interfaces
auto lo

iface lo inet loopback
iface eth0 inet static
address 192.168.1.9
netmask 255.255.255.0
network 192.168.1.0
broadcast 192.168.1.255

allow-hotplug wlan0
iface wlan0 inet manual
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp
```

Next reboot the Raspberry Pi and the IP address will be statically assigned
to 192.168.1.9.  






