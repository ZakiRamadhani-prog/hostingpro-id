"""WSGI entrypoint for production servers.

Use this `application` variable with WSGI servers like Gunicorn/uWSGI.
"""

from app_factory import create_app

application = create_app()

