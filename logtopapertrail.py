#!/usr/bin/env python3.5
# coding: utf-8

"""Simple Flask application to transfer log to Papertrail."""


import os
import sys
import logging
from logging.handlers import SysLogHandler
from flask import Flask, jsonify, request


# Get Papertrail information
host = os.environ.get('PAPERTRAIL_HOST', None)
port = os.environ.get('PAPERTRAIL_PORT', None)

if not host:
    print("cannot find Papertrail host !")

if not port:
    print("cannot find Papertrail port !")

if not port or not host:
    sys.exit(1)

port = int(port)


# Define application
app = Flask(__name__)


# Define log
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

syslog = SysLogHandler(address=(host, port))
formatter = logging.Formatter('%(asctime)s %(message)s',
                              datefmt='%b %d %H:%M:%S')
syslog.setFormatter(formatter)
logger.addHandler(syslog)


# Application
@app.route('/')
def index():
    """Index."""
    return '{} ready !'.format(__name__)


@app.route('/log', methods=['POST', ])
def send():
    """Transfer log."""
    # Get information from request
    level = request.form.get('level', '').upper()
    hostname = request.form.get('hostname', '')
    progname = request.form.get('progname', '')
    message = request.form.get('message', '')

    # Check
    errmsg = None
    if not level or level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
        errmsg = ("level parameter must be 'debug', 'info', 'warning' or "
                  "'error'")
    elif not hostname:
        errmsg = "missing hostname parameter"
    elif not progname:
        errmsg = "missing progname parameter"
    elif not message:
        errmsg = "missing message parameter"
    if errmsg:
        return jsonify(dict(status='error', comment=errmsg)), 400

    # Compose log message
    levelno = logging.__dict__[level]
    msg = '{hostname} {progname}: {level}  {message}'.format(**locals())
    logger.log(level=levelno, msg=msg)
    return jsonify(dict(status='ok'))


if __name__ == '__main__':

    # Test application
    app.run(host='0.0.0.0', port=5080)
