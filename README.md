# Tarea 4 — Implementación y Consultas en MongoDB (`cafeteria_colombiana_db`)

Repositorio correspondiente al aporte individual y grupal de la **Tarea 4: Almacenamiento y Consultas de Datos en Big Data** (Universidad Nacional Abierta y a Distancia — UNAD, curso `202016911`).

## Caso de Uso

Gestión de catálogo y pedidos para una **cafetería colombiana de especialidad** (`cafeteria_colombiana_db`), modelada en MongoDB con dos colecciones:
- **`productos`** (10 documentos): catálogo de bebidas y productos de panadería/repostería con `producto_id`, `nombre`, `categoria`, `precio_base` y `disponible`.
- **`pedidos`** (105 documentos iniciales): órdenes con `codigo_orden`, `fecha_hora`, `canal`, `estado`, `metodo_pago`, arreglo embebido `items` (con `personalizaciones`) y `total`.

# [Enlace a presentación online](https://ejemplo.com "Enlace a presentación online")

## Estructura del Repositorio
├── app.py          0
├── consultas.py    1
├── capturas/       2
│   └── .gitkeep    3
└── README.md       4

0. Conexión a MongoDB, limpieza/carga inicial (10 productos y 105 pedidos) y ejecución secuencial de consultas
1. Menú interactivo y ejecución individual (1 al 8) de operaciones CRUD, filtros, $lookup y agregaciones
2. Carpeta para almacenar las capturas de pantalla de las consultas y resultados
3. Mantiene la carpeta versionada en Git mientras se agregan las imágenes
4. Documentación del proyecto y guía de ejecución
 
Requisitos Previos
MongoDB ejecutándose en mongodb://localhost:27017/.
Python 3 con el controlador pymongo instalado:
pip install pymongo

Ejecución
Poblar la base de datos y ejecutar la secuencia base (app.py): python app.py

Ejecutar consultas individuales o mediante menú (consultas.py):

# Menú interactivo
python consultas.py

# Ejecución directa por número de consulta (1 a 8)
python consultas.py 1   # CRUD: Inserción (ORD-2001)
python consultas.py 2   # CRUD: Selección
python consultas.py 3   # CRUD: Actualización
python consultas.py 4   # CRUD: Eliminación
python consultas.py 5   # Filtro: Entregados > $20.000 por pago digital ($gt,$in)
python consultas.py 6   # Join ($lookup) entre pedidos y productos
python consultas.py 7   # Agregación: Estadísticas por método de pago ($match,$group, $avg,$sum)
python consultas.py 8   # Agregación: Ventas por franja horaria ($hour)

Autor
Mario Enrique Gómez Carrillo — Ingeniería de Sistemas, UNAD.

