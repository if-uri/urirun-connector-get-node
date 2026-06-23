# TODO

- [ ] Add a Docker smoke (`docker-test` target + compose) matching the other
      `urirun-connector-*` repos, then extend CI to run it.
- [ ] Optionally fetch and verify the live get.ifuri.com installer checksum
      behind an explicit `--online` flag.
- [ ] Add example flows that health-check a node before dispatching work to it.
- [ ] Promote the hub catalog entry from `planned` to `available` once published.
