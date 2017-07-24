
from tkinter import*
import threespace as ts_api
import time


#Window
root=Tk()


def nothing():
    print("its just a test")

def start():
    print("WBL")

#Menu
menu=Menu(root)
root.configure(menu=menu)

subMenu= Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="New Project", command=nothing)
subMenu.add_command(label="Extra", command=nothing)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=nothing)

editMenu=Menu(menu)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Redo", command=nothing)


#Table Chart
import tkinter as tk
class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        t = SimpleTable(self, 10,2)
        t.pack(side="top", fill="x")
        t.set(0,0,"IT WORKS")

class SimpleTable(tk.Frame):
    def __init__(self, parent, rows=10, columns=2):
        # use black background so it "peeks through" to 
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tk.Label(self, text="%s/%s" % (row, column), 
                                 borderwidth=0, width=30)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

if __name__ == "__main__":
    app = ExampleApp()

#Status Bar

status= Label(root,text="testing..", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

#Tool Bar

toolbar= Frame(root)
insertButton = Button(toolbar, text="Start", command=start)#while is true, stream
insertButton.pack(side=LEFT, padx=5, pady=50)
#insertButton.config( height = 10, width = 10 )
printButton= Button(toolbar, text="Stop", command=nothing)#pause, then wait fot start
printButton.pack(side=LEFT, padx=5, pady=50)
#printButton.config( height = 50, width = 10 )
resetButton=Button(toolbar,text="Reset", command=nothing)
resetButton.pack(side=LEFT, padx=5, pady=50)
#resetButton.config( height = 50, width = 10 )
connectButton=Button(toolbar,text="Connect", command=nothing)
connectButton.pack(side=LEFT, padx=5, pady=50)
#connectButton.config( height = 50, width = 10 )
disconnectButton=Button(toolbar,text="Disconnect", command=nothing)
disconnectButton.pack(side=LEFT, padx=5, pady=50)
#disconnectButton.config( height = 50, width = 10 )

toolbar.pack(side=BOTTOM, fill=X)


#root window
root.title("Graphical User Interface")
root.geometry("700x600")



        
root.mainloop()



