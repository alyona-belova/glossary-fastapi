from sqlmodel import SQLModel, Field
from typing import Optional, List
import json

class TermBase(SQLModel):
    term: str
    definition: str
    sources: Optional[str] = None
    related_terms: Optional[str] = None

class Term(TermBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    @property
    def related_terms_list(self) -> List[int]:
        return json.loads(self.related_terms) if self.related_terms else []

class TermCreate(TermBase):
    pass

class TermRead(TermBase):
    id: int

class TermUpdate(SQLModel):
    term: Optional[str] = None
    definition: Optional[str] = None
    sources: Optional[str] = None
    related_terms: Optional[str] = None
