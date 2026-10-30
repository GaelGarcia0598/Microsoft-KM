"""Automated document classification with TF-IDF + Naive Bayes / Logistic Regression.

Usage:
    python src/classifier.py                       # train, evaluate, save figures
    python src/classifier.py --text "Step 1: ..."  # classify a new text
    python src/classifier.py --file path/to/doc.txt
"""
import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT, load_documents  # noqa: E402

CATEGORIES = ["policy", "manual", "incident_report", "kb_article", "technical_doc", "project_report"]
SEED = 42


def make_model(kind):
    clf = MultinomialNB(alpha=0.1) if kind == "naive_bayes" else LogisticRegression(max_iter=1000, C=10)
    vec = TfidfVectorizer(lowercase=True, stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
    return make_pipeline(vec, clf)


def train_and_evaluate(docs):
    X = [d["text"] for d in docs]
    y = [d["category"] for d in docs]
    idx = np.arange(len(docs))
    X_tr, X_te, y_tr, y_te, _, i_te = train_test_split(
        X, y, idx, test_size=0.25, stratify=y, random_state=SEED)
    print(f"Documents loaded: {len(docs)}  |  train: {len(X_tr)}  test: {len(X_te)}")
    print(f"Categories: {', '.join(CATEGORIES)}\n")

    results = {}
    for kind in ("naive_bayes", "logistic_regression"):
        model = make_model(kind).fit(X_tr, y_tr)
        pred = model.predict(X_te)
        cv = cross_val_score(make_model(kind), X, y,
                             cv=StratifiedKFold(5, shuffle=True, random_state=SEED))
        results[kind] = (model, pred, accuracy_score(y_te, pred), cv)
        print(f"=== {kind} ===")
        print(f"Test accuracy: {results[kind][2]:.2%}   5-fold CV: {cv.mean():.2%} (+/- {cv.std():.2%})")
        print(classification_report(y_te, pred, labels=CATEGORIES, zero_division=0))

    best = max(results, key=lambda k: results[k][3].mean())
    print(f"Selected model: {best}\n")
    model, pred = results[best][0], results[best][1]
    print("Test-set predictions:")
    for i, p in zip(i_te, pred):
        mark = "OK " if p == docs[i]["category"] else "ERR"
        print(f"  [{mark}] {docs[i]['id']:<20} true={docs[i]['category']:<16} pred={p}")
    save_confusion(y_te, pred, best)
    return model


def save_confusion(y_true, y_pred, name):
    cm = confusion_matrix(y_true, y_pred, labels=CATEGORIES)
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(CATEGORIES)), CATEGORIES, rotation=40, ha="right")
    ax.set_yticks(range(len(CATEGORIES)), CATEGORIES)
    for i in range(len(CATEGORIES)):
        for j in range(len(CATEGORIES)):
            ax.text(j, i, cm[i, j], ha="center", va="center",
                    color="white" if cm[i, j] > cm.max() / 2 else "black")
    ax.set_xlabel("Predicted category")
    ax.set_ylabel("True category")
    ax.set_title(f"Confusion matrix on test set ({name})")
    fig.tight_layout()
    out = ROOT / "evidence" / "confusion_matrix.png"
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, dpi=150)
    print(f"\nConfusion matrix saved to {out}")


def classify_text(model, text):
    probs = model.predict_proba([text])[0]
    ranked = sorted(zip(model.classes_, probs), key=lambda t: -t[1])
    return ranked


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", help="Text of a new document to classify")
    ap.add_argument("--file", help="Path of a new document to classify")
    args = ap.parse_args()

    model = train_and_evaluate(load_documents())

    texts = []
    if args.text:
        texts.append(args.text)
    if args.file:
        texts.append(Path(args.file).read_text(encoding="utf-8"))
    if not texts:
        texts = [
            "Step 1: open Settings. Step 2: click Add device and follow the wizard to install the scanner driver.",
            "The mail server stopped responding at 03:20. The on-call engineer restarted it and the root cause was a full disk.",
            "Employees must not share their credentials. Failure to comply will result in sanctions.",
            "Symptom: the laptop cannot connect to Wi-Fi. Cause: outdated driver. Solution: reinstall the adapter driver.",
            "The system architecture includes an API gateway, three microservices and a PostgreSQL database with defined schemas.",
            "Quarterly report: customer satisfaction rose 8 percent and the project stayed within budget.",
        ]
        print("\nClassification of NEW unseen documents:")
    for t in texts:
        ranked = classify_text(model, t)
        print(f"\n  Text: {t[:90]}{'...' if len(t) > 90 else ''}")
        print(f"  -> Predicted category: {ranked[0][0]} ({ranked[0][1]:.0%})  | 2nd: {ranked[1][0]} ({ranked[1][1]:.0%})")


if __name__ == "__main__":
    main()
