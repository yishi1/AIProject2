import math
import random
import matplotlib

from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np


def function_to_optimize(x,y):
    #compute the result of the function
    r = math.sqrt(x**2 + y**2)
    z = round(math.sin(x**2 + 3*y**2) / (0.1 + r**2) + (x**2+5*y**2)*math.exp(1-r**2)/2,5)
    return z


def getneighbors(x,y,step_size,xmin,xmax,ymin,ymax):
    #function to get all neighbors inside the range
    neighbors = []
    if(x+step_size < xmax):
	    neighbors.append([x+step_size,y])
    if(x-step_size > xmin):
	    neighbors.append([x-step_size,y])
    if(x+step_size < xmax and y+step_size < ymax):
	    neighbors.append([x+step_size,y+step_size])
    if(x-step_size > xmin and y-step_size > ymin):
	    neighbors.append([x-step_size,y-step_size])
    if(y+step_size < ymax):
	    neighbors.append([x,y+step_size])
    if(y-step_size > ymin):
	    neighbors.append([x,y-step_size])
    if(x+step_size < xmax and y-step_size > ymin):
	    neighbors.append([x+step_size,y-step_size])
    if(x-step_size > xmin and y+step_size < ymax):
	    neighbors.append([x-step_size,y+step_size])
    return neighbors


def hill_climb(function, step_size, xmin, xmax, ymin, ymax):
    xpath=[]
    ypath=[]
    zpath=[]

    x=round(random.uniform(xmin,xmax),5)
    y=round(random.uniform(ymin,ymax),5)
    z = function_to_optimize(x,y)

    #get path for x, y and z
    xpath.append(x)
    ypath.append(y)
    zpath.append(z)
    findmin=False

    #loop while min is not found
    while (findmin is False):
        myneighbor = getneighbors(x,y,step_size,xmin,xmax,ymin,ymax)
        findmin=True
        for i in myneighbor:
            value = function_to_optimize(i[0],i[1])
            #if the result of neighbor is less than z, replace it
            if (value < z):
                x = round(i[0],5)
                y = round(i[1],5)
                z = value

                #add it to the path
                xpath.append(x)
                ypath.append(y)
                zpath.append(z)
                findmin = False

        #break when we found the min
        if findmin is True:
            #return the path
            return xpath,ypath,zpath

def hill_climb_random_restart(function, step_size, num_restarts, xmin, xmax, ymin, ymax):
    #set a default path
    minxpath,minypath,minzpath = hill_climb(function_to_optimize,step_size,xmin,xmax,ymin,ymax)
    num=0

    while (num < num_restarts):
        xpath,ypath,zpath = hill_climb(function_to_optimize,step_size,xmin,xmax,ymin,ymax)
        num +=1

         #if the result of neighbor is less than minimum z, replace it
        if zpath[-1] < minzpath[-1]:
            minxpath=xpath
            minypath=ypath
            minzpath=zpath

    print("Hill Climbing Random Restart:")
    print("The coordinate of min is:")
    print("X = ",minxpath[-1])
    print("Y = ",minypath[-1])
    print("Z = ",minzpath[-1])
    print()
    return minxpath,minypath,minzpath


def simulated_annealing(function, step_size, max_temp, xmin, xmax, ymin, ymax):
    xpath=[]
    ypath=[]
    zpath=[]

    x = round(random.uniform(xmin,xmax),5)
    y = round(random.uniform(ymin,ymax),5)
    z = function_to_optimize(x,y)

    xpath.append(x)
    ypath.append(y)
    zpath.append(z)

    T = max_temp

    #set the minimum temperature
    min_temp=0.00001
    while (T > min_temp):
        myneighbor = getneighbors(x,y,step_size,xmin,xmax,ymin,ymax)
        for i in myneighbor:
            value = function_to_optimize(i[0],i[1])
            delta = value - z

            #if delta less than 0, replace the value and coordinate of z
            if delta < 0:
                x = round(i[0],5)
                y = round(i[1],5)
                z = value

                xpath.append(x)
                ypath.append(y)
                zpath.append(z)

            else:
                #Compute the probability to move when delta is not less than 0 and determine if it moves or not
                p = math.exp(-delta/T)
                if p >= random.random():
                     x = round(i[0],5)
                     y = round(i[1],5)
                     z = value

                     xpath.append(x)
                     ypath.append(y)
                     zpath.append(z)
        T = T * 0.99

    print("Simulated Annealing:")
    print("The coordinate of min is:")
    print("X = ",x)
    print("Y = ",y)
    print("Z = ",z)
    print()
    return xpath,ypath,zpath

def graph(xpath,ypath,zpath):
    #plot the graph
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)

    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    Z = (np.sin(X**2 + 3*Y**2) / (0.1 + R**2) + (X**2+5*Y**2)*np.exp(1-R**2)/2)

    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, color='white',
                       linewidth=0, antialiased=False)

    ax.set_zlim(-5,5)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    ax.plot(xpath,ypath,zpath)
    plt.show()

def main():
    #get path for each function and plot the graph
    xpath,ypath,zpath=hill_climb(function_to_optimize,0.01,-2.5,2.5,-2.5,2.5)
    print("Hill Climbing:")
    print("The coordinate of min is:")
    print("X = ",xpath[-1])
    print("Y = ",ypath[-1])
    print("Z = ",zpath[-1])
    print()
    graph(xpath,ypath,zpath)
    xpath,ypath,zpath=hill_climb_random_restart(function_to_optimize,0.01,3,-2.5,2.5,-2.5,2.5)
    graph(xpath,ypath,zpath)
    xpath,ypath,zpath=simulated_annealing(function_to_optimize,0.01,100,-2.5,2.5,-2.5,2.5)
    graph(xpath,ypath,zpath)

main()
