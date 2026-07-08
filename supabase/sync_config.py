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


PASOS = {
    "H001": ["Consume 60-90 g de carbohidratos por hora en fondos", "Come antes de tener hambre, no cuando ya te falta energía", "Suma salidas largas suaves para depender menos del azúcar"],
    "H002": ["Aumenta el volumen aeróbico de forma progresiva", "Mete fuerza y trabajo de calidad al final de las salidas largas"],
    "H003": ["Sal más controlado y guarda para el final", "Regula por potencia o sensación en las subidas"],
    "H004": ["Suma volumen suave (zona 2, poder conversar)", "Evita que casi todo tu entrenamiento sea intenso"],
    "H005": ["Añade intervalos de umbral (8-20 min) sobre tu base", "Cuida la nutrición en los esfuerzos duros"],
    "H006": ["Incluye sprints cortos y arrancadas", "Trabaja fuerza-velocidad en el gimnasio"],
    "H007": ["Hidrátate con sodio/electrolitos, no solo agua", "Aclimátate al calor de forma progresiva"],
    "H008": ["Prioriza el sueño y baja la carga 1-2 semanas", "Asegura días realmente suaves entre los duros"],
    "H009": ["Que la mayoría de tus salidas sean realmente suaves", "Una sola sesión de calidad planificada por semana"],
    "H010": ["Sube potencia con entrenamiento específico de ciclismo", "Si procede, ajusta el peso de forma gradual y con apoyo"],
    "H011": ["Fuerza 2 veces por semana (ejercicios básicos)", "Practica torque a baja cadencia en la bici"],
    "H012": ["Estructura la semana: base + intensidad + fuerza", "Varía el estímulo, no repitas siempre la misma salida"],
    "H013": ["No te obsesiones con el número del pulso", "Trabajo aeróbico suave; valora una revisión fisiológica y cardíaca"],
    "H015": ["Hazte un bike fit si aún no lo tienes", "Trabaja movilidad de cadera y activación del glúteo", "Si duele o persiste, consúltalo con fisioterapia"],
}


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
    HIP = {h["codigo"]: {"nombre": h["nombre"], "recomendacion": one(h.get("recomendacion", "")), "pasos": PASOS.get(h["codigo"], [])}
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
