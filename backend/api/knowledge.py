import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.api.auth import require_role
from backend.models.user import User
from backend.models.document import Document, DocumentChunk
from backend.utils.validators import is_allowed_upload
from backend.services import rag_service
from ai.rag.chunker import chunk_text
from ai.rag.ingest import extract_text_from_file

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "educational_content", "_uploads")


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    subject: str = Form(...),
    topic: str = Form(...),
    title: str = Form(...),
    author: str = Form(""),
    url: str = Form(""),
    license: str = Form("Open Educational Resource"),
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher", "admin")),
):
    contents = await file.read()
    ok, message = is_allowed_upload(file.filename, len(contents))
    if not ok:
        raise HTTPException(status_code=400, detail=message)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    document = Document(
        title=title, subject=subject, topic=topic, author=author,
        source_url=url, license=license, file_path=file_path,
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    return {"message": "Document uploaded. Call /api/knowledge/ingest to index it.", "document_id": document.id}


@router.post("/ingest")
def ingest_document(document_id: int, db: Session = Depends(get_db),
                     user: User = Depends(require_role("teacher", "admin"))):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    text = extract_text_from_file(document.file_path)
    chunks = chunk_text(text)

    for idx, chunk in enumerate(chunks):
        db.add(DocumentChunk(document_id=document.id, chunk_index=idx, content=chunk,
                              section=f"Section {idx + 1}"))
    db.commit()

    rag_service.build_index(db)
    return {"message": f"Ingested {len(chunks)} chunks from '{document.title}'.", "chunk_count": len(chunks)}


@router.get("/search")
def search_knowledge(query: str, db: Session = Depends(get_db),
                      user: User = Depends(require_role("student", "teacher", "admin"))):
    results = rag_service.retrieve(db, query, top_k=5)
    return results


@router.get("/resources")
def list_resources(db: Session = Depends(get_db),
                    user: User = Depends(require_role("student", "teacher", "admin"))):
    documents = db.query(Document).all()
    grouped: dict[str, int] = {}
    for d in documents:
        grouped[d.subject] = grouped.get(d.subject, 0) + 1
    return {"by_subject": grouped, "total": len(documents)}
