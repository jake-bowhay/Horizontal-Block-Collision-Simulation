import tkinter


class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.Run = tkinter.Button(self)
        self.Run['text'] = 'Run Simulation'
        self.Run['command'] = print('Run')
        self.Run.pack(side='top')


root = tkinter.Tk()
app = Application(master=root)
app.mainloop()
