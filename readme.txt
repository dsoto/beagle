this is a repo with various files related to getting a
beagle board up and running and sending out a datastream
to the pachube servers.

package installations performed:
opkg update
opkg upgrade
opkg install bash
opkg install python
opkg install python-modules
opkg install python-setuptools
opkg install python-pyserial
# this was key to getting easy_install to run
# on the beagleboard but not the beaglebone
opkg install python-dev --force-overwrite
easy_install requests
easy_install twiggy
opkg install git
opkg install emacs
opkg install sqlite3
opkg install kernel-module-ftdi-sio


