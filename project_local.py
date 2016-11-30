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

##########################
#HELPERS
##########################
    
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

#get all possible lines to be drawn    
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

#get sorted, x and y separated lists of lines drawn
def get_x_y_lines(lines,max_line):
    x_lines=[0,max_line]
    y_lines=[0,max_line]
    for line in lines:
        if line[1] == 0:
            x_lines.append(line[0])
        else:
            y_lines.append(line[0])
    return sorted(x_lines),sorted(y_lines)

#determine if there are collisions in a potential solution
def collisions(points,lines):
    n=len(points)+1
    x_interval,y_interval=get_x_y_lines(lines,n)
    boxes=[]
    for point in points:
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

#create a list of all lines to try adding (all possible lines not in the solution)
def generate_possible_lines(points,lines_drawn):
    all_possible = get_possible(points)
    for line in lines_drawn:
        if line in all_possible:
            all_possible.remove(line)
    return(all_possible)

#try to find a solution by removing all combinations of two lines and adding one line
def remove_line(points,lines_drawn):
    x = get_combinations(lines_drawn)
    possible_lines = generate_possible_lines(points,lines_drawn)
    #print("Possible Lines",possible_lines)
    sol=[]
    for pair in x:
        lines_drawn.remove(pair[0])
        lines_drawn.remove(pair[1])
        possible_lines.append(pair[0])
        possible_lines.append(pair[1])
        for possible_line in possible_lines:
            lines_drawn.append(possible_line)
            #print("Checking... Removed:",pair,"Added:",possible_line)
            #plot(points,lines_drawn)
            if not collisions(points,lines_drawn):
                #print("Removed:",pair,"Added",possible_line)
                #sol.append(copy.copy(lines_drawn))
                return copy.copy(lines_drawn)
            lines_drawn.remove(possible_line)
        lines_drawn.insert(0,pair[1])
        lines_drawn.insert(0,pair[0])
        possible_lines.remove(pair[0])
        possible_lines.remove(pair[1])
    #return sol
    return None

##########################
#SOLUTION
##########################

def solution(points):
    sol,y_lines = get_all_possible(points)
    best_sol = copy.copy(sol)
    while sol:
        if len(sol)<len(best_sol):
            best_sol = copy.copy(sol)
        sol = remove_line(points,sol)
    return best_sol
    
def read_file(filename):
    points = []
    with open(os.getcwd()+'/input/'+filename, 'r') as f:
        inpt = f.readlines()
        for point in inpt[1:]:
            point = point.split(' ')
            points.append(((int(point[0])),(int(point[1]))))
    return points

##########################
# Main Program: Import Data
##########################

if __name__ == "__main__":
    print("##########################")
    print("Running Local Algorithm")
    print("##########################")
    
    for filename in os.listdir(os.getcwd()+'/input'):
        points = read_file(filename)
        print(filename)
        output = solution(points)
        with open(os.getcwd()+'/output_local/'+filename, 'w') as o_file:
            o_file.write(str(len(output))+'\n')
            for point in output:
                if point[1] == 0:
                    o_file.write('v '+str(point[0])+'\n')
                else:
                    o_file.write('h '+str(point[0])+'\n')
        print("write success")


