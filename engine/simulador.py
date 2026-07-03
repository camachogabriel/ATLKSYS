#!/usr/bin/env python3
"""Simulador mínimo del motor de razonamiento ATL (v1.1).

Ejecuta un caso de validación contra la base de conocimiento:
puntos -> confianza -> hipótesis activadas -> ranking -> resultado explicado.

Uso: python3 engine/simulador.py knowledge/casos/mhv-001.yaml
"""
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
NIVELES = ["baja", "media", "alta", "muy-alta"]


def cargar(nombre):
    with open(RAIZ / "knowledge" / f"{nombre}.yaml") as f:
        return yaml.safe_load(f)


def confianza(puntos):
    if puntos <= 3:
        return "baja"
    if puntos <= 7:
        return "media"
    if puntos <= 12:
        return "alta"
    return "muy-alta"


def nombres_elementos():
    n = {}
    for c in cargar("capacidades")["capacidades"]:
        n[c["codigo"]] = c["nombre"]
    for f in cargar("factores")["factores"]:
        n[f["codigo"]] = f["nombre"]
    em = cargar("emergentes")
    for e in em["emergentes"] + em["estados_derivados"]:
        n[e["codigo"]] = e["nombre"]
    return n


def simular(respuestas_caso, contexto=None):
    """respuestas_caso: lista de (codigo_pregunta, id_respuesta)."""
    preguntas = {q["codigo"]: q for q in cargar("preguntas")["preguntas"]}
    estado, traza = {}, []

    for qc, rid in respuestas_caso:
        q = preguntas[qc]
        r = next(x for x in q["respuestas"] if x["id"] == rid)
        efectos = dict(r.get("puntos") or {})
        for pc in r.get("puntos_condicionales", []):
            if _cumple(pc["si"], contexto or {}):
                for k, v in pc["puntos"].items():
                    efectos[k] = efectos.get(k, 0) + v
        for k, v in efectos.items():
            estado[k] = estado.get(k, 0) + v
        traza.append((qc, q["texto"], r["texto"], efectos))

    return estado, traza


def _cumple(cond, ctx):
    for campo, expr in cond.items():
        val = ctx.get(campo)
        if val is None:
            return False
        if isinstance(expr, str) and expr[0] in "<>":
            if not eval(f"{val} {expr[0]} {expr[1:]}"):
                return False
        elif val != expr:
            return False
    return True


def evaluar_hipotesis(estado):
    activadas = []
    for h in cargar("hipotesis")["hipotesis"]:
        ok = True
        for c in h.get("condiciones", []):
            pts = estado.get(c["elemento"], 0)
            nivel = NIVELES.index(confianza(pts))
            if "confianza_minima" in c and nivel < NIVELES.index(c["confianza_minima"]):
                ok = False
            if "confianza_maxima" in c and nivel > NIVELES.index(c["confianza_maxima"]):
                ok = False
        for c in h.get("contraindicadores", []):
            if estado.get(c["elemento"], 0) <= c["puntos_maximos"]:
                ok = False
        if ok:
            score = sum(max(estado.get(e, 0), 0) for e in h["elementos"])
            activadas.append((score, h))
    activadas.sort(key=lambda x: -x[0])
    return activadas


def main(ruta_caso):
    with open(ruta_caso) as f:
        caso = yaml.safe_load(f)
    nombres = nombres_elementos()

    # Respuestas de afinación del caso (formato: pregunta + id de respuesta)
    respuestas = [(a["pregunta"], a.get("respuesta_id", "A")) for a in caso["afinacion"]]
    estado, traza = simular(respuestas, caso.get("contexto"))

    print(f"=== {caso['codigo']}: {caso['consulta']} ===\n")
    print("Afinación:")
    for qc, qt, rt, ef in traza:
        print(f"  {qc} {qt}\n    -> {rt}  {ef}")

    print("\nEstado de conocimiento:")
    for cod, pts in sorted(estado.items(), key=lambda x: -x[1]):
        print(f"  {cod} {nombres.get(cod, cod):40s} {pts:+3d}  ({confianza(pts)})")

    activadas = evaluar_hipotesis(estado)
    print("\nHipótesis activadas:")
    if not activadas:
        print("  (ninguna — resultado preliminar, ofrecer 'Afinar mi resultado')")
    for i, (score, h) in enumerate(activadas):
        rol = "PRINCIPAL" if i == 0 else (
            "secundaria" if score >= activadas[0][0] * 0.5 else "descartada por ranking")
        print(f"  [{rol}] {h['codigo']} {h['nombre']} (score {score})")
        if i == 0:
            print(f"    {h['texto'].strip()}")
            print(f"    Recomendación: {h['recomendacion'].strip()}")
            print(f"    Falta: {', '.join(h['informacion_faltante'])}")

    esperada = caso.get("hipotesis", {}).get("principal", "")
    if activadas and esperada:
        print(f"\nEsperada por el caso: '{esperada}'")
        print(f"Obtenida:             '{activadas[0][1]['nombre']}'")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else RAIZ / "knowledge/casos/mhv-001.yaml")
