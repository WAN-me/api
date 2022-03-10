#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
from gunicorn.app.wsgiapp import run

if __name__ == '__main__':
    os.system("fuser 5000/tcp -k >> /dev/null")
    os.chdir("/root/tests/api/")
    os.system('git pull origin test')
    sys.argv = [
        sys.argv[0],
        '-w',
        '8',
        '-b',
        '0.0.0.0:5000',
        'api:api',
        '--access-logfile=-']
    sys.exit(run())
