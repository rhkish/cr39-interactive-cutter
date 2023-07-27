
from pathlib import Path
import h5py
from cr39py.scan import Scan
from cr39py.cut import Cut
import numpy as np
import matplotlib.pyplot as plt
import sys 
from imagepointsdraw import ImagePointsDraw
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import numpy.ma as ma




#Load Data from cpsa for plotting
cpsa_path = Path("C:\\", "Users", "Reece", "Desktop", "PRAD UROP stuff", "test.cpsa")

scan = Scan.from_cpsa(cpsa_path)
#scan.to_hdf5(Path(os.path.dirname(os.path.realpath(__file__)), "temp.hdf5")) #might not work
dc_array = scan.trackdata[:,2:4]
print(dc_array[:,0])


#Plot and select in CD space
print("Select the desired region")
draw_obj = ImagePointsDraw()
imargs = {
    'extent' : [0, 30,
                0, 100],
    'origin' : 'lower',
}
dedges = np.arange(0, 30, 0.5)
cedges = np.arange(-0.5, 100.5, 1)

draw_obj.drawContours(dc_array.T, dedges, cedges, **imargs)
plt.xlabel("diameter")
plt.ylabel("contrast")
plt.show()

poly = draw_obj.getSelectedPolygon()

bool_mask = np.zeros(dc_array.shape, dtype=np.bool_)
plt.cla()

for i in range(len(dc_array)):
    bool_mask[i][0] = poly.contains(Point(dc_array[i][0], dc_array[i][1]))
    bool_mask[i][1] = bool_mask[i][0]


#Select corresponding points and show plot of xy space
xy_array = scan.trackdata[:, 0:2]
masked_xy_array = ma.MaskedArray(xy_array, mask = ~bool_mask)
kept_xy_array = masked_xy_array[~masked_xy_array.mask] #1D list of all non-masked values
kept_xy_array = np.reshape(kept_xy_array, (-1, 2))

counts, xedges, yedges, im = plt.hist2d(kept_xy_array[:,0],kept_xy_array[:,1], bins = (100,100), range = [[-5, 5],[-5,5]]) 
plt.title("xy histogram")
plt.xlabel("x (um)")
plt.ylabel("y (um)")
plt.colorbar()
plt.show()

np.savetxt("xy_hist.csv", counts, delimiter = ",")


