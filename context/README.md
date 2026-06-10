# Context layer

Este directorio existe para resolver un problema concreto:
una IA o una persona nueva debería poder entrar al repo con **cero contexto previo** y entender rápido qué información es estable, qué información cambia día a día, qué archivos son fuente de verdad y cómo tomar decisiones sin inventar.

## Qué leer primero

Si llegás sin contexto, el orden recomendado es:

1. `context/health-brief.md`
2. `context/profile.yaml`
3. `context/current-state.md`
4. `context/decision-rules.md`
5. `context/data-sources.yaml`
6. `performance/README.md`
7. `performance/rules/SYSTEM_RULES.md`
8. `performance/data/biometrics.csv`
9. `performance/data/sessions.csv`
10. `performance/data/fitness_metrics.csv`
11. `performance/data/match_details.csv`
12. `performance/data/supplements.csv`
13. `medical/README.md`

## Principio de diseño

Separar capas. No mezclar todo en un solo archivo.

- **Health brief** → resumen ejecutivo para onboarding rápido.
- **Profile** → datos relativamente estables del usuario que cambian lento.
- **Current state** → objetivos, prioridades, protocolos y contexto activo.
- **Decision rules** → cómo interpretar y cómo no interpretar los datos.
- **Data sources** → mapa de fuentes de verdad del repo.
- **Performance** → capa operativa diaria multi-CSV.
- **Medical** → evidencia clínica, estudios, diagnósticos, medicación y notas de salud cuando existan.

## Regla crítica

No usar los CSV diarios para guardar contexto estable.

Ejemplos de contexto estable:
- edad,
- sexo,
- altura,
- peso de referencia,
- objetivo principal,
- preferencias de interpretación,
- reglas del sistema.

Eso va acá, no en la capa operativa diaria.

## Regla de ausencia de datos

Si algo no está documentado en el repo, tratarlo como:
- **desconocido**, no como falso,
- y nunca inventarlo.

Ejemplo:
- si no hay estudios de laboratorio cargados, eso significa **no documentados acá**, no “no existen”.

## Objetivo final

El repo tiene que servir para que una IA o una persona puedan:
- reconstruir el contexto importante,
- saber qué datos son confiables,
- entender qué decisiones son consistentes con el sistema,
- y detectar rápido qué falta documentar.
