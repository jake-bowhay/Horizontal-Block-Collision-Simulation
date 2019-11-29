import tkinter
from block_simulator import Simulation

class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.Run = tkinter.Button(self)
        self.Run['text'] = 'Run Simulation'
        self.Run['command'] = lambda: self.launch_simulation()
        self.Run.pack(side='top')

    def launch_simulation(self):
        simulation = Simulation(1280, 720, "Block Collision Simulator", resizable=False)


root = tkinter.Tk()
app = Application(master=root)
app.mainloop()
