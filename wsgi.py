"""
WSGI entry point for PythonAnywhere.

In the Web tab, set:
  Source code: /home/YOUR_USERNAME/HarfHizlisi
  Working directory: /home/YOUR_USERNAME/HarfHizlisi
  WSGI configuration file: /var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py

Point that file at this module, e.g.:

    import sys
    path = '/home/YOUR_USERNAME/HarfHizlisi'
    if path not in sys.path:
        sys.path.insert(0, path)
    from wsgi import application
"""

from app import app

application = app
