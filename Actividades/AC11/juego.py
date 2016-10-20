import os
import random

class Juego:

    def __init__(self):
        b = os.listdir("cartas")
        c = os.listdir("cartas")
        self.jugador1=b
        self.jugador2=c
        self.jugador1.remove("jugador_1.png")
        self.jugador1.remove("jugador_2.png")
        self.jugador2.remove("jugador_1.png")
        self.jugador2.remove("jugador_2.png")
        self.cartas = ['ace','2','3','4','5','6','7','8','9','10','jack','queen','king']
        self.num = 0
        self.carta_actual = self.cartas[0]
        self.ultima_carta = None
        self.pozo = []

    def saca_jugador1(self):
        if self.carta_actual == 'king':
            self.carta_actual= self.cartas[0]
            self.num=0
        else:
            self.num+=1
            self.carta_actual = self.cartas[self.num]
        carta = random.choice(self.jugador1)
        self.jugador1.remove(carta)
        self.ultima_carta = carta
        self.pozo.append(carta)
        if len(self.jugador1)>0:
            return carta
        else:
            return True

    def saca_jugador2(self):
        if self.carta_actual == 'king':
            self.carta_actual= self.cartas[0]
            self.num=0
        else:
            self.num+=1
            self.carta_actual = self.cartas[self.num]
        carta = random.choice(self.jugador2)
        self.jugador2.remove(carta)
        self.ultima_carta = carta
        self.pozo.append(carta)
        if len(self.jugador2)>0:
            return carta
        else:
            return True

    def compara_jugador1(self):
        if self.carta_actual in self.ultima_carta or 'joker' in self.ultima_carta:
            for carta in self.pozo:
                self.jugador2.append(carta)
            self.pozo=[]
            self.carta_actual = 'ace'
            self.num = 0
            return True
        else:
            for carta in self.pozo:
                self.jugador1.append(carta)
            self.pozo=[]
            self.carta_actual = 'ace'
            self.num = 0
            return False

    def compara_jugador2(self):
        if self.carta_actual in self.ultima_carta or 'joker' in self.ultima_carta:
            for carta in self.pozo:
                self.jugador1.append(carta)
            self.pozo=[]
            self.carta_actual = 'ace'
            self.num = 0
            return True
        else:
            for carta in self.pozo:
                self.jugador2.append(carta)
            self.pozo=[]
            self.carta_actual = 'ace'
            self.num = 0
            return False