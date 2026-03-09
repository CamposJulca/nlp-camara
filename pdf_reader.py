import re
import pdfplumber

PATRON_ENCABEZADO = re.compile(
    r"Página\s+\d+\s+de\s+\d+\s+"
    r"Cámara de Comercio.*?"
    r"-{20,}\s*",
    re.DOTALL
)


def leer_pdf(ruta):

    texto = ""

    with pdfplumber.open(ruta) as pdf:
        for page in pdf.pages:
            contenido = page.extract_text()

            if contenido:
                texto += contenido + "\n"

    texto = PATRON_ENCABEZADO.sub("", texto)

    return texto