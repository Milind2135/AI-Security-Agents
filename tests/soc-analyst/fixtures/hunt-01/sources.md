# Data sources (SYNTHETIC — Elastic, for soc-analyst hunt tests)

Platform: Elastic Security (query language ES|QL). Time zone: UTC.
In scope: 120 developer and build hosts (`host.name` like `dev-ws-*` and `build-*`).

| Data | Index | Key fields |
|---|---|---|
| EDR process events | `logs-endpoint.events.process-*` | `@timestamp`, `host.name`, `user.name`, `process.name`, `process.command_line`, `process.parent.name` |
| EDR network events | `logs-endpoint.events.network-*` | `@timestamp`, `host.name`, `process.name`, `destination.ip`, `destination.domain`, `destination.port` |
| GitHub audit log | `logs-github.audit-*` | `@timestamp`, `github.actor`, `github.action`, `github.repo` |

Sample process event:
```json
{"@timestamp":"2026-11-10T09:12:03Z","host.name":"dev-ws-07","user.name":"dev07","process.parent.name":"node","process.name":"git","process.command_line":"git fetch origin"}
```
Known gap: 8 of the 120 hosts have no EDR agent (build-31 to build-38).
