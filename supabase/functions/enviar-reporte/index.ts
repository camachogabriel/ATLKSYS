// AthleteTrainLab - Edge Function: enviar reporte por correo
// Se dispara vía Database Webhook al INSERT en public.evaluaciones.
// Cruza la hipótesis con el catálogo de servicios y envía el correo (Resend).
//
// Requisitos (configurar en Supabase, no en el código):
//   - Secret RESEND_API_KEY  (Project Settings -> Edge Functions -> Secrets)
//   - Secret FROM_EMAIL      (remitente verificado en Resend, ej. hola@tudominio.com)
//   - Database Webhook: tabla evaluaciones, evento INSERT -> esta función
// Si falta RESEND_API_KEY la función no falla: registra y responde 200 (no-op).

import { serve } from "https://deno.land/std@0.224.0/http/server.ts";

// Catálogo mínimo hipótesis -> servicio (espejo de knowledge/servicios.yaml).
// Mantener en sync; el YAML es la fuente de verdad.
const SERVICIOS: Record<string, { nombre: string; gancho: string; prioridad: number }> = {
  SV_BIKEFIT: { nombre: "Estudio de posición (Bike Fit)", prioridad: 1, gancho: "Tu evaluación apunta a que la posición o la técnica te están sobrecargando. Un bike fit suele desbloquear rendimiento y comodidad." },
  SV_COACHING: { nombre: "Planes de entrenamiento / coaching", prioridad: 1, gancho: "Tu mayor margen está en cómo entrenas. Un plan estructurado convierte tu esfuerzo en mejora real." },
  SV_NUTRICION: { nombre: "Asesoría nutricional", prioridad: 1, gancho: "La energía disponible parece tu limitante. Una estrategia de alimentación e hidratación cambia cómo terminas los fondos." },
  SV_FISIOLOGIA: { nombre: "Valoración fisiológica y tests", prioridad: 2, gancho: "Para afinar conviene medir: umbrales, metabolismo y respuesta cardíaca." },
  SV_CONTACTO: { nombre: "Habla con nosotros", prioridad: 9, gancho: "¿Quieres que revisemos tu caso a fondo? Escríbenos para una orientación personalizada." },
};
const REGLAS: Record<string, string[]> = {
  H015: ["SV_BIKEFIT"], H009: ["SV_COACHING"], H012: ["SV_COACHING"],
  H002: ["SV_COACHING"], H008: ["SV_COACHING"], H001: ["SV_NUTRICION"],
  H007: ["SV_NUTRICION"], H004: ["SV_FISIOLOGIA"], H005: ["SV_FISIOLOGIA"],
  H013: ["SV_FISIOLOGIA"], H010: ["SV_FISIOLOGIA"], H006: ["SV_FISIOLOGIA"],
};

function serviciosPara(hipPrincipal: string | null): string[] {
  const set = new Set<string>();
  if (hipPrincipal && REGLAS[hipPrincipal]) REGLAS[hipPrincipal].forEach((s) => set.add(s));
  set.add("SV_CONTACTO"); // cierre siempre
  return [...set].sort((a, b) => SERVICIOS[a].prioridad - SERVICIOS[b].prioridad);
}

serve(async (req) => {
  try {
    const payload = await req.json();
    const row = payload.record ?? payload; // webhook: {type, record, ...}
    const email = row.email;
    const key = Deno.env.get("RESEND_API_KEY");
    const from = Deno.env.get("FROM_EMAIL") ?? "AthleteTrainLab <onboarding@resend.dev>";

    if (!email) return new Response("sin email, nada que enviar", { status: 200 });
    if (!key) {
      console.log("RESEND_API_KEY no configurada; no se envía (no-op). Fila:", row.id);
      return new Response("no-op: falta RESEND_API_KEY", { status: 200 });
    }

    const svs = serviciosPara(row.hipotesis_principal);
    const bloques = svs.map((c) =>
      `<div style="border:1px solid #30363d;border-radius:10px;padding:14px;margin:10px 0">
         <strong style="color:#2dd4bf">${SERVICIOS[c].nombre}</strong>
         <p style="color:#8b949e;font-size:14px;margin:6px 0 0">${SERVICIOS[c].gancho}</p>
       </div>`).join("");
    const html =
      `<div style="font-family:sans-serif;max-width:560px;margin:auto;color:#e6edf3;background:#0d1117;padding:24px;border-radius:12px">
         <h2>Tu evaluación AthleteTrainLab</h2>
         <p style="color:#8b949e">Gracias por completar tu análisis. Según tus respuestas, esto es lo que puede ayudarte más:</p>
         ${bloques}
         <p style="color:#6e7681;font-size:12px;margin-top:20px">Orientación basada en tus respuestas, no un diagnóstico médico.</p>
       </div>`;

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
