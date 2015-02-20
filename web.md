# Web

Having your own personal web server offers many freedoms like a blog and
webmail.  In this section you will install the Apache webserver, MySQL database,
PHP (a web scripting language), and finally Wordpress blogging software.  The
main digital freedom offered here is that you can post a blog post and not
have your readers have to suffer through advertisments.  Not only will your
blog be advertisment free but you will have massive amounts of storage space
and no file limits for media files.  The only file size limitation you will
have is based on how much storage space you can install on your Raspberry PI.

## Apache Web Server

Apache is a popular open source web server that offers much flexiblity and
excellent documentation.  As of June 2013 it is estimated that Apache serve 54%
of all active web sites.  On its own, Apache can serve HTML files over HTTP, and
with additional modules can serve dynamic web pages using scripting languages
such as PHP.  Apache is easy to install by typing in the  following command:

```bash
sudo apt-get install apache2 -y
```

```bash
sudo apt-get update
sudo apt-get upgrade
sudo rpi-update
```

## Testing the web server

By default, Apache puts a test HTML file in the web folder.  This default web
page is served when you browse to 'http://192.168.1.26' (or whatever your PI's
IP address is) from another computer on the network.  To find the PI's IP
address, type `hostname -I` at the command line. Find out more about your
PI's IP address see 
[IP Address](https://github.com/raspberrypi/documentation/blob/master/troubleshooting/hardware/networking/ip-address.md).

https://github.com/raspberrypi/documentation/blob/master/troubleshooting/hardware/networking/ip-address.md

Browse to the
default web page from another computer on the network and you should see
the following:

![Apache success message](images/apache-it-works.png)

This means you have Apache working!

## Install PHP

PHP is a server-side scripting language designed for web development with
a very large install base.  Most "web apps" are created with PHP.  Latter on
we will install WordPress which uses PHP.  To allow your Apache server to
process PHP files, you'll need to isntall PHP5 and PHP5 module for Apache.
Type the following command to install these:

```bash
sudo apt-get install php5 libapache2-mod-php5 -y
```

## Test PHP

To test PHP we will create a dynamic web page then refresh in our browser and
watch the time change.  First use this command to remove the default web page:

```bash
sudo rm /var/www/index.html
```

Then use the nano text editor to create a new index file which will be called
index.php.

```bash
sudo nano /var/www/index.php
```

Simply copy and paste the following PHP code 

```php
<?php echo date('Y-m-d H:i:s');
```

Into the Nano text editor then exit with control-x.  An attempt to exit will
force  Nano to offer to save the file which you should select 'Y' for yes.  Now
browse to the default web page by going to 'http://192.168.1.26' (or whatever
your Pi's IP address is) from another computer on the network.  If you reload
the page you will notice that if PHP is installed correctly the date/time will
be updated.







