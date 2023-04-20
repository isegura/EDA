from graph import *
import tkinter as tk

class GraphGUI:
    def __init__(self, master):
        self.master = master
        self.vertices = []

        # create a listbox to display vertices
        self.vertex_listbox = tk.Listbox(self.master)
        self.vertex_listbox.pack(side=tk.LEFT, padx=100, pady=100)


# create the main window and start the GUI
root = tk.Tk()
app = GraphGUI(root)
root.mainloop()

labels = ['A', 'B', 'C', 'D', 'E']
g = Graph(labels)

# Now, we add the edges
g.add_edge('A', 'C', 12)  # A->(12)C
g.add_edge('A', 'D', 60)  # A->(60)D
g.add_edge('B', 'A', 10)  # B->(10)A
g.add_edge('C', 'B', 20)  # C->(20)B
g.add_edge('C', 'D', 32)  # C->(32)D
g.add_edge('E', 'A', 7)   # E->(7)A
