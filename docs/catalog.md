# 规则目录（自动生成）

只修改根目录 `.list` 和 `routing.json`，不要手改 YAML 或本目录生成文件。

| 列表 | 分类 | Surge 条数 | Mihomo 条数 | 兼容性 | 用途 |
|---|---|---:|---:|---|---|
| [ai-apple](../ai-apple.list) | ai | 19 | 19 | 完整 | Apple Intelligence、Siri 和相关中继 |
| [ai-claude](../ai-claude.list) | ai | 26 | 26 | 完整 | Claude 及共享依赖，优先于 OpenAI |
| [ai-chat](../ai-chat.list) | ai | 35 | 35 | 完整 | OpenAI / ChatGPT 及依赖 |
| [ai-google](../ai-google.list) | ai | 20 | 20 | 完整 | Google AI 和已指定的身份敏感业务 |
| [ai](../ai.list) | ai | 113 | 113 | 完整 | 其他 AI 与单组兼容列表；不是所有子表的完整并集 |
| [us](../us.list) | ai | 10 | 10 | 完整 | 沿用 AI 组的美国业务例外 |
| [ben](../ben.list) | work-us | 59 | 59 | 完整 | 个人及业务站点，沿用 Work-US |
| [mmc](../mmc.list) | work-us | 48 | 48 | 完整 | 业务、网络及 SaaS 站点，沿用 Work-US |
| [twitter](../twitter.list) | ai | 32 | 32 | 完整 | X / Twitter 账号、API 与图片，跟固定 AI 落地；大流量视频由 video-proxy 先匹配 |
| [video-proxy](../video-proxy.list) | proxy | 3 | 3 | 完整 | X 媒体例外，必须位于 twitter 之前 |
| [proxy](../proxy.list) | proxy | 13 | 13 | 完整 | 普通代理例外；未纳入共享业务顺序 |
| [tv](../tv.list) | proxy | 25 | 25 | 完整 | 电视、媒体元数据和抓取服务 |
| [ziniao](../ziniao.list) | client-direct | 12 | 12 | 完整 | 紫鸟客户端与服务；默认留在本地处理 |
| [mmcdirect](../mmcdirect.list) | client-direct | 74 | 74 | 完整 | 本地直连例外；不要整表接管到境外 Hub |
| [capcut](../capcut.list) | client-direct | 10 | 10 | 完整 | 剪映及字节媒体端点 |
| [wechat](../wechat.list) | client-direct | 344 | 342 | 部分：USER-AGENT 留在 Surge | 微信域名/IP/ASN；2 条 USER-AGENT 仅 Surge 可用 |
| [wecom](../wecom.list) | client-direct | 8 | 8 | 完整 | 企业微信端点 |
| [tvdirect](../tvdirect.list) | client-direct | 47 | 47 | 完整 | 直连媒体及 CDN 例外 |
| [oix-hk](../oix-hk.list) | dedicated | 3 | 3 | 完整 | oix 香港专用规则；不自动并入普通代理 |
| [spectrum](../spectrum.list) | dedicated | 6 | 6 | 完整 | Spectrum 账户及 CDN；出口由私有配置绑定 |
| [yy](../yy.list) | client-source | 6 | 0 | 仅本地源地址，不生成 Hub 规则 | 运营设备源 IP，只在本地网关使用 |
| [zhuli](../zhuli.list) | client-source | 3 | 0 | 仅本地源地址，不生成 Hub 规则 | 助理设备源 IP，只在本地网关使用 |
| [agg-proxy](../agg-proxy.list) | proxy | 1766 | 1749 | 部分：USER-AGENT 留在 Surge | 生成：聚合 14 个上游服务类列表（网关→入口、手机→Proxy）；no-resolve 无 IP 规则者并入同一类 |
| [agg-google](../agg-google.list) | ai | 903 | 888 | 部分：USER-AGENT 留在 Surge | 生成：Google/YouTube/Gemini/GoogleVoice 聚合（网关→入口、手机→AI-Google） |
| [agg-workus](../agg-workus.list) | work-us | 167 | 167 | 完整 | 生成：Adobe/LinkedIn/Reddit/Shopify/TruthSocial 聚合（Work-US；TikTok 因网关侧折叠到入口而单独引用上游） |
| [agg-workus-nr](../agg-workus-nr.list) | work-us | 571 | 571 | 完整 | 生成：Facebook/Instagram 聚合（Work-US, no-resolve；两者带 IP 规则故单独一组） |
| [agg-direct](../agg-direct.list) | client-direct | 127 | 90 | 部分：USER-AGENT 留在 Surge | 生成：Apple/AppStore/iCloud/Speedtest 聚合（DIRECT） |
| [skk-microsoft](../skk-microsoft.list) | proxy | 84 | 84 | 完整 | 收编自 ruleset.skk.moe non_ip/microsoft.conf（AGPL-3.0） |
| [skk-microsoft-cdn](../skk-microsoft-cdn.list) | client-direct | 54 | 52 | 部分：USER-AGENT 留在 Surge | 收编自 ruleset.skk.moe non_ip/microsoft_cdn.conf（AGPL-3.0；URL-REGEX 仅 Surge） |
| [skk-apple-services](../skk-apple-services.list) | client-direct | 26 | 18 | 部分：USER-AGENT 留在 Surge | 收编自 ruleset.skk.moe non_ip/apple_services.conf（AGPL-3.0；PROCESS-NAME 仅 Surge） |
| [skk-apple-cdn](../skk-apple-cdn.list) | client-direct | 160 | 160 | 完整 | 收编自 ruleset.skk.moe domainset/apple_cdn.conf（AGPL-3.0；bare domain 已转 DOMAIN-SUFFIX） |

“语法可用于 Mihomo”不代表应在境外 Hub 接管：国内直连与源设备规则仍由本地网关负责。
