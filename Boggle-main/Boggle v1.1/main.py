# Este codigo fue hecho por Ruben Dominguez, matricula: 329806
# Ultima actualizacion hecha el 12/2/20
# Objetivo: juego del boogle implementando un trie para la busqueda y almacenamiento del diccionario
# y una tabala hash abierta lineal con metodos de hash de extraccion y division para las palabras ya  encontradas
# patch 1.1: Se agrega una tabla hash para la revision de repeticiones, mejora el reseteo de esa forma

# se utiliza tkinter para el GUI y random para las letras
from tkinter import *
from tkinter import messagebox
from random import randint

# GLOBALES
root = Tk()  # ventana
listButtons = []
listFrames = []
listEliminadas = [None for x in range(100_000)]
CLICKED = "#299C99"  # color en hexadecimal
cadena = StringVar()  # cadena que muestra la palabra en pantalla
aBuscar = ""  # variable global para buscar la palabra
score = StringVar()  # cadena que muestra el score en pantalla
scoreInt = 0
haGanado = False

# estas lineas permiten con frames y canvas tener un scrolleable para la lista de palabras
listaFrame = Frame(root, width=400, height=480, relief=FLAT, bg="#DFDFDF")  # el frame de palabras
c = Canvas(listaFrame)  # el canvas donde va nuestro frmae anterior
scrollbar = Scrollbar(listaFrame, orient="vertical", command=c.yview)  # el widget de scrollbar
sf = Frame(c)  # metemos el canvas, que contiene un frame
sf.bind("<Configure>", lambda e: c.configure(scrollregion=c.bbox("all")))  # configuramos el evento con bind
c.create_window((0, 0), window=sf, anchor="nw")  # finalmente configuramos el canvas
c.configure(yscrollcommand=scrollbar.set)

# estas lineas ponen el frame scrolleable en pantalla con grid y pack
listaFrame.grid(row=1, column=1, rowspan=2, sticky=NSEW)
c.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

tablero = Frame(root, width=400, height=400, relief=FLAT, bg="#64AC69")  # frame que contiene las letras

botonesFrame = Frame(root, width=400, height=50, relief=FLAT, bg="#4F7880")  # frame que contiene los botones de abajo
botonesFrame.grid_propagate(False)
botonesFrame.columnconfigure(0, weight=1)
botonesFrame.rowconfigure(0, weight=1)


# Nuestro trie para verificacion y agregacion de palabras
# Notese que en la funcion insertar no se usa buscar por simplicidad
class Nodo:
    def __init__(self):
        self.hijos = [None for x in range(26)]
        self.esFin = False


class Trie:
    def __init__(self):  # contructor
        self.root = self.crearNodo()  # la raiz del trie con la funcion que le crea el nodo

    # regresa una instancia de un nodo vacio
    def crearNodo(self):
        return Nodo()

    # como lo dice el nombre genera enteros de los chars
    def charToNum(self, caracter):
        return ord(caracter) - ord("a")  # ord convierte un string a un entero

    # inserta la palabra
    def insertar(self, palabra):
        # lo empezamos en la raiz para empezar la insercion
        iterador = self.root
        longitud = len(palabra)

        for profundidad in range(longitud):
            index = self.charToNum(palabra[profundidad])  # generamos en que hijo esta

            if not iterador.hijos[index]:
                iterador.hijos[index] = self.crearNodo()  # si no encuentr nodo lo crea y asi con cada nuevo nodo

            # se desplaza al siguiente nodo, creado o no
            iterador = iterador.hijos[index]

        # marca el ultimo como fin de palabra, sea nuevo o no
        iterador.esFin = True

    # busca la palabra, muy parecido a la funcion anterior
    def buscar(self, palabra):
        # lo empezamos en la raiz para empezar la busqueda
        iterador = self.root
        longitud = len(palabra)

        for profundidad in range(longitud):
            index = self.charToNum(palabra[profundidad])
            if not iterador.hijos[index]:
                return False
            iterador = iterador.hijos[index]

        return iterador is not None and iterador.esFin  # retorna un booleano si se obtuvo un iterador y es fin

    # NO HAY BORRAR, PARA ESO TENEMOS A LA TABLA HASH :)


# con lo mas batalle fue esto, tkinter no maneja el estar sobre un boton y ponerlo de otro color
# esta clase que hereda de los botones del framework me permite modificar el funcionamiento del evento hover y otras
# cosillas que me gustaron :)
# Este boton1 es para las letras y tiene varias funciones
class HoverButton(Button):
    def __init__(self, master, **kw):  # constructor
        Button.__init__(self, master=master, **kw)  # pasamos los argumentos de la clase anterior llamando al contructor
        self.y = None
        self.x = None
        self.letra = None
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)  # bind nos permite mapear una funcion a un evento
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    # cuando le presionas pasa, desactiva la letra y le cambia el color
    def on_enter(self, _):
        if self["state"] != DISABLED:
            self['background'] = "#DDF0F0"

    # cuando el mouse deja el boton se activa (no es necesario el click)
    def on_leave(self, _):
        if self["state"] != DISABLED:
            self['background'] = self.defaultBackground

    # funcion de click para las letras
    def on_click(self, _):
        if self["state"] != DISABLED:
            self['background'] = self["activebackground"]
            clicked(self.x, self.y)  # funcion de comprobacion y desactivacion de botones
            if len(str(cadena.get())) <= 28:  # aqui comprobamos lo de las 28 letras para tener un cap
                cadena.set(cadena.get() + self.letra)
            else:
                mmm = messagebox.showwarning("No se pase joben unu",
                                             """Exedente de caracteres, no hay palabras en el diccionario
mayores a 28 caracteres, piquele check para resetear y tenga
más cuidado.
Aunque le pique a más letras no serán agregadas a la palabra.""")


# de nuevo tenemos la herencia del boton pero estos botones son los de abajo y no son iguales a las letras, es
# por esto que deben tener otra funcionalidad, solamente son botones que te dejan cambiar el color como un gamer
# PARA MAS DOCUMENTACION VISITE LA CLASE DE ARRIBA
class HoverButton2(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, _):
        self['background'] = self['activebackground']

    def on_leave(self, _):
        self['background'] = self.defaultBackground


trie = Trie()  # pongo este objeto aqui despues de las clases porque no mepermite ponerlo arriba antes de la declaracion


# funcion de comprobacion, desabilita o habilita las teclas segun la posicion
def clicked(x, y):
    # desabilitamos todas las teclas
    for a in range(8):
        for b in range(8):
            listButtons[a][b]["state"] = DISABLED

    # esta parte del codigo me gusta mucho, el problema es que es muy compleja. La logica viene de una operacion
    # ternaria, cambia los 8 botones de alrededor del boton clickeado cuidando con maximos y minimos que no se salga
    # de el tablero, verifica si esta clickeada para poder ponerla en su estado correcto. Basicamente checa si
    # esta clikeada ponla habilitada, si no, no hagas nada y dejala desabilitada

    listButtons[max(0, x - 1)][max(0, y - 1)]["state"] = NORMAL if listButtons[max(0, x - 1)][max(0, y - 1)][
                                                                       "bg"] != CLICKED else DISABLED
    listButtons[max(0, x - 1)][y]["state"] = NORMAL if listButtons[max(0, x - 1)][y]["bg"] != CLICKED else DISABLED
    listButtons[max(0, x - 1)][min(7, y + 1)]["state"] = NORMAL if listButtons[max(0, x - 1)][min(7, y + 1)][
                                                                       "bg"] != CLICKED else DISABLED
    listButtons[x][max(0, y - 1)]["state"] = NORMAL if listButtons[x][max(0, y - 1)]["bg"] != CLICKED else DISABLED
    listButtons[x][min(7, y + 1)]["state"] = NORMAL if listButtons[x][min(7, y + 1)]["bg"] != CLICKED else DISABLED
    listButtons[min(7, x + 1)][max(0, y - 1)]["state"] = NORMAL if listButtons[min(7, x + 1)][max(0, y - 1)][
                                                                       "bg"] != CLICKED else DISABLED
    listButtons[min(7, x + 1)][y]["state"] = NORMAL if listButtons[min(7, x + 1)][y]["bg"] != CLICKED else DISABLED
    listButtons[min(7, x + 1)][min(7, y + 1)]["state"] = NORMAL if listButtons[min(7, x + 1)][min(7, y + 1)][
                                                                       "bg"] != CLICKED else DISABLED


# funcion que devuelve un char de un entero, usado en el random para convertir los ints en letras
def numToChar(num):
    return num + ord("a")


# funcion del boton check, checa en el trie y en la tabla hash para comprobar si existe y que no este repetida
def prove():
    global listButtons, aBuscar, trie, score, scoreInt, haGanado, listEliminadas

    encontrada = False  # bandera para saber si esta en la tabla

    aBuscar = cadena.get()  # variable local que permite buscar la palabra
    cadena.set("")
    enTrie = trie.buscar(aBuscar)  # busca en el trie la palabra

    if enTrie:

        indice = funHash(aBuscar)  # con la funcion hash obtengo la llave
        while listEliminadas[indice] is not None:
            if aBuscar != listEliminadas[indice]:
                indice += 1  # como se evitaron las colisiones fue abierto lineal
            else:
                encontrada = True
                break  # esta va pal Juan

        if not encontrada:
            scoreInt += len(aBuscar)
            score.set("Score: " + str(scoreInt))

            indice = funHash(aBuscar)  # retorno a la llave original en caso de haber cambiado
            while listEliminadas[indice] is not None:
                indice += 1  # manejo las colisiones linealmente (se dejan 10 espacios vacios asegurados entre letras)
            listEliminadas[indice] = aBuscar

            Label(sf, text=aBuscar.upper() + " (+" + str(len(aBuscar)) + ")", font=("Helvetica", 12), fg="green",
                  anchor=W).pack(
                fill=X)  # agregar a la lista de palabras de color verde

            # Condicion de gane
            if scoreInt >= 50 and not haGanado:
                haGanado = True
                ganastesxd = messagebox.askyesno("GANADOR!!!!", "Has juntado más de 50 puntos, ¿deseas continuar?")
                if not ganastesxd:
                    bye()  # salida del programa

    if not enTrie:  # si no esta en el trie se agrega de color rojo
        Label(sf, text=aBuscar.upper(), font=("Helvetica", 12), fg="red", anchor=W).pack(fill=X)
    elif encontrada:  # si esta en la tabla hash se agrega de color amarillo
        Label(sf, text=aBuscar.upper() + " (+0)", font=("Helvetica", 12), fg="#CBCB3F", anchor=W).pack(fill=X)

    # reseteo de botones
    for a in range(8):
        for b in range(8):
            listButtons[a][b]["state"] = NORMAL
            listButtons[a][b]["bg"] = listButtons[a][b].defaultBackground


# creo que un poco obvio
def bye():
    root.destroy()


# funcion hash con extraccion, plegado y multiplicacion que me permite generar un espaciado de 10 por el modulo
def funHash(palabra):
    global listEliminadas

    suma = 0
    for i in range(len(palabra)):
        suma += ord(palabra[i]) * i * i * 10

    resultado = suma % 100_000
    return resultado


# funcion que me deja implementar un message box con las reglas, va ligado al boton rules
def daRules():
    response = messagebox.showinfo("Información que cura",
                                   """-Para jugar empiece seleccionando casillas adyacentes para formar palabras.      
-Cuando tenga la palabra deseada presione check, si se equivica no importa, no se descuentan puntos :)
-Acumulará puntos dependiendo de la longitud.
-Gana si tiene más de 50 puntos!

NOTA: No se permiten palabras de más de 28 caracteres, no sea guarro.""")


# funcion de reset de tablero y puntaje, lleva el argumento de primer para ahorrar codigo al ejecutar codigo por
# primera vez ya que se hacen las mismas operaciones pero sin los destructores
def deNuevo(primer):
    global listFrames, listButtons, listEliminadas, scoreInt, sf, trie
    scoreInt = 0
    score.set("Score: " + str(scoreInt))
    cadena.set("")

    if not primer:  # si no es la primera iteracion
        for i in range(len(listEliminadas)):  # limpia la lista de de entradas hash
            listEliminadas[i] = None

        for widget in sf.winfo_children():  # destruye el wigget de palabras
            widget.destroy()

        for x in range(8):  # limpia el tablero
            for y in range(8):
                listFrames[x][y].destroy()
                listButtons[x][y].destroy()

        listFrames.clear()
        listButtons.clear()

    # generamos el tablero
    for x in range(8):
        b = []  # lista de botones para las letras (local)
        f = []  # lista de frames para meter dentro los botones (local)
        for y in range(8):
            f.append(Frame(tablero, width=50, height=50))
            f[y].grid_propagate(False)
            f[y].columnconfigure(0, weight=1)
            f[y].rowconfigure(0, weight=1)
            f[y].grid(row=x, column=y)

            numero = randint(0, 35)  # generacion aleatoria de letras. Las vocales tienen x3 de probabilidades de salir
            if numero == 34 or numero == 35:
                letra = "a"
            elif numero == 32 or numero == 33:
                letra = "e"
            elif numero == 30 or numero == 31:
                letra = "i"
            elif numero == 28 or numero == 29:
                letra = "o"
            elif numero == 26 or numero == 27:
                letra = "u"
            else:
                letra = str(chr(numToChar(numero)))

            b.append(
                HoverButton(f[y], relief=FLAT, text=letra.upper(), font="Fixedsys 24 bold", activebackground=CLICKED))
            b[y].x = x
            b[y].y = y
            b[y].letra = letra
            b[y].grid(sticky="wens")
        listButtons.append(b)  # se copian a la lista global
        listFrames.append(f)  # se copian a la lista global


def main():
    global listButtons, listFrames, cadena, score, trie

    # insercion de palabras
    with open("diccionario.txt") as file_in:
        palabras = file_in.read().splitlines()
    for palabra in palabras:
        trie.insertar(palabra.lower())

    # funcion del GUI
    root.title("My Boggle  v1.1")
    cadena = StringVar()
    score = StringVar()
    score.set("Score: 0")
    root.geometry("800x500")
    root.resizable(False, False)

    # labels
    construccionLabel = Label(root, textvariable=cadena, font=("Helvetica", 30), fg="#686868", anchor=W)
    scoreLabel = Label(botonesFrame, textvariable=score, font=("Helvetica", 24), fg="White", bg="#4F7880", anchor=W)

    # botones
    check = Button(root, text="CHECK", font=("Helvetica", 12, "bold"), bg="#3FD421", activebackground="#37811D",
                   relief=FLAT, command=prove)
    resetB = HoverButton2(botonesFrame, text="RESET", font=("Helvetica", 11, "bold"), width=6, relief=FLAT,
                          bg="#1E95C2", fg="white", activebackground="#15566E", command=lambda: deNuevo(False))
    exitB = HoverButton2(botonesFrame, text="EXIT", font=("Helvetica", 11, "bold"), width=6, relief=FLAT, bg="#1E95C2",
                         fg="white", activebackground="#15566E", command=bye)
    rulesB = HoverButton2(botonesFrame, text="RULES", font=("Helvetica", 11, "bold"), width=6, relief=FLAT,
                          bg="#1E95C2", fg="white", activebackground="#15566E", command=daRules)

    deNuevo(True)  # generacion del tablero y la lista por primera vez

    # sistema grid para desplegar las cosas en pantalla
    tablero.grid(row=1, column=0, sticky=W)
    listaFrame.grid(row=1, column=1, rowspan=2, sticky=NSEW)
    botonesFrame.grid(row=2, column=0, sticky=W)
    check.grid(row=0, column=1, sticky=NS + E)
    construccionLabel.grid(row=0, column=0, columnspan=2, sticky=NSEW)
    scoreLabel.grid(row=0, column=0, sticky=W)
    resetB.grid(row=0, column=1, sticky=NS)
    exitB.grid(row=0, column=3, sticky=NS)
    rulesB.grid(row=0, column=2, sticky=NS)

    # main loop para que el juego se cicle. Parte de Tkinter
    try:
        while True:
            root.update_idletasks()
            root.update()
    except TclError:
        pass


# ejecucion principal del codigo
if __name__ == "__main__":
    main()
