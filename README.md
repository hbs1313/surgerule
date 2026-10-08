# Surge / SMART Hub 共享分流规则

一份规则源，供本地 Surge 和使用 Mihomo 的 SMART Hub 使用。

```text
根目录 *.list（唯一匹配规则源） + routing.json（分类、共享顺序与策略名称）
    ├─ Surge：直接引用原 .list
    ├─ Mihomo：引用自动生成的同名 .yaml（behavior: classical）
    └─ 自动生成目录、兼容性说明和两端引用片段
```

**规则集只回答“匹配哪些请求”，不包含服务器、密码或固定出口 IP。**
`AI`、`AI-Claude`、`Work-US`、`Proxy` 是调用端代理组名称；实际选择哪个出口，
仍由私有 Surge / Hub 配置决定。调度器不得改写这些业务身份。

## 从哪里查看与使用

- [完整规则目录](docs/catalog.md)：列出全部列表、用途、条数和兼容性。
- [机器可读目录](docs/catalog.json)：输出计数、排除类型和有效规则哈希。
- [Surge 本地分流片段](examples/surge-shared.dconf)：各业务绑定自身策略组。
- [Surge 交给 SMART 的入口片段](examples/surge-smart-ingress.dconf)：共享业务统一绑定入口，出口由 Hub 决定。
- [Mihomo 远程 provider 与规则片段](examples/mihomo-shared.yaml)。
- [接入、更新、回退与边界](docs/usage.md)。

保留根目录原文件名和 URL；不要求现有消费者改目录。第三方 Google、YouTube、
TikTok 等列表并未复制进本仓库，仍保留原来的独立来源与排序。

## 维护方式

需要新增域名时，只编辑对应 `.list`，然后运行：

```sh
sh scripts/sync-yaml.sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/build-rules.py --check
git diff --check
```

- 新增列表时，还必须在 `routing.json` 的 `lists` 中声明分类和兼容性，避免漏生成。
- 仅新增一个业务域名不需要修改 Python、YAML、示例或目录；生成器会同步产物。
- `routing.json.rules` 是**共享业务**的顺序和策略映射，不是完整网关配置。
- 不手改 `.yaml`、`docs/catalog.*` 或三个生成片段；它们会被重新生成覆盖。
- `--check` 只检查，不写文件。CI 校验所有源、生成文件、例外和优先级回归；
  不再只检查一个硬编码 YAML 清单。
- 将审核后的源文件和生成产物一起提交、推送。CI 检查不等于生产切换。

## 明确的兼容边界

| 范围 | Surge | Mihomo / SMART Hub |
|---|---|---|
| 19 个完整兼容列表 | 原 `.list` | 同名 `.yaml`，有效规则顺序一致 |
| `wechat` | 全部规则，包括 User-Agent | `.yaml` 仅含可支持的域名、IP、ASN；2 条 User-Agent 不可复现 |
| `yy`、`zhuli` | 本地源设备 IP 分流 | 不生成 YAML；远端 Hub 看不到原 LAN 设备身份 |

未来新出现未知规则类型会直接报错，不会自动“跳过”。共享业务列表必须完整兼容，
不能通过丢掉不支持的条目生成一个看似成功的 Hub 规则集。

本次整理不调整域名匹配范围或现有策略顺序；`wechat` 和 `mmc` 的旧说明已校正，
但实际动作仍取决于消费者绑定。

## 顺序不能随意改变

- Apple / Claude / OpenAI / Google 专用 AI 列表先于通用 `ai` 和 Work-US。
- Claude 与 OpenAI 的部分认证、支付、验证码和遥测依赖重叠，当前由先匹配的 Claude 组处理。
- `ai.list` 是通用及兼容列表，**不是全部 AI 子表的完整并集**；只引用它不等于完整覆盖。
- `video-proxy` 必须在 `twitter` 前，才能让指定视频域名覆盖 `twimg.com` 的宽后缀。
- `ben` / `mmc` 中有 Azure、Cloudflare 等宽后缀；若提前，可能抢走 AI 依赖。
- `proxy`、`tvdirect` 等独立列表也有交集；不要把“格式整理”当作授权重排或跨表去重。

## 发布不等于部署

`main` URL 适合自动拉取；完整 commit SHA URL 适合可审计、可回退的固定版本。
**地址中固定了 SHA 的客户端不会因为仓库 push 自动升级**，哪怕设置了每小时刷新。
AI 身份敏感环境建议两端使用同一个已验证 SHA，再按部署步骤一起升级。

不要提交服务器密钥、面板访问密钥、家庭隧道信息或私有客户端配置。

官方格式依据：[Surge Rule Sets](https://manual.nssurge.com/rules/ruleset.html)、
[Surge HTTP Rules](https://manual.nssurge.com/rules/http.html)、
[Mihomo rule-providers](https://wiki.metacubex.one/config/rule-providers/)、
[Mihomo provider 内容](https://wiki.metacubex.one/config/rule-providers/content/)。
