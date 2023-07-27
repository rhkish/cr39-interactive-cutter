
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
darray = scan.trackdata[:,2]
carray = scan.trackdata[:,3]
xarray = scan.trackdata[:, 0]
yarray = scan.trackdata[:, 1]

#alter as needed
dmax = 30
dmin = 0
cmax = 5
cmin = 0

good_indices = np.logical_and(np.logical_and(darray > dmin, darray < dmax), np.logical_and(carray > cmin, carray < cmax))
darray = darray[good_indices]
carray = carray[good_indices]
xarray = xarray[good_indices]
yarray = yarray[good_indices]

#Plot and select in CD space
print("Select the desired region")
draw_obj = ImagePointsDraw()
imargs = {
    'extent' : [0, 30,
                0, 100],
    'origin' : 'lower',
}
dedges = np.arange(0, 30, 0.5)
cedges = np.arange(-0.5, 30.5, 1)

draw_obj.drawContours(darray, carray, dedges, cedges, **imargs)
plt.xlabel("diameter")
plt.ylabel("contrast")
plt.show()

poly = draw_obj.getSelectedPolygon()

bool_mask = np.zeros(darray.shape, dtype=np.bool_)
plt.cla()

for i in range(len(darray)):
    bool_mask[i] = poly.contains(Point(darray[i], carray[i]))


#Select corresponding points and show plot of xy space
yarray = yarray[bool_mask]
xarray = xarray[bool_mask]

counts, xedges, yedges, im = plt.hist2d(xarray, yarray, bins = (100,100), range = [[-5, 5],[-5,5]]) 
plt.title("xy histogram")
plt.xlabel("x (um)")
plt.ylabel("y (um)")
plt.colorbar()
plt.show()

np.savetxt("xy_hist.csv", counts, delimiter = ",")


