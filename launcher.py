import tkinter
from tkinter import messagebox
from block_simulator import Simulation


class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.NumberOfBlocks = 0
        self.BlockRows = []
        self.Velocity = None
        self.ValidatorVelocity = (self.register(self.validate), '%P', 1, 100)
        self.ValidatorMass = (self.register(self.validate), '%P', 1, 1000000)
        self.ValidatorElasticity = (self.register(self.validate), '%P', 0, 1)
        self.create_widgets(master)

    def create_widgets(self, master):
        tkinter.Label(master, text='Horizontal Block Collision Simulator',
                      font=('Lucida Grande', 30)).grid(row=0, column=1, columnspan=3, sticky='we')

        tkinter.Button(master, text='Add Block', command=lambda: self.generate_button_row(master)) \
            .grid(row=2, column=1)

        tkinter.Button(master, text='Remove Block', command=lambda: self.delete_button_row()).grid(row=2, column=2)

        tkinter.Button(master, text='Run Simulation', command=lambda: self.launch_simulation()).grid(row=2, column=3)

        tkinter.Label(master, text='Starting velocity (1-100):').grid(row=3, column=1)
        self.Velocity = tkinter.Entry(master, validate='key', validatecommand=self.ValidatorVelocity)
        self.Velocity.grid(row=3, column=2)

        tkinter.Label(master, text='Mass').grid(row=4, column=2)
        tkinter.Label(master, text='Elasticity').grid(row=4, column=3)

        for row in range(2):
            self.generate_button_row(master)

    def validate(self, Value, MinValue,MaxValue):
        try:
            IntValue = float(Value)
            if float(MinValue) <= IntValue <= float(MaxValue):
                return True
            else:
                messagebox.showerror('Value out of Range', 'Value must be between {}-{}'.format(MinValue, MaxValue))
                return False
        except ValueError:
            if len(Value) == 0:
                return True
            messagebox.showerror('Invalid input', 'Value must be an number')
            return False

    def generate_button_row(self, master):
        if self.NumberOfBlocks < 10:
            self.NumberOfBlocks += 1
            Row = []
            RowNumber = self.NumberOfBlocks + 4
            Row.append(tkinter.Label(master, text='Block {}'.format(self.NumberOfBlocks)))
            Row.append(tkinter.Entry(master, validate='key', validatecommand=self.ValidatorMass))
            Row.append(tkinter.Entry(master, validate='key', validatecommand=self.ValidatorElasticity))
            for x, Item in enumerate(Row):
                Item.grid(row=RowNumber, column=x + 1)
            self.BlockRows.append(Row)
        else:
            messagebox.showwarning('Maximum Number Exceeded', "The maximum number of blocks that can be simulated is 10")

    def delete_button_row(self):
        if len(self.BlockRows) == 1:
            messagebox.showerror('Can\'t delete', 'Simulation must have at least one block')
        else:
            LastRow = self.BlockRows.pop()
            for Item in LastRow:
                Item.grid_forget()
            self.NumberOfBlocks -= 1

    def launch_simulation(self):
        try:
            Data = {'StartVelocity': float(self.Velocity.get()), 'Blocks': []}
            for Row in self.BlockRows:
                RowData = {'Mass': float(Row[1].get()), 'Elasticity': float(Row[2].get())}
                Data['Blocks'].append(RowData)
        except ValueError:
            messagebox.showerror('Invalid Input', 'Values cannot be blank')
        else:
            Simulation(Data, 1280, 720, "Block Collision Simulator", resizable=False)


root = tkinter.Tk()
root.title('Block Simulator')
app = Application(master=root)
app.mainloop()
