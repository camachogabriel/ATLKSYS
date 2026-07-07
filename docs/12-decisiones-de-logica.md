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

Implementado en v1.1 con mapeo simple: `knowledge/objetivos.yaml` define objetivos O### que apuntan a la limitación LP### cuya batería investiga lo mismo (ej. O001 "Terminar los fondos más fuerte" → LP001). El motor, la batería y las hipótesis son idénticos; cambian dos cosas:

1. **Puerta de entrada**: pantalla inicial "¿Qué te trae por aquí?" → algo me frena (limitación) / quiero mejorar algo (objetivo).
2. **Copy del resultado**: en modo objetivo la hipótesis se presenta como "tu mayor palanca de mejora" en vez de "tu limitación probable", y el resultado sin causa dominante se presenta en positivo ("no hay un freno claro; estas son tus áreas con más margen").

Cada objetivo declara además `capacidades_determinantes` (informativo, para el informe). Mapeo 1-a-N objetivo→limitaciones queda para cuando un objetivo real no encaje en una sola LP.

## D8. Escala de confianza (límites cerrados)

| Puntos | Confianza |
|---|---|
| ≤3 | Baja |
| 4–7 | Media |
| 8–12 | Alta |
| ≥13 | Muy alta |

El ejemplo del cap. 3 (12 = Alta) es correcto; el del cap. 9 (13 = Alta) queda corregido a Muy alta.

## D9. Selección de la siguiente pregunta (afinación)

Candidatas = preguntas de afinación no respondidas cuyos `metadatos_requeridos` estén todos en los metadatos activos.

Orden: mayor **impacto potencial** primero (máximo valor absoluto de puntos entre sus respuestas). Empate: código menor. Así el quiz pregunta primero lo que más puede mover el ranking, acortando la evaluación.

## D10. Batería por tipo de problema

Las preguntas de batería inicial declaran `tipos: [...]` y se seleccionan por el `tipo` de la limitación elegida, no por código LP. Esto cumple la spec original ("la batería depende del tipo de problema") y permite que varias limitaciones compartan batería sin duplicar preguntas. Tipos v1: fondo-largo, distribucion-de-esfuerzo, subida, fatiga-muscular-metabolica, cambio-de-ritmo, recuperacion-intrasesion, ambiente.

## D11. Capacidades (fisiológico) vs. dimensiones de rendimiento (objetivos/emergentes)

Las dimensiones clásicas de fitness (fuerza, velocidad, potencia, resistencia aeróbica, resistencia anaeróbica, flexibilidad) describen el **rendimiento observable/medible** — lo que se ve en un test. Las **capacidades** de ATL (C001-C005) describen los **mecanismos fisiológicos** que producen ese rendimiento. Son dos capas distintas y ATL las mantiene separadas a propósito: mezclarlas rompería la distinción causa/síntoma que es el valor del sistema.

Regla de asignación de capas:

| Capa | Qué es | Dónde vive en ATL |
|---|---|---|
| Lenguaje del cliente | Cómo expresa su problema o meta | Limitaciones (LP###) y Objetivos (O###) |
| Rendimiento observable | Velocidad, potencia, resistencia aeróbica/anaeróbica, durabilidad, economía | Objetivos y Capacidades emergentes (E###) |
| Mecanismo fisiológico | La causa que el motor razona | Capacidades (C###) |
| Contexto modificable | | Factores (F###) |

Consecuencias:

- **Velocidad y potencia NO son capacidades.** Son resultados: potencia = fuerza × velocidad de contracción, dependiente de C004 + C005 + sistema energético. Entran como objetivos/emergentes y el motor los traduce a sus determinantes fisiológicos vía `capacidades_determinantes`.
- **Resistencia anaeróbica** ya está cubierta por C002 (glucolítica oxidativa / tolerancia al lactato); no se añade capacidad nueva.
- **Flexibilidad**: en ciclismo rara vez es limitante; si se necesita, entra como factor (junto a técnica), no como capacidad.
- El puente cliente→fisiología ya existe: `knowledge/objetivos.yaml` mapea cada objetivo a la limitación cuya batería lo investiga y declara sus `capacidades_determinantes`. En modo objetivo, el informe habla en lenguaje de rendimiento ("tu palanca para X es Y") mientras el motor razona en la capa fisiológica.

Decisión: **capacidades y factores permanecen fisiológicos/contextuales; el lenguaje de rendimiento se modela en objetivos y emergentes.** Enriquecer el sistema con nuevas dimensiones de rendimiento se hace agregando objetivos, no capacidades.

## D12. Peso, estatura e IMC como señal de composición corporal

El contexto inicial captura `peso_kg` y `estatura_cm` (opcionales). Con ellos se calcula el IMC = peso / (estatura_m)². Usos:

1. **Señal de investigación (no conclusión).** Si IMC ≥ 27, se activa el metadato `composicion-corporal` al iniciar la evaluación, abriendo su ruta de afinación (Q027/Q028) aunque la batería no lo hubiera abierto. El IMC no suma puntos ni concluye por sí solo — solo dirige (coherente con el principio metadatos = dirección, y con "el contexto modifica la interpretación, no concluye").
2. **Relación peso-potencia.** Alimenta H010 y el objetivo O002 (subir más rápido).
3. **Informe.** Se muestra el IMC con su categoría y una nota honesta: es una referencia inicial, la masa muscular puede elevarlo sin exceso de grasa, y cualquier ajuste debe ser gradual y con apoyo profesional (salvaguarda de bienestar; nunca recomendar déficits agresivos).

Otros usos previstos de peso/estatura (futuro): escalar recomendaciones de carbohidratos (g/h) e hidratación al tamaño corporal, y estimar vatios/kg cuando el usuario aporte potencia. El código de evaluación incluye peso y estatura (campos 5 y 6 del contexto); códigos antiguos sin ellos siguen siendo válidos.

Umbral IMC ≥ 27 (no 25) para reducir falsos positivos en deportistas musculados. Calibrable.

## D13. Adiposidad central como señal orientadora hacia C002 (no diagnóstico)

Cuando el IMC es alto y hay indicios de peso en la zona central (Q057-A), ATL **no** infiere ni menciona causas metabólicas/hormonales (resistencia a la insulina, etc.): eso es terreno médico fuera de alcance. Lo que hace es tratarlo como **una señal débil más** que orienta hacia una limitación que el sistema ya modela — la capacidad glucolítica oxidativa (C002).

Salvaguardas:

- El peso central suma solo **+1 a C002** (orientador, leve). Nunca concluye por sí solo: H005 (limitación glucolítica) exige C002 en confianza alta (≥8), que solo se alcanza con evidencia de rendimiento que lo respalde.
- La evidencia que sí pesa viene del patrón de rendimiento: Q058 (bien en suave / mal en intensidad, +5), Q059 (mala tolerancia a 2-5 min duros, +3), Q014/Q015 (piernas se queman en sostenido, +3/+5). Es el patrón acumulado —adiposidad + intolerancia a la intensidad + piernas que arden + buen fondo suave— el que converge en C002.
- La salida es siempre "limitación glucolítica" con recomendación de entrenamiento y nutrición (H005). En ningún punto se nombra insulina, hormonas ni diagnóstico.
- Q057-A también suma F001 +1 (nutrición) y abre el metadato `intensidad` para investigar el contraste suave/intenso.

Principio: usar la pista para orientar la solución, sin afirmar la causa fisiopatológica.

## D14. Discriminar nutricional vs. aeróbico en fondos (perfil delgado dependiente de carbos)

Un ciclista delgado que "se le cae la máquina" en fondos parece tener limitación aeróbica, pero suele ser **disponibilidad energética**: reservas de glucógeno pequeñas + alta dependencia del carbohidrato + baja oxidación de grasa → agota el combustible antes de tiempo. Es el espejo de D13 (IMC alto → C002).

Discriminador clave (Q060): **¿comer revive el rendimiento?**
- Sí, como y revivo → D001 +5 (nutricional/energético; NO aeróbico).
- No, sigo fundido aunque coma → C001 +3, E001 +1 (ahí sí mirar aeróbico/durabilidad).

Refuerzo (Q061): dependencia declarada de comer para rendir → D001.

IMC bajo (< 20) como señal orientadora: abre las rutas `disponibilidad-energetica`, `nutricion` y `carbohidratos` al iniciar (dirección, no puntos), para que el discriminador aparezca. Umbral calibrable.

H001 se amplió para cubrir ambos casos (no alimentarse / alta dependencia) y su recomendación incluye construir base aeróbica para mejorar la oxidación de grasa. Como H004 (aeróbica) exige C001 alta y el discriminador manda los puntos a D001, el motor separa correctamente "es nutricional" de "es aeróbico".

## D15. Género/sexo como contexto de interpretación (no de puntaje)

El sexo biológico se captura en el contexto (hombre / mujer / prefiero no decirlo). Los umbrales numéricos de IMC son iguales por sexo (OMS); lo que cambia es la composición e interpretación:

- **NO modifica el puntaje** de capacidades ni factores (evitar estereotipos y ciencia frágil; la lógica peso-potencia y "comer revive" es sexo-neutra). Igual que la edad, el sexo modula la interpretación, no concluye.
- **Sí ajusta el mensaje** del informe:
  - IMC alto en mujer: recordatorio de que la grasa esencial es mayor y necesaria; el objetivo es más potencia, no grasa corporal muy baja.
  - IMC bajo: refuerzo de disponibilidad energética; en mujeres, mención de que la energía crónicamente baja puede afectar ciclo/huesos/rendimiento (conciencia de RED-S), con sugerencia de valoración profesional — sin diagnosticar.

El código de evaluación incluye el sexo (campo 7 del contexto); códigos previos sin él siguen siendo válidos.

## D16. Reformulación por modo, opción de escape y entrenamiento estructurado

Tres ajustes nacidos de pruebas reales (objetivo O001, código del 2026-07-06):

1. **Texto por modo.** Las preguntas de batería pueden declarar `texto_objetivo`, que el quiz usa en modo objetivo. Evita que preguntas escritas para "algo me falla" suenen presuntuosas cuando el usuario solo quiere rendir más (ej. Q009 pasa de «cuando se apaga el motor…» a «si el ritmo se te cae al final…»).
2. **Opción de escape.** Q009 gana la opción E ("ninguna; aguanto bien, solo quiero rendir más"), que no concluye nada: activa metadatos amplios (intensidad, respiración, fuerza) para que el motor siga investigando por las rutas de mayor impacto (D9). Toda pregunta de caracterización con opciones cerradas debería ofrecer una salida así, para no forzar respuestas que no aplican.
3. **Entrenamiento estructurado (Q062).** Detecta si el usuario solo "sale a rodar" sin trabajos de intensidad/fuerza → alimenta F005 (estructura) y abre la ruta de fuerza. Cubre el caso "quiere ir más rápido y su entrenamiento no está estructurado".

Además, H002 (durabilidad) refuerza su recomendación: se construye sobre base aeróbica con fuerza y calidad al final de sesiones largas; fuerza y aeróbico van de la mano.

## D17. Capa de pulso (indicador de frecuencia cardíaca)

La FC y el desacople cardíaco son **indicadores** (spec cap. 2 y 8), no capacidades: formas de observar capacidades/factores. Solo aplican a quien usa pulsómetro.

- Contexto: pregunta "¿Entrenas con monitor de ritmo cardíaco?" → `ctx.usa_hr`. Si es sí, se siembra el metadato `pulso` al iniciar.
- Las preguntas de pulso se activan con `[pulso, <ruta>]`: aparecen solo si el usuario usa pulsómetro Y la ruta correspondiente está abierta. No suman por sí solas evidencia de una capacidad nueva; refuerzan factores/capacidades ya existentes:
  - Q063 [pulso, intensidad]: pulso disparado en cuestas → C001 (nivel aeróbico); pulso plano/no sube → F003 (fatiga).
  - Q064 [pulso, calor]: pulso alto a igual intensidad en calor → D003 estrés térmico + F002 hidratación.
  - Q065 [pulso, disponibilidad-energetica]: desacople al final de fondos (sube aunque baje el ritmo) → F002 hidratación + D001 + E001 (indicador clásico de deriva cardíaca por deshidratación/combustible).
  - Q066 [pulso, recuperacion]: pulso en reposo elevado → F003 recuperación/fatiga.

El código de evaluación incluye `usa_hr` (campo 8); códigos previos siguen válidos. Ampliable: HRV, zonas, umbral por FC, etc.

## D18. Limitación de respuesta cardíaca + doble texto por modo

**LP008 "Se me sube mucho el pulso" / O007 "Pulsar menos en esfuerzos intensos".** Nuevo tipo `respuesta-cardiaca`. La limitación implica uso de pulsómetro, así que su batería (Q067-Q069) siembra el metadato `pulso` y abre rutas según la respuesta: pulso alto en todo→aeróbica (C001→H004), en calor→D003 (H007), con fatiga→F003 (H008). Matiz de honestidad: la FC es individual; si el usuario responde "solo al compararme, me siento bien", no se fuerza hipótesis (resultado preliminar tranquilizador). No se crea capacidad nueva: la FC es indicador.

**Doble texto por modo (generalización de D16).** Toda pregunta puede declarar `texto_objetivo`; el quiz lo usa en modo objetivo (fallback a `texto`). Principio: las preguntas neutras ("¿tienes plan de hidratación?") no lo necesitan; solo las que suenan a problema ("¿cuándo aparece el problema?" → "¿en qué momento se te complica subir?"). Se rellena `texto_objetivo` de forma incremental donde el enfoque cambie.

## D19. FC para entender el esfuerzo: normal individual vs. sobreesfuerzo

El pulso alto tiene dos lecturas opuestas y ATL las separa con Q071/Q072:

- **Individual normal (H013):** misma potencia y sensaciones que otros, respira bien pese al número alto → suma a D005 (respuesta cardíaca individual). H013 no es una limitación: dice que el pulso alto probablemente es fisiología personal, sugiere trabajo aeróbico suave y recomienda valoración fisiológica y cardíaca profesional (orientación, no diagnóstico). Se descarta si hay señales de sobreesfuerzo real (contraindicador C001).
- **Sobreesfuerzo (H004):** pulso alto + respiración agitada + sufre más que sus pares → C001 (base aeróbica / trabaja por encima de su nivel).

Además Q070 usa la FC como lente del esfuerzo: si al final del fondo el pulso queda más alto que al inicio a igual ritmo, el fondo fue más fuerte de lo sostenible → dosificación (F006). Se distingue de Q065 (desacople que sube al aflojar → hidratación/combustible).

Principio: la FC no se compara entre personas; se usa para entender el esfuerzo propio, no como número absoluto.

## D20. Fase de perfil general (pre-carga de puntos)

Antes de la batería, un bloque corto de preguntas `tipo: perfil` se hace a todos (independiente de la limitación) y **sí genera puntos** (a diferencia de la batería). Pre-carga los factores más comunes para acortar la afinación:

- Q073 "¿Sabes comer e hidratarte en ciclismo?" → estrategia nutricional (D002) y, si no le presta atención, abre rutas nutrición/carbohidratos.
- Q074 "¿Sigues un plan de entrenamiento?" → estructura (F005); "no, hago lo que puedo" abre `intensidad`.

Estos puntos no disparan hipótesis por sí solos (H001 exige D001 media; H012 exige F005 alta), pero suman al score y a la confianza, de modo que la evaluación converge con menos preguntas de afinación. Se registran en el código de evaluación y el replay los reproduce. Flujo: contexto → modo → limitación/objetivo → **perfil** → batería → afinación → informe.

## D21. Perfil de recuperación + limitación de estancamiento

- **Perfil (Q075):** recuperación y sueño → F003, junto a nutrición (Q073) y plan (Q074). El estrés NO va en perfil; se investiga como afinación dentro del estancamiento.
- **LP009 "Entreno pero siento que no mejoro"** (tipo `estancamiento`) + O008 "Volver a progresar". Su batería (Q076-Q079) separa las causas típicas de una meseta: entrenamiento monótono/sin progresión → F005; muy intenso sin días suaves + mal descanso → F003 (sobrecarga); molestia localizada → técnica; y cuánto tiempo lleva constante.
- **Afinación nueva:** Q081 estrés → F003; Q082 mismo estímulo por años → F005; Q083 molestia con el gesto → F007.
- **Hipótesis:** H008 ampliada a "recuperación insuficiente / sobrecarga" (incluye exceso de intensidad sin recuperar); H015 "molestia/sobrecarga localizada" → revisar posición/bike fit y valorar fisioterapia (derivación, no diagnóstico). El estancamiento por falta de estructura ya lo cubren H009/H012.
