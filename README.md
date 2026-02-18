<a name="readme-top"></a>

<div align="center">
  <h1 align="center" style="border-bottom: none">Maestrist: AI Agent Platform</h1>
  <p align="center"><b>Part of the Orcest AI Ecosystem</b></p>
</div>

<div align="center">
  <a href="https://github.com/orcest-ai/Maestrist/blob/main/LICENSE"><img src="https://img.shields.io/badge/LICENSE-MIT-20B2AA?style=for-the-badge" alt="MIT License"></a>
</div>

<hr>

Maestrist is an AI agent platform that enables autonomous software development through intelligent agents. It is a core component of the **Orcest AI** ecosystem, integrated with **RainyModel** (rm.orcest.ai) for intelligent LLM routing across free, internal, and premium providers.

### Orcest AI Ecosystem

| Service | Domain | Role |
|---------|--------|------|
| **Lamino** | llm.orcest.ai | LLM Workspace |
| **RainyModel** | rm.orcest.ai | LLM Routing Proxy |
| **Maestrist** | agent.orcest.ai | AI Agent Platform |
| **Orcide** | ide.orcest.ai | Cloud IDE |
| **Login** | login.orcest.ai | SSO Authentication |

## Features

- **AI-Driven Development**: Autonomous agents that can write, test, and debug code
- **Multiple Agent Types**: CodeAct, Browsing, Visual Browsing, and more
- **RainyModel Integration**: Smart LLM routing with automatic fallback (Free → Internal → Premium)
- **SSO Authentication**: Enterprise-grade access control via login.orcest.ai
- **Extensible Architecture**: Plugin system for custom agents and tools
- **MCP Compatibility**: Full Model Context Protocol support
- **Web Browsing**: Agents can browse and interact with web pages
- **Multi-Model Support**: Works with any OpenAI-compatible LLM provider

## Quick Start

### Using Docker (Recommended)

```bash
docker run -it \
  -e LLM_BASE_URL="https://rm.orcest.ai/v1" \
  -e LLM_API_KEY="your-rainymodel-key" \
  -e LLM_MODEL="rainymodel/agent" \
  -p 3000:3000 \
  orcestai/maestrist
```

### Configuration

Maestrist uses RainyModel as its default LLM backend. Configure via environment variables:

```bash
LLM_BASE_URL=https://rm.orcest.ai/v1
LLM_API_KEY=<your-rainymodel-api-key>
LLM_MODEL=rainymodel/agent
```

Or via `config.toml`:

```toml
[llm]
model = "rainymodel/agent"
api_key = "your-rainymodel-api-key"
base_url = "https://rm.orcest.ai/v1"
```

## Development

```bash
make build
make setup-config
make run
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

This project is licensed under the [MIT License](LICENSE).

Part of the [Orcest AI](https://orcest.ai) ecosystem.
