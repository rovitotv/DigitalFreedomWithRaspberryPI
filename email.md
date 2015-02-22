# Email

The Raspberry Pi is an ideal choice for a home email server as it is small,
quiet, and consumes a small amount of power.  Linux supports a large number of
email software packages, it can be confusing to try to figure out where to 
start.  After experimenting with several different combinations I settled on
using Postfix, Dovecot, Spamassassin, and Sieve.  Some people like web mail
and might want to look into Squirrelmail, if time permits I might add a 
Squirrelmail section to this guide.  

# Postfix

Postfix is a Mail Transfer Agent (MTA) which is the program that lets you
send and receive email using a Internet protocol called Simple Mail Transfer
Protocol (SMTP).  Email servers across the Internet use SMTP on port 25 to
communicate with each other, you the user must employ IMAP (on port 143 
or 993), or POP (on port 110 or 995) to process email.  As is almost always
the case with Unix separate programs are used to accomplish a small task and
do that small task well.  

## Postfix Setup

To install Postfix first login to the Raspberry Pi using SSH then execute the
following commands:

```bash
sudo apt-get update
sudo apt-get install postfix
```
Almost immediately after installing Postfix a text based GUI menu will appear
with some options.  Select the second option "Internet Site" and then set
the mail name to be your domain name.  For example my domain name is 
rovitotv.org so I use rovitotv.org, leave off the www or any other host
names.  The setup script for Postfix will do configuration for you and you will
see a long list of output but at some point you will receive the following 
warning:

```bash
postmulti: warning: inet_protocols: disabling IPv6 name/address support: Address family not supported by protocol
```

Don't panic this is normal.  IPv6 is a new type of IP address that was created
to remedy the problem of all the IPv4 addresses being allocated but very few
Internet Service Providers support IPv6.  To fix this problem we can specify 
that Postfix only used the IPv4 protocol in the Postfix configuration file. 
Postfix has two configuration files main.cf, which specifies typical 
configuration options, and master.cf, which specifies the services Postfix
will run.  Edit the file `/etc/postfix/main.cf` with your favorite editor with
the command:

```bash
sudo nano /etc/postfix/main.cf
```

Then add the line `inet_protocols = ipv4` to the end of the main.cf file.  Check
the variable `myhostname` in the configuration file main.cf and make sure the
host name is your fully qualified domain name.  It is important to have the 
correct host name because your server will use this host name to talk to other
email servers, and some will reject your emails if you don't use a fully
qualified domain name.  For example my domain name is rovitotv.org and I like to
use the host name of `mail` for all email activities so my `myhostname` line
in main.cf is `myhostname = mail.rovitotv.org`.  Now restart Postfix and you
shouldn't see the IPv6 warning any more:

```bash
sudo service postfix restart
```

## Mailbox Setup

This guide will use "Maildir" configuration which places a Maildir directory
in each users home directory where the email will be stored.  To tell Postfix
to use the Maildir format, add the following lines to `/etc/postfix/main.cf`:

```bash
home_mailbox = Maildir/
mailbox_command =
```

When a new user account is added to the Raspberry Pi we want a Maildir to
be added to the new user's home directory along with common email 
sub-directories for drafts, sent, spam, trash, etc.  To accomplish this we
need to modify Raspbian's "skeleton" used to create a new user's home directory,
commands to do this are included with Dovecot (IMAP server) so we will install
Dovecot now with the following commands:

```bash
sudo apt-get update
sudo apt-get install dovecot-common dovecot-imapd
```
Once again this will produce a large amount of output: other Dovecot packages
will be installed and the configuration files will be created.  You will see
errors - don't panic we will fix those errors in later sections.  After 
Dovecot is installed use the following commands to create the "skeleton" 
mail folders:

```bash
sudo maildirmake.dovecot /etc/skel/Maildir
sudo maildirmake.dovecot /etc/skel/Maildir/.Drafts
sudo maildirmake.dovecot /etc/skel/Maildir/.Sent
sudo maildirmake.dovecot /etc/skel/Maildir/.Spam
sudo maildirmake.dovecot /etc/skel/Maildir/.Trash
sudo maildirmake.dovecot /etc/skel/Maildir/.Templates
```
Next add new users that will be using the email system on your Raspberry Pi by
using the command `sudo adduser USER`.  Replace USER with the user name you
are doing this for, and repeat for each user.  

## Access Restrictions

SMTP servers like Postfix can be used by spammers to send out massive amounts
of spam if they are not configured correctly.  A few access restrictions can
make a huge difference and lower the probability of your Raspberry Pi to be
used for spamming. 

Add the following to `/etc/postfix/main.cf` to restrict who can send emails
to external mail servers:

```bash
smtpd_recipient_restrictions =
        permit_sasl_authenticated,
        reject_unauth_destination
```

Next restart Postfix so the configuration reloads:

```bash
sudo service postfix reload
```

The SMTP protocol starts with a 'Helo' command when one SMTP server is 
speaking to another SMTP server, hence 'Helo' restrictions can be useful way of
blocking spam.  Add the following to `/etc/postfix/main.cf`:

```bash
smtpd_helo_required = yes
smtpd_helo_restrictions =
        permit_mynetworks,
        permit_sasl_authenticated,
        reject_invalid_helo_hostname,
        reject_non_fqdn_helo_hostname,
        reject_unknown_helo_hostname
     	check_helo_access hash:/etc/postfix/helo_access
```
The last restriction added with the last line checks a file for custom rules
you are going to build into the list of restrictions.  Edit the file
`/etc/postfix/helo_access` and add the following lines:

```bash
rovitotv.org       REJECT     Get lost - you're lying about who you are
www.rovitotv.org   REJECT     Get lost - you're lying about who you are
mail.rovitotv.org  REJECT     Get lost - you're lying about who you are
```

Change rovitotv.org to your domain name.  Next tell Postfix to map the file
and then restart Postfix:

```bash
sudo postmap /etc/postfix/helo_access
sudo service postfix restart
```

With those changes made anyone who tries to `ehlo` with one of the host names
you defined in the file `/etc/postfix/helo_access` will get rejected, and sees
the "get lost" message.  The legitimate servers won't have that problem,
because they will already have been accepted higher up the list with
`permit_mynetworks`. 


Take note to understand in more detail what these access restrictions do please
see [samhobbs.co.uk](https://samhobbs.co.uk/2013/12/raspberry-pi-email-server-part-1-postfix).


# Dovecot

Dovecot is used for two things Internet Message Access Protocol (IMAP) 
functionality and it checks that you are who you say you are when using Simple Authentication and Security Layer (SASL)
before you send or fetch email.  IMAP is a protocol for email retrieval and 
storage, it will allow email clients (phone, tablet, computer, etc) to process
email.  

## Configuration

Earlier when we installed Dovecot several errors were reports in the SSH 
terminal which are once again caused by the lack of IPv6 support.  To remove
the errors, open the main Dovecot configuration file `/etc/dovecot/dovecot.conf`
and change the line `listen = *, ::` to:

```bash
listen = *
```

The `*` means "all IPv4 addresses", the `::` means "all IPv6 addresses".  Now
restart Dovecot and you should not get any errors:

```bash
sudo service dovecot restart
```

Next we need to configure Dovecot to know where the Mailbox is stored so open
`/etc/dovecot/conf.d/10-mail.conf` and find this line:

```bash
mail_location = mbox:~/mail:INBOX=/var/mail/%u
```

then change it to this line:

```bash
mail_location = maildir:~/Maildir
```

Postfix now needs to be configured to use Dovecot for SASL authentication. Open
`/etc/postfix/main.cf` and add these lines:

```bash
smtpd_sasl_type = dovecot
smtpd_sasl_path = private/auth
smtpd_sasl_auth_enable = yes
```

Dovecot needs to be configured to listed for SASL authentication requests from
Postfix.  Open `/etc/dovecot/conf.d/10-master.conf` and comment out the current
block that begines with `service auth` (place a # at the start of each line).
Replace is with this:

```bash
service auth {
        unix_listener /var/spool/postfix/private/auth {
                mode = 0660
                user = postfix
                group = postfix
        }
}
```

Next we want to configure Postfix to listen on port 465 for encrypted
connections.  The first step is telling Postfix to listen on port 465, so open
`/etc/postfix/master.cf` and uncomment the smtps line plus two lines below then
add a new smtpd_recipient_restrictions line.  The configuration file should
match the lines listed below:

```bash
smtps     inet  n       -       -       -       -       smtpd
  -o syslog_name=postfix/smtps
  -o smtpd_tls_wrappermode=yes
  -o smtpd_recipient_restrictions=permit_sasl_authenticated,reject  
```

Then we want to configure Postfix to only advertise SASL authentication over
encrypted connections so you don't accidentally send your password in the 
clear.  Open `/etc/postfix/main.cf` and add this line:

```bash
smtpd_tls_auth_only = yes
```

Now restart Postfix with the following commands:

```bash
sudo service postfix restart
```

Next we need to enable IMAPS (imap with SSL/TLS), the standard port for this
is 993.  Edit `/etc/dovecot/conf.d/10-master.conf`, find the "service imap-login"
block and uncomment the post and SSL lines to that it looks like this:

```bash
service imap-login {
  inet_listener imap {
    port = 143
  } 
  inet_listener imaps {
    port = 993
    ssl = yes
  }

  # Number of connections to handle before starting a new process. Typically
  # the only useful values are 0 (unlimited) or 1. 1 is more secure, but 0
  # is faster. 
  #service_count = 1

  # Number of processes to always keep waiting for more connections.
  #process_min_avail = 0

  # If you set service_count=0, you probably need to grow this.
  #vsz_limit = $default_vsz_limit
}
```

Now restart Dovecot with the following commands:

```bash
sudo service dovecot restart
```
At this point the configuration for Postfix and Dovecot are complete.  The
two systems will work to process email but they are not using ideal SSL 
certificates nor is Spamassassin setup yet.  Don't open up your firewall 
ports just yet lets setup Spamassassin next.  

Take note to understand in more detail Dovecot setup please
see [samhobbs.co.uk](https://samhobbs.co.uk/2013/12/raspberry-pi-email-server-part-2-dovecot).

# SpamAssassin

SpamAssassin uses a variety of spam-detection techniques, that includes 
DNS-based and fuzzy checksum based spam detection, Bayesian filtering,
external programs, blacklists and online databases.  In this section we will
integrate SpamAssassin with Postfix to automatically filter all mail coming
into the Raspberry Pi.  A user can use IMAP to drop messages into the Spam 
folder and SpamAssassin will learn overtime what a user considers Spam or Ham.
Ham is the opposite of Spam and is good email that a user wants to see.  It is
rare but sometimes SpamAssassin will make mistakes so you should from time to
time check your Spam folder.  

## Install and Configure SpamAssassin

The first step is to obviously install SpamAssassin:

```bash
sudo apt-get update
sudo apt-get install spamassassin
```

To configure SpamAssassin we need to edit the values in the file
`/etc/spamassasin/local.cf`.  In some cases some of these configuration
variables might already be set in which case you can leave them as they are,
or change them as you see fit. Some of the variables just need to be
uncommented so they will work.

The variable rewrite_header will add the spam score to the subject line of
the emails that SpamAssassin considers to be spam:

```bash
rewrite_header Subject [***** SPAM _SCORE_ *****]
```

Obviously the higher the _SCORE_ the higher probability that SpamAssassin
believes the email is spam.  SpamAssassin will also flag spam emails with
"X-Spam-Flag: YES" in the email headers. The flag "X-Spam-Flag" will be
used to sort emails, the rewritten subject line is to make it easier to
see the score.

This next setting will tell SpamAssassin to modify headers only, without
making any changes to the body of the email:

```bash
report_safe 0
```

The variable `required_score` determines what the minimum score should be for
a email to be considered spam, the default is 5 but you might have to adjust
this score depending on if you get a number of false positives.  

```bash
required_score 5.0
```
The variable `use_bayes` determines if SpamAssassin will use Bayesian filtering
or not.  Bayesian filtering is the algorithm that SpamAssassin uses to 
'learn' a user's determination if an email is spam or ham.  

```bash
use_bayes 1
```

Turn on `bayes_auto_learn` to enable the Bayesian classifier auto-learning.

```bash
bayes_auto_learn 1
```

Save your modifications of the configuration file `/etc/spamassassin/local.cf`
and edit the configuration file `/etc/default/spamassassin` to set:

```bash
ENABLED=1
```

Then start the SpamAssassin daemon:

```bash
sudo service spamassassin start
```

## Configure Postfix to use SpamAssassin




# LMTP & Sieve mailbox sorting




# References

- [Debian Mail Server with Postfix and Dovecot](https://scaron.info/technology/debian-mail-postfix-dovecot.html)
- [Raspberry Pi Email Server](https://samhobbs.co.uk/raspberry-pi-email-server)