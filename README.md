# Tarea 4 — Implementación y Consultas en MongoDB (`cafeteria_colombiana_db`)

Repositorio correspondiente al aporte individual y grupal de la **Tarea 4: Almacenamiento y Consultas de Datos en Big Data** (Universidad Nacional Abierta y a Distancia — UNAD, curso `202016911`).

## Caso de Uso

Gestión de catálogo y pedidos para una **cafetería colombiana de especialidad** (`cafeteria_colombiana_db`), modelada en MongoDB con dos colecciones:
- **`productos`** (10 documentos): catálogo de bebidas y productos de panadería/repostería con `producto_id`, `nombre`, `categoria`, `precio_base` y `disponible`.
- **`pedidos`** (105 documentos iniciales): órdenes con `codigo_orden`, `fecha_hora`, `canal`, `estado`, `metodo_pago`, arreglo embebido `items` (con `personalizaciones`) y `total`.

## Estructura del Repositorio

```text
.
├── app.py          # Conexión a MongoDB, limpieza/carga inicial (10 productos y 105 pedidos) y ejecución secuencial de consultas
├── consultas.py    # Menú interactivo y ejecución individual (1 al 8) de operaciones CRUD, filtros, $lookup y agregaciones
└── README.md       # Documentación del proyecto y guía de ejecución
