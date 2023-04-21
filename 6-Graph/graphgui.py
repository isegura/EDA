from graph import *
from sympy.solvers import solve
from sympy import Symbol
import tkinter as tk
import math

class GraphGUI:
    def __init__(self, graph: Graph = None):
        # PAD AÑADE SEPARACIÓN
        # create the main window and start the GUI
        root = tk.Tk()
        root.title('Graph')
        root.geometry('600x600')
        root.resizable(False, False)
        root.mainloop()

class Node:
    def __init__(self, canvas: tk.Canvas, radius:int, posx: int, posy: int, bg: str = "White", text: str = ""):
        self.radius = radius
        self.pos_x = posx
        self.pos_y = posy
        self.circle = canvas.create_oval(self.pos_x, self.pos_y, self.pos_x + self.radius*2, self.pos_y + self.radius*2, fill=bg, width=2)

class Edge:
    def __init__(self, canvas: tk.Canvas, start: Node, end: Node):
        self.start = self.__calculate_start(start)
        self.end = self.__calculate_end(end)
        self.line = canvas.create_line(self.start[0], self.start[1], self.end[0], self.end[1], arrow=tk.LAST)

    def __calculate_start(self, start: Node) -> tuple:
        return (start.pos_x + start.radius, start.pos_y + start.radius)

    def __calculate_end(self, end: Node) -> tuple:
        center_end = (end.pos_x + end.radius, end.pos_y + end.radius)

        x1 = self.start[0]
        y1 = self.start[1]
        x2 = center_end[0]
        y2 = center_end[1]

        v1 = x2 - x1
        v2 = y2 - y1
        x = Symbol('x')
        print(solve((x - center_end[0])**2 + (((v2*x + v2*center_end[0] + v1*center_end[1])/v2)-center_end[1])**2- end.radius**2, x))
        """edge_angle = math.atan2(y, x) * (180.0 / math.pi)
        print(edge_angle)
        x = math.cos(math.radians(edge_angle)) * end.radius
        y = math.sin(math.radians(edge_angle)) * end.radius"""
        #return (center_end[0] - int(x), center_end[0] - + int(y))




labels = ['A', 'B', 'C', 'D', 'E']
g = Graph(labels)

# Now, we add the edges
g.add_edge('A', 'C', 12)  # A->(12)C
g.add_edge('A', 'D', 60)  # A->(60)D
g.add_edge('B', 'A', 10)  # B->(10)A
g.add_edge('C', 'B', 20)  # C->(20)B
g.add_edge('C', 'D', 32)  # C->(32)D
g.add_edge('E', 'A', 7)   # E->(7)A

# Creamos la ventana
root = tk.Tk()

# Creamos el canvas y lo añadimos a la ventana
canvas = tk.Canvas(root, width=600, height=600)
canvas.pack(padx=10, pady=10)

# Creamos los círculos como óvalos con el mismo ancho y alto para que sean circulares
circle1 = Node(canvas, 50, 100, 100)
circle2 = Node(canvas, 50, 200, 350)

# Creamos una línea que una los círculos
line = Edge(canvas, circle1, circle2)

# Mostramos la ventana
root.mainloop()
