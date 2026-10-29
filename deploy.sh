#!/usr/bin/env bash
# Despliegue a staging: levanta la app, comprueba que responde y la apaga
set -euo pipefail

setsid .venv/bin/python app.py > app.log 2>&1 &
PID=$!
trap 'kill -- -"$PID" 2>/dev/null || true' EXIT

for i in $(seq 1 15); do
  if curl -fsS http://localhost:5000/health 2>/dev/null; then
    echo
    echo "Desplegado en staging y respondiendo"
    exit 0
  fi
  sleep 1
done

echo "La app no respondió en 15 segundos:"
cat app.log
exit 1
