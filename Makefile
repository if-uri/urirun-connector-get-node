.PHONY: help manifest bindings smoke test
help: ## List targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  %-10s %s\n",$$1,$$2}'
manifest: ## Print the connector manifest
	urirun-get-node manifest
bindings: ## Print urirun bindings
	urirun-get-node bindings
smoke: ## bindings -> urirun connectors smoke (validate/compile/run/MCP/A2A)
	urirun-get-node bindings | urirun connectors smoke - \
	  --run 'node://host/runtime/query/health' --payload '{}' \
	  --allow 'node://host/*' --name get-node
test: ## Install editable + smoke
	pip install -e . && python3 -m pytest -q && $(MAKE) smoke
