import numpy as np
import h5py
import binascii
import sys
import logging
from matplotlib import pyplot
from matplotlib import pyplot as plt
from matplotlib import image
from itertools import count
from shapely import geometry
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point, LineString, MultiLineString, box, MultiPolygon
import numpy
import numpy as geek
import math
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework import generics
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework import status
import ast
logger = logging.getLogger(__name__)#
class S100V_V(viewsets.ViewSet): 
    print("=========+++")
    http_method_names = ['get', 'post', 'put']
    print("__________")
    def get_queryset(self):
        print("=+++++++")
        return HttpResponse("get")
    def create(self, request):
        print("in method")
        return Response("Created h5 file successfully")
    def list(self, request):
        # second()
        logger.info("*******************************")
        return Response("Listed h5 file")
    def retrieve(self, request):
        return Response("Retrieve h5 file successfully")
def home(request):
    print("HHHHHHH")
    print(request)
    print("DDDDDDDDDDDD")
    return render(request, 'index.html')
    print("rrrrrrrrrrr")


def second():
    if __name__ == "__main__":
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")
    # print("SSSSSSSS")
    # print(sys.argv[1])
    # # sys.argv[2]
    # if (sys.argv[1] == 'runserver'):
    #     print("run")
    logger.info("++++++++++++++++++++++")
    if len(sys.argv) < 2:
        raise Exception("Please pass the input file")


    fileName = sys.argv[1]
    # print("1111111111")
    # # print(fileName)
    # print(len(sys.argv))
    # if len(sys.argv) ==2 and fileName == 'manage' and fileName.endswith(None):
    #     print(fileName)
    #     print(length)

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

    plt.interactive(False)

    indexValues = list(hf[firstKey][secondKey][thirdKey]['values'])
    print("IIIIII")
    for iter_chunks in hf[firstKey][secondKey][thirdKey]['values'].iter_chunks():
        print(iter_chunks)
    # a = np.array(indexValues, dtype=object)
        if(count == 3):
            break
        a = np.array(hf[firstKey][secondKey][thirdKey]['values'][iter_chunks][:500], dtype=object)

        seq2 = count(2) # we don't know in advance how many different objects we'll see
        d = {0:0, 1:1}  # but we know that the integers are either 0 or 1

        for o in a.flatten():
            # print(o)
            if o not in d: d[o] = next(seq2)

        # with the help of the dictionary, here it is a plottable matrix
        b = np.array([d[x] for x in a.flatten()]).reshape(a.shape)
        c = a.tolist()
        internalcount = 1
        cellobj = []
        fig = plt.figure()
        ax = fig.add_subplot(111)
        from matplotlib.collections import PatchCollection
        from descartes import PolygonPatch
        for singleobj in c:
            if(internalcount == 2):
                break
        print("-------")
        # polygonobj = geometry.asPolygon(singleobj)

        # cellobj.append(PolygonPatch(polygonobj, fc='blue'))
        # pointObj = geometry.asPoint(singleobj)
        # lineobj = geometry.asLineString(singleobj)
        # print("=========")
        # polyobj = geometry.asPolygon([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])
        # print("ppppppppppp")
        # pyplot.plot(polyobj)
        # print("00000000000")
        # ax.add_collection(PatchCollection(cellobj, match_original=True))
        # internalcount = internalcount+1
        # print("lllllll")
        # pyplot.show()
        # print("yyyyyyyyyy")

        import shapely.geometry as sg
        import shapely.ops as so
        import matplotlib.pyplot as plt
        print("=======")
        print(singleobj)
        r1 = sg.Polygon([(-25.07,0.07),(0,1),(1,1),(1,0),(0,0)])
        print("**********")
        r2 = sg.box(0.5,0.5,1.5,1.5)
        r3 = sg.box(4,4,5,5)
        print("rrrrrrrrrrr")
        new_shape = so.cascaded_union([r1, r2, r3])
        print("111")
        fig, axs = plt.subplots()
        axs.set_aspect('equal', 'datalim')

        for geom in new_shape.geoms:    
            xs, ys = geom.exterior.xy    
            axs.fill(xs, ys, alpha=0.5, fc='r', ec='none')

        plt.show()

