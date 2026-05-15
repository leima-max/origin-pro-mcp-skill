# Security Notes / 安全说明

## English

This package is designed to be shared without local secrets.

Before publishing a fork or derivative package, check for:

- API keys, access tokens, passwords, and bearer tokens
- local connector configuration
- absolute paths containing user names
- third-party integration settings
- generated experiment data that should not be public

Recommended scan:

```powershell
rg -n "key|token|secret|credential|password|local_user_path|connector_specific_env"
```

Do not commit real MCP client configuration if it contains local paths or credentials. Use `examples/mcporter.example.json` as a template instead.

## 中文

本包按可共享方式整理，不应包含本地密钥。

发布 fork 或衍生包前，请检查：

- API key、access token、password、bearer token
- 本地连接器配置
- 带用户名的绝对路径
- 第三方集成配置
- 不应公开的实验数据

推荐扫描：

```powershell
rg -n "key|token|secret|credential|password|local_user_path|connector_specific_env"
```

不要提交包含本机路径或凭据的真实 MCP client 配置。请使用 `examples/mcporter.example.json` 作为模板。
