# Plan Semanal Tipo (Template)

_Capa `performance/plans/` · Ejemplo de semana aplicando `principles/TRAINING.md` + `rules/READINESS_RULES.md`._

Este es un **template de semana base**, no un plan fijo. Cada semana se arma sobre esta estructura y se ajusta con el gate de readiness (verde/amarillo/rojo) y la carga real (partidos, clases, trabajo, sueño).

---

## Contexto fijo del usuario

- **Objetivo (jerarquía):** velocidad > agilidad > aceleración > fuerza.
- **Carga fija semanal:** clase de pádel **martes 8AM** (técnica) + partidos de pádel según agenda.
- **Trabajo:** remoto (programador) — el estrés laboral cuenta como carga.
- **Recuperación:** sueño/HRV primero; el sistema lee HRV/RHR vs baseline, no valores absolutos.

---

## Estructura base de la semana

| Día | Bloque | Cualidad / Foco | Nota de carga |
|---|---|---|---|
| **Lunes** | Velocidad/Agilidad | Sprints cortos + cambios de dirección | Estado fresco, primera del bloque. Intención máxima, pocas series. |
| **Martes** | Clase de pádel 8AM | Técnica (drive/revés) | Carga moderada. No programar fuerza pesada el mismo día. |
| **Miércoles** | Fuerza | Base neuromotora (sentadilla, empuje, jalón) | RPE 7-8. No pico si hay partido el jueves. |
| **Jueves** | Velocidad/Agilidad O Recovery | Según carga acumulada | Si martes+miércoles dejaron fatiga → recovery/movilidad. |
| **Viernes** | Fuerza | Complemento (tirón, core, unilateral) | RPE 7. |
| **Sábado** | Partido de pádel (si hay) | Competitivo | Cuenta como carga alta. |
| **Domingo** | Recovery | Movilidad, estiramiento, caminata | Activo, no sedentario. |

**Frecuencia mínima por cualidad priorizada:** velocidad/agilidad ×2, fuerza ×2. Si una semana no llega, se baja intensidad — no se elimina la sesión (regla 2).

---

## Aplicación del gate de readiness (regla 3)

Cada día, antes de ejecutar el bloque, se lee la franja del día:

| Franja | Acción sobre el bloque del día |
|---|---|
| 🟢 **Verde** | Ejecutar tal cual. |
| 🟡 **Amarilla** | Bajar volumen ~30% O intensidad (RPE −2). La cualidad priorizada se mantiene pero más corta. |
| 🔴 **Roja** | Reemplazar por recovery / saltar la cualidad priorizada. No entrenar fundido. |

**Regla de oro:** si el día es amarillo/rojo, se ajusta el bloque de HOY, no se "compensa" mañana. La semana se recalibra, no se recupera con una sesión heroica (regla 6).

---

## Ejemplo concreto (semana con clase martes + partido sábado)

**Lunes (verde):** Velocidad — 6×20m sprints con descanso completo + 4×3 cambios de dirección. RPE 8. Fresco.
**Martes (amarilla):** Clase de pádel 8AM normal (técnica, no es esfuerzo máximo). Sin fuerza el mismo día. RPE 6.
**Miércoles (verde):** Fuerza — sentadilla 4×5, press 4×6, jalón 4×8. RPE 7. (No pico: hay partido sábado.)
**Jueves (amarilla):** Recovery — movilidad + caminata 30min. Se salta velocidad (fatiga de martes+miércoles).
**Viernes (verde):** Fuerza — tirón 4×6, core 3×10, unilateral 3×8. RPE 7.
**Sábado (verde):** Partido de pádel. Carga alta, se respeta.
**Domingo (verde):** Recovery activo — estiramiento + caminata.

**Si el sábado fuera rojo:** el partido se juega igual (es compromiso social/competitivo) pero se baja la intensidad de la semana previa (miércoles/viernes más suaves) y el domingo es recovery completo.

---

## Regla de recalibración por torneo (regla 4)

- Semana con **torneo de pádel** → no programar pico de fuerza. Fuerza se baja a RPE 6-7, mantenimiento.
- Semana con **clase + 2 partidos** → velocidad/agilidad se reduce a 1 sesión, priorizando frescura para el pádel.
- **Mal sueño sostenido** (amarilla/roja varios días) → el plan se recalibra hacia recovery, no se fuerza.

---

## Cómo se usa

1. Cada domingo se arma la semana siguiente sobre esta base (fechas + carga real conocida).
2. Cada día se lee la franja de readiness y se ajusta el bloque.
3. Solo se declara mejora lo que subió en `fitness_metrics.csv` (KPI), no "fui al gym" (regla 5).
