from sqlmodel import Session, select
from .models import Term, TermCreate, TermUpdate

def get_terms(session: Session):
    return session.exec(select(Term)).all()

def get_term_by_id(session: Session, term_id: int):
    return session.get(Term, term_id)

def get_term_by_keyword(session: Session, keyword: str):
    return session.exec(select(Term).where(Term.term == keyword)).first()

def create_term(session: Session, payload: TermCreate):
    term = Term.from_orm(payload)
    session.add(term)
    session.commit()
    session.refresh(term)
    return term

def update_term(session: Session, term_id: int, payload: TermUpdate):
    term = session.get(Term, term_id)
    if not term:
        return None
    data = payload.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(term, key, value)
    session.add(term)
    session.commit()
    session.refresh(term)
    return term

def delete_term(session: Session, term_id: int):
    term = session.get(Term, term_id)
    if not term:
        return False
    session.delete(term)
    session.commit()
    return True
