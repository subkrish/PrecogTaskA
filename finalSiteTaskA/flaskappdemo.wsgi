#!/usr/bin/python
import sys

sys.path.insert(0,"/var/www/html/flaskappdemo/")

from flaskappdemo import app as application
application.secret_key = "somesecretsessionkey"