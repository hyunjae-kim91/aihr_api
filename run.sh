#!/bin/bash
# gunicorn app:app --bind 0.0.0.0:8000 -w 3 -k uvicorn.workers.UvicornWorker
uvicorn app:app --host 0.0.0.0 --port 8000
