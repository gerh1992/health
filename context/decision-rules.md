# Decision rules

Estas reglas existen para que una IA o una persona nueva no saque conclusiones malas por falta de contexto.

## 1. No inventar datos
Si un dato no está en el repo, tratarlo como desconocido.
No completar huecos con suposiciones silenciosas.

## 2. Separar hechos de interpretación
- Hechos estables → `context/profile.yaml`
- Estado/objetivos/prioridades → `context/current-state.md`
- Log operativo diario → `performance/data/biometrics.csv`, `performance/data/sessions.csv`, `performance/data/fitness_metrics.csv`, `performance/data/match_details.csv`, `performance/data/supplements.csv`
- Regla/sistema → `performance/rules/`
- Evidencia médica → `medical/`

## 3. No usar una métrica aislada para una conclusión fuerte
No concluir “está recuperado” o “está fundido” por un solo HRV o un solo RHR.
Siempre cruzar con:
- sueño,
- baseline reciente,
- carga acumulada,
- percepción subjetiva,
- entrenamiento reciente.

## 4. Baseline primero, valor absoluto después
Para sleep/recovery, priorizar el desvío vs. baseline personal reciente.
Los valores absolutos importan menos que:
- dirección,
- magnitud del cambio,
- persistencia del desvío.

## 5. Performance > completitud obsesiva
Guardar lo que cambia decisiones.
No convertir el sistema en una bitácora exhaustiva de todo lo que pasó si eso no mejora decisiones.

## 6. No mezclar contexto estable con eventos diarios
Edad, sexo, altura, metas, sesgos interpretativos, protocolos y antecedentes no pertenecen a los CSV diarios.

## 7. No confundir ausencia de entrenamiento con ausencia de carga
Pádel, mal sueño, estrés, enfermedad, alcohol, caminatas, molestias y fatiga acumulada también afectan la carga real del sistema.

## 8. Diferenciar dato reportado vs inferido
Cuando algo sea inferido o reconstruido, marcarlo explícitamente en comentarios o documentación.
Nunca presentarlo como hecho reportado si no lo fue.

## 9. En conflicto entre documentación y memoria implícita, gana el repo
Si una IA recuerda algo pero no está documentado o contradice el repo, el repo manda hasta que se corrija explícitamente.

## 10. Toda modificación importante debe dejar rastro
Antes de modificar:
- `git pull --rebase`

Después de modificar:
- verificar
- commit con contexto
- push

## 11. Prioridad de lectura para tomar decisiones
1. `context/profile.yaml`
2. `context/current-state.md`
3. `context/decision-rules.md`
4. `performance/rules/SYSTEM_RULES.md`
5. `performance/data/biometrics.csv`
6. `performance/data/sessions.csv`
7. `performance/data/fitness_metrics.csv`
8. `performance/data/match_details.csv`
9. `performance/data/supplements.csv`
10. `medical/` si existe información relevante
