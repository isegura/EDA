import tkinter as tk
import math

class GraphGUI:
    def __init__(self, graph, node_radius: int = 40, scr_width: int = 600, scr_height: int = 600):
        """
        Creates a GraphGUI object, which will display the graph in a external window. Nodes can be moved with the mouse.
        The creation of the window will stop the execution of the program until the window is closed. Thus, it is recommended
        to create the GraphGUI object at the end of the program.
        :param graph: The graph to be displayed
        :param node_radius: The radius of the nodes (default 40)
        :param scr_width: The width of the window (default 600)
        :param scr_height: The height of the window (default 600)
        """
        if type(node_radius) != int:
            raise TypeError("The parameter node_radius must be an integer")
        if type(scr_width) != int or type(scr_height) != int:
            raise TypeError("The parameters scr_width and scr_height must be integers")
        if node_radius < 10 or node_radius > 100:
            raise ValueError("The parameter node_radius must be a value between 10 and 100")
        if scr_width < 200 or scr_height < 200:
            raise ValueError("The parameters scr_width and scr_height must be values greater than 200")
        if scr_width > 1000 or scr_height > 1000:
            raise ValueError("The parameters scr_width and scr_height must be values less than 1000")
        self.graph = graph
        # create the main window and start the GUI
        root = tk.Tk()
        root.title('GraphGUI')
        root.resizable(False, False)

        # Create the canvas
        self.canvas = tk.Canvas(root, width=scr_width, height=scr_height)
        self.canvas.pack(padx=10, pady=10)

        # Preparation for the nodes display
        scr_center = (scr_width//2, scr_height//2)
        display_radius = min(scr_width, scr_height)//2 - node_radius - 10
        arch_angle = 360/len(graph._vertices)
        first_node_pos = (scr_center[0] - node_radius, scr_center[1] - node_radius)

        # Display the nodes
        self.nodes =[]
        i = 0
        angle = 0
        for vertex in self.graph._vertices:
            if i == 0:
                self.nodes.append(Node(self.canvas, node_radius, first_node_pos[0], first_node_pos[1], text=str(vertex)))
            else:
                self.nodes.append(Node(self.canvas,
                                       node_radius,
                                       scr_center[0] - node_radius - display_radius*math.sin(math.radians(angle)),
                                       scr_center[1] - node_radius - display_radius*math.cos(math.radians(angle)),
                                       text=str(vertex)))
            i += 1
            angle += arch_angle

        # Display the edges
        i = 0
        self.edges = []
        for vertex in self.graph._vertices:
            for adj in self.graph._vertices[vertex]:
                for node in self.nodes:
                    if node.id == str(adj.vertex):
                        self.edges.append(Edge(self.canvas, self.nodes[i], node, adj.weight))
                        node.asociated_edges_IN.append(self.edges[-1])
                        self.nodes[i].asociated_edges_OUT.append(self.edges[-1])
            i += 1

        self.canvas.tag_bind("movil", "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind("movil", "<Button1-Motion>", self.move)
        self.selected_node = None

        root.mainloop()

    def on_press(self, event):
        node = self.canvas.find_withtag(tk.CURRENT)
        self.selected_node = (node, event.x, event.y)

    def move(self, event):
        x, y = event.x, event.y
        node, x0, y0 = self.selected_node
        for i in self.nodes:
            if i.circle == node[0] or i.text == node[0]:
                self.canvas.move(i.circle, x - x0, y - y0)
                self.canvas.move(i.text, x - x0, y - y0)
                i.pos_x += x - x0
                i.pos_y += y - y0
                for edge in i.asociated_edges_IN:
                    edge_start = edge.start_node
                    weight = edge.weight
                    i.asociated_edges_IN.remove(edge)
                    self.canvas.delete(edge.line)
                    self.canvas.delete(edge.window)
                    del edge
                    edge = Edge(self.canvas, edge_start, i, weight)
                    i.asociated_edges_IN.append(edge)
                for adj in self.graph._vertices[i.id]:
                    for nd in self.nodes:
                        if nd.id == str(adj.vertex):
                            for edge in nd.asociated_edges_IN:
                                if edge.start_node == i:
                                    edge_end = edge.end_node
                                    weight = edge.weight
                                    nd.asociated_edges_IN.remove(edge)
                                    self.canvas.delete(edge.line)
                                    self.canvas.delete(edge.window)
                                    del edge
                                    edge = Edge(self.canvas, i, edge_end, weight)
                                    nd.asociated_edges_IN.append(edge)


        self.selected_node = (node, x, y)

class Node:
    def __init__(self, canvas: tk.Canvas, radius:int, posx: int, posy: int, text: str, bg: str = "White"):
        self.asociated_edges_IN = []
        self.asociated_edges_OUT = []
        self.canvas = canvas
        self.id = text
        self.radius = radius
        self.pos_x = posx
        self.pos_y = posy
        self.circle = canvas.create_oval(self.pos_x, self.pos_y, self.pos_x + self.radius*2, self.pos_y + self.radius*2, fill=bg, width=2)
        self.text = canvas.create_text(self.pos_x + self.radius, self.pos_y + self.radius, text=text)
        canvas.addtag_enclosed("movil", self.pos_x - 3, self.pos_y - 3, self.pos_x + self.radius * 2 + 3, self.pos_y + self.radius * 2 + 3)

class Edge:
    def __init__(self, canvas: tk.Canvas, start: Node, end: Node, weight: int =1):
        self.start_node = start
        self.end_node = end
        self.weight = weight
        self.start = self.__calculate_start(start, end)
        self.end = self.__calculate_end(start, end)
        self.line = canvas.create_line(self.start[0], self.start[1], self.end[0], self.end[1], arrow=tk.LAST, width=1.5)
        self.window = canvas.create_window((self.start[0] + self.end[0])//2, (self.start[1] + self.end[1])//2, window=tk.Label(canvas, text=str(weight)))

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
