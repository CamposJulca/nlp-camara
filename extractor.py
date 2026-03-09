import re
import spacy

nlp = spacy.load("es_core_news_md")

INICIO_CARGO = re.compile(
    r"^(Gerente|Presidente|Representante|Suplente|Primer|Segundo|Tercer|"
    r"Revisor|Por |Inscrita|Del Libro|Con El|CARGO|ÓRGANO|JUNTA|"
    r"PRINCIPAL|REVISORES|REFORMAS)",
    re.IGNORECASE
)

PATRON_REP = re.compile(
    r"^(Gerente|Presidente|Representante)\s+(.+?)\s+(C\.C\.|P\.P\.|C\.E\.)\s+No\.\s*([\w\.]+)",
    re.IGNORECASE
)

PATRON_SUPLENTE = re.compile(
    r"^(Suplente|Primer|Segundo|Tercer)",
    re.IGNORECASE
)


def limpiar_nit(nit):

    partes = nit.split()

    if len(partes) == 2:
        return f"{partes[0]}-{partes[1]}"

    return nit.replace(" ", "")


def unir_continuaciones(texto):
    """Une las líneas de continuación (nombres partidos por columnas del PDF) a la línea anterior."""

    lineas = texto.split("\n")
    resultado = []

    for linea in lineas:
        linea = linea.strip()

        if not linea:
            resultado.append("")
            continue

        if INICIO_CARGO.match(linea):
            resultado.append(linea)
        elif resultado and resultado[-1]:
            resultado[-1] += " " + linea
        else:
            resultado.append(linea)

    return "\n".join(resultado)


def extraer_nombre_con_nlp(linea):
    """Usa spaCy para extraer entidades PER de la línea."""

    doc = nlp(linea)
    personas = [ent.text for ent in doc.ents if ent.label_ == "PER"]

    return personas[0].title().strip() if personas else None


def extraer_representante(seccion):

    seccion = re.sub(r"^CARGO\s+NOMBRE\s+IDENTIFICACI[ÓO]N\s*$", "", seccion, flags=re.MULTILINE)
    seccion = unir_continuaciones(seccion)

    for linea in seccion.split("\n"):
        linea = linea.strip()

        if not linea or PATRON_SUPLENTE.match(linea):
            continue

        m = PATRON_REP.match(linea)

        if m:
            nombre_bruto = m.group(2).strip()
            tipo_doc     = m.group(3).strip()
            num_doc      = m.group(4).replace(".", "")

            nombre = extraer_nombre_con_nlp(nombre_bruto) or nombre_bruto.title()

            return nombre, tipo_doc, num_doc

    return "", "", ""


def extraer_seccion(texto, encabezado):

    idx = texto.find(encabezado)

    if idx == -1:
        return ""

    return texto[idx + len(encabezado):]


def extraer_datos(texto):

    razon_social = ""
    nit = ""
    representante = ""
    tipo_documento = ""
    cedula = ""

    razon_match = re.search(
        r"Raz[oó]n\s+social\s*[:\-]\s*(.+)",
        texto,
        re.IGNORECASE
    )

    nit_match = re.search(
        r"Nit\s*[:\-]\s*([\d\.]+\s*\d?)",
        texto,
        re.IGNORECASE
    )

    if razon_match:
        razon_social = razon_match.group(1).strip()

    if nit_match:
        nit = limpiar_nit(nit_match.group(1))

    seccion = extraer_seccion(texto, "REPRESENTANTES LEGALES")

    if seccion:
        representante, tipo_documento, cedula = extraer_representante(seccion)

    return {
        "razon_social": razon_social,
        "nit": nit,
        "representante_legal": representante,
        "tipo_documento": tipo_documento,
        "cedula_representante": cedula
    }
