# Maintenance

Maintenance is an important part of having a computer on the internet.  As a 
operator/owner it is critical you take care of your Raspberry Pi or it
could become hacked and data loss will occur.  

## Backups

A regular schedule for backing up your Raspberry Pi will insure that if 
hardware failure or hacking occurs then your precious data can be recovered.  
Based on my personal experience data needs to be in multiple locations because
hardware failure in two computers at the same time is highly unlikely.

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

Media that you upload into Wordpress to use in your blog posts is stored in
'/var/www/wp-content/uploads' by year and month.  To backup this directory 
use the following command:

```bash
cd ~
zip -r 20150221WordPressContentUploads.zip /var/www/wp-content/uploads
```

Same idea with the backup file name by using the year-month-day the backup
files will automatically sort in almost any directory listing.  Now use scp
to copy this zip file to a different computer for safe keeping.

## Rasbian updates

Operating systems are complex pieces of software therefore they will need to
be updated and patched on a frequent basis.    