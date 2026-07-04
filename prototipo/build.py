#!/usr/bin/env python3
"""Genera prototipo/quiz.html embebiendo la base de conocimiento actual.

Uso: python3 prototipo/build.py
"""
import json
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent


def cargar(n):
    with open(RAIZ / "knowledge" / f"{n}.yaml") as f:
        return yaml.safe_load(f)


def main():
    em = cargar("emergentes")
    nombres = {}
    for c in cargar("capacidades")["capacidades"]:
        nombres[c["codigo"]] = c["nombre"]
    for f in cargar("factores")["factores"]:
        nombres[f["codigo"]] = f["nombre"]
    for e in em["emergentes"] + em["estados_derivados"]:
        nombres[e["codigo"]] = e["nombre"]

    data = {
        "preguntas": cargar("preguntas")["preguntas"],
        "hipotesis": cargar("hipotesis")["hipotesis"],
        "limitaciones": cargar("limitaciones")["limitaciones"],
        "objetivos": cargar("objetivos")["objetivos"],
        "nombres": nombres,
    }
    plantilla = (RAIZ / "prototipo/plantilla.html").read_text()
    salida = plantilla.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    (RAIZ / "prototipo/quiz.html").write_text(salida)
    print(f"quiz.html generado ({len(salida)//1024} KB)")


if __name__ == "__main__":
    main()
