# urirun-connector-get-node

Node bootstrap and health connector for [ifURI](https://ifuri.com) /
[urirun](https://github.com/if-uri/urirun). It exposes the
[get.ifuri.com](https://get.ifuri.com) node installer one-liner and a local
runtime health check as `node://` routes.

Catalog page: <https://connect.ifuri.com/connectors/get-node>

## Routes

| URI | Operation |
| --- | --- |
| `node://get/installer/query/script` | get.ifuri.com bootstrap command (no network call) |
| `node://host/runtime/query/health` | local urirun runtime health (version, CLI, importability) |

## Install

```bash
pip install "urirun-connector-get-node @ git+https://github.com/if-uri/urirun-connector-get-node.git@v0.1.0"
# or, from the hub:
urirun connectors install get-node --execute
```

## Use

```bash
urirun-get-node health
urirun-get-node installer --profile lan --connectors planfile,time-tools
```

Both routes are read-only and contact no network at call time; the installer
route only *returns* the command string. The connector projects to MCP tools and
A2A skills like any other urirun connector.

## License

Released under the terms in [LICENSE](LICENSE).
