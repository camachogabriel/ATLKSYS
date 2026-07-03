---
Proyecto: AthleteTrainLab
Documento: Arquitectura General
Versión: 1.0
Estado: Borrador oficial para revisión
---

# Arquitectura General

## 1. Propósito del documento

Este documento define la arquitectura general de AthleteTrainLab en su primera versión funcional. Su objetivo es describir cómo se organiza el sistema, cuáles son sus componentes principales y cómo interactúan durante una evaluación.

AthleteTrainLab no se concibe como un formulario tradicional ni como una calculadora de rendimiento. Es un sistema de razonamiento diseñado para reducir la incertidumbre sobre las limitaciones que afectan el rendimiento deportivo. La arquitectura se construye alrededor de una idea central: el sistema debe comprender qué le ocurre al deportista antes de recomendar qué hacer.

## 2. Principio arquitectónico central

El sistema se basa en la siguiente secuencia:

```text
Consulta principal
-> Clasificación inicial
-> Batería inicial
-> Metadatos activos
-> Preguntas de afinación
-> Puntos sobre capacidades y factores
-> Estado de conocimiento
-> Hipótesis
-> Intervenciones recomendadas
-> Reevaluación
```

Esta arquitectura separa claramente tres responsabilidades:

1. Obtener información del usuario.
2. Organizar esa información en una estructura útil.
3. Razonar sobre esa estructura para generar hipótesis.

## 3. Qué problema resuelve el sistema

El problema principal no es que los deportistas carezcan de datos. El problema es que muchas veces no saben formular la pregunta correcta.

Ejemplos de preguntas mal planteadas:

- "¿Cómo mejoro mi FTP?"
- "¿Qué entrenamiento hago para subir más rápido?"
- "¿Por qué me falta aire?"

Estas preguntas piden una solución antes de comprender el problema. AthleteTrainLab invierte el proceso: primero caracteriza la limitación, luego investiga causas posibles y finalmente prioriza intervenciones.

## 4. Entrada del sistema

La entrada puede darse por dos vías.

### 4.1 Análisis por limitación

El usuario parte de una limitación percibida:

- Al final de los fondos se me apaga el motor.
- En las cuestas me falta el aire.
- No puedo responder cambios de ritmo.
- Se me cargan mucho las piernas.

Esta es la entrada principal para la versión inicial.

### 4.2 Análisis por objetivo

El usuario parte de un objetivo:

- Quiero preparar un gran fondo.
- Quiero mejorar en subidas de 30 minutos.
- Quiero mejorar mi rendimiento en MTB maratón.

Internamente, el sistema traduce el objetivo a posibles limitaciones futuras o capacidades determinantes. El motor no cambia; solo cambia la puerta de entrada.

## 5. Objetos principales

La evaluación puede entenderse como un objeto dinámico que se va llenando conforme el usuario responde.

### 5.1 Evaluación

Contiene toda la información generada durante un análisis.

Campos principales:

- Contexto del usuario.
- Consulta principal.
- Metadatos activos.
- Capacidades activadas.
- Factores activados.
- Preguntas realizadas.
- Puntos acumulados.
- Estado de conocimiento.
- Hipótesis generadas.
- Resultado final.

### 5.2 Contexto

Datos que no explican por sí solos la limitación, pero condicionan la interpretación.

Ejemplos:

- Edad.
- Sexo.
- Peso.
- Estatura.
- Experiencia deportiva.
- Frecuencia de entrenamiento.
- Disciplina.
- Nivel técnico.

### 5.3 Consulta principal

Es la necesidad inicial del usuario. Puede ser una limitación o un objetivo. No se interpreta directamente como una causa.

### 5.4 Metadatos

Son conectores semánticos. No tienen peso. Sirven para dirigir el sistema hacia rutas de investigación.

Ejemplo:

Respuesta: "No tengo estrategia de alimentación para fondos largos."

Metadatos generados:

- nutrición
- carbohidratos
- hidratación
- fondos largos
- disponibilidad energética

### 5.5 Capacidades

Representan propiedades fisiológicas o neuromusculares desarrollables mediante adaptación al entrenamiento.

Capacidades v1.0:

- C001 Capacidad aeróbica.
- C002 Capacidad glucolítica oxidativa.
- C003 Capacidad anaeróbica aláctica.
- C004 Fuerza.
- C005 Capacidad neuromuscular.

### 5.6 Factores

Elementos modificables o contextuales que influyen en el desarrollo o expresión de las capacidades.

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

### 5.7 Hipótesis

Una hipótesis es una explicación probable construida a partir del estado de conocimiento. No es un diagnóstico.

Ejemplo:

"La limitación principal parece estar relacionada con una estrategia nutricional insuficiente para fondos largos, con contribución secundaria de composición corporal y dosificación del esfuerzo."

## 6. Flujo completo de una evaluación

### Paso 1: Contexto inicial

El sistema recoge datos básicos que ayudan a interpretar el caso. Estos datos no generan conclusiones por sí solos.

### Paso 2: Consulta principal

El usuario elige si quiere analizar una limitación o prepararse para un objetivo.

### Paso 3: Clasificación inicial

El sistema identifica el tipo de problema:

- Fondo largo.
- Subida corta.
- Subida larga.
- Sprint.
- Cambio de ritmo.
- Recuperación.
- Dolor.
- Calor.

### Paso 4: Batería inicial específica

No existe una batería universal. La batería depende del tipo de problema.

Ejemplo: para fondos largos se investigan nutrición, hidratación, clima, pacing, sueño, fatiga y sensación final.

### Paso 5: Activación de metadatos

Las respuestas iniciales activan metadatos. Los metadatos no suman puntos; indican qué áreas merece la pena investigar.

### Paso 6: Preguntas de afinación

El sistema selecciona preguntas específicas relacionadas con los metadatos activos.

### Paso 7: Puntos

Las respuestas de afinación suman o restan puntos a capacidades o factores.

### Paso 8: Estado de conocimiento

El sistema calcula qué tan fuerte es la evidencia para cada capacidad o factor.

### Paso 9: Hipótesis

El sistema interpreta el patrón de puntos y genera hipótesis priorizadas.

### Paso 10: Resultado

El usuario recibe:

- Hipótesis principal.
- Hipótesis secundarias.
- Evidencia utilizada.
- Nivel de confianza.
- Información faltante.
- Recomendaciones iniciales.

## 7. Principios de diseño

### 7.1 Simplicidad primero

La versión inicial utiliza reglas, metadatos y puntos. No se implementan modelos probabilísticos complejos ni IA generativa como núcleo del razonamiento.

### 7.2 Explicabilidad

Toda conclusión debe poder explicarse. El sistema debe mostrar qué respuestas llevaron a una hipótesis.

### 7.3 Arquitectura estable, conocimiento evolutivo

La arquitectura no debe cambiar constantemente. Lo que evoluciona es la base de conocimiento: preguntas, metadatos, factores, hipótesis y casos.

### 7.4 No diagnosticar

AthleteTrainLab no emite diagnósticos médicos ni fisiológicos absolutos. Genera hipótesis orientativas.

### 7.5 Reducir incertidumbre

Una buena evaluación no elimina la incertidumbre; la reduce lo suficiente para tomar mejores decisiones.

## 8. Resumen operativo

AthleteTrainLab puede resumirse así:

```text
El usuario expresa una limitación.
El sistema la clasifica.
El sistema pregunta lo mínimo necesario para saber qué investigar.
Los metadatos activan rutas de afinación.
Las respuestas generan puntos.
Los puntos construyen estados de conocimiento.
Los estados de conocimiento generan hipótesis.
Las hipótesis orientan intervenciones.
```
