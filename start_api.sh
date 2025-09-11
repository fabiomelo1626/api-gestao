#!/bin/bash
cd /root/api-saude
/root/api-saude/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 7000
