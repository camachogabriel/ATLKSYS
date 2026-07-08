#!/usr/bin/env python3
"""Genera supabase/functions/enviar-reporte/index.ts desde el conocimiento.

Fuentes de verdad: knowledge/servicios.yaml + knowledge/hipotesis.yaml.
Tras editarlos:
    python3 supabase/build_function.py
    # y redeplegar la función (vía MCP o `supabase functions deploy enviar-reporte`)
"""
import json
from pathlib import Path
import yaml

RAIZ = Path(__file__).resolve().parent.parent
LOGO_URL = "https://static.wixstatic.com/media/9d1be0_e4ee180b08184d159adbfa2a55f4ace3~mv2.png/v1/fill/w_405,h_254/ATLLogoColores.png"
SITE = "https://www.athletetrainlab.com"
IG = "https://www.instagram.com/athletetrainlab"
WA = "https://wa.me/50688445505"
AGENDA = "https://www.athletetrainlab.com/contactoatl"


def _oneline(s):
    return " ".join((s or "").split())


def main():
    cat = yaml.safe_load(open(RAIZ / "knowledge/servicios.yaml"))["servicios"]
    servicios, reglas, siempre = {}, {}, []
    for s in cat:
        cod = s["codigo"]
        servicios[cod] = {"nombre": s["nombre"], "gancho": _oneline(s["gancho"]),
                          "url": s.get("url", AGENDA), "prioridad": s.get("prioridad", 5)}
        if s.get("siempre"):
            siempre.append(cod)
        for h in s.get("activar_si", {}).get("hipotesis", []):
            reglas.setdefault(h, []).append(cod)

    hips = yaml.safe_load(open(RAIZ / "knowledge/hipotesis.yaml"))["hipotesis"]
    hipotesis = {h["codigo"]: {"nombre": h["nombre"], "recomendacion": _oneline(h.get("recomendacion", ""))}
                 for h in hips}

    data = json.dumps({"SERVICIOS": servicios, "REGLAS": reglas, "SIEMPRE": siempre,
                       "HIPOTESIS": hipotesis}, ensure_ascii=False)

    ts = TEMPLATE.replace("__DATA__", data).replace("__LOGO__", LOGO_URL) \
        .replace("__SITE__", SITE).replace("__IG__", IG).replace("__WA__", WA).replace("__AGENDA__", AGENDA)
    out = RAIZ / "supabase/functions/enviar-reporte/index.ts"
    out.write_text(ts)
    print(f"index.ts generado ({len(servicios)} servicios, {len(hipotesis)} hipótesis)")


TEMPLATE = r'''// AthleteTrainLab - Edge Function: enviar reporte por correo
// GENERADO por supabase/build_function.py desde knowledge/servicios.yaml + hipotesis.yaml.
// No editar a mano: edita el YAML y regenera.
//
// Requisitos: secrets RESEND_API_KEY y FROM_EMAIL; webhook INSERT -> esta función.
// Sin RESEND_API_KEY no falla: registra y responde 200 (no-op).

import { serve } from "https://deno.land/std@0.224.0/http/server.ts";

const K = __DATA__;
const { SERVICIOS, REGLAS, SIEMPRE, HIPOTESIS } = K;
const LOGO = "__LOGO__", SITE = "__SITE__", IG = "__IG__", WA = "__WA__", AGENDA = "__AGENDA__";

function serviciosPara(hip: string | null): string[] {
  const set = new Set<string>(SIEMPRE);
  if (hip && REGLAS[hip]) REGLAS[hip].forEach((s: string) => set.add(s));
  return [...set].sort((a, b) => SERVICIOS[a].prioridad - SERVICIOS[b].prioridad);
}

function construirHTML(row: any): string {
  const hip = row.hipotesis_principal ? HIPOTESIS[row.hipotesis_principal] : null;
  const resultado = (hip && !row.preliminar)
    ? `<div style="border-left:4px solid #4fa96e;background:#f0f9f4;padding:14px 16px;border-radius:8px;margin:0 0 8px">
         <div style="color:#1a1a2e;font-weight:700;font-size:15px">${hip.nombre}</div>
         <div style="color:#5a6472;font-size:14px;margin-top:6px">${hip.recomendacion}</div>
       </div>`
    : `<div style="border-left:4px solid #e7c13c;background:#fdf8ec;padding:14px 16px;border-radius:8px;margin:0 0 8px">
         <div style="color:#1a1a2e;font-weight:700;font-size:15px">Tu evaluación quedó preliminar</div>
         <div style="color:#5a6472;font-size:14px;margin-top:6px">Con unas preguntas más (o una cita con nosotros) podemos precisar dónde tienes más margen de mejora.</div>
       </div>`;

  const cards = serviciosPara(row.hipotesis_principal).map((c) => {
    const s = SERVICIOS[c];
    return `<div style="border:1px solid #e6e8eb;border-radius:10px;padding:16px;margin:10px 0">
      <div style="color:#1a1a2e;font-weight:700;font-size:15px">${s.nombre}</div>
      <div style="color:#5a6472;font-size:14px;margin:6px 0 12px">${s.gancho}</div>
      <a href="${s.url}" style="display:inline-block;background:#0d1117;color:#fff;text-decoration:none;font-size:13px;font-weight:700;padding:9px 16px;border-radius:8px">Ver más</a>
    </div>`;
  }).join("");

  return `<div style="background:#f4f5f7;padding:24px 0;font-family:Arial,Helvetica,sans-serif">
    <div style="max-width:560px;margin:auto;background:#fff;border-radius:14px;overflow:hidden;border:1px solid #e6e8eb">
      <div style="background:#0d1117;padding:20px;text-align:center">
        <img src="${LOGO}" alt="AthleteTrainLab" width="150" style="display:inline-block;max-width:150px">
      </div>
      <div style="padding:26px 28px">
        <h1 style="font-size:20px;margin:0 0 6px;color:#1a1a2e">Tu evaluación está lista</h1>
        <p style="color:#5a6472;font-size:14px;margin:0 0 18px">Gracias por completar tu análisis en AthleteTrainLab. Esto es lo que encontramos:</p>
        ${resultado}
        <h2 style="font-size:15px;margin:22px 0 4px;color:#1a1a2e">Cómo podemos ayudarte</h2>
        ${cards}
        <div style="text-align:center;margin-top:20px">
          <a href="${WA}" style="display:inline-block;background:#25d366;color:#fff;text-decoration:none;font-size:14px;font-weight:700;padding:12px 22px;border-radius:9px;margin:4px">Escríbenos por WhatsApp</a>
          <a href="${AGENDA}" style="display:inline-block;background:#4fa96e;color:#fff;text-decoration:none;font-size:14px;font-weight:700;padding:12px 22px;border-radius:9px;margin:4px">Agenda una cita</a>
        </div>
      </div>
      <div style="background:#f4f5f7;padding:16px 28px;text-align:center;color:#8b95a3;font-size:12px">
        <a href="${SITE}" style="color:#4fa96e;text-decoration:none">athletetrainlab.com</a> ·
        <a href="${IG}" style="color:#4fa96e;text-decoration:none">Instagram</a><br>
        Orientación basada en tus respuestas, no un diagnóstico médico.
      </div>
    </div>
  </div>`;
}

serve(async (req) => {
  try {
    const payload = await req.json();
    const row = payload.record ?? payload;
    const email = row.email;
    const key = Deno.env.get("BREVO_API_KEY");
    const fromRaw = Deno.env.get("FROM_EMAIL") ?? "AthleteTrainLab <athletetrainlab@gmail.com>";
    const m = fromRaw.match(/^(.*)<(.+)>$/);
    const fromName = m ? m[1].trim() : "AthleteTrainLab";
    const fromEmail = m ? m[2].trim() : fromRaw.trim();

    if (!email) return new Response("sin email, nada que enviar", { status: 200 });
    if (!key) {
      console.log("BREVO_API_KEY no configurada; no-op. Fila:", row.id);
      return new Response("no-op: falta BREVO_API_KEY", { status: 200 });
    }

    const r = await fetch("https://api.brevo.com/v3/smtp/email", {
      method: "POST",
      headers: { "Content-Type": "application/json", "accept": "application/json", "api-key": key },
      body: JSON.stringify({
        sender: { name: fromName, email: fromEmail },
        to: [{ email }],
        subject: "Tu evaluación AthleteTrainLab",
        htmlContent: construirHTML(row),
      }),
    });
    return new Response(await r.text(), { status: r.ok ? 200 : 502 });
  } catch (e) {
    console.error("error en enviar-reporte:", e);
    return new Response("error: " + (e as Error).message, { status: 500 });
  }
});
'''

if __name__ == "__main__":
    main()
