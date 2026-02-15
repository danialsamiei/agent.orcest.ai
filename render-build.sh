#!/bin/bash
set -e
# Render.com build: Python deps + frontend build
uv sync --frozen && uv cache prune --ci
cd frontend && npm ci --ignore-scripts && npm run build && cd ..
