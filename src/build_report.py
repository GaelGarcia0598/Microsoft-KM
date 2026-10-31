"""Builds the project progress report (PDF) with ReportLab."""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, Preformatted, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

ROOT = Path(__file__).resolve().parent.parent
EV = ROOT / "evidence"
REPO_URL = "https://github.com/GaelGarcia0598/Microsoft-KM"
NAVY = colors.HexColor("#17365d")
LIGHT = colors.HexColor("#d9e9f6")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], textColor=NAVY, fontSize=17, spaceBefore=6, spaceAfter=8)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], textColor=NAVY, fontSize=12.5, spaceBefore=8, spaceAfter=4)
B = ParagraphStyle("B", parent=ss["BodyText"], fontSize=10, leading=14, spaceAfter=5)
SM = ParagraphStyle("SM", parent=B, fontSize=8.5, leading=11, textColor=colors.HexColor("#555555"))
CAP = ParagraphStyle("CAP", parent=SM, alignment=TA_CENTER, spaceAfter=10)
CELL = ParagraphStyle("CELL", parent=B, fontSize=8.5, leading=11, spaceAfter=0)
CELLB = ParagraphStyle("CELLB", parent=CELL, fontName="Helvetica-Bold", textColor=colors.white)
CODE = ParagraphStyle("CODE", fontName="Courier", fontSize=7.6, leading=9.4, backColor=colors.HexColor("#f3f5f7"),
                      borderPadding=5, spaceAfter=8)
W = letter[0] - 1.5 * inch


def P(t, s=B):
    return Paragraph(t, s)


def img(name, width=W, caption=None):
    path = EV / name
    iw, ih = ImageReader(str(path)).getSize()
    flow = [Image(str(path), width=width, height=width * ih / iw)]
    if caption:
        flow.append(P(caption, CAP))
    return KeepTogether(flow)


def table(rows, widths, header=True):
    data = [[P(str(c), CELLB if (header and i == 0) else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#9fb3c8")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef5fb")])]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
    t.setStyle(TableStyle(st))
    return t


def footer(c, d):
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(0.75 * inch, 0.5 * inch, "Microsoft - Knowledge Management System | Gael Andrés García García")
    c.drawRightString(letter[0] - 0.75 * inch, 0.5 * inch, f"Page {d.page}")


def build():
    s = []
    # ---------- Cover ----------
    s += [Spacer(1, 1.2 * inch),
          P("Sistemas y tecnologías de administración del conocimiento",
            ParagraphStyle("c1", parent=H2, alignment=TA_CENTER, textColor=colors.HexColor("#2a7ba8"), fontSize=14)),
          P("Knowledge Management System for Microsoft",
            ParagraphStyle("c2", parent=H1, alignment=TA_CENTER, fontSize=26, leading=31, spaceBefore=14)),
          P("Project progress report: lifecycle map, ontology, automated classification and semantic search",
            ParagraphStyle("c3", parent=B, alignment=TA_CENTER, fontSize=12, textColor=colors.HexColor("#555555"))),
          Spacer(1, 0.4 * inch)]
    cov = Table([[P("<b>Student</b>", CELLB), P("Gael Andrés García García", CELL)],
                 [P("<b>Instructor</b>", CELLB), P("Jonathan Alexis Puente Guerrero", CELL)],
                 [P("<b>Course</b>", CELLB), P("Sistemas y tecnologías de administración del conocimiento", CELL)],
                 [P("<b>Deliverable</b>", CELLB), P("Project progress document", CELL)],
                 [P("<b>Date</b>", CELLB), P("10/30/2026", CELL)],
                 [P("<b>Repository</b>", CELLB), P(f'<link href="{REPO_URL}" color="blue">{REPO_URL}</link>', CELL)]],
                colWidths=[1.6 * inch, W - 1.6 * inch])
    cov.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), NAVY), ("GRID", (0, 0), (-1, -1), 0.5, colors.white),
                             ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#f2f6fa")),
                             ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    s += [cov, PageBreak()]

    # ---------- 1 Company ----------
    s += [P("1. Description of the company: Microsoft", H1),
          P("<b>Microsoft Corporation</b> is a global technology company (headquartered in Redmond, Washington, USA) that develops "
            "software, cloud services (Azure, Microsoft 365, Dynamics 365), devices and AI products. It is the organization "
            "analysed in Activity 1. This project keeps the IT Technical Support domain of Activity 2 (customers, incidents, "
            "systems, technicians, tools and documents) and extends that ontology. <i>Note: the 48 sample documents are synthetic "
            "examples written in the style of Microsoft support, cloud, security and management documents; they are not real "
            "internal Microsoft documents.</i>"),
          P("a) Type of organization", H2),
          P("A multinational technology company (software, cloud and devices) that builds products and also operates and "
            "supports cloud infrastructure and business applications for consumers, enterprises and public institutions."),
          P("b) Core activities", H2),
          table([["Area", "Core activities", "Knowledge generated"],
                 ["Customer and technical support", "Receives and resolves support cases by phone, email, chat and portal (24/7 for critical customers).",
                  "Troubleshooting solutions, recurring issues, customer feedback."],
                 ["Cloud and infrastructure operations", "Operates Azure, networks, VPN gateways, Exchange Online, backups and customer cloud migrations.",
                  "Incident reports, configurations, root-cause analyses."],
                 ["Security", "Microsoft Defender, Microsoft Entra ID access control, audits, phishing response.",
                  "Policies, audit findings, threat lessons learned."],
                 ["Product engineering and projects", "Development on GitHub and Azure DevOps, platform upgrades, customer onboarding.",
                  "Technical designs, progress and closure reports."],
                 ["Management", "SLA monitoring, planning, training (Microsoft Learn), customer relationship.",
                  "Performance reports, KPIs, satisfaction surveys."]],
                [1.6 * inch, 2.9 * inch, W - 4.5 * inch]),
          Spacer(1, 6),
          P("c) Types of knowledge and documents handled", H2),
          P("Microsoft manages both <b>explicit</b> knowledge (documents) and <b>tacit</b> knowledge (the diagnostic judgment of "
            "senior engineers, which the lifecycle tries to turn into documents). Six document types are handled and are "
            "the categories used by the classifier:"),
          table([["Document type (category)", "Purpose", "Typical content"],
                 ["Policy (policy)", "Rules and obligations", "Password, remote work, change management, backup, escalation."],
                 ["Manual (manual)", "How-to instructions for users", "Step-by-step guides: VPN client, email on mobile, printer setup."],
                 ["Incident report (incident_report)", "Record of what happened", "Timeline, affected system, root cause, corrective action."],
                 ["KB article (kb_article)", "Fast troubleshooting", "Symptom, cause, solution; e.g. VPN error 809."],
                 ["Technical documentation (technical_doc)", "How systems are built", "Architecture, API reference, schema, configuration."],
                 ["Project / performance report (project_report)", "Management information", "KPIs, SLA compliance, audits, project status."]],
                [2.1 * inch, 1.7 * inch, W - 3.8 * inch]),
          PageBreak()]

    # ---------- 2 Lifecycle ----------
    s += [P("2. Knowledge lifecycle map", H1),
          P("The map extends the five stages of Activity 1 (Microsoft) to six stages adapted to Microsoft, separating "
            "<i>organize / classify</i> from <i>store / document</i> as required by this project. Gold stages are the ones "
            "supported by the Python prototype."),
          img("lifecycle_map.png", caption="Figure 1. Knowledge lifecycle map of Microsoft."),
          table([["Stage", "How it happens at Microsoft", "Documents / outputs", "Support"],
                 ["1. Creation / acquisition", "Technicians capture lessons from tickets and incident reviews; project teams write designs; training and vendor documentation is acquired.", "Incident reports, drafts, designs", "Templates"],
                 ["2. Storage / documentation", "Documents are saved in the repository using standard templates and metadata (author, version, system, date).", "All six document types", "Repository"],
                 ["3. Organization / classification", "Each document is tagged by type, topic, system and department following the ontology.", "Metadata, category labels", "<b>Prototype 1: classifier</b>"],
                 ["4. Sharing", "Knowledge portal and search, onboarding, handoffs and weekly knowledge sessions.", "Search results, training", "<b>Prototype 2: search</b>"],
                 ["5. Application", "Technicians resolve incidents with KB articles; policies guide changes; managers use reports to decide.", "Resolved tickets, decisions", "-"],
                 ["6. Update / improvement", "Post-incident reviews, feedback and SLA metrics trigger revision; old documents are superseded or retired.", "New versions, lessons learned", "Review cycle"]],
                [1.25 * inch, 3.0 * inch, 1.35 * inch, W - 5.6 * inch]),
          PageBreak()]

    # ---------- 3 Ontology ----------
    s += [P("3. Ontology / conceptual graph of organizational knowledge", H1),
          P("The ontology (<font face='Courier'>ontology/MicrosoftKM.owl</font>, OWL/RDF-XML) extends the Activity 2 model "
            "(Incident, Technician, System, Tool, Document, Customer) with the classes needed to organize knowledge. It has "
            "<b>15 classes</b>, <b>20 object properties</b>, 8 data properties and sample individuals "
            "(e.g. incident INC-1001, KB-201, a remote-work policy)."),
          img("ontology_graph.png", caption="Figure 2. Ontology graph: domain concepts (blue), document types (gold) and relationships (red arrows)."),
          P("Elements of the model", H2),
          table([["Element", "Content"],
                 ["a) Main concepts", "Incident, System, Technician, Tool, Customer, Topic, Department, LifecycleStage, Document."],
                 ["b) Document types", "Policy, Manual, IncidentReport, KBArticle, TechnicalDoc, ProjectReport (all subclasses of Document)."],
                 ["c) Relations between concepts", "reportedBy, affects, resolves, uses, supports, dependsOn, memberOf."],
                 ["d) Relations between documents and concepts", "documents, describes, aboutTopic, authoredBy, ownedBy, inStage, governs, guides, solves, summarizes; document to document: derivedFrom, supersedes, relatedTo."]],
                [1.9 * inch, W - 1.9 * inch]),
          Spacer(1, 6),
          img("document_concept_graph.png", caption="Figure 3. Which document types relate to which concepts, and through which property."),
          P("Example of how knowledge is connected: incident <b>INC-1001</b> (VPN outage) <i>affects</i> the Azure VPN Gateway and is "
            "<i>resolved by</i> a support engineer. Its <b>incident report</b> <i>documents</i> the incident; the <b>KB-201</b> article is "
            "<i>derivedFrom</i> that report, <i>solves</i> the incident, and <i>describes</i> the Azure VPN Gateway; the "
            "<b>remote-work policy</b> <i>governs</i> the same system. A user searching for \"VPN\" can therefore reach the "
            "policy, the manual, the incident and the fix through the graph."),
          PageBreak()]

    # ---------- 4 Prototype ----------
    s += [P("4. Explanation of the prototype", H1),
          P("The prototype is written in Python 3 with scikit-learn and has two components that implement the stages "
            "<i>organize / classify</i> and <i>share</i> of the lifecycle. Source code and test documents are in the repository."),
          table([["File", "Role"],
                 ["build_corpus.py", "Creates the 48 sample documents (data/documents/&lt;category&gt;/*.txt)."],
                 ["src/classifier.py", "TF-IDF + Naive Bayes / Logistic Regression classifier, evaluation and prediction of new text."],
                 ["src/semantic_search.py", "TF-IDF vectors, cosine similarity and ranked results; optional ontology-based query expansion."],
                 ["src/evaluate_search.py", "12-query evaluation of the search component."],
                 ["src/build_diagrams.py", "Generates the OWL file, ontology graphs and lifecycle map."],
                 ["ontology/*.owl", "MicrosoftKM.owl (this project) and ITSupportOntology_Activity2.owl (previous activity)."]],
                [1.9 * inch, W - 1.9 * inch]),
          P("4.1 Document set", H2),
          P("48 short documents, 8 per category (policy, manual, incident_report, kb_article, technical_doc, project_report), "
            "written to resemble Microsoft support, cloud, security and management documents (synthetic, not real internal documents). The first line is the title and the rest is the body."),
          P("4.2 Automated classification", H2),
          P("<b>Steps:</b> (i) load all documents and their category labels; (ii) vectorize with <font face='Courier'>TfidfVectorizer</font> "
            "(lowercase, English stop words, unigrams + bigrams, sublinear term frequency); (iii) split 75% / 25% with stratification "
            "(36 train / 12 test) and train Multinomial Naive Bayes and Logistic Regression; (iv) compare using test accuracy and "
            "5-fold cross-validation, keep the best model and predict the category (with probability) of new documents."),
          Preformatted("vec = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), sublinear_tf=True)\n"
                       "model = make_pipeline(vec, LogisticRegression(max_iter=1000, C=10))\n"
                       "model.fit(X_train, y_train)\n"
                       "model.predict_proba([new_text])      # probability per category", CODE),
          P("4.3 Semantic search", H2),
          P("<b>Steps:</b> (i) the user types a natural language query; (ii) the query is transformed with the same fitted TF-IDF "
            "vectorizer into a vector; (iii) cosine similarity between the query vector and every document vector is computed; "
            "(iv) the top-k documents with score &gt; 0 are shown with their category and similarity. An optional flag "
            "<font face='Courier'>--expand</font> adds related terms taken from the ontology concepts (e.g. <i>slow</i> adds "
            "<i>performance, freeze, disk usage</i>) so that the search is less dependent on exact words."),
          Preformatted("qvec   = vectorizer.transform([query])\n"
                       "scores = cosine_similarity(qvec, doc_matrix)[0]\n"
                       "top    = scores.argsort()[::-1][:k]", CODE),
          P("<b>Limitation:</b> TF-IDF matches shared vocabulary; it does not understand meaning. That is why it is called "
            "<i>basic</i> semantic search. Synonyms that are not in the ontology lexicon are not captured, and the document set "
            "is small and synthetic, so the results demonstrate the method, not production accuracy."),
          PageBreak()]

    # ---------- 5 Evidence ----------
    s += [P("5. Evidence of prototype operation", H1),
          P("The following captures show the real console output of the scripts (rendered as terminal images by "
            "<font face='Courier'>src/make_screenshots.py</font> from the actual execution results)."),
          P("5.1 Classification", H2),
          img("screenshot_classifier_training.png", caption="Figure 4. Training and evaluation of both models."),
          P("On the 12-document test set Naive Bayes reached 83.3% and Logistic Regression 91.7%; with 5-fold cross-validation "
            "Naive Bayes obtained 87.6% and Logistic Regression 93.8%, so Logistic Regression was selected. The test set is small, so the cross-validation "
            "figure is the more reliable estimate."),
          img("screenshot_classifier_predictions.png", caption="Figure 5. Test predictions and classification of six new, unseen texts."),
          img("confusion_matrix.png", width=W * 0.62, caption="Figure 6. Confusion matrix of the selected model on the test set."),
          PageBreak(),
          P("5.2 Semantic search", H2),
          img("screenshot_search_vpn.png", caption="Figure 7. Query: how do I fix a VPN connection problem."),
          P("The top result is the VPN technical specification; the VPN KB article (the most useful answer) ranks third, behind the "
            "printer-offline KB article that matched the word \"fix\". This is a real weakness of plain TF-IDF and is reported "
            "in the evaluation below."),
          img("screenshot_search_printer.png", caption="Figure 8. Query: steps to install a printer."),
          img("screenshot_search_expansion.png", caption="Figure 9. Effect of the ontology-based query expansion (score of the best match rises from 0.255 to 0.482)."),
          img("screenshot_search_evaluation.png", caption="Figure 10. Evaluation with 12 queries, with and without expansion."),
          P("The search returned a document of the expected category as first result in <b>11 of 12 queries (92%)</b>. "
            "The only miss is the VPN query above. Expansion did not change the top-1 accuracy on this set but increased "
            "similarity scores for matching documents."),
          PageBreak()]

    # ---------- 6 Prior work ----------
    s += [P("6. Evidence of earlier practical exercises", H1),
          P("The project builds directly on the previous activities and on the experiments carried out while developing the prototype."),
          table([["Exercise", "What was done", "Contribution to this project"],
                 ["Activity 1: Knowledge life cycle at Microsoft", "Analysis of knowledge creation, storage, sharing, application and update; tacit vs explicit knowledge; AI support (classification, semantic search, outdated-content detection).", "Base of the lifecycle map (Section 2) and the idea of AI-assisted classification and search."],
                 ["Activity 2: IT Technical Support ontology", "OWL ontology with 6 classes, 9 object properties and 8 data properties, checked with the HermiT reasoner.", "Extended into MicrosoftKM.owl (Section 3), keeping its classes and properties."],
                 ["Classification tests", "Naive Bayes vs Logistic Regression, hold-out and 5-fold cross-validation, confusion matrix, prediction of new documents.", "Prototype 1 (Section 5.1)."],
                 ["Information retrieval exercises", "TF-IDF vectors, cosine similarity ranking, query expansion with ontology terms, 12-query evaluation.", "Prototype 2 (Section 5.2)."],
                 ["Conceptual representation", "Ontology graph, document-concept relation matrix and lifecycle map.", "Figures 1 to 3."]],
                [1.65 * inch, 2.9 * inch, W - 4.55 * inch]),
          Spacer(1, 8),
          img("activity2_ontology_graph.png", width=W * 0.6, caption="Figure 11. Ontology graph from Activity 2 (starting point of the new ontology)."),
          P("Activity 1 and Activity 2 reports are the submitted evidence of those exercises."),
          P("7. Conclusions and next steps", H1),
          P("The prototype shows that classification and retrieval can support two lifecycle stages with very little infrastructure. "
            "Next steps: expand the corpus with real, anonymized documents; add metadata extraction (system, topic) so documents "
            "are tagged with ontology individuals; replace TF-IDF with embeddings for true semantic matching; and add a review step "
            "where a person confirms the predicted category, consistent with the human-review principle of Activity 1."),
          P(f'Repository: <link href="{REPO_URL}" color="blue">{REPO_URL}</link>')]

    out = ROOT / "docs" / "Microsoft_KM_Project_Progress.pdf"
    SimpleDocTemplate(str(out), pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch, topMargin=0.7 * inch,
                      bottomMargin=0.8 * inch, title="Microsoft Solutions - Knowledge Management System",
                      author="Gael Andrés García García").build(s, onFirstPage=lambda c, d: None, onLaterPages=footer)
    print("Wrote", out)


if __name__ == "__main__":
    build()
