# Render Deployment – agent.orcest.ai

## تنظیمات ضروری

### 1. Build Command

```
apt-get update && apt-get install -y tmux && cd frontend && npm ci && npm run build && cd .. && uv sync
```

### 2. Start Command

```
uv run -- uvicorn openhands.server.listen:app --host 0.0.0.0 --port $PORT
```

### 3. Health Check Path: `/health`

### 4. متغیرهای محیطی الزامی

در **Environment** این متغیرها را اضافه کنید:

| متغیر | مقدار | توضیح |
|-------|-------|--------|
| `OH_APP_MODE` | `oss` | صفحه اصلی از `/` بدون ریدایرکت به login |
| `RUNTIME` | `local` | بدون Docker روی Render (LocalRuntime) |
| `WORKSPACE_BASE` | `/tmp/workspace` | مسیر workspace برای sandbox |
| `OH_SECRET_KEY` | (Generate) | حفظ secrets بین ری‌استارت‌ها |

### 5. کلید API (در Settings یا Environment)

یکی از این متغیرها را برای مدل پیش‌فرض تنظیم کنید:

- `OPENAI_API_KEY` – برای GPT-4o
- `ANTHROPIC_API_KEY` – برای Claude

یا پس از ورود، از **Settings → LLM** کلید API را وارد کنید.

---

## رفع خطای ۵۰۰ در New Conversation

اگر بعد از لاگین و وارد کردن API key خطای ۵۰۰ می‌گیرید:

1. `RUNTIME=local` را حتماً تنظیم کنید (Render بدون Docker است)
2. `WORKSPACE_BASE=/tmp/workspace` را اضافه کنید
3. در Build Command نصب `tmux` را اضافه کنید (LocalRuntime به آن نیاز دارد)
4. مطمئن شوید کلید API در Settings ذخیره شده است
5. یک بار سرویس را Manual Deploy کنید

---

## Blueprint

با `render.yaml` این تنظیمات به‌صورت خودکار اعمال می‌شوند.
