SSLstrip+
========

This is just a mirror of the original SSLstrip+ code by Leonardo Nve, which had to be taken down because of a gag order.

**For this to work you also need a DNS server that reverses the changes made by the proxy, you can find it at https://github.com/singe/dns2proxy**

Description
===========

This is a new version of [Moxie´s SSLstrip] (http://www.thoughtcrime.org/software/sslstrip/) with the new feature to avoid HTTP Strict Transport Security (HSTS) protection mechanism.  
  
This version changes HTTPS to HTTP as the original one plus the hostname at html code to avoid HSTS. Check my slides at BlackHat ASIA 2014 [OFFENSIVE: EXPLOITING DNS SERVERS CHANGES] (http://www.slideshare.net/Fatuo__/offensive-exploiting-dns-servers-changes-blackhat-asia-2014) for more information.  

Demo video at: http://www.youtube.com/watch?v=uGBjxfizy48
