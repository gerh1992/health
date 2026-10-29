# Backlog de Tareas del Sistema (TASKS.md)

Este archivo registra las tareas de **evolución, mejoras técnicas, scripts de análisis y cambios de arquitectura** del repositorio `health`.

> **Nota:** La ingesta diaria de métricas (sueño, entrenamientos, partidos) **no** requiere crear una tarea aquí; se reporta de forma directa por chat al agente.

---

## 📥 Backlog (Pendientes)

<!-- Agrega aquí nuevas iniciativas, scripts o refactorizaciones -->

- [ ] **[TASK-001] Script de análisis de correlación sueño-rendimiento**: Crear un script en `performance/ops/analyze_sleep_vs_performance.py` que cruce `biometrics.csv` y `match_details.csv` para evaluar impacto de horas de sueño (<7h) y HRV en el winrate de partidos.
- [ ] **[TASK-002] Monitoreo de carga aguda y crónica (ACWR)**: Diseñar un script o reporte que calcule la relación entre carga de trabajo semanal (RPE * Duración de `sessions.csv`) para prevenir sobreentrenamiento.

---

## 🔄 En Progreso

<!-- Mueve aquí las tareas en las que la IA o tú estén trabajando actualmente -->

---

## ✅ Completadas

<!-- Mueve aquí las tareas terminadas junto con su fecha -->

- [x] **[TASK-000] Setup de gobernanza IA (2026-10-29)**: Creación de `AGENTS.md` y `TASKS.md` para orquestar agentes y separar ingesta de datos de tareas de ingeniería.
