# Importamos las librerías necesarias:
import pygame
import numpy as np
import time

# Para comenzar vamos a crear la pantalla de nuestro juego
pygame.init()

ancho = 1000
largo = 1000

pantalla = pygame.display.set_mode((largo, ancho))

fondo = 255, 0, 0
pantalla.fill(fondo)

# Número de celdas
numceldaX, numceldaY = 50, 50

# Dimensiones de las celdas
dimceldaancho = ancho / numceldaX
dimceldalargo = largo / numceldaY

#iniciamos la matriz en ceros (muertas) con la funcion de numpy np.zeros que nos genera esos ceros

estado = np.zeros((numceldaX, numceldaY))

# Autómata andar

# Control de la ejecución del juego
pausa = False

# Bucle de ejecución
while True:

    # Creamos un copia del gameState sobre la que haremos los cambios,
    # para que se realicen a la vez en cada vuelta del bucle
    nuevoestado = np.copy(estado)

    # Coloreamos la pantalla totalmente de gris cada vuelta.
    pantalla.fill (fondo)

    # Creamos un lapso de tiempo para que se aprecie mejor el movimiento
    time.sleep(0.1)

    # Registramos eventos del teclado y ratón
    eventoRaton = pygame.event.get()
    

            
    for evento in eventoRaton:
        # Detectamos si se presiona una tecla
        if evento.type == pygame.KEYDOWN:
            pausa = not pausa
        # Detectamos si se presiona el ratón
        click = pygame.mouse.get_pressed()

        if sum(click) > 0:
            posicionX, posicionY = pygame.mouse.get_pos()
            celdaX, celdaY = int(np.floor(posicionX / dimceldaancho)), int(np.floor(posicionY / dimceldalargo))
            nuevoestado[celdaX, celdaY] = 1

    for y in range(0, numceldaX):
        for x in range(0, numceldaY):

            if  not pausa:

                # Calculamos el número de vecinos cercanos
                numveci = estado[(x-1) % numceldaX, (y-1) % numceldaY] + \
                          estado[(x)   % numceldaX, (y-1) % numceldaY] + \
                          estado[(x+1) % numceldaX, (y-1) % numceldaY] + \
                          estado[(x-1) % numceldaX, (y)   % numceldaY] + \
                          estado[(x+1) % numceldaX, (y)   % numceldaY] + \
                          estado[(x-1) % numceldaX, (y+1) % numceldaY] + \
                          estado[(x)   % numceldaX, (y+1) % numceldaY] + \
                          estado[(x+1) % numceldaX, (y+1) % numceldaY]

                # Una celda muerta con exactamente 3 vecinas vivas revivirá.
                if estado[x, y] == 0 and numveci == 3:
                    nuevoestado[x, y] = 1

                # Una celda viva con menos de 2 o más de 3 celdas vivas alrededor muere.
                elif estado[x, y] == 1 and (numveci < 2 or numveci > 3):
                    nuevoestado[x, y] = 0

            # Creamos el polígono de cada celda a dibujar
            poligono = [((x) * dimceldaancho, y * dimceldalargo),
                    ((x + 1) * dimceldaancho, y * dimceldalargo),
                    ((x + 1) * dimceldaancho, (y + 1) * dimceldalargo),
                    ((x) * dimceldaancho, (y + 1) * dimceldalargo)]

            # Y dibujamos la celda para cada par de X e Y.
            if nuevoestado[x, y] == 0:
                pygame.draw.polygon(pantalla, (128, 128, 128), poligono, 1)
            else:
                pygame.draw.polygon(pantalla, (255, 255, 255), poligono, 0)

    # Actualizamos el estado del juegos y lo guardamos en la lista bidimensional
    estado = np.copy(nuevoestado)

    # Actualizamos la pantalla
    pygame.display.flip()