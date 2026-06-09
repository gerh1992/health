# health

Repo privado para el sistema de datos de salud / rendimiento.

Objetivos:
- que los archivos del sistema sean inspeccionables,
- que toda modificación tenga trazabilidad,
- que el historial quede auditado con git,
- que el sistema pueda crecer por subsistemas sin volverse una caja negra.

## Estado actual
Por ahora el repo contiene el subsistema de performance:
- sueño,
- entrenamiento,
- suplementos,
- reglas operativas del log.

Más adelante se pueden agregar otros subsistemas de salud dentro de este mismo repo.

## Estructura actual
```text
health/
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
```

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

## Nota sobre contexto general de salud
Todavía no se definió el diseño final para contexto biométrico/antecedentes/estudios.
Cuando se defina, conviene agregarlo de manera explícita y con estructura, no mezclarlo arbitrariamente con el CSV operativo.
