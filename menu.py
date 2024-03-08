# Será la interfaz que unirá el programa principal y la base de datos.
import os
import helpers
import database as db

def iniciar():
    while True:
        helpers.limpiar_pantalla()

        print("========================")
        print("* Bienvenido al Gestor *")
        print("========================")
        print("[1] Listar los clientes ")
        print("[2] Buscar un cliente   ")
        print("[3] Crear un cliente    ")
        print("[4] Modificar un cliente")
        print("[5] Eliminar un cliente ")
        print("[6] Cerrar el Gestor    ")
        print("========================")

        opcion = input("> ")
        helpers.limpiar_pantalla()

        if opcion == "1":
            print("Listando los clientes...\n")
            for cliente in db.Clientes.lista:
                print(cliente)

        elif opcion == "2":
            print("Buscando un cliente...\n")
            dni = helpers.leer_texto(3,3,"DNI (tiene que tener 2 números y 1 letra)").upper()
            cliente = db.Clientes.buscar(dni)
            print(cliente) if cliente else print("Cliente no encontrado!")

        elif opcion == "3":
            print("Creando un cliente...\n")
            dni = None
            while True:
                dni = helpers.leer_texto(3, 3, "DNI (Tiene que tener 2 números y 1 letra)").upper()
                if helpers.validar_dni(dni, db.Clientes.lista):
                    break
            nombre = helpers.leer_texto(2, 30, "Nombre (De 2 a 30 caracteres)").capitalize()
            apellido = helpers.leer_texto(2, 30, "Apellido (De 2 a 30 caracteres)").capitalize()
            db.Clientes.crear(dni, nombre, apellido)
            print("Cliente creado con éxito!")
            

        elif opcion == "4":
            print("Modificando un cliente...\n")
            dni = helpers.leer_texto(3,3,"DNI (Tiene que tener 2 números y 1 letra)").upper()
            cliente = db.Clientes.buscar(dni)
            if cliente:
                nombre = helpers.leer_texto(2, 30, f"Nombre (De 2 a 30 caracteres) [{cliente.nombre}]").capitalize()
                apellido = helpers.leer_texto(2, 30, f"Apellido (De 2 a 30 caracteres) [{cliente.apellido}]").capitalize()
                db.Clientes.modificar(cliente.dni, nombre, apellido)
                print("Cliente modificado con éxito!")
            else:
                print("Cliente no encontrado!")


        elif opcion == "5":
            print("Eliminando un cliente...\n")
            dni = helpers.leer_texto(3,3,"DNI (Tiene que tener 2 números y 1 letra)").upper()
            print("Cliente eliminado con éxito!") if db.Clientes.borrar(dni) else print("Cliente no encontrado!")

        elif opcion == "6":
            print("Saliendo...\n")
            break

        input ("\nPresiona ENTER para continuar...")