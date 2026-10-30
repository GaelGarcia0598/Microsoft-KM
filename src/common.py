"""Shared helpers: corpus loading and text utilities."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC_DIR = ROOT / "data" / "documents"


def load_documents(doc_dir=DOC_DIR):
    """Return a list of dicts: id, category, title, text (title + body)."""
    docs = []
    for path in sorted(Path(doc_dir).rglob("*.txt")):
        raw = path.read_text(encoding="utf-8").strip()
        title, _, body = raw.partition("\n")
        docs.append({
            "id": path.stem,
            "category": path.parent.name,
            "title": title.strip(),
            "text": f"{title} {body}".strip(),
        })
    if not docs:
        raise SystemExit(f"No documents found in {doc_dir}. Run build_corpus.py first.")
    return docs
