"""
HTTP client for router communication. Currently a placeholder. Future versions will support vendor-specific integrations.
"""

import requests
from connection import RouterConnection


class RouterClient:
    """HTTP client for router communication."""

    def __init__(self, connection: RouterConnection):
        self._connection = connection

    def _create_session(self) -> requests.Session:
        """Create and configure an HTTP session."""

        session = requests.Session()
        session.verify = self._connection.verify_tls
        return session