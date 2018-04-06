# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 16:57:06 2018

Modify the function for matching Harris corner points to also take a maximum
pixel distance between points for them to be considered as correspondences, in
order to make matching more robust.

@author: PEDRO NEL MENDOZA
"""

# Firstly, the necessary libraries and modules are imported 
from PIL import Image
from numpy import *
from pylab import *
from scipy.ndimage import filters
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

def get_descriptors(im,filtered_coords,wid=5):
  """ For each point return, pixel values around the point 
    using a neighbourhood of width 2*wid+1. (Assume points are
    extracted with min_distance > wid). """
  desc = []
  for coords in filtered_coords:
    patch = im[coords[0]-wid:coords[0]+wid+1, coords[1]-wid:coords[1]+wid+1].flatten()
    desc.append(patch)
    
  return desc

def match(desc1,desc2,locs1,locs2,threshold=0.5):                   # Aggregate locs1, locs2 as parameters of function match.
  """ For each corner point descriptor in the first image,
    select its match to second image using 
    normalized cross-correlation. """
    
  n = len(desc1[0])
  
  # pair-wise distances
  d = -ones((len(desc1),len(desc2)))
  for i in range(len(desc1)):
    for j in range(len(desc2)):
          maximum_pixel_dist = sqrt((sum((locs1[i]-locs2[j])**2)))  # Calculate maximum pixel distance between points
          if maximum_pixel_dist <= 100:                             # Compare maximum pixel distance between points with a value of 100, in order to make matching more robust.
             d1 = (desc1[i] - mean(desc1[i])) / std(desc1[i])
             d2 = (desc2[j] - mean(desc2[j])) / std(desc2[j])
             ncc_value = sum(d1 * d2) / (n-1)
             if ncc_value > threshold:
                   d[i,j] = ncc_value
          
  ndx = argsort(-d)
  matchscores = ndx[:,0]
  
  return matchscores

def match_twosided(desc1,desc2,locs1,locs2,threshold=0.5):          # Aggregate locs1, locs2 as parameters of function match_twosided
  """ Two-sided symmetric version of match(). """
  
  matches_12 = match(desc1,desc2,locs1,locs2,threshold)             # Aggregate locs1, locs2 to make matches of image 1 to image 2 taking a maximum pixel distance between points for them to be considered as correspondences
  matches_21 = match(desc2,desc1,locs2,locs1,threshold)             # Aggregate locs1, locs2 to make matches of image 2 to image 1 taking a maximum pixel distance between points for them to be considered as correspondences
  
  ndx_12 = where(matches_12 >= 0)[0]
  
  # remove matches that are not symmetric
  for n in ndx_12:
    if matches_21[matches_12[n]] != n:
      matches_12[n] = -1

  return matches_12

def appendimages(im1,im2):
  """ Return a new image that appends the two images side-by-side. """

  # select the image with the fewest rows and fill in enough empty rows
  rows1 = im1.shape[0]
  rows2 = im2.shape[0]
  
  if rows1 < rows2:
    im1 = concatenate((im1,zeros((rows2-rows1,im1.shape[1]))),axis=0)
  elif rows1 > rows2:
    im2 = concatenate((im2,zeros((rows1-rows2,im2.shape[1]))),axis=0)
  # if none of these cases they are equal, no filling needed           

  return concatenate((im1,im2), axis=1)

def plot_matches(im1,im2,locs1,locs2,matchscores,show_below=True):
  """ Show a figure with lines joining the accepted matches 
    input: im1,im2 (images as arrays), locs1,locs2 (feature locations),
    matchscores (as output from 'match()'),
    show_below (if images should be shown below matches). """
    
  im3 = appendimages(im1,im2)
  if show_below:
    im3 = vstack((im3,im3))
    imshow(im3)

    cols1 = im1.shape[1]
    for i,m in enumerate(matchscores):
      if m>0:
        plot([locs1[i][1],locs2[m][1]+cols1],[locs1[i][0],locs2[m][0]],'c')
    axis('off')

# Read two images to arrays with the images converted to grayscale with convert('L')    
im1 = array(Image.open(os.path.abspath('data/sf_view1.jpg')).convert('L'))
im2 = array(Image.open(os.path.abspath('data/sf_view2.jpg')).convert('L'))

wid = 5
harrisim = compute_harris_response(im1,5)             # Compute the Harris corner detector response function for each pixel in a graylevel image.
filtered_coords1 = get_harris_points(harrisim,wid+1)  # Return corners from a Harris response image.
d1 = get_descriptors(im1,filtered_coords1,wid)        # Get descriptors for each point return. Pixel values around the point using a neighbourhood of width 2*wid+1.

harrisim = compute_harris_response(im2,5)             # Compute the Harris corner detector response function for each pixel in a graylevel image.
filtered_coords2 = get_harris_points(harrisim,wid+1)  # Return corners from a Harris response image.
d2 = get_descriptors(im2,filtered_coords2,wid)        # Get descriptors for each point return. Pixel values around the point using a neighbourhood of width 2*wid+1.

print 'starting matching'                             # Print the message 'starting matching'
matches = match_twosided(d1,d2,filtered_coords1,filtered_coords2) # Two-sided symmetric version of match(). match(), for each corner point descriptor in the first image, select its match to second image using normalized cross-correlation.
                                                                  # In the above line, to make matches, filtered_coords1 and filtered_coords2 are aggregated. 
figure()
gray()
plot_matches(im1,im2,filtered_coords1,filtered_coords2,matches)   # Show a figure with lines joining the accepted matches
show()
