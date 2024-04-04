# Importamos las librerias 
import math 
import cv2 
import mediapipe as mp 
import time 


#---------- creamos una clase ------
class detectormanos():
    #-----inicializamos los parametros de la funcion ---  
    def __init__(self, mode= False, maxManos=2, model_complexity=1, Confdeteccion=0.5, Confsegui = 0.5):
        self.mode = mode 
        self.maxManos = maxManos
        self.compl = model_complexity
        self.Confdeteccion = Confdeteccion
        self.Confsegui = Confsegui
    #---- creamos los objetos que detectaran las manos y las dibujaran 
        self.mpmanos = mp.solutions.hands
        self.manos = self.mpmanos.Hands(self.mode, self.maxManos, self.compl, self.Confdeteccion, self.Confsegui)
        self.dibujo = mp.solutions.drawing_utils
        self.tip=[4,8,16,20]
#----------Funcion para encontrar las manos -----------------
    def encontrarmanos (self, frame, dibujar = True):
        imgcolor = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
        self.resultados = self.manos.process(imgcolor)

        if self.resultados.multi_hand_landmarks:
            for mano in self.resultados.multi_hand_landmarks:
                if  dibujar : 
                    self.dibujo.draw_landmarks(frame, mano, self.mpmanos.HAND_CONNECTIONS)
        return frame 
#----------- Funcion para encontrar la posicion --------
    def encontrarposicion (self, frame , ManoNum = 0 , dibujar = True, color = [] ): 
        xlista=[]
        ylista=[]
        bbox=[]
        player = 0 
        self.lista = []
        if self.resultados.multi_hand_landmarks:
            miMano = self.resultados.multi_hand_landmarks[ManoNum]
            prueba = self.resultados.multi_hand_landmarks
            player = len(prueba)
            #printplayer 
            for id, lm in enumerate(miMano.landmark):
                alto, ancho , c = frame.shape 
                cx, cy = int (lm.x * ancho ) , int (lm.y * alto )
                xlista.append(cx)
                ylista.append(cy)
                self.lista.append([id, cx, cy])
                if dibujar :
                    cv2.circle(frame,(cx, cy), 3,(0, 0, 0), cv2.FILLED)
        
            xmin, xmax = min(xlista), max(xlista)
            ymin, ymax = min(ylista), max(ylista)
            bbox = xmin, ymin, xmax, ymax
            if dibujar:
                cv2.rectangle(frame,(xmin - 20 , ymin -20), (xmax - 20 , ymax -20 ), color , 2)
        return self.lista, bbox, player      