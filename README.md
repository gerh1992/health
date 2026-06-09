# health

Repo privado para el sistema de datos de salud / rendimiento.

Objetivos:
- que los archivos del sistema sean inspeccionables,
- que toda modificación tenga trazabilidad,
- que el historial quede auditado con git,
- que el sistema pueda crecer por subsistemas sin volverse una caja negra.

## Objetivo funcional del repo
Que una IA o una persona nueva, con **cero contexto previo**, pueda entrar al repo y entender:
- qué es estable,
- qué cambia día a día,
- cuáles son las fuentes de verdad,
- qué reglas de interpretación existen,
- y qué información importante todavía falta documentar.

## Estado actual
Hoy el repo tiene dos capas principales:
- `context/` → contexto estable + reglas de lectura + mapa de fuentes
- `performance/` → log operativo de sueño, entrenamiento, recovery y suplementos

Y deja preparado:
- `medical/` → evidencia clínica / estudios / lesiones / medicación / reports

## Estructura actual
```text
health/
  README.md
  .gitignore
  context/
    README.md
    profile.yaml
    current-state.md
    decision-rules.md
    data-sources.yaml
  performance/
    README.md
    data/
      performance_log.csv
    schema/
      SCHEMA.json
    rules/
      SYSTEM_RULES.md
    ops/
      backup_performance_log.sh
    backups/           # ignorado por git
  medical/
    README.md
```

## Orden de lectura recomendado para una IA o persona nueva
1. `context/profile.yaml`
2. `context/current-state.md`
3. `context/decision-rules.md`
4. `context/data-sources.yaml`
5. `performance/README.md`
6. `performance/rules/SYSTEM_RULES.md`
7. `performance/data/performance_log.csv`
8. `medical/README.md`

## Workflow acordado
1. `git pull --rebase`
2. editar
3. verificar
4. `git add -A`
5. `git commit` con contexto
6. `git push`

## Convención de commits sugerida
- `data: ...`
- `rules: ...`
- `schema: ...`
- `ops: ...`
- `docs: ...`

No hace falta una convención rígida, pero sí contexto suficiente para entender qué cambió y por qué.

## Autores
- Cambios automáticos hechos por Hermes: `Hermes Agent <hermes@local>`
- Cambios manuales del usuario: tu identidad/config de git

## Principio de modelado
No mezclar en un mismo archivo:
- hechos estables,
- eventos diarios,
- evidencia médica,
- reglas del sistema,
- e interpretaciones.

Separar esas capas hace que el sistema sea legible, mantenible y reusable por otras IAs.
