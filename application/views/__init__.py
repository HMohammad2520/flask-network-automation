from flask import Blueprint
from typing import List

from .api import api
from .auth import auth
from .root import root
from .test import test
from .website import website

blueprints: List[Blueprint] = [
    api,
    auth,
    root,
    test,
    website,
]

__all__ = ['blueprints']