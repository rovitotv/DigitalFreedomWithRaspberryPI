# Web

Having your own personal web server offers many freedoms like a blog and
webmail.  In this section you will install the Apache webserver and [Pelican
static site generator software](http://blog.getpelican.com).  The main digital
freedom offered here is that you can post a blog post and not have your readers
have to suffer through advertisements.  Not only will your blog be advertisement
free but you will have massive amounts of storage space and no file limits for
media files.  The only file size limitation you will have is based on how much
storage space you can install on your Raspberry Pi.

Why Pelican static site generator software over WordPress or Drupal? Pelican 
takes Markdown or restructured text documents and converts them to HTML.  In
addition it automatically creates links for categorizes and places those
links on each page.  The reasons why we switched to Pelican are:

- Security is improved because all of the web content is static so no place
to inject malicious code like within the MySQL database for instance.
- Easier to setup and maintain.  We are installing less software so it 
takes fewer steps. Maintenance is improved because your web site will be 
a group of text files so no databases to backup.  
- Faster less software running on the Raspberry PI makes the performance much
faster.  

## Apache Web Server

Apache is a popular open source web server that offers much flexibility and
excellent documentation.  As of June 2013 it is estimated that Apache serve 54%
of all active web sites.  On its own, Apache can serve HTML files over HTTP, and
with additional modules can serve dynamic web pages using scripting languages
such as PHP.  Apache is easy to install by typing in the  following command:

```bash
sudo apt-get install apache2 -y
```

### Testing the web server

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

## Pelican

The Pelican software is written in [Python](http://python.org) a most excellent
scripting language!!!  To install Pelican we use pip which is a tool for
installing and managing Python packages.  

```bash
sudo pip install pelican markdown
```




# Conclusion

Now you have your own website and control the content.  Have fun blogging see
the WordPress site for more instructions on how to use 
[wordpress.org](http://codex.wordpress.org/WordPress_Lessons).









