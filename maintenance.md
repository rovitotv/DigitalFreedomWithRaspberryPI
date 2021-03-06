# Maintenance

Maintenance is an important part of having a computer on the internet.  As a 
operator/owner it is critical you take care of your Raspberry Pi or it
could become hacked and data loss will occur.  

## Backups

A regular schedule for backing up your Raspberry Pi will insure that if 
hardware failure or hacking occurs then your precious data can be recovered.  
Based on my personal experience data needs to be in multiple locations because
hardware failure in two computers at the same time is highly unlikely. The
Raspberry Pi uses a SD flash card which are volatile and will deteriorate over
time.  Some people have setup the Raspberry Pi to boot off of a external
hard disk or USB thumb drive to minimize wear and tear on the SD flash card,
but I have found that setup complicated so my solution is to perform backups
often.  

### Backup WordPress

As you know from the installation WordPress uses a MySQL database to store
comments, posts, and user information.  This database can be backup up to a
file on the Raspberry Pi with the following command:

```bash
mysqldump --add-drop-table -h localhost -u root -p wordpress | bzip2 -c > 20150221WordPress.bak.sql.bz2
```

The command above will perform a "dump" of the "wordpress" database then 
compress that information with bzip2 and save to a file name of 
20150221WordPress.bak.sql.bz2.  I like to use the year-month-day in my backup
name so I can keep a history just in case.  This file will be pretty small
depending on how many posts on your blog you actually have.  Use scp (secure
copy) to copy the file from the Raspberry Pi to a location for safe keeping.

Media that you upload into WordPress to use in your blog posts is stored in
'/var/www/wp-content/uploads' by year and month.  We want to make a zip archive
of all the files in this directory so first we have to install the zip
utility by using the command:

```bash
sudo apt-get install zip
```

To backup the WordPress content directory use the following command:

```bash
cd ~
zip -r 20150221WordPressContentUploads.zip /var/www/wp-content/uploads
```

Same idea with the backup file name by using the year-month-day the backup
files will automatically sort in almost any directory listing.  Now use scp
to copy this zip file to a different computer for safe keeping.

### Automatic Backups

Included with this guide in the [script directory](https://github.com/rovitotv/DigitalFreedomWithRaspberryPI/blob/master/Scripts/backup.py) is
a Python script that will automatically backup your WordPress database and 
uploaded content called `backup.py` which has the following
command line options:

```bash
usage: backup.py [-h] -b BACKUPDIRECTORY -p PASSWORDMYSQL

optional arguments:
  -h, --help            show this help message and exit
  -b BACKUPDIRECTORY, --backupDirectory BACKUPDIRECTORY
                        path to backup dir
  -p PASSWORDMYSQL, --passwordMySQL PASSWORDMYSQL
                        MySQL password
```

The backup script is simple, feel free to have a look at the code.  It will
create a directory with the current date and place all the backup files in 
that directory.  The script follows a similar backup procedure as above and
is called based on the following example:

```bash
sudo python backup.py -b /media/usbhd/backups -p PASSWORD
```

Of course you have to replace `PASSWORD` with your MySQL password.  Check the
files in the backup directory to make sure the script is working properly.  

## Raspbian updates

Operating systems are complex pieces of software therefore they will need to
be updated and patched on a frequent basis.  The Raspbian commands to perform
updates are:

```bash
sudo apt-get update
sudo apt-get upgrade
sudo rpi-update
sudo reboot
```

Once you have your Raspberry Pi system up and running you should consider
subscribing to the [debian-security-announce emai list](https://lists.debian.org/debian-security-announce/).  This is a low volume email list that will show securtiy
ammouncements for Debian which is the basis for Raspbian.  Most security 
problems can be traced to unpatched computers so please update and upgrade 
often to keep your Raspberry Pi running in good shape.  Performance improvements
are being commited to Raspbian all the time and one of the best ways to get
these performance updates is by the commands listed above.  

