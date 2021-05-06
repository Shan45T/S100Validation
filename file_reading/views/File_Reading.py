import numpy as np
import h5py
import binascii
import sys
import logging
from matplotlib import pyplot as plt
from shapely import geometry
from shapely.geometry.polygon import LinearRing, Polygon,LineString
from shapely.geometry import GeometryCollection
import pprint
import itertools
from descartes import PolygonPatch    
from matplotlib.collections import PatchCollection
import shapely.ops as so
from datetime import datetime

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(filename="output.txt", format=format, level=logging.INFO,
                        datefmt="%Y%m%d_%H:%M:%S")

if len(sys.argv) < 2:
    raise Exception("Please pass the input file")

fileName = sys.argv[1]
if(fileName.endswith('.h5') or fileName.endswith('.H5')):
    length = len(fileName)
    lastIndex=0
    if(fileName.__contains__('_')):
        lastIndex = fileName.rindex('_')        
        if(length >= lastIndex+4):
            subFileName = fileName[:lastIndex]
            logging.info(" subFileName : "+subFileName)
            hf = h5py.File(subFileName+'_%d.h5','r', driver='family', memb_size=0)
    else:
        logging.info('file reading other case')            
        hf = h5py.File(fileName,'r')
else:
    raise Exception("Please pass the H5 input file")   

firstKey = list(hf.keys())[0]
secondKey = list(hf[firstKey])[0]
thirdKey = list(hf[firstKey][secondKey])[0]
fourKey = list(hf[firstKey][secondKey][thirdKey])[0]
data_four = list(hf[firstKey][secondKey][thirdKey][fourKey])


count1 =1

#fileobj = open("output.txt","w")

for iter_chunks1 in hf[firstKey][secondKey][thirdKey]['values'].iter_chunks():    

    if(count1 == 2):
        break
    firstChunk = np.array(hf[firstKey][secondKey][thirdKey]['values'][iter_chunks1], dtype=object)      
    
    listobj = firstChunk.tolist()    
    internalcount = 1
    for singleobj in listobj:                
        if(internalcount ==3):
            break
        pointobj = geometry.asPoint(singleobj)
        polyObj = geometry.asPolygon(singleobj)

        try:
            logging.info("" + 'Polygon is empty  = '+str(polyObj.is_empty) +"\n")
            logging.info("" + 'Polygon is closed  = '+str(polyObj.is_closed) +"\n")           
            logging.info("" + 'Polygon is valid  = '+str(polyObj.is_valid) +"\n") # If it is false giving some warning message in log cosole
            logging.info("" + 'Polygon boundary  = '+str(polyObj.boundary) +"\n")
            logging.info("" + 'Polygon envelope  = '+str(polyObj.envelope) +"\n")
            
            logging.info(' Point related methods and its results \n ')

            logging.info("" + 'Point is empty  = '+str(pointobj.is_empty) +"\n")
            logging.info("" + 'Point is closed  = '+str(pointobj.is_closed) +"\n")
            logging.info("" + 'Point is valid  = '+str(pointobj.is_valid) +"\n")# If it is false giving some warning message in log cosole
            logging.info("" + 'Point boundary  = '+str(pointobj.boundary) +"\n")
            logging.info("" + 'Point envelope  = '+str(pointobj.envelope) +"\n")           

            plt.plot(polyObj.boundary.xy)
            #plt.plot(polyObj.exterior.xy)
            
            plt.show()
        except Exception as e:
            print(e)
        internalcount = internalcount + 1    
    count1 = count1 + 1
