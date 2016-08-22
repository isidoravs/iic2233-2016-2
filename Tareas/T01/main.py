# Isidora Vizcaya - Tarea 01 - IIC2233
import sys
from programonRojo import ProgramonRojo, PCBastian, Menu


print("Bienvenido a Programón Rojo")
programon_rojo = ProgramonRojo()
PC = PCBastian(programon_rojo)

game_running = False
while not game_running:
    ingreso = input("[1] Log In\n[2] Sign Up\n[3] Salir\n >")
    if ingreso.isdigit():
        if ingreso == "1":
            # jugador ya registrado
            programon_rojo.log_in()
            game_running = True
        elif ingreso == "2":
            # nuevo jugador
            programon_rojo.sign_up(PC)
            game_running = True
        elif ingreso == "3":
            sys.exit()
        else:
            print("Ingrese una opcion valida")
    else:
        print("Ingrese una opcion valida")

menu = Menu(programon_rojo, PC)
menu.run()
