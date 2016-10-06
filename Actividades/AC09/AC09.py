# AC09
from random import randint, expovariate, uniform
from collections import deque
import main


class Restaurant:
    def __init__(self, nro_mesas):
        self.mesas = nro_mesas
        self.mesas_disponibles = nro_mesas
        self.menu = {"Filete": (5600, 5, 8, 0.15), "Nino": (3500, 3, 5, 0.2),
                     "Consome": (4800, 3, 6, 0.1), "Porotos": (5600, 6, 8, 0.1),
                     "Ensalada": (2600, 3, 4, 0.05), "Asiento": (5600, 4, 6, 0.1),
                     "Pollo": (3500, 5, 7, 0.3)}

    def asignar_plato(self, grupo, tiempo_actual, menu):
        for persona in grupo.personas:
            proba = uniform(0, 1)
            if proba <= 0.15:
                persona.tiempo_plato = randint(5, 8)
                grupo.cuenta += 5600
                menu["Filete"] += 5600
            elif proba <= 0.35:
                persona.tiempo_plato = randint(3, 5)
                grupo.cuenta += 3500
                menu["Nino"] += 3500
            elif proba <= 0.45:
                persona.tiempo_plato = randint(3, 6)
                grupo.cuenta += 4800
                menu["Consome"] += 4800
            elif proba <= 0.55:
                persona.tiempo_plato = randint(6, 8)
                grupo.cuenta += 5600
                menu["Porotos"] += 5600
            elif proba <= 0.6:
                persona.tiempo_plato = randint(3, 4)
                grupo.cuenta += 2600
                menu["Ensalada"] += 2600
            elif proba <= 0.7:
                persona.tiempo_plato = randint(4, 6)
                grupo.cuenta += 5600
                menu["Asiento"] += 5600
            else:
                persona.tiempo_plato = randint(5, 7)
                grupo.cuenta += 3500
                menu["Pollo"] += 3500

        grupo.llegada_pedido = tiempo_actual + max(grupo.personas, key=lambda x: x.tiempo_plato).tiempo_plato
        grupo.tiempo_mesa_lista = grupo.llegada_pedido + max(grupo.personas, key=lambda x: x.tiempo_comer).tiempo_comer


    @property
    def _mesas_disponibles(self):
        return self.mesas_disponibles


class Persona:
    def __init__(self):
        self.espera_mesa = randint(15, 25)
        self.espera_plato = randint(6, 10)
        self.tiempo_comer = randint(20, 30)
        self.tiempo_plato = None

class Grupo:
    def __init__(self, nro_personas):
        self.personas = [Persona() for _ in range(nro_personas)]
        self.tiempo_espera_mesa = min(self.personas, key=lambda x: x.espera_mesa).espera_mesa
        self.tiempo_espera_plato = min(self.personas, key=lambda x: x.espera_plato).espera_plato
        self.llegada_pedido = float("Inf")
        self.tiempo_mesa_lista = float("Inf")
        self.cuenta = 0


class Simulacion:
    def __init__(self, nro_mesas, tiempo_simulacion, tasa_llegada):
        self.tiempo_maximo = tiempo_simulacion
        self.tasa_llegada = tasa_llegada
        self.tiempo_simulacion = 0
        self.tiempo_prox_grupo = 0
        self.cola = deque()
        self.restaurant = Restaurant(nro_mesas)
        self.grupos_mesas = list()

        self.dinero_ganado = 0
        self.platos = {"Filete": 0, "Nino": 0, "Consome": 0, "Porotos": 0,
                       "Ensalada":0, "Asiento": 0, "Pollo": 0}

        self.por_demora_plato = 0
        self.por_demora_fila = 0
        self.satisfechos = 0

        self.prox_mesa_lista = None
        self.prox_retira_fila = None
        self.prox_retira_mesa = None

        self.plato_no_entregado = 0


    def proximo_grupo(self, tasa_llegada):
        self.tiempo_proximo_grupo = self.tiempo_simulacion + \
                                    round(expovariate(tasa_llegada))

    def run(self):
        self.proximo_grupo(self.tasa_llegada)
        while self.tiempo_simulacion < self.tiempo_maximo:
            if len(self.cola) > 0:
                self.prox_retira_fila = min(self.cola,
                                            key=lambda c: c.tiempo_espera_mesa)

            else:
                self.prox_retira_fila = None

            if len(self.grupos_mesas) > 0:
                self.prox_retira_mesa = min(self.grupos_mesas,
                                            key=lambda c: c.tiempo_espera_plato)
                self.prox_mesa_lista = min(self.grupos_mesas,
                                           key=lambda c: c.tiempo_mesa_lista)
            else:
                self.prox_retira_mesa = None
                self.prox_mesa_lista = None

            try:
                self.tiempo_simulacion = min(self.tiempo_prox_grupo,
                                             self.prox_retira_fila.tiempo_espera_mesa,
                                             self.prox_retira_mesa.tiempo_espera_plato,
                                             self.mesa_lista.tiempo_mesa_lista)
            except (AttributeError):
                self.tiempo_simulacion = self.tiempo_prox_grupo

            # llega un grupo
            if self.tiempo_simulacion == self.tiempo_prox_grupo:
                self.cola.append(Grupo(randint(2, 7)))
                self.proximo_grupo(self.tasa_llegada)
                main.report_event(self.tiempo_simulacion, main.LLEGADA_CLIENTE)

                if len(self.cola[
                           0].personas) <= 5 and self.restaurant._mesas_disponibles >= 1:
                    self.restaurant.asignar_plato(self.cola[0],
                                                   self.tiempo_simulacion, self.platos)
                    self.restaurant.mesas_disponibles -= 1
                    self.grupos_mesas.append(self.cola[0])
                    self.cola.popleft()
                elif len(self.cola[
                             0].personas) > 5 and self.restaurant._mesas_disponibles >= 2:
                    self.restaurant.asignar_plato(self.cola[0],
                                                   self.tiempo_simulacion, self.platos)
                    self.restaurant.mesas_disponibles -= 2
                    self.grupos_mesas.append(self.cola[0])
                    self.cola.popleft()

            # mesa termina satisfecha
            elif self.tiempo_simulacion == self.prox_mesa_lista.tiempo_mesa_lista:
                self.grupos_mesas.remove(self.prox_mesa_lista)
                main.report_event(self.tiempo_simulacion, main.PAGAR)
                if len(self.prox_mesa_lista.personas) > 5:
                    self.restaurant.mesas_disponibles += 2
                    self.satisfechos += len(self.prox_mesa_lista.personas)

                elif len(self.prox_mesa_lista.personas) <= 5:
                    self.restaurant.mesas_disponibles += 1
                    self.satisfechos += len(self.prox_mesa_lista.personas)

            # mesa se va enojada
            elif self.tiempo_simulacion == self.prox_retira_mesa.tiempo_espera_plato:
                self.grupos_mesas.remove(self.prox_retira_mesa)
                main.report_event(self.tiempo_simulacion, main.PACIENCIA_COMIDA)
                if len(self.prox_retira_mesa.personas) > 5:
                    self.restaurant.mesas_disponibles += 2
                    self.por_demora_plato += len(self.prox_retira_mesa.personas)
                    self.dinero_ganado -= self.prox_retira_mesa.cuenta
                    self.plato_no_entregado += self.prox_retira_mesa.cuenta

                elif len(self.prox_retira_mesa.personas) <= 5:
                    self.restaurant.mesas_disponibles += 1
                    self.por_demora_plato += len(self.prox_retira_mesa.personas)
                    self.dinero_ganado -= self.prox_retira_mesa.cuenta
                    self.plato_no_entregado += self.prox_retira_mesa.cuenta

            # se retiran de la fila
            elif self.tiempo_simulacion == self.prox_retira_fila.tiempo_espera_mesa:
                main.report_event(self.tiempo_simulacion, main.PACIENCIA_FILA)
                self.cola.remove(self.prox_retira_fila)
                self.por_demora_fila += len(self.prox_retira_fila.personas)

        print("Estadisticas:")
        print("Plato que genera mas ingresos: {}".format(max(self.platos, key=lambda x: self.platos[x])))
        print("Dinero ganado: {}".format(self.dinero_ganado))
        print("Perdidas por platos no entregados: {}".format(self.plato_no_entregado))
        print("Personas por demora de plato: {}".format(self.por_demora_plato))
        print("Personas por demora de fila: {}".format(self.por_demora_fila))
        print("Personas satisfecha: {}".format(self.satisfechos))


if __name__ == "__main__":
    tasa_llegada = 0.1
    s = Simulacion(10, tasa_llegada, 50)
    s.run()





