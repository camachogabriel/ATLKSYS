# Puntos abiertos de lógica (detectados al estructurar la spec v1.0)

Para resolver en la fase de afinación, antes de implementar:

1. **Destinos de puntos sin código.** La spec asigna puntos a "disponibilidad energética", "durabilidad", "estrategia nutricional", "base aeróbica", "estrés térmico" — ninguno es capacidad (C###) ni factor (F###). Provisionalmente les asigné códigos D### (estados derivados) y E### (emergentes) en `knowledge/emergentes.yaml`. Decidir: ¿los puntos apuntan solo a C/F, o también a emergentes/derivados? ¿Cómo se agregan D/E hacia C/F al generar hipótesis?

2. **Puntos contextuales.** Q002 respuesta "60 g/h" dice "+1 o 0 según contexto". Falta definir el mecanismo de modulación por contexto (edad, duración del fondo, intensidad).

3. **Metadatos fuera de la lista oficial.** Los ejemplos usan `disponibilidad-energetica`, `durabilidad`, `estrategia-nutricional` como metadatos, pero no están en la lista principal de 22. Añadidos con nota en `metadatos.yaml`.

4. **Criterio de parada cuantitativo.** El motor define 4 condiciones de parada pero ninguna es operativa (¿cuántos puntos = "suficiente evidencia"? ¿qué profundidad máxima?).

5. **Áreas iniciales vs metadatos.** Las limitaciones (LP###) listan "áreas iniciales" que mezclan capacidades, factores y conceptos (ej. `intensidad-relativa`, `termorregulacion`, `cadencia`) que no existen como entidad. Unificar vocabulario.

6. **Generación de hipótesis.** No hay regla explícita de cómo el patrón de puntos se convierte en hipótesis priorizadas (¿umbral? ¿ranking simple? ¿plantillas de hipótesis por combinación?). La biblioteca de hipótesis (H###) aún no existe.

7. **Análisis por objetivo.** La traducción objetivo → limitaciones futuras / capacidades determinantes está mencionada pero sin reglas.

8. **Confianza solapada.** Tabla de confianza: 8-12 alta, >12 muy alta — el ejemplo del cap. 3 marca 12 como "Alta" y el cap. 9 muestra 13 como "Alta". Fijar límites exactos.
