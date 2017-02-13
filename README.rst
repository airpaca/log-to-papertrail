log-to-papertrail
=================

Simple Flask_ application to transfer logs into Papertrail_.


Why ?
-----

On linux, you can use remote syslog and the ``logger`` command to save
script's output. That's the best method.

I made this little Flask_ application to transfer/convert log of external
applications (mainly Microsoft Windows application). These ones are made by a
external company, are installed on a Microsoft Windows server. These
applications send classic ``POST`` requests into this Flask_ application.



How ?
-----

First, you must define two environment variables to specify Papertrail_ host
and port. You can get these informations from your Papertrail_ account.

- ``PAPERTRAIL_HOST`` : hostname of your Papertrail_ log account.
- ``PAPERTRAIL_PORT`` : port of Papertrail_ log accout.

Start the application and use the ``/log`` route (``POST`` method) to transfer
a message into Papertrail_ with these parameters:

- ``level`` (same levels as the Python logging library)
- ``hostname`` (hostname of the server)
- ``progname`` (program name)
- ``message`` (the message to log)

The application return a 400 status code with an error message if a parameter
is missing.

**This method do not check if the message is received by Papertrail.**


Example of use::

    curl -X POST -F level=info -F hostname=server1 -F progname=usefulprog -F "message=task done"

After that command, you must see your message in your Papertrail_ account.



.. _Flask: http://flask.pocoo.org/
.. _Papertrail: https://papertrailapp.com/


