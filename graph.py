# -*- coding: utf-8 -*-
"""graph-dictionaryWD.ipynb

# Graph implementation using a Python dictionary

This implementation allows to represent any kind of graphs.
"""

class AdjacentVertex:
    def __init__(self,vertex,weight):
        self.vertex=vertex
        self.weight=weight
  
    def __str__(self):
        return '('+str(self.vertex)+','+str(self.weight)+')'

class Graph():
    def __init__(self,labels,directed=True):
        self.labels=labels
        self.vertices={}
        for v in self.labels:
            self.vertices[v]=[]
        self.directed=directed
    
    def addEdge(self, start, end, weight=0):
        if start not in self.labels:
            print(start,' does not exist!')
            return
        if end not in self.labels:
            print(end,' does not exist!')
            return
        
        self.vertices[start].append(AdjacentVertex(end,weight))
        if self.directed==False:
            self.vertices[end].append(AdjacentVertex(start,weight))
      
    def containsEdge(self, start, end):
        if start not in self.labels:
            print(start,' does not exist!')
            return 0
        if end not in self.labels:
            print(end,' does not exist!')
            return 0

        for adj in self.vertices[start]:
            if adj.vertex==end:
                return adj.weight
        return 0

    def removeEdge(self,start,end):
        if start not in self.labels:
            print(start,' does not exist!')
            return
        if end not in self.labels:
            print(end,' does not exist!')
            return

        for adj in self.vertices[start]:
            if adj.vertex==end:
                self.vertices[start].remove(adj)
        if self.directed==False:
            for adj in self.vertices[end]:
                if adj.vertex==start:
                    self.vertices[end].remove(adj)
  
    def __str__(self):
        result=''
        for v in self.labels:
            result+='\n'+str(v)+':'
            for adj in self.vertices[v]:
                result+=str(adj)
            
        return result
