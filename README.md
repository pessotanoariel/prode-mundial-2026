# Prode Mundial 2026

Motor de simulación y predicción para la Copa Mundial de la FIFA 2026 desarrollado en Python.

El proyecto comenzó como una herramienta para participar en un prode entre compañeros de trabajo y evolucionó hacia un experimento de analítica deportiva e ingeniería de datos, incorporando simulación completa del torneo, clasificación de mejores terceros, implementación del Anexo C de FIFA y automatización de todas las rondas eliminatorias.

---

## Objetivos del proyecto

* Consumir y procesar datos internacionales de fútbol basados en Elo Ratings.
* Generar predicciones de partidos utilizando métricas de fuerza relativa y forma reciente.
* Simular la fase de grupos completa.
* Determinar clasificados a eliminación directa según el formato oficial de FIFA 2026.
* Construir automáticamente el cuadro eliminatorio utilizando las reglas oficiales del Anexo C.
* Simular todas las rondas hasta la final y el partido por el tercer puesto.
* Servir como proyecto práctico para profundizar conocimientos de Python, modelado de datos, testing y arquitectura de pipelines.

---

## Características principales

### Ingesta y procesamiento

* Ingesta automatizada de datasets externos.
* Conversión y normalización de archivos TSV.
* Construcción de datasets procesados para análisis y simulación.
* Cálculo de fuerza de selección mediante Elo Ratings.
* Cálculo de forma reciente utilizando resultados históricos.

### Predicción de partidos

* Probabilidad de victoria basada en Elo.
* Ajuste mediante forma reciente.
* Probabilidad dinámica de empate.
* Predicción de marcador.
* Clasificación de confianza.
* Clasificación de riesgo de sorpresa (upset risk).

### Simulación del Mundial 2026

* Simulación completa de fase de grupos.
* Tabla de posiciones por grupo.
* Clasificación de primeros y segundos.
* Selección de los 8 mejores terceros.
* Desempate por enfrentamiento directo entre dos equipos.
* Implementación del formato oficial de 48 selecciones.

### Eliminación directa

* Implementación del Anexo C de FIFA.
* Generación automática de dieciseisavos de final (Round of 32).
* Simulación de octavos, cuartos, semifinales, tercer puesto y final.
* Resolución de empates mediante tiempo suplementario o penales.
* Orquestador único para ejecutar toda la simulación.

### Calidad y mantenibilidad

* Arquitectura modular.
* Logging centralizado.
* Validaciones y manejo de errores.
* Tests automatizados con pytest.
* Documentación técnica del pipeline.

---

## Estructura del proyecto

```text
prode-mundial-2026/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── output/
│
├── docs/
│   ├── annex_c.md
│   └── knockout_pipeline.md
│
├── src/
│   ├── analysis/
│   ├── ingestion/
│   ├── knockout/
│   ├── predictor/
│   └── processing/
│
├── tests/
│
├── README.md
├── README_EN.md
└── requirements.txt
```

---

## Flujo de simulación

```text
Datasets externos
        ↓
Ingesta
        ↓
Procesamiento
        ↓
Fuerza de equipos y forma reciente
        ↓
Predicciones de fase de grupos
        ↓
Clasificación
        ↓
Mejores terceros
        ↓
Anexo C FIFA
        ↓
Round of 32
        ↓
Round of 16
        ↓
Quarterfinals
        ↓
Semifinals
        ↓
Third Place Match
        ↓
Final
```

---

## Ejecución

### Crear entorno virtual

```bash
python -m venv .venv
```

### Activar entorno

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / Mac

```bash
source .venv/bin/activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar simulación completa

```bash
python -m src.knockout.tournament
```

---

## Testing

Ejecutar todos los tests:

```bash
pytest
```

Actualmente se incluyen pruebas para:

* Resolución de ganadores en eliminación directa.
* Construcción de rondas posteriores.
* Implementación del Anexo C de FIFA.

---

## Documentación adicional

* `docs/knockout_pipeline.md`
* `docs/annex_c.md`

---

## Roadmap

### Mejoras futuras

### Próximas mejoras

* Desempates entre tres o más equipos.
* Fair Play como criterio de desempate.
* Ranking FIFA como criterio de desempate.
* Integración de Elo dinámico en fase de grupos.
* Actualización automática diaria de datasets.
* Visualización avanzada del cuadro eliminatorio.
* Frontend Next.js.

---

## Descargo

Las predicciones generadas por el proyecto tienen fines educativos, experimentales y recreativos. No constituyen recomendaciones de apuestas ni garantías sobre resultados reales.
