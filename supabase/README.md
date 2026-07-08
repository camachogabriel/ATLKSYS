# Supabase — captura y correo (en producción)

## Flujo
```
Quiz (GitHub Pages) --insert--> tabla evaluaciones --trigger pg_net--> Edge Function enviar-reporte --Brevo--> correo
```
- Quiz capta y escribe en `evaluaciones` (RLS insert-only). No envía correo.
- Trigger `on_evaluacion_insert` (pg_net) llama a la función al insertarse una fila.
- Edge Function `enviar-reporte` cruza la hipótesis con `servicios.yaml` y envía por Brevo.
- Sugerencias de casos propios del usuario -> tabla `sugerencias` (RLS insert-only).

## Correo (Brevo)
- Proveedor: Brevo (api.brevo.com/v3/smtp/email). Free 300/día.
- Dominio `athletetrainlab.com` autenticado (DKIM brevo1/brevo2 + SPF + brevo-code) vía integración Brevo-Wix.
- Secrets en Supabase (Edge Functions): `BREVO_API_KEY`, `FROM_EMAIL` (= "AthleteTrainLab <hola@athletetrainlab.com>"), opcional `REPLY_TO` (default athletetrainlab@gmail.com).
- Remitente desde el dominio autenticado (cumple requisitos Google/Yahoo/MS). Respuestas via reply-to al gmail.

## Cambiar servicios / correo
Editar `knowledge/servicios.yaml` (fuente única) -> `python3 supabase/build_function.py` -> redeploy de la función.

## Diagnóstico
La respuesta de Brevo queda en `net._http_response` (Postgres):
`select status_code, content from net._http_response order by created desc limit 5;`
- content con `messageId` = enviado. `no-op` = falta BREVO_API_KEY. Error de Brevo = aparece su mensaje.

## Pendiente / mejoras
- Panel para leer evaluaciones + sugerencias.
- Verificar entregabilidad real (bandeja vs spam) con envíos a varios proveedores.
