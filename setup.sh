#!/bin/bash

echo "====================================="
echo "Configurando entorno SARLAFT NLP"
echo "====================================="

# 1. verificar python
if ! command -v python >/dev/null 2>&1; then
    echo "[ERROR] Python no está instalado"
    exit 1
fi

echo "[INFO] Python detectado:"
python --version

# 2. crear entorno virtual
echo "[INFO] Creando entorno virtual..."

python -m venv venv

# 3. activar entorno
echo "[INFO] Activando entorno..."

source venv/bin/activate

# 4. actualizar pip
echo "[INFO] Actualizando pip..."

pip install --upgrade pip

# 5. instalar dependencias
echo "[INFO] Instalando librerías..."

pip install pdfplumber spacy

# 6. descargar modelo NLP español
echo "[INFO] Descargando modelo de lenguaje..."

python -m spacy download es_core_news_md

echo "====================================="
echo "Entorno configurado correctamente"
echo "====================================="

echo ""
echo "Para activar el entorno manualmente:"
echo "source venv/bin/activate"