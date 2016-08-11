# AC01 -  Diego Iruretagoyena, Isidora Vizcaya
import datetime
import sys


class Automotora:
    def __init__(self, nombre):
        self.nombre = nombre
        self.sucursales = []
        self.autos = []

    def actualizar(self):
        for sucursal in self.sucursales:
            self.autos += sucursal.nuevos + sucursal.usados

    def agregarSucursal(self, sucursal):
        self.sucursales.append(sucursal)

    def busqueda(self, filtro, parametro):
        self.actualizar()
        resultado = []
        if filtro == "año":
            año_minimo = parametro[0]
            año_maximo = parametro[1]
            for auto in self.autos:
                if auto.año >= año_minimo and auto.año <= año_maximo:
                    resultado.append(auto)

        if filtro == "precio":
            precio_minimo = parametro[0]
            precio_maximo = parametro[1]
            for auto in self.autos:
                if auto.precio >= precio_minimo and auto.precio <= precio_maximo:
                    resultado.append(auto)

        if filtro == "marca":
            for auto in self.autos:
                if auto.marca == parametro[0]:
                    resultado.append(auto)

        if filtro == "transmision":
            for auto in self.autos:
                if auto.transmision == parametro[0]:
                    resultado.append(auto)

        if filtro == "estado":
            for auto in self.autos:
                if auto.estado == parametro[0]:
                    resultado.append(auto)

        return resultado


class Auto:
    def __init__(self, id_auto, marca, año, modelo, transimision, precio, estado, dueño):
        self.id_auto = id_auto
        self.marca = marca
        self.modelo = modelo
        self.transmision = transimision # MT o AT
        self.precio = precio
        self.estado = estado # nuevo o usado
        self.dueño = dueño


class Sucursal:
    def __init__(self, nombre):
        self.nombre = nombre
        self.usados = []
        self.nuevos = []
        self.cantidad_autos = 0

    def agregarAuto(self, auto):
        self.cantidad_autos += 1
        if auto.estado == "nuevo":
            self.nuevos.append(auto)
        if auto.estado == "usado":
            self.usados.append(auto)


class Dueño:
    def __init__(self, nombre, rut, telefono, correo):
        self.nombre = nombre
        self.rut = rut
        self.telefono = telefono
        self.correo = correo

A = Sucursal("Sucursal 1")
B = Sucursal("Sucursal 2")
automotora = Automotora("Automotora Mavrakis")
automotora.agregarSucursal(A)
automotora.agregarSucursal(B)

usuario = int(input("Perfil del usuario: \n 1. Trabajador \n 2. Cliente"))
if usuario == 1:
    opcion = int(input("1. Cambiar precio de un auto \n 2. Conocer la cantidad"
                       " de autos a la venta \n 3. Salir del sistema"))
    if opcion == 1:
        id_buscado = int(input("Ingrese el id del auto"))
        nuevo_precio = int(input("Ingrese del nuevo precio"))
        for sucursal in automotora.sucursales:
            for auto in sucursal.usados:
                if auto.id_auto == id_buscado:
                    auto.precio = nuevo_precio
                    break    
            for auto in sucursal.nuevos:
                if auto.id_auto == id_buscado:
                    auto.precio = nuevo_precio
                    break
    elif opcion == 2:
        total_autos = 0
        for sucursal in automotora.sucursales:
            total_autos += sucursal.cantidad_autos
    elif opcion == 3:
        sys.exit()
elif usuario == 2:
    opcion = int(input("1. Filtrar \n 2. Salir del sistema"))
    if opcion == 1:
        opcion2 = int(input("Filtrar por \n 1. Año \n 2. Precio \n 3. Marca \n 4. Transmision  \n 5. Estado"))
        if opcion2 == 1:
            año_min = int(input("Ingrese un año minimo"))
            año_max = int(input("Ingrese un año máximo"))
        if opcion2 == 2:
            precio_min = int(input("Ingrese un precio minimo"))
            precio_max = int(input("Ingrese un precio máximo"))
        if opcion2 == 3:
            marca = input("Ingrese una marca")
        if opcion2 == 4:
            transmision = input("Ingrese una transmision")
        if opcion2 == 5:
            estado = input("Ingrese un estado")
    if opcion == 2:
        sys.exit()
