from datetime import datetime, timezone
from pprint import pprint
import sys
from pymongo import MongoClient

# Conexión a la base de datos ya poblada
cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["cafeteria_colombiana_db"]


def insertar_crud():
  print("\n--- 1. CRUD: Inserción ---")
  print(f"Total pedidos ANTES de insertar: {db.pedidos.count_documents({})}")
  res = db.pedidos.insert_one({
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
  print(f"Total pedidos DESPUÉS de insertar: {db.pedidos.count_documents({})}")
  print("Documento recién agregado:")
  pprint(db.pedidos.find_one({"_id": res.inserted_id}))


def seleccionar_crud():
  print("\n--- 2. CRUD: Selección ---")
  doc = db.pedidos.find_one({"codigo_orden": "ORD-2001"})
  if doc:
    print("Documento encontrado:")
    pprint(doc)
  else:
    print("No se encontró el documento ORD-2001 (ejecuta primero la opción 1).")


def actualizar_crud():
  print("\n--- 3. CRUD: Actualización ---")
  antes = db.pedidos.find_one({"codigo_orden": "ORD-2001"})
  if not antes:
    print("No existe ORD-2001. Ejecuta primero la opción 1.")
    return

  print(f"Estado ANTES de actualizar: {antes['estado']}")
  res = db.pedidos.update_one(
      {"codigo_orden": "ORD-2001"}, {"$set": {"estado": "Entregado"}}
  )
  despues = db.pedidos.find_one({"codigo_orden": "ORD-2001"})
  print(f"Documentos modificados: {res.modified_count}")
  print(f"Estado DESPUÉS de actualizar: {despues['estado']}")
  print("Documento actualizado completo:")
  pprint(despues)


def eliminar_crud():
  print("\n--- 4. CRUD: Eliminación ---")
  doc_borrar = db.pedidos.find_one({"codigo_orden": "ORD-2001"})
  if not doc_borrar:
    print("No existe ORD-2001 para eliminar.")
    return

  print("Documento a eliminar:")
  pprint(doc_borrar)
  print(f"Total pedidos ANTES de eliminar: {db.pedidos.count_documents({})}")

  res = db.pedidos.delete_one({"codigo_orden": "ORD-2001"})

  print(f"Documentos eliminados: {res.deleted_count}")
  print(f"Total pedidos DESPUÉS de eliminar: {db.pedidos.count_documents({})}")
  print(
      "Verificación de búsqueda tras eliminar:"
      f" {db.pedidos.find_one({'codigo_orden': 'ORD-2001'})}"
  )


def filtros():
  print("\n--- 5. Filtro: Pedidos Entregados > $20.000 por pago digital ---")
  query = {
      "estado": "Entregado",
      "total": {"$gt": 20000},
      "metodo_pago": {"$in": ["Tarjeta", "Nequi/Daviplata"]},
  }
  total_coincidencias = db.pedidos.count_documents(query)
  print(
      "Criterios aplicados: estado='Entregado', total > 20000, pago en"
      " [Tarjeta, Nequi/Daviplata]"
  )
  print(f"Total de pedidos que cumplen el filtro: {total_coincidencias}")
  print("Mostrando los primeros 3 resultados:\n")

  for doc in db.pedidos.find(query).limit(3):
    pprint(doc)
    print("-" * 40)


def join_lookup():
  print("\n--- 6. Join ($lookup) entre 'pedidos' y 'productos' ---")
  print(
      "Cruzando 'pedidos.items.producto_id' con 'productos.producto_id'...\n"
  )
  resultados = db.pedidos.aggregate([
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
  for doc in resultados:
    print(f"Orden: {doc['codigo_orden']} | Total: ${doc['total']} COP")
    print("Ítems comprados en el pedido:")
    pprint(doc["items"])
    print("Información traída desde la colección 'productos' ($lookup):")
    pprint(doc["detalle_catalogo"])
    print("=" * 50)


def agregacion_pagos():
  print("\n--- 7. Agregación: Estadísticas por método de pago ---")
  print("Filtro previo ($match): solo pedidos con estado = 'Entregado'\n")
  resultados = db.pedidos.aggregate([
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
  for doc in resultados:
    print(
        f"Método de pago: {doc['_id']:<16} | "
        f"Pedidos: {doc['cantidad_pedidos']:<3} | "
        f"Ingresos: ${doc['ingresos_totales']:,.0f} COP | "
        f"Promedio: ${doc['ticket_promedio']:,.2f} COP"
    )


def agregacion_horas():
  print("\n--- 8. Agregación: Ventas por franja horaria ---")
  print("Filtro previo ($match): solo pedidos con estado = 'Entregado'\n")
  resultados = db.pedidos.aggregate([
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
  for doc in resultados:
    hora = f"{doc['_id']:02d}:00 - {doc['_id']:02d}:59"
    print(
        f"Franja {hora} | "
        f"Órdenes entregadas: {doc['total_ordenes']:<3} | "
        f"Ventas acumuladas: ${doc['ventas_franja_cop']:,.0f} COP"
    )


# Menú para ejecutar cada función directamente desde la terminal
if __name__ == "__main__":
  acciones = {
      "1": insertar_crud,
      "2": seleccionar_crud,
      "3": actualizar_crud,
      "4": eliminar_crud,
      "5": filtros,
      "6": join_lookup,
      "7": agregacion_pagos,
      "8": agregacion_horas,
  }

  # Permite ejecutar pasando el número directo (ej: python consultas.py 1)
  if len(sys.argv) > 1 and sys.argv[1] in acciones:
    acciones[sys.argv[1]]()
  else:
    print(
        "\nElige la consulta a ejecutar:\n"
        "1: Insertar | 2: Seleccionar | 3: Actualizar | 4: Eliminar\n"
        "5: Filtros  | 6: Join ($lookup) | 7: Agg Pagos | 8: Agg Horas"
    )
    opcion = input("Número de opción: ").strip()
    if opcion in acciones:
      acciones[opcion]()
    else:
      print("Opción no válida.")