"""
ASGI entry for local development with uvicorn.

    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Production (PythonAnywhere): use wsgi.py → Flask WSGI app, not this module.
"""

from asgiref.wsgi import WsgiToAsgi

from app import create_app

app = WsgiToAsgi(create_app())
