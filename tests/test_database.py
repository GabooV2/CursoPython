import csv
import copy
import config
import helpers
import unittest
import database as db

class TestDatabase(unittest.TestCase):

    def setUp(self):
        db.Clientes.lista = [
            db.Cliente("23H", "Pedro", "Lopez"),
            db.Cliente("11P","Martin","Rojas"),
            db.Cliente("30F","Julio","Diaz")
        ]

    def testBuscarCliente(self):
        cliente_existente = db.Clientes.buscar("11P")
        cliente_inexistente = db.Clientes.buscar("44V")
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)

    def testCrearCliente(self):
        nuevo_cliente = db.Clientes.crear("33X","Marta","Dominguez")
        self.assertEqual(len(db.Clientes.lista),4)
        self.assertEqual(nuevo_cliente.dni, "33X")
        self.assertEqual(nuevo_cliente.nombre, "Marta")
        self.assertEqual(nuevo_cliente.apellido, "Dominguez")

    def testModificarCliente(self):
        modificar_cliente = copy.copy(db.Clientes.buscar("30F"))
        cliente_modificado = db.Clientes.modificar("30F","Lucia","Mendez")
        self.assertEqual(modificar_cliente.nombre,"Julio")
        self.assertEqual(cliente_modificado.nombre,"Lucia")

    def testEliminarCliente(self):
        eliminar_cliente = db.Clientes.borrar("11P")
        cliente_rebuscado = db.Clientes.buscar("11P")
        self.assertEqual(eliminar_cliente.dni, "11P")
        self.assertIsNone(cliente_rebuscado)

    def testValidarDNI(self):
        self.assertTrue(helpers.validar_dni("99A", db.Clientes.lista))
        self.assertFalse(helpers.validar_dni("992323323e", db.Clientes.lista))
        self.assertFalse(helpers.validar_dni("aaa", db.Clientes.lista))
        self.assertFalse(helpers.validar_dni("11P", db.Clientes.lista))

    def testEscrituraCsv(self):
        db.Clientes.borrar("11P")
        db.Clientes.borrar("23H")
        db.Clientes.modificar("30F", "Momo","Ramon")

        dni, nombre, apellido = None, None, None
        with open(config.DATABASE_PATH, newline="\n") as fichero:
            reader = csv.reader(fichero, delimiter=";")
            dni,nombre, apellido = next(reader)
    
        self.assertEqual(dni, "30F")
        self.assertEqual(nombre, "Momo")
        self.assertEqual(apellido, "Ramon")
