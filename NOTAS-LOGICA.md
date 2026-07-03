# Puntos abiertos de lógica

Los 8 puntos detectados al estructurar la spec v1.0 fueron **resueltos** en `docs/12-decisiones-de-logica.md`:

| # | Punto | Resolución |
|---|---|---|
| 1 | Destinos de puntos sin código | D1: cuatro tipos evaluables C/F/D/E, todos con código |
| 2 | Puntos contextuales | D2: `puntos_condicionales` sobre campos de contexto |
| 3 | Metadatos fuera de lista | D3: oficializados + regla de crecimiento |
| 4 | Criterio de parada | D4: 4 condiciones operativas, máx. 25 preguntas |
| 5 | Vocabulario áreas iniciales | D5: tabla de mapeo, aplicada en `limitaciones.yaml` |
| 6 | Generación de hipótesis | D6: biblioteca H### en `hipotesis.yaml` + ranking por score |
| 7 | Análisis por objetivo | D7: pospuesto a v1.2 (`objetivos.yaml`) |
| 8 | Confianza solapada | D8: ≤3 baja, 4-7 media, 8-12 alta, ≥13 muy alta |

## Pendientes nuevos

- Calibrar rangos de confianza y el umbral 50% del ranking con los 30 casos de validación (Fase 2).
- Crear `objetivos.yaml` (v1.2).
- Definir el algoritmo de selección de la *siguiente* pregunta cuando hay varias activadas (orden por impacto potencial vs. orden fijo por batería).
