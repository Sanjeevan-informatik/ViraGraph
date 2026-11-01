"""Optional FastAPI entrypoints. Install viragraph[api] to enable."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .core import parse_fasta, summary
from .graph import build_graph

app = FastAPI(title="ViraGraph API", version="0.1.0")

class FastaPayload(BaseModel):
    fasta: str = Field(min_length=1, max_length=2_000_000)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.post("/v1/summary")
def sequence_summary(payload: FastaPayload) -> dict:
    try:
        return summary(parse_fasta(payload.fasta))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

@app.post("/v1/graph")
def sequence_graph(payload: FastaPayload) -> dict:
    try:
        return build_graph(parse_fasta(payload.fasta))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
