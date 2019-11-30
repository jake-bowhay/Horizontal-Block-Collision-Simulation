import tkinter
from block_simulator import Simulation


class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.NumberOfBlocks = 1
        self.create_widgets(master)

    def create_widgets(self, master):
        tkinter.Label(master, text='Horizontal Block Collision Simulator',
                      font=('Lucida Grande', 30)).grid(row=0, column=1, columnspan=3, sticky='we')

        tkinter.Button(master, text='Add Block',command=lambda: self.generate_button_row(master, self.NumberOfBlocks))\
            .grid(row=2, column=1)

        tkinter.Button(master, text='Remove Block').grid(row=2, column=2)

        tkinter.Button(master, text='Run Simulation', command=lambda: self.launch_simulation()).grid(row=2, column=3)

        tkinter.Label(master, text='Mass').grid(row=3, column=2)
        tkinter.Label(master, text='Elasticity').grid(row=3, column=3)

        for row in range(1, 3):
            self.generate_button_row(master, row)

    def generate_button_row(self, master, BlockNumber):
        RowNumber = BlockNumber + 3
        tkinter.Label(master, text='Block {}'.format(BlockNumber)).grid(row=RowNumber, column=1, sticky='w')
        tkinter.Entry(master).grid(row=RowNumber, column=2)
        tkinter.Entry(master).grid(row=RowNumber, column=3)
        self.NumberOfBlocks += 1

    def launch_simulation(self):
        simulation = Simulation(1280, 720, "Block Collision Simulator", resizable=False)


root = tkinter.Tk()
root.title('Block Simulator')
app = Application(master=root)
app.mainloop()
