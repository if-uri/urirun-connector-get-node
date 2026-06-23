# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.

from __future__ import annotations

import json

import urirun
from urirun import v2
from urirun_connector_get_node import (
    connector_manifest,
    health,
    installer_script,
    main,
    runtime_health,
    urirun_bindings,
)

ROUTE_INSTALLER = "node://get/installer/query/script"
ROUTE_HEALTH = "node://host/runtime/query/health"


def test_installer_default() -> None:
    result = installer_script()
    assert result["ok"] is True
    assert result["command"] == "curl -fsSL https://get.ifuri.com | bash"
    assert result["connectors"] == []


def test_installer_with_profile_and_connectors() -> None:
    result = installer_script(profile="lan", connectors="planfile, time-tools")
    assert result["connectors"] == ["planfile", "time-tools"]
    assert "profile=lan" in result["url"]
    assert "connectors=planfile,time-tools" in result["url"]
    assert result["command"].startswith("curl -fsSL 'https://get.ifuri.com/?")


def test_runtime_health() -> None:
    result = runtime_health()
    assert result["ok"] is True
    assert result["urirunImportable"] is True
    assert "python" in result


def test_health_handler_matches_runtime() -> None:
    assert health()["ok"] is True


def test_bindings_are_isolated_handlers() -> None:
    b = urirun_bindings()["bindings"]
    assert set(b) == {ROUTE_INSTALLER, ROUTE_HEALTH}

    installer = b[ROUTE_INSTALLER]
    # registry-portable in-process handler: runs out-of-process via urirun.exec
    assert installer["adapter"] == "local-function-subprocess"
    assert installer["python"]["module"] == "urirun_connector_get_node.core"
    assert installer["python"]["export"] == "installer_script"
    assert "argv" not in installer
    assert installer["inputSchema"]["properties"]["profile"]["default"] == "default"

    health_b = b[ROUTE_HEALTH]
    assert health_b["adapter"] == "local-function-subprocess"
    assert health_b["python"]["module"] == "urirun_connector_get_node.core"
    assert health_b["python"]["export"] == "health"
    assert "argv" not in health_b
    json.dumps(urirun_bindings())  # serializable: no live ref leaks


def test_runtime_executes_from_compiled_registry() -> None:
    # the whole point: a serialized->compiled registry still runs the route
    registry = urirun.compile_registry(json.loads(json.dumps(urirun_bindings())))
    env = v2.run(ROUTE_HEALTH, registry, mode="execute",
                 policy=urirun.policy(allow=["node://*"]))
    assert env["ok"] is True
    data = urirun.result_data(env)
    assert data["ok"] is True and data["urirunImportable"] is True


def test_manifest_prose_plus_derived_routes() -> None:
    m = connector_manifest()
    assert m["id"] == "get-node"
    assert set(m["routes"]) == {ROUTE_INSTALLER, ROUTE_HEALTH}
    assert m["uriSchemes"] == ["node"]
    assert m["summary"]  # prose preserved
    assert m["install"]["mode"] == "urirun-extra"


def test_cli_bindings_and_manifest(capsys) -> None:
    assert main(["bindings"]) == 0
    assert ROUTE_INSTALLER in json.loads(capsys.readouterr().out)["bindings"]
    assert main(["manifest"]) == 0
    assert json.loads(capsys.readouterr().out)["id"] == "get-node"
