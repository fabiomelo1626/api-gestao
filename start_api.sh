#!/bin/bash
cd /root/api-gestao
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 9000
