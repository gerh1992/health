# Performance subsystem

Este subsistema guarda la fuente de verdad operativa de performance y recovery.

Incluye:
- sueño,
- HRV/RHR,
- calidad subjetiva y energía,
- sesiones de entrenamiento / recovery / trabajo / social,
- métricas de rendimiento,
- detalles de partidos,
- suplementos,
- reglas, esquema y tooling del subsistema.

## Archivos clave
- Datos canónicos:
  - `data/biometrics.csv`
  - `data/sessions.csv`
- `data/fitness_metrics.csv`
- `data/match_details.csv`
- `data/padel_match_reviews.csv`
- `data/supplements.csv`
- Schema: `schema/SCHEMA.json`
- Reglas operativas: `rules/SYSTEM_RULES.md`
- Reglas de reviews tácticos de pádel: `rules/PADEL_REVIEW_RULES.md`
- Script de validación: `ops/validate_log.py`
- Script de backup canónico: `ops/backup_performance_data.sh`
- Alias legacy del comando de backup: `ops/backup_performance_log.sh` (redirige al backup multi-CSV)
- Backups locales ignorados por git: `backups/`

## Modelo actual
La arquitectura actual es multi-CSV.
Cada archivo representa una entidad distinta para evitar mezclar métricas heterogéneas en una sola fila:

- `biometrics.csv` → recovery diario y sueño
- `sessions.csv` → eventos/sesiones principales del día
- `fitness_metrics.csv` → lifts, tests y métricas de performance ligadas a una sesión
- `match_details.csv` → detalle competitivo por partido individual, incluso cuando varias filas pertenecen a una misma sesión/día
- `padel_match_reviews.csv` → review táctico/reflexivo por partido para detectar patrones y definir experimentos futuros
- `supplements.csv` → adherencia diaria a suplementos

## Criterio de logging
- registrar recovery/sueño en `biometrics.csv` cuando haya datos reportados,
- registrar cada evento principal en `sessions.csv`,
- registrar sólo métricas de performance que cambian decisiones en `fitness_metrics.csv`,
- registrar detalle de partidos sólo cuando aporta contexto competitivo útil,
- cuando hay varios partidos en una misma sesión/día, registrar una fila por partido en `match_details.csv` ligada al mismo `Session_Id`,
- registrar reviews tácticos de pádel en `padel_match_reviews.csv` cuando aportan aprendizaje, frustración útil o hipótesis para el próximo partido,
- registrar suplementos en `supplements.csv` sin inventar tomas no reportadas.

## Convención de placeholders
- `-` significa dato desconocido, no reportado o no disponible.
- No significa cero.
- No debe reinterpretarse automáticamente como resultado negativo.
- Si una distinción futura requiere más precisión, debe modelarse en schema/documentación, no inferirse en silencio.

## Regla operativa
Antes de modificar el subsistema:
1. `git pull --rebase`
2. editar
3. validar (`python3 performance/ops/validate_log.py`)
4. si corresponde, generar backup (`performance/ops/backup_performance_data.sh`)
5. `git add -A`
6. commit con contexto
7. push
