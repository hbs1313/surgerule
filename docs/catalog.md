# 规则目录（自动生成）

只修改根目录 `.list` 和 `routing.json`，不要手改 YAML 或本目录生成文件。

| 列表 | 分类 | Surge 条数 | Mihomo 条数 | 兼容性 | 用途 |
|---|---|---:|---:|---|---|
| [ai-apple](../ai-apple.list) | ai | 19 | 19 | 完整 | Apple Intelligence、Siri 和相关中继 |
| [ai-claude](../ai-claude.list) | ai | 26 | 26 | 完整 | Claude 及共享依赖，优先于 OpenAI |
| [ai-chat](../ai-chat.list) | ai | 35 | 35 | 完整 | OpenAI / ChatGPT 及依赖 |
| [ai-google](../ai-google.list) | ai | 20 | 20 | 完整 | Google AI 和已指定的身份敏感业务 |
| [ai](../ai.list) | ai | 113 | 113 | 完整 | 其他 AI 与单组兼容列表；不是所有子表的完整并集 |
| [us](../us.list) | ai | 9 | 9 | 完整 | 沿用 AI 组的美国业务例外 |
| [ben](../ben.list) | work-us | 59 | 59 | 完整 | 个人及业务站点，沿用 Work-US |
| [mmc](../mmc.list) | work-us | 48 | 48 | 完整 | 业务、网络及 SaaS 站点，沿用 Work-US |
| [twitter](../twitter.list) | work-us | 32 | 32 | 完整 | X / Twitter；媒体例外需先匹配 |
| [video-proxy](../video-proxy.list) | proxy | 2 | 2 | 完整 | X 媒体例外，必须位于 twitter 之前 |
| [proxy](../proxy.list) | proxy | 13 | 13 | 完整 | 普通代理例外；未纳入共享业务顺序 |
| [tv](../tv.list) | proxy | 25 | 25 | 完整 | 电视、媒体元数据和抓取服务 |
| [ziniao](../ziniao.list) | client-direct | 12 | 12 | 完整 | 紫鸟客户端与服务；默认留在本地处理 |
| [mmcdirect](../mmcdirect.list) | client-direct | 77 | 77 | 完整 | 本地直连例外；不要整表接管到境外 Hub |
| [capcut](../capcut.list) | client-direct | 10 | 10 | 完整 | 剪映及字节媒体端点 |
| [wechat](../wechat.list) | client-direct | 344 | 342 | 部分：USER-AGENT 留在 Surge | 微信域名/IP/ASN；2 条 USER-AGENT 仅 Surge 可用 |
| [wecom](../wecom.list) | client-direct | 8 | 8 | 完整 | 企业微信端点 |
| [tvdirect](../tvdirect.list) | client-direct | 47 | 47 | 完整 | 直连媒体及 CDN 例外 |
| [oix-hk](../oix-hk.list) | dedicated | 3 | 3 | 完整 | oix 香港专用规则；不自动并入普通代理 |
| [spectrum](../spectrum.list) | dedicated | 6 | 6 | 完整 | Spectrum 账户及 CDN；出口由私有配置绑定 |
| [yy](../yy.list) | client-source | 6 | 0 | 仅本地源地址，不生成 Hub 规则 | 运营设备源 IP，只在本地网关使用 |
| [zhuli](../zhuli.list) | client-source | 3 | 0 | 仅本地源地址，不生成 Hub 规则 | 助理设备源 IP，只在本地网关使用 |

“语法可用于 Mihomo”不代表应在境外 Hub 接管：国内直连与源设备规则仍由本地网关负责。
