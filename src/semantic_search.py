"""Basic semantic search: TF-IDF vectors + cosine similarity.

Usage:
    python src/semantic_search.py "how do I fix a VPN connection problem" -k 5
    python src/semantic_search.py "laptop slow" --expand     # ontology-based query expansion
    python src/semantic_search.py                            # runs demo queries
"""
import argparse
import sys
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

sys.path.insert(0, str(Path(__file__).parent))
from common import load_documents  # noqa: E402

# Ontology concept -> related terms. Used for optional query expansion so that
# a query using one term also matches documents that use a related term.
CONCEPT_LEXICON = {
    "vpn": ["remote access", "tunnel", "gateway", "certificate"],
    "slow": ["performance", "freeze", "disk usage", "startup"],
    "email": ["outlook", "mail", "exchange", "mailbox", "smtp"],
    "wifi": ["wireless", "access point", "network", "dhcp"],
    "password": ["credentials", "authentication", "account", "locked"],
    "attack": ["ransomware", "phishing", "malicious", "security"],
    "crash": ["outage", "downtime", "unavailable", "stopped responding"],
    "backup": ["restore", "recovery", "retention", "storage"],
}


def expand_query(query):
    q = query.lower()
    extra = [t for key, related in CONCEPT_LEXICON.items() if key in q for t in related]
    return f"{query} {' '.join(extra)}" if extra else query


class SemanticSearch:
    def __init__(self, docs):
        self.docs = docs
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words="english",
                                          ngram_range=(1, 2), sublinear_tf=True)
        self.matrix = self.vectorizer.fit_transform([d["text"] for d in docs])

    def search(self, query, k=5, expand=False):
        if expand:
            query = expand_query(query)
        qvec = self.vectorizer.transform([query])             # query -> TF-IDF vector
        scores = cosine_similarity(qvec, self.matrix)[0]      # cosine similarity
        order = scores.argsort()[::-1][:k]
        return [(self.docs[i], float(scores[i])) for i in order if scores[i] > 0]


def show(engine, query, k, expand):
    print(f'\nQuery: "{query}"' + ("  [ontology expansion ON]" if expand else ""))
    hits = engine.search(query, k, expand)
    if not hits:
        print("  No relevant documents found.")
    for rank, (doc, score) in enumerate(hits, 1):
        print(f"  {rank}. [{score:.3f}] ({doc['category']}) {doc['title']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?", help="Natural language query")
    ap.add_argument("-k", type=int, default=5, help="Number of results")
    ap.add_argument("--expand", action="store_true", help="Expand the query with ontology concepts")
    args = ap.parse_args()

    engine = SemanticSearch(load_documents())
    print(f"Index built: {len(engine.docs)} documents, {len(engine.vectorizer.vocabulary_)} TF-IDF terms")
    queries = [args.query] if args.query else [
        "how do I fix a VPN connection problem",
        "what is the procedure when a user forgets or must change a password",
        "ransomware attack on a laptop",
        "steps to install a printer",
        "database server down because of disk full",
        "customer satisfaction and SLA results",
    ]
    for q in queries:
        show(engine, q, args.k, args.expand)
    if not args.query:
        show(engine, "my laptop is very slow", args.k, False)
        show(engine, "my laptop is very slow", args.k, True)


if __name__ == "__main__":
    main()
