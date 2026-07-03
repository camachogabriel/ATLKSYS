---
Proyecto: AthleteTrainLab
Documento: Sistema de Preguntas
Versión: 1.0
Estado: Borrador oficial para revisión
---

# Sistema de Preguntas

## 1. Principio

Las preguntas no son el centro del sistema. Son mecanismos para obtener evidencia.

La inteligencia del sistema está en las respuestas, sus metadatos y sus puntos.

## 2. Tipos de preguntas

### Preguntas de contexto

Definen quién es el deportista.

Ejemplos:

- Edad.
- Peso.
- Estatura.
- Experiencia.
- Frecuencia de entrenamiento.

### Preguntas de clasificación

Definen qué tipo de problema se investiga.

Ejemplos:

- ¿Dónde ocurre?
- ¿Cuándo ocurre?
- ¿Cuánto dura el esfuerzo?

### Preguntas de batería inicial

Abren rutas de investigación mediante metadatos.

Ejemplo:

- ¿Tienes estrategia de alimentación para fondos largos?

### Preguntas de afinación

Asignan puntos.

Ejemplo:

- ¿Cuántos carbohidratos consumes por hora?

## 3. Estructura de una pregunta

Cada pregunta debe tener:

- Código.
- Texto.
- Contexto.
- Tipo.
- Respuestas.
- Metadatos generados.
- Puntos por respuesta.
- Condiciones de aparición.

## 4. Ejemplo completo

### Q001 - Estrategia de alimentación en fondos largos

Texto:

¿Tienes una estrategia de alimentación para fondos largos?

Respuestas:

A. No, como cuando tengo hambre.

Metadatos:

- nutrición
- carbohidratos
- fondos largos

Puntos:

- No suma puntos todavía si es batería inicial.

B. Sí, pero no siempre la cumplo.

Metadatos:

- nutrición
- estrategia nutricional

C. Sí, consumo carbohidratos de forma planificada.

Metadatos:

- nutrición
- carbohidratos

## 5. Ejemplo de afinación

### Q002 - Carbohidratos por hora

Texto:

¿Cuántos gramos de carbohidratos consumes por hora durante un fondo largo?

Respuestas:

| Respuesta | Puntos |
|---|---|
| No consumo | Disponibilidad energética +5 |
| No calculo | Estrategia nutricional +3 |
| 30 g/h | Disponibilidad energética +3 |
| 60 g/h | Disponibilidad energética +1 |
| Más de 60 g/h | Disponibilidad energética -3 |

## 6. Regla de diseño

Cada respuesta debe representar un escenario diferente desde el punto de vista del razonamiento.

No deben existir dos respuestas distintas que produzcan exactamente el mismo efecto.
