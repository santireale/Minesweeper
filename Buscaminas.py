# !/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import sqlite3
import pygame
import random
from wx import *
from wx.dataview import DataViewListCtrl

class Buscaminas(App):

    def OnInit(self):
        self.font = Font(14, 76, 90, 90)
        f = self.f = Frame(None, -1, "BIENVENIDOS A BUSCAMINAS",pos=(-1,-1), size=(700, 300))
        f.Centre(HORIZONTAL|VERTICAL)
        f.SetBackgroundColour(BLACK)
        icono = Icon("carita.jpg")
        f.SetIcon(icono)
        g = self.g = GridBagSizer(1,1)
        fondo1 = Bitmap("fondoDatos.jpg",BITMAP_TYPE_JPEG)
        fondo2 = Bitmap("fondoResultados.jpg",BITMAP_TYPE_JPEG)
        botonIngreso = BitmapButton(f, bitmap=fondo1,size=(340,263))
        botonPuntaje = BitmapButton(f, bitmap=fondo2,size=(340,263))
        botonIngreso.Bind(EVT_BUTTON, self.frameDatos)
        botonPuntaje.Bind(EVT_BUTTON, self.framePuntaje)
        g.Add(botonIngreso, pos=(0,0))
        g.Add(botonPuntaje, pos=(0,1))
        f.SetSizerAndFit(g)
        f.Show()
        return True

    def frameDatos(self,event):
        self.f.Show(False)
        frameDatos = self.frameDatos = Frame(None, -1, "", size=(250, 450),style=(CAPTION))
        frameDatos.Centre(HORIZONTAL|VERTICAL)
        frameDatos.SetBackgroundColour(BLACK)
        panelDatos = self.panelDatos = Panel(frameDatos)
        gridDatos = self.gridDatos = GridBagSizer(3, 5)
        ## Jugador
        cCaract = self.cCaract = StaticText(panelDatos,-1,"Max 7 caracteres")
        cCaract.SetForegroundColour(WHITE)
        tJugador = self.tJugador = StaticText(panelDatos, -1, "JUGADOR:")
        tJugador.SetFont(self.font)
        tJugador.SetForegroundColour(WHITE)
        gridDatos.Add(tJugador, pos=(0, 4), flag=ALIGN_CENTER_HORIZONTAL)
        cJugador = self.cJugador = TextCtrl(panelDatos, -1, "", (50, 50), (115, -1))
        gridDatos.Add(cJugador, pos=(1, 4))
        gridDatos.Add(cCaract, pos=(2,4),flag=ALIGN_CENTER_HORIZONTAL)
        ## Dimensiones
        tDimen = self.tDimen = StaticText(panelDatos, -1, "DIMENSION:")
        tDimen.SetFont(self.font)
        tDimen.SetForegroundColour(WHITE)
        gridDatos.Add(tDimen, pos=(4, 4), flag=ALIGN_CENTER_HORIZONTAL)
        dimenList = ["10x10", "15x15", "20x20"]
        dimen = self.dimen = ComboBox(panelDatos, 200, "", (50, 50), (115, -1), dimenList,CB_DROPDOWN | TE_PROCESS_ENTER)
        gridDatos.Add(dimen, pos=(5, 4))
        ## Minas Cantidad
        cant10=StaticText(panelDatos, -1, "10x10 - Min: 1 Max: 99")
        cant10.SetForegroundColour(WHITE)
        cant15=StaticText(panelDatos, -1, "15x15 - Min: 1 Max: 224")
        cant15.SetForegroundColour(WHITE)
        cant20=StaticText(panelDatos, -1, "20x20 - Min: 1 Max: 399")
        cant20.SetForegroundColour(WHITE)
        tMinas = self.tMinas = StaticText(panelDatos, -1, "MINAS:")
        tMinas.SetFont(self.font)
        tMinas.SetForegroundColour(WHITE)
        gridDatos.Add(tMinas, pos=(7, 4), flag=ALIGN_CENTER_HORIZONTAL)
        cMinas = self.cMinas = TextCtrl(panelDatos, -1, "", (50, 50), (115, -1))
        gridDatos.Add(cMinas, pos=(8, 4))
        gridDatos.Add(cant10, pos=(9, 4),flag=ALIGN_CENTER_HORIZONTAL)
        gridDatos.Add(cant15, pos=(10, 4),flag=ALIGN_CENTER_HORIZONTAL)
        gridDatos.Add(cant20, pos=(11, 4),flag=ALIGN_CENTER_HORIZONTAL)
        ## Botones
        imgAceptar = Bitmap("aceptarDatos.jpg",BITMAP_TYPE_JPEG)
        b_aceptar = BitmapButton(panelDatos, bitmap=imgAceptar, size=(115, 45))
        imgCancelar = Bitmap("cancelarDatos.jpg",BITMAP_TYPE_JPEG)
        b_cancelar = BitmapButton(panelDatos,bitmap=imgCancelar,size=(115, 45))
        gridDatos.Add(b_aceptar, pos=(13, 4))
        gridDatos.Add(b_cancelar, pos=(14, 4))
        b_aceptar.Bind(EVT_BUTTON, self.aceptarDatos)
        b_cancelar.Bind(EVT_BUTTON, self.cancelarDatos)
        panelDatos.SetSizer(gridDatos)
        frameDatos.Show()
        return True

    def framePuntaje(self,event):
        framePuntajes = self.framePuntajes = Frame (None, -1, "Puntajes", size=(1140,500))
        framePuntajes.Centre(HORIZONTAL|VERTICAL)
        icono = Icon("carita.jpg")
        framePuntajes.SetIcon(icono)
        panelPuntajes = self.panelPuntajes = Panel(framePuntajes, -1)
        dvlcPuntajes10 = self.dvlcPuntajes10 = DataViewListCtrl(panelPuntajes)
        dvlcPuntajes15 = self.dvlcPuntajes15 = DataViewListCtrl(panelPuntajes)
        dvlcPuntajes20 = self.dvlcPuntajes20 = DataViewListCtrl(panelPuntajes)
        encabezado = [('ID', 25),('Jugador', 100),('Dimension', 85),('Minas', 80),('Minutos', 80)]
        for enca in encabezado:
            dvlcPuntajes10.AppendTextColumn(enca[0], width=enca[1], align=ALIGN_CENTER)
            dvlcPuntajes15.AppendTextColumn(enca[0], width=enca[1], align=ALIGN_CENTER)
            dvlcPuntajes20.AppendTextColumn(enca[0], width=enca[1], align=ALIGN_CENTER)
        boxPuntajes = self.boxPuntajes = BoxSizer(HORIZONTAL)
        boxPuntajes.Add(dvlcPuntajes10,1,EXPAND)
        boxPuntajes.Add(dvlcPuntajes15,1,EXPAND)
        boxPuntajes.Add(dvlcPuntajes20,1,EXPAND)
        panelPuntajes.SetSizer(boxPuntajes)
        framePuntajes.Show()
        try:
            self.cargarDVLC(self)
        except:
            pass
        return True

    def cargarDVLC(self,event):
        def cargarDVLC10(self):
            try:
                con = sqlite3.connect("puntaje10.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM puntajes")
                ROWS = cur.fetchall()
                for ROW in ROWS:
                    self.dvlcPuntajes10.AppendItem([ROW[0], ROW[1],ROW[2], ROW[3],ROW[4]])
                con.commit()
                con.close()
            except:
                pass
            return True
        def cargarDVLC15(self):
            try:
                con = sqlite3.connect("puntaje15.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM puntajes")
                ROWS = cur.fetchall()
                for ROW in ROWS:
                    self.dvlcPuntajes15.AppendItem([ROW[0], ROW[1],ROW[2], ROW[3],ROW[4]])
                con.commit()
                con.close()
            except:
                pass
            return True
        def cargarDVLC20(self):
            try:
                con = sqlite3.connect("puntaje20.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM puntajes")
                ROWS = cur.fetchall()
                for ROW in ROWS:
                    self.dvlcPuntajes20.AppendItem([ROW[0], ROW[1],ROW[2], ROW[3],ROW[4]])
                con.commit()
                con.close()
            except:
                pass
            return True
        cargarDVLC10(self)
        cargarDVLC15(self)
        cargarDVLC20(self)
        return True

    def agregarResultado(self, event):
        dimen = self.dimen.GetValue()
        minas = self.cMinas.GetValue()
        nom = self.cJugador.GetValue()
        tiem = float(self.tiempoFinal - self.tiempoInicial)
        if tiem>=0.60:
            min=tiem/60
            seg=tiem-(60*min)
            min=str(min)
            seg=str(seg)
            tiem=min+seg
        else:
            tiem=tiem/60
        tiem = str(tiem)
        tiem=tiem[0:4]
        def agregar10(n, d, m, t):
            con = sqlite3.connect("puntaje10.db")
            cur = con.cursor()
            try:
                cur.execute("CREATE TABLE puntajes(Id INTEGER PRIMARY KEY, Jugador TEXT, Dimension TEXT,  Minas INTEGER, Tiempo TEXT)")
                cur.execute("INSERT INTO puntajes(Jugador, Dimension, Minas, Tiempo) VALUES (?,?,?,?)", (n, d, m, t))
            except:
                cur.execute("INSERT INTO puntajes(Jugador, Dimension, Minas, Tiempo) VALUES (?,?,?,?)", (n, d, m, t))
            con.commit()
            con.close()
            return True
        def agregar15(n, d, m, t):
            con = sqlite3.connect("puntaje15.db")
            cur = con.cursor()
            try:
                cur.execute("CREATE TABLE puntajes(Id INTEGER PRIMARY KEY, Jugador TEXT, Dimension TEXT,  Minas INTEGER, Tiempo TEXT)")
                cur.execute("INSERT INTO puntajes(Jugador, Dimension, Minas, Tiempo) VALUES (?,?,?,?)", (n, d, m, t))
            except:
                cur.execute("INSERT INTO puntajes(Jugador, Dimension, Minas, Tiempo) VALUES (?,?,?,?)", (n, d, m, t))
            con.commit()
            con.close()
            return True
        def agregar20(n, d, m, t):
            con = sqlite3.connect("puntaje20.db")
            cur = con.cursor()
            try:
                cur.execute("CREATE TABLE puntajes(Id INTEGER PRIMARY KEY, Jugador TEXT, Dimension TEXT,  Minas INTEGER, Tiempo TEXT)")
                cur.execute("INSERT INTO puntajes(Jugador, Dimension, Minas, Tiempo) VALUES (?,?,?,?)", (n, d, m, t))
            except:
                cur.execute("INSERT INTO puntajes(Jugador, Dimension, Minas, Tiempo) VALUES (?,?,?,?)", (n, d, m, t))
            con.commit()
            con.close()
            return True
        if dimen == '10x10':
            agregar10(nom,dimen,minas,tiem)
        else:
            if dimen == '15x15':
                agregar15(nom, dimen, minas, tiem)
            else:
                if dimen == '20x20':
                    agregar20(nom, dimen, minas, tiem)
        return True

    def definirValores(self):
        dim = self.dimen.GetValue()
        if dim == "10x10":
            self.dimen_Matriz = 10
            self.dimen_Pantalla = [255, 255]
        else:
            if dim == "15x15":
                self.dimen_Matriz = 15
                self.dimen_Pantalla = [380, 380]
            else:
                if dim == "20x20":
                    self.dimen_Matriz = 20
                    self.dimen_Pantalla = [505, 505]
        return True

    def verificarNumeroMinas(self,event):
        s=False
        minas=0
        try:
            minas = int(self.cMinas.GetValue())
            dim = self.dimen.GetValue()
            if dim == "10x10":
                self.cant = 99
            elif dim == "15x15":
                self.cant = 224
            elif dim == "20x20":
                self.cant = 399
            if (minas >= 1) and (minas <= self.cant):
                s = True
        except:
            s=False
            pass
        return s

    def verificarDimensiones(self,event):
        s=False
        dim=''
        try:
            dim = self.dimen.GetValue()
            if dim=='10x10' or dim=='15x15' or dim=='20x20':
                s=True
        except:
            s=False
            pass
        return s

    def verificarNombre(self,event):
        s=False
        n=''
        try:
            n= self.cJugador.GetValue()
            if n!='' and len(n)<=7:
                s=True
        except:
            pass
        return s

    def cancelarDatos(self,event):
        self.frameDatos.Close()
        self.f.Show()
        return True

    def aceptarDatos(self,event):
        if self.verificarDimensiones(self) and self.verificarNumeroMinas(self) and self.verificarNombre(self):
            self.frameDatos.Show(False)
            self.definirValores()
            self.pantallaDeJuego()
        return True

    ## ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ wx

    def randomMinas(self): ## Genera coordenadas aleatorias y coloca las minas en la grilla logica
        c=0
        cant=int(self.cMinas.GetValue())
        while c<cant:
            i = random.randint(0, int(self.dimen_Matriz)-1)
            j = random.randint(0, int(self.dimen_Matriz)-1)
            if self.grillalogica[i][j] !=10:
                self.grillalogica[i][j] = 10
                c=c+1
        return True

    def crearArray(self,x): # Creacion del array bidimensional
        grid = []
        for fila in range(self.dimen_Matriz):
            grid.append([])
            for columna in range(self.dimen_Matriz):
                grid[fila].append(x)
        return grid

    def colocarValores(self): # Coloca los valores correspondientes a cada celda
        long=int(self.dimen_Matriz)
        for x in range(long):
            for y in range(long):
                if self.grillalogica[x][y] != 10:
                    count = 0
                    for a in [1, 0, -1]:
                        for b in [1, 0, -1]:
                            try:
                                if self.grillalogica[x + a][y + b] == 10:
                                    if (x + a > -1 and y + b > -1):
                                        count += 1
                            except:
                                pass
                    self.grillalogica[x][y] = count
        return True

    def corroborarMinas(self): ## Verificar si el usuario clickeo correctamente en todas las minas
        s=True
        for x in range(self.dimen_Matriz):
            for y in range(self.dimen_Matriz):
                if self.grillalogica2[x][y]==False:
                    s=False
                if self.grillalogica[x][y]!=10 and self.grilla[x][y]==100:
                    s=False
        if s:
            self.juegoTerminado(True)

    ## ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓ pg

    def juegoTerminado(self,log):
        for x in range(self.dimen_Matriz):
            for y in range(self.dimen_Matriz):
                if log == True:
                    if self.grillalogica[x][y] == 10:
                        self.grilla[x][y] = 100
                    else:
                        self.grilla[x][y] = self.determinarNumero(x, y)
                else:
                    self.grilla[x][y] = self.determinarNumero(x, y)
        if log == False:
            if self.dimen_Pantalla[0] == 255:
                imagen = pygame.image.load("perdio10x10.jpg")
            else:
                if self.dimen_Pantalla[0] == 380:
                    imagen = pygame.image.load("perdio15x15.jpg")
                else:
                    if self.dimen_Pantalla[0] == 505:
                        imagen = pygame.image.load("perdio20x20.jpg")
        else:
            self.tiempoFinal = time.time()
            if self.dimen_Pantalla[0] == 255:
                imagen = pygame.image.load("gano10x10.jpg")
            else:
                if self.dimen_Pantalla[0] == 380:
                    imagen = pygame.image.load("gano15x15.jpg")
                else:
                    if self.dimen_Pantalla[0] == 505:
                        imagen = pygame.image.load("gano20x20.jpg")
            self.agregarResultado(self)
        imagen = imagen.convert()
        self.pantalla.blit(imagen, (0,0))
        pygame.display.flip()  # Actualizamos la pantalla con lo dibujado.
        lis = False
        while not lis:
            for evento in pygame.event.get():
                if evento.type==pygame.MOUSEBUTTONDOWN:
                    lis = True
        self.pantalla.fill(BLACK)
        self.permitirClick = False
        return True

    def dibujarPantalla(self):
        for fila in range(self.dimen_Matriz):  # Pinta celda = Rejilla
            for columna in range(self.dimen_Matriz):
                imagen = pygame.image.load("transparente.jpg") ## IMG 0 ---
                if self.grilla[fila][columna] == 1:
                    imagen = pygame.image.load("uno.jpg")
                    ##IMG 1 -----------------------------------------
                elif self.grilla[fila][columna] == 2:
                    imagen = pygame.image.load("dos.jpg")
                    ##IMG 2 -----------------------------------------
                elif self.grilla[fila][columna] == 3:
                    imagen = pygame.image.load("tres.jpg")
                    ##IMG 3 -----------------------------------------
                elif self.grilla[fila][columna] == 4:
                    imagen = pygame.image.load("cuatro.jpg")
                    ##IMG 4 -----------------------------------------
                elif self.grilla[fila][columna] == 5:
                    imagen = pygame.image.load("cinco.jpg")
                    ##IMG 5 -----------------------------------------
                elif self.grilla[fila][columna] == 6:
                    imagen = pygame.image.load("seis.jpg")
                    ##IMG 6 -----------------------------------------
                elif self.grilla[fila][columna] == 7:
                    imagen = pygame.image.load("siete.jpg")
                    ##IMG 7 -----------------------------------------
                elif self.grilla[fila][columna] == 8:
                    imagen = pygame.image.load("ocho.jpg")
                    ## IMG 8 -----------------------------------------
                elif self.grilla[fila][columna] == 9:
                    imagen = pygame.image.load("negro.jpg")
                    ## IMG 0 -----------------------------------------
                elif self.grilla[fila][columna] == 10:
                    imagen = pygame.image.load("diez.jpg")
                    ## IMG 10 -----------------------------------------
                elif self.grilla[fila][columna] == 100:
                    imagen = pygame.image.load("bandera.jpg")
                    ## IMG B -----------------------------------------
                imagen = imagen.convert()
                self.pantalla.blit(imagen, (columna * 25 + 5, fila * 25 + 5))
        pygame.display.flip()  # Actualizamos la pantalla con lo dibujado.

    def determinarNumero(self,fila,colum):
        num=-1
        if self.grillalogica[fila][colum] == 0:
            num=9
        elif self.grillalogica[fila][colum] == 1:
            num=1
        elif self.grillalogica[fila][colum] == 2:
            num=2
        elif self.grillalogica[fila][colum] == 3:
            num=3
        elif self.grillalogica[fila][colum] == 4:
            num=4
        elif self.grillalogica[fila][colum] == 5:
            num=5
        elif self.grillalogica[fila][colum] == 6:
            num=6
        elif self.grillalogica[fila][colum] == 7:
            num=7
        elif self.grillalogica[fila][colum] == 8:
            num=8
        elif self.grillalogica[fila][colum] == 9:
            num=9
        elif self.grillalogica[fila][colum] == 10:
            num=10
        elif self.grillalogica[fila][colum] == 100:
            num=100
        return num

    def verificarPos(self,num,fil,col): ##num, numero de click 1-izq 3-der
        max = int(self.dimen_Matriz) - 1
        if num==1:
            if self.grillalogica[fil][col] == 0:
                self.grillalogica[fil][col] = self.determinarNumero(fil, col)
                self.grillalogica2[fil][col] = True
                if (fil == 0) or (col == 0) or (fil == max) or (col == max):
                    if fil == 0 and col == 0:
                        for x in [0, 1]:
                            for y in [0, 1]:
                                if self.grilla[fil+x][col+y]!=100:
                                    self.grilla[fil + x][col + y] = self.determinarNumero(fil + x, col + y)
                                    self.grillalogica2[fil + x][col + y] = True
                                    self.verificarPos(1, fil + x, col + y)
                    else:
                        if fil == 0 and col == max:
                            for x in [0, 1]:
                                for y in [-1, 0]:
                                    if self.grilla[fil + x][col + y] != 100:
                                        self.grilla[fil + x][col + y] = self.determinarNumero(fil + x, col + y)
                                        self.grillalogica2[fil + x][col + y] = True
                                        self.verificarPos(1, fil + x, col + y)
                        else:
                            if fil == max and col == 0:
                                for x in [-1, 0]:
                                    for y in [0, 1]:
                                        if self.grilla[fil + x][col + y] != 100:
                                            self.grilla[fil + x][col + y] = self.determinarNumero(fil + x, col + y)
                                            self.grillalogica2[fil + x][col + y] = True
                                            self.verificarPos(1, fil + x, col + y)
                            else:
                                if fil == max and col == max:
                                    for x in [-1, 0]:
                                        for y in [-1, 0]:
                                            if self.grilla[fil + x][col + y] != 100:
                                                self.grilla[fil + x][col + y] = self.determinarNumero(fil + x, col + y)
                                                self.grillalogica2[fil + x][col + y] = True
                                                self.verificarPos(1, fil + x, col + y)
                                else:
                                    if fil == 0:
                                        for x in [0, 1]:
                                            for y in [-1, 0, 1]:
                                                if self.grilla[fil + x][col + y] != 100:
                                                    self.grilla[fil + x][col + y] = self.determinarNumero(fil + x, col + y)
                                                    self.grillalogica2[fil + x][col + y] = True
                                                    self.verificarPos(1, fil + x, col + y)
                                    else:
                                        if col == 0:
                                            for x in [-1, 0, 1]:
                                                for y in [0, 1]:
                                                    if self.grilla[fil + x][col + y] != 100:
                                                        self.grilla[fil + x][col + y] = self.determinarNumero(fil + x,col + y)
                                                        self.grillalogica2[fil + x][col + y] = True
                                                        self.verificarPos(1, fil + x, col + y)
                                        else:
                                            if fil == max:
                                                for x in [-1, 0]:
                                                    for y in [-1, 0, 1]:
                                                        if self.grilla[fil + x][col + y] != 100:
                                                            self.grilla[fil + x][col + y] = self.determinarNumero(fil + x,
                                                                                                              col + y)
                                                            self.grillalogica2[fil + x][col + y] = True
                                                            self.verificarPos(1, fil + x, col + y)
                                            else:
                                                if col == max:
                                                    for x in [-1, 0, 1]:
                                                        for y in [-1, 0]:
                                                            if self.grilla[fil + x][col + y] != 100:
                                                                self.grilla[fil + x][col + y] = self.determinarNumero(fil + x, col + y)
                                                                self.grillalogica2[fil + x][col + y] = True
                                                                self.verificarPos(1, fil + x, col + y)
                    self.corroborarMinas()
                else:
                    for x in [-1, 0, 1]:
                        for y in [-1, 0, 1]:
                            if self.grilla[fil + x][col + y] != 100:
                                self.grilla[fil + x][col + y] = self.determinarNumero(fil + x, col + y)
                                self.grillalogica2[fil + x][col + y] = True
                                self.verificarPos(1, fil + x, col + y)
                    self.corroborarMinas()
            else:
                if self.grillalogica[fil][col] == 10:
                    self.juegoTerminado(False)
        else:
            if self.grilla[fil][col] == 0:
                self.grillalogica2[fil][col] = False
            else:
                self.grillalogica2[fil][col] = True
        self.corroborarMinas()
        return True

    def pantallaDeJuego(self):
        pygame.init()## Inicio pygame
        self.dimen_Celda = 20 ##Tamaño de las celdas
        self.margen = 5 ## Margen entre las celdas
        self.permitirClick = True ## Permite al usuario interactuar con la pantalla antes de que gane/pierda
        self.grilla = self.crearArray(0) # Creo grilla que se muestra en la pantalla
        self.grillalogica = self.crearArray(0) # Creo grilla que almacena los valores
        self.grillalogica2 = self.crearArray(False) # Creo grilla que almacena VoF segun si se tocó o no la celda
        self.randomMinas() # Creo lista con coordenada aleatorias
        self.colocarValores() # Asigno (en grilla logica) la cantidad de minas que esta tocando cada celda
        self.pantalla = pygame.display.set_mode(self.dimen_Pantalla)  # LARGO y ALTO de la pantalla
        pygame.display.set_caption("Buscaminas")  # Título de la pantalla.
        self.hecho = False  # Iteramos hasta que el usuario pulse el botón de salir.
        # -------- Programa principal de pygame -----------
        self.dibujarPantalla()
        self.tiempoInicial = time.time()
        while not self.hecho:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.hecho = True
                else:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if self.permitirClick == True:
                            pos = pygame.mouse.get_pos()  # Obtiene posición presionada por el usuario.
                            columna = pos[0] // (self.dimen_Celda + self.margen)  # Cambio coordenada x de la pantalla por coordenadas reticulares
                            fila = pos[1] // (self.dimen_Celda + self.margen)  # Cambio coordenada y de la pantalla por coordenadas reticulares
                            if evento.button == 1: ## Click 1 - Click izquierdo
                                if self.grillalogica2[fila][columna] == False:
                                    self.grilla[fila][columna] = self.determinarNumero(fila,columna)
                                    self.grillalogica2[fila][columna] = True
                                    self.verificarPos(1, fila, columna)
                            if evento.button == 3: ## Click 3 - Click Derecho
                                    if self.grillalogica2[fila][columna] == False:
                                        self.grilla[fila][columna] = 100
                                    else:
                                        if self.grilla[fila][columna] == 100:
                                            self.grilla[fila][columna] = 0
                                    self.verificarPos(2, fila, columna)
                            self.dibujarPantalla()
        pygame.quit()
        self.frameDatos.Close()
        self.f.Show()

a=Buscaminas()
a.MainLoop()