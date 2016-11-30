
# coding: utf-8

# In[17]:

##########################
# CS 430 Final Project
# Rachael Affenit, Emily Warman
# Greedy Approach
##########################

import os
import copy
import itertools
import matplotlib.pyplot as plt
import math


# In[18]:

##########################
# Helper Functions & Global Vars
##########################

# Global vars
points = []

#import test file
def importf(file):
    filepath = os.getcwd()+'/input/'
    with open(filepath+file, 'r') as f:
        inpt = f.readlines()
        for point in inpt[1:]:
            point = point.split(' ')
            points.append(((int(point[0])),(int(point[1]))))

#define plot function
get_ipython().magic('matplotlib inline')
def plot(points,graph,x_lines,y_lines):
    plt.scatter(*zip(*points))
    axes = plt.gca()
    #plot lines drawn
    for line in x_lines:
        plt.plot([line, line],[0,len(points)], color='b', linestyle='-',linewidth=2)
    for line in y_lines:
        plt.plot([0,len(points)],[line,line], color='b', linestyle='-', linewidth=2)
    #plot remaining
    for point in graph.keys():
        for p2 in graph[point]:
            plt.plot([point[0], p2[0]], [point[1], p2[1]], linestyle='-', linewidth=2)
    plt.show()

#get all permutations of a list of possible lines
def get_permutations(lines):
    return itertools.permutations(lines)

#make a list of possible lines (range function that takes floats)
def drange(x, y, jump):
    r=[]
    while x < y:
        r.append(float(x))
        x += jump
    return r

#create lists of possible points (min x to max x, min y to max y)
def get_all_possible(points):
    x_sort = sorted(points, key=lambda x: x[0])
    y_sort = sorted(points, key=lambda x: x[1])
    x_min = x_sort[0][0]
    x_max = x_sort[-1][0]
    y_min = y_sort[0][1]
    y_max = y_sort[-1][1]
    
    return (drange(x_min+.5,x_max+.5,1), drange(y_min+.5,y_max+.5,1))

#make a graph of all possible graph points
def make_graph(points):
    initial_graph = dict.fromkeys(points)
    for point in initial_graph.keys():
        c_copy = copy.copy(points)
        c_copy.remove(point)
        initial_graph[point] = c_copy
    return initial_graph

#find how many points are separated by a given line
def separate(gg, line, idx):
    left = []
    right = []
    separated = 0
    
    #mark points left and right (or above and below) the line to be drawn
    for point in gg.keys():
        if point[idx] < line:
            left.append(point)
        if point[idx] > line:
            right.append(point)
    #separate the points
    for point in gg.keys():
        if point in left:
            for p2 in right:
                if p2 in gg[point]:
                    separated += 1
        if point in right:
            for p2 in left:
                if p2 in gg[point]:
                    separated += 1
    return separated

#draw a new parallel line to separate points
def draw(gg, line, idx):
    left = []
    right = []
    separated = 0
    
    #mark points left and right (or above and below) the line to be drawn
    for point in gg.keys():
        if point[idx] < line:
            left.append(point)
        if point[idx] > line:
            right.append(point)
    #separate the points
    for point in gg.keys():
        if point in left:
            for p2 in right:
                if p2 in gg[point]:
                    gg[point].remove(p2)
                    separated += 1
        if point in right:
            for p2 in left:
                if p2 in gg[point]:
                    gg[point].remove(p2)
                    separated += 1
    return gg, separated

def read_file(filename):
    points = []
    with open(os.getcwd()+'/input/'+filename, 'r') as f:
        inpt = f.readlines()
        for point in inpt[1:]:
            point = point.split(' ')
            points.append(((int(point[0])),(int(point[1]))))
    return points

def nodes_left(graph):
    for point in graph.keys():
        if graph[point]!=[]:
            return True
    return False


# SEPARATING POINTS BY AXIS-PARALLEL LINES
# 
# Think about the points given as vertices of a graph. Imagine that when there are no lines drawn, no points are separated from each other. The graph is fully connected.
# 
# The figure below represents the example input as a fully connected graph.

# In[19]:

##########################
# Example Separations
##########################

print("##########################################")
print("Separating Points by Axis-Parallel Lines")
print("##########################################")

# Show an example graph
points = []
importf('instanceExample.txt')
print("Example Graph")
plot(points,make_graph(points),[],[])


# When a vertical line is drawn between the points, the connections between the points to the left of the line and right (or top and bottom if horizontal) of the line are broken. When there are no edges in the graph, each point is fully separated from its neighbors. See example below:

# In[20]:

# Show example separations
print("First separation")
graph = make_graph(points)
draw(graph, 2.5, 0)
plot(points,graph,[2.5],[])

print("Second separation")
draw(graph, 2.5, 1)
plot(points,graph,[2.5],[2.5])

print("Third separation")
draw(graph, 1.5, 0)
plot(points,graph,[1.5,2.5],[2.5])


# GREEDY ALGORITHM SOLUTION
# 
# The professor's paper stated that the optimal number of lines to draw is 2*sqrt(n)-2 (n=number of points). This assumption has been made for the sake of our algorithms.
# 
# Our greedy solution algorithm does the following:
# 1. Gets all vertical lines that can be drawn between the leftmost point and rightmost point and all horizontal lines that can be drawn between the topmost point and bottommost point
# 2. Initializes the graph representation shown above
# 3. Calculates the number of lines drawn in an optimal solution
# 4. While the graph is still connected at any point:
#     For every possible horizontal and vertical line to be drawn:
#         simulate separations by the line in the graph
#         if more new separations occur than current best, make this line the new best
#     Add the best line to the output information
#    
#    Return all output information
# 
# The running time of this algorithm would be O(n^4) with the three loops present.
#     The outside while loop iterates through all n nodes in the graph
#     This calls find_best, with a time complexity of O(n^3) due to its call to the O(n^2) method "separate"inside the for loop

# In[21]:

##########################
# Greedy Algorithm Solution
##########################
def find_best(graph, all_lines, lines_drawn, idx):
    best_sep = 0
    best_line = None
    for line in all_lines:
        if line in lines_drawn:
            continue
        else:
            sep = separate(graph, line, idx)
            if sep > best_sep:
                best_line = line
                best_sep = sep
    return best_line, best_sep
            
def segment(points):
    all_x_lines, all_y_lines = get_all_possible(points)
    graph = make_graph(points)
    OPT = math.ceil(math.sqrt(len(points))*2)-2
    
    S = []
    vh = []
    x_lines_drawn = []
    y_lines_drawn = []
    total_lines_drawn = 0
    
    while nodes_left(graph):
        best_line = None
        best_axis = 0
        
        best_line_x, separated_x = find_best(graph, all_x_lines, x_lines_drawn, 0)
        best_line_y, separated_y = find_best(graph, all_y_lines, y_lines_drawn, 1)
        
        if separated_x >= separated_y:
            best_line = best_line_x
            best_axis = 0
        else:
            best_line = best_line_y
            best_axis = 1
        
        if best_axis: 
            y_lines_drawn.append(best_line)
        else: 
            x_lines_drawn.append(best_line)
        
        S.append(best_line)
        vh.append(best_axis)
        total_lines_drawn += 1
        
        graph,sep = draw(graph, best_line, best_axis)

    return (graph,S,vh,total_lines_drawn,x_lines_drawn,y_lines_drawn)


# In[22]:

##########################
# Testing Greedy Algorithm
##########################

print("##########################")
print("Testing Greedy Algorithm")
print("##########################")

points = []
importf('instance_04.txt') ###### CHANGE THIS FILE NAME IN ORDER TO TEST A DIFFERENT INSTANCE FILE ######
graph,S,vh,total_lines,x_lines,y_lines = segment(points)
plot(points,graph,x_lines,y_lines)
print(x_lines)
print(y_lines)
print("")
print (total_lines)
for i in range (0,len(S)):
    if (vh[i] == 0):
        print ("v ", S[i])
    elif (vh[i] == 1):
        print ("h ", S[i])


# In[23]:

##########################
# Example of Algorithm Failure
##########################

print("##########################")
print("Example of Algorithm Failure")
print("##########################")

# Algorithm Result
points = []
importf('instanceFail.txt')
print("Algorithm Result")

graph,S,vh,total_lines,x_lines,y_lines = segment(points)
plot(points,graph,x_lines,y_lines)
print (total_lines)
for i in range (0,len(S)):
    if (vh[i] == 0):
        print ("v ", S[i])
    elif (vh[i] == 1):
        print ("h ", S[i])
        
# Optimal Result
points = []
importf('instanceFail.txt')
print("")
print("Optimal Result")
graph = make_graph(points)

#print("First separation")
draw(graph, 4.5, 0)
#plot(points,graph,[4.5],[])

#print("Second separation")
draw(graph, 4.5, 1)
#plot(points,graph,[4.5],[4.5])

#print("Third separation")
draw(graph, 7.5, 0)
#plot(points,graph,[4.5, 7.5],[4.5])

#print("Fourth separation")
draw(graph, 8.5, 1)
#plot(points,graph,[4.5, 7.5],[4.5, 8.5])

#print("Fifth separation")
draw(graph, 6.5, 0)
#plot(points,graph,[4.5, 7.5, 8.5],[4.5, 8.5])

#print("Sixth separation")
draw(graph, 8.5, 0)
plot(points,graph,[4.5, 7.5, 8.5, 6.5],[4.5, 8.5])

print("6\nv 4.5\nh 4.5\nv 7.5\nh 8.5\nv 6.5\nv 8.5")


# In[24]:

print("##########################")
print("Running Greedy Algorithm")
print("##########################")

if __name__ == "__main__":
    for filename in os.listdir(os.getcwd()+'/input'):
        points = []
        points = read_file(filename)
        print(filename)
        g,S,vh,tot,x,y = segment(points)
        with open(os.getcwd()+'/output_greedy/'+filename, 'w') as o_file:
            o_file.write(str(len(S))+'\n')
            for i in range (0,len(S)):
                if (vh[i] == 0):
                    o_file.write('v '+str(S[i])+'\n')
                elif (vh[i] == 1):
                    o_file.write('h '+str(S[i])+'\n')

        print("write success")


# In[ ]:



