---
Proyecto: AthleteTrainLab
Documento: Motor de Razonamiento
Versión: 1.0
Estado: Borrador oficial para revisión
---

# Motor de Razonamiento

## 1. Propósito

El Motor de Razonamiento es el núcleo de AthleteTrainLab. Su función es transformar información incompleta en hipótesis útiles para orientar decisiones de entrenamiento, nutrición, recuperación y estrategia.

El motor no diagnostica. No busca certeza absoluta. Su objetivo es reducir la incertidumbre.

## 2. Principio central

El motor no busca respuestas. Busca evidencia.

Las preguntas son el mecanismo para obtener evidencia. Las respuestas generan metadatos y puntos. Los puntos construyen estados de conocimiento. Los estados de conocimiento generan hipótesis.

## 3. Flujo lógico

```text
Contexto inicial
-> Consulta principal
-> Clasificación inicial
-> Batería inicial
-> Metadatos activos
-> Preguntas de afinación
-> Puntos
-> Estado de conocimiento
-> Hipótesis
-> Resultado
```

## 4. Fase 1: Contexto inicial

El sistema obtiene datos básicos:

- Edad.
- Sexo.
- Peso.
- Estatura.
- Experiencia deportiva.
- Frecuencia de entrenamiento.
- Disciplina.
- Nivel técnico.

Estos datos no generan conclusiones por sí solos. Solo modifican la forma en que se interpreta la evidencia.

Ejemplo:

Un deportista de 43 años, 80 kg, 167 cm, con más de dos años de experiencia pero entrenando 2-3 veces por semana, no debe interpretarse igual que un atleta de 22 años que entrena seis veces por semana.

## 5. Fase 2: Consulta principal

El usuario inicia con una limitación o un objetivo.

### Limitación

"Al final de los fondos se me apaga el motor."

### Objetivo

"Quiero preparar un gran fondo."

Internamente, los objetivos se traducen a capacidades determinantes y posibles limitaciones futuras.

## 6. Fase 3: Clasificación inicial

Antes de preguntar causas, el sistema identifica qué tipo de problema está analizando.

Dimensiones utilizadas:

- Duración del esfuerzo.
- Momento en que aparece.
- Terreno.
- Sensación predominante.
- Contexto.
- Nivel del deportista.

Ejemplo:

"Me cuesta producir potencia en una subida de más de 30 minutos al final de un fondo."

Clasificación:

- Esfuerzo prolongado.
- Subida larga.
- Aparece al final de un fondo.
- Puede involucrar nutrición, durabilidad, pacing, base aeróbica y composición corporal.

## 7. Fase 4: Batería inicial

La batería inicial no busca resolver el caso. Busca identificar qué áreas merecen investigación.

No existe una sola batería universal. Cada tipo de problema tiene su propia batería inicial.

Ejemplo: fondo largo.

Preguntas iniciales posibles:

- ¿Tienes estrategia de alimentación?
- ¿Tienes estrategia de hidratación?
- ¿El clima fue más caliente de lo habitual?
- ¿Dormiste bien?
- ¿El esfuerzo fue controlado o muy exigente desde el inicio?
- ¿Qué sentiste al final: hambre, sueño, piernas vacías, falta de aire, dolor de cabeza?

## 8. Fase 5: Metadatos

Las respuestas de la batería inicial activan metadatos.

Ejemplo:

Respuesta: "No tengo estrategia de alimentación."

Metadatos:

- nutrición
- carbohidratos
- fondos largos
- disponibilidad energética

El motor no suma puntos todavía. Solo decide qué rutas investigar.

## 9. Fase 6: Preguntas de afinación

El sistema busca preguntas asociadas a los metadatos activos.

Si los metadatos activos son:

- nutrición
- carbohidratos
- hidratación

Entonces aparecen preguntas como:

- ¿Consumes carbohidratos durante el fondo?
- ¿Cuántos gramos por hora consumes?
- ¿Cuánto líquido tomas por hora?
- ¿Terminas con hambre, sueño o dolor de cabeza?

## 10. Fase 7: Puntos

En las preguntas de afinación, las respuestas sí suman o restan puntos.

Ejemplo:

Pregunta: "¿Cuántos carbohidratos consumes por hora?"

Respuesta: "No consumo."

Efecto:

- Disponibilidad energética +5.
- Durabilidad +1.
- Pacing 0.

## 11. Fase 8: Estado de conocimiento

El sistema acumula puntos por capacidad o factor.

Ejemplo:

| Elemento | Puntos | Confianza |
|---|---:|---|
| Disponibilidad energética | 12 | Alta |
| Durabilidad | 6 | Media |
| Base aeróbica | 3 | Baja |
| Estrés térmico | 0 | Baja |

## 12. Fase 9: Hipótesis

El motor interpreta el patrón.

Ejemplo:

Hipótesis principal:

"La limitación parece estar relacionada principalmente con una estrategia nutricional insuficiente para fondos largos."

Hipótesis secundarias:

- Posible contribución de durabilidad.
- Posible contribución de composición corporal.

## 13. Fase 10: Resultado

El resultado debe contener:

- Hipótesis principal.
- Hipótesis secundarias.
- Evidencia utilizada.
- Nivel de confianza.
- Información faltante.
- Recomendaciones iniciales.

## 14. Criterio de parada

El motor deja de preguntar cuando se cumple una de estas condiciones:

1. Ya existe suficiente evidencia para entregar una orientación inicial.
2. Las preguntas restantes no modificarían significativamente la conclusión.
3. Se alcanzó el máximo de profundidad definido para esa versión.
4. El usuario decide detenerse.

El sistema también puede ofrecer la opción:

"Afinar mi resultado."

Esto permite aumentar la confianza mediante más preguntas.

## 15. Reglas del motor

### Regla 1

La ausencia de evidencia no es evidencia en contra.

### Regla 2

No se descarta una hipótesis hasta tener evidencia contradictoria suficiente.

### Regla 3

Toda pregunta debe aportar evidencia o activar metadatos útiles.

### Regla 4

El sistema debe explicar por qué llegó a una hipótesis.

### Regla 5

Primero se caracteriza el problema; después se investigan causas.

## 16. Ejemplo resumido

Consulta:

"Al final de los fondos se me apaga el motor."

Batería inicial:

- Sin estrategia nutricional.
- Clima normal.
- Sueño adecuado.
- Esfuerzo controlado al inicio.

Metadatos activos:

- nutrición
- carbohidratos
- fondos largos

Afinación:

- No consume carbohidratos.
- Termina con mucha hambre y sueño.

Puntos:

- Disponibilidad energética +12.
- Durabilidad +4.
- Base aeróbica +2.

Hipótesis:

La limitación principal probablemente se relaciona con baja disponibilidad energética durante fondos largos.

## 17. Resumen

El motor funciona en dos etapas:

1. Exploración: metadatos.
2. Confirmación: puntos.

Esta separación permite mantener el sistema simple, explicable y escalable.
