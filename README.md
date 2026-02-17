<a name="readme-top"></a>

<div align="center">
  <h1 align="center" style="border-bottom: none">🎼 Maestrist</h1>
  <h3 align="center"><em>Masterful Agent Ecosystem for Strategic Task Resolution and Innovative Swarm Technology</em></h3>
  <p align="center"><strong>Ignite Your AI Agent Symphony.</strong></p>
</div>

<div align="center">
  <a href="https://github.com/danialsamiei/agent.orcest.ai/blob/main/LICENSE"><img src="https://img.shields.io/badge/LICENSE-MIT-7C3AED?style=for-the-badge" alt="MIT License"></a>
  <a href="https://agent.orcest.ai"><img src="https://img.shields.io/badge/Live_Demo-agent.orcest.ai-3B82F6?style=for-the-badge" alt="Live Demo"></a>
  <br/>
  <a href="https://orcest.ai"><img src="https://img.shields.io/badge/Powered_by-Orcest.ai-7C3AED?style=for-the-badge" alt="Orcest.ai"></a>
</div>

<hr>

🎼 **Maestrist** is the ultimate self-hosted, multi-agent AI coding platform — the advanced agent companion to [Orcest.ai](https://orcest.ai). Built to surpass Devin.ai in features, scalability, and global competition.

> **Fork Heritage**: Maestrist is built upon the excellent [OpenHands](https://github.com/All-Hands-AI/OpenHands) framework (MIT licensed), extended with Orcest ecosystem integration, orchestral-themed UX, and multi-agent swarm capabilities.

---

## ✨ What is Maestrist?

Maestrist is an AI-driven development platform that orchestrates intelligent agents to build, maintain, and deploy software. Think of it as a conductor leading an orchestra of AI agents — each specialized, all synchronized.

### Key Features

- 🤖 **AI Software Agent SDK** — Composable Python library for defining and running agents
- 🎯 **Multi-Agent Orchestration** — Swarm mode for parallel task execution
- 🖥️ **Local GUI** — React-based dashboard with real-time agent interaction
- ⌨️ **CLI Mode** — Terminal-first experience powered by any LLM
- 🔌 **Orcest.ai Integration** — Connect to Orcest workflow orchestration and model routing via [dargah.ai](https://dargah.ai)
- 🐳 **Self-Hosted Excellence** — Docker/Kubernetes ready, one-click deploy
- 🌐 **Global i18n** — 14+ language support out of the box
- 🔐 **Enterprise Ready** — Auth, RBAC, multi-tenancy, Stripe billing

---

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
docker compose up maestrist
```

### Using Render (Cloud Deploy)

Deploy directly to [Render](https://render.com) with our `render.yaml`:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/danialsamiei/agent.orcest.ai)

### Local Development

```bash
# Clone the repo
git clone https://github.com/danialsamiei/agent.orcest.ai.git
cd agent.orcest.ai

# Build everything (backend + frontend)
make build

# Run the application
make run
```

### CLI Mode

```bash
# Install and run via CLI
pip install maestrist-ai
maestrist
```

---

## 🏗️ Architecture

```
maestrist/
├── openhands/              # Core agent framework (Python)
│   ├── agenthub/           # Agent implementations (CodeAct, Browsing, etc.)
│   ├── app_server/         # V1 Application Server (FastAPI)
│   ├── server/             # Legacy V0 Server
│   ├── runtime/            # Runtime environments (Docker, CLI, K8s)
│   ├── llm/                # LLM integrations (OpenAI, Anthropic, etc.)
│   ├── events/             # Event-driven architecture
│   └── storage/            # Data persistence layer
├── frontend/               # React dashboard (TypeScript)
├── enterprise/             # Enterprise features (Auth, Billing, Integrations)
├── skills/                 # Agent skill definitions
├── containers/             # Docker configurations
└── third_party/            # Third-party runtime integrations
```

---

## 🎨 Orcest Ecosystem

Maestrist is designed as a core component of the **Orcest.ai** ecosystem:

| Component | Description |
|-----------|-------------|
| [**Orcest.ai**](https://orcest.ai) | Workflow orchestration platform |
| [**Dargah.ai**](https://dargah.ai) | Multi-model AI gateway & routing |
| **Maestrist** | AI agent coding platform (this repo) |

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

Maestrist is available under the **MIT License** — see the [LICENSE](LICENSE) file for details.

The `enterprise/` directory contains additional functionality under the [Polyform Free Trial License](enterprise/LICENSE).

---

## 🙏 Acknowledgments

- Built upon [OpenHands](https://github.com/All-Hands-AI/OpenHands) by the All Hands AI team
- Powered by the [Orcest.ai](https://orcest.ai) ecosystem
- Inspired by the vision of AI agents conducting a symphony of code

---

<div align="center">
  <strong>🎼 Maestrist: Ignite Your AI Agent Symphony.</strong>
  <br/>
  <em>Masterful Agent Ecosystem for Strategic Task Resolution and Innovative Swarm Technology</em>
  <br/><br/>
  <a href="https://agent.orcest.ai">Live Demo</a> · <a href="https://orcest.ai">Orcest.ai</a> · <a href="https://github.com/danialsamiei/agent.orcest.ai/issues">Report Bug</a>
</div>
