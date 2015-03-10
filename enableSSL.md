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

## Filename Extensions

To stay organized we will use the following conventions for extensions of
file names.  Linux doesn't care about file name extensions as much as Windows
does but by using the same extension it will help us stay organized and
easier to follow.  

* **.csr** for the certificate signing request (CSR)
* **.crt** for the signed certificate file
* **.key** for the key file