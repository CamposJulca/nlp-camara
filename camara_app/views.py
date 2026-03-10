import os
import sys
import tempfile

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from pdf_reader import leer_pdf
from extractor import extraer_datos


# ── Vista web (interfaz HTML) ────────────────────────────────────────────────

def index(request):
    resultados = []
    errores = []

    if request.method == 'POST':
        archivos = request.FILES.getlist('pdfs')

        for archivo in archivos:
            tmp_path = None
            try:
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
                if tmp_path and os.path.exists(tmp_path):
                    os.unlink(tmp_path)

    return render(request, 'camara_app/index.html', {
        'resultados': resultados,
        'errores': errores,
    })


# ── API REST (consumida por automation-hub-finagro) ──────────────────────────

class ExtraerCertificadosApiView(APIView):
    """
    POST /api/extraer/

    Recibe uno o varios PDFs de Cámara de Comercio.
    Devuelve JSON con 'resultados' y 'errores'.
    Los campos devueltos son los que espera el módulo SARLAFT:
      representante, tipo_doc, cedula
    """
    parser_classes = [MultiPartParser]

    def post(self, request):
        archivos = request.FILES.getlist('archivos')
        if not archivos:
            return Response(
                {'error': 'Se requiere al menos un archivo PDF.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        resultados = []
        errores = []

        for archivo in archivos:
            tmp_path = None
            try:
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                    for chunk in archivo.chunks():
                        tmp.write(chunk)
                    tmp_path = tmp.name

                texto = leer_pdf(tmp_path)
                datos = extraer_datos(texto)

                resultados.append({
                    'archivo':       archivo.name,
                    'razon_social':  datos.get('razon_social', ''),
                    'nit':           datos.get('nit', ''),
                    'representante': datos.get('representante_legal', ''),
                    'tipo_doc':      datos.get('tipo_documento', ''),
                    'cedula':        datos.get('cedula_representante', ''),
                })
            except Exception as e:
                errores.append({'archivo': archivo.name, 'error': str(e)})
            finally:
                if tmp_path and os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        return Response({'resultados': resultados, 'errores': errores})
