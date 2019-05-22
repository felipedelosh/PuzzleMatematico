"""
@FelipedelosH


5/17/2019

Juego de ordenamiento de numeros:

Sea una matrix de 3x3 se busca que se ordene de la siguiente manera:

123
8 4
765
"""

from tkinter import *
from random import sample

class SW:
    def __init__(self):
        self.pantalla = Tk()
        # Se declara el lugar donde se pintan los elementos
        # Se declara el lugar donde se llaman los eventos
        self.tela = Canvas(self.pantalla, width=640, height=480, bg="snow")
        self.btnAyuda = Button(self.tela,
         text="?",
          bg="green",
           command= lambda : self.mostrarMensaje('Ayuda', 'Intenta hacer esto:\n\n\n123\n8  4\n765'))
        self.btnEmpezar = Button(self.tela, text="Empezar!!!", bg='red', command=self.empezarJuego)
        self.btnvolverEmpezar = Button(self.tela, text="Otra Vez!!!", bg="red", command=self.restart)
        
        # Aqui se organizaran de manera aleatoria los numeros
        self.temp = []
        # Esto es lo que se quiere lograr
        self.estadoFinal = [1,2,3,8,0,4,7,6,5]
        # Aqui estan contenidos la casi matrix donde se pintan los numeros
        self.tablero = []
        self.mostrarContenido()
        

    def mostrarContenido(self):
        # Se configura la pantalla principal
        self.pantalla.title("Puzzle by loko")
        self.pantalla.geometry("640x480")
        # se pintan los elementos del juego
        self.tela.place(x=0, y=0)
        self.btnAyuda.place(x=600, y=20)
        self.btnEmpezar.place(x=250, y=200)
        # Se vincula la self.tela con el evento de presionar el teclado
        self.tela.bind_all("<Key>",self.press_key)
        # Se pinta la pantalla principal
        self.pantalla.mainloop()

    def empezarJuego(self):
        # Ordeno de forma aleatorea en temp
        self.temp = []
        self.temp = sample(self.estadoFinal, k=len(self.estadoFinal))
        # procedo a ocultar el botom de empezar partida
        self.btnEmpezar.place_forget()
        # Procedo a colocar el boton de re-start
        self.btnvolverEmpezar.place(x=10, y=10)
        # procedo a pintar el tablero
        # limpio el tablero primero
        self.tablero = []
        self.tela.delete(ALL)
        # Se declara un auxiliar para reccorrer los numeros alearoreos
        aux = 0
        # Procedo a pintar los rectangulos
        for i in range(0, 3):
            for j in range(0, 3):
                x0 = 150 + ((j)*100)
                y0 = 90 + (i*100)
                x1 = x0 + 100
                y1 = y0 + 100
                self.tela.create_rectangle(x0, y0, x1, y1)
                # Se agrega la posicion de los numeros que se van a pintar
                self.tablero.append((self.temp[aux], x0, y0))
                aux = aux + 1

        # En este momentos los rectangulos y la matrix han sido pintados
        # Se procede a pintar los numeros
        self.pintarNumeros()

    def pintarNumeros(self):
        # i (#nro, posx, posy)
        # Procedo a ponerles un id *numero*
        # Procedo a pintar los numeros
        for i in self.tablero:
            # No se debe de pintar el 0
            if i[0] != 0:
                self.tela.create_text(i[1]+50, i[2]+50, text=str(i[0]), tags="numero")
            else:
                self.tela.create_text(i[1]+50, i[2]+50, text='0', tags="numero", state=HIDDEN)

    def restart(self):
        self.empezarJuego()


    def actualizarNumeros(self):
        for i in self.tela.find_withtag("numero"):
            # Capture todos los items que contienen numeros
            # procedo a tomar el item i y asignarlo a donde corresponde x,y
            for xy in self.tablero:
                if str(xy[0]) == str(self.tela.itemcget(i, 'text')):
                    self.tela.coords(i, xy[1]+50, xy[2]+50)

    def mostrarMensaje(self, titulo, texto):
        # Se define una ventana emergente
        poppup = Toplevel()
        poppup.title(titulo)
        msg = Message(poppup, text=texto)
        msg.place(x=20, y=20)

    
    # AL presionar se desata el evento
    def press_key(self, event):
        """Mover UP"""
        if str(event.keysym) == "Up":
            if self.puedoMover("00"):
                self.intercambio("00")
        """Mover DOWN"""
        if str(event.keysym) == "Down":
            if self.puedoMover("10"):
                self.intercambio("10")
        """Mover RI"""
        if str(event.keysym) == "Right":
            if self.puedoMover("01"):
                self.intercambio("01")
        """Mover LEFT"""
        if str(event.keysym) == "Left":
            if self.puedoMover("11"):
                self.intercambio("11")

        # Se hizo el intercabio procede actualizarse
        self.actualizarNumeros()
        # Se actualizo porcede a determinarse si esa es la respuesta
        # Borro temporal
        self.temp = []
        # Reconstruyo temp
        for i in self.tablero:
            self.temp.append(i[0])

        if self.temp == self.estadoFinal:
            self.mostrarMensaje('Fin del Juego', 'Ganaste')

    # metodo que verifica si se puede mover.
    # Solo se encarga de buscar en que posicion esta el cero
    # luego de ello que no este en ciertas posiciones
    # mov es de tipo str 00 : up ; 01 : ri ; 10 : down ; 11 : left
    def puedoMover(self, mov):
        # procedo a buscar el cero por fuerza bruta
        donde = 0
        for i in self.tablero:
            if i[0] == 0:
                break
            donde = donde + 1
        """
        [0][1][2]
        [3][4][5]
        [6][7][8]
        """

        if mov == "00":
            return donde < 6

        if mov == "01":
            return donde != 0 and donde != 3 and donde != 6

        if mov == "10":
            return donde > 2

        if mov == "11":
            return donde != 2 and donde != 5 and donde != 8


    # Se procede a buscar el 0 y luego intercambiarlo
    # Nota: ya se comprobo que se podia cambiar
    # mov es de tipo str 00 : up ; 01 : ri ; 10 : down ; 11 : left
    def intercambio(self, mov):
        donde = 0
        for i in self.tablero:
            if i[0] == 0:
                break
            donde = donde + 1
        """
        [0][1][2]
        [3][4][5]
        [6][7][8]
        """
        # Capturo el pivote
        pivote = self.tablero[donde]
        # Declaro el candidato
        candidato = None

        # Para mover arriba solo hay que sumar 3
        if mov == "00":
            candidato = self.tablero[donde + 3]

        # Para mover derecha solo hay que restar 1
        if mov == "01":
            candidato = self.tablero[donde - 1]

        # Para mover abajo solo hay que restar 3
        if mov == "10":
            candidato = self.tablero[donde - 3]

        # Para mover a la izq solo se suma 1
        if mov == "11":
            candidato = self.tablero[donde + 1]

        # Procedo a capturar las posiciones x,y de pivote y candidato
        piv_arg = pivote[0]
        piv_x = candidato[1]
        piv_y = candidato[2]
        can_arg = candidato[0]
        can_x = pivote[1]
        can_y = pivote[2]
        # Reconstruyo xq tupla no soporta asignacion
        pivote = (piv_arg, piv_x, piv_y)
        candidato = (can_arg, can_x, can_y)
        

        # Estoy trabajando con objetos la unica manera es crear obj
        # luego destruir el originar y reemplazarlo
        newObj = []
        for i in self.tablero:
            if i[0] == 0:
                newObj.append(candidato)
            elif i[0] == candidato[0]:
                newObj.append(pivote)
            else:
                newObj.append(i)

        # Destruyo el tablero anterior
        self.tablero = newObj

# Se declara la construccion del sw
sw = SW()