from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
from .database import init_db, get_session
from .models import Term, TermCreate, TermRead, TermUpdate
from .crud import get_terms, get_term_by_id, get_term_by_keyword, create_term, update_term, delete_term
from fastapi.staticfiles import StaticFiles
import uvicorn, os

app = FastAPI(title="Glossary API", version="1.0")

@app.on_event("startup")
def on_startup():
    init_db()

static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

@app.get("/api/terms", response_model=List[TermRead])
def api_list_terms(session: Session = Depends(get_session)):
    return get_terms(session)

@app.get("/api/terms/{keyword}", response_model=TermRead)
def api_get_term(keyword: str, session: Session = Depends(get_session)):
    found = get_term_by_keyword(session, keyword)
    if found:
        return found
    if keyword.isdigit():
        node = get_term_by_id(session, int(keyword))
        if node:
            return node
    raise HTTPException(status_code=404, detail="Term not found")

@app.post("/api/terms", response_model=TermRead, status_code=201)
def api_create_term(payload: TermCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(Term).where(Term.term == payload.term)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Term already exists")
    term = create_term(session, payload)
    return term

@app.put("/api/terms/{term_id}", response_model=TermRead)
def api_update_term(term_id: int, payload: TermUpdate, session: Session = Depends(get_session)):
    term = update_term(session, term_id, payload)
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    return term

@app.delete("/api/terms/{term_id}", status_code=204)
def api_delete_term(term_id: int, session: Session = Depends(get_session)):
    ok = delete_term(session, term_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Term not found")
    return None

@app.get("/api/graph")
def api_graph(session: Session = Depends(get_session)):
    terms = session.exec(select(Term)).all()
    nodes = [{"id": t.id, "label": t.term, "title": t.definition} for t in terms]
    edges = []
    for t in terms:
        for rid in t.related_terms_list:
            if session.get(Term, rid):
                edges.append({"from": t.id, "to": rid})
    return {"nodes": nodes, "edges": edges}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
