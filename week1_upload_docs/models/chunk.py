from pydantic import BaseModel

class Chunk(BaseModel):
    doc_id: str
    chunk_id: int
    text: str
