import sys
import os

from django.shortcuts import render

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from pdf_reader import leer_pdf
from extractor import extraer_datos


def index(request):
    resultados = []
    errores = []

    if request.method == 'POST':
        archivos = request.FILES.getlist('pdfs')

        for archivo in archivos:
            try:
                import tempfile
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                    for chunk in archivo.chunks():
                        tmp.write(chunk)
                    tmp_path = tmp.name

                texto = leer_pdf(tmp_path)
                datos = extraer_datos(texto)
                datos['archivo'] = archivo.name
                resultados.append(datos)
            except Exception as e:
                errores.append({'archivo': archivo.name, 'error': str(e)})
            finally:
                if 'tmp_path' in locals() and os.path.exists(tmp_path):
                    os.unlink(tmp_path)

    return render(request, 'camara_app/index.html', {
        'resultados': resultados,
        'errores': errores,
    })
