"""
Connection parameters required to communicate with a router. Currently a placeholder. Future versions will support vendor-specific integrations.
"""


from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RouterConnection:
    """Connection parameters required to communicate with a router."""

    address: str
    username: str
    password: str
    timeout: int
    verify_tls: bool
