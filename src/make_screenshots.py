"""Renders real console output of the prototype as terminal-style screenshots (evidence/*.png)."""
import subprocess
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable


def run(args):
    r = subprocess.run([PY, *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                       env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
    return r.stdout.rstrip("\n")


def render(command, text, name, lines=None):
    rows = text.split("\n")
    if lines:
        rows = rows[lines[0]:lines[1]]
    h = max(2.0, 0.205 * (len(rows) + 3))
    fig = plt.figure(figsize=(12.5, h), facecolor="#0c0c0c")
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off"); ax.set_facecolor("#0c0c0c")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.text(0.01, 1 - 0.55 / h, f"PS NovaTech-KM> {command}", color="#4ec9b0", family="monospace", fontsize=9.5, va="top")
    ax.text(0.01, 1 - 1.0 / h, "\n".join(rows), color="#cccccc", family="monospace", fontsize=9, va="top",
            linespacing=1.3)
    out = ROOT / "evidence" / name
    fig.savefig(out, dpi=140, facecolor=fig.get_facecolor()); plt.close(fig)
    print("Wrote", out)


if __name__ == "__main__":
    clf = run(["src/classifier.py"])
    rows = clf.split("\n")
    split = next(i for i, r in enumerate(rows) if r.startswith("Test-set predictions"))
    new = next(i for i, r in enumerate(rows) if r.startswith("Classification of NEW"))
    render("python src/classifier.py   (training and evaluation)", "\n".join(rows[:split]), "screenshot_classifier_training.png")
    render("python src/classifier.py   (test predictions and new documents)", "\n".join(rows[split:]),
           "screenshot_classifier_predictions.png")
    render('python src/semantic_search.py "how do I fix a VPN connection problem"',
           run(["src/semantic_search.py", "how do I fix a VPN connection problem"]), "screenshot_search_vpn.png")
    render('python src/semantic_search.py "steps to install a printer"',
           run(["src/semantic_search.py", "steps to install a printer"]), "screenshot_search_printer.png")
    srch = run(["src/semantic_search.py"]).split("\n")
    i = next(i for i, r in enumerate(srch) if "my laptop is very slow" in r)
    render('python src/semantic_search.py   (demo, with and without ontology expansion)', "\n".join(srch[i - 1:]),
           "screenshot_search_expansion.png")
    render("python src/evaluate_search.py", run(["src/evaluate_search.py"]), "screenshot_search_evaluation.png")
