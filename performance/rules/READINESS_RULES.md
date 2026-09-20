# Readiness System Rules (Gate de Ejecución)

_Capa `performance/rules/` · Sistema de readiness para decidir, cada día, si el plan semanal se ejecuta tal cual o se escala._

Complementa a `principles/TRAINING.md` (qué se optimiza) y a `SYSTEM_RULES.md` (estructura de datos). Este documento define **cómo se ejecuta el plan en función del estado de recuperación**.

---

## 1. El ciclo (modelo mental)

**Estímulo (carga) → Fatiga → Recuperación → Supercompensación.**

El sistema se diseña sobre DOS grupos de inputs, separados porque se usan en momentos distintos:

**A. Inputs de DISEÑO** — palancas que se programan la semana:
- **Cualidad objetivo** (jerarquía: velocidad > agilidad > aceleración > fuerza)
- **Frecuencia** (sesiones clave por semana)
- **Intensidad** (RPE / % de esfuerzo útil)
- **Volumen** (series/reps — pesa menos que la calidad)
- **Carga total real** (pádel, fútbol, trabajo estresante, mal sueño)

**B. Inputs de EJECUCIÓN** — señales que cada día deciden si el plan corre tal cual o se escala:
- **Recuperación objetiva:** HRV y RHR vs baseline personal (desvío + dirección + persistencia, NUNCA valor absoluto)
- **Sueño** (horas + calidad)
- **Energía subjetiva**
- Siempre **cruzadas** — ninguna señal sola manda.

Regla maestra: **A genera el plan; B es un gate.** El plan se diseña para ejecutarse a estado fresco; si la señal dice "no estás fresco", el estímulo se baja ANTES de ejecutarlo, no se sufre.

---

## 2. Bandas de readiness (3 bandas)

El gate tiene tres franjas. **La señal PEOR manda** (regla conservadora): si una señal dice rojo aunque las demás digan verde, manda el rojo.

| Franja | Señal (la peor manda) | Acción sobre el plan |
|---|---|---|
| 🟢 **Verde** | HRV/RHR ≈ baseline, sueño ≥7h, energía ok | Plan tal cual |
| 🟡 **Amarilla** | HRV ↓ 5–10% o sueño 6–7h o energía 4–5 | Bajar volumen ~30% O intensidad (RPE −2) |
| 🔴 **Roja** | HRV ↓ ≥10% (baseline prom 7d) por ≥3 días seguidos Y sueño <7h | Reemplazar sesión por recovery / saltar cualidad priorizada |

**Umbrales confirmados (2026-09-20):**
- Franja roja = **HRV ↓ ≥10% vs baseline (promedio 7d) durante ≥3 días consecutivos, cruzado con sueño <7h.**
- Si las señales discrepan, **manda la peor.**

---

## 3. Reglas simples del sistema (IF/THEN)

1. **Cualidad de arriba primero.** Velocidad/agilidad siempre a estado fresco, antes del bloque de fuerza fatigante. Si compiten, gana la cualidad superior.
2. **Frecuencia sostenida > sesión heroica.** Cada cualidad priorizada tiene frecuencia mínima semanal; si no se llega, se baja intensidad — no se elimina la sesión.
3. **Gate de readiness.** Verde → plan tal cual. Amarilla → baja volumen o intensidad. Roja → sesión reemplazada por recovery o se salta la cualidad priorizada.
4. **Carga total, no solo gimnasio.** Deporte (pádel/fútbol), trabajo estresante y mal sueño cuentan como carga real. Semana con torneo → recalibrar fuerza. Nunca pico de fuerza en semana con torneo.
5. **Solo se repite/escala lo medible (KPI).** No "fui al gym": sube kg/salto/sprint en `fitness_metrics.csv`. Lo que no se mide no mejoró.
6. **Día sin intención = no-día.** Si no se va a dar intención máxima a un bloque velocidad/fuerza, ese día no es el día (fatiga sin estímulo = ruido, no señal).

---

## 4. Operacionalización

- El gate se computa **automáticamente** desde `performance/data/biometrics.csv` con `performance/ops/regla_readiness.py`.
- El script respeta la convención de placeholders: `-` = desconocido, se ignora para el cálculo (no se cuenta como cero ni como buena señal).
- Baseline HRV = promedio móvil de los últimos 7 días con dato válido.
- Output: franja del día actual (o de una fecha dada) + qué señal la disparó.