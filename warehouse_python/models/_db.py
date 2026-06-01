"""
models/_db.py
-------------
Shared SQLAlchemy instance — imported by all model modules
to avoid circular imports.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
