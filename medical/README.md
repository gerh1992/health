# Medical subsystem

Este directorio está reservado para información clínica o de salud más amplia que no pertenece al log operativo diario.

## Qué debería vivir acá
- estudios de laboratorio,
- diagnósticos,
- lesiones,
- medicación,
- suplementos crónicos si pasan a ser clínicamente relevantes,
- informes médicos,
- imágenes o reportes,
- antecedentes personales/familiares relevantes,
- contraindicaciones o flags para toma de decisiones.

## Qué no debería vivir acá
- logs diarios de sueño o entrenamiento,
- contexto estable básico ya modelado en `context/profile.yaml`,
- interpretaciones sueltas sin fuente,
- archivos duplicados del CSV operativo.

## Estructura sugerida cuando empiece a poblarse
```text
medical/
  README.md
  conditions/
  injuries/
  medications/
  labs/
  imaging/
  reports/
```

## Regla de calidad
Cada documento médico debería responder, idealmente, estas preguntas:
- qué es,
- fecha,
- fuente,
- por qué importa,
- qué decisiones puede cambiar.

## Estado actual
Scaffold vacío. Todavía no hay evidencia médica formal cargada en este repo.
