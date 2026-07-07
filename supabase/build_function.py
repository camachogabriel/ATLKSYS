#!/usr/bin/env python3
"""Genera supabase/functions/enviar-reporte/index.ts desde knowledge/servicios.yaml.

Única fuente de verdad = servicios.yaml. Tras editar el catálogo:
    python3 supabase/build_function.py
    # y redeplegar la función (vía MCP o `supabase functions deploy enviar-reporte`)
"""
import json
from pathlib import Path
import yaml

RAIZ = Path(__file__).resolve().parent.parent


def main():
    cat = yaml.safe_load(open(RAIZ / "knowledge/servicios.yaml"))["servicios"]
    servicios, reglas, siempre = {}, {}, []
    for s in cat:
        cod = s["codigo"]
        servicios[cod] = {"nombre": s["nombre"], "gancho": " ".join(s["gancho"].split()),
                          "prioridad": s.get("prioridad", 5)}
        if s.get("siempre"):
            siempre.append(cod)
        for h in s.get("activar_si", {}).get("hipotesis", []):
            reglas.setdefault(h, []).append(cod)

    data = json.dumps({"SERVICIOS": servicios, "REGLAS": reglas, "SIEMPRE": siempre},
                      ensure_ascii=False, indent=2)

    ts = '''// AthleteTrainLab - Edge Function: enviar reporte por correo
// GENERADO por supabase/build_function.py desde knowledge/servicios.yaml.
// No editar a mano el bloque de datos; edita el YAML y regenera.
//
// Requisitos: secrets RESEND_API_KEY y FROM_EMAIL; webhook INSERT -> esta función.
// Sin RESEND_API_KEY no falla: registra y responde 200 (no-op).

import { serve } from "https://deno.land/std@0.224.0/http/server.ts";

const CATALOGO = __DATA__;
const { SERVICIOS, REGLAS, SIEMPRE } = CATALOGO;

function serviciosPara(hip: string | null): string[] {
  const set = new Set<string>(SIEMPRE);
  if (hip && REGLAS[hip]) REGLAS[hip].forEach((s: string) => set.add(s));
  return [...set].sort((a, b) => SERVICIOS[a].prioridad - SERVICIOS[b].prioridad);
}

serve(async (req) => {
  try {
    const payload = await req.json();
    const row = payload.record ?? payload;
    const email = row.email;
    const key = Deno.env.get("RESEND_API_KEY");
    const from = Deno.env.get("FROM_EMAIL") ?? "AthleteTrainLab <onboarding@resend.dev>";

    if (!email) return new Response("sin email, nada que enviar", { status: 200 });
    if (!key) {
      console.log("RESEND_API_KEY no configurada; no-op. Fila:", row.id);
      return new Response("no-op: falta RESEND_API_KEY", { status: 200 });
    }

    const bloques = serviciosPara(row.hipotesis_principal).map((c) =>
      `<div style="border:1px solid #30363d;border-radius:10px;padding:14px;margin:10px 0"><strong style="color:#2dd4bf">${SERVICIOS[c].nombre}</strong><p style="color:#8b949e;font-size:14px;margin:6px 0 0">${SERVICIOS[c].gancho}</p></div>`).join("");
    const html =
      `<div style="font-family:sans-serif;max-width:560px;margin:auto;color:#e6edf3;background:#0d1117;padding:24px;border-radius:12px"><h2>Tu evaluación AthleteTrainLab</h2><p style="color:#8b949e">Gracias por completar tu análisis. Según tus respuestas, esto es lo que puede ayudarte más:</p>${bloques}<p style="color:#6e7681;font-size:12px;margin-top:20px">Orientación basada en tus respuestas, no un diagnóstico médico.</p></div>`;

    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${key}` },
      body: JSON.stringify({ from, to: email, subject: "Tu evaluación AthleteTrainLab", html }),
    });
    return new Response(await r.text(), { status: r.ok ? 200 : 502 });
  } catch (e) {
    console.error("error en enviar-reporte:", e);
    return new Response("error: " + (e as Error).message, { status: 500 });
  }
});
'''
    ts = ts.replace("__DATA__", data)
    out = RAIZ / "supabase/functions/enviar-reporte/index.ts"
    out.write_text(ts)
    print(f"index.ts generado ({len(servicios)} servicios, {len(reglas)} hipótesis mapeadas)")


if __name__ == "__main__":
    main()
