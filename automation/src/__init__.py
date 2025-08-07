"""
Teamcenter Automation Framework
© 2025 Murray Kopit. All Rights Reserved.
"""

__version__ = "1.0.0"
__author__ = "Murray Kopit"
__email__ = "murr2k@gmail.com"

from .client.rest_client import TeamcenterRESTClient
from .client.auth import AuthenticationManager

__all__ = [
    'TeamcenterRESTClient',
    'AuthenticationManager'
]