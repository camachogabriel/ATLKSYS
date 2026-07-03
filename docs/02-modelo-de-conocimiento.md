---
Proyecto: AthleteTrainLab
Documento: Modelo de Conocimiento
Versión: 1.0
Estado: Borrador oficial para revisión
---

# Modelo de Conocimiento

## 1. Propósito

El modelo de conocimiento define las entidades que utiliza AthleteTrainLab para razonar. No describe la interfaz ni el código, sino la estructura conceptual que permite convertir respuestas de un usuario en hipótesis útiles.

El sistema se basa en cinco bibliotecas principales:

1. Capacidades.
2. Factores.
3. Metadatos.
4. Preguntas.
5. Hipótesis.

A estas se agregan bibliotecas auxiliares:

- Indicadores.
- Capacidades emergentes.
- Limitaciones percibidas.
- Casos de validación.
- Intervenciones.

## 2. Capacidades

Una capacidad es una propiedad fisiológica o neuromuscular inherente al organismo que puede desarrollarse mediante adaptación al entrenamiento y cuya expresión influye en el rendimiento deportivo.

Criterios para considerar algo una capacidad:

- Debe existir como propiedad fisiológica o neuromuscular real.
- Debe poder desarrollarse mediante entrenamiento.
- Debe explicar múltiples limitaciones percibidas.
- Debe poder analizarse mediante evidencia directa o indirecta.
- No debe ser simplemente la combinación de otras capacidades.

Capacidades v1.0:

| Código | Capacidad |
|---|---|
| C001 | Capacidad aeróbica |
| C002 | Capacidad glucolítica oxidativa |
| C003 | Capacidad anaeróbica aláctica |
| C004 | Fuerza |
| C005 | Capacidad neuromuscular |

## 3. Factores

Un factor es un elemento modificable, contextual o estratégico que puede influir en el desarrollo o expresión de una capacidad. A diferencia de una capacidad, un factor no siempre representa una adaptación biológica.

Ejemplos:

- Nutrición.
- Hidratación.
- Recuperación.
- Composición corporal.
- Estrategia de entrenamiento.
- Pacing.
- Técnica.
- Coordinación.
- Ambiente.
- Equipamiento.

Un factor puede ser la causa más importante de una limitación aunque la capacidad fisiológica esté relativamente bien desarrollada.

Ejemplo:

Un deportista puede tener buena capacidad aeróbica, pero una estrategia nutricional deficiente puede hacer que al final de un fondo se sienta completamente vacío.

## 4. Metadatos

Los metadatos son conectores. No son conclusiones y no tienen peso propio.

Sirven para enlazar:

- Respuestas con áreas de investigación.
- Áreas de investigación con preguntas.
- Preguntas con capacidades y factores.
- Capacidades y factores con hipótesis.

Ejemplo:

Pregunta: "¿Tienes una estrategia de alimentación para fondos largos?"

Respuesta: "No."

Metadatos generados:

- nutrición
- carbohidratos
- fondos largos
- disponibilidad energética

Estos metadatos le indican al sistema que debe buscar preguntas más específicas sobre carbohidratos, hidratación y estrategia nutricional.

## 5. Preguntas

Una pregunta es un mecanismo para obtener evidencia. La pregunta no es el conocimiento principal; el conocimiento está en las respuestas y sus efectos.

Cada pregunta debe tener:

- Código.
- Texto.
- Contexto de aplicación.
- Tipo de pregunta.
- Respuestas posibles.
- Metadatos que puede generar.
- Puntos que cada respuesta suma o resta.
- Condiciones para aparecer.

Regla fundamental:

> Toda pregunta debe modificar el estado de conocimiento o activar metadatos útiles. Si una pregunta no cambia el razonamiento, no debe existir.

## 6. Respuestas

Las respuestas son la unidad operativa más importante del sistema. Cada respuesta puede:

- Activar metadatos.
- Sumar puntos.
- Restar puntos.
- Mantener hipótesis abiertas.
- Descartar rutas de investigación.

Ejemplo:

Pregunta: "¿Cuántos carbohidratos consumes por hora en fondos largos?"

Respuestas:

| Respuesta | Efecto probable |
|---|---|
| No consumo | Disponibilidad energética +5 |
| Sí, pero no calculo | Estrategia nutricional +3 |
| Aproximadamente 30 g/h | Disponibilidad energética +3 |
| Aproximadamente 60 g/h | Nutrición insuficiente +1 o 0 según contexto |
| Más de 60 g/h | Nutrición insuficiente -3 |

## 7. Hipótesis

Una hipótesis es una explicación probable construida a partir del estado de conocimiento.

No se genera al inicio. Se genera cuando el sistema ha reunido suficiente evidencia.

Una hipótesis debe incluir:

- Nombre.
- Capacidades involucradas.
- Factores involucrados.
- Evidencia a favor.
- Evidencia en contra.
- Nivel de confianza.
- Recomendación asociada.
- Información faltante.

## 8. Indicadores

Los indicadores no son capacidades. Son mediciones o señales que ayudan a observar capacidades o factores.

Ejemplos:

- FTP.
- VO2max.
- LT1.
- LT2.
- Lactato.
- Frecuencia cardíaca.
- Potencia.
- HRV.
- Desacople cardíaco.
- RPE.

El FTP, por ejemplo, puede interpretarse como un indicador de una capacidad emergente relacionada con el rendimiento sostenido, pero no es una capacidad primaria.

## 9. Capacidades emergentes

Una capacidad emergente es una manifestación funcional que surge de la interacción entre múltiples capacidades y factores.

Ejemplos:

- Durabilidad.
- Economía.
- Rendimiento en subida.
- Rendimiento en fondos largos.
- Rendimiento en contrarreloj.
- Recuperación entre esfuerzos.

No se entrenan directamente como si fueran capacidades primarias. Se mejoran interviniendo sobre las capacidades y factores que las componen.

## 10. Limitaciones percibidas

Son la forma en que el usuario expresa su problema.

Ejemplos:

- Al final del fondo se me apaga el motor.
- Me falta el aire en las cuestas.
- No puedo responder ataques.
- Se me queman las piernas.
- Me recupero muy lento.

Las limitaciones percibidas no son diagnósticos. Son entradas al sistema.

## 11. Intervenciones

Las intervenciones son acciones destinadas a modificar capacidades o factores.

Ejemplos:

- Bloque aeróbico.
- Trabajo de intensidad.
- Estrategia de carbohidratos.
- Entrenamiento de fuerza.
- Mejora de sueño.
- Ajuste de pacing.

La intervención nace de la hipótesis, no de la capacidad aislada.

## 12. Relación general entre entidades

```text
Limitación percibida
-> Metadatos
-> Preguntas
-> Respuestas
-> Puntos
-> Capacidades / Factores
-> Estado de conocimiento
-> Hipótesis
-> Intervención
```

## 13. Regla de estabilidad

El modelo de conocimiento puede crecer, pero no debe cambiar su estructura salvo que aparezca un problema real que no pueda resolverse con las entidades existentes.
