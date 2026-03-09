import sys
import json

from pdf_reader import leer_pdf
from extractor import extraer_datos


def main():

    if len(sys.argv) < 2:
        print("Uso:")
        print("python main.py archivo.pdf")
        sys.exit(1)

    archivo = sys.argv[1]

    print("\n[INFO] Leyendo PDF")

    texto = leer_pdf(archivo)

    print("[INFO] Extrayendo datos")

    datos = extraer_datos(texto)

    print("\nRESULTADO:\n")

    print(json.dumps(datos, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()