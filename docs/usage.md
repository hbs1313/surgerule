# 两端接入与维护边界

## 1. 选择远程地址

Surge 直接消费源列表，例如：

```ini
RULE-SET,https://raw.githubusercontent.com/hbs1313/surgerule/main/ai-claude.list,AI-Claude,extended-matching,update-interval=3600
```

Mihomo / SMART Hub 消费同源生成的 YAML：

```yaml
rule-providers:
  canonical-ai-claude:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/hbs1313/surgerule/main/ai-claude.yaml
    path: ./surgerule/ai-claude.yaml
    interval: 3600
rules:
  - RULE-SET,canonical-ai-claude,AI-Claude
```

`AI-Claude` 必须是私有配置里已经存在的组。上面不是可直接启动的完整代理配置，
不含出口定义或默认规则。`path` 是 Hub 本地缓存，不是 GitHub 路径。

固定版本时，把两端 URL 中的 `main` 都替换为同一个完整 40 位 commit SHA。
SHA 地址内容不可变，刷新间隔不能让它跳到新提交。自动更新的 `main` 则由各端
独立缓存和定时拉取，不保证同一秒生效，不能声称原子同步。

## 2. 选择谁决定境外出口

### Surge 自己分业务

使用 [surge-shared.dconf](../examples/surge-shared.dconf) 的绑定片段；AI、Work-US、
Proxy 的落地选择留在 Surge 私有代理组中。

### Surge 只选跨境入口，SMART Hub 分业务

使用 [surge-smart-ingress.dconf](../examples/surge-smart-ingress.dconf) 的绑定方式，
先在私有配置中定义 `SMART-入口`（或替换为自己已有入口组名）。每个候选入口应到同一 Hub。
Hub 合并 [mihomo-shared.yaml](../examples/mihomo-shared.yaml) 的 providers 和业务规则，
由 Hub 上已有的 AI / Work-US / Proxy 组选择落地。入口调度不能改这些组。

### 合并时必须保留

1. 本地国内直连、私网、Ponte/Tailscale 与专用账户例外；不要用示例覆盖整个 `[Rule]`。
2. 共享 AI 接管规则位于宽泛 Apple DIRECT 等规则之前，避免未到 Hub 就被直连。
3. 第三方 Google/YouTube 的身份规则、TikTok 等现有规则及其已核验的插入位置。
4. Surge 专用 User-Agent 等元数据匹配。远端 Hub 不能凭列表转换还原被加密或转发时未传入的属性。
5. Hub 的私网拒绝规则、已有监听/密钥、代理组成员与选择，以及最终 MATCH。

三个生成片段只有共享业务部分，刻意不包含这些私有内容。不要把可导入片段当成整套生产配置。

## 3. 兼容性例外

- `wechat.list` 的两条 USER-AGENT 保留在原源列表内，Surge 继续读取；
  `wechat.yaml` 不含这两条，缺失类型与数量见 [catalog.json](catalog.json)。
  这不是完全等价列表，不应用于要求完整 User-Agent 语义的 Hub 接管。
- `yy.list`、`zhuli.list` 依据本地源设备 IP。虽然另一些客户端可用 SRC-IP-CIDR
  表达类似规则，境外 Hub 收到的是转发后的连接，不能据此识别原局域网设备，故不自动转换。
- client-direct 分类的 YAML 只是语法可用于 Mihomo，方便本地 Mihomo 网关消费，
  **并不建议将国内/本地直连业务发送到境外 Hub 再“DIRECT”**。
- `spectrum`、`oix-hk` 是专用账户/区域路径；没有把它们自动并入 AI 或 Work-US。

## 4. 发布与回退

1. 改 `.list`，必要时改 `routing.json`；生成、测试、审阅 diff。
2. 经授权提交、推送，并检查 CI 和 raw URL 可获取性。
3. 另行部署生产引用：确认本地网关、Hub、手机需要的版本与绑定，不改变现有落地身份。
4. 检查加载后的有效规则和新请求；语法通过、文件已下载不等于实际业务已生效。

固定版本回退：恢复先前已经验证的 SHA 引用，并重新校验/加载；不要整份覆盖含密钥或
后续改动的配置。`main` 自动更新的规则需要先恢复对应内容或切回旧 SHA，不能依赖缓存长期保留。

仓库本身不会登录网关、推送配置、重启服务或改变代理组选择。
