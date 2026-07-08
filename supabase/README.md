# Supabase — captura y reporte por correo

## Arquitectura (separación captura / entrega)

```
Quiz (GitHub Pages)  --insert-->  tabla evaluaciones  --webhook INSERT-->  Edge Function enviar-reporte  --Brevo-->  correo al usuario
```

- **Quiz**: solo capta y escribe en `evaluaciones` (RLS insert-only). No envía correo.
- **Edge Function `enviar-reporte`**: al insertarse una fila, cruza la hipótesis con el catálogo de servicios y envía el correo. La lógica comercial (qué servicio ofrecer) es conocimiento versionable en `knowledge/servicios.yaml`.

## Catálogo de servicios

`knowledge/servicios.yaml` es la **única fuente de verdad** del mapeo hipótesis → servicio (bike fit, coaching, nutrición, valoración fisiológica, contacto). `engine/reporte.py` prueba el emparejamiento en local. El `index.ts` de la función **se genera** desde el YAML:

```
python3 supabase/build_function.py     # regenera functions/enviar-reporte/index.ts
# luego redeplegar la función (MCP o `supabase functions deploy enviar-reporte`)
```

No editar el bloque de datos del `index.ts` a mano: editar el YAML y regenerar.

## Pasos manuales pendientes (los hace Gabriel)

1. **Cuenta en Brevo** (resend.com, plan gratis). Verificar un dominio remitente (o usar `onboarding@resend.dev` para pruebas).
2. **Secrets** en Supabase → Project Settings → Edge Functions → Secrets:
   - `BREVO_API_KEY` = la API key de Brevo.
   - `FROM_EMAIL` = remitente verificado, ej. `AthleteTrainLab <hola@tudominio.com>`.
   Sin `BREVO_API_KEY` la función no falla: registra y no envía (no-op).
3. **Database Webhook**: Supabase → Database → Webhooks → crear:
   - Tabla `public.evaluaciones`, evento `INSERT`.
   - Tipo: Supabase Edge Function → `enviar-reporte`.
   - Incluye la service role key en el header (opción del asistente de webhooks).

## Probar

Tras configurar los secrets, completar una evaluación en el quiz debería llegar un correo. Los logs de la función están en Supabase → Edge Functions → enviar-reporte → Logs.
