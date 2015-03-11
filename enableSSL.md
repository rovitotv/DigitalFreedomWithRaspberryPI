# Enable SSL

Secure Socket Layer (SSL) is a cryptographic protocol designed to provide
communications security over a computer network. SSL uses X.509 certificates
to authenticate the counterparty with whom they are communicating.  This is
also called public/privte key encryption. SSL is the same technology that
banks, government agencies, Amazon, and Apple use to protect web sites and
encrypt passwords between a client and a web site.  If you plan on using
your Raspberry Pi's WordPress dashboard or Own Cloud I highly recommend that
you enable SSL.  By using CACert the certificates are free but they might
require that a user download the certificates and install in the browser.  

# Filename Extensions

To stay organized we will use the following conventions for extensions of
file names.  Linux doesn't care about file name extensions as much as Windows
does but by using the same extension it will help us stay organized and
easier to follow.  

* **.csr** for the certificate signing request (CSR)
* **.crt** for the signed certificate file
* **.key** for the key file

# Generate your certificate

First ssh into your Raspberry Pi, these commands must be performed on the
Raspberry Pi.  The instructions below use a two step process to generate
your certificate.  Second generate your private key with the following command:

```bash
openssl genrsa -out <filename for your private key>.key 4096
```

Replace the varialbe `<filename for your private key>.key` with 
`domain_name.key`, so for example with my domain `rovitotv.key`
is the name I used.  To create a private key of 4,096 bits takes some time so
be patient.  Next generate a new certificate signing request (CSR) which
uses the private key you generated above.  Use the commend below to 
generate a new CSR:

```bash
openssl req -new -key <filename for your private key>.key -out <filename for the CSR>.csr
```

Use the same convention by using your domain name for the file names.  For my
domain of rovitotv.org I used the command 
`openssl req -new -key rovitotv.key -out rovitotv.csr`.  After the 
command is entered some user input must be provided.  Here is a list of 
information you will be asked for:

* Country Name (use a two letter code e.g. US)
* State or Province Name (e.g. Ohio)
* Locality Name (e.g. Middletown)
* Organization Name (e.g. company Todd Rovito's Personal Website)
* Organizational Unit Name (e.g. Website)
* Common Name (your FQDN e.g. www.rovitotv.org)
* Email Address (email must be valid e.g. webmaster@rovitotv.org)

** Don't set a password - leave it blank when asked.  The key will be protected
by setting the appropriate permissions. **

# Install the CAcert root certificate into your browser

Using the browser on another computer connect to cacert.org.  Most likely you
will receive an error, this is because CACert's root certificate is not
published with web browsers by default.  When the browser presents an error
you need to trust the certificate or web site then you can proceed with this
guide.  Hopefully in the future CACert will be published with all web
browsers.  Directions on how to import the CACert's root certificate are
included for several operating systems and web browser's on 
[CACert's wiki page](http://wiki.cacert.org/FAQ/ImportRootCert?action=show&redirect=ImportRootCert)


# Required Email Address

CAcert has a robot verification process which verifies that you own the
domain it is signing a certificate for by sending a verification link to
one of the following email addresses:

* root@yourdomain.com
* webmaster@yourdomain.com
* postmaster@yourdomain.com

Hopefully you followed this guide and setup your own email server, in which
case you just have to setup a few email aliases on your server.  Setting up
an alias is easier than setting up three different unique email accounts.
On your Raspberry Pi email server edit the file `/etc/aliases` and add:

```bash
postmaster: yourusername
webmaster: yourusername
root: yourusername
```

Next run the command to load the new aliases:

```bash
sudo newaliases
```

Finally reload postfix to force the alias change to take effect.

```bash
sudo service postfix reload
```

# Send the Certificate Signing Request to CAcert

First on a computer with a web browser go to the [CACert website](https://cacert.org)
and create an account:

Please note that CACert has signed its own SSL certificate so your browser may
throw and error if you haven't imported the root cert yet.

After you have created your account and loggin in, navigate to 
**server certificates -> new**.  This will start the process to upload the
csr file to CAcert so they can sign a valid certificate.  On the Raspberry Pi
use the following command to output the Certificate Signing Request (CSR) file
that you created above and then copy & paste it into the CSR box:

```bash
cat <filename for the CSR>.csr
```

and then click submit.  Clicking submit will generate a email and will now
show the server certificate in the browser.  Now copy and paste the server
certificate into a file with nano or transfer from your email client.

```bash
nano <path to your cert>.crt
```

For the path again use the convention of your domain name, for example my
CRT file is `rovitotv.crt`.  Recall the CRT file is the official signed 
certificate file.

**NOTE: the BEGIN CERTIFICATE and END CERTIFICATE lines are part of the 
certificate.**

# Certificate file locations, permissions, and owernship

The certificates must be in the proper location and have the right file
permissions or the SSL system will not function.  At this point all three
files should be in your home directory on the Raspberry Pi.  Please set
the permissions to be read/write/execute for user only by using the command:

```bash
chmod 600 domain.*
```

Replace domain with your domain name.  The key file is the private key so it
must be protected and only the root user should be able to read it.  Next copy 
your key file to the proper directory and set the correct owner and permission:

```bash
sudo cp ~/rovitotv.key /etc/ssl/private/rovitotv.key
sudo chown root:root /etc/ssl/private/rovitotv.key
sudo chmod 600 /etc/ssl/private/rovitotv.key
```

Most of the services that we have installed on the Raspberry Pi like Apache,
Postfix, and Dovecot, require root privileges to start up, but they quickly
drop to a normal user like www-data for Apache.  Hence the certificate file
needs to be readable by all users.  Unlike the key file your signed 
certificate file is not a secret, rather the opporsite the certificate file
is sent to each user when establishing a secure session.  But only the root
user can actually modify the CRT file.  Use the following
commands to copy your certificate file to the proper directory and set the
correct owner and permission:

```bash
sudo cp ~/rovitotv.crt /etc/ssl/certs/rovitotv.crt
sudo chown root:root /etc/ssl/certs/rovitotv.crt
sudo chmod 644 /etc/ssl/certs/rovitotv.crt
```

# Configuration for Apache and WordPress

To get the Apache web server to use SSL is straight forward.  First use the
following commands:

```bash
sudo a2enmod ssl
sudo a2ensite default-ssl
```

Then you have to edit the file `/etc/apache2/sites-available/default-ssl` and
change line 12 to `AllowOverride All`.  Next restart apache with the 
command:

```bash
sudo service apache2 restart
```

Then you want to add a parameter to the top of your default-ssl
Apache configuration file that will stop Apache using SSL version 3.  SSL
version 3 has a recently discovered vulnerability known as the 
[POODLE attack](https://community.qualys.com/blogs/securitylabs/2014/10/15/ssl-3-is-dead-killed-by-the-poodle-attack).  To turn it off simply add the parameter 
`SSLProtocol All -SSLv2 -SSLv3` to the file 
`/etc/apache2/sites-available/default-ssl` after the
`<VirtualHost _default_:443> tag.

At this point you should be able to use your browser and go to 
`https://www.yourdomain.com`.  Recall if you don't add the CACert to your
browser and or operating system you will get an error.  It is possible to force
all users to use https even if they initiate a http get request.  We recommend
forcing all users over to SSL by default.  Google 
[recently announced](http://googleonlinesecurity.blogspot.co.uk/2014/08/https-as-ranking-signal_6.html)
that content on https will be given a higher ranking than content with http. 
Forcing everybody to https is simple to do so we recommend it! Edit the default
Apache config file `/etc/apache2/sites-available/default` to look like the
example below:

```bash
<VirtualHost *:80>
ServerName www.rovitotv.org
<IfModule mod_rewrite.c>
  <IfModule mod_ssl.c>
    <Location />
      RewriteEngine on
      RewriteCond %{HTTPS} !^on$ [NC]
      RewriteRule . https://%{HTTP_HOST}%{REQUEST_URI}  [L]
    </Location>
  </IfModule>
</IfModule>
</VirtualHost>
```

The configuration information above uses the Apache module rewrite to rewrite
all incoming traffic to use https.  After the configuration file is changed
restart Apache with the command:

```bash
sudo service apache2 reload
```

The WordPress configuration has to be modified slightly to use https, so in
your browser go to the URL `https://www.YOURDOMAIN.org/wp-login.php` then
enter your credintials. Next go to the left side and select `Settings->General`
then change the WordPress Address (URL) and Site Address (URL) to include the
https prefix.  For example my values are `https://www.rovitotv.org`.  After 
those values are set hit the `Save Changes` button at the bottom of the screen.
Next modify the file `/var/www/wp-config.php` to include the configuration line
`define('FORCE_SSL_ADMIN', true);`.  This constant will force all logins and
all admin sessions to happen over SSL.

As a final check you should check the SSL capability of your web site by
using [Qualys SSL Labs tools](https://www.ssllabs.com/ssltest/index.html).


# References

- [SSL Certificate Signing with CACert for Raspberry Pi...](https://samhobbs.co.uk/2014/04/ssl-certificate-signing-cacert-raspberry-pi-ubuntu-debian?page=1)






