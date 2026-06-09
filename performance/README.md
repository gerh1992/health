# Performance subsystem

Este subsistema guarda la fuente de verdad de:
- sueño,
- entrenamiento,
- suplementos,
- reglas y esquema del log.

## Archivos clave
- CSV canónico: `data/performance_log.csv`
- Schema: `schema/SCHEMA.json`
- Reglas operativas: `rules/SYSTEM_RULES.md`
- Script de backup: `ops/backup_performance_log.sh`
- Backups locales ignorados por git: `backups/`

## Criterio de logging
- una fila `biometrics` por día cuando hay métricas de sueño/recovery,
- una fila `session` por evento significativo,
- filas `kpi` solo para lifts/tests que cambian decisiones,
- filas `accessory` solo cuando preservarlas realmente agrega valor.

## Compatibilidad
Existen symlinks de compatibilidad desde la ruta histórica `~/.hermes/data/performance/` hacia esta nueva estructura para no romper workflows viejos durante la transición.
