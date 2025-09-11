#!/bin/bash
cd /root/api-saude
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 7000
