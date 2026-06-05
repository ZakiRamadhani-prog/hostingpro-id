"""WSGI entrypoint for PythonAnywhere.

PythonAnywhere expects:
- file: wsgi.py
- callable: application

This module must be importable from PythonAnywhere project root.
"""

from app_factory import create_app

application = create_app()

