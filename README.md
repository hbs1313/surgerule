# Surge Rule Sets

Personal routing rules used by Surge and compatible YAML rule providers.

## Rule-set map

| File | Intended policy | Purpose |
| --- | --- | --- |
| `ai.list` | `AI` | AI products and exact product dependencies |
| `ben.list` | `AI` | Personal services that require the stable US/AI exit |
| `mmc.list` | `Proxy` | Business, network, and SaaS services using the general proxy |
| `mmcdirect.list` | `DIRECT` | Explicit direct-access exceptions |
| `ziniao.list` | `DIRECT` | Ziniao client and service endpoints |
| `twitter.list` | `AI` | X/Twitter traffic |
| `capcut.list` | profile-dependent | CapCut and ByteDance media endpoints |
| `tv.list` | `Proxy` | TV metadata, media, and scraping services |
| `tvdirect.list` | `DIRECT` | TV and CDN endpoints that work better directly |
| `wechat.list` | profile-dependent | WeChat domain, IP, ASN, and user-agent rules |
| `wecom.list` | profile-dependent | WeCom-specific domains |
| `yy.list` | profile-dependent | Operations-team source IPs |
| `zhuli.list` | profile-dependent | Assistant-team source IPs |

## Maintenance rules

- The `.list` file is the source of truth.
- A same-named `.yaml` file must contain the same active rules under `payload:`.
- Prefer `DOMAIN-SUFFIX` or exact `DOMAIN` rules over broad `DOMAIN-KEYWORD` rules.
- Use `IP-CIDR`/`IP-CIDR6` with `no-resolve` for literal networks.
- Do not add credentials, proxy server secrets, API keys, or private identity data.
- Avoid whole-ASN and shared-platform suffix rules unless the entire network or
  platform is intentionally in scope.
- Keep a domain in only one list when those lists are assigned to different
  policies.
