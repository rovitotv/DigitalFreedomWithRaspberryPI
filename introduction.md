# Introduction

The digital revolution and especially the development of the personal computer
was all about enabling users by giving us a computer on our desk.  I have found
the last few years disturbing as people migrated to on-line commercial driven
enterprises to manage email (yahoo mail, gmail, hotmail), our files (dropbox,
box), and social (Facebook, Twitter).  Admittedly I have used the services above
especially gmail but the advent of advertisements following me around the web
based on the email in my gmail account has become the final straw.  Besides I am
a Computer Scientist so shouldn't I manage my own email, blog, and file syncing
service?  As a self proclaimed geek I need to  stop being lazy.  While these
services mentioned above are convenient each user pays a price in privacy and
control.  Computer hardware has never been cheaper especially with products like
the Raspberry Pi ($35).  Sure you have to add a power supply ($5) and flash card
($25), for a total one time cost of $65.   Then each year I recommend a domain
name ($15) and a official SSL certificate ($9.99).  The first year of operation
will cost $7.49 a month while additional years of operation will cost $2.08 a
month.  A small price to pay for your digital freedom.  In addition reading this
guide and learning how email, blog, and other services work is educational and
fun.  I don't believe that a computer geek should never use popular services
such as Twitter and Facebook, a savvy computer geek will figure out how to use
the  popularity of these services and mix with her own tools.  A mix of Twitter
and Facebook along with a personal blog has the benefit of catching some of
socials popularity plus it means content will be stored on a Raspberry Pi for
safe keeping.

This guide will step you through the process of setting up a personal blog and
email server.  It will also provide a number of Python scripts for testing and
automatic install of a blog and email server if you don't want to go through the
configuration.

## What you will have at the end of this guide

If you follow this guide carefully you will end up with the following:

1. A WordPress blog/email server that can run 24/7/365 for under $5 of 
electricity per year.  The operating costs are very low $2.08 a month after
the first year to pay for the $65 in hardware costs.
2. Personal domain that supports both email and web for example rovitotv.org.
3. The ability to connect to the Raspberry Pi from anywhere to post a blog
entry or read/send email using a secure IMAP connection on your phone, tablet,
or computer.
4. Complete control over your personal communication.  Your emails and blog will
be stored on YOUR Raspberry Pi mini server, and nobody is scanning them to sell
you advertisements.  
5. Ability to customize your blog with themes or plug-ins and ability to control
your email with custom sorting and marking.  


## Rules of Engagement

This guide will refer you to other sources of documentation especially hardware
and network setup.  As time permits I may add suggestions on hardware and
network setup.

## Prerequisites

### The Command Line

A guide like this requires extensive knowledge of the Linux command line.  The
fact is Linux is based on Unix and Unix (therefore by extension Linux) needs to
be operated from the command line.  The Linux command line is extremely powerful
and if you have never used the command line before and you spend the time to
learn it you will come to appreciate its power and simplicity.  Teaching readers
the command line is beyond the scope of this guide but I will point you to an
excellent free reference called  [The Linux Command
Line](http://linuxcommand.org/tlcl.php).  I highly recommend `The Linux Command
Line` but it is an in-depth book if you read chapters 1 - 10 that should cover
most of the ground you need to understand to complete this guide.  The skills
you learn in this guide and the book `The Linux Command Line` will serve you
well in using a computer.


### A Text Editor

After the command line the next thing to master as a prerequisite to this book
is a text editor.  A text editor is used to edit configuration files which are
prevalent in Linux systems. The Raspberry Pi Operating System Raspbian includes
nano which is a good editor to get started but any self respected Linux geek
will use vi.  Some people might recommend emacs.  Both vi and emacs are 
powerful editors that once again will serve you well not only for this guide
but mastering computers.  `The Linux Command Line` book recommended above
also includes a chapter on vi, see chapter 12.  