#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
from gunicorn.app.wsgiapp import run

if __name__ == '__main__':
    os.system("fuser 3000/tcp -k >> /dev/null")
    os.chdir("/root/prod/api")
    os.system('git pull origin master')
    sys.argv = [
        sys.argv[0],
        '-w',
        '8',
        '-b',
        '0.0.0.0:3000',
        'api:api',
        '--access-logfile=-']
    sys.exit(run())
