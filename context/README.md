# Context layer

Este directorio existe para resolver un problema concreto:
una IA o una persona nueva debería poder entrar al repo con **cero contexto previo** y entender rápido qué información es estable, qué información cambia día a día, qué archivos son fuente de verdad y cómo tomar decisiones sin inventar.

## Qué leer primero

Si llegás sin contexto, el orden recomendado es:

1. `context/profile.yaml`
2. `context/current-state.md`
3. `context/decision-rules.md`
4. `context/data-sources.yaml`
5. `performance/README.md`
6. `performance/data/performance_log.csv`
7. `medical/README.md`

## Principio de diseño

Separar capas. No mezclar todo en un solo archivo.

- **Profile** → datos relativamente estables del usuario que cambian lento.
- **Current state** → objetivos, prioridades, protocolos y contexto activo.
- **Decision rules** → cómo interpretar y cómo no interpretar los datos.
- **Data sources** → mapa de fuentes de verdad del repo.
- **Performance** → log operativo diario.
- **Medical** → evidencia clínica, estudios, diagnósticos, medicación y notas de salud cuando existan.

## Regla crítica

No usar el CSV diario para guardar contexto estable.

Ejemplos de contexto estable:
- edad,
- sexo,
- altura,
- peso de referencia,
- objetivo principal,
- preferencias de interpretación,
- reglas del sistema.

Eso va acá, no en el log diario.

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
