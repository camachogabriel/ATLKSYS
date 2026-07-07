#!/usr/bin/env python3
"""Generador de reporte y emparejamiento de servicios (ATL).

Dada una evaluación (hipótesis activadas), decide qué servicios ofrecer según
`knowledge/servicios.yaml`. Es el "cerebro" que reutiliza la Edge Function de
correo; aquí se puede probar en local.

Uso:
    from reporte import servicios_para
    servicios_para(["H015"])            # -> lista de servicios ofrecidos
"""
from pathlib import Path
import yaml

RAIZ = Path(__file__).resolve().parent.parent


def _cargar(nombre):
    with open(RAIZ / "knowledge" / f"{nombre}.yaml") as f:
        return yaml.safe_load(f)


def servicios_para(hipotesis_activadas):
    """hipotesis_activadas: lista de códigos H### (principal + secundarias).
    Devuelve la lista de servicios a ofrecer, ordenada por prioridad."""
    activ = set(hipotesis_activadas or [])
    catalogo = _cargar("servicios")["servicios"]
    elegidos = []
    for s in catalogo:
        cond = s.get("activar_si", {})
        if s.get("siempre") or (set(cond.get("hipotesis", [])) & activ):
            elegidos.append(s)
    elegidos.sort(key=lambda s: s.get("prioridad", 5))
    return elegidos


def reporte_de(resultado):
    """resultado: dict devuelto por simulador.evaluacion_completa.
    Devuelve un dict listo para renderizar en correo/HTML."""
    hips = [h["codigo"] for _, h in resultado.get("hipotesis", [])]
    principal = resultado["hipotesis"][0][1] if resultado.get("hipotesis") else None
    return {
        "hipotesis_principal": principal["nombre"] if principal else None,
        "recomendacion": (principal.get("recomendacion") or "").strip() if principal else None,
        "preliminar": resultado.get("preliminar"),
        "servicios": [
            {"codigo": s["codigo"], "nombre": s["nombre"], "gancho": s["gancho"].strip()}
            for s in servicios_para(hips)
        ],
    }


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(RAIZ / "engine"))
    from simulador import evaluacion_completa

    # Demo: caso de sobrecarga de cuádriceps -> bike fit
    guion = {"Q073": "B", "Q074": "C", "Q075": "B", "Q084": "A", "Q085": "A",
             "Q086": "A", "Q087": "A", "Q088": "A", "Q090": "A", "Q089": "A", "Q083": "A"}
    r = evaluacion_completa("LP010", lambda q: guion.get(q["codigo"], q["respuestas"][-1]["id"]),
                            {}, verbose=False)
    rep = reporte_de(r)
    print("Hipótesis:", rep["hipotesis_principal"], "| preliminar:", rep["preliminar"])
    print("Servicios ofrecidos:")
    for s in rep["servicios"]:
        print(f"  - {s['nombre']}")
