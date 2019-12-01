import tkinter
from tkinter import messagebox
from block_simulator import Simulation


class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.NumberOfBlocks = 0
        self.BlockRows = []
        self.create_widgets(master)

    def create_widgets(self, master):
        tkinter.Label(master, text='Horizontal Block Collision Simulator',
                      font=('Lucida Grande', 30)).grid(row=0, column=1, columnspan=3, sticky='we')

        tkinter.Button(master, text='Add Block', command=lambda: self.generate_button_row(master))\
            .grid(row=2, column=1)

        tkinter.Button(master, text='Remove Block', command=lambda: self.delete_button_row()).grid(row=2, column=2)

        tkinter.Button(master, text='Run Simulation', command=lambda: self.launch_simulation()).grid(row=2, column=3)

        tkinter.Label(master, text='Mass').grid(row=3, column=2)
        tkinter.Label(master, text='Elasticity').grid(row=3, column=3)

        for row in range(1, 3):
            self.generate_button_row(master)

    def generate_button_row(self, master):
        print(self.NumberOfBlocks)
        if self.NumberOfBlocks < 5:
            self.NumberOfBlocks += 1
            Row = []
            RowNumber = self.NumberOfBlocks + 4
            Row.append(tkinter.Label(master, text='Block {}'.format(self.NumberOfBlocks)))
            for i in range(2):
                Row.append(tkinter.Entry(master))
            for x, Item in enumerate(Row):
                Item.grid(row=RowNumber, column=x + 1)
            self.BlockRows.append(Row)
        else:
            messagebox.showwarning('Maximum Number Exceeded', "The maximum number of blocks that can be simulated is 5")

    def delete_button_row(self):
        try:
            LastRow = self.BlockRows.pop()
        except:
            messagebox.showerror('Error', 'No block to delete')
        else:
            for Item in LastRow:
                Item.grid_forget()
            self.NumberOfBlocks -= 1

    def launch_simulation(self):
        simulation = Simulation(1280, 720, "Block Collision Simulator", resizable=False)


root = tkinter.Tk()
root.title('Block Simulator')
app = Application(master=root)
app.mainloop()
