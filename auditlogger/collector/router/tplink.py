"""TP-Link router provider, backed by the third-party tplinkrouterc6u client.

TP-Link's admin-panel login uses a proprietary RSA/AES-encrypted password
exchange that differs across firmware generations. Rather than reimplement
that here, this wraps tplinkrouterc6u (https://github.com/AlexandrErohin/TP-Link-Archer-C6U),
an actively maintained, open-source library that already handles it and
auto-selects the right client class for the detected router model.
"""

from __future__ import annotations
from typing import Any

from tplinkrouterc6u import TplinkRouterProvider

from .base import RouterProvider
from .connection import RouterConnection


class TplinkProvider(RouterProvider):
    """Collects WAN IP, gateway, and DNS info from a TP-Link router's admin panel."""

    def __init__(self, connection: RouterConnection) -> None:
        self._connection = connection

    def collect(self) -> dict[str, Any]:
        """Return WAN/gateway/DNS info, or {} if the router can't be reached.

        Any auth, network, or library error here is swallowed rather than
        raised: per docs/architecture.md, collectors must fail independently
        without breaking the rest of the audit snapshot. This currently
        catches the broad Exception class, since tplinkrouterc6u's specific
        exception hierarchy isn't something I've verified against a live
        router - narrowing this once real failure modes are observed (e.g.
        wrong password vs. router unreachable) would be a good follow-up.
        """
        router = TplinkRouterProvider.get_client(
            self._connection.address,
            self._connection.password,
            self._connection.username,
            verify_ssl=self._connection.verify_tls,
            timeout=self._connection.timeout,
        )

        try:
            router.authorize()
            status = router.get_ipv4_status()
        except Exception:
            return {}
        else:
            return {
                "wan_ip": status.wan_ipv4_ipaddr,
                "gateway": status.wan_ipv4_gateway,
                "dns_primary": status.wan_ipv4_pridns,
                "dns_secondary": status.wan_ipv4_snddns,
            }
        finally:
            try:
                router.logout()
            except Exception:
                pass