from flask import Blueprint
from typing import List

from .api import api_bp
from .apps import apps_bp
from .auth import auth_bp
from .root import root_bp
from .test import test_bp

blueprints: List[Blueprint] = [
    api_bp,
    apps_bp,
    auth_bp,
    root_bp,
    test_bp,
]

__all__ = ['blueprints', 'apps_bp']