# Report, lab 05

Fill this in as you go. Write in your own words.

**Name: Sobar Danil**
**Group: PO 25-Z**
**Date: 10.11.26**

## What works

Tick only what works. "Almost works" is not ticked.

- [x] M1: the app answers `GET /tasks`
- [x] M2: `TaskIn`, `TaskPatch` and `Task` pass the shell checks
- [x] M3: all six routes and the 404 handler. Bruno, fastapi: 13 of 13
- [x] M4: tasks survive a restart
- [x] M5: one log line per request
- [x] Both servers: socket 13 of 13, fastapi 13 of 13

## The traceback from M3

Paste the last six lines of the traceback you got for `GET /tasks/999` before the handler existed. Mark the frames that are in your files.

```
    result = context.run(func, *args)
  File "…/main.py", line 60, in get_task          <-- my file
    return store.get(task_id)
  File "…/storage.py", line 49, in get            <-- my file
    raise TaskNotFound(task_id)
errors.TaskNotFound: Task 999 not found           <-- my errors.py
```

## The same request, two servers

| Request | Lab 04 (socket) | Lab 05 (FastAPI) |
|---|---|---|
| `POST /tasks`, body `{"title": "x"` | `400`, body `<h1>Bad Request</h1>` (HTML) | `422`, JSON: `{"detail":[{"type":"json_invalid","loc":["body",13],...}]}` |
| `GET /tasks/abc` | `400`, body `<h1>Bad Request</h1>` (HTML) | `422`, JSON: `{"detail":[{"type":"int_parsing","loc":["path","task_id"],...}]}` |
| `PATCH /tasks/1`, body `{"done": "yes"}` | `422`, `{"detail": "done must be true or false"}` | `200`, `done` becomes `true` |

Which answer is better for each row, and why? One line each.

- **Broken JSON:** FastAPI is better: its JSON error says the JSON is broken and where, while the socket server sends a bare HTML "Bad Request".
- **`/tasks/abc`:** FastAPI is better: `loc` points to `path` and `task_id`, so the client knows which part was wrong; the socket server gives only an HTML page.
- **`done: "yes"`:** the socket server is better: a string is not a boolean, and FastAPI quietly turns `"yes"` into `true` (Pydantic lax mode), which hides a client mistake.

## What FastAPI did for you

For each line, name the place in your lab 04 code (file and function) that did the same job by hand. Then name what does it in lab 05.

| Job | Lab 04: where you wrote it | Lab 05: what does it |
|---|---|---|
| reading the body to `Content-Length` | `server.py`, `handle_client` (the `conn.recv` loop for POST, PUT, PATCH) | Uvicorn and Starlette read the body before the route is called |
| turning the JSON text into a dict | `tasks.py`, `create_task`, `replace_task`, `patch_task` (`json.loads(body)`) | FastAPI parses the body and Pydantic builds `TaskIn` or `TaskPatch` |
| `"7"` from the path becoming the number 7 | `tasks.py`, `get_task`, `replace_task`, `patch_task`, `delete_task` (`int(task_id)`) | the type hint `task_id: int` in the route |
| checking that `title` is there and not blank | `tasks.py`, `check_new` (and `check_patch` for PATCH) | `TaskIn` and `TaskPatch` in `schemas.py` (`Field` and the validators) |
| answering 405 for `PATCH /tasks` | `router.py`, `path_exists`, used in `server.py`, `handle_client` | FastAPI's router, automatically |
| turning the result into JSON bytes with a status line | `server.py`, `respond` and `respond_json` | `response_model=Task` and `status_code=...` on each route |

How many lines is your `tasks.py` from lab 04? **124 lines.**

How many lines are your `schemas.py`, `storage.py` and `main.py` together, without M4 and M5? **136 lines** (`schemas.py` 44, `storage.py` 41, `main.py` 51).