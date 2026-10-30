"""Small evaluation of the semantic search: does the top result have the expected category?"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import load_documents  # noqa: E402
from semantic_search import SemanticSearch  # noqa: E402

TESTS = [
    ("how do I fix a VPN connection problem", {"kb_article", "manual"}),
    ("steps to install a printer", {"manual"}),
    ("ransomware attack on a laptop", {"incident_report"}),
    ("what must employees do about passwords", {"policy"}),
    ("database server crashed at night", {"incident_report"}),
    ("customer satisfaction results", {"project_report"}),
    ("api endpoint to create a ticket", {"technical_doc"}),
    ("wifi connected but no internet", {"kb_article"}),
    ("backup retention and recovery rules", {"policy"}),
    ("my laptop is very slow", {"kb_article"}),
    ("how to add email to my phone", {"manual"}),
    ("network topology vlan firewall zones", {"technical_doc"}),
]

if __name__ == "__main__":
    engine = SemanticSearch(load_documents())
    for expand in (False, True):
        ok = 0
        print(f"\nSemantic search evaluation (ontology expansion {'ON' if expand else 'OFF'})")
        for q, expected in TESTS:
            hits = engine.search(q, 3, expand)
            top = hits[0][0] if hits else None
            good = top is not None and top["category"] in expected
            ok += good
            print(f"  [{'OK ' if good else 'MISS'}] {q:<42} -> {top['title'] if top else 'none'}")
        print(f"Top-1 category accuracy: {ok}/{len(TESTS)} = {ok / len(TESTS):.0%}")
