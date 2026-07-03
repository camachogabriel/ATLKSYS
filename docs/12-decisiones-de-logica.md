# Decisiones de Lógica v1.1

Resuelve los 8 puntos abiertos de `NOTAS-LOGICA.md`. Estas decisiones completan la spec v1.0 sin cambiar su arquitectura (regla de estabilidad).

## D1. Elementos evaluables (destinos de puntos)

Los puntos pueden apuntar a cuatro tipos de elemento, todos con código:

| Tipo | Código | Ejemplo |
|---|---|---|
| Capacidad | C### | C001 Capacidad aeróbica |
| Factor | F### | F001 Nutrición |
| Estado derivado | D### | D001 Disponibilidad energética |
| Capacidad emergente | E### | E001 Durabilidad |

Regla: todo destino de puntos debe existir en `knowledge/` con código. No se normalizan D/E hacia C/F: "disponibilidad energética" es más precisa que "nutrición" y esa precisión mejora la hipótesis. La relación D/E → C/F queda declarada en `emergentes.yaml` (`relacionado_con`) y se usa solo para explicar, no para transferir puntos.

## D2. Puntos contextuales

Una respuesta puede tener puntos condicionales según el contexto de la evaluación:

```yaml
puntos: {D001: 1}
puntos_condicionales:
  - si: {duracion_fondo_h: ">3"}
    puntos: {D001: 1}     # se suma al base
```

v1.1 solo admite condiciones sobre campos del contexto inicial y de la clasificación. Nada de fórmulas.

## D3. Metadatos

La lista oficial incluye los 22 originales + `disponibilidad-energetica`, `durabilidad`, `estrategia-nutricional` (usados por los ejemplos de la spec). Un metadato nuevo solo se agrega si al menos una pregunta lo genera y al menos una pregunta se activa con él.

## D4. Criterio de parada operativo

El motor deja de preguntar cuando se cumple cualquiera:

1. **Evidencia suficiente**: algún elemento alcanza confianza ALTA (≥8 puntos) y ninguna pregunta pendiente puede alterar el top-2 del ranking (impacto máximo pendiente < diferencia entre 2º y 3º).
2. **Agotamiento**: no quedan preguntas activadas por los metadatos activos.
3. **Profundidad máxima**: 25 preguntas respondidas (v1).
4. **Usuario detiene**.

Si al parar ningún elemento llegó a confianza ALTA, el resultado se marca como preliminar y se ofrece "Afinar mi resultado".

## D5. Vocabulario unificado

Las `areas_iniciales` de una limitación referencian únicamente metadatos oficiales o códigos (C/F/D/E). Términos sueltos de la spec se mapean:

| Término spec | Se convierte en |
|---|---|
| capacidad-aerobica | C001 |
| capacidad-glucolitica-oxidativa | C002 |
| capacidad-anaerobica-alactica | C003 |
| fuerza | C004 |
| capacidad-neuromuscular | C005 |
| intensidad-relativa | metadato `intensidad` |
| termorregulacion / adaptacion-al-calor | metadato `calor` + D003 |
| cadencia | metadato `tecnica` |
| posicionamiento | metadato `tecnica` |
| fatiga-previa / fatiga-acumulada | metadato `recuperacion` |
| durabilidad | E001 |
| estrategia-de-entrenamiento | F005 |

## D6. Generación de hipótesis (biblioteca H###)

Las hipótesis NO se generan por texto libre: son plantillas en `knowledge/hipotesis.yaml`. Cada una define:

- `condiciones`: elementos con confianza mínima requerida (activación).
- `contraindicadores`: elementos cuya evidencia en contra la descarta.
- `elementos`: códigos involucrados (para score y explicación).
- `recomendacion` e `informacion_faltante`.

Algoritmo:

1. Al cerrar la evaluación, se evalúan todas las plantillas.
2. Activadas = cumplen `condiciones` y ningún `contraindicador`.
3. `score(H) = Σ puntos positivos de sus elementos`.
4. Principal = mayor score. Secundarias = resto con score ≥ 50% del principal o confianza media en su elemento núcleo.
5. El resultado lista, por hipótesis, las respuestas que aportaron puntos (explicabilidad).

## D7. Análisis por objetivo

Se pospone a v1.2. Mientras tanto, cada objetivo se mapeará manualmente a 1-3 limitaciones LP### mediante una tabla `objetivos.yaml` (aún no creada). El motor no cambia.

## D8. Escala de confianza (límites cerrados)

| Puntos | Confianza |
|---|---|
| ≤3 | Baja |
| 4–7 | Media |
| 8–12 | Alta |
| ≥13 | Muy alta |

El ejemplo del cap. 3 (12 = Alta) es correcto; el del cap. 9 (13 = Alta) queda corregido a Muy alta.
