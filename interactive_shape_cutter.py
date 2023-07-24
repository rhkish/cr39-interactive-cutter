
from pathlib import Path
import h5py
from cr39py.scan import Scan
from cr39py.cut import Cut
import numpy as np
import matplotlib.pyplot as plt
import pickle
import glob
import sys
sys.path.insert(1, "../Select-Arbitrary-Shapes-in-Images-main")
#import reconstruction 
from imagepointsdraw import ImagePointsDraw
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import numpy.ma as ma
import matplotlib
import os




#Load Data from cpsa for plotting
cpsa_path = Path("C:\\", "Users", "Reece", "Desktop", "PRAD UROP stuff", "test.cpsa")

scan = Scan.from_cpsa(cpsa_path)
#scan.to_hdf5(Path(os.path.dirname(os.path.realpath(__file__)), "temp.hdf5")) #might not work
dc_array = scan.trackdata[:,2:4]
print(dc_array)


#Plot and select in CD space
print("Select the desired region")
draw_obj = ImagePointsDraw()
imargs = {
    'extent' : [0, 100,
                0, 100],
    'origin' : 'lower',
    'vmin' : 0, 'vmax' : np.max(dc_array)
}
draw_obj.drawImage(dc_array.T, **imargs)
plt.xlabel("diameter")
plt.ylabel("contrast")
plt.show()

poly = draw_obj.getSelectedPolygon()

bool_mask = np.zeros(Bfield.T.shape, dtype=np.bool_)

for i in range(bool_mask.shape[0]):
    for j in range(bool_mask.shape[1]):
        bool_mask[i][j] = poly.contains(Point(x[i][j], y[i][j]))



#Select corresponding points and show plot of xy space

