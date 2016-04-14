#!/usr/bin/python
# -*- coding: UTF-8 -*-
from random import random, choice

import matplotlib as mpl
mpl.use('agg')   # generate postscript output by default

from pylab import *
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.transforms import Affine2D
import mpl_toolkits.axisartist.floating_axes as floating_axes

mpl.rcParams['font.size'] = 10
fig = plt.figure()

#plot_extents = 0, 10, 0, 10
#transform = Affine2D().rotate_deg(45)
#helper = floating_axes.GridHelperCurveLinear(transform, plot_extents)
#axis = floating_axes.FloatingSubplot(fig, 111, grid_helper=helper)

ax = fig.add_subplot(111, projection='3d')

# compute two-dimensional histogram
hist, xedges, yedges = np.histogram2d(x, y, bins=10)

for z in [2011, 2012, 2013, 2014]:
     xs = xrange(1,13)
     ys = 10 * np.random.rand(12)

     color =plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
     ax.bar(xs, ys, zs=z, zdir='y', color=color, alpha=0.8)

ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(xs))
ax.yaxis.set_major_locator(mpl.ticker.FixedLocator(ys))

ax.set_xlabel('Dimension')
ax.set_ylabel('Layer')
ax.set_zlabel('Metric')

plt.savefig(sys.stdout)
plt.show()

