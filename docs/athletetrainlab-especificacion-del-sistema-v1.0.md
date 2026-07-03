# AthleteTrainLab - Especificación del Sistema v1.0

Documento maestro generado a partir de los capítulos oficiales.



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


---

# Capacidades

## 1. Definición oficial

Una capacidad es una propiedad fisiológica o neuromuscular inherente al organismo que puede desarrollarse mediante procesos de adaptación al entrenamiento y cuya expresión influye en el rendimiento deportivo.

Las capacidades no se inventan para el sistema. Se derivan de la fisiología del ejercicio. AthleteTrainLab solo decide cuáles modela en su primera versión.

## 2. Criterios de inclusión

Una capacidad entra en el sistema si cumple estos criterios:

1. Existe fisiológicamente.
2. Puede desarrollarse mediante entrenamiento.
3. Explica múltiples limitaciones.
4. Puede investigarse mediante evidencia.
5. No es simplemente un indicador o una capacidad emergente.

## 3. Lista v1.0

| Código | Capacidad | Estado |
|---|---|---|
| C001 | Capacidad aeróbica | Activa |
| C002 | Capacidad glucolítica oxidativa | Activa |
| C003 | Capacidad anaeróbica aláctica | Activa |
| C004 | Fuerza | Activa |
| C005 | Capacidad neuromuscular | Activa |

## C001 - Capacidad aeróbica

### Definición

Capacidad del organismo para producir energía mediante el metabolismo oxidativo y sostener esfuerzos prolongados con un bajo costo fisiológico.

### Rol

Permite sostener esfuerzos largos, tolerar volumen de entrenamiento, recuperar mejor y retrasar la fatiga.

### Adaptaciones

- Mayor volumen sistólico.
- Mayor volumen plasmático.
- Mayor densidad mitocondrial.
- Mayor capilarización.
- Mayor actividad oxidativa.
- Mejor utilización de grasas y carbohidratos.

### Evidencias

- Duración tolerada.
- Respiración.
- RPE.
- Frecuencia cardíaca.
- Potencia.
- Lactato.
- Desacople cardíaco.
- Recuperación entre esfuerzos.

### Limitaciones relacionadas

- Me fatigo antes de lo esperado.
- Se me cae el ritmo en esfuerzos largos.
- Me falta aire en subidas largas.
- Me cuesta terminar fondos.

## C002 - Capacidad glucolítica oxidativa

### Definición

Capacidad para sostener tasas elevadas de producción energética usando carbohidratos con participación glucolítica y oxidativa.

### Rol

Es clave en esfuerzos moderados-altos y prolongados: FTP, LT2, subidas de 20-60 minutos, contrarreloj y ritmo de carrera.

### Adaptaciones

- Mayor oxidación de carbohidratos.
- Mejor aclaramiento de lactato.
- Mayor tolerancia a intensidades cercanas al umbral.
- Mejor estabilidad metabólica.

### Evidencias

- Potencia 10-60 min.
- Lactato a intensidades moderadas-altas.
- RPE elevado sostenido.
- Ardor muscular.
- Caída de ritmo cerca del umbral.

### Limitaciones relacionadas

- Se me queman las piernas en subidas largas.
- No puedo sostener ritmo fuerte.
- Me caigo en esfuerzos de 20-40 minutos.
- Me cuesta mantener el FTP.

## C003 - Capacidad anaeróbica aláctica

### Definición

Capacidad de producir energía rápidamente mediante ATP-PCr en esfuerzos explosivos y muy cortos.

### Rol

Explica sprints, arrancadas, cambios de ritmo cortos y capacidad de respuesta explosiva.

### Adaptaciones

- Mejor utilización de fosfocreatina.
- Mayor potencia máxima.
- Mejor recuperación entre esfuerzos explosivos.
- Mayor reclutamiento de fibras rápidas.

### Evidencias

- Potencia 5-15 s.
- Sprint.
- Capacidad de acelerar.
- Respuesta a ataques cortos.

### Limitaciones relacionadas

- No tengo chispa.
- Me cuesta arrancar fuerte.
- Pierdo los sprints.

## C004 - Fuerza

### Definición

Capacidad del sistema neuromuscular para producir tensión contra una resistencia.

### Rol

Permite aplicar torque, tolerar cargas musculares, mejorar la producción de potencia y reducir fatiga localizada.

### Adaptaciones

- Mayor fuerza máxima.
- Mejor reclutamiento.
- Mayor rigidez musculotendinosa.
- Mejor tolerancia a esfuerzos de alto torque.

### Evidencias

- Dificultad con baja cadencia.
- Fatiga muscular localizada.
- Historial de fuerza.
- Sensación de falta de fuerza.

### Limitaciones relacionadas

- Se me cargan mucho los cuádriceps.
- Me cuesta pedalear con baja cadencia.
- Siento que las piernas fallan antes que la respiración.

## C005 - Capacidad neuromuscular

### Definición

Capacidad del sistema nervioso para reclutar, sincronizar y activar unidades motoras de forma eficiente.

### Rol

Explica calidad de activación, respuesta a cambios de ritmo, coordinación muscular y eficiencia del movimiento.

### Adaptaciones

- Mejor reclutamiento.
- Mejor sincronización.
- Mayor velocidad de activación.
- Mejor eficiencia de aplicación de fuerza.

### Evidencias

- Cambios de ritmo.
- Cadencia.
- Fluidez del movimiento.
- Pérdida de coordinación bajo fatiga.

### Limitaciones relacionadas

- Me cuesta responder ataques.
- Siento el pedaleo torpe.
- Pierdo eficiencia cuando me fatigo.

## 4. Lo que NO es capacidad

No son capacidades primarias:

- FTP.
- VO2max.
- Durabilidad.
- Economía.
- Rendimiento en subida.
- Nutrición.
- Pacing.
- Técnica.
- Composición corporal.

Estos elementos pueden ser indicadores, factores o capacidades emergentes.


---

# Factores

## 1. Definición

Un factor es un elemento modificable, contextual o estratégico que puede afectar el desarrollo o la expresión de una capacidad.

Los factores no son capacidades porque no necesariamente representan una adaptación fisiológica directa. Sin embargo, pueden ser la causa principal de una limitación.

## 2. Factores v1.0

| Código | Factor |
|---|---|
| F001 | Nutrición |
| F002 | Hidratación |
| F003 | Recuperación |
| F004 | Composición corporal |
| F005 | Estrategia de entrenamiento |
| F006 | Pacing |
| F007 | Técnica |
| F008 | Coordinación |
| F009 | Ambiente |
| F010 | Equipamiento |

## F001 - Nutrición

Influye sobre disponibilidad energética, recuperación, adaptación y rendimiento durante esfuerzos largos o intensos.

Evidencias:

- Estrategia de alimentación.
- Carbohidratos por hora.
- Hambre al terminar.
- Sueño o vacío energético.
- Timing de comidas.

Limitaciones relacionadas:

- Me apago al final del fondo.
- Me da hambre fuerte.
- Me cuesta sostener ritmo después de varias horas.

## F002 - Hidratación

Afecta termorregulación, volumen plasmático, percepción del esfuerzo y rendimiento, especialmente en calor.

Evidencias:

- Líquido por hora.
- Sodio.
- Sed extrema.
- Dolor de cabeza.
- Calambres.
- Orina oscura.

## F003 - Recuperación

Incluye sueño, estrés, fatiga acumulada y capacidad de asimilar carga.

Evidencias:

- Calidad de sueño.
- Estrés laboral.
- Fatiga al iniciar entrenamientos.
- Bajo deseo de entrenar.
- Rendimiento irregular.

## F004 - Composición corporal

No es una capacidad, pero modifica la relación entre energía producida y trabajo externo, especialmente en subidas.

Evidencias:

- Peso.
- Estatura.
- Contexto de subidas.
- Cambios recientes de peso.
- Hábitos nutricionales.

## F005 - Estrategia de entrenamiento

Incluye estructura, progresión, distribución de intensidad, especificidad y continuidad.

Evidencias:

- Entrena siempre igual.
- Mucha zona suave sin intensidad.
- Mucha intensidad sin base.
- Falta de progresión.
- Falta de objetivos.

## F006 - Pacing

Capacidad aprendida para distribuir el esfuerzo. Es un factor porque se aprende, practica y ajusta.

Evidencias:

- Sale muy fuerte.
- Explota al final.
- No regula subidas.
- Compite por encima de sus posibilidades al inicio.

## F007 - Técnica

Habilidad aprendida que modifica la expresión de capacidades.

Evidencias:

- Pedaleo poco fluido.
- Mala posición.
- Dolor localizado.
- Pérdida de eficiencia bajo fatiga.

## F008 - Coordinación

Habilidad de organizar el movimiento. En esta versión se clasifica como factor técnico, no como capacidad primaria.

## F009 - Ambiente

Incluye calor, humedad, altitud, viento, terreno y condiciones externas.

## F010 - Equipamiento

Incluye bicicleta, posición, desarrollos, presión de llantas y material.

## 3. Regla de intervención

La intervención se dirige al factor limitante identificado, no a la capacidad de forma aislada.

Ejemplo:

Si el problema es disponibilidad energética, la intervención principal no es más entrenamiento aeróbico, sino una estrategia de carbohidratos e hidratación.


---

# Limitaciones Percibidas

## 1. Definición

Una limitación percibida es la forma en que el deportista describe aquello que siente que restringe su rendimiento.

No es una causa. No es una hipótesis. Es una entrada al sistema.

## 2. Función en el sistema

La limitación percibida permite clasificar el problema y seleccionar una batería inicial específica.

## 3. Ejemplos principales

### LP001 - Al final de los fondos se me apaga el motor

Tipo: Fondo largo.

Áreas iniciales:

- Nutrición.
- Hidratación.
- Durabilidad.
- Pacing.
- Recuperación.
- Clima.

### LP002 - Me falta el aire en las cuestas

Tipo: Subida.

Áreas iniciales:

- Capacidad aeróbica.
- Pacing.
- Composición corporal.
- Fuerza.
- Intensidad relativa.

### LP003 - Se me queman las piernas

Tipo: Fatiga muscular / metabólica.

Áreas iniciales:

- Capacidad glucolítica oxidativa.
- Fuerza.
- Pacing.
- Nutrición.
- Cadencia.

### LP004 - No puedo responder ataques

Tipo: Cambio de ritmo.

Áreas iniciales:

- Capacidad anaeróbica aláctica.
- Capacidad neuromuscular.
- Fuerza.
- Posicionamiento.
- Fatiga previa.

### LP005 - Me recupero lento entre esfuerzos

Tipo: Recuperación intrasesión.

Áreas iniciales:

- Capacidad aeróbica.
- Recuperación.
- Pacing.
- Nutrición.
- Fatiga acumulada.

### LP006 - Me siento fuerte al inicio y exploto al final

Tipo: Distribución de esfuerzo / durabilidad.

Áreas iniciales:

- Pacing.
- Nutrición.
- Hidratación.
- Durabilidad.
- Estrategia de entrenamiento.

### LP007 - Rindo mucho peor en calor

Tipo: Ambiente.

Áreas iniciales:

- Hidratación.
- Termorregulación.
- Adaptación al calor.
- Sodio.
- Pacing.

## 4. Clasificación mínima

Cada limitación debe tener:

- Código.
- Texto del usuario.
- Tipo de esfuerzo.
- Duración.
- Momento de aparición.
- Sensación principal.
- Metadatos iniciales.
- Batería inicial asociada.

## 5. Regla

La limitación no debe convertirse demasiado rápido en hipótesis. Primero debe caracterizarse:

- Dónde ocurre.
- Cuándo ocurre.
- Cómo se siente.
- En qué contexto ocurre.


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


---

# Sistema de Metadatos

## 1. Definición

Los metadatos son etiquetas que conectan respuestas con rutas de investigación.

No tienen peso. No son evidencia fuerte. No generan hipótesis directamente.

## 2. Función

Los metadatos responden:

> ¿Qué vale la pena investigar ahora?

## 3. Ejemplo

Respuesta:

"No tengo estrategia de alimentación para fondos largos."

Metadatos:

- nutrición
- carbohidratos
- hidratación
- fondos largos
- disponibilidad energética

El sistema busca preguntas relacionadas con esos metadatos.

## 4. Metadatos principales v1.0

- nutrición
- carbohidratos
- hidratación
- sodio
- sueño
- recuperación
- estrés
- calor
- pacing
- intensidad
- respiración
- piernas
- fatiga muscular
- dolor localizado
- fondos largos
- subidas largas
- sprint
- cambios de ritmo
- fuerza
- técnica
- coordinación
- composición corporal

## 5. Reglas

- Los metadatos no suman puntos.
- Los metadatos pueden activar preguntas.
- Una respuesta puede generar múltiples metadatos.
- Un metadato puede estar relacionado con múltiples preguntas.
- Los metadatos deben mantenerse simples.

## 6. Diferencia con puntos

Metadatos = dirección.

Puntos = fuerza de evidencia.

Ejemplo:

Metadato: carbohidratos.

Pregunta activada: carbohidratos por hora.

Respuesta: no consumo.

Puntos: disponibilidad energética +5.


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


---

# Roadmap

## 1. Fase 1 - Especificación del sistema

Objetivo:

Documentar completamente el sistema antes de escribir código.

Entregables:

- Arquitectura.
- Modelo de conocimiento.
- Motor de razonamiento.
- Capacidades.
- Factores.
- Sistema de preguntas.
- Metadatos.
- Puntos.
- Casos de validación.

## 2. Fase 2 - Base de conocimiento mínima

Objetivo:

Crear una primera versión funcional con:

- 5 capacidades.
- 10 factores.
- 20 limitaciones percibidas.
- 100 preguntas.
- 30 casos de validación.

## 3. Fase 3 - Prototipo funcional

Objetivo:

Implementar el motor en software.

Componentes:

- Base de datos.
- Backend.
- Motor de preguntas.
- Sistema de puntos.
- Resultado básico.

## 4. Fase 4 - Interfaz pública

Objetivo:

Crear experiencia web premium para usuarios.

Características:

- Una pregunta por pantalla.
- Diseño minimalista.
- Resultado tipo dashboard.
- Tarjeta de perfil compartible.

## 5. Fase 5 - Monetización

Modelo:

Evaluación inicial gratuita o accesible.

Monetización mediante:

- Planes de entrenamiento.
- Evaluaciones completas.
- Seguimiento.
- Integración con TrainingPeaks.

## 6. Fase 6 - Integraciones

Futuro:

- TrainingPeaks.
- Garmin.
- Strava.
- Whoop.
- Lactato.
- VO2.

## 7. Fase 7 - IA asistida

La IA no debe reemplazar el motor.

Debe usar la base de conocimiento para:

- Interpretar texto libre.
- Generar explicaciones.
- Redactar informes.
- Ayudar a entrenadores.

## 8. Principio de evolución

El conocimiento evoluciona.

La arquitectura permanece estable.
