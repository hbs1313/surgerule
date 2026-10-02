# Surge Rule Sets

Personal routing rules used by Surge and compatible YAML rule providers.

## Rule-set map

| File | Intended policy | Purpose |
| --- | --- | --- |
| `ziniao.list` | `DIRECT` | Ziniao client and service endpoints |
| `mmcdirect.list` | `DIRECT` | Explicit direct-access exceptions: local services, Amazon marketplaces, single sites, speed tests |
| `capcut.list` | `DIRECT` | CapCut and ByteDance media endpoints |
| `wechat.list` | `DIRECT` | WeChat domain, IP, ASN, and user-agent rules |
| `wecom.list` | `DIRECT` | WeCom-specific domains |
| `tvdirect.list` | `DIRECT` | TV and CDN endpoints that work better directly |
| `proxy.list` | `Proxy` | Single sites through the general proxy |
| `oix-hk.list` | `oix-hk` | Sites pinned to the oix Hong Kong group |
| `spectrum.list` | fixed US exit | Spectrum / Spectrum Business sites, account, API and CDN |
| `ai-apple.list` | `AI-Apple` | Apple Intelligence, Siri and Private Relay endpoints |
| `ai-chat.list` | `AI-Chat` | ChatGPT / Claude and their content and authentication dependencies |
| `ai-google.list` | `AI-Google` | Google AI products |
| `ai.list` | `AI` | AI products and exact product dependencies |
| `us.list` | `AI` | Sites that need the general US exit |
| `ben.list` | `Work-US` | Personal and business services on the stable US identity |
| `twitter.list` | `Work-US` | X/Twitter traffic |
| `mmc.list` | `Work-US` | Business, network, and SaaS services |
| `tv.list` | `Proxy` | TV metadata, media, and scraping services |
| `yy.list` | profile-dependent | Operations-team source IPs |
| `zhuli.list` | profile-dependent | Assistant-team source IPs |

The table is in the order the Surge profiles evaluate the lists. Which list goes to
which policy, and in what order, is set in the shared `[Rule]` section of the Surge
profiles; this repository holds the domains.

## Maintenance rules

- The `.list` file is the source of truth.
- A same-named `.yaml` file must contain the same active rules under `payload:`.
- Prefer `DOMAIN-SUFFIX` or exact `DOMAIN` rules over broad `DOMAIN-KEYWORD` rules.
- Use `IP-CIDR`/`IP-CIDR6` with `no-resolve` for literal networks.
- Do not add credentials, proxy server secrets, API keys, or private identity data.
- Avoid whole-ASN and shared-platform suffix rules unless the entire network or
  platform is intentionally in scope.
- Keep a domain in only one list when those lists are assigned to different
  policies. One exception: `ai-apple.list`, `ai-chat.list` and `ai-google.list` are
  evaluated ahead of `ai.list` and win; `ai.list` still names those products for
  consumers that have a single AI policy.
- A new site goes into the list of the exit it needs; the profiles pick the change
  up at their next daily refresh of the lists.
