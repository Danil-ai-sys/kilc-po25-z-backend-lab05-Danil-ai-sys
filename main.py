"""The app: routes, the error handler, logging. Run it with: fastapi dev main.py"""

import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from config import settings

logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(levelname)-7s %(name)s: %(message)s",
)

from errors import TaskNotFound  # noqa: E402
from models import Task  # noqa: E402
from schemas import TaskIn, TaskPatch  # noqa: E402
from storage import Storage  # noqa: E402

logger = logging.getLogger(__name__)

app = FastAPI(title="Tasks API")
store = Storage(settings.data_file)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("%s %s -> unhandled error", request.method, request.url.path)
        raise
    ms = (time.perf_counter() - start) * 1000
    logger.info("%s %s -> %d (%.1f ms)", request.method, request.url.path, response.status_code, ms)
    return response


@app.exception_handler(TaskNotFound)
def task_not_found(request: Request, exc: TaskNotFound) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": f"Task {exc.task_id} not found", "code": "task_not_found"},
    )


@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    return store.get_all()


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskIn) -> Task:
    return store.add(payload)


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    return store.get(task_id)


@app.put("/tasks/{task_id}", response_model=Task)
def replace_task(task_id: int, payload: TaskIn) -> Task:
    return store.update(task_id, payload.model_dump())


@app.patch("/tasks/{task_id}", response_model=Task)
def patch_task(task_id: int, payload: TaskPatch) -> Task:
    return store.update(task_id, payload.model_dump(exclude_unset=True))


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    store.delete(task_id)
