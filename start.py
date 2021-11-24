#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
from gunicorn.app.wsgiapp import run

if __name__ == '__main__':
    os.chdir("/root/tests/wm-api/")
    sys.argv = [sys.argv[0], '-w', '8', '-b', '0.0.0.0:5000', 'api:api','--access-log=-']
    sys.exit(run())