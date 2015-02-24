# Setup

## Hardware

I highly recommend the Raspberry PI 2 because it is the same price as the
Raspberry PI model B but has four cores and 1 GB of RAM.  Same price but six
times the performance with double the RAM not many down sides to the Raspberry
PI 2.  Yes a Raspberry PI model B will work with this book but it will be slow.
As far as flash cards I use a class 10 that is 16 GB of size.

## Operating System

This book uses Raspbian operating system which is the "official" operating 
system for the Raspberry PI.  It is based on Debian Linux "Wheezy" and includes
many packages that will make digital freedom easy obtainable.  

## NOOBS


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


