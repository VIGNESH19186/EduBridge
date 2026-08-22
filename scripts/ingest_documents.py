"""
Bulk-ingest all files under data/educational_content/ (excluding _uploads,
which is handled via the API) into the documents/document_chunks tables.

Run with:
    python scripts/ingest_documents.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.database.database import SessionLocal, Base, engine  # noqa: E402
from backend.models.document import Document, DocumentChunk  # noqa: E402
from backend.services import rag_service  # noqa: E402
from ai.rag.ingest import extract_text_from_file  # noqa: E402
from ai.rag.chunker import chunk_text  # noqa: E402

CONTENT_ROOT = os.path.join(os.path.dirname(__file__), "..", "data", "educational_content")


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    ingested = 0
    try:
        for subject_dir in os.listdir(CONTENT_ROOT):
            full_dir = os.path.join(CONTENT_ROOT, subject_dir)
            if not os.path.isdir(full_dir) or subject_dir == "_uploads":
                continue
            for filename in os.listdir(full_dir):
                file_path = os.path.join(full_dir, filename)
                if not os.path.isfile(file_path):
                    continue

                existing = db.query(Document).filter(Document.file_path == file_path).first()
                if existing:
                    continue

                title = filename.rsplit(".", 1)[0].replace("_", " ").title()
                document = Document(title=title, subject=subject_dir.replace("_", " ").title(),
                                     topic="", author="EduBridge Content Team",
                                     license="Open Educational Resource", file_path=file_path)
                db.add(document)
                db.commit()
                db.refresh(document)

                text = extract_text_from_file(file_path)
                chunks = chunk_text(text)
                for idx, chunk in enumerate(chunks):
                    db.add(DocumentChunk(document_id=document.id, chunk_index=idx,
                                          content=chunk, section=f"Section {idx + 1}"))
                db.commit()
                ingested += 1
                print(f"Ingested: {title} ({len(chunks)} chunks)")

        rag_service.build_index(db)
        print(f"\nDone. {ingested} new documents ingested.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
