# Render Deployment – agent.orcest.ai

## تنظیمات ضروری

### 1. Build Command

```
cd frontend && npm ci && npm run build && cd .. && uv sync
```

### 2. Start Command

```
uv run -- uvicorn openhands.server.listen:app --host 0.0.0.0 --port $PORT
```

### 3. Health Check Path: `/health`

### 4. متغیرهای محیطی (Environment Variables)

| متغیر | مقدار | توضیح |
|-------|-------|--------|
| `RUNTIME` | `cli` | CLIRuntime: بدون نیاز به tmux یا Docker |
| `SKIP_DEPENDENCY_CHECK` | `1` | رد شدن از بررسی وابستگی‌ها |
| `WORKSPACE_BASE` | `/tmp/workspace` | مسیر workspace |
| `OH_SECRET_KEY` | (Generate) | حفظ secrets بین restart |
| `PYTHON_VERSION` | `3.12.12` | تضمین نصب Python سازگار با `>=3.12,<3.14` برای `uv sync` |

### 5. کلید API

- `OPENAI_API_KEY` – برای GPT-4o
- یا `ANTHROPIC_API_KEY` – برای Claude
- یا در رابط وب از **Settings → LLM** وارد کنید

---

## Deploy

بعد از تنظیم env vars، **Manual Deploy** با **Clear build cache** بزنید.
