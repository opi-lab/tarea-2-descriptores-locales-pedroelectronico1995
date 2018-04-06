# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 23:21:38 2018

@author: PEDRO NEL MENDOZA
"""

# Firstly, the necessary libraries and modules are imported 
from PIL import Image
from numpy import *
from pylab import *
from scipy.ndimage import filters
import matplotlib.pyplot as plt
import os

def compute_harris_response(im,sigma=3):
  """ Compute the Harris corner detector response function 
    for each pixel in a grayscale image. """
    
  # derivatives
  imx = zeros(im.shape)
  filters.gaussian_filter(im, (sigma,sigma), (0,1), imx)
  imy = zeros(im.shape)
  filters.gaussian_filter(im, (sigma,sigma), (1,0), imy)
    
  # compute components of the Harris Matrix
  Wxx = filters.gaussian_filter(imx*imx,sigma)
  Wxy = filters.gaussian_filter(imx*imy,sigma)
  Wyy = filters.gaussian_filter(imy*imy,sigma)
    
  # determinant and trace
  Wdet = Wxx*Wyy - Wxy**2
  Wtr = Wxx + Wyy
    
  return Wdet / Wtr

def get_harris_points(harrisim,min_dist=10,threshold=0.1):
  """ Return corners from a Harris response image 
    min_dist is the minimum number of pixels separating 
    corners and image boundary. """
    
  # find top corner candidates above a threshold
  corner_threshold = harrisim.max() * threshold
  harrisim_t = (harrisim > corner_threshold) * 1
    
  # get coordinates of candidates
  coords = array(harrisim_t.nonzero()).T
    
  # ...and their values
  candidate_values = [harrisim[c[0],c[1]] for c in coords]
    
  # sort candidates
  index = argsort(candidate_values)
    
  # store allowed point locations in array
  allowed_locations = zeros(harrisim.shape)
  allowed_locations[min_dist:-min_dist,min_dist:-min_dist] = 1
    
  # select the best points taking min_distance into account 
  filtered_coords = []
  for i in index:
    if allowed_locations[coords[i,0],coords[i,1]] == 1:
      filtered_coords.append(coords[i])
      allowed_locations[(coords[i,0]-min_dist):(coords[i,0]+min_dist),
            (coords[i,1]-min_dist):(coords[i,1]+min_dist)] = 0
                            
  return filtered_coords

def plot_harris_points(im,filtered_coords):
  """ Plots corners found in image. """
  
  figure()
  gray()
  imshow(im)
  plot([p[1] for p in filtered_coords],[p[0] for p in filtered_coords],'*')
  axis('off')
  show()

# to read an image to array with the image converted to grayscale with convert('L')
im = array(Image.open(os.path.abspath('data/castillo_hohenzollern.jpg')).convert('L'))

# Changing sigma for take different scales both for the x, y directions and the averaging
# Leaving the other values (min_dist=10,threshold=0.1) unchanged

print("CORNER POINTS DETECTED CHANGING SIGMA")

i = 1;
plt.figure(figsize=(16,6))
for sigma in xrange(1,32,2):
    harrisim = compute_harris_response(im,sigma)             # Compute the Harris corner detector response function for each pixel in a graylevel image.
    filtered_coords = get_harris_points(harrisim)            # Return corners from a Harris response image.
    plt.subplot(16,6,i)                          
    plt.title('Corner points detected with sigma=%i' %sigma) # Add a title to each plot  
    plt.axis('off')                                          # Remove the axis
    plot_harris_points(im, filtered_coords)                  # Plots corners found in image.
    i = i + 1;
plt.show()

# Changing min_dist 
# Leaving the other values (sigma=3,threshold=0.1) unchanged

print ("CORNER POINTS DETECTED CHANGING MIN_DIST")
i = 1;
plt.figure(figsize=(16,6))
for min_dist in xrange(4,83,6):
    harrisim = compute_harris_response(im)                             # The same as on line 28.
    filtered_coords_mindist = get_harris_points(harrisim,min_dist)     # The same as on line 29.
    plt.subplot(16,6,i)
    plt.title('Corner points detected with min_dist=%i' %min_dist)     # Add a title to each plot  
    plt.axis('off')                                                    # Remove the axis
    plot_harris_points(im, filtered_coords_mindist)                    # Plots corners found in image.
    i = i + 1;
plt.show()

# Changing threshold
#Leaving the other values (sigma=3,min_dist=10) unchanged

print("CORNER POINTS DETECTED CHANGING THRESHOLD")

i = 1;
plt.figure(figsize=(16,6))
threshold = 0.01
while threshold<0.4:
    harrisim = compute_harris_response(im)                               # The same as on line 28.
    filtered_coords_threshold = get_harris_points(harrisim,10,threshold) # The same as on line 29.
    plt.subplot(16,6,i)
    plt.title('Corner points detected with threshold=%f' %threshold)     # Add a title to each plot  
    plt.axis('off')                                                      # Remove the axis
    plot_harris_points(im, filtered_coords_threshold)                    # Plots corners found in image.
    i = i + 1;
    threshold = threshold+0.04
plt.show()    

'''
PART ONE:
-Changing only sigma for take different scales both for the x, y directions and the averaging.
-Leaving the other values (min_dist=10,threshold=0.1) unchanged.

In this part, it can be shown that as the sigma value increases (parameter that defines the
scale of the Gaussian filters used in the corners detection process), it is more difficult
to detect interesting points, in other words, corners of the image through the Harris Corner 
Detector; this is because the standard deviation increases the blurring of the image, so 
it can see that every time sigma increases, the points detected as corners overlap each
other.

PART TWO:
-Changing min_dist 
-Leaving the other values (sigma=3,threshold=0.1) unchanged

In this part, as the min_dist value increases (which corresponds to the minimum number of pixels
separating corners and image boundary), the number of interest points or corners detections
in the image decreases; this allows a better visualization of detected points. This is also 
achieved thanks to the Harris Corner Detector eliminates points whose cornerness measure is not
larger than the cornerness values of all points within a certain distance (min_dist).

PART THREE:
-Changing threshold
-Leaving the other values (sigma=3,min_dist=10) unchanged

In this part, with the increment of the threshold value (which refers to a threshold for the 
selection of corner points), it can be seen that the number of interest points or corners
detections in the image decreases; this can be explained by the fact that the threshold makes 
a cornerness map to eliminate weak corners. This is an approach that often gives good results,
together with the constraint imposed by the min_dist value.
'''