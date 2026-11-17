# SQL Query Agent — notas de D.J.

Agente del repo `ashishpatel26/500-AI-Agents-Projects` (`agents/04-sql-query-agent`),
elegido por D.J. el 15/11/2026 como primer proyecto de práctica de programación.
Pregunta en lenguaje normal y el agente escribe el SQL, lo ejecuta y responde.

## Qué cambió respecto al original

- `agent.py`: se añadió `build_llm()`. El original solo sabía usar OpenAI (de pago).
  Ahora con `LLM_PROVIDER=gemini` usa Gemini gratis, que habla el mismo protocolo
  que OpenAI, así que el resto del código no cambia. Con `LLM_PROVIDER=openai`
  vuelve al original (GPT-4o-mini + `OPENAI_API_KEY`).
- `.env.example`: documenta las dos opciones.
- La base `alo-rico-rico.sqlite` es una COPIA fresca del Excel, generada con
  `~/workspace/bodegacontrol-sqlite/migrar_excel_a_sqlite.py`. El agente la abre
  en **solo lectura** por defecto: no puede modificar tus datos. Para regenerarla,
  corre de nuevo el script de migración con `--out` a este archivo.

## Cómo conseguir la clave gratis (Gemini)

1. En el teléfono, abre https://aistudio.google.com con tu cuenta de Google.
2. Toca "Get API key" → "Create API key".
3. No pide tarjeta. Copia la clave y pásamela por la bóveda segura (yo no la veo
   en el chat) o guárdala tú en el archivo `.env` de esta carpeta.

## Cómo correrlo

```bash
cd ~/workspace/aprendizaje-programacion/sql-query-agent
cp .env.example .env   # solo la primera vez, y pon tu clave en .env
source .venv/bin/activate
python agent.py --db alo-rico-rico.sqlite
```

O una sola pregunta:

```bash
python agent.py --db alo-rico-rico.sqlite --question "¿Cuáles son los 3 productos que más venden?"
```

## Tablas de la base (para saber qué preguntar)

- `products`: productos (name, category, cashPrice, transferPrice, stock, cost)
- `sales`: ventas (date, product_name, quantity, total, client, payment_method)
- `purchases`: lotes de compra (lot_number, product_name, quantity, unit_cost, supplier)
- `credit_sales`: ventas a crédito (client, product_name, amount, paid)
- `debt_payments`: abonos de deudas (client, amount, date)
- `clients`: clientes (name, phone, level)
- `expenses`: gastos (date, description, amount, category)
- `daily_closes`: cierres de caja

## Preguntas de ejemplo (en español, el agente responde en español)

- "¿Cuánto debe Yiyo en total?"
- "¿Cuáles son los 5 productos que más se vendieron este mes?"
- "¿Cuánto se vendió en efectivo y cuánto por transferencia en noviembre?"
- "¿Qué productos tienen stock 0?"
- "¿Cuánto se gastó en pan este mes?"
