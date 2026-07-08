#!/usr/bin/env python3
"""Genera el SQL para sincronizar knowledge/*.yaml -> tabla public.config_correo.

La Edge Function enviar-reporte lee su configuración (servicios, reglas,
hipótesis, recursos, buckets) desde esa tabla, así cambiar ofertas/videos NO
requiere redeploy: se corre este SQL (via MCP execute_sql o psql).

    python3 supabase/sync_config.py   # imprime el SQL de upsert
"""
import json, yaml
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
one = lambda s: " ".join((s or "").split())


def short(t, n=170):
    t = one(t)
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"


def build():
    serv = yaml.safe_load(open(RAIZ / "knowledge/servicios.yaml"))["servicios"]
    SERV, REG, SIEMPRE = {}, {}, []
    for s in serv:
        c = s["codigo"]
        SERV[c] = {"nombre": s["nombre"], "gancho": one(s["gancho"]), "url": s.get("url"), "prioridad": s.get("prioridad", 5)}
        if s.get("siempre"):
            SIEMPRE.append(c)
        for h in s.get("activar_si", {}).get("hipotesis", []):
            REG.setdefault(h, []).append(c)
    HIP = {h["codigo"]: {"nombre": h["nombre"], "recomendacion": short(h.get("recomendacion", ""))}
           for h in yaml.safe_load(open(RAIZ / "knowledge/hipotesis.yaml"))["hipotesis"]}
    REC = [{"titulo": r["titulo"], "url": r["url"], "hipotesis": r.get("hipotesis", []), "general": bool(r.get("general"))}
           for r in yaml.safe_load(open(RAIZ / "knowledge/recursos.yaml"))["recursos"]]
    BUCKETS = {
        "Aeróbico / fondo": ["C001", "D004", "E006", "E004"],
        "Umbral / intensidad": ["C002", "E005"],
        "Explosividad": ["C003", "C005"],
        "Fuerza": ["C004", "F004"],
        "Energía / nutrición": ["D001", "D002", "F001", "F002", "D003", "E001"],
        "Recuperación / entreno": ["F003", "F005", "F006", "F007"],
    }
    return {"servicios": SERV, "reglas": REG, "siempre": SIEMPRE, "hipotesis": HIP, "recursos": REC, "buckets": BUCKETS}


def main():
    rows = build()
    lit = lambda v: json.dumps(v, ensure_ascii=False).replace("'", "''")
    vals = ",\n".join("('%s', '%s'::jsonb)" % (k, lit(v)) for k, v in rows.items())
    print("insert into public.config_correo (clave,valor) values\n" + vals +
          "\non conflict (clave) do update set valor=excluded.valor, updated_at=now();")


if __name__ == "__main__":
    main()
