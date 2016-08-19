# ciudades y sus entidades
# revisar si son necesarias las clases Tienda y CentroProgramon RR


class Ciudad:
    def __init__(self, name, ide, trainers):
        self.name = name
        self.ide = ide
        if self.ide != 0:  # ? RR, Pallet Town
            self.tienda = Tienda()
            self.centro = CentroProgramon()
            self.gimnasio = Gimnasio(self.name, self.ide, trainers)


class Tienda:
    def __init__(self):
        # atributos a definir RR
        # stock infinito
        pass

    def vender(self, jugador):  # jugador es objeto de la clase Jugador
        # aumentar prograbolas y quitar yenes
        # metodo de Tienda o Jugador? RR
        pass


class CentroProgramon:
    # se puede acceder al PC de Bastian para cambiar del equipo algun
    # programon capturado que se encuentra en el PC RR
    pass


class Gimnasio:
    def __init__(self, city_name, city_id, trainers):  # unico para cada ciudad
        self.city_name = city_name
        self.city_id = city_id
        self.leader = trainers[0]  # trainers[0].trainer_type == "leader"
        self.trainers = trainers[1:]  # lista de objetos de la clase Trainer

    def entrar(self, jugador):
        ciudades_batalla = jugador.batallas.keys()  # ciudades donde ha batallado
        if self.city_name not in ciudades_batalla:
            print("Bienvenido! Al parecer no te has enfrentado a ninguno de nuestros entrenadores:")
            nuevo_gimnasio = [[contrincante.name, 0, 0] for contrincante in self.trainers]
            jugador.batallas[self.city_name] = nuevo_gimnasio
            beated_trainers = 0

        else:
            print("Bienvenido! Veo que no es la primera vez que pasas por aqui.\nHas ganado a:")
            beated_trainers = 0
            for batalla in jugador.batallas[self.city_name]:
                if batalla[1] != 0:
                    beated_trainers += 1
                    print(batalla[0])

        if beated_trainers == jugador.batallas[self.city_name]:
            print("Felicitaciones! Le has ganado a todos los entrenadores, es tu turno de enfrentarte al lider.")
            batalla_lider = Batalla(self.city_name, jugador, self.leader, jugador.equipo,
                                    self.leader.programon_squad, False)


        else:
            print(" ~ Trainers ~ ")
            display = "\n".join("[{}]: {}".format(i + 1, self.trainers[i]) for i in range(len(self.trainers)))
            print(display)

            contrincante = input("Escoge un entrenador para comenzar la batalla: ")
            while True:
                contrincante = input("Escoge un entrenador para comenzar la batalla: ")
                if contrincante.isdigit():
                    if int(contrincante)-1 not in range(len(self.trainers)):
                        print("Ingrese un numero de entrenador valido")
                    else:
                        break  # RR
                else:
                    print("Ingrese el numero del entrenador a batallar")

            batalla_trainer= Batalla(self.city_name, jugador, self.trainer[contrincante - 1], jugador.equipo,
                                     self.trainer[contrincante - 1].programon_squad, False)







