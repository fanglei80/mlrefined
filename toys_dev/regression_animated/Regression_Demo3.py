# This file pairs with chapter 3 of the textbook "Machine Learning Refined" published by Cambridge University Press, 
# free for download at www.mlrefined.com

import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from IPython import display

class Regression_Demo3:
    def __init__(self,csvname):
        self.x = 0
        self.y = 0
        
        self.ln = []
        self.pt = []
        self.interactive_pt = []
        self.k = 0

        fig = plt.figure(num=None, figsize=(10, 5), dpi=80, facecolor='w', edgecolor='k')
        self.ax1 = fig.add_subplot(131)
        self.ax2 = fig.add_subplot(132,projection='3d')
        self.ax3 = fig.add_subplot(133)

        self.load_data(csvname)
        self.plot_pts()
        self.make_cost_surface()
          
        self.ax_to_plot = self.ax3
        self.cid = fig.canvas.mpl_connect('button_press_event', self)
        
    # load in a two-dimensional dataset from csv - input should be in first column, oiutput in second column, no headers 
    def load_data(self,csvname):
        # load data
        data = np.asarray(pd.read_csv(csvname,header = None))
        self.x = data[:,0]
        self.y = data[:,1]
        
        # center data
        self.x = self.x - np.mean(self.x)
        self.y = self.y - np.mean(self.y)
       
    ##### plotting functions ####
    # plot data
    def plot_pts(self):
        self.ax1.scatter(self.x,self.y)
        xgap = float(max(self.x) - min(self.x))/float(10)
        self.ax1.set_xlim([min(self.x)-xgap,max(self.x)+xgap])
        ygap = float(max(self.y) - min(self.y))/float(10)
        self.ax1.set_ylim([min(self.y)-ygap,max(self.y)+ygap])
        self.ax1.set_xticks([])
        self.ax1.set_yticks([])
        
    # create cost surface
    def make_cost_surface(self):
        # make grid over which surface will be plotted
        r = np.linspace(-2,2,100) 
        s,t = np.meshgrid(r,r)
        s = np.reshape(s,(np.size(s),1))
        t = np.reshape(t,(np.size(t),1))

        # generate surface based on given data - done very lazily - recomputed each time
        g = 0
        P = len(self.y)
        for p in range(0,P):
            g+= (s + t*self.x[p] - self.y[p])**2

        # reshape and plot the surface, as well as where the zero-plane is
        s.shape = (np.size(r),np.size(r))
        t.shape = (np.size(r),np.size(r))
        g.shape = (np.size(r),np.size(r))
        self.ax2.plot_surface(s,t,g,alpha = 0.15)
        self.ax2.plot_surface(s,t,g*0,alpha = 0.1)

        # make plot look nice
        self.ax2.view_init(10,20)        
        self.ax2.set_xticks([])
        self.ax2.set_yticks([])
        self.ax2.set_zticks([])
        self.ax2.set_xlabel('intercept ',fontsize = 14,labelpad = -5)
        self.ax2.set_ylabel('slope  ',fontsize = 14,labelpad = -5)
        self.ax2.zaxis.set_rotate_label(False)  # disable automatic rotation
        self.ax2.set_zlabel('cost  ',fontsize = 14, rotation = 0,labelpad = 1)
        
        levels = np.linspace(0,len(self.x),20)
        self.ax3.contour(s,t,g,levels,linewidths = 2)
        self.ax3.set_xticks([])
        self.ax3.set_yticks([])
        self.ax3.set_xlim([-2,2])
        self.ax3.set_ylim([-2,2])

        self.ax3.set_xlabel('intercept ',fontsize = 14,labelpad = 5)
        self.ax3.set_ylabel('slope  ',fontsize = 14,labelpad = 5)
        
   
    #### computation functions ####    
    def compute_cost(self,b,w):
        cost = 0
        for p in range(0,len(self.y)):
            cost +=(b + w*self.x[p] - self.y[p])**2
        return cost

    def __call__(self, event):
        if not event.inaxes:
            return
        # remove current fit line from plot
        if self.k > 0:
            for part in self.ln:
                part.remove()
            self.pt.remove()
            self.interactive_pt.remove()
        self.k += 1
        
        # plot click
        b = event.ydata
        w = event.xdata
        
        self.interactive_pt = self.ax_to_plot.scatter(w,b)
                
        # plot first parameters on cost surface
        cost = self.compute_cost(w,b)
        self.pt = self.ax2.scatter(w,b,cost,color = 'r',marker = 'x',linewidth = 3, alpha = 0.8)
                    
        # plot the line generated by most recent params
        s = np.linspace(np.min(self.x)-1, np.max(self.x)+10, 100)
        t = w + s*b
        self.ln = self.ax1.plot(s,t,'-r',linewidth = 3) 
                       
        # clear panels
        display.clear_output(wait=True)
        display.display(plt.gcf()) 
        