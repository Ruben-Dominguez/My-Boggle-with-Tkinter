from tkinter import *
from tkinter import messagebox
from random import randint

# globales
root = Tk()
listButtons = []
listFrames = []
CLICKED = "#299C99"
cadena = StringVar()
aBuscar = ""
score = StringVar()
scoreInt = 0
rows = 0
haGanado = False

listaFrame = Frame(root, width=400, height=480, relief=FLAT, bg="#DFDFDF")
c = Canvas(listaFrame)
scrollbar = Scrollbar(listaFrame, orient="vertical", command=c.yview)
sf = Frame(c)
sf.bind("<Configure>", lambda e: c.configure(scrollregion=c.bbox("all")))
c.create_window((0, 0), window=sf, anchor="nw")
c.configure(yscrollcommand=scrollbar.set)

listaFrame.grid(row=1, column=1, rowspan=2, sticky=NSEW)
c.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

tablero = Frame(root, width=400, height=400, relief=FLAT, bg="#64AC69")

botonesFrame = Frame(root, width=400, height=50, relief=FLAT, bg="#4F7880")
botonesFrame.grid_propagate(False)
botonesFrame.columnconfigure(0, weight=1)
botonesFrame.rowconfigure(0, weight=1)


# Nuestro trie para verificacion y agregacion de palabras
# Notese que en la funcion insertar no se usa buscar por simplicidad
class Nodo:
    def __init__(self):
        self.valor = ""
        self.hijos = [None for x in range(26)]
        self.esFin = False


class Trie:
    def __init__(self):
        self.root = self.crearNodo()

    def crearNodo(self):
        # regresa una instancia de un nodo vacio
        return Nodo()

    def charToNum(self, caracter):
        return ord(caracter) - ord("a")

    def insertar(self, palabra):
        # lo empezamos en la raiz para empezar la insercion
        iterador = self.root
        longitud = len(palabra)

        for profundidad in range(longitud):
            index = self.charToNum(palabra[profundidad])

            if not iterador.hijos[index]:
                iterador.hijos[index] = self.crearNodo()

            # se desplaza al siguiente nodo, creado o no
            iterador = iterador.hijos[index]

        # marca el ultimo como fin de palabra, sea nuevo o no
        iterador.esFin = True

    def buscar(self, palabra):
        # lo empezamos en la raiz para empezar la busqueda
        iterador = self.root
        longitud = len(palabra)

        for profundidad in range(longitud):
            index = self.charToNum(palabra[profundidad])
            if not iterador.hijos[index]:
                return False
            iterador = iterador.hijos[index]

        return iterador is not None and iterador.esFin

    def borrar(self, palabra):
        # lo empezamos en la raiz para empezar la busqueda
        iterador = self.root
        longitud = len(palabra)

        for profundidad in range(longitud):
            index = self.charToNum(palabra[profundidad])
            if not iterador.hijos[index]:
                return False
            iterador = iterador.hijos[index]

        if iterador is not None and iterador.esFin:
            iterador.esFin = False


reference = None


class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        self.y = None
        self.x = None
        self.letra = None
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def on_enter(self, _):
        if self["state"] != DISABLED:
            self['background'] = "#DDF0F0"

    def on_leave(self, _):
        if self["state"] != DISABLED:
            self['background'] = self.defaultBackground

    def on_click(self, _):
        print(self.x, self.y)
        if self["state"] != DISABLED:
            self['background'] = self["activebackground"]
            clicked(self.x, self.y)
            if len(str(cadena.get())) <= 28:
                cadena.set(cadena.get() + self.letra)
            else:
                mmm = messagebox.showwarning("No se pase joben unu",
                                             """Exedente de caracteres, no hay palabras en el diccionario
                                             mayores a 28 caracteres, piquele check para resetear y tenga
                                             más cuidado.
                                             Aunque le pique a más letras no serán agregadas a la palabra.""")


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


trie = Trie()


def clicked(x, y):
    for a in range(8):
        for b in range(8):
            listButtons[a][b]["state"] = DISABLED

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


def numToChar(num):
    return num + ord("a")


def prove():
    global listButtons, aBuscar, trie, score, scoreInt, haGanado

    aBuscar = cadena.get()
    cadena.set("")

    if trie.buscar(aBuscar):
        scoreInt += len(aBuscar)
        score.set("Score: " + str(scoreInt))
        trie.borrar(aBuscar)
        Label(sf, text=aBuscar.upper(), font=("Helvetica", 14), fg="green", anchor=W).pack(fill=X)
        if scoreInt >= 50 and not haGanado:
            haGanado = True
            ganastesxd = messagebox.askyesno("GANADOR!!!!", "Has juntado más de 50 puntos, ¿deseas continuar?")
            if not ganastesxd:
                bye()
    else:
        Label(sf, text=aBuscar.upper(), font=("Helvetica", 14), fg="red", anchor=W).pack(fill=X)

    for a in range(8):
        for b in range(8):
            listButtons[a][b]["state"] = NORMAL
            listButtons[a][b]["bg"] = listButtons[a][b].defaultBackground


def bye():
    root.destroy()


def daRules():
    response = messagebox.showinfo("Información que cura",
                                   """"-Para jugar empiece seleccionando casillas adyacentes para formar palabras.      
-Cuando tenga la palabra deseada presione check, si se equivica no importa, no se descuentan puntos :)
-Acumulará puntos dependiendo de la longitud.
-Gana si tiene más de 50 puntos!

NOTA: No se permiten palabras de más de 28 caracteres, no sea guarro.""")


def deNuevo():
    global listFrames, listButtons, scoreInt, sf, trie
    scoreInt = 0
    score.set("Score: " + str(scoreInt))
    cadena.set("")

    with open("diccionario.txt") as file_in:
        palabras = file_in.read().splitlines()

    for palabra in palabras:
        trie.insertar(palabra.lower())

    for widget in sf.winfo_children():
        widget.destroy()

    for x in range(8):
        for y in range(8):
            listFrames[x][y].destroy()
            listButtons[x][y].destroy()

    listFrames.clear()
    listButtons.clear()

    for x in range(8):
        b = []
        f = []
        for y in range(8):
            f.append(Frame(tablero, width=50, height=50))
            f[y].grid_propagate(False)
            f[y].columnconfigure(0, weight=1)
            f[y].rowconfigure(0, weight=1)
            f[y].grid(row=x, column=y)

            letra = str(chr(numToChar(randint(0, 25))))
            b.append(
                HoverButton(f[y], relief=FLAT, text=letra.upper(), font="Fixedsys 24 bold", activebackground=CLICKED))
            b[y].x = x
            b[y].y = y
            b[y].letra = letra
            b[y].grid(sticky="wens")
        listButtons.append(b)
        listFrames.append(f)


def main():
    global listButtons, listFrames, cadena, score, trie
    # insercion de palabras
    with open("diccionario.txt") as file_in:
        palabras = file_in.read().splitlines()

    for palabra in palabras:
        trie.insertar(palabra.lower())

    # funcion del GUI
    root.title("My Boggle")
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
                          bg="#1E95C2", fg="white", activebackground="#15566E", command=deNuevo)
    exitB = HoverButton2(botonesFrame, text="EXIT", font=("Helvetica", 11, "bold"), width=6, relief=FLAT, bg="#1E95C2",
                         fg="white", activebackground="#15566E", command=bye)
    rulesB = HoverButton2(botonesFrame, text="RULES", font=("Helvetica", 11, "bold"), width=6, relief=FLAT,
                          bg="#1E95C2", fg="white", activebackground="#15566E", command=daRules)

    for x in range(8):
        b = []
        f = []
        for y in range(8):
            f.append(Frame(tablero, width=50, height=50))
            f[y].grid_propagate(False)
            f[y].columnconfigure(0, weight=1)
            f[y].rowconfigure(0, weight=1)
            f[y].grid(row=x, column=y)

            letra = str(chr(numToChar(randint(0, 25))))
            b.append(
                HoverButton(f[y], relief=FLAT, text=letra.upper(), font="Fixedsys 24 bold", activebackground=CLICKED))
            b[y].x = x
            b[y].y = y
            b[y].letra = letra
            b[y].grid(sticky="wens")
        listButtons.append(b)
        listFrames.append(f)

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

    try:
        while True:
            root.update_idletasks()
            root.update()
    except TclError:
        pass


# ejecucion principal del codigo
if __name__ == "__main__":
    main()
