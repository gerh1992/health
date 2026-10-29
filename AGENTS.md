# Instrucciones para Agentes IA (health)

Este repositorio almacena y procesa el sistema de datos de salud, entrenamiento y rendimiento personal.

---

## 🧭 Mapa Rápido de Fuentes de Verdad

- **Principios rectores (el porqué):** `principles/TRAINING.md`
- **Contexto y perfil:** `context/profile.yaml`, `context/health-brief.md`, `context/decision-rules.md`
- **Reglas del sistema de rendimiento:** `performance/rules/SYSTEM_RULES.md`
- **Definición de esquemas de datos:** `performance/schema/SCHEMA.json`
- **Datos (Base de datos CSV):** `performance/data/*.csv`
- **Script de validación determinística:** `performance/ops/validate_log.py`
- **Backlog de evolución del sistema:** `TASKS.md`

---

## 🚦 Protocolo de Trabajo según el Pedido

El trabajo con el usuario se divide en dos carriles claramente diferenciados:

### Carril 1: Ingesta de Datos Diarios (Operativo)
*Se dispara cuando el usuario provee datos por chat (ej. "Dormí 7.2hs, HRV 55", "Jugué un partido de pádel...", "Entrené fuerza...").*
1. **No requiere crear una entrada en `TASKS.md`**; la ingesta diaria es directa y conversacional.
2. Lee y sigue las reglas de modelado y despiece multi-CSV en `performance/rules/SYSTEM_RULES.md`:
   - `biometrics.csv`: Sueño y recuperación diaria.
   - `sessions.csv`: Eventos principales del día.
   - `fitness_metrics.csv`: Cargas, saltos, métricas enlazadas a `Session_Id`.
   - `match_details.csv`: Partidos competitivos individuales.
   - `padel_match_reviews.csv`: Reseñas tácticas y reflexiones subjetivas.
   - `supplements.csv`: Adherencia a suplementos.
   - `players.csv`: Catálogo maestro de jugadores.
3. Respeta los tipos de datos y constraints de `performance/schema/SCHEMA.json`. Usa `-` para campos no reportados (nunca `0` ni `None`).
4. **Validación obligatoria:** Ejecuta siempre:
   ```bash
   python3 performance/ops/validate_log.py
   ```
   Si arroja errores, corrígelos de inmediato antes de dar por finalizada la respuesta.

---

### Carril 2: Evolución, Código y Mejoras del Sistema (Ingeniería)
*Se dispara cuando se van a crear scripts de análisis, refactorizar esquemas, migrar datos o automatizar reportes.*
1. **Seguimiento en `TASKS.md`:** Consulta la tarea correspondiente o créala antes de iniciar si es una mejora estructural o nueva funcionalidad.
2. Mueve la tarea a `🔄 En Progreso` mientras trabajas en ella y a `✅ Completadas` al terminar.
3. **Criterios y principios:**
   - Para métricas de rendimiento y salud, consulta `principles/TRAINING.md` y `context/decision-rules.md`.
   - Si una tarea modifica columnas o añade un nuevo CSV:
     - Actualiza `performance/schema/SCHEMA.json`.
     - Actualiza `performance/rules/SYSTEM_RULES.md`.
     - Actualiza las validaciones en `performance/ops/validate_log.py`.
4. Verifica que `python3 performance/ops/validate_log.py` pase con 0 errores.

---

## 📦 Git & Versionado

1. Antes de realizar cambios, asegúrate de estar sincronizado:
   ```bash
   git pull --rebase
   ```
2. Al terminar la tarea y validar que no hay errores:
   - Haz un commit con prefijo contextual (`data:`, `ops:`, `schema:`, `rules:`, `docs:`):
     ```bash
     git add -A
     git commit -m "tipo: descripción clara del cambio"
     git push
     ```
