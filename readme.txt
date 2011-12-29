this is a repo with various files related to getting a
beagle board up and running and sending out a datastream
to the pachube servers.

pachube configuration:
drdrsoto@gmail.com mbpb

https://pachube.com/feeds/39985

api key - yKcC6HugqvNtshxI6qEreOPYs9qQG7gZfloc3JQWPbQ


package installations performed:
opkg update
opkg upgrade
opkg install bash
opkg install python
opkg install python-modules
opkg install python-setuptools
opkg install python-pyserial
# this was key to getting easy_install to run
opkg install python-dev --force-overwrite
easy_install requests
easy_install twiggy
opkg install git
opkg install emacs


beaglebone notes
----------------

192.168.1.36

to set date:
> date +%Y%m%d%H%M -s "201112251148"

to restart network services, often necessary on usb/serial disconnection
> /etc/init.d/networking restart

problems
--------
screen doesn't work for keeping process going after ssh logout
currently cannot install emacs
cannot get git pull working with ssh keys
sometimes modem will not register when being plugged in after disconnection

opkg
----
i backed up a feed file and the new one points at eufeeds for the python
distribution to get some packages working.

installed new ftdi drivers from beagle page and now can connect over usb

i am sending out exactly the same string from a python interpreter
on my laptop and on the beagle and on the mac, i'm getting success
while on the beagle it has never posted to the website.

there is something going on with the serial output, but i don't know
how to sniff that output...maybe pipe it into an arduino?

this string works from my macbook after making a socket
string = 'POST /service/currentvalue HTTP/1.1\r\nHost: app.nimbits.com\r\nContent-Length: 101\r\nContent-Type: application/x-www-form-urlencoded\r\nAccept-Encoding: identity\r\nAccept: */*\r\nUser-Agent: pysoto\r\n\r\nsecret=01787ade-c6d6-4f9b-8b86-20850af010d9&email=drdrsoto%40gmail.com&value=19&point=603_Test_Stream'

problem may have to do with 'babble interrupt'

if i try to send 128 characters, it barfs.  so, try to break string into
smaller bits and send out bits with delays...but, i'm not sure if this
is due to the beagle or the arduino receiver.  either way, i suppose
it is worth trying.

12/25/11 2:41 PM
trying to send serial strings over ftdi -> arduino to laptop.  seems
to be working, will try with modem.

12/25/11 2:56 PM
i am now able to send posts to nimbits over gprs.  still saw what i think
was a 'babble' failure in about 1 of 10 tries.

next step is to put this in a loop and

github
------
beaglebone angstrom comes with dropbear installed which didn't work

opkg install openssh
now github pull is working after copying over my public and private keys

to get uno mounted:
opkg install kernel-module-cdc-acm
/dev/ttyACM0

to get ftdi arduino mounted
opkg install kernel-module-ftdi-sio


12/27/11 6:42 PM

beaglebone 2 install (BB_02)

making sd card didn't work

trying the card that came with beaglebone in linux sdk box
but it hangs during boot

card labeled 11-16-11 comes up with
Angstrom v2011.10-core - Kernel 3.1.0+

/sys/devices/platform/tsc does not exist (but does on first beaglebone)

12/27/11 6:56 PM
hooked up to router
192.168.1.26 was assigned
ssh in and
opkg update; opkg upgrade
12/27/11 7:49 PM
wow, the upgrade might take hours...
upgrade did take a few hours but the ain ports didn't work afterward

12/27/11 10:03 PM
i've taken the sd card (kingston 2GB) from BB_01 and plugged it in
and it boots in BB_02.
Angstrom v2011.12-core - Kernel 3.1.0+
plugging in to ubuntu a boot partition with MLO and u-boot.img come up
and a Angstrom partition with the filesystem

12/27/11 10:20 PM
lots of cards don't boot now.  i'm having paranoid thoughts of
"what if booting with the 2011.12-core has written something
in NAND or something that isn't compatible with older versions?


12/28/11 12:25 AM
good card md5
dsoto@ubuntu:/media/boot$ md5sum *
f27d79e6a72ee4c6b29c1b59d5557b42  MLO
32cf3646e7f4fdf2cf85526d525cedc4  u-boot.img
these good ones don't match the website md5sums
they do match the google cached site from 19 dec 2011


bad card md5
dsoto@ubuntu:/media/boot$ md5sum *
d466bbf066be009fdf25badd49d099a5  MLO
cd991c3a9b2cbaadac9ee8b57cce878a  u-boot.img
these do match the website (today 28 dec 2011)

so, they ARE different.  whats up with that?

12/28/11 12:34 AM
i copied the good MLO and u-boot.img from the good card (now labeled G)
to the other card and now it boots.
Angstrom v2011.10-core - Kernel 3.1.0+
(still no ain* ports)
was not able to ssh into machine (connection refused)
will try update

12/28/11 2:08 AM
LetoThe2nd suggests (nohup screen &) to get a "kind-of" detached screen


12/28/11 3:01 PM
screen
python gprs_post.py &
exit
kills process

nohup screen &
doesn't start a screen session or create a socket visible in screen -list

nohup python gprs_post.py &
creates process but is killed on logout

ok, this might have worked.  start a screen session through the usb
that will then be persistent.  ssh in and attach to that screen.
is working for now...

