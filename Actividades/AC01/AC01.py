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
    def __init__(self, id_auto, marca, año, modelo, transimision, precio, estado, dueño=""):
        self.id_auto = id_auto
        self.marca = marca
        self.modelo = modelo
        self.transmision = transimision # MT o AT
        self.precio = precio
        self.estado = estado # nuevo o usado
        self.dueño = dueño

    def __repr__(self):
        print("ID: {0} \n Marca: {1} \n Modelo: {2} \n Transmision: {3} \n Precio: {4} \n Estado: {2} \n".format(self.id_auto, self.marca, self.modelo, self.transmision, self.precio, self.estado))

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

    def contador(self):
        cuenta = len(self.usados) + len(self.nuevos)
        self.cantidad_autos = cuenta
        return cuenta


class Dueño:
    def __init__(self, nombre, rut, telefono, correo):
        self.nombre = nombre
        self.rut = rut
        self.telefono = telefono
        self.correo = correo

    def __repr__(self):
        print("nombre: {0}, rut: {1}, telefono: {3}, correo: {4}".format(self.nombre, self.rut, self.telefono, self.correo))

rafael = Dueño("Rafael", "193453234", 982838289, "m@m.cl")
javier = Dueño("Javier", "193453234", 282929383, "javier@muc.cl")
nicolas = Dueño("Nicolas", "193453234", 827838393, "nic@m.cl")
juan = Dueño("Juan", "193453234", 982838289, "m@m.cl")
miguel = Dueño("Miguel", "193453234", 282929383, "javier@muc.cl")
vicente = Dueño("Vicente", "193453234", 827838393, "nic@m.cl")

auto1 = Auto(1, "Toyota", 2014, "Yaris Sport", "AT", 8000000, "usado", rafael)
auto2 = Auto(2, "Porsche", 2016, "911", "MT", 40000000, "usado", javier)
auto3 = Auto(3, "Tesla", 2015, "TesX", "MT", 2000000, "usado", nicolas)
auto4 = Auto(4, "Ford", 2013, "F-150", "AT", 8000000, "nuevo")
auto5 = Auto(5, "Lexus", 2012, "LX100", "AT", 40000000, "nuevo")
auto6 = Auto(6, "BMW", 2011, "Z-4", "AT", 30000000, "nuevo")

auto7 = Auto(7, "BMW", 2011, "Z-4", "AT", 30000000, "usado", juan)
auto8 = Auto(8, "BMW", 2011, "Z-4", "AT", 30000000, "usado", miguel)
auto9 = Auto(9, "BMW", 2011, "Z-4", "AT", 30000000, "nuevo", vicente)
auto10 = Auto(10, "BMW", 2011, "Z-4", "AT", 30000000, "nuevo")
auto11 = Auto(11, "BMW", 2011, "Z-4", "AT", 30000000, "nuevo")
auto12 = Auto(12, "BMW", 2011, "Z-4", "AT", 30000000, "nuevo"

A = Sucursal("Sucursal 1")
B = Sucursal("Sucursal 2")
A.agregarAuto(auto1)
A.agregarAuto(auto2)
A.agregarAuto(auto3)
A.agregarAuto(auto4)
A.agregarAuto(auto5)
A.agregarAuto(auto6)

B.agregarAuto(auto7)
B.agregarAuto(auto8)
B.agregarAuto(auto9)
B.agregarAuto(auto10)
B.agregarAuto(auto11)
B.agregarAuto(auto12)

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

    if opcion == 2:
        total_autos = 0
        for sucursal in automotora.sucursales:
            total_autos += sucursal.cantidad_autos
        print("Hay un total de {} autos".format(total_autos))

    if opcion == 3:
        sys.exit()

if usuario == 2:
    opcion = int(input("1. Filtrar \n 2. Salir del sistema"))
    if opcion == 1:
        opcion2 = int(input("Filtrar por \n 1. Año \n 2. Precio \n 3. Marca \n 4. Transmision  \n 5. Estado"))
        if opcion2 == 1:
            año_min = int(input("Ingrese un año minimo"))
            año_max = int(input("Ingrese un año máximo"))
            parametro = [año_min, año_max]
            resultado = automotora.busqueda("año", parametro)

        if opcion2 == 2:
            precio_min = int(input("Ingrese un precio minimo"))
            precio_max = int(input("Ingrese un precio máximo"))
            parametro = [precio_min, precio_max]
            resultado = automotora.busqueda("precio", parametro)

        if opcion2 == 3:
            marca = input("Ingrese una marca")
            parametro = [marca]
            resultado = automotora.busqueda("marca", parametro)

        if opcion2 == 4:
            transmision = input("Ingrese una transmision")
            parametro = [transmision]
            resultado = automotora.busqueda("transmision", parametro)

        if opcion2 == 5:
            estado = input("Ingrese un estado")
            parametro = [estado]
            resultado = automotora.busqueda("estado", parametro)

        for auto in resultado:
            print(auto)
            print(auto.dueño)

    if opcion == 2:
        sys.exit()