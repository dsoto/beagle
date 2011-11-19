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
# this was key to getting easy_install to run
opkg install python-dev --force-overwrite
easy_install requests
opkg install git
opkg install emacs
