---
Proyecto: AthleteTrainLab
Documento: Sistema de Puntos
Versión: 1.0
Estado: Borrador oficial para revisión
---

# Sistema de Puntos

## 1. Definición

Los puntos representan evidencia acumulada sobre una capacidad o factor.

No son probabilidades matemáticas. No deben interpretarse como diagnóstico.

## 2. Cuándo aparecen

Los puntos no aparecen en todas las preguntas.

Fase inicial:

- Genera metadatos.

Fase de afinación:

- Suma o resta puntos.

## 3. Escala inicial sugerida

| Valor | Interpretación |
|---:|---|
| +5 | Evidencia muy fuerte a favor |
| +3 | Evidencia moderada |
| +1 | Evidencia leve |
| 0 | No modifica |
| -1 | Evidencia leve en contra |
| -3 | Evidencia moderada en contra |
| -5 | Evidencia fuerte en contra |

## 4. Ejemplo

Pregunta:

¿Cuántos carbohidratos consumes por hora?

Respuesta:

No consumo.

Puntos:

- Disponibilidad energética +5.
- Durabilidad +1.

## 5. Estado de conocimiento

Al acumular puntos, el sistema construye estados.

Ejemplo:

| Elemento | Puntos | Confianza |
|---|---:|---|
| Disponibilidad energética | 13 | Alta |
| Durabilidad | 5 | Media |
| Base aeróbica | 2 | Baja |

## 6. Conversión a confianza

La confianza puede clasificarse de forma simple:

| Puntos | Confianza |
|---:|---|
| 0-3 | Baja |
| 4-7 | Media |
| 8-12 | Alta |
| >12 | Muy alta |

Estos rangos deben calibrarse con casos reales.

## 7. Regla

Una hipótesis no nace de una sola respuesta. Nace del patrón acumulado.

## 8. Transparencia

El resultado debe mostrar qué respuestas aportaron puntos relevantes.
