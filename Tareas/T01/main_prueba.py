# programa principal (primer intento) RR
# Isidora Vizcaya - Tarea 01 - IIC2233
# todos los imports
import sys


# todas las instanciaciones necesarias
# antes de ingresar al sistema
print("Bienvenido a Programón Rojo")  # mayor produccion RR
programonRojo = ProgramonRojo()
game_running = False

while not game_running:
    ingreso = input("[1] Log In\n[2] Sign Up\n >")
    if ingreso.isdigit():
        if ingreso == "1":
            # jugador ya registrado
            programonRojo.log_in()
            game_running = True
        elif ingreso == "2":
            # nuevo jugador
            programonRojo.sign_up()
            game_running = True
        else:
            print("Ingrese una opción válida")
    else:
        print("Ingrese una opción válida")

if game_running:
    # inicializo el PC
    PC = PCBastian(programonRojo)

    pass
else:
    sys.exit()

# se tiene la variable programonRojo.player como instancia de la clase Jugador

