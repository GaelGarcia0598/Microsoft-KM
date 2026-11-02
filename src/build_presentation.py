"""Genera la presentación resumen del proyecto (docs/Microsoft_KM_Presentacion.pptx)."""
from pathlib import Path
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
EV = ROOT / "evidence"
NAVY = RGBColor(0x1F, 0x3A, 0x5F)
BLUE = RGBColor(0x00, 0x78, 0xD4)
GREY = RGBColor(0x44, 0x44, 0x44)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


def text(slide, x, y, w, h, content, size=20, bold=False, color=GREY):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    items = content if isinstance(content, list) else [content]
    for i, t in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = t
        p.font.size, p.font.bold, p.font.color.rgb = Pt(size), bold, color
        p.space_after = Pt(8)
    return tb


def new(title):
    s = prs.slides.add_slide(BLANK)
    bar = s.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(1.1))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    text(s, 0.5, 0.2, 12.3, 0.8, title, 30, True, RGBColor(255, 255, 255))
    return s


def image(slide, name, x, y, maxw, maxh):
    w, h = Image.open(EV / name).size
    k = min(maxw / w, maxh / h)
    slide.shapes.add_picture(str(EV / name), Inches(x + (maxw - w * k) / 2), Inches(y), Inches(w * k), Inches(h * k))


def bullets(slide, items, x=0.6, y=1.5, w=12, size=22):
    text(slide, x, y, w, 5.5, ["• " + i for i in items], size)


# 1 Portada
s = prs.slides.add_slide(BLANK)
bg = s.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid()
bg.fill.fore_color.rgb = NAVY
bg.line.fill.background()
W = RGBColor(255, 255, 255)
text(s, 0.8, 2.0, 11.5, 1.5, "Sistema de Gestión del Conocimiento para Microsoft", 40, True, W)
text(s, 0.8, 3.8, 11.5, 1, "Mapa del ciclo de vida, ontología, clasificación automática y búsqueda semántica", 22, False, W)
text(s, 0.8, 5.3, 11.5, 1.2, ["Gael Andrés García García",
                              "Sistemas y tecnologías de administración del conocimiento",
                              "Profesor: Jonathan Alexis Puente Guerrero"], 18, False, W)

# 2 Objetivo
s = new("Objetivo y alcance del proyecto")
bullets(s, ["Construir un prototipo de gestión del conocimiento para una organización real: Microsoft.",
            "Parte de la Actividad 1 (ciclo de vida del conocimiento en Microsoft) y la Actividad 2 (ontología de soporte técnico).",
            "Componentes: mapa del ciclo de vida, ontología, clasificador automático y búsqueda semántica.",
            "Corpus de 48 documentos sintéticos (6 categorías × 8), escritos al estilo de documentos de Microsoft; no son documentos internos reales."])

# 3 Empresa
s = new("1. La organización: Microsoft")
bullets(s, ["Tipo: empresa multinacional de tecnología (software, nube, dispositivos e IA).",
            "Actividades: soporte técnico, operaciones de nube (Azure, Microsoft 365), seguridad (Defender, Entra ID), "
            "ingeniería de producto (GitHub, Azure DevOps) y gestión.",
            "Conocimiento explícito: políticas, manuales, reportes de incidentes, artículos KB, documentación técnica, reportes de proyecto.",
            "Conocimiento tácito: el criterio de diagnóstico de los ingenieros senior, que el ciclo busca documentar."], size=21)

# 4 Ciclo de vida
s = new("2. Mapa del ciclo de vida del conocimiento")
image(s, "lifecycle_map.png", 0.4, 1.25, 8.4, 5.9)
text(s, 8.9, 1.4, 4.2, 5.5, ["Seis etapas:", "1. Creación / adquisición", "2. Almacenamiento", "3. Organización / clasificación",
                             "4. Compartir", "5. Aplicación", "6. Actualización / mejora continua",
                             "Las etapas 3 y 4 están cubiertas por el prototipo."], 18)

# 5 Ontología
s = new("3. Ontología del conocimiento organizacional")
image(s, "ontology_graph.png", 0.3, 1.25, 8.6, 5.9)
text(s, 9.0, 1.4, 4.1, 5.5, ["Archivo OWL: MicrosoftKM.owl",
                             "15 clases, 20 propiedades de objeto, 8 de datos.",
                             "Conceptos: Incidente, Sistema, Técnico, Herramienta, Cliente, Tema, Departamento.",
                             "Tipos de documento: Política, Manual, Reporte de incidente, Artículo KB, Documentación técnica, Reporte de proyecto.",
                             "Extiende la ontología de la Actividad 2."], 16)

# 6 Relaciones
s = new("Relaciones entre documentos y conceptos")
image(s, "document_concept_graph.png", 0.4, 1.25, 8.0, 5.9)
text(s, 8.6, 1.4, 4.5, 5.5, ["Documento → concepto: documents, describes, governs, guides, solves, aboutTopic, authoredBy.",
                             "Documento → documento: derivedFrom, supersedes, relatedTo.",
                             "Ejemplo: el incidente INC-1001 (falla de VPN) se vincula con su reporte, el artículo KB-201 y la política de trabajo remoto."], 16)

# 7 Clasificador
s = new("4. Clasificación automática de documentos")
bullets(s, ["Carga de los 48 documentos con su categoría.",
            "Vectorización con TF-IDF (unigramas y bigramas, stop words en inglés).",
            "Modelos: Naive Bayes y Regresión Logística (división 75/25 estratificada).",
            "Resultados en prueba: NB 83.3 %, RL 91.7 %. Validación cruzada de 5 pliegues: NB 87.6 %, RL 93.8 %.",
            "Se seleccionó Regresión Logística; también clasifica textos nuevos."], size=21)

# 8 Evidencia clasificador
s = new("Evidencia del clasificador")
image(s, "screenshot_classifier_training.png", 0.3, 1.3, 7.4, 5.8)
image(s, "confusion_matrix.png", 7.9, 1.3, 5.2, 5.8)

# 9 Búsqueda
s = new("5. Búsqueda semántica básica")
bullets(s, ["Recibe una consulta en lenguaje natural.",
            "La convierte en vector con el mismo TF-IDF de los documentos.",
            "Calcula la similitud coseno contra cada documento y muestra los más relevantes.",
            "Extra: expansión de consulta usando conceptos de la ontología "
            "(ej. \"my laptop is very slow\": puntaje 0.255 → 0.482).",
            "Evaluación con 12 consultas: 11 de 12 (92 %) devolvieron la categoría esperada en el primer resultado."], size=21)

# 10 Evidencia búsqueda
s = new("Evidencia de la búsqueda")
image(s, "screenshot_search_printer.png", 0.3, 1.3, 6.3, 2.9)
image(s, "screenshot_search_expansion.png", 6.8, 1.3, 6.3, 2.9)
image(s, "screenshot_search_evaluation.png", 3.0, 4.3, 7.3, 3.0)

# 11 Limitaciones
s = new("Limitaciones y trabajo futuro")
bullets(s, ["TF-IDF no entiende el significado: la consulta \"how do I fix a VPN connection problem\" falló "
            "(el artículo correcto quedó en 3.er lugar).",
            "El corpus es pequeño y sintético; la precisión real puede variar.",
            "Mejoras: embeddings semánticos, corpus más grande, interfaz web y reentrenamiento continuo."], size=21)

# 12 Conclusiones
s = new("Conclusiones y repositorio")
bullets(s, ["Se integró el trabajo de las Actividades 1 y 2 en un sistema funcional de gestión del conocimiento.",
            "El prototipo cubre las etapas de organización y compartición del ciclo de vida.",
            "Repositorio con código, documentos de prueba, ontología y reporte:",
            "https://github.com/GaelGarcia0598/Microsoft-KM"], size=22)

out = ROOT / "docs" / "Microsoft_KM_Presentacion.pptx"
prs.save(out)
print("Wrote", out)
