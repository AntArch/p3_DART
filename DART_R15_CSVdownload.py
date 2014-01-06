__author__ = 'arb'

"""
Created on Tue Sep 10 12:53:34 2013

@author: arb

Plotting the r15 geophysics by dynamically accessing a file held in the DART repository
"""
#######################################################import libraries
#import urllib2
import urllib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

rc('font', family='serif')
import scipy.ndimage as nd

#Import the data
#This should be a file URI from DARTPrortal
'''
Bibtex citation:
    @data{dart_r15_ddcf_20110928_20110928_rawpreserve_b.csv, doi = {not allocated}, url = {http://dartportal.leeds.ac.uk/storage/f/dart_r15_ddcf_20110928_20110928_rawpreserve_b.csv}, author = "{Robert Fry}", publisher = {DART repository, School of Computing, University of Leeds}, title = {dart_r15_ddcf_20110928_20110928_rawpreserve_b.csv}, year = {2013}, note = {DART is a Science and Heritage project funded by AHRC and EPSRC. Further DART data and details can be found at http://dartportal.leeds.ac.uk} }

Associated Metatadata: https://dartportal.leeds.ac.uk/dataset/dart_geophysics_geoscanrm15/resource/f6387bd6-bd0a-4d3d-ba49-feee4c05a77d
'''
inputURI = "http://dartportal.leeds.ac.uk/storage/f/dart_r15_ddcf_20110928_20110928_rawpreserve_a.csv"
#inputURI = "http://dartportal.leeds.ac.uk/storage/f/dart_r15_hhcc_20120321_20120321_rawpreserve_a.csv"

#Access the URI
#webdata = urllib.urlopen(inputURI) #python2

webdata = urllib.request.urlopen(inputURI)#python3

#read the data into a list
data = np.genfromtxt(webdata, skip_header=1, delimiter=",")

print('the data as a list')
print(data)

#restructure the array into a 20 x 20 matrix (appropriate for this data)
#although not sure if the orientation is right
griddata = data[:, 2].reshape(20, 20)


#print data
print('The data recast as in a 20x20 grid array')
print(griddata)

#restructure the array into a 20 x 20 matrix (appropriate for this data) automatically calculating the dimensions
print('Total number of elements in INPUT data: ', np.size(data[:, 2])) #search on third column
print('Number of dimensions for INPUT data: ', np.ndim(data[:, 2]))
print('SQRT of total number of elements in INPUT data: ', np.sqrt(np.size(data[:, 2])))

#although not sure if the orientation is right
griddata = data[:, 2].reshape(np.sqrt(np.size(data[:, 2])), np.sqrt(np.size(data[:, 2])))


#print data
print('Total number of elements in OUTPUT data: ', np.size(griddata))
print('Number of dimensions for OUTPUT data: ', np.ndim(griddata))
print('SQRT of total number of elements in OUTPUT data: ', np.sqrt(np.size(griddata)))
print('The data recast as in a ', np.sqrt(np.size(griddata)), ' x ', np.sqrt(np.size(griddata)), ' grid array')
print(griddata)

#Plot the data

dataDir = "/home/arb/Delme/"
plt.imshow(griddata, origin='lower')

plt.gray()
cb = plt.colorbar()
cb.set_label('Value Range')
plt.xlabel('GridEast')
plt.ylabel('GridNorth')
plt.suptitle('Raw data')
plt.savefig(dataDir + 'r15_raw' + '.png')
plt.show()

#Calculate derivatives
gridSobel = nd.sobel(griddata)
gridLaplace = nd.laplace(griddata)
gridPrewitt = nd.prewitt(griddata)
gridGaussian = nd.gaussian_filter(griddata, 1)
gridMinimum = nd.minimum_filter(griddata, size=(3, 3))

#Plot a derivative
plt.imshow(gridGaussian, origin='lower')
plt.gray()
#show image
cb = plt.colorbar()
cb.set_label('Value Range')
plt.xlabel('GridEast')
plt.ylabel('GridNorth')
plt.suptitle('Raw data')
plt.savefig(dataDir + 'r15_gaussianDerivative' + '.png')
plt.show()


#The data and derivatives
plt.subplot(1, 3, 2)
plt.imshow(griddata, origin='lower')
plt.gray()
cb = plt.colorbar()
cb.set_label('Value Range')
plt.xlabel('GridEast')
plt.ylabel('GridNorth')
plt.title('Raw data')

plt.subplot(3, 3, 1)
plt.imshow(gridSobel, origin='lower')
plt.gray()
plt.title('Sobel filter')

plt.subplot(3, 3, 3)
plt.imshow(gridLaplace, origin='lower')
plt.gray()
plt.title('Laplace filter')

plt.subplot(3, 3, 4)
plt.imshow(gridPrewitt, origin='lower')
plt.gray()
plt.title('Prewitt filter')

plt.subplot(3, 3, 6)
plt.imshow(gridGaussian, origin='lower')
plt.gray()
plt.title('Gaussian filter')

plt.subplot(3, 3, 7)
plt.imshow(gridMinimum, origin='lower')
plt.gray()
plt.title('3x3 minimum filter')

plt.subplot(3, 3, 9)
plt.imshow(griddata - gridGaussian, origin='lower')
plt.gray()
plt.title('Data - Gaussian Filter')

plt.suptitle('Raw data and derivatives')
plt.savefig(dataDir + 'r15_multipleDerivatives' + '.png')
plt.show()

print('Finished')