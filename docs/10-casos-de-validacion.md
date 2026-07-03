---
Proyecto: AthleteTrainLab
Documento: Casos de Validación
Versión: 1.0
Estado: Borrador oficial para revisión
---

# Casos de Validación

## 1. Propósito

Los casos de validación sirven para probar si el motor razona como un entrenador.

No se usan para entrenar una IA. Se usan para validar la metodología.

## 2. Caso MHV-001

### Consulta

"Al final de los fondos largos se me apaga el motor."

### Contexto

- 43 años.
- 80 kg.
- 167 cm.
- Más de 2 años entrenando.
- Entrena 2-3 veces por semana.

### Clasificación

- Fondo largo.
- Fatiga al final.
- Posible subida al final.

### Batería inicial

Preguntas sugeridas:

- Estrategia de alimentación.
- Estrategia de hidratación.
- Clima.
- Sueño.
- Intensidad/pacing.
- Síntomas finales.

### Respuestas simuladas

- No tiene estrategia nutricional.
- Clima normal.
- Durmió bien.
- Se siente exigido desde el inicio de la subida final.
- Termina con hambre y sueño.

### Metadatos activos

- nutrición
- carbohidratos
- fondos largos
- disponibilidad energética
- pacing
- durabilidad

### Afinación

Pregunta:

¿Cuántos carbohidratos consume por hora?

Respuesta:

No consume o consume muy poco.

Puntos:

- Disponibilidad energética +5.
- Durabilidad +1.

### Hipótesis

Hipótesis principal:

Estrategia nutricional insuficiente para fondos largos.

Factores contribuyentes:

- Mayor costo energético por composición corporal.
- Posible pacing inadecuado.
- Posible baja durabilidad si se confirma con más evidencia.

### Intervención inicial

Diseñar estrategia de carbohidratos e hidratación antes de concluir que la limitación principal es baja capacidad aeróbica.

## 3. Caso MHV-002

### Consulta

"En la primera cuesta ya me falta el aire."

### Clasificación

- Subida temprana.
- No depende de fatiga acumulada.

### Áreas iniciales

- Capacidad aeróbica.
- Intensidad relativa.
- Composición corporal.
- Pacing.
- Fuerza.

### Diferencia con MHV-001

La nutrición durante el esfuerzo pierde importancia inicial porque el problema ocurre temprano.

## 4. Caso MHV-003

### Consulta

"No puedo responder ataques."

### Áreas iniciales

- Capacidad anaeróbica aláctica.
- Capacidad neuromuscular.
- Fuerza.
- Fatiga previa.
- Posicionamiento.

## 5. Regla de validación

Un caso valida el sistema si:

- La batería inicial corresponde al tipo de problema.
- Los metadatos abren rutas lógicas.
- Las preguntas de afinación son relevantes.
- Los puntos conducen a una hipótesis explicable.
- La recomendación no salta a conclusiones prematuras.
