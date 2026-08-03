"""Thin HTTP surface over the Inception runtime (FastAPI). The engine is the source of truth;
this just exposes seed/incept/twin/replay/revoke/dry-run over HTTP with fail-closed status codes."""
from __future__ import annotations
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from .engine import InceptionEngine
from .organs import ReadOnlyAdapter, RetrieverOrgan

_LOG = Path(os.environ.get("INCEPTION_LOG", "/tmp/inception/events.jsonl"))
app = FastAPI(title="Inception runtime", version="0.1.0")
engine = InceptionEngine(_LOG)
adapter = ReadOnlyAdapter(engine)
retriever = RetrieverOrgan(engine)

@app.post("/twins/incept")
def incept(seed: dict):
    if "seed_id" not in seed:
        raise HTTPException(422, "seed_id required")
    state = engine.incept(seed)
    code = 201 if state["status"] == "READY" else 202
    return {"state": state, "http": code}

@app.get("/twins/{twin_id}")
def status(twin_id: str):
    return adapter.status(twin_id)

@app.get("/twins/{twin_id}/replay")
def replay(twin_id: str):
    ok, broken = engine.verify_chain()
    if not ok:
        raise HTTPException(409, f"receipt chain broken at index {broken}")
    return engine.replay(twin_id)

@app.post("/twins/{twin_id}/revoke")
def revoke(twin_id: str):
    try:
        return engine.revoke(twin_id)
    except KeyError:
        raise HTTPException(404, "twin not found")

@app.post("/twins/{twin_id}/dry-run")
def dry_run(twin_id: str, body: dict):
    r = adapter.dry_run(twin_id, body.get("action", "noop"))
    if not r["ok"]:
        raise HTTPException(409, r["reason"])
    return r
