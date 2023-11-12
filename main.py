# Juan González Arranz - T1 - DESLIZATOR (II)
# Archivo principal

import wx
from wx.core import ALIGN_CENTER
import logica
import iconos
import time


class Pantalla(wx.Frame):
    #Define la pantalla principal de la aplicación
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        #Construcción de la interfaz
        self.SetSize((666, 546))
        self.SetMinSize((550,400))
        self.SetTitle(u"DESLIZATOR II")
        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        #Botones
        botones = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(botones, 0, wx.ALL | wx.EXPAND, 5)
        self.button_NEW = wx.Button(self.panel_1, wx.ID_ANY, "Nueva Partida")
        self.button_NEW.SetBitmap(wx.Bitmap(iconos.get_new_icon.GetImage()))
        botones.Add(self.button_NEW, 0, 0, 0)
        self.button_NEW.Disable()   #Deshabilitado hasta que se cargue un fichero
        self.button_OPEN = wx.Button(self.panel_1, wx.ID_ANY, "Abrir Fichero")
        self.button_OPEN.SetBitmap(wx.Bitmap(iconos.get_open_icon.GetImage()))
        botones.Add(self.button_OPEN, 0, 0, 0)
        self.button_SET = wx.Button(self.panel_1, wx.ID_ANY, "Ajustes Tablero")
        self.button_SET.SetBitmap(wx.Bitmap(iconos.get_set_icon.GetImage()))
        botones.Add(self.button_SET, 0, 0, 0)
        self.button_SET.Disable()   #Deshabilitado hasta que se cargue un fichero
        label_2 = wx.StaticText(self.panel_1, wx.ID_ANY, "DESLIZATOR II ~ ©Juan González Arranz", style=wx.ALIGN_RIGHT)
        botones.Add(label_2, 1, wx.ALL, 5)
        #Puntuación / Lista
        area_juego = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(area_juego, 1, wx.ALL | wx.EXPAND, 5)
        informacion = wx.BoxSizer(wx.VERTICAL)
        area_juego.Add(informacion, 0, wx.ALL | wx.EXPAND, 3)
        puntos = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, "Puntos"), wx.HORIZONTAL)
        informacion.Add(puntos, 0, wx.ALL | wx.EXPAND, 0)
        self.pantallaPuntos = wx.TextCtrl(self.panel_1, wx.ID_ANY, "0", style=wx.TE_READONLY)
        puntos.Add(self.pantallaPuntos, 0, 0, 0)
        lista_jugadas = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, "Lista de Jugadas"), wx.HORIZONTAL)
        informacion.Add(lista_jugadas, 1, wx.EXPAND, 0)
        self.historial_jugadas = wx.ListBox(self.panel_1, wx.ID_ANY, choices=[])
        lista_jugadas.Add(self.historial_jugadas, 1, wx.EXPAND, 0)
        #Tablero
        tablero = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, "Tablero"), wx.VERTICAL)
        area_juego.Add(tablero, 1, wx.ALL | wx.EXPAND, 3)
        self.zona_juego = wx.Panel(self.panel_1, wx.ID_ANY)
        tablero.Add(self.zona_juego, 1, wx.EXPAND, 0)
        #Mensaje informativo
        self.mensaje_ayuda = wx.StaticText(self.panel_1, wx.ID_ANY, "Pulse y arrastre el bloque que desea mover")
        sizer_1.Add(self.mensaje_ayuda, 0, wx.ALL, 5)
        self.panel_1.SetSizer(sizer_1)
        self.Layout()

        #Eventos
        self.Bind(wx.EVT_BUTTON, self.on_nueva_partida, self.button_NEW)
        self.Bind(wx.EVT_BUTTON, self.on_abrir_fichero, self.button_OPEN)
        self.Bind(wx.EVT_BUTTON, self.on_abrir_ajustes, self.button_SET)
        self.zona_juego.Bind(wx.EVT_PAINT, self.evento_dibujar)
        self.zona_juego.Bind(wx.EVT_LEFT_DOWN, self.hacer_click)
        self.zona_juego.Bind(wx.EVT_LEFT_UP, self.soltar_click)
        
        #Parámetros de la aplicación
        self.num_filas = 12 #Se asigna el 12 por defecto
        self.COLOR_1 = wx.Brush(wx.Colour("green"))
        self.COLOR_2 = wx.Brush(wx.Colour("blue"))
        self.COLOR_3 = wx.Brush(wx.Colour("red"))
        self.COLOR_FONDO = wx.Brush(wx.Colour((240,240,240)))
        self.LINEA_NEGRO = wx.Pen(wx.Colour("black"))
        self.LINEA_FONDO = wx.Pen(wx.Colour((240,240,240)))
        self.bloquear_click = True  #Usado para omitir los clicks (hay que bloquear la entrada)
        self.tab = None #Tablero. No asignado hasta que no haya un fichero
        self.click_en_zona = False  #True si ha habido un EVT_LEFT_DOWN y no un EVT_LEFT_UP todavía

    def on_nueva_partida(self, event):
        #ENT: Evento cuando se pulsa el botón de "Nuevo"
        #SAL: Abre el diálogo de nueva partida y reinicia el tablero si se ha dado al OK
        with NuevaPartidaDialog(self) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.tab = logica.Tablero(self.fichero, self.num_filas) #Reiniciamos el tablero
                self.tab.insertar_fila()                                #Insertamos la primera fila
                #Reinicio de la partida
                self.historial_jugadas.Clear() 
                self.pantallaPuntos.SetLabel(str(self.tab.puntos))
                self.bloquear_click = False
                self.actualizar_dibujo()

    def on_abrir_fichero(self, event):
        #ENT: Evento cuando se pulsa el botón de "Abrir"
        #SAL: Abre el diálogo de nuevo fichero y lo carga si es adecuado y se ha dado al OK
        with AbrirFicheroDialog(self) as dlg:
            if dlg.ShowModal() == wx.ID_OK: #Ya sabemos que el fichero es adecuado
                self.fichero = dlg.fichero
                self.tab = logica.Tablero(self.fichero, self.num_filas)     #Inicializamos tab
                self.tab.insertar_fila()                                    #Inserción de la primera fila
                #Desbloqueamos los botones - importante para el primer inicio
                self.button_NEW.Enable()
                self.button_SET.Enable()
                #Reinicio de la partida
                self.historial_jugadas.Clear()
                self.pantallaPuntos.SetLabel(str(self.tab.puntos))
                self.bloquear_click = False
                self.actualizar_dibujo()

    def on_abrir_ajustes(self, event):
        #ENT: Evento cuando se pulsa el botón de "Ajustes"
        #SAL: Abre el diálogo de ajustes y cambia el número de filas si se ha dado al OK
        with AjustesTableroDialog(self) as dlg:
            dlg.spin_filas.SetValue(self.num_filas) #Carga del valor actual de filas
            if dlg.ShowModal() == wx.ID_OK:
                if self.num_filas != dlg.spin_filas.GetValue(): #Solo reiniciamos todo si se ha cambiado algo
                    self.num_filas = dlg.spin_filas.GetValue()
                    self.tab = logica.Tablero(self.fichero, self.num_filas)
                    self.tab.insertar_fila()
                    #Reinicio de la partida
                    self.historial_jugadas.Clear()
                    self.pantallaPuntos.SetLabel(str(self.tab.puntos))
                    self.bloquear_click = False
                    self.actualizar_dibujo()

    def evento_dibujar(self, event):
        #ENT: Evento para actualizar el dibujo
        #SAL: Llamada al método para dibujar el tablero (sin animación)
        self.dibujar(wx.PaintDC(self.zona_juego))
    
    def actualizar_dibujo(self):
        #SAL: Llamada al método para dibujar el tablero (sin animación)
        self.dibujar(wx.ClientDC(self.zona_juego))

    def dibujar(self, dc):
        #ENT: El dc en cuestión donde se deba dibujar (depende de si es un evento o una llamada de otra función)
        #SAL: Dibujado del tablero general, sin animación
        if self.tab != None:  #Solo ocurre si ya se ha creado un tablero
            dc.Clear()
            self.ancho_col = dc.GetSize().GetWidth()//10 #Actualiza el valor del ancho de cada columna
            self.alto_fil = dc.GetSize().GetHeight()//(self.num_filas) #Actualiza el valor del alto de cada fila
            for fila in range(self.num_filas):
                ref_y = self.alto_fil*fila
                for bloque in self.tab.datos[fila]:
                    if bloque.color == 0:
                        dc.SetBrush(self.COLOR_1)
                    elif bloque.color == 1:
                        dc.SetBrush(self.COLOR_2)
                    else:
                        dc.SetBrush(self.COLOR_3)
                    ref_x = bloque.col_inic*self.ancho_col
                    dc.DrawRectangle(ref_x, ref_y, self.ancho_col*bloque.longitud, self.alto_fil)

    def fin_partida(self):
        #SAL: Imprime el mensaje de Game Over por todo el tablero, hacia abajo
        #     Cuando llega al fondo se reinicia la animación, solo se para cuando se inicia una nueva partida
        dc = wx.ClientDC(self.zona_juego)
        ref_y = 0
        while self.bloquear_click:  #Se mantiene hasta que se inicie una nueva partida
            self.actualizar_dibujo()
            if ref_y >= dc.GetSize().GetHeight():
                ref_y = 0
            dc.SetBrush(self.COLOR_FONDO)
            dc.DrawRectangle(0,ref_y, dc.GetSize().GetWidth(), 40)
            dc.SetTextForeground((0,0,0))
            dc.SetFont(wx.Font(30, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD))
            dc.DrawLabel("GAME OVER", wx.Rect(0,ref_y, dc.GetSize().GetWidth(), 40), alignment=ALIGN_CENTER)
            ref_y += self.ancho_col
            wx.Yield()
            time.sleep(0.5)

    def hacer_click(self, event):
        #ENT: Evento de apretar click izquierdo
        #SAL: Registra la localización donde se ha apretado el botón
        self.pos_x_0 = event.GetPosition().x
        self.pos_y_0 = event.GetPosition().y
        self.click_en_zona = True

    def soltar_click(self, event):
        #ENT: Evento de soltar el botón izquierdo
        #SAL: Siempre que se pueda procesar la jugada, procede a mover el bloque y a continuar con el resto de fases
        if self.click_en_zona and not self.bloquear_click: #En cualquiera de estos casos hay que omitir el evento
            self.bloquear_click = True #No permite la introducción de más jugadas hasta que no hayamos terminado con esta
            self.click_en_zona = False
            pos_x_1 = event.GetPosition().x
            #Calculamos la entrada como si fuese la versión por teclado
            entrada = chr(self.pos_y_0 // self.alto_fil+ord("A")) + str(self.pos_x_0 // self.ancho_col)
            if pos_x_1 > self.pos_x_0:
                entrada += ">"
            else:
                entrada += "<"
            #Movimiento del bloque
            bandera, col_inicial, bloque = self.tab.jugada(entrada)
            if bandera == -3:
                #Se ha pulsado dentro de la "zona" pero fuera de lo usado para el tablero
                self.bloquear_click = False
                return
            elif bandera == -2:
                self.mensaje_ayuda.SetLabelText("AVISO: El bloque no puede moverse en esa dirección")
                self.bloquear_click = False
                return
            elif bandera == -1: #No hay ningún bloque en ese lugar
                entrada = "---"
            else:
                self.movimiento(col_inicial, bloque)  #Movimiento animado del bloque en cuestión
            self.mensaje_ayuda.SetLabel("Pulse y arrastre el bloque que desea mover") #Se restaura el mensaje informativo
            self.historial_jugadas.Append(entrada)

            seguir = True
            while seguir: #Dejamos caer los bloques y eliminamos filas las veces necesarias
                self.caida()
                seguir = self.tab.eliminacion()
                self.actualizar_dibujo()
                self.pantallaPuntos.SetLabel(str(self.tab.puntos))
        
            if self.tab.lleno(): #Se acabó la partida
                self.fin_partida()
            else:   
                self.tab.insertar_fila()
                self.actualizar_dibujo()
                self.bloquear_click = False
                
    def caida(self):
        #SAL: Calcula los bloques que daben caer, los actualiza y representa la acción con una animación en el tablero
        dc = wx.ClientDC(self.zona_juego)
        for fila in range(self.num_filas-2,-1,-1):
            movimientos = self.tab.caida(fila)  #Lista de listas por cada bloque: [columna0, filaOriginal, filaFinal, longitud, color]
            if len(movimientos)!=0:
                for item in movimientos:    #Transformación de la columna y filas a valores de posición en el panel
                    item[0] *= self.ancho_col
                    item[1] *= self.alto_fil
                    item[2] *= self.alto_fil

                seguir = True
                while seguir:
                    for item in movimientos:       #Movemos un poquito cada bloque que deba hacerlo en esta fila
                        if item[1] <= item[2]:
                            dc.SetPen(self.LINEA_FONDO) #Pintamos del color del fondo encima del rectángulo - solo en el espacio que se queda "libre"
                            dc.SetBrush(self.COLOR_FONDO)
                            dc.DrawRectangle(item[0], item[1], self.ancho_col*item[3], (item[2]-item[1]) // 10 +1)
                            if item[4] == 0:            #Volvemos a pintar el rectángulo
                                dc.SetBrush(self.COLOR_1)
                            elif item[4] == 1:
                                dc.SetBrush(self.COLOR_2)
                            else:
                                dc.SetBrush(self.COLOR_3)
                            item[1] += (item[2]-item[1]) // 10 +1   #Movimiento
                            dc.SetPen(self.LINEA_NEGRO)
                            dc.DrawRectangle(item[0], item[1], self.ancho_col*item[3], self.alto_fil)
                            wx.Yield() # Permitimos que se actualice el resto de la GUI
                        else:
                            seguir = False #Cuando termine uno, habrán terminado todos (los bloques más alejados caen más rápido)
                    time.sleep(0.001)
            self.actualizar_dibujo()    #Con cada fila actualizamos el dibujo para disimular imperfecciones
                
    def movimiento(self, col_inicial, bloque):
        #ENT: La columna original inicial y el bloque después de haberlo "movido"
        #SAL: Realiza la animación del movimiento lateral de un bloque, mostrada en la zona del tablero
        dc = wx.ClientDC(self.zona_juego)
        #Información original del bloque
        ref_x = col_inicial*self.ancho_col
        ref_y = bloque.fil * self.alto_fil
        #Información final
        ref_x_fin = bloque.col_inic *self.ancho_col

        if  bloque.col_inic - col_inicial < 0:   #Movimiento hacia la izquierda
            while ref_x > ref_x_fin:
                dc.SetPen(self.LINEA_FONDO) #Pintamos del color del fondo encima del rectángulo - sólo en el espacio que se queda "libre"
                dc.SetBrush(self.COLOR_FONDO)
                dc.DrawRectangle(ref_x+self.ancho_col*bloque.longitud-((ref_x - ref_x_fin) // 10 +1), ref_y, (ref_x - ref_x_fin) // 10 +1, self.alto_fil)
                if bloque.color == 0:   #Volvemos a pintar el rectángulo
                    dc.SetBrush(self.COLOR_1)
                elif bloque.color == 1:
                    dc.SetBrush(self.COLOR_2)
                else:
                    dc.SetBrush(self.COLOR_3)
                ref_x -= (ref_x - ref_x_fin) // 10 +1
                dc.SetPen(self.LINEA_NEGRO)
                dc.DrawRectangle(ref_x, ref_y, self.ancho_col*bloque.longitud, self.alto_fil)
                wx.Yield() # Permitimos que se actualice el resto de la GUI
                time.sleep(0.001)
        else: #Movimiento hacia la derecha
            while ref_x < ref_x_fin:
                dc.SetPen(self.LINEA_FONDO) #Pintamos del color del fondo encima del rectángulo - sólo en el espacio que se queda "libre"
                dc.SetBrush(self.COLOR_FONDO)
                dc.DrawRectangle(ref_x, ref_y, (ref_x_fin - ref_x) // 10 +1, self.alto_fil)
                if bloque.color == 0:   #Volvemos a pintar el rectángulo
                    dc.SetBrush(self.COLOR_1)
                elif bloque.color == 1:
                    dc.SetBrush(self.COLOR_2)
                else:
                    dc.SetBrush(self.COLOR_3)
                ref_x += (ref_x_fin - ref_x) // 10 +1
                dc.SetPen(self.LINEA_NEGRO)
                dc.DrawRectangle(ref_x, ref_y, self.ancho_col*bloque.longitud, self.alto_fil)
                wx.Yield() # Permitimos que se actualice el resto de la GUI
                time.sleep(0.001)
        self.actualizar_dibujo() #Para evitar imperfecciones
        

class NuevaPartidaDialog(wx.Dialog):
    #Diálogo sencillo para la confirmación de que se quiere empezar una nueva partida
    #SAL: La señal de OK o de CANCEL
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP
        wx.Dialog.__init__(self, *args, **kwds)
        #Construcción de la interfaz
        self.SetSize((350, 120))
        self.SetTitle("Nueva Partida")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap(iconos.get_new_icon.GetImage()))
        self.SetIcon(_icon)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        label_1 = wx.StaticText(self, wx.ID_ANY, u"Empezar de nuevo borrará todo el progreso actual.\n¿Estás seguro?", style=wx.ALIGN_CENTER_HORIZONTAL)
        sizer_1.Add(label_1, 0, wx.ALL | wx.EXPAND, 5)
        botones = wx.StdDialogButtonSizer()
        sizer_1.Add(botones, 0, wx.ALIGN_RIGHT | wx.ALL, 4)
        self.button_OK = wx.Button(self, wx.ID_OK, "")
        botones.AddButton(self.button_OK)
        self.button_CANCEL = wx.Button(self, wx.ID_CANCEL, "")
        self.button_CANCEL.SetDefault()
        botones.AddButton(self.button_CANCEL)
        botones.Realize()
        self.SetSizer(sizer_1)

        self.SetAffirmativeId(self.button_OK.GetId())   #Cuando se de al OK el valor devuelto será wx.ID_OK
        self.SetEscapeId(self.button_CANCEL.GetId())    #Cuando se de al Cancelar el valor devuelto será wx.ID_CANCEL
        self.Layout()

class AbrirFicheroDialog(wx.Dialog):
    #Diálogo para la introducción de una ruta de fichero con los bloques
    #SAL: La señal de OK o CANCEL. Se debe leer el valor de la ruta antes de destruir el diálogo
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP
        wx.Dialog.__init__(self, *args, **kwds)
        #Construcción de la interfaz
        self.SetSize((350, 135))
        self.SetTitle("Abrir Fichero")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap(iconos.get_open_icon.GetImage()))
        self.SetIcon(_icon)
        self.sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.label_1 = wx.StaticText(self, wx.ID_ANY, "Introduzca la ruta del fichero de bloques:", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.sizer_1.Add(self.label_1, 0, wx.ALL | wx.EXPAND, 5)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_1.Add(sizer_3, 1, wx.ALL | wx.EXPAND, 5)
        self.intro_ruta = wx.TextCtrl(self, wx.ID_ANY, "")
        sizer_3.Add(self.intro_ruta, 1, wx.EXPAND, 0)
        self.button_EXAM = wx.Button(self, wx.ID_ANY, "Examinar...")
        sizer_3.Add(self.button_EXAM, 0, wx.EXPAND, 0)
        botones = wx.StdDialogButtonSizer()
        self.sizer_1.Add(botones, 0, wx.ALIGN_RIGHT | wx.ALL, 4)
        self.button_OK = wx.Button(self, wx.ID_OK, "")
        self.button_OK.Disable()    #No se habilita hasta que no se escribe algo
        botones.AddButton(self.button_OK)
        self.button_CANCEL = wx.Button(self, wx.ID_CANCEL, "")
        botones.Add(self.button_CANCEL, 0, 0, 0)
        botones.Realize()
        self.SetSizer(self.sizer_1)
        self.SetAffirmativeId(self.button_OK.GetId())   #Cuando se de al OK el valor devuelto será wx.ID_OK (si se cumplen las condiciones)
        self.SetEscapeId(self.button_CANCEL.GetId())    #Cuando se de al Cancelar el valor devuelto será wx.ID_CANCEL
        self.Layout()

        #Eventos
        self.Bind(wx.EVT_TEXT, self.ruta_cambia, self.intro_ruta)
        self.Bind(wx.EVT_BUTTON, self.on_abrir_explorer, self.button_EXAM)
        self.Bind(wx.EVT_BUTTON, self.on_confirm, self.button_OK)

    def ruta_cambia(self, event): #Habilitamos el botón de OK si se escribe algo
        self.button_OK.Enable()

    def on_abrir_explorer(self, event): #Botón de examinar - abrimos el diálogo de explorador del sistema
        with wx.FileDialog(self, "Abrir fichero de filas", wildcard="Documentos de texto (*.txt)|*.txt", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as explorador:
            if explorador.ShowModal() == wx.ID_OK:
                self.intro_ruta.SetValue(explorador.GetPath())

    def on_confirm(self, event):  
        #Se ha dado al botón de OK, se debe comprobar la validez del fichero
        #SAL: Si el archivo referenciado es válido, se cierra el diálogo
        todo_correcto = True
        try:
            self.fichero = self.intro_ruta.GetValue()   #Valor al que se accede si está todo OK
            archivo = open(self.fichero)
            lista_referencia = archivo.readlines()
            if len(lista_referencia)==0:    #Vacío
                self.label_1.SetLabel("¡El fichero está vacío!")
                self.label_1.SetForegroundColour(wx.Colour("red"))
                self.sizer_1.Layout()
                todo_correcto = False
            else:
                #Comprobación de formato
                for fila in lista_referencia: 
                    if len(fila)>11:
                        self.label_1.SetLabel("Error al leer el archivo. El formato no es compatible.")
                        self.label_1.SetForegroundColour(wx.Colour("red"))
                        self.sizer_1.Layout()
                        todo_correcto = False
        except IOError:
            self.label_1.SetLabel("Error al leer el archivo. Puede que no sea accesible o no exista.")
            self.label_1.SetForegroundColour(wx.Colour("red"))
            self.sizer_1.Layout()
            todo_correcto = False
        
        if todo_correcto:
            self.EndModal(wx.ID_OK) #Se cierra el diálogo devolviendo el valor wx.ID_OK

class AjustesTableroDialog(wx.Dialog):
    #Diálogo para el cambio del número de filas
    #SAL: La señal de OK o CANCEL, y se debe leer el valor del spin antes de destruirlo
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP
        wx.Dialog.__init__(self, *args, **kwds)
        #Construcción de la interfaz
        self.SetSize((532, 150))
        self.SetTitle("Ajustes del Tablero de Juego")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap(iconos.get_set_icon.GetImage()))
        self.SetIcon(_icon)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.dimensiones = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Dimensiones"), wx.VERTICAL)
        sizer_1.Add(self.dimensiones, 0, wx.ALL | wx.EXPAND, 5)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        self.dimensiones.Add(sizer_4, 0, wx.EXPAND, 0)
        label_1 = wx.StaticText(self, wx.ID_ANY, u"Número de filas:         ", style=wx.ALIGN_LEFT)
        sizer_4.Add(label_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.spin_filas = wx.SpinCtrl(self, wx.ID_ANY, "12", min=1, max=100)
        sizer_4.Add(self.spin_filas, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_2 = wx.StaticText(self, wx.ID_ANY, u"Cualquier cambio restablecerá la partida a su estado inicial.")
        sizer_1.Add(label_2, 0, wx.ALL, 5)
        self.botones = wx.StdDialogButtonSizer()
        sizer_1.Add(self.botones, 0, wx.ALIGN_RIGHT | wx.ALL, 4)
        self.button_OK = wx.Button(self, wx.ID_OK, "")
        self.button_OK.SetDefault()
        self.botones.AddButton(self.button_OK)
        self.button_CANCEL = wx.Button(self, wx.ID_ANY, "Cancelar")
        self.botones.Add(self.button_CANCEL, 0, 0, 0)
        self.botones.Realize()
        self.SetSizer(sizer_1)

        self.SetAffirmativeId(self.button_OK.GetId())   #Cuando se de al OK el valor devuelto será wx.ID_OK
        self.SetEscapeId(self.button_CANCEL.GetId())    #Cuando se de al Cancelar el valor devuelto será wx.ID_CANCEL
        self.Layout()

class MyApp(wx.App):
    #La aplicación
    #Crea la pantalla principal y la muestra
    def OnInit(self):
        self.frame = Pantalla(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    #Se crea la "aplicación" y se ejecuta el bucle principal
    app = MyApp()
    app.MainLoop()