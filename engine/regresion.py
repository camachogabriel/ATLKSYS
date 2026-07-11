#!/usr/bin/env python3
"""Suite de regresión del motor ATL.

Corre los casos de knowledge/casos/regresion.yaml contra el motor y afirma el
resultado (titular / hipótesis disparada / preliminar) tras el reordenamiento
por núcleo (D26). Sale con código 1 si algún caso falla.

Uso:  python3 engine/regresion.py
"""
import sys
import pathlib
import importlib.util

import yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("sim", RAIZ / "engine" / "simulador.py")
sim = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sim)


def correr_caso(caso):
    guion = caso.get("guion", {})

    def responder(q):
        return guion.get(q["codigo"], q["respuestas"][0]["id"])

    res = sim.evaluacion_completa(
        caso["limitacion"], responder, dict(caso.get("contexto", {})), verbose=False)
    act = sim.rankear_nucleo(res["hipotesis"], caso["limitacion"])
    titular = act[0][1]["codigo"] if act else None
    disparadas = [h["codigo"] for _, h in act]

    fallos = []
    if "titular" in caso and titular != caso["titular"]:
        fallos.append(f"titular={titular} (esperado {caso['titular']})")
    if "activada" in caso and caso["activada"] not in disparadas:
        fallos.append(f"{caso['activada']} no disparó")
    if "no_activada" in caso and caso["no_activada"] in disparadas:
        fallos.append(f"{caso['no_activada']} NO debía disparar")
    if "preliminar" in caso and res["preliminar"] != caso["preliminar"]:
        fallos.append(f"preliminar={res['preliminar']}")
    return fallos, titular, disparadas


def main():
    casos = yaml.safe_load(open(RAIZ / "knowledge" / "casos" / "regresion.yaml"))["casos"]
    n_fallos = 0
    for c in casos:
        fallos, titular, disparadas = correr_caso(c)
        if fallos:
            n_fallos += 1
            print(f"FALLA  {c['id']:26s} {'; '.join(fallos)}  ·  disparadas={disparadas}")
        else:
            print(f"OK     {c['id']:26s} titular={titular or '-'}")
    total = len(casos)
    print(f"\n{total - n_fallos}/{total} OK")
    sys.exit(1 if n_fallos else 0)


if __name__ == "__main__":
    main()
