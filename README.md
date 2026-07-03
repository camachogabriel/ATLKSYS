# AthleteTrainLab (ATL)

Sistema de razonamiento para identificar qué limita el rendimiento de un deportista. No es un formulario ni una calculadora: primero caracteriza la limitación, luego investiga causas y finalmente prioriza intervenciones.

```text
Consulta → Clasificación → Batería inicial → Metadatos → Afinación → Puntos
→ Estado de conocimiento → Hipótesis → Intervenciones
```

## Estructura del repo

| Carpeta | Contenido |
|---|---|
| `docs/` | Especificación v1.0 (11 capítulos + documento maestro) |
| `knowledge/` | Base de conocimiento estructurada (YAML): capacidades, factores, emergentes, metadatos, limitaciones, preguntas, puntos |
| `knowledge/casos/` | Casos de validación (MHV-###) |
| `engine/` | Motor de razonamiento (Fase 3, pendiente) |

## Principios de diseño

1. Simplicidad primero: reglas, metadatos y puntos; sin IA generativa como núcleo.
2. Explicabilidad: toda hipótesis muestra la evidencia que la generó.
3. Arquitectura estable, conocimiento evolutivo.
4. No diagnosticar: hipótesis orientativas, no diagnósticos médicos.
5. Reducir incertidumbre, no eliminarla.

## Estado

- [x] Fase 1 — Especificación del sistema
- [ ] Fase 2 — Base de conocimiento mínima (5 capacidades ✓, 10 factores ✓, 20 limitaciones [7/20], 100 preguntas [2/100], 30 casos [3/30])
- [ ] Fase 3 — Prototipo funcional (motor)
- [ ] Fase 4 — Interfaz pública
- [ ] Fase 5+ — Monetización, integraciones, IA asistida

Ver `NOTAS-LOGICA.md` para puntos abiertos detectados al estructurar la base de conocimiento.
