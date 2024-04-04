import cv2
import random
import SeguimientoDeManos as sm
import os
import imutils
import logging

# Configurar el nivel de registro y obtener el logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Declaracion de variables
fs = False
fu = False
fd = False
fj = False
fr = False
fgia = False
fgus = False
femp = False
fder = False
fizq = False
conteo = 0

# Accedemos a la carpeta
path = 'imagenes'
images = []
clases = []
lista = os.listdir(path)

try:
    for lis in lista:
        # Leemos las image
        imgdb = cv2.imread(f'{path}/{lis}')
        # Almacenamos imagen
        images.append(imgdb)
        # Almacenamos nombre
        clases.append(os.path.splitext(lis)[0])
    logger.info("Imágenes cargadas correctamente: %d", len(images))
except Exception as e:
    logger.error("Error al cargar las imágenes: %s", e)

# Lectura de la cámara
try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("No se pudo abrir la cámara")
except Exception as e:
    logger.error("Error al abrir la cámara: %s", e)

# Declaramos el detector
try:
    detector = sm.detectormanos(Confdeteccion=0.9)
except Exception as e:
    logger.error("Error al inicializar el detector de manos: %s", e)



# Empezamos
while True:
    try:
        # Lectura de la cámara
        ret, frame = cap.read()
        if not ret:
            raise Exception("No se pudo capturar un frame de la cámara")

        # Extraemos la mitad del frame
        al, an, c = frame.shape
        cx = int(an / 2)
        cy = int(al / 2)

        # Espejo
        frame = cv2.flip(frame, 1)
        cv2.imshow('Frame', frame) ###
        # Encontramos las manos
        frame = detector.encontrarmanos(frame, dibujar=True)
        juego = random.randint(3, 5) 

        # Posiciones manos 1
        lista1, bbbox, jug = detector.encontrarposicion(frame, ManoNum=0, dibujar=True, color=[0, 255, 0])
            # 1 jugador 
        if jug == 1: 
            #dividimos pantalla
            cv2.line(frame, (cx,0), (cx,480),(0,255,0),2)

            #Mostramos jugadores
            cv2.rectangle(frame, (245,25),(380,60),(0,0,0), -1)
            cv2.putText(frame, '1 JUGADOR' ,(250,50), cv2.FONT_HERSHEY_SIMPLEX,0.71,(0,255,0),2)
            t = cv2.waitKey(1)

            #Presiona s 
            if t == 83 or t == 115 or fs == True: 
                # Cambiamos flag s 
                fs = True
                # Obtenemos posicion de la mano 
                if len (lista1) != 0: 
                    # Extraemos coordenadas de dedo indice 
                    x1 , y1 = lista1[9][1:] 

                    #print conteo 
                    # Conteo juego 
                    if conteo <= 2:
                        # Leemos la imagen inicial 
                        #print(name)
                        img = images[conteo]
                        # Redimensinamiento 
                        img = imutils.resize(img, width=240,height=240)
                        ali , ani , c = img.shape

                        #Definimo en que parte de la pantalla esta 
                        # Izquierda 
                        if x1 < cx:
                            # flag lado 
                            fizq = True 
                            fder = False 
                            #Mostramos imagen 
                            frame[130: 130 + ali, 350 : 350 + ani ]= img 
                            #Empezamos conteo 
                            # superamos el umbral 
                            if y1 < cy - 40 and fd == False:
                                fu = True 
                                cv2.circle(frame, (cx , cy), 5, (255,255,0), -1)

                            #bajamos del umbral con flag 
                            elif y1 > cy - 40 and fu == True :
                                conteo = conteo + 1 
                                fu = False
                        
                        # Derecha 
                        elif x1 > cx :
                            #flag lado 
                            fder = True 
                            fizq = False 
                            #Mostramos imagen 
                            frame[130: 130 + ali, 350 : 350 + ani ]= img 
                            #Empezamos conteo 
                            #superamos el umbral 
                            if y1 < cy - 40 and fd == False:
                                fu = True 
                                cv2.circle(frame, (cx , cy), 5, (255,255,0), -1)
                            #bajamos del umbral con flag 
                            elif y1 > cy - 40 and fu == True :
                                conteo = conteo + 1 
                                fu = False

                    #Play 
                    elif conteo == 3:
                        # si no jugamos jugamos 
                        if fj == False and fr == False:
                            # Elegimos piedra papel o tijera 
                            juego = random.randit(3,5)
                            fj = True 
                        
                        #Izquierda 
                        if fizq == True and fder == False : 
                            #Mostramos 
                            img == images[juego]
                            #Redimensionamos 
                            img = imutils.resize(img, width=240 , height=240)
                            ali, ani , c = img.shape
                            # Mostramos la imagen 
                            frame[130:130 + ali, 350 : 350 + ani ] = img 
                            print(juego)

                            #Si ya jugamos 
                            if fj == True and fr == False : 
                                #Extraemos valores 
                                #Punta DI 
                                x2 , y2 = lista1[8][1:]
                                #Punta DM
                                x3 , y3 = lista1[12][1:]
                                #Punta DA
                                x4, y4 = lista1[16][1:]

                                #Falange DI
                                x22 , y22 = lista1[6][1:]
                                #Falange DM
                                x33, y33 = lista1[10][1:] 
                                #Falande DA 
                                x44, y44 = lista1[14][1:]

                                #Condiciones de posicion 
                                #Piedra 
                                if x2 < x22 and x3 < x33 and x4 < x44:
                                    # IA papel 
                                    if juego == 3:
                                        # Gana IA 
                                        print ('GANA LA IA')
                                        #Bandera ganador 
                                        fgia= True
                                        fgus = False 
                                        fmep = False 
                                        fr = True 
                                    #IA piedra 
                                    elif juego == 4: 
                                        # Empate 
                                        print('EMPATE')
                                        # Flags ganador 
                                        fgia= False 
                                        fgus = False 
                                        femp = True 
                                        fr= True 
                                    #IA tijer 
                                    elif juego == 5:
                                        # Gana usuario 
                                        print ('GANASTE')   
                                        #Flags ganador 
                                        fgia = False 
                                        fgus = True 
                                        femp = False 
                                        fr = True 
                                
                                # Papel 
                                elif x2 > x22 and x3 > x33 and x4 > x44:
                                    #IA papel 
                                    if juego == 3:
                                        # EMPATE 
                                        print('EMPATE')
                                        #Flags empate 
                                        fgia= False 
                                        fgus = False 
                                        femp = True 
                                        fr= True 
                                    #IA piedra 
                                    elif juego == 4:
                                        #GANA USUARIO 
                                        print('GANASTE')
                                        #FLAGS WINs 
                                        fgia = False 
                                        fgus = True 
                                        femp = False 
                                        fr = True 
                                    elif juego == 5:
                                        # Pierde usuario 
                                        print('PERDISTE')
                                        fgia= True
                                        fgus = False 
                                        fmep = False 
                                        fr = True 
                                #Tijera
                                elif x2 > x22 and x3 > x33 and x4 < x44:
                                    #IA papel 
                                    if juego == 3:
                                        #Gana usuario 
                                        print('GANASTE')
                                        #FLAGS
                                        fgia = False 
                                        fgus = True 
                                        femp = False 
                                        fr = True
                                    #IA piedra 
                                    elif juego == 4: 
                                        #Gana IA 
                                        print ('PERDISTE')
                                        #Flags
                                        fgia= True
                                        fgus = False 
                                        fmep = False 
                                        fr = True 
                                    elif juego == 5:
                                        # EMPATE 
                                        print('EMPATE')
                                        #Flags empate 
                                        fgia= False 
                                        fgus = False 
                                        femp = True 
                                        fr= True 
                                        
                            # Mostramos ganador 
                            # IA 
                            if fgia == True:
                                #Mostramos 
                                gan = images[6]
                                alig, anig, c = gan.shape 
                                #Mostramos imagen 
                                frame [130: 130 + alig, 180: 180 + anig] = gan 
                                #reset 
                                if t == 82 or t == 114: 
                                    fs = False 
                                    fu = False 
                                    fd = False 
                                    fj = False 
                                    fr = False 
                                    fgia = False 
                                    fgus = False 
                                    femp = False 
                                    fder = False 
                                    fizq = False 
                                    conteo = 0
                            # USUARIO 
                            elif fgus == True :
                                # mostramos 
                                gan = images[7]
                                alig, anig, c = gan.shape 
                                #mostramos imagen 
                                frame [130: 130 + alig, 180: 180 +anig] = gan 

                                #reset 
                                if t == 82 or t == 142:
                                    fs = False 
                                    fu = False 
                                    fd = False 
                                    fj = False 
                                    fr = False 
                                    fgia = False 
                                    fgus = False 
                                    femp = False 
                                    fder = False 
                                    fizq = False 
                                    conteo = 0
                            #EMPATE 
                            elif femp == True:
                                # mostramos
                                gan = images[8]
                                alig, anig, c = gan.shape 
                                #mostramos imagen 
                                frame [130: 130 + alig, 180: 180 +anig] = gan 

                                #reset 
                                if t == 82 or t == 142:
                                    fs = False 
                                    fu = False 
                                    fd = False 
                                    fj = False 
                                    fr = False 
                                    fgia = False 
                                    fgus = False 
                                    femp = False 
                                    fder = False 
                                    fizq = False 
                                    conteo = 0 
                        #Derecha 
                        if fizq == False and fder == True:
                            #Mostramos 
                            img == images [juego]
                            #Redimensionamos 
                            img = imutils.resize(img, width=240 , height=240)
                            ali, ani , c = img.shape
                            # Mostramos la imagen 
                            frame[130:130 + ali, 30 : 30 + ani ] = img 
                            print(juego)

                            #Si ya jugamos 
                            if fj == True and fr== False : 
                                #Extraemos valores 
                                #Punta DI 
                                x2 , y2 = lista1[8][1:]
                                #Punta DM
                                x3 , y3 = lista1[12][1:]
                                #Punta DA
                                x4, y4 = lista1[16][1:]

                                #Falange DI
                                x22 , y22 = lista1[6][1:]
                                #Falange DM
                                x33, y33 = lista1[10][1:] 
                                #Falande DA 
                                x44, y44 = lista1[14][1:]

                                #Condicion de la posicion
                                #Piedra 
                                if x2 > x22 and x3 > x33 and x4 > x44:
                                    # IA papel 
                                    if juego == 3:
                                        # Gana IA 
                                        print ('GANA LA IA')
                                        #Bandera ganador 
                                        fgia= True
                                        fgus = False 
                                        fmep = False 
                                        fr = True 
                                    #IA piedra 
                                    elif juego == 4: 
                                        # Empate 
                                        print('EMPATE')
                                        # Flags ganador 
                                        fgia= False 
                                        fgus = False 
                                        femp = True 
                                        fr= True 
                                    #IA tijer 
                                    elif juego == 5:
                                        # Gana usuario 
                                        print ('GANASTE')   
                                        #Flags ganador 
                                        fgia = False 
                                        fgus = True 
                                        femp = False 
                                        fr = True 
                                # Papel 
                                elif x2 < x22 and x3 < x33 and x4 < x44:
                                    #IA papel 
                                    if juego == 3:
                                        # EMPATE 
                                        print('EMPATE')
                                        #Flags empate 
                                        fgia= False 
                                        fgus = False 
                                        femp = True 
                                        fr= True 
                                    #IA piedra 
                                    elif juego == 4:
                                        #GANA USUARIO 
                                        print('GANASTE')
                                        #FLAGS WINs 
                                        fgia = False 
                                        fgus = True 
                                        femp = False 
                                        fr = True 
                                    elif juego == 5:
                                        # Pierde usuario 
                                        print('PERDISTE')
                                        fgia= True
                                        fgus = False 
                                        fmep = False 
                                        fr = True 
                                #Tijera
                                elif x2 < x22 and x3 < x33 and x4 > x44:
                                    #IA papel 
                                    if juego == 3:
                                        #Gana usuario 
                                        print('GANASTE')
                                        #FLAGS
                                        fgia = False 
                                        fgus = True 
                                        femp = False 
                                        fr = True
                                    #IA piedra 
                                    elif juego == 4: 
                                        #Gana IA 
                                        print ('PERDISTE')
                                        #Flags
                                        fgia= True
                                        fgus = False 
                                        fmep = False 
                                        fr = True 
                                    elif juego == 5:
                                        # EMPATE 
                                        print('EMPATE')
                                        #Flags empate 
                                        fgia= False 
                                        fgus = False 
                                        femp = True 
                                        fr= True
                            # Mostramos ganador 
                            # IA 
                            if fgia == True:
                                #Mostramos 
                                gan = images[6]
                                alig, anig, c = gan.shape 
                                #Mostramos imagen 
                                frame [130: 130 + alig, 180: 180 + anig] = gan 
                                #reset 
                                if t == 82 or t == 114: 
                                    fs = False 
                                    fu = False 
                                    fd = False 
                                    fj = False 
                                    fr = False 
                                    fgia = False 
                                    fgus = False 
                                    femp = False 
                                    fder = False 
                                    fizq = False 
                                    conteo = 0
                            # USUARIO 
                            elif fgus == True :
                                # mostramos 
                                gan = images[7]
                                alig, anig, c = gan.shape 
                                #mostramos imagen 
                                frame [130: 130 + alig, 180: 180 +anig] = gan 

                                #reset 
                                if t == 82 or t == 142:
                                    fs = False 
                                    fu = False 
                                    fd = False 
                                    fj = False 
                                    fr = False 
                                    fgia = False 
                                    fgus = False 
                                    femp = False 
                                    fder = False 
                                    fizq = False 
                                    conteo = 0
                            #EMPATE 
                            elif femp == True:
                                # mostramos
                                gan = images[8]
                                alig, anig, c = gan.shape 
                                #mostramos imagen 
                                frame [130: 130 + alig, 180: 180 +anig] = gan 

                                #reset 
                                if t == 82 or t == 142:
                                    fs = False 
                                    fu = False 
                                    fd = False 
                                    fj = False 
                                    fr = False 
                                    fgia = False 
                                    fgus = False 
                                    femp = False 
                                    fder = False 
                                    fizq = False 
                                    conteo = 0     
        
        
    except Exception as e:
        logger.error("Error durante la ejecución del bucle principal: %s", e)
        # Aquí puedes agregar cualquier otra acción, como enviar una notificación por correo electrónico o guardar un registro de errores en un archivo
