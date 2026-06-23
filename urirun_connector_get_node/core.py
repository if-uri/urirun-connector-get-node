# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.

"""Node bootstrap and health routes for urirun.

Two read-only ``node://`` routes:

* ``node://get/installer/query/script`` -- the get.ifuri.com one-liner that
  bootstraps a urirun node (optionally with a profile and connectors), returned
  as text without contacting the network.
* ``node://host/runtime/query/health``  -- local urirun runtime health: version,
  importability and CLI availability.

Each route is declared once with a typed ``@conn.handler(..., isolated=True)``:
the function signature becomes the input schema and the body returns the JSON
result. ``isolated=True`` runs the route out-of-process through the shared
``python -m urirun.exec`` runner, so the binding stays **registry-portable** --
it executes from a compiled/served registry (``urirun run`` / ``urirun node
serve``) with only the package importable, no ``_exec.py`` shim and no
console-script install.

The manifest stays prose-only; ``routes``/``uriSchemes`` are derived from the
declared routes.
"""

from __future__ import annotations

import shutil
from importlib import metadata
from typing import Any

import urirun

CONNECTOR_ID = "get-node"
conn = urirun.connector(CONNECTOR_ID, scheme="node")

GET_BASE_URL = "https://get.ifuri.com"


# --- route logic (real implementation) ------------------------------------

def _connector_list(connectors: str) -> list[str]:
    return [item.strip() for item in connectors.split(",") if item.strip()]


def runtime_health() -> dict[str, Any]:
    """Report local urirun runtime health without touching the network."""
    import platform
    import sys

    try:
        version = metadata.version("urirun")
    except metadata.PackageNotFoundError:
        version = getattr(urirun, "__version__", "unknown")

    cli = shutil.which("urirun")
    importable = hasattr(urirun, "connector")
    return {
        "ok": bool(importable),
        "connector": CONNECTOR_ID,
        "urirunVersion": version,
        "urirunImportable": importable,
        "cliAvailable": cli is not None,
        "cliPath": cli,
        "python": platform.python_version(),
        "executable": sys.executable,
    }


# --- route declarations: schema + isolated handler all derived -------------

@conn.handler(
    "node://get/installer/query/script",
    isolated=True,
    meta={"label": "Get the node installer script"},
)
def installer_script(profile: str = "default", connectors: str = "") -> dict[str, Any]:
    """Return the get.ifuri.com bootstrap command for a node (no network call)."""
    selected = _connector_list(connectors)
    query = []
    if profile and profile != "default":
        query.append(f"profile={profile}")
    if selected:
        query.append("connectors=" + ",".join(selected))
    suffix = ("?" + "&".join(query)) if query else ""
    command = f"curl -fsSL '{GET_BASE_URL}/{suffix}' | bash" if suffix else f"curl -fsSL {GET_BASE_URL} | bash"
    return {
        "ok": True,
        "connector": CONNECTOR_ID,
        "profile": profile,
        "connectors": selected,
        "url": f"{GET_BASE_URL}/{suffix}" if suffix else GET_BASE_URL,
        "command": command,
    }


@conn.handler(
    "runtime/query/health",
    isolated=True,
    meta={"label": "Check local urirun runtime health"},
)
def health() -> dict[str, Any]:
    """Report local urirun runtime health without touching the network."""
    return runtime_health()


# --- authoring surface: bindings / manifest / CLI --------------------------

def urirun_bindings() -> dict[str, Any]:
    """Serializable v2 bindings for this connector (entry point: urirun.bindings)."""
    return conn.bindings()


def connector_manifest() -> dict[str, Any]:
    """Full manifest: prose (connector.manifest.json) + routes/uriSchemes/
    adapterKinds/examples derived from the handlers."""
    return conn.manifest(urirun.load_manifest(__package__))


def main(argv: list[str] | None = None) -> int:
    """Console-script entry point: subcommands + dispatch derived from the handlers."""
    return conn.cli(argv, manifest_prose=urirun.load_manifest(__package__))


if __name__ == "__main__":
    import sys

    raise SystemExit(main())
