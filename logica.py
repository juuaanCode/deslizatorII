# Juan González Arranz - T1 - DESLIZATOR (II)
# Archivo de lógica principal del juego. Creado adaptando la versión del profesor.

CH_FICH = ord('A')  # Inicio secuencia caracteres fichero (mayúsculas)
CH_FIL = ord('A')   # Inicio secuencia caracteres que representan filas
CH_COL = ord('0')   # Inicio secuencia caracteres que representan columnas

def ciclo(lista):
    #ENT: Una lista
    #SAL: Devuelve de forma cíclica los elementos de la lista
    while True:
        for elemento in lista:
            yield elemento

class Bloque(object):
    #Representa un bloque con las propiedades: fila, columna inicial, final, valor (color) y tamaño
    def __init__(self, fil, col_inic, col_fin, color):
        self.fil = fil
        self.col_inic = col_inic
        self.col_fin = col_fin
        self.color = color                      #Número que representa el color
        self.longitud = col_fin - col_inic + 1  #Tamaño del bloque

    def desplazar(self, dx, dy):
        #ENT: Desplazamiento horizontal y vertical
        #SAL: Actualiza la posición del bloque
        self.fil += dy
        self.col_inic += dx
        self.col_fin += dx

class Tablero(object):
    #Representa el tablero con las propiedades: entrada (filas de referencia), numero de filas y columnas, puntos y una matriz con bloques
    def __init__(self, nombre_fich, num_fil):
        #ENT: la ruta del fichero y el número de filas
        with open(nombre_fich) as fich:
            self.entrada = ciclo(fich.read().splitlines())
        self.num_fil = num_fil
        self.num_col = 10
        self.puntos = 0
        self.datos = [[] for _ in range(num_fil)]   #Representación del tablero

    def lleno(self):
        #SAL: True si hay bloques en la primera fila (fin de partida)
        return len(self.datos[0]) > 0

    def insertar_fila(self):
        #SAL: Asigna una nueva fila de bloques en la parte superior del tablero
        linea = next(self.entrada)
        self.datos[0] = [Bloque(0,c0,c1,color) for (c0,c1,color) in self.bloques_en_linea(linea)]

    def jugada(self, entrada):
        #ENT: Jugada (string)
        #     Comprueba si es posible ejecutar la jugada y la ejecuta si lo es
        #SAL: Bandera, la columna original del bloque y el bloque después del movimiento
        #Los valores de "bandera" pueden ser:
        # -2 -> El bloque no puede desplazarse
        # -1 -> No hay bloque en esa posición
        #  0 -> Jugada válida

        fila = ord(entrada[0])- CH_FIL
        columna = ord(entrada[1])- CH_COL
        
        try:
            ind = self.numero_bloque(self.datos[fila], columna)
        except IndexError: #Ha habido un error de posición
            return -3, None, None
        if ind < 0:
            #No hay ningún bloque ahí
            return -1,None, None

        bloque = self.datos[fila][ind]
        if entrada[2] == '<':            
            if ind == 0:
                #Bloque más a la izquierda de la fila
                if bloque.col_inic == 0:  #No podemos moverlo
                    return -2, None, None
                #Lo movemos al borde
                distancia = -bloque.col_inic
            else:
                bloque_anterior = self.datos[fila][ind - 1]
                distancia = bloque.col_inic - bloque_anterior.col_fin - 1    #Espacio entre bloques
                if distancia == 0:  #Imposible moverlo
                    return -2, None, None
                #Lo movemos de forma que se "pegue" al bloque anterior
                distancia = -distancia
        elif entrada[2] == '>':
            if ind == len(self.datos[fila])-1:
                #Bloque más a la derecha de la fila
                if bloque.col_fin == self.num_col-1:  #Pegado a borde
                    return -2, None, None
                #Lo movemos al borde
                distancia = self.num_col-bloque.col_fin-1
            else:
                bloque_siguiente = self.datos[fila][ind + 1]
                distancia = bloque_siguiente.col_inic - bloque.col_fin - 1    #Espacio entre bloques
                if distancia == 0:  #Pegado a nuestro bloque
                    return -2, None, None
                #Lo movemos de forma que se "pegue" al bloque siguiente
        #Actualizamos el bloque
        col_inicial = bloque.col_inic   #Columna original, antes de cualquier movimiento
        bloque.desplazar(distancia, 0)
        return 0, col_inicial, bloque

    def caida(self, fila):  
        #ENT: El número de la fila sobre la que se quiere procesar la caída
        #SAL: Mueve los bloques y devuelve una lista con información de los movidos.
        #     La información es una lista por cada bloque: [columna0, filaOriginal, filaFinal, longitud, color]
        movimientos = []
        for bloque in self.datos[fila][:]: #Se trabaja con una copia de la fila
            # Se comprueban huecos en filas inferiores
            fil_des = pos_hueco = -1
            for i in range(fila+1, self.num_fil):
                if self.pos_ins_bloque(self.datos[i], bloque) != -1:
                    pos_hueco = self.pos_ins_bloque(self.datos[i], bloque)
                else: 
                    break
                fil_des = i
            # Si hay descenso, mover el bloque
            if fil_des > -1:
                self.datos[fila].remove(bloque)
                self.datos[fil_des].insert(pos_hueco, bloque)
                bloque.desplazar(0, fil_des - fila) #Actualizar el bloque
                movimientos.append([bloque.col_inic,fila,fil_des,bloque.longitud, bloque.color])    #Guardamos información
        return movimientos

    def eliminacion(self):
        #SAL: Elimina las filas completas, detectando si se produce una "reacción en cadena"
        #     Devuelve True si ha habido eliminaciones (no reacción en cadena) porque hay que recalcular caída
        eliminacion = False
        for fila in range(self.num_fil):
            if self.fila_completa(self.datos[fila], self.num_col):
                if all(map(lambda b: b.color == self.datos[fila][0].color, self.datos[fila][1:])):
                    #Bloques del mismo color -> REACCIÓN EN CADENA
                    eliminacion = False
                    for fila in range(self.num_fil):
                        self.puntos += sum((bloque.longitud for bloque in self.datos[fila]))    #Sumamos todos los puntos
                        self.datos[fila] = []   #Vaciamos todas las filas
                    break
                self.datos[fila] = []
                eliminacion = True
                self.puntos += self.num_col
        return eliminacion

    # ************** OPERACIONES AUXILIARES ********************
    
    @staticmethod
    def bloques_en_linea(lin):
        #ENT: Línea de texto
        #SAL: Devuelve una tupla (columna inicial, final y valor/color) por cada bloque que
        #     aparece en la línea de texto (formato fichero).
        i, n, c_ant = 0, 0, ' '
        for c in lin:
            if c != c_ant:
                if c_ant != ' ':
                    yield (i-n, i-1, ord(c_ant.upper())-CH_FICH)
                c_ant = c
                n = 1
            else:
                n += 1
            i += 1
        if c_ant != ' ':
            yield (i-n, i-1, ord(c_ant.upper())-CH_FICH)

    @staticmethod
    def numero_bloque(lis, col):
        #ENT: Fila y columna en la que puede estar un bloque
        #SAL: Devuelve su índice en la lista o -1 si no existe
        i = 0
        for bloque in lis:
            if bloque.col_inic <= col <= bloque.col_fin:
                return i
            i += 1
        return -1

    @staticmethod    
    def pos_ins_bloque(lis, blo):
        #ENT: Fila y bloque
        #SAL: Devuelve la posición donde se debería insertar un bloque
        #     si existe un hueco para él (o -1 si no se puede insertar)
        i = 0 #Búsqueda del primer bloque totalmente posterior al nuestro
        for bloque_pos in lis:
            if bloque_pos.col_inic > blo.col_fin:
                break
            i += 1
        # Si existe colisión, es con el bloque anterior al posterior
        return i if i == 0 or lis[i-1].col_fin < blo.col_inic else -1

    @staticmethod
    def fila_completa(fila, numcol):
        #ENT: Fila y el número de columnas del tablero
        #SAL: True si la fila está completa
        if len(fila) == 0:
            return False
        # Comprobación de que los bloques inicial y final cubren los extremos 
        if fila[0].col_inic != 0 or fila[-1].col_fin != numcol-1:
            return False
        # Comprobación de que todos los bloques están "pegados"
        for (b1, b2) in zip(fila, fila[1:]):
            if b1.col_fin+1 != b2.col_inic:
                return False
        return True