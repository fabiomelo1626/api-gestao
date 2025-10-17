#!/bin/bash
cd /root/API-AGENDA
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 9000
