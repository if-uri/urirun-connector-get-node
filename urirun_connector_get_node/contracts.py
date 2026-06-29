# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.
"""Route contracts for the get-node connector — node installer and runtime health, read-only."""
from __future__ import annotations

from urirun_connectors_toolkit.contract_gate import Contract

CONTRACTS: dict[str, Contract] = {
    "installer/query/script": Contract(
        version="v1",
        effect="query",
        reversible=False,
        inp={"profile": "?str", "connectors": "?str"},
        out={"ok": "bool", "url": "str", "command": "str", "profile": "str", "connectors": "list"},
        errors=(),
        examples=(
            {
                "payload": {},
                "result": {
                    "ok": True,
                    "connector": "get-node",
                    "url": "https://get.urirun.com/",
                    "command": "curl -fsSL https://get.urirun.com/ | bash",
                    "profile": "default",
                    "connectors": [],
                },
            },
        ),
    ),
    "runtime/query/health": Contract(
        version="v1",
        effect="query",
        reversible=False,
        inp={},
        out={"ok": "bool", "version": "?str", "connectors": "list"},
        errors=(),
        examples=(
            {
                "payload": {},
                "result": {
                    "ok": True,
                    "connector": "get-node",
                    "version": "0.4.174",
                    "connectors": ["kvm", "scanner"],
                },
            },
        ),
    ),
}
