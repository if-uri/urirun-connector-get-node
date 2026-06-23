# get-node connector — examples

Emit node installer scripts.

## Install
```bash
urirun install urirun-connector-get-node
```
`urirun install` resolves catalog ids via connect.ifuri.com; `--catalog <url>` points at a
local/on-prem registry; a full package name / git URL / path falls back to `pip install`.

## Run
```bash
# Emit node installer scripts (read)
urirun run 'node://get/installer/query/script' --payload '{}' --execute --allow 'node://*'

# preview without running (dry-run): drop --execute
urirun run 'node://get/installer/query/script' --payload '{}' --allow 'node://*'
```

## Inspect the runtime (no path — like error:// / log://)
```bash
urirun list | grep 'node://'                                   # this connector's routes
urirun run 'registry://local/routes/query/list' --payload '{"scheme":"node"}' --allow 'registry://*'
urirun run 'registry://local/bindings/query/show' --payload '{"uri":"node://get/installer/query/script"}' --allow 'registry://*'   # full typed contract
urirun errors                                                      # recent runtime errors (error://)
```

## Generate a client / API surface from the binding
```bash
urirun discover | urirun gen openapi - --out openapi.json   # OpenAPI 3 (one path per route)
urirun discover | urirun gen proto   - --out service.proto  # protobuf + gRPC (typed rpc per route)
urirun discover | urirun gen client  - --out client.py      # typed Python client
```
