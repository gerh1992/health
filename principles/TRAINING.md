# Principios de Entrenamiento

_Capa `principles/` · Estable · Revisar solo con evidencia o cambio de dirección_

Este documento define **qué se optimiza, qué importa y qué no** en el entrenamiento (gimnasio, deporte y cualidades motoras). No es un plan semanal: es la base sobre la que se construyen los planes y se interpretan los datos.

---

## 1. Qué se optimiza (jerarquía)

La meta es **performance atlética**, en este orden de prioridad:

1. **Velocidad** — desplazamiento y ejecución a máxima demanda
2. **Agilidad** — cambio de dirección y reacción
3. **Aceleración** — de 0 a máxima velocidad en el menor tiempo
4. **Fuerza** — base neuromotora que sostiene las tres de arriba

Regla de jerarquía: **la fuerza es el cimiento, no el fin.** Se entrena para levantar fuerte porque eso empuja velocidad/agilidad/aceleración. Si un día de fuerza compite con un estímulo de velocidad fresca, gana la cualidad de arriba en la jerarquía.

## 2. Qué NO se optimiza

- **Estética** — explícitamente no-prioridad. No se diseñan sesiones ni se eligen cargas por hipertrofia u apariencia. Cualquier ganancia estética es subproducto, no objetivo.
- **Agotamiento acumulado** — cansarse no es entrenar. Una sesión "dura" que deja la semana siguiente fundida es una sesión mal diseñada.
- **Cardio "por hacer cardio"** — el volumen aeróbico se decide según lo que sirve a la recuperación/velocidad, no como meta autónoma.

## 3. Calidad > Volumen de sesión

El estímulo que produce adaptación es **intensidad útil + intención**, no duración prolongada.
- Cada serie importante que se hace a media intención es una repetición desperdiciada que solo suma fatiga.
- Si no podés darle intención máximal a un bloque de velocidad/fuerza, ese día no es el día — porque la fatiga sin estímulo es ruido, no señal.

## 4. Carga progresiva con señal de salida (medible)

La mejora no es "fui al gimnasio". La mejora es **un KPI que sube**: más kg, salto más alto, sprint más rápido.
- Cada estímulo debe repetirse o escalarse; lo que no se mide no se puede decir que mejoró.
- Fuente de verdad para adaptación = `performance/data/fitness_metrics.csv` (Is_KPI). `sessions.csv` es el contexto, no la señal de progreso.

## 5. Fatiga como recurso, no como meta

El entrenamiento es un **estímulo de estrés** que genera fatiga; la adaptación viene de supercompensar.
- La fatiga es el costo que se paga por el estímulo — hay que pagarlo, pero **nunca gastarlo sin obtener estímulo**.
- La lectura longitudinal (HRV/RHR/sueño/energía subj.) es el medidor de fatiga del sistema. Ética: si la señal de recuperación cae sostenidamente, el plan está mal calibrado, no "falta fuerza de voluntad".

## 6. Consistencia semanal > sesión heroica

Gana el que respeta la semana, no el que un día logró un PR y quedó 3 días fundido.
- El plan semanal define el estímulo; la sesión individual es una pieza.
- Una sesión ejecutada a mediana calidad pero dentro del plan vale más que una sesión aislada gigante que rompe la semana.

## 7. El deporte (pádel) es parte de la carga, no un extra

Todo lo que cuesta recuperación en la semana — pádel, fútbol, social pesado, trabajo estresante, mal sueño — **cuenta como carga real** del sistema.
- El plan de entrenamiento se calibra contra la carga TOTAL de la semana, no solo contra las sesiones de gimnasio.
- Pádel técnico/competitivo entra en la ecuación de fatiga; no se programa un pico de fuerza dentro de una semana con torneo.

## 8. Velocidad/agilidad/aceleración son habilidades, no solo capacidades

Se mejoran entrenando **intención y técnica a estado fresco**, no añadiendo volumen.
- Exigen: estado de recuperación decente, esfuerzos máximos cortos, descanso completo entre repeticiones.
- La mayoría de las ganancias vienen de ejecutar bien y pocas veces, no de acumular series.

## 9. Hipótesis testeable > dogma

Los cambios de protocolo se tratan como **experimentos**: variable, expectativa, ventana, y qué decisión cambia si funciona.
- Si no se puede definir "qué aprendo de esto", no se cambia nada todavía.
- El auto-testing es preferido sobre sobre-ajustar ruido de logs diarios: se mide la señal, no cada fluctuación.

---

## Cómo se usa este documento

- Todo plan semanal, sesión y análisis de datos debe poder trazar su razón hasta uno de estos principios.
- Si un dato longitudinal contradice un principio, no se edita el principio a la ligera: se revisa el sistema (calibración, plan) primero.
- Si los principios cambian, se refleja en git con el motivo explícito.