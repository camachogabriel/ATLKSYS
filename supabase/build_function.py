#!/usr/bin/env python3
"""Genera supabase/functions/enviar-reporte/index.ts desde el conocimiento.

Fuentes de verdad: knowledge/servicios.yaml + hipotesis.yaml + recursos.yaml.
Tras editarlos:
    python3 supabase/build_function.py   # regenera index.ts
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

# Ejes del radar (hexágono) y qué códigos de estado suma cada uno.
BUCKETS = {
    "Aeróbico / fondo": ["C001", "D004", "E006", "E004"],
    "Umbral / intensidad": ["C002", "E005"],
    "Explosividad": ["C003", "C005"],
    "Fuerza": ["C004", "F004"],
    "Energía / nutrición": ["D001", "D002", "F001", "F002", "D003", "E001"],
    "Recuperación / entreno": ["F003", "F005", "F006", "F007"],
}


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

    recs = yaml.safe_load(open(RAIZ / "knowledge/recursos.yaml"))["recursos"]
    recursos = [{"titulo": r["titulo"], "url": r["url"], "hipotesis": r.get("hipotesis", []),
                 "general": bool(r.get("general"))} for r in recs]

    data = json.dumps({"SERVICIOS": servicios, "REGLAS": reglas, "SIEMPRE": siempre,
                       "HIPOTESIS": hipotesis, "RECURSOS": recursos, "BUCKETS": BUCKETS},
                      ensure_ascii=False)

    ts = (TEMPLATE.replace("__DATA__", data).replace("__LOGO__", LOGO_URL)
          .replace("__SITE__", SITE).replace("__IG__", IG).replace("__WA__", WA).replace("__AGENDA__", AGENDA))
    (RAIZ / "supabase/functions/enviar-reporte/index.ts").write_text(ts)
    print(f"index.ts generado ({len(servicios)} servicios, {len(hipotesis)} hipótesis, {len(recursos)} recursos)")


TEMPLATE = r'''// AthleteTrainLab - Edge Function: enviar reporte por correo (Brevo)
// GENERADO por supabase/build_function.py. No editar a mano: edita los YAML y regenera.
import { serve } from "https://deno.land/std@0.224.0/http/server.ts";

const K = __DATA__;
const { SERVICIOS, REGLAS, SIEMPRE, HIPOTESIS, RECURSOS, BUCKETS } = K;
const LOGO = "__LOGO__", SITE = "__SITE__", IG = "__IG__", WA = "__WA__", AGENDA = "__AGENDA__";

function serviciosPara(hip) {
  const set = new Set(SIEMPRE);
  if (hip && REGLAS[hip]) REGLAS[hip].forEach((s) => set.add(s));
  return [...set].sort((a, b) => SERVICIOS[a].prioridad - SERVICIOS[b].prioridad);
}

function recursosPara(hip) {
  let v = RECURSOS.filter((r) => hip && r.hipotesis.includes(hip));
  if (v.length === 0) v = RECURSOS.filter((r) => r.general);
  return v.slice(0, 3);
}

// Radar (hexágono) como imagen vía QuickChart, a partir del estado de puntos.
function radarURL(estado) {
  const labels = Object.keys(BUCKETS);
  const vals = labels.map((lab) =>
    BUCKETS[lab].reduce((s, cod) => s + Math.max(0, (estado && estado[cod]) || 0), 0));
  if (vals.every((x) => x === 0)) return null;
  const cfg = {
    type: "radar",
    data: { labels, datasets: [{ data: vals, fill: true,
      backgroundColor: "rgba(79,169,110,0.35)", borderColor: "#4fa96e",
      pointBackgroundColor: "#0d1117", borderWidth: 2 }] },
    options: { plugins: { legend: { display: false } },
      scale: { ticks: { display: false, beginAtZero: true, max: 12, stepSize: 3 },
        pointLabels: { fontSize: 11, fontColor: "#1a1a2e" }, gridLines: { color: "#e0e3e7" } } },
  };
  return "https://quickchart.io/chart?w=440&h=320&bkg=white&c=" + encodeURIComponent(JSON.stringify(cfg));
}

function construirHTML(row) {
  const hip = row.hipotesis_principal ? HIPOTESIS[row.hipotesis_principal] : null;
  const resultado = (hip && !row.preliminar)
    ? `<div style="border-left:4px solid #4fa96e;background:#f0f9f4;padding:14px 16px;border-radius:8px;margin:0 0 8px"><div style="color:#1a1a2e;font-weight:700;font-size:15px">${hip.nombre}</div><div style="color:#5a6472;font-size:14px;margin-top:6px">${hip.recomendacion}</div></div>`
    : `<div style="border-left:4px solid #e7c13c;background:#fdf8ec;padding:14px 16px;border-radius:8px;margin:0 0 8px"><div style="color:#1a1a2e;font-weight:700;font-size:15px">Tu evaluación quedó preliminar</div><div style="color:#5a6472;font-size:14px;margin-top:6px">Con unas preguntas más (o una cita con nosotros) podemos precisar dónde tienes más margen de mejora.</div></div>`;

  const radar = radarURL(row.estado);
  const radarBlock = radar
    ? `<div style="text-align:center;margin:18px 0 4px"><img src="${radar}" alt="Hacia dónde apunta tu evaluación" width="440" style="max-width:100%;border:1px solid #e6e8eb;border-radius:10px"></div><p style="color:#8b95a3;font-size:12px;text-align:center;margin:0 0 6px">Hacia dónde apunta tu evaluación. Refleja las áreas analizadas según tus respuestas, no un test completo de tus capacidades.</p>`
    : "";

  const cards = serviciosPara(row.hipotesis_principal).map((c) => {
    const s = SERVICIOS[c];
    return `<div style="border:1px solid #e6e8eb;border-radius:10px;padding:16px;margin:10px 0"><div style="color:#1a1a2e;font-weight:700;font-size:15px">${s.nombre}</div><div style="color:#5a6472;font-size:14px;margin:6px 0 12px">${s.gancho}</div><a href="${s.url}" style="display:inline-block;background:#0d1117;color:#fff;text-decoration:none;font-size:13px;font-weight:700;padding:9px 16px;border-radius:8px">Ver más</a></div>`;
  }).join("");

  const recs = recursosPara(row.hipotesis_principal);
  const recBlock = recs.length ? `<h2 style="font-size:15px;margin:22px 0 6px;color:#1a1a2e">Recursos para ti</h2>${recs.map((r) =>
    `<a href="${r.url}" style="display:block;text-decoration:none;border:1px solid #e6e8eb;border-radius:10px;padding:12px 14px;margin:8px 0;color:#1a1a2e"><span style="color:#c33a5b;font-weight:700">▶ Video</span> &nbsp;${r.titulo}</a>`).join("")}` : "";

  return `<div style="background:#f4f5f7;padding:24px 0;font-family:Arial,Helvetica,sans-serif"><div style="max-width:560px;margin:auto;background:#fff;border-radius:14px;overflow:hidden;border:1px solid #e6e8eb">
    <div style="background:#0d1117;padding:22px;text-align:center"><img src="${LOGO}" alt="AthleteTrainLab" width="170" style="display:inline-block;max-width:170px"></div>
    <div style="padding:26px 28px">
      <h1 style="font-size:20px;margin:0 0 6px;color:#1a1a2e">Tu evaluación está lista</h1>
      <p style="color:#5a6472;font-size:14px;margin:0 0 14px">Gracias por completar tu análisis. AthleteTrainLab no es un diagnóstico: es un sistema que, a partir de tus respuestas, estima <strong>qué áreas conviene revisar</strong> para que rindas mejor. Reduce la incertidumbre y te orienta por dónde empezar; no reemplaza una valoración profesional.</p>
      ${resultado}
      ${radarBlock}
      <h2 style="font-size:15px;margin:22px 0 4px;color:#1a1a2e">Cómo podemos ayudarte</h2>
      ${cards}
      ${recBlock}
      <div style="text-align:center;margin-top:20px"><a href="${WA}" style="display:inline-block;background:#25d366;color:#fff;text-decoration:none;font-size:14px;font-weight:700;padding:12px 22px;border-radius:9px;margin:4px">Escríbenos por WhatsApp</a><a href="${AGENDA}" style="display:inline-block;background:#4fa96e;color:#fff;text-decoration:none;font-size:14px;font-weight:700;padding:12px 22px;border-radius:9px;margin:4px">Agenda una cita</a></div>
    </div>
    <div style="background:#f4f5f7;padding:16px 28px;text-align:center;color:#8b95a3;font-size:12px"><a href="${SITE}" style="color:#4fa96e;text-decoration:none">athletetrainlab.com</a> · <a href="${IG}" style="color:#4fa96e;text-decoration:none">Instagram</a><br>Orientación basada en tus respuestas, no un diagnóstico médico.</div>
  </div></div>`;
}

serve(async (req) => {
  try {
    const payload = await req.json();
    const row = payload.record ?? payload;
    const email = row.email;
    const key = Deno.env.get("BREVO_API_KEY");
    const fromRaw = Deno.env.get("FROM_EMAIL") ?? "AthleteTrainLab <hola@athletetrainlab.com>";
    const replyRaw = Deno.env.get("REPLY_TO") ?? "athletetrainlab@gmail.com";
    const m = fromRaw.match(/^(.*)<(.+)>$/);
    const fromName = m ? m[1].trim() : "AthleteTrainLab";
    const fromEmail = m ? m[2].trim() : fromRaw.trim();

    if (!email) return new Response("sin email", { status: 200 });
    if (!key) { console.log("no BREVO_API_KEY; no-op", row.id); return new Response("no-op", { status: 200 }); }

    const r = await fetch("https://api.brevo.com/v3/smtp/email", {
      method: "POST",
      headers: { "Content-Type": "application/json", "accept": "application/json", "api-key": key },
      body: JSON.stringify({
        sender: { name: fromName, email: fromEmail },
        replyTo: { email: replyRaw, name: "AthleteTrainLab" },
        to: [{ email }],
        subject: "Tu evaluación AthleteTrainLab",
        htmlContent: construirHTML(row),
      }),
    });
    return new Response(await r.text(), { status: r.ok ? 200 : 502 });
  } catch (e) {
    console.error("error enviar-reporte:", e);
    return new Response("error: " + e.message, { status: 500 });
  }
});
'''

if __name__ == "__main__":
    main()
