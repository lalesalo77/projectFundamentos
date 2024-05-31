import os
import re
from prettytable import PrettyTable

# Función para leer los productos desde el archivo
def leer_productos(archivo):
    productos = []
    if os.path.exists(archivo):
        with open(archivo, 'r') as file:
            for linea in file:
                nombre, precio, cantidad = linea.strip().split(',')
                productos.append({
                    'nombre': nombre,
                    'precio': float(precio),
                    'cantidad': int(cantidad)
                })
    return productos

# Función para guardar los productos en el archivo
def guardar_productos(archivo, productos):
    with open(archivo, 'w') as file:
        for producto in productos:
            file.write(f"{producto['nombre']},{producto['precio']},{producto['cantidad']}\n")

# Función para inicializar el archivo de productos con un producto predefinido
def inicializar_productos(archivo):
    if not os.path.exists(archivo):
        productos = [{'nombre': 'tenis', 'precio': 800000, 'cantidad': 80}]
        guardar_productos(archivo, productos)

# Función para añadir un producto
def anadir_producto(archivo, nombre, precio, cantidad):
    productos = leer_productos(archivo)
    for producto in productos:
        if producto['nombre'].lower() == nombre.lower():
            print(f"Ya existe un producto con el nombre '{nombre}'.")
            print("Producto existente:")
            tabla = PrettyTable()
            tabla.field_names = ["Nombre", "Precio", "Cantidad"]
            tabla.add_row([producto['nombre'], producto['precio'], producto['cantidad']])
            print(tabla)
            aumentar = input(f"¿Desea aumentar la cantidad de '{nombre}'? (s/n): ").lower()
            if aumentar == 's':
                producto['cantidad'] += cantidad
                guardar_productos(archivo, productos)
                print("Cantidad aumentada correctamente.")
            return
    productos.append({'nombre': nombre, 'precio': precio, 'cantidad': cantidad})
    guardar_productos(archivo, productos)
    return {'nombre': nombre, 'precio': precio, 'cantidad': cantidad}

# Función para eliminar un producto
def eliminar_producto(archivo, nombre):
    productos = leer_productos(archivo)
    productos = [producto for producto in productos if producto['nombre'].lower() != nombre.lower()]
    guardar_productos(archivo, productos)
    print(f"Producto '{nombre}' eliminado correctamente.")

# Función para ver los productos en formato de tabla
def ver_productos(archivo):
    productos = leer_productos(archivo)
    tabla = PrettyTable()
    tabla.field_names = ["Nombre", "Precio", "Cantidad"]
    for producto in productos:
        tabla.add_row([producto['nombre'], producto['precio'], producto['cantidad']])
    print(tabla)

# Función para guardar los clientes
def guardar_cliente(archivo, cliente, compra, total):
    with open(archivo, 'a') as file:
        file.write(f"{cliente}|{compra}|{total}\n")

def ver_compras(clientes_archivo):
    if os.path.exists(clientes_archivo):
        tabla_compras = PrettyTable()
        tabla_compras.field_names = ["Cliente", "Compra", "Total"]
        with open(clientes_archivo, 'r') as file:
            for linea in file:
                partes = linea.strip().split('|')
                if len(partes) == 3:
                    cliente, compra, total = partes
                    tabla_compras.add_row([cliente, compra, total])
                else:
                    print(f"Formato incorrecto en la línea: {linea.strip()}")
        print(tabla_compras)
    else:
        print("Aún no se han realizado compras.")



def menu_principal():
    print("Bienvenido a la tienda virtual")
    nombre = input("Por favor, ingrese su nombre: ")

    productos_archivo = 'productos.txt'
    clientes_archivo = 'clientes.txt'
    inicializar_productos(productos_archivo)

    if nombre.lower() == 'admin':
        print("\n--- Bienvenido querido administrador, ¿qué desea realizar? ---")
        while True:
            print("\n--- Menú Admin ---")
            tabla_menu = PrettyTable()
            tabla_menu.field_names = ["Opción", "Descripción"]
            tabla_menu.add_row(["1", "Añadir productos"])
            tabla_menu.add_row(["2", "Eliminar productos"])
            tabla_menu.add_row(["3", "Ver mis productos"])
            tabla_menu.add_row(["4", "Ver compras de los clientes"])
            tabla_menu.add_row(["5", "Salir"])
            print(tabla_menu)
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                while True:
                    nombre_producto = input("Nombre del producto: ")
                    precio_producto = float(input("Precio del producto: "))
                    cantidad_producto = int(input("Cantidad del producto: "))
                    producto_anadido = anadir_producto(productos_archivo, nombre_producto, precio_producto, cantidad_producto)
                    if producto_anadido:
                        print(f"Producto añadido: Nombre: {producto_anadido['nombre']}, Precio: {producto_anadido['precio']}, Cantidad: {producto_anadido['cantidad']}")
                    otro_producto = input("¿Desea añadir otro producto? (s/n): ")
                    if otro_producto.lower() != 's':
                        print("\n--- Lista de Productos Añadidos ---")
                        ver_productos(productos_archivo)
                        break
            elif opcion == '2':
                nombre_producto = input("Nombre del producto a eliminar: ")
                eliminar_producto(productos_archivo, nombre_producto)
            elif opcion == '3':
                print("\n--- Lista de Productos ---")
                ver_productos(productos_archivo)
            elif opcion == '4':
                print("\n--- Compras de los Clientes ---")
                ver_compras(clientes_archivo)
            elif opcion == '5':
                print(f"Adiós, {nombre}")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
    else:
        print(f"Bienvenid@ {nombre}, seleccione la opción que desee realizar.")
        while True:
            print("\n--- Menú Cliente ---")
            tabla_menu = PrettyTable()
            tabla_menu.field_names = ["Opción", "Descripción"]
            tabla_menu.add_row(["1", "Comprar productos"])
            tabla_menu.add_row(["2", "Ver compras"])
            tabla_menu.add_row(["3", "Salir"])
            print(tabla_menu)
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                carrito = []
                while True:
                    print("\n--- Lista de Productos ---")
                    ver_productos(productos_archivo)
                    nombre_producto = input("Ingrese el nombre del producto que desea comprar: ")
                    if nombre_producto == '0':
                        break
                    productos = leer_productos(productos_archivo)
                    producto_encontrado = False
                    for producto in productos:
                        if producto['nombre'].lower() == nombre_producto.lower():
                            producto_encontrado = True
                            cantidad_comprar = int(input(f"¿Cuántos {nombre_producto} desea comprar?: "))
                            if producto['cantidad'] >= cantidad_comprar:
                                producto['cantidad'] -= cantidad_comprar
                                carrito.append({'nombre': nombre_producto, 'cantidad': cantidad_comprar, 'precio': producto['precio']})
                                guardar_productos(productos_archivo, productos)
                                print("Producto añadido al carrito.")
                            else:
                                print("No hay suficiente cantidad en stock.")
                            break
                    if not producto_encontrado:
                        print("No hay de esos. Seleccione por favor uno de nuestros productos o presione 0 para cancelar la compra.")

                    otro_producto = input("¿Desea comprar más productos? (s/n): ")
                    if otro_producto.lower() != 's':
                        break

                if carrito:
                    total = sum(item['cantidad'] * item['precio'] for item in carrito)
                    print(f"\n--- Resumen de la Compra ---")
                    tabla_carrito = PrettyTable()
                    tabla_carrito.field_names = ["Cantidad", "Nombre", "Precio Unitario"]
                    for item in carrito:
                        tabla_carrito.add_row([item['cantidad'], item['nombre'], item['precio']])
                    print(tabla_carrito)
                    print(f"Total a pagar: {total}")

                    while True:
                        metodo_pago = input("¿Desea pagar en efectivo o tarjeta? (efectivo/tarjeta): ").lower()
                        if metodo_pago == 'efectivo':
                            print(f"Valor a pagar en efectivo: {total}")
                            break
                        elif metodo_pago == 'tarjeta':
                            print("Recibiendo pago...")
                            print(".....")
                            print(f"Pago recibido por un valor de {total}")
                            break
                        else:
                            print("Método de pago no válido. Por favor, indique si desea pagar en efectivo o tarjeta.")

                    compras = ", ".join([f"{item['cantidad']} x {item['nombre']}" for item in carrito])
                    guardar_cliente(clientes_archivo, nombre, compras, total)
            elif opcion == '2':
                print("\n--- Tus Compras ---")
                if os.path.exists(clientes_archivo):
                    tabla_compras = PrettyTable()
                    tabla_compras.field_names = ["Compra", "Total"]
                    with open(clientes_archivo, 'r') as file:
                        for linea in file:
                            try:
                                cliente, compra, total = linea.strip().split('|')
                                if cliente == nombre:
                                    tabla_compras.add_row([compra, total])
                            except ValueError:
                                print(f"Formato incorrecto en la línea: {linea.strip()}")
                    print(tabla_compras)
                else:
                    print("Aún no has realizado ninguna compra.")
            elif opcion == '3':
                print(f"Adiós, {nombre}")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu_principal()
