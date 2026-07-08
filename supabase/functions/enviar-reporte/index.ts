// AthleteTrainLab - enviar-reporte
// Config (servicios, hipótesis, recursos, buckets) vive en la tabla
// public.config_correo (se sincroniza con `python3 supabase/sync_config.py`).
// Envío por Brevo. Esta función se despliega tal cual (no se genera).
import { serve } from "https://deno.land/std@0.224.0/http/server.ts";

const SB_URL = Deno.env.get("SUPABASE_URL");
const SB_SVC = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
const LOGO = "https://static.wixstatic.com/media/9d1be0_e4ee180b08184d159adbfa2a55f4ace3~mv2.png/v1/fill/w_405,h_254/ATLLogoColores.png";
const SITE = "https://www.athletetrainlab.com", IG = "https://www.instagram.com/athletetrainlab", WA = "https://wa.me/50688445505", AGENDA = "https://www.athletetrainlab.com/contactoatl";
const LEAD = Deno.env.get("LEAD_EMAIL") ?? "athletetrainlab@gmail.com";

async function cargarConfig() {
  const r = await fetch(SB_URL + "/rest/v1/config_correo?select=clave,valor", { headers: { apikey: SB_SVC, Authorization: "Bearer " + SB_SVC } });
  const rows = await r.json();
  const c: any = {};
  for (const row of rows) c[row.clave] = row.valor;
  return c;
}

function serviciosPara(C: any, hip: string | null) {
  const set = new Set<string>(C.siempre || []);
  if (hip && C.reglas[hip]) C.reglas[hip].forEach((s: string) => set.add(s));
  return [...set].sort((a, b) => C.servicios[a].prioridad - C.servicios[b].prioridad);
}
function recursosPara(C: any, hip: string | null) {
  let v = (C.recursos || []).filter((r: any) => hip && r.hipotesis.includes(hip));
  if (!v.length) v = (C.recursos || []).filter((r: any) => r.general);
  return v.slice(0, 3);
}
function radarURL(C: any, estado: any) {
  const B = C.buckets || {}; const labels = Object.keys(B);
  const vals = labels.map((l) => B[l].reduce((s: number, cod: string) => s + Math.max(0, (estado && estado[cod]) || 0), 0));
  if (vals.every((x) => x === 0)) return null;
  const cfg = {
    type: "radar",
    data: { labels, datasets: [{ label: "Tu evaluación", data: vals, fill: true, backgroundColor: "rgba(79,169,110,0.35)", borderColor: "#4fa96e", pointBackgroundColor: "#0d1117", borderWidth: 2 }] },
    options: { legend: { display: false }, title: { display: false }, plugins: { legend: { display: false } },
      scale: { ticks: { display: false, beginAtZero: true, max: 12, stepSize: 3 }, pointLabels: { fontSize: 11, fontColor: "#1a1a2e" }, gridLines: { color: "#e0e3e7" } } },
  };
  return "https://quickchart.io/chart?w=440&h=320&bkg=white&c=" + encodeURIComponent(JSON.stringify(cfg));
}
function esc(s: string) {
  return String(s).replace(/[<>&"']/g, (c) => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;", "'": "&#39;" }[c] as string));
}
function primerNombre(n: any) {
  if (!n) return "";
  const p = String(n).trim().split(/\s+/)[0];
  return p ? p.charAt(0).toUpperCase() + p.slice(1) : "";
}
function construirHTML(C: any, row: any): string {
  const hip = row.hipotesis_principal ? (C.hipotesis || {})[row.hipotesis_principal] : null;
  const nom = primerNombre(row.nombre);
  const saludo = nom ? `Hola ${esc(nom)}: ` : "";
  const resultado = (hip && !row.preliminar)
    ? `<div style='border-left:4px solid #4fa96e;background:#f0f9f4;padding:14px 16px;border-radius:8px;margin:0 0 8px'><div style='color:#1a1a2e;font-weight:700;font-size:15px'>${hip.nombre}</div><div style='color:#5a6472;font-size:14px;margin-top:6px'>${hip.recomendacion}</div></div>`
    : `<div style='border-left:4px solid #e7c13c;background:#fdf8ec;padding:14px 16px;border-radius:8px;margin:0 0 8px'><div style='color:#1a1a2e;font-weight:700;font-size:15px'>Tu evaluación quedó preliminar</div><div style='color:#5a6472;font-size:14px;margin-top:6px'>Con unas preguntas más (o una cita con nosotros) podemos precisar dónde tienes más margen de mejora.</div></div>`;
  const pasosBlock = (hip && !row.preliminar && hip.pasos && hip.pasos.length)
    ? `<div style='margin:2px 0 8px'><div style='color:#1a1a2e;font-weight:700;font-size:14px;margin:8px 0 4px'>Qué puedes empezar a hacer</div><ul style='color:#5a6472;font-size:14px;margin:0;padding-left:20px'>${hip.pasos.map((p: string) => `<li style='margin:4px 0'>${p}</li>`).join("")}</ul></div>`
    : "";
  const radar = radarURL(C, row.estado);
  const radarBlock = radar ? `<div style='text-align:center;margin:18px 0 4px'><img src='${radar}' alt='Hacia dónde apunta tu evaluación' width='440' style='max-width:100%;border:1px solid #e6e8eb;border-radius:10px'></div><p style='color:#8b95a3;font-size:12px;text-align:center;margin:0 0 6px'>Hacia dónde apunta tu evaluación. Refleja las áreas analizadas según tus respuestas, no un test completo de tus capacidades.</p>` : "";
  const cards = serviciosPara(C, row.hipotesis_principal).map((c) => { const s = C.servicios[c]; return `<div style='border:1px solid #e6e8eb;border-radius:10px;padding:16px;margin:10px 0'><div style='color:#1a1a2e;font-weight:700;font-size:15px'>${s.nombre}</div><div style='color:#5a6472;font-size:14px;margin:6px 0 12px'>${s.gancho}</div><a href='${s.url}' style='display:inline-block;background:#0d1117;color:#fff;text-decoration:none;font-size:13px;font-weight:700;padding:9px 16px;border-radius:8px'>Ver más</a></div>`; }).join("");
  const recs = recursosPara(C, row.hipotesis_principal);
  const recBlock = recs.length ? `<h2 style='font-size:15px;margin:22px 0 6px;color:#1a1a2e'>Recursos para ti</h2>${recs.map((r: any) => `<a href='${r.url}' style='display:block;text-decoration:none;border:1px solid #e6e8eb;border-radius:10px;padding:12px 14px;margin:8px 0;color:#1a1a2e'><span style='color:#c33a5b;font-weight:700'>▶ Video</span> &nbsp;${r.titulo}</a>`).join("")}` : "";
  return `<div style='background:#f4f5f7;padding:24px 0;font-family:Arial,Helvetica,sans-serif'><div style='max-width:560px;margin:auto;background:#fff;border-radius:14px;overflow:hidden;border:1px solid #e6e8eb'><div style='background:#0d1117;padding:22px;text-align:center'><img src='${LOGO}' alt='AthleteTrainLab' width='170' style='display:inline-block;max-width:170px'></div><div style='padding:26px 28px'><h1 style='font-size:20px;margin:0 0 6px;color:#1a1a2e'>Tu evaluación está lista</h1><p style='color:#5a6472;font-size:14px;margin:0 0 14px'>${saludo}Gracias por completar tu análisis. AthleteTrainLab no es un diagnóstico: es un sistema que, a partir de tus respuestas, estima <strong>qué áreas conviene revisar</strong> para que rindas mejor. Reduce la incertidumbre y te orienta por dónde empezar; no reemplaza una valoración profesional.</p>${resultado}${pasosBlock}${radarBlock}<h2 style='font-size:15px;margin:22px 0 4px;color:#1a1a2e'>Cómo podemos ayudarte</h2>${cards}${recBlock}<div style='background:#f0f9f4;border:1px solid #d5ead9;border-radius:10px;padding:16px 18px;margin:22px 0 4px'><div style='color:#1a1a2e;font-weight:700;font-size:15px;margin-bottom:6px'>Los 3 pilares: entrenamiento, descanso y nutrición</div><div style='color:#5a6472;font-size:14px'>Mejorar nunca depende de una sola cosa. El entrenamiento, el descanso y la nutrición son un trípode que debe estar en equilibrio: no puedes entrenar más sin una buena recuperación y una buena alimentación que lo sostengan. Entrenar y progresar depende tanto de esos dos pilares como del entreno en sí. Es lo que la mayoría pasa por alto, y por eso es lo primero que conviene cuidar.</div></div><div style='text-align:center;margin-top:16px'><a href='${WA}' style='display:inline-block;background:#25d366;color:#fff;text-decoration:none;font-size:14px;font-weight:700;padding:12px 22px;border-radius:9px;margin:4px'>Escríbenos por WhatsApp</a><a href='${AGENDA}' style='display:inline-block;background:#4fa96e;color:#fff;text-decoration:none;font-size:14px;font-weight:700;padding:12px 22px;border-radius:9px;margin:4px'>Agenda una cita</a></div></div><div style='background:#f4f5f7;padding:16px 28px;text-align:center;color:#8b95a3;font-size:12px'><a href='${SITE}' style='color:#4fa96e;text-decoration:none'>athletetrainlab.com</a> · <a href='${IG}' style='color:#4fa96e;text-decoration:none'>Instagram</a><br>Orientación basada en tus respuestas, no un diagnóstico médico.</div></div></div>`;
}

async function avisoInterno(row: any, key: string, from: { name: string; email: string }) {
  const nom = row.nombre || row.email;
  const canal = row.telefono ? "WhatsApp / mensaje de texto" : "Correo";
  const html = `<div style='font-family:Arial,sans-serif;font-size:14px;color:#1a1a2e'>` +
    `<p>Nueva persona interesada en los servicios (marcó el checkbox en la evaluación).</p>` +
    `<p><b>Nombre:</b> ${esc(row.nombre || "—")}<br>` +
    `<b>Correo:</b> ${esc(row.email || "—")}<br>` +
    `<b>Teléfono:</b> ${esc(row.telefono || "—")}<br>` +
    `<b>Canal sugerido:</b> ${canal}</p>` +
    `<p><b>Limitación:</b> ${esc(row.limitacion || "—")} · <b>Hipótesis:</b> ${esc(row.hipotesis_principal || "—")}${row.preliminar ? " (preliminar)" : ""}<br>` +
    `<b>Código:</b> ${esc(row.codigo || "—")}</p>` +
    `<p style='color:#5a6472'>Responde a este correo para escribirle directamente.</p></div>`;
  await fetch("https://api.brevo.com/v3/smtp/email", { method: "POST", headers: { "Content-Type": "application/json", "accept": "application/json", "api-key": key }, body: JSON.stringify({ sender: from, replyTo: { email: row.email, name: row.nombre || "Contacto" }, to: [{ email: LEAD }], subject: "Contactar: " + nom, htmlContent: html }) });
}
serve(async (req) => {
  try {
    const payload = await req.json();
    const row = payload.record ?? payload;
    const email = row.email;
    const key = Deno.env.get("BREVO_API_KEY");
    const fromRaw = Deno.env.get("FROM_EMAIL") ?? "AthleteTrainLab <hola@athletetrainlab.com>";
    const replyRaw = Deno.env.get("REPLY_TO") ?? "athletetrainlab@gmail.com";
    const mm = fromRaw.match(/^(.*)<(.+)>$/);
    const fromName = mm ? mm[1].trim() : "AthleteTrainLab";
    const fromEmail = mm ? mm[2].trim() : fromRaw.trim();
    if (!email) return new Response("sin email", { status: 200 });
    if (!key) { console.log("no BREVO_API_KEY; no-op", row.id); return new Response("no-op", { status: 200 }); }
    const C = await cargarConfig();
    const r = await fetch("https://api.brevo.com/v3/smtp/email", { method: "POST", headers: { "Content-Type": "application/json", "accept": "application/json", "api-key": key }, body: JSON.stringify({ sender: { name: fromName, email: fromEmail }, replyTo: { email: replyRaw, name: "AthleteTrainLab" }, to: [{ email }], subject: "Tu evaluación AthleteTrainLab", htmlContent: construirHTML(C, row) }) });
    if (row.quiere_info) { try { await avisoInterno(row, key, { name: fromName, email: fromEmail }); } catch (e) { console.error("aviso interno falló:", e); } }
    return new Response(await r.text(), { status: r.ok ? 200 : 502 });
  } catch (e) {
    console.error("error enviar-reporte:", e);
    return new Response("error: " + (e as Error).message, { status: 500 });
  }
});
