#!/usr/bin/python3

from matplotlib import pyplot as plt
import numpy as np
import matplotlib
import numpy.ma as ma
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def addPoint(scat, new_point, c='C0'):
    old_off = scat.get_offsets()
    new_off = np.concatenate([old_off,np.array(new_point, ndmin=2)])
    old_c = scat.get_facecolors()
    new_c = np.concatenate([old_c, np.array(matplotlib.colors.to_rgba(c), ndmin=2)])

    scat.set_offsets(new_off)
    scat.set_facecolors(new_c)

    scat.axes.figure.canvas.draw_idle()

def removePoint(scat):
    off = scat.get_offsets()[:-1]
    c = scat.get_facecolors()[:-1]

    scat.set_offsets(off)
    scat.set_facecolors(c)

    scat.axes.figure.canvas.draw_idle()
    


class ImagePointsDraw:

    def __init__(self,):
        self.x_points= []
        self.y_points= []

    def onClickPoint(self, event,):

        if event.button == 1:
            self.x_points.append(event.xdata)
            self.y_points.append(event.ydata)
            addPoint(self.scat, (event.xdata, event.ydata))
            self.line.set_data(self.x_points, self.y_points)
            self.line.figure.canvas.draw()

        elif event.button == 3:
            
            self.deleteLastSelection()
            

    def drawImage(self, data, **imargs):
        fig, ax = plt.subplots()
        fig.canvas.mpl_connect('button_press_event', self.onClickPoint)
        im = ax.imshow(data, alpha = .8, **imargs)
        ax.set_title("Press left mouse to select points\n Press right mouse to remove last selected point")
        fig.colorbar(im, ax=ax)
        self.scat = ax.scatter(self.x_points, self.y_points)
        self.line, = ax.plot([0], [0])        

    def drawContours(self, data0, data1, edges0, edges1, **imargs):
        fig, ax = plt.subplots()
        fig.canvas.mpl_connect('button_press_event', self.onClickPoint)
        #im = ax.imshow(data, alpha = .8, **imargs)
        hist, dedges, cedges = np.histogram2d(data0, data1, bins = (edges0, edges1))
        
        mesh0 = edges0[0:-1] + 0.25 
        mesh1 = edges1[0:-1] + 0.5
        contours = ax.contour(mesh0, mesh1, hist.T, levels = 20, colors = 'black', **imargs)
        ax.set_title("Press left mouse to select area\n Press right mouse to remove last selected point\n Select points CCW")
        self.scat = ax.scatter(self.x_points, self.y_points)
        self.line, = ax.plot([0], [0])

            

    def deleteLastSelection(self,):

        removePoint(self.scat)
        try:
            self.x_points.pop()
            self.y_points.pop()
            self.line.set_data(self.x_points, self.y_points)
            self.line.figure.canvas.draw()
        except:
            print("Cannot remove points when there are none!")
            

    def getSelectedPolygon(self,):
        vertices = [Point(point) for point in zip(self.x_points, self.y_points)]
        return Polygon(vertices)

        

        


