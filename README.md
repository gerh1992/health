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
- `performance/` → capa operativa multi-CSV de sueño, entrenamiento, recovery, métricas y suplementos

Y deja preparado:
- `medical/` → evidencia clínica / estudios / lesiones / medicación / reports

## Estructura actual
```text
health/
  README.md
  .gitignore
  context/
    README.md
    health-brief.md
    profile.yaml
    current-state.md
    decision-rules.md
    data-sources.yaml
  performance/
    README.md
    data/
      biometrics.csv
      sessions.csv
      fitness_metrics.csv
      match_details.csv
      supplements.csv
    schema/
      SCHEMA.json
    rules/
      SYSTEM_RULES.md
    ops/
      validate_log.py
      backup_performance_data.sh
      backup_performance_log.sh   # alias legacy del comando; delega al backup multi-CSV
    backups/           # ignorado por git
  medical/
    README.md
```

## Orden de lectura recomendado para una IA o persona nueva
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
