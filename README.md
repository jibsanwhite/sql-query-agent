# Agente SQL

Responde preguntas en lenguaje natural sobre una base de datos SQLite, generando y ejecutando SQL.

Escribes una pregunta como si hablaras con una persona y el agente escribe el SQL, lo ejecuta y te devuelve la respuesta.

```text
Pregunta → LLM (genera SQL) → SQLite → LLM (redacta la respuesta) → Respuesta
```

## De dónde viene

Adaptación del agente `04-sql-query-agent` del repositorio [500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects) (ashishpatel26, MIT).

El cambio principal es `build_llm()` en `agent.py`: el agente original solo funcionaba con la clave de pago de OpenAI. Esta versión también funciona con **Gemini gratis**, sin tarjeta, y se cambia de un proveedor a otro con una sola línea en el `.env`. El resto del código no cambia.

## Requisitos

- Python 3.10 o superior
- Una clave de API: de Gemini (gratis) o de OpenAI (de pago)

## Instalación

```bash
pip install -r requirements.txt
cp .env.example .env
```

Después edita el `.env` con UNA de las dos opciones:

```bash
# Opción 1 (recomendada, gratis): Gemini
LLM_PROVIDER=gemini
GEMINI_API_KEY=tu_clave_de_gemini_aqui
```

La clave de Gemini se consigue en [Google AI Studio](https://aistudio.google.com): **Get API key → Create API key**. Es gratis y no pide tarjeta.

```bash
# Opción 2 (original del repo, de pago): OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=tu_clave_de_openai
```

## Uso

```bash
# Modo demo: crea una base de ejemplo (tienda en línea) y pregunta sobre ella
python agent.py

# Tu propia base de datos
python agent.py --db ruta/a/tu/base.sqlite

# Una sola pregunta, sin entrar al modo interactivo
python agent.py --db mi_base.sqlite --question "¿Cuántos clientes tenemos por país?"
```

La base se abre **en solo lectura** por defecto: el agente puede consultar, pero no modificar nada. Usa `--allow-write` solo con una base desechable si quieres permitir cambios de verdad.

## Preguntas de ejemplo

- "¿Cuántos clientes tenemos en cada país?"
- "¿Cuáles son los 3 productos más vendidos?"
- "¿Cuál fue el ingreso total del mes pasado?"
- "¿Qué cliente ha gastado más?"

## Archivos

| Archivo | Qué es |
| --- | --- |
| `agent.py` | El agente completo (base de ejemplo, conexión, `build_llm()`) |
| `README.md` | Este archivo |
| `NOTAS.md` | Notas en español: cómo funciona, qué se cambió y qué falta |
| `.env.example` | Plantilla del `.env` con las dos opciones de clave |
| `requirements.txt` | Dependencias de Python |
| `metadata.yaml` | Datos del proyecto original |

## Seguridad

- Nunca subas el archivo `.env`: ahí va tu clave.
- Nunca subas una base de datos real: puede tener productos, ventas, clientes y deudas de verdad.
- El agente abre la base en solo lectura, pero revísalo siempre antes de correrlo contra datos importantes.
