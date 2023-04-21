import tkinter as tk
import math
from graph import *

class GraphGUI:
    def __init__(self, graph: Graph = None):
        if type(graph) != Graph:
            raise TypeError("The parameter must be a Graph object")
        self.graph = graph
        # create the main window and start the GUI
        root = tk.Tk()
        root.title('Graph')
        root.resizable(False, False)

        # Create the canvas
        canvas = tk.Canvas(root, width=600, height=600)
        canvas.pack(padx=10, pady=10)

        circle1 = Node(canvas, 50, 500, 500)
        circle2 = Node(canvas, 50, 350, 100)
        circle3 = Node(canvas, 50, 100, 500)

        # Creamos una línea que una los círculos
        Edge(canvas, circle1, circle2)
        Edge(canvas, circle2, circle3)
        Edge(canvas, circle2, circle1)

        root.mainloop()

class Node:
    def __init__(self, canvas: tk.Canvas, radius:int, posx: int, posy: int, bg: str = "White", text: str | None = None):
        self.radius = radius
        self.pos_x = posx
        self.pos_y = posy
        self.circle = canvas.create_oval(self.pos_x, self.pos_y, self.pos_x + self.radius*2, self.pos_y + self.radius*2, fill=bg, width=2)
        if text:
            self.text = canvas.create_text(self.pos_x + self.radius, self.pos_y + self.radius, text=text)

class Edge:
    def __init__(self, canvas: tk.Canvas, start: Node, end: Node, weight: int =1):
        self.start = self.__calculate_start(start, end)
        self.end = self.__calculate_end(start, end)
        self.line = canvas.create_line(self.start[0], self.start[1], self.end[0], self.end[1], arrow=tk.LAST)
        canvas.create_text((self.start[0] + self.end[0])//2, (self.start[1] + self.end[1])//2, text=str(weight))
        canvas.create_window((self.start[0] + self.end[0])//2, (self.start[1] + self.end[1])//2, window=tk.Label(canvas, text=str(weight)))

    def __calculate_start(self, start: Node, end: Node) -> tuple:
        """
        It calculates the initial position of the arrow that connects the nodes "start" and "end"
        :param start: Node
        :param end: Node
        :return: tuple with the initial position of the arrow
        """
        center_start = (start.pos_x + start.radius, start.pos_y + start.radius)
        center_end = (end.pos_x + end.radius, end.pos_y + end.radius)

        x1 = center_start[0]
        y1 = center_start[1]
        x2 = center_end[0]
        y2 = center_end[1]

        x = x2 - x1
        y = y2 - y1
        edge_angle = math.atan2(y, x) * (180.0 / math.pi)
        x = math.cos(math.radians(edge_angle)) * start.radius
        y = math.sin(math.radians(edge_angle)) * start.radius
        return (center_start[0] + int(x), center_start[1] + int(y))

    def __calculate_end(self, start: Node, end: Node) -> tuple:
        """
        It calculates the final position of the arrow that connects the nodes "start" and "end"
        :param start: Node
        :param end: Node
        :return: tuple with the final position of the arrow
        """
        center_start = (start.pos_x + start.radius, start.pos_y + start.radius)
        center_end = (end.pos_x + end.radius, end.pos_y + end.radius)

        x1 = center_start[0]
        y1 = center_start[1]
        x2 = center_end[0]
        y2 = center_end[1]

        x = x2 - x1
        y = y2 - y1
        edge_angle = math.atan2(y, x) * (180.0 / math.pi)
        x = math.cos(math.radians(edge_angle)) * end.radius
        y = math.sin(math.radians(edge_angle)) * end.radius
        return  (center_end[0] - int(x), center_end[1] - int(y))




labels = ['A', 'B', 'C', 'D', 'E']
g = Graph(labels)

# Now, we add the edges
g.add_edge('A', 'C', 12)  # A->(12)C
g.add_edge('A', 'D', 60)  # A->(60)D
g.add_edge('B', 'A', 10)  # B->(10)A
g.add_edge('C', 'B', 20)  # C->(20)B
g.add_edge('C', 'D', 32)  # C->(32)D
g.add_edge('E', 'A', 7)   # E->(7)A

GraphGUI(g)