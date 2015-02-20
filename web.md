# Web

Having your own personal web server offers many freedoms like a blog and
webmail.  In this section you will install the Apache webserver, MySQL database,
PHP (a web scripting language), and finally Wordpress blogging software.  The
main digital freedom offered here is that you can post a blog post and not
have your readers have to suffer through advertisements.  Not only will your
blog be advertisement free but you will have massive amounts of storage space
and no file limits for media files.  The only file size limitation you will
have is based on how much storage space you can install on your Raspberry PI.

## Apache Web Server

Apache is a popular open source web server that offers much flexibility and
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
process PHP files, you'll need to install PHP5 and PHP5 module for Apache.
Type the following command to install these:

```bash
sudo apt-get install php5 libapache2-mod-php5 -y
```

## Testing PHP

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

into the Nano text editor then exit with control-x.  An attempt to exit will
force  Nano to offer to save the file which you should select 'Y' for yes.  Now
browse to the default web page by going to 'http://192.168.1.26' (or whatever
your Pi's IP address is) from another computer on the network.  If you reload
the page you will notice that if PHP is installed correctly the date/time will
be updated.

## MySQL

MySQL (pronounced My Sequel or My S-Q-L) is a popular database engine. A 
database offers an easy way to store and retrieve data in a standard way using
the language SQL (structured query language).  Install the MySQL server and
PHP-MySQL packages by entering the following command into the terminal:

```bash
sudo apt-get install mysql-server php5-mysql -y
```

When installing MySQL you will be asked for a root password. You'll need to 
remember this to allow your website to access the database.  MySQL is a large
install so be patient as the database system is installed.

## Test MySQL

MySQL should install just fine but I like to confirm critical pieces of 
software are functioning so let us test the MySQL setup.  During the install
you should of entered a password for the "root" MySQL user.  A username of
root indicates that user has administrator privileges so extra caution should
be used when using the root user for any system.  To test MySQL lets login to
the database with the following command:

```bash
mysql -u root -p
```

If you don't recieve any access denied messages then the database has been 
installed correctly.  







