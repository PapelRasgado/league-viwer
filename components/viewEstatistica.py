from tkinter import *
from PIL import Image, ImageTk
from services import api_service, menu_service

global bg
bg = "#182422"

global fg
fg = "#F3E171"

class EstatisticasInvo:
    def __init__(self, invocador, key):
        self.invocador = invocador
        self.key = key
        self.root = Tk()
        self.root.title("League Viwer")
        self.root.resizable(False, False)
        self.root.geometry("900x700")
        self.root["background"] = bg
        self.root.update()

        #renderizar logo
        self.container = Frame(self.root, bg = bg)
        #self.container.pack(side = TOP)
        self.container.grid(row = 0, column = 0, columnspan = 5)
        self.container.place(y = 0, x = 330)
        #self.container.place(x = 340, y = 0)
        img = Image.open('../src/img/lol_logo.png')
        width, height = img.size
        img = img.resize((width // 2, height // 2), Image.ANTIALIAS)
        self.logoImg = ImageTk.PhotoImage(img)
        self.painel = Label(self.container, image=self.logoImg, bg = bg)
        self.painel.image = self.logoImg
        self.painel.pack(anchor=W, fill=Y, side=TOP)
        
        #Botão para voltar
        self.button = Frame(self.root)
        self.button.pack()
        self.button.place(x=30, y=20)
        self.back = Button(self.button, text="◄ VOLTAR", bg="Grey10", fg="Grey90", font=("Arial Black", "13", "bold",
                                                                                        "italic"),
                        bd=2, activebackground="Grey20", activeforeground="Grey90",
                        relief="solid", height=1, width=15, command=self.close)
        self.back.pack()



    def close(self):
        self.root.destroy()
        from components import menu
        self.menuG = menu.MenuAut()

        #Lista de ultimas partidas jogadas pelo invocador
        self.matches = api_service.getLastMatches(self.invocador.accountId, key)
        #Id dos campeões mais jogados
        self.idsMains = menu_service.mostPlayedChampions(self.invocador.id, self.key, idC=True)
        #Ids dos campeões mais jogados ultimamente
        self.idsLast = api_service.filterMostPlayedChampions(self.key, self.matches, self.invocador)
        
        #Ultimas partidas dos campeões mais jogados pelo invocador.
        self.lastMainMatches = api_service.filterMatchesByChampions(self.key, self.matches, self.idsMains, self.invocador)
        print(self.lastMainMatches)
        #Partidas dos campeões mais jogados ultimamente pelo invocador.
        self.lastMostMatches = api_service.filterMatchesByChampions(self.key, self.matches,self.idsLast, self.invocador)
        print(self.lastMostMatches)
        #Convertendo os ids para objetos do tipo campeão
        self.listaChamp1 = [menu_service.champById(c) for c in self.lastMainMatches.keys()]
        self.listaChamp2 = [menu_service.champById(c) for c in self.lastMostMatches.keys()]
        
        

    def renderChampions(self):
        self.mainsFrame = Frame(self.root, bd = 2, bg= "white",anchor = W)
        self.mainsFrame.pack(side = LEFT)
        
        self.playedFrame = Frame(self.root, bd = 2, bg= "white",anchor = W)
        self.mainsFrame.pack(side = RIGHT)