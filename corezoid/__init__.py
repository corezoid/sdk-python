"""
Corezoid Python SDK
~~~~~~~~~~~~~~~~~~

A modern Python client library for interacting with the Corezoid Process Engine platform.

:copyright: (c) 2024 by Corezoid.
:license: MIT, see LICENSE for more details.
"""

from .client import CorezoidClient
from .operations import RequestOperation
from .exceptions import CorezoidError
from .batch import OperationBatch
from .config import Config

__version__ = '0.1.0'
