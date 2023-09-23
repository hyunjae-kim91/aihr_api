#!/bin/sh
gunicorn app:app --bind 0.0.0.0:8000 -w 3 -k uvicorn.workers.UvicornWorker