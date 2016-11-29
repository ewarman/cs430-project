
# coding: utf-8

# In[21]:

##########################
# CS 430 Final Project
# Emily Warman, Rachael Affenit
# Local Approach
##########################

import os
import copy
import itertools
import matplotlib.pyplot as plt
import math
import numpy as np


# In[22]:

get_ipython().magic('matplotlib inline')

def plot(points,lines):
    plt.scatter(*zip(*points))
    axes = plt.gca()
    #plot lines drawn
    for line in lines:
        if line[1]==0:
            plt.plot([line[0], line[0]],[0,len(points)], color='b', linestyle='-',linewidth=2)
        else:
            plt.plot([0,len(points)],[line[0],line[0]], color='b', linestyle='-', linewidth=2)
    plt.show()
    
#get all permutations of a list of possible lines
def get_combinations(lines):
    return itertools.combinations(lines,2)

#make a list of possible lines (range function that takes floats)
def drange(x, y, jump):
    r=[]
    while x < y:
        r.append(float(x))
        x += jump
    return r

#create lists of possible points (min x to max x, min y to max y)
#O(nlogn)
def get_all_possible(points):
    x_sort = sorted(points, key=lambda x: x[0])
    y_sort = sorted(points, key=lambda x: x[1])
    x_min = x_sort[0][0]
    x_max = x_sort[-1][0]
    y_min = y_sort[0][1]
    y_max = y_sort[-1][1]
    x = [0]*len(x_sort)
    y = [1]*len(y_sort)
    
    return (list(zip(drange(x_min+.5,x_max+.5,1),x))), (list(zip(drange(y_min+.5,y_max+.5,1),y)))
    #return drange(x_min+.5,x_max+.5,1)
    
def get_possible(points):
    x_sort = sorted(points, key=lambda x: x[0])
    y_sort = sorted(points, key=lambda x: x[1])
    x_min = x_sort[0][0]
    x_max = x_sort[-1][0]
    y_min = y_sort[0][1]
    y_max = y_sort[-1][1]
    x = [0]*len(x_sort)
    y = [1]*len(y_sort)
    
    return (list(zip(drange(x_min+.5,x_max+.5,1),x))) + (list(zip(drange(y_min+.5,y_max+.5,1),y)))
    #return drange(x_min+.5,x_max+.5,1)

def get_x_y_lines(lines):
    x_lines=[]
    y_lines=[]
    for line in lines:
        if line[1] == 0:
            x_lines.append(line[0])
        else:
            y_lines.append(line[0])
    return x_lines,y_lines

def collisions(points,lines):
    n=len(points)
    #if pair[0] not in lines:
       # print(pair[0],lines)
    #else:
     #   lines.remove(pair[0])
    #if pair[1] not in lines:
    #    print(pair[1],lines)
    #else:
    #    lines.remove(pair[1])
    #if possible_line in lines:
    #    print(possible_line,lines)
    #else:
    #    lines.append(possible_line)
    x_lines,y_lines=get_x_y_lines(lines)
    x_interval = [0]
    x_interval.extend(x_lines)
    x_interval.append(len(points)+1)
    y_interval = [0]
    y_interval.extend(y_lines)
    y_interval.append(len(points)+1)
    boxes=[]
    for point in points:
        #find box of point
        #print(point)
        x_box=0
        while point[0]>=x_interval[x_box] and x_box<len(x_interval):
            x_box+=1
        y_box=0
        while point[1]>=y_interval[y_box] and y_box<len(y_interval):
            y_box+=1
        box = (x_box-1,y_box-1)
        if box in boxes:
            return True
        else:
            boxes.append(box)
    return False

def generate_possible_lines(points,lines_drawn):
    all_possible = get_possible(points)
    for line in lines_drawn:
        if line in all_possible:
            all_possible.remove(line)
    return(all_possible)


# In[23]:

def solution(points,lines_drawn):
    print(len(lines_drawn))
    if len(lines_drawn)==math.ceil(math.sqrt(len(points))*2)-2:
        return(lines_drawn)
    
    x = get_combinations(lines_drawn)
    possible_lines = generate_possible_lines(points,lines_drawn)
    
    for pair in x:
        lines_drawn.remove(pair[0])
        lines_drawn.remove(pair[1])
        all_collisions=True
        for possible_line in possible_lines:
            lines_drawn.append(possible_line)
            if collisions(points,lines_drawn)==False:
                all_collisions=False
                solution(points,lines_drawn)
                #print("CALL TO SOLUTION:",lines_drawn,possible_lines)
                #solution(points,lines_drawn)
                #sol_stack.append(copy.copy(lines_drawn))
            lines_drawn.remove(possible_line)
        lines_drawn.append(pair[0])
        lines_drawn.append(pair[1])
        if all_collisions:
            return(lines_drawn)
    #print(sol_stack)
    return(lines_drawn)


# In[27]:

##########################
# Main Program: Import Data
##########################
#for filename in os.listdir(os.getcwd()+'/input'):
    
def read_file(filename):
    points = []
    with open('input/'+filename, 'r') as f:
        inpt = f.readlines()
        for point in inpt[1:]:
            point = point.split(' ')
            points.append(((int(point[0])),(int(point[1]))))
    return points

points = read_file('instance04.txt')
all_x_lines,all_y_lines=get_all_possible(points)
print(len(points))
ld = solution(points,all_x_lines)
#print(ld)
plot(points,ld)


# In[20]:
vh = np.zeros(len(ld))
print (len(ld))
for i in range (0,len(ld)):
    if (vh[i] == 0):
        print ("v ", ld[i][0])
    elif (vh[i] == 1):
        print ("h ", ld[i][1])


# In[13]:

possible_lines = generate_possible_lines(points,all_x_lines)
#print(possible_lines)


# In[7]:
