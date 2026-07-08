#!/usr/bin/env python3
"""Simulador del motor de razonamiento ATL (v1.2) - flujo completo.

Limitación -> batería inicial -> metadatos -> afinación adaptativa (D9)
-> criterio de parada (D4) -> hipótesis (D6) -> resultado explicado.

Uso: python3 engine/simulador.py knowledge/casos/mhv-001.yaml
"""
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
NIVELES = ["baja", "media", "alta", "muy-alta"]
MAX_PREGUNTAS = 25


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


def _efectos(respuesta, contexto):
    ef = dict(respuesta.get("puntos") or {})
    for pc in respuesta.get("puntos_condicionales", []):
        if _cumple(pc["si"], contexto or {}):
            for k, v in pc["puntos"].items():
                ef[k] = ef.get(k, 0) + v
    return ef


def _impacto(pregunta):
    m = 0
    for r in pregunta["respuestas"]:
        for v in (r.get("puntos") or {}).values():
            m = max(m, abs(v))
        for pc in r.get("puntos_condicionales", []):
            for v in pc["puntos"].values():
                m = max(m, abs(v))
    return m


def evaluar_hipotesis(estado):
    activadas = []
    for h in cargar("hipotesis")["hipotesis"]:
        ok = True
        for c in h.get("condiciones", []):
            nivel = NIVELES.index(confianza(estado.get(c["elemento"], 0)))
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
    activadas.sort(key=lambda x: (-x[0], x[1]["codigo"]))
    return activadas


def resolver_objetivo(codigo):
    """Traduce un objetivo O### a su limitación asociada (D7)."""
    o = next(x for x in cargar("objetivos")["objetivos"] if x["codigo"] == codigo)
    return o["limitacion_asociada"]


def evaluacion_completa(limitacion, responder, contexto=None, verbose=True):
    """Recorre el flujo completo.

    limitacion: código LP### (u O###, que se traduce vía resolver_objetivo).
    responder: función (pregunta) -> id de respuesta elegida.
    """
    if limitacion.startswith("O"):
        limitacion = resolver_objetivo(limitacion)
    preguntas = cargar("preguntas")["preguntas"]
    metadatos, estado, respondidas, traza = set(), {}, set(), []

    # D12/D14: el IMC abre rutas de investigación (señal, no conclusión)
    if contexto and contexto.get("peso_kg") and contexto.get("estatura_cm"):
        m = contexto["estatura_cm"] / 100
        contexto["imc"] = round(contexto["peso_kg"] / (m * m), 1)
        if contexto["imc"] >= 27:
            metadatos.add("composicion-corporal")
        elif contexto["imc"] < 20:
            metadatos.update(["disponibilidad-energetica", "nutricion", "carbohidratos"])
    if contexto and contexto.get("usa_hr"):
        metadatos.add("pulso")   # D17: habilita la capa de pulso

    # Fase perfil general (D20): puntos + metadatos, para todos
    for q in sorted([x for x in preguntas if x["tipo"] == "perfil"],
                    key=lambda x: x["codigo"]):
        rid = responder(q)
        r = next(x for x in q["respuestas"] if x["id"] == rid)
        ef = _efectos(r, contexto)
        for k, v in ef.items():
            estado[k] = estado.get(k, 0) + v
        metadatos.update(r.get("metadatos", []))
        respondidas.add(q["codigo"])
        traza.append(("perfil", q, r, ef))

    # Fase batería inicial: seleccionada por el tipo de la limitación (D10)
    lim = next(x for x in cargar("limitaciones")["limitaciones"]
               if x["codigo"] == limitacion)
    bateria = [q for q in preguntas if q["tipo"] == "bateria-inicial"
               and lim["tipo"] in (q.get("tipos") or [])]
    for q in sorted(bateria, key=lambda x: x["codigo"]):
        rid = responder(q)
        r = next(x for x in q["respuestas"] if x["id"] == rid)
        metadatos.update(r.get("metadatos", []))
        respondidas.add(q["codigo"])
        traza.append(("batería", q, r, {}))

    # Fase afinación adaptativa (D9 + D4)
    while len(respondidas) < MAX_PREGUNTAS:
        candidatas = [q for q in preguntas if q["tipo"] == "afinacion"
                      and q["codigo"] not in respondidas
                      and set(q["condiciones_aparicion"].get("metadatos_requeridos", []))
                      <= metadatos
                      and not (set(q["condiciones_aparicion"].get("metadatos_excluidos", []))
                               & metadatos)]
        if not candidatas:
            parada = "agotamiento"
            break
        if any(confianza(p) in ("alta", "muy-alta") for p in estado.values()):
            parada = "evidencia suficiente"
            break
        q = sorted(candidatas, key=lambda x: (-_impacto(x), x["codigo"]))[0]
        rid = responder(q)
        r = next(x for x in q["respuestas"] if x["id"] == rid)
        ef = _efectos(r, contexto)
        for k, v in ef.items():
            estado[k] = estado.get(k, 0) + v
        metadatos.update(r.get("metadatos", []))
        respondidas.add(q["codigo"])
        traza.append(("afinación", q, r, ef))
    else:
        parada = "profundidad máxima"

    activadas = evaluar_hipotesis(estado)
    preliminar = not any(confianza(p) in ("alta", "muy-alta") for p in estado.values())

    if verbose:
        nombres = nombres_elementos()
        print(f"Limitación: {limitacion} | Preguntas: {len(respondidas)} | Parada: {parada}\n")
        for fase, q, r, ef in traza:
            extra = f"  {ef}" if ef else f"  metadatos: {r.get('metadatos')}" if r.get("metadatos") else ""
            print(f"  [{fase}] {q['codigo']} {q['texto']}\n      -> {r['texto']}{extra}")
        print(f"\nMetadatos activos: {sorted(metadatos)}")
        print("\nEstado de conocimiento:")
        for cod, pts in sorted(estado.items(), key=lambda x: -x[1]):
            print(f"  {cod} {nombres.get(cod, cod):38s} {pts:+3d}  ({confianza(pts)})")
        print(f"\nResultado{' PRELIMINAR' if preliminar else ''}:")
        if not activadas:
            print("  Sin hipótesis activadas -> ofrecer 'Afinar mi resultado'")
        for i, (score, h) in enumerate(activadas):
            rol = "PRINCIPAL" if i == 0 else (
                "secundaria" if score >= activadas[0][0] * 0.5 else "no reportada")
            print(f"  [{rol}] {h['codigo']} {h['nombre']} (score {score})")
            if i == 0:
                print(f"    Recomendación: {h['recomendacion'].strip()}")

    return {"estado": estado, "metadatos": metadatos, "hipotesis": activadas,
            "parada": parada, "preliminar": preliminar, "n_preguntas": len(respondidas)}


def desde_caso(ruta):
    with open(ruta) as f:
        caso = yaml.safe_load(f)
    guion = dict(caso.get("respuestas_guion", {}))

    def responder(q):
        return guion.get(q["codigo"], q["respuestas"][0]["id"])

    print(f"=== {caso['codigo']}: {caso['consulta']} ===\n")
    res = evaluacion_completa(caso["limitacion"], responder, caso.get("contexto"))
    esperada = (caso.get("hipotesis") or {}).get("principal", "")
    if esperada and res["hipotesis"]:
        obtenida = res["hipotesis"][0][1]["nombre"]
        print(f"\nEsperada: '{esperada}'\nObtenida: '{obtenida}'")
        print("VALIDACIÓN:", "OK" if esperada == obtenida else "REVISAR")
    return res


if __name__ == "__main__":
    desde_caso(sys.argv[1] if len(sys.argv) > 1 else RAIZ / "knowledge/casos/mhv-001.yaml")
