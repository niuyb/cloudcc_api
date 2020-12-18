import redis

from .base import *  # NOQA

DEBUG = True

MODE = "develop"

import socket

myname = socket.getfqdn(socket.gethostname())
myaddr = socket.gethostbyname(myname)

# NEW_SUPPORT_HOST = "http://" + myaddr + ":8000"
# OLD_SUPPORT_HOST = "http://support.istarshine.com"
