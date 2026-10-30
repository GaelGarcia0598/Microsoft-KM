"""Builds the NovaTech knowledge ontology (OWL/RDF-XML), the ontology graphs and the lifecycle map.

Extends the IT Technical Support ontology from Activity 2 with document types,
topics, departments and lifecycle stages.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parent.parent
NS = "http://example.org/ontologies/novatech-km#"

NAVY, BLUE, RED, GOLD, GREY = "#17365d", "#d9e9f6", "#c0392b", "#fff0c8", "#7a8794"

# (class, parent, comment)
CLASSES = [
    ("Incident", None, "A reported disruption affecting an IT system (from Activity 2)."),
    ("Technician", None, "A support specialist who resolves incidents and authors documents."),
    ("System", None, "Application, service or infrastructure component supported by NovaTech."),
    ("Tool", None, "Software or utility used to diagnose or fix incidents."),
    ("Customer", None, "A client or user who reports an incident."),
    ("Topic", None, "A subject area used to classify knowledge (VPN, Email, Security...)."),
    ("Department", None, "An organizational unit that owns knowledge."),
    ("LifecycleStage", None, "A stage of the knowledge life cycle."),
    ("Document", None, "Explicit knowledge stored by NovaTech."),
    ("Policy", "Document", "Rules and obligations (security, privacy, change management)."),
    ("Manual", "Document", "Step-by-step user guide or operating instructions."),
    ("IncidentReport", "Document", "Record of an incident: timeline, root cause and corrective action."),
    ("KBArticle", "Document", "Troubleshooting article: symptom, cause and solution."),
    ("TechnicalDoc", "Document", "Architecture, specification, API or configuration reference."),
    ("ProjectReport", "Document", "Performance, progress, audit and closure reports."),
]

# (property, domain, range, comment)
OBJECT_PROPS = [
    ("reportedBy", "Incident", "Customer", "Incident was reported by a customer."),
    ("affects", "Incident", "System", "Incident disrupts a system."),
    ("resolves", "Technician", "Incident", "Technician resolves an incident."),
    ("uses", "Technician", "Tool", "Technician uses a tool."),
    ("supports", "Tool", "System", "Tool supports a system."),
    ("dependsOn", "System", "System", "System relies on another system."),
    ("documents", "Document", "Incident", "Document records or explains an incident."),
    ("describes", "Document", "System", "Document describes a system."),
    ("aboutTopic", "Document", "Topic", "Document belongs to a topic."),
    ("authoredBy", "Document", "Technician", "Document was written by a technician."),
    ("ownedBy", "Document", "Department", "Department responsible for the document."),
    ("inStage", "Document", "LifecycleStage", "Current lifecycle stage of the document."),
    ("memberOf", "Technician", "Department", "Technician belongs to a department."),
    ("supersedes", "Document", "Document", "A newer document replaces an older one."),
    ("relatedTo", "Document", "Document", "Documents that complement each other."),
    ("derivedFrom", "KBArticle", "IncidentReport", "KB article created from a resolved incident report."),
    ("solves", "KBArticle", "Incident", "KB article gives the fix for a type of incident."),
    ("governs", "Policy", "System", "Policy sets rules for a system."),
    ("guides", "Manual", "Customer", "Manual instructs users."),
    ("summarizes", "ProjectReport", "Incident", "Report aggregates incident metrics."),
]

DATA_PROPS = [
    ("title", "Document"), ("version", "Document"), ("lastReviewed", "Document"),
    ("incidentId", "Incident"), ("priorityLevel", "Incident"), ("status", "Incident"),
    ("name", "Technician"), ("specialty", "Technician"),
]

INDIVIDUALS = [  # (id, class, [(prop, target)])
    ("VPN_Service", "System", []), ("Email_Service", "System", []),
    ("Topic_VPN", "Topic", []), ("Topic_Security", "Topic", []),
    ("Dept_Support", "Department", []), ("Dept_Operations", "Department", []),
    ("Stage_Share", "LifecycleStage", []), ("Stage_Apply", "LifecycleStage", []),
    ("Carlos_Ruiz", "Technician", [("memberOf", "Dept_Support"), ("resolves", "INC-1001")]),
    ("INC-1001", "Incident", [("affects", "VPN_Service")]),
    ("IR-INC-1001", "IncidentReport", [("documents", "INC-1001"), ("aboutTopic", "Topic_VPN"),
                                       ("authoredBy", "Carlos_Ruiz"), ("ownedBy", "Dept_Operations")]),
    ("KB-201", "KBArticle", [("derivedFrom", "IR-INC-1001"), ("solves", "INC-1001"),
                             ("aboutTopic", "Topic_VPN"), ("describes", "VPN_Service"),
                             ("inStage", "Stage_Share")]),
    ("Policy-Remote-Work", "Policy", [("governs", "VPN_Service"), ("aboutTopic", "Topic_Security"),
                                      ("relatedTo", "KB-201")]),
]


def write_owl():
    o = ['<?xml version="1.0"?>',
         f'<rdf:RDF xmlns="{NS}" xml:base="{NS[:-1]}"',
         '     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"',
         '     xmlns:owl="http://www.w3.org/2002/07/owl#"',
         '     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"',
         '     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">',
         f'  <owl:Ontology rdf:about="{NS[:-1]}">',
         '    <rdfs:label>NovaTech Knowledge Management Ontology</rdfs:label>',
         '    <rdfs:comment>Extends the IT Technical Support ontology with document types, topics, departments and lifecycle stages.</rdfs:comment>',
         '  </owl:Ontology>']
    for name, parent, comment in CLASSES:
        o.append(f'  <owl:Class rdf:about="{NS}{name}"><rdfs:label>{name}</rdfs:label>'
                 f'<rdfs:comment>{comment}</rdfs:comment>'
                 + (f'<rdfs:subClassOf rdf:resource="{NS}{parent}"/>' if parent else '') + '</owl:Class>')
    for p, d, r, c in OBJECT_PROPS:
        o.append(f'  <owl:ObjectProperty rdf:about="{NS}{p}"><rdfs:label>{p}</rdfs:label>'
                 f'<rdfs:comment>{c}</rdfs:comment><rdfs:domain rdf:resource="{NS}{d}"/>'
                 f'<rdfs:range rdf:resource="{NS}{r}"/></owl:ObjectProperty>')
    for p, d in DATA_PROPS:
        o.append(f'  <owl:DatatypeProperty rdf:about="{NS}{p}"><rdfs:label>{p}</rdfs:label>'
                 f'<rdfs:domain rdf:resource="{NS}{d}"/><rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>'
                 '</owl:DatatypeProperty>')
    for ind, cls, props in INDIVIDUALS:
        body = ''.join(f'<{p} rdf:resource="{NS}{t}"/>' for p, t in props)
        o.append(f'  <owl:NamedIndividual rdf:about="{NS}{ind}"><rdf:type rdf:resource="{NS}{cls}"/>{body}</owl:NamedIndividual>')
    o.append('</rdf:RDF>')
    out = ROOT / "ontology" / "NovaTechKM.owl"
    out.write_text("\n".join(o), encoding="utf-8")
    print("Wrote", out, f"({len(CLASSES)} classes, {len(OBJECT_PROPS)} object properties)")


def box(ax, xy, text, w=2.6, h=0.9, fc=BLUE, ec=NAVY, fs=10, bold=True):
    x, y = xy
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=fc, ec=ec, lw=2, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=NAVY,
            fontweight="bold" if bold else "normal", zorder=4)


def arrow(ax, p1, p2, label=None, rad=0.0, color=RED, style="-|>", ls="-", lw=1.8, lpos=0.5, fs=8.5, dy=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=14, lw=lw, color=color,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=2,
                                 shrinkA=22, shrinkB=22))
    if label:
        x = p1[0] + (p2[0] - p1[0]) * lpos
        y = p1[1] + (p2[1] - p1[1]) * lpos + dy
        ax.text(x, y, label, fontsize=fs, color=color, ha="center", va="center", fontweight="bold",
                bbox=dict(fc="white", ec="none", pad=1.0), zorder=5)


def _old_ontology_graph():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(-10, 13); ax.set_ylim(-5.2, 8); ax.axis("off")
    ax.set_title("NovaTech Knowledge Ontology: domain concepts, document types and relations",
                 fontsize=16, color=NAVY, fontweight="bold")
    P = {"Document": (1, 2), "Topic": (1, 6.3), "System": (7, 5), "Incident": (7, 1.8),
         "Customer": (11, 1.8), "Tool": (11, 5), "Technician": (-6, 3.2), "Department": (-6, 6.5),
         "LifecycleStage": (-6, 0)}
    for n, p in P.items():
        box(ax, p, n, w=3.0 if n == "Document" else 2.6, fc="#c3dcf2" if n == "Document" else BLUE)
    rel = [("Document", "Topic", "aboutTopic", 0, .5), ("Document", "System", "describes", -.15, .5),
           ("Document", "Incident", "documents", 0, .5), ("Technician", "Document", "authoredBy (inverse)", .0, .5),
           ("Document", "Department", "ownedBy", -.2, .55), ("Document", "LifecycleStage", "inStage", 0, .5),
           ("Technician", "Department", "memberOf", 0, .5), ("Technician", "Incident", "resolves", .22, .5),
           ("Incident", "System", "affects", 0, .5), ("Incident", "Customer", "reportedBy", 0, .5),
           ("Tool", "System", "supports", 0, .5)]
    for a, b, l, rad, lp in rel:
        arrow(ax, P[a], P[b], l, rad, lpos=lp)
    arrow(ax, P["Technician"], P["Tool"], "uses", -0.25, lpos=.5, dy=0)
    ax.text(7, 6.4, "System dependsOn System", ha="center", fontsize=8.5, color=RED, fontweight="bold")
    ax.text(1, 3.55, "supersedes / relatedTo (Document-Document)", ha="center", fontsize=8.5, color=RED, fontweight="bold")
    subs = ["Policy", "Manual", "IncidentReport", "KBArticle", "TechnicalDoc", "ProjectReport"]
    xs = [-7.5, -4.2, -0.9, 2.4, 5.7, 9.0]
    for n, x in zip(subs, xs):
        box(ax, (x, -3.6), n, w=2.9, fc=GOLD, ec="#b58a00", fs=10)
        arrow(ax, (x, -3.6), (1, 2), None, 0.0, color=GREY, ls="--", lw=1.4)
    ax.text(1, -1.0, "subClassOf Document", ha="center", fontsize=10, color=GREY, fontweight="bold",
            bbox=dict(fc="white", ec="none"))
    ax.text(1, -4.85, "Blue boxes = domain concepts (Activity 2 classes + new classes)   |   Gold boxes = document types   |   "
            "Red arrows = object properties (domain to range)   |   Dashed = subclass",
            ha="center", fontsize=9, color=GREY)
    fig.tight_layout()
    out = ROOT / "evidence" / "ontology_graph.png"
    fig.savefig(out, dpi=150); plt.close(fig); print("Wrote", out)


def _old_doc_concept_graph():
    fig, ax = plt.subplots(figsize=(14, 8.2))
    ax.set_xlim(-1, 15); ax.set_ylim(-0.8, 9); ax.axis("off")
    ax.set_title("Relations between document types and domain concepts", fontsize=16, color=NAVY, fontweight="bold")
    docs = [("Policy", 8), ("Manual", 6.7), ("IncidentReport", 5.4), ("KBArticle", 4.1),
            ("TechnicalDoc", 2.8), ("ProjectReport", 1.5)]
    concepts = {"System": 7.8, "Customer": 6.4, "Incident": 4.9, "Topic": 3.4, "Technician": 2.1, "Department": 0.7}
    D = {n: (2, y) for n, y in docs}
    C = {n: (12, y) for n, y in concepts.items()}
    for n, p in D.items():
        box(ax, p, n, w=3.0, fc=GOLD, ec="#b58a00", h=0.75)
    for n, p in C.items():
        box(ax, p, n, w=2.6, h=0.75)
    links = [("Policy", "System", "governs", .0), ("Manual", "Customer", "guides", .0),
             ("IncidentReport", "Incident", "documents", .0), ("KBArticle", "Incident", "solves", .08),
             ("TechnicalDoc", "System", "describes", -.12), ("ProjectReport", "Incident", "summarizes", -.1),
             ("IncidentReport", "Technician", "authoredBy", .0), ("KBArticle", "Topic", "aboutTopic", .0),
             ("ProjectReport", "Department", "ownedBy", .0), ("Policy", "Topic", "aboutTopic", -.05)]
    for a, b, l, r in links:
        arrow(ax, D[a], C[b], l, r, lpos=.5 if a != "Policy" or b != "Topic" else .3)
    arrow(ax, D["KBArticle"], D["IncidentReport"], "derivedFrom", 0.45, color="#1e7e34", lpos=.5)
    arrow(ax, D["Manual"], D["KBArticle"], "relatedTo", -0.45, color="#1e7e34", lpos=.5)
    ax.text(7, -0.5, "Green arrows: relations between documents   |   Red arrows: relations between documents and concepts",
            ha="center", fontsize=9.5, color=GREY)
    fig.tight_layout()
    out = ROOT / "evidence" / "document_concept_graph.png"
    fig.savefig(out, dpi=150); plt.close(fig); print("Wrote", out)


def lifecycle_map():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(-11, 11); ax.set_ylim(-7, 7.2); ax.axis("off")
    ax.set_title("NovaTech Solutions: Knowledge Lifecycle Map", fontsize=18, color=NAVY, fontweight="bold")
    stages = [
        ("1. CREATE / ACQUIRE", "Tickets, incident reviews, project work,\nvendor docs, training, expert interviews",
         "Tacit to explicit: engineers write\nreports, drafts and lessons learned", (0, 5.3), False),
        ("2. STORE / DOCUMENT", "Standard templates; stored in the\nKnowledge Repository with metadata\n(author, version, system, date)",
         "Docs: Policy, Manual, Incident Report,\nKB Article, Technical Doc, Project Report", (7.4, 2.7), False),
        ("3. ORGANIZE / CLASSIFY", "Taxonomy + ontology tagging: type,\ntopic, system, department",
         "PROTOTYPE 1: TF-IDF + Logistic\nRegression auto-classifies documents", (7.4, -2.7), True),
        ("4. SHARE", "Portal, search, onboarding, handoffs,\nweekly knowledge sessions",
         "PROTOTYPE 2: TF-IDF + cosine\nsimilarity semantic search", (0, -5.3), True),
        ("5. APPLY", "Technicians resolve incidents with KB\narticles and runbooks; policies guide\nchanges; managers decide with reports",
         "Outcome: faster resolution,\nfewer escalations", (-7.4, -2.7), False),
        ("6. UPDATE / IMPROVE", "Post-incident reviews, user feedback,\nSLA metrics, quarterly review; outdated\ndocs revised or retired (supersedes)",
         "Feedback loop returns to stage 1", (-7.4, 2.7), False),
    ]
    for t, d, e, (x, y), ai in stages:
        fc = GOLD if ai else BLUE
        ec = "#b58a00" if ai else NAVY
        ax.add_patch(FancyBboxPatch((x - 3.1, y - 1.25), 6.2, 2.5, boxstyle="round,pad=0.02,rounding_size=0.2",
                                    fc=fc, ec=ec, lw=2.2, zorder=3))
        ax.text(x, y + 0.85, t, ha="center", va="center", fontsize=12, color=NAVY, fontweight="bold", zorder=4)
        ax.text(x, y + 0.1, d, ha="center", va="center", fontsize=8.8, color="#222", zorder=4)
        ax.text(x, y - 0.8, e, ha="center", va="center", fontsize=8.5, color=RED if ai else "#444",
                style="italic", zorder=4)
    centers = [s[3] for s in stages]
    for i in range(6):
        a, b = centers[i], centers[(i + 1) % 6]
        link(ax, a, b, ((6.2, 2.5), (6.2, 2.5)), None, color=NAVY, lw=3, rad=-0.12)
    ax.add_patch(FancyBboxPatch((-2.6, -1.1), 5.2, 2.2, boxstyle="round,pad=0.02,rounding_size=0.3",
                                fc="white", ec=NAVY, lw=2.5, zorder=3))
    ax.text(0, 0.45, "NovaTech Knowledge Base", ha="center", fontsize=13, color=NAVY, fontweight="bold", zorder=4)
    ax.text(0, -0.35, "Ontology-structured explicit knowledge\n+ tacit knowledge of technicians", ha="center",
            fontsize=9.5, color="#333", zorder=4)
    ax.text(0, -6.75, "Gold = stages supported by the automated prototype   |   Tacit knowledge becomes explicit in stage 1 "
            "and is refined continuously through stage 6", ha="center", fontsize=9.5, color=GREY)
    fig.tight_layout()
    out = ROOT / "evidence" / "lifecycle_map.png"
    fig.savefig(out, dpi=150); plt.close(fig); print("Wrote", out)


def _clip(c, size, toward):
    """Point where the segment from box centre c towards `toward` leaves the box."""
    (cx, cy), (w, h), (tx, ty) = c, size, toward
    dx, dy = tx - cx, ty - cy
    s = min((w / 2) / abs(dx) if dx else 1e9, (h / 2) / abs(dy) if dy else 1e9)
    return cx + dx * s, cy + dy * s


def link(ax, a, b, sizes, label, color=RED, ls="-", lw=1.8, lpos=0.5, rad=0.0, dx=0, dy=0, arrowhead=True):
    pa = _clip(a, sizes[0], b)
    pb = _clip(b, sizes[1], a)
    ax.add_patch(FancyArrowPatch(pa, pb, arrowstyle="-|>" if arrowhead else "-", mutation_scale=15, lw=lw,
                                 color=color, linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=2,
                                 shrinkA=2, shrinkB=2))
    if label:
        ax.text(pa[0] + (pb[0] - pa[0]) * lpos + dx, pa[1] + (pb[1] - pa[1]) * lpos + dy, label, fontsize=9,
                color=color, ha="center", va="center", fontweight="bold",
                bbox=dict(fc="white", ec="none", pad=1.2), zorder=5)


def ontology_graph():
    W, H = 2.7, 0.9
    fig, ax = plt.subplots(figsize=(16, 10.5))
    ax.set_xlim(-11, 11); ax.set_ylim(-5.4, 8.8); ax.axis("off")
    ax.set_title("NovaTech Knowledge Ontology: domain concepts, document types and relations",
                 fontsize=16, color=NAVY, fontweight="bold")
    P = {"Document": (0, 4), "Topic": (-7.5, 4), "LifecycleStage": (7.5, 4), "Department": (-7.5, 0.5),
         "Incident": (0, 0), "System": (7.5, 0.5), "Technician": (-7.5, -2.8), "Tool": (7.5, -2.8),
         "Customer": (0, -4.3)}
    for n, p in P.items():
        box(ax, p, n, w=W, h=H, fc="#c3dcf2" if n == "Document" else BLUE)
    sz = (W, H)
    for a, b, l, kw in [("Document", "Topic", "aboutTopic", {}), ("Document", "LifecycleStage", "inStage", {}),
                        ("Document", "Department", "ownedBy", {}), ("Document", "Incident", "documents", {}),
                        ("Document", "System", "describes", {}), ("Document", "Technician", "authoredBy", {"lpos": .6}),
                        ("Technician", "Department", "memberOf", {}), ("Technician", "Incident", "resolves", {}),
                        ("Technician", "Tool", "uses", {"dy": 0.0}), ("Incident", "System", "affects", {}),
                        ("Incident", "Customer", "reportedBy", {}), ("Tool", "System", "supports", {})]:
        link(ax, P[a], P[b], (sz, sz), l, **kw)
    ax.add_patch(FancyArrowPatch((8.4, 1.0), (8.9, 0.5), connectionstyle="arc3,rad=-1.6", arrowstyle="-|>",
                                 mutation_scale=14, lw=1.8, color=RED, zorder=2))
    ax.text(9.9, 1.35, "dependsOn", fontsize=9, color=RED, fontweight="bold", ha="center")
    ax.text(0, 2.3, "Document: supersedes / relatedTo (Document to Document)", ha="center", fontsize=9,
            color=RED, fontweight="bold")
    subs = ["Policy", "Manual", "IncidentReport", "KBArticle", "TechnicalDoc", "ProjectReport"]
    xs = [-8.8, -5.3, -1.8, 1.8, 5.3, 8.8]
    for n, x in zip(subs, xs):
        box(ax, (x, 7.6), n, w=3.2, h=0.8, fc=GOLD, ec="#b58a00", fs=10)
        link(ax, (x, 7.6), P["Document"], ((3.2, 0.8), sz), None, color=GREY, ls="--", lw=1.4)
    ax.text(0, 6.2, "subClassOf Document", ha="center", fontsize=10, color=GREY, fontweight="bold",
            bbox=dict(fc="white", ec="none"))
    ax.text(0, -5.2, "Blue = domain concepts (Activity 2 classes + new)   |   Gold = document types   |   "
            "Red arrows = object properties (domain to range)   |   Dashed = subclass", ha="center", fontsize=9, color=GREY)
    fig.tight_layout()
    out = ROOT / "evidence" / "ontology_graph.png"
    fig.savefig(out, dpi=150); plt.close(fig); print("Wrote", out)


def doc_concept_graph():
    """Relation matrix: which document type is linked to which concept, and how."""
    docs = ["Policy", "Manual", "IncidentReport", "KBArticle", "TechnicalDoc", "ProjectReport"]
    cols = ["System", "Customer", "Incident", "Topic", "Technician", "Department", "Document"]
    cells = {("Policy", "System"): "governs", ("Policy", "Topic"): "aboutTopic",
             ("Manual", "Customer"): "guides", ("Manual", "Topic"): "aboutTopic",
             ("IncidentReport", "Incident"): "documents", ("IncidentReport", "Technician"): "authoredBy",
             ("IncidentReport", "System"): "describes",
             ("KBArticle", "Incident"): "solves", ("KBArticle", "Topic"): "aboutTopic",
             ("KBArticle", "System"): "describes", ("KBArticle", "Document"): "derivedFrom IncidentReport",
             ("TechnicalDoc", "System"): "describes", ("TechnicalDoc", "Document"): "relatedTo / supersedes",
             ("ProjectReport", "Incident"): "summarizes", ("ProjectReport", "Department"): "ownedBy",
             ("ProjectReport", "Technician"): "authoredBy"}
    fig, ax = plt.subplots(figsize=(15, 6.2))
    ax.axis("off")
    ax.set_title("Document type to concept relation matrix", fontsize=15, color=NAVY, fontweight="bold")
    text = [[cells.get((d, c), "") for c in cols] for d in docs]
    colors = [[GOLD if cells.get((d, c)) else "white" for c in cols] for d in docs]
    tbl = ax.table(cellText=text, rowLabels=docs, colLabels=cols, cellColours=colors, loc="center",
                   cellLoc="center", rowColours=[BLUE] * 6, colColours=[BLUE] * len(cols))
    tbl.auto_set_font_size(False); tbl.set_fontsize(10); tbl.scale(1, 2.6)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor(NAVY)
        if r == 0 or c == -1:
            cell.set_text_props(fontweight="bold", color=NAVY)
    fig.tight_layout()
    out = ROOT / "evidence" / "document_concept_graph.png"
    fig.savefig(out, dpi=150); plt.close(fig); print("Wrote", out)


if __name__ == "__main__":
    (ROOT / "evidence").mkdir(exist_ok=True)
    write_owl()
    ontology_graph()
    doc_concept_graph()
    lifecycle_map()
