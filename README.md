# Microsoft: Knowledge Management System (prototype)

Course project for *Sistemas y tecnologías de administración del conocimiento*.
Organization: **Microsoft** (as in Activity 1). The sample documents are synthetic, written in the style of Microsoft support, cloud, security and management documents; they are not real internal documents.

## Contents

| Path | Description |
|---|---|
| `data/documents/<category>/*.txt` | 48 sample documents in 6 categories (policy, manual, incident_report, kb_article, technical_doc, project_report) |
| `src/classifier.py` | Automated classification: TF-IDF + Naive Bayes / Logistic Regression |
| `src/semantic_search.py` | Semantic search: TF-IDF + cosine similarity (optional ontology query expansion) |
| `src/evaluate_search.py` | Evaluation of the search with 12 queries |
| `ontology/MicrosoftKM.owl` | Ontology (15 classes, 20 object properties); `ITSupportOntology_Activity2.owl` is the base from Activity 2 |
| `src/build_diagrams.py` | Generates the OWL file, ontology graphs and lifecycle map |
| `src/make_screenshots.py`, `src/build_report.py` | Evidence images and the PDF report |
| `evidence/` | Diagrams, console outputs and screenshots |
| `docs/Microsoft_KM_Project_Progress.pdf` | Project progress document |

## Run

```bash
pip install -r requirements.txt
python build_corpus.py            # (re)creates the document set
python src/classifier.py          # train, evaluate and classify new documents
python src/classifier.py --text "Step 1: open Settings. Step 2: click Add device."
python src/semantic_search.py "how do I fix a VPN connection problem" -k 5
python src/semantic_search.py "my laptop is very slow" --expand
python src/evaluate_search.py
```

## Results (48 documents)

- Classification: 100% on the 12-document test set; 5-fold CV 91.8% (Naive Bayes) and 95.8% (Logistic Regression).
- Search: expected category as top result in 11 of 12 test queries (92%).

The document set is small and synthetic; results demonstrate the method, not production accuracy.
