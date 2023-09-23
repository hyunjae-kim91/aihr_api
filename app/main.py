import time
import uuid
from dataclasses import dataclass, asdict
from fastapi import  FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .predict import predict_router


@dataclass
class AppConfig:
    version: str = "v0.1"
    prefix: str = ""
    title: str = "predict_waiting_time"
    description: str = "predict_waiting_time"


app = FastAPI(**asdict(AppConfig()))


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.middleware("http")
async def add_trace_code_header(request: Request, call_next):
    """uuid를 trace code로 발급"""
    trace_code = request.headers.get("X-Trace-Code")
    if trace_code is None:
        trace_code = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Trace-Code"] = trace_code
    return response


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """api 처리시간"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(predict_router.router)