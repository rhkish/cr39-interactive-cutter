
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
from cr39py.response import track_energy



#Load Data from cpsa for plotting
cpsa_path = Path("C:\\", "Users", "Reece", "Desktop", "PRAD UROP stuff", "A2023081602_A6_track_5h_40x_s6.cpsa")
XY_mode = True #If user wants to select in XY space as well and get an energy spectrum histogram out


scan = Scan.from_cpsa(cpsa_path)
#scan.to_hdf5(Path(os.path.dirname(os.path.realpath(__file__)), "temp.hdf5")) #might not work
darray = scan.trackdata[:,2]
carray = scan.trackdata[:,3]
xarray = scan.trackdata[:, 0]
yarray = scan.trackdata[:, 1]

#alter as needed
dmax = 30
dmin = 0
cmax = 40
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
    'extent' : [0, 40,
                0, 100],
    'origin' : 'lower',
}
dedges = np.arange(0, 30, 0.5)
cedges = np.arange(-0.5, 40.5, 1)

draw_obj.drawContours(darray, carray, dedges, cedges, **imargs)
plt.xlabel("diameter")
plt.ylabel("contrast")
plt.show()

poly = draw_obj.getSelectedPolygon()

bool_mask = np.zeros(darray.shape, dtype=np.bool_)
plt.clf()

for i in range(len(darray)): #Actual selection of points
    bool_mask[i] = poly.contains(Point(darray[i], carray[i]))


xarray = xarray[bool_mask]
yarray = yarray[bool_mask]

print("select data region")
#plot in xy space
if XY_mode:
    draw_obj = ImagePointsDraw()
    draw_obj.drawHist(xarray, yarray)
    
else:
    counts, xedges, yedges, im = plt.hist2d(xarray, yarray, bins = (100,100), range = [[-5, 5],[-5,5]]) 
    plt.colorbar()

plt.title("xy histogram")
plt.xlabel("x (um)")
plt.ylabel("y (um)")
plt.show()
if not XY_mode:
    np.savetxt("xy_hist.csv", counts, delimiter = ",") #program ends here

else:
    #get number of points + area inside selected region
    poly = draw_obj.getSelectedPolygon()
    plt.clf()
    count = 0
    for i in range(len(xarray)):
        if poly.contains(Point(xarray[i], yarray[i])):
            count += 1

    area = poly.area

    print("data_counts = " + str(count),"data_area = " + str(area))


#background
print("now select background")
for i in range(len(darray)): #Actual selection of points
    bool_mask[i] = poly.contains(Point(darray[i], carray[i]))



#plot in xy space
if XY_mode:
    draw_obj = ImagePointsDraw()
    draw_obj.drawHist(xarray, yarray)
    
else:
    counts, xedges, yedges, im = plt.hist2d(xarray, yarray, bins = (100,100), range = [[-5, 5],[-5,5]]) 
    plt.colorbar()

plt.title("xy histogram")
plt.xlabel("x (um)")
plt.ylabel("y (um)")
plt.show()
if not XY_mode:
    np.savetxt("xy_hist.csv", counts, delimiter = ",") #program ends here

else:
    #get number of points + area inside selected region
    poly = draw_obj.getSelectedPolygon()
    plt.clf()
    bcount = 0
    for i in range(len(xarray)):
        if poly.contains(Point(xarray[i], yarray[i])):
            bcount += 1

    barea = poly.area

    print("background_counts = " + str(bcount),"background_area = " + str(barea))
    
    final_count = count - area/barea*bcount
    final_fluence = final_count/area
    final_error = np.sqrt(final_count)/area
    print("final_fluence = " + str(final_fluence))
    print("final_error = " + str(final_error))




