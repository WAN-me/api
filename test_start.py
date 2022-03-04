#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
from gunicorn.app.wsgiapp import run

if __name__ == '__main__':
    sys.argv = [
        sys.argv[0],
        '-w',
        '8',
        '-b',
        '127.0.0.1:3000',
        'api:api',
        '--access-logfile=-']
    sys.exit(run())
