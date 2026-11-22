from datetime import datetime, timezone
from pprint import pprint
from pymongo import MongoClient

# 1. Conectar al servidor local de MongoDB
cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["cafeteria_colombiana_db"]

# Limpiar colecciones previas si existen
db.productos.drop()
db.pedidos.drop()

# 2. Insertar catálogo en la colección 'productos' (10 documentos)
productos_catalogo = [
    {
        "producto_id": "PROD-01",
        "nombre": "Tinto Campesino",
        "categoria": "Bebidas Calientes",
        "precio_base": 3500,
        "disponible": True,
    },
    {
        "producto_id": "PROD-02",
        "nombre": "Café Latte",
        "categoria": "Bebidas Calientes",
        "precio_base": 7500,
        "disponible": True,
    },
    {
        "producto_id": "PROD-03",
        "nombre": "Capuccino Vainilla",
        "categoria": "Bebidas Calientes",
        "precio_base": 8500,
        "disponible": True,
    },
    {
        "producto_id": "PROD-04",
        "nombre": "Granizado de Café",
        "categoria": "Bebidas Frías",
        "precio_base": 9500,
        "disponible": True,
    },
    {
        "producto_id": "PROD-05",
        "nombre": "Cold Brew Naranja",
        "categoria": "Bebidas Frías",
        "precio_base": 9000,
        "disponible": True,
    },
    {
        "producto_id": "PROD-06",
        "nombre": "Almojábana Horneada",
        "categoria": "Panadería",
        "precio_base": 4500,
        "disponible": True,
    },
    {
        "producto_id": "PROD-07",
        "nombre": "Pandebono Valluno",
        "categoria": "Panadería",
        "precio_base": 4000,
        "disponible": True,
    },
    {
        "producto_id": "PROD-08",
        "nombre": "Croissant de Almendras",
        "categoria": "Panadería",
        "precio_base": 7000,
        "disponible": True,
    },
    {
        "producto_id": "PROD-09",
        "nombre": "Torta de Zanahoria",
        "categoria": "Repostería",
        "precio_base": 8000,
        "disponible": True,
    },
    {
        "producto_id": "PROD-10",
        "nombre": "Arepa de Chocolo con Queso",
        "categoria": "Típicos",
        "precio_base": 6500,
        "disponible": True,
    },
]
db.productos.insert_many(productos_catalogo)

# 3. Generar e insertar 105 documentos en la colección 'pedidos'
estados = [
    "Entregado",
    "Entregado",
    "Entregado",
    "Entregado",
    "En preparación",
    "Cancelado",
]
canales = ["Barra", "App Móvil", "Domicilio"]
metodos_pago = ["Efectivo", "Tarjeta", "Nequi/Daviplata"]
opciones_personalizacion = [
    ["Leche deslactosada"],
    ["Leche de almendras", "Sin azúcar"],
    ["Extra shot espresso"],
    ["Caliente"],
    ["Con hielo extra"],
    ["Sin personalización"],
]

lista_pedidos = []

for i in range(1, 106):
  num_items = (i % 3) + 1
  items_pedido = []
  total_pedido = 0

  for j in range(num_items):
    prod = productos_catalogo[(i + j) % len(productos_catalogo)]
    cantidad = ((i + j) % 2) + 1
    pers = opciones_personalizacion[(i + j) % len(opciones_personalizacion)]

    items_pedido.append({
        "producto_id": prod["producto_id"],
        "nombre_producto": prod["nombre"],
        "cantidad": cantidad,
        "precio_unitario": prod["precio_base"],
        "personalizaciones": pers,
    })
    total_pedido += prod["precio_base"] * cantidad

  hora = 7 + (i % 14)
  minuto = (i * 7) % 60
  fecha_orden = datetime(2026, 11, 15, hora, minuto, 0, tzinfo=timezone.utc)

  lista_pedidos.append({
      "codigo_orden": f"ORD-{1000 + i}",
      "fecha_hora": fecha_orden,
      "canal": canales[i % len(canales)],
      "estado": estados[i % len(estados)],
      "metodo_pago": metodos_pago[i % len(metodos_pago)],
      "items": items_pedido,
      "total": total_pedido,
  })

db.pedidos.insert_many(lista_pedidos)
print(f"Productos insertados: {db.productos.count_documents({})}")
print(f"Pedidos insertados: {db.pedidos.count_documents({})}")
print("-" * 50)

# ==========================================
# EJECUCIÓN DE CONSULTAS PARA CAPTURAS
# ==========================================

# A. CRUD BÁSICO

print("\n--- 1. CRUD: Inserción ---")
db.pedidos.insert_one({
    "codigo_orden": "ORD-2001",
    "fecha_hora": datetime(2026, 11, 15, 16, 30, 0, tzinfo=timezone.utc),
    "canal": "Barra",
    "estado": "En preparación",
    "metodo_pago": "Nequi/Daviplata",
    "items": [{
        "producto_id": "PROD-02",
        "nombre_producto": "Café Latte",
        "cantidad": 1,
        "precio_unitario": 7500,
        "personalizaciones": ["Leche de avena"],
    }],
    "total": 7500,
})

print("\n--- 2. CRUD: Selección ---")
pprint(db.pedidos.find_one({"codigo_orden": "ORD-2001"}))

print("\n--- 3. CRUD: Actualización ---")
db.pedidos.update_one(
    {"codigo_orden": "ORD-2001"}, {"$set": {"estado": "Entregado"}}
)
pprint(db.pedidos.find_one({"codigo_orden": "ORD-2001"}))

print("\n--- 4. CRUD: Eliminación ---")
res_del = db.pedidos.delete_one({"codigo_orden": "ORD-2001"})
print(f"Documentos eliminados: {res_del.deleted_count}")

# B. FILTROS Y OPERADORES
print("\n--- 5. Filtro: Pedidos Entregados > $20.000 por pago digital ---")
filtro = db.pedidos.find({
    "estado": "Entregado",
    "total": {"$gt": 20000},
    "metodo_pago": {"$in": ["Tarjeta", "Nequi/Daviplata"]},
}).limit(3)
for doc in filtro:
  pprint(doc)

# C. JOIN CON $lookup
print("\n--- 6. Join ($lookup) entre pedidos y productos ---")
join_resultado = db.pedidos.aggregate([
    {"$match": {"estado": "Entregado"}},
    {"$limit": 2},
    {
        "$lookup": {
            "from": "productos",
            "localField": "items.producto_id",
            "foreignField": "producto_id",
            "as": "detalle_catalogo",
        }
    },
])
for doc in join_resultado:
  pprint(doc)

# D. AGREGACIONES (Contar, Sumar, Promediar y Franja Horaria)
print("\n--- 7. Agregación: Estadísticas por método de pago ---")
agg_pagos = db.pedidos.aggregate([
    {"$match": {"estado": "Entregado"}},
    {
        "$group": {
            "_id": "$metodo_pago",
            "cantidad_pedidos": {"$sum": 1},
            "ingresos_totales": {"$sum": "$total"},
            "ticket_promedio": {"$avg": "$total"},
        }
    },
    {"$sort": {"ingresos_totales": -1}},
])
for doc in agg_pagos:
  pprint(doc)

print(
    "\n--- 8. Agregación: Ventas por franja horaria (solo estado Entregado) ---"
)
agg_horas = db.pedidos.aggregate([
    {"$match": {"estado": "Entregado"}},
    {
        "$group": {
            "_id": {"$hour": "$fecha_hora"},
            "total_ordenes": {"$sum": 1},
            "ventas_franja_cop": {"$sum": "$total"},
        }
    },
    {"$sort": {"_id": 1}},
])
for doc in agg_horas:
  pprint(doc)