import matplotlib
matplotlib.use('Agg')
import numpy as np
import h5py
import binascii
import sys
import logging
from matplotlib import pyplot
from matplotlib import image
from itertools import count
from rest_framework.response import Response
from django.http import HttpResponse
from file_reading.serializer.S100UPLOADFILE import *
from rest_framework import status
import config
from rest_framework import views, viewsets
import json


logger = logging.getLogger(__name__)

class S100MapView(viewsets.ModelViewSet):   

    def create(self, request):
        try:
            
            serializer_class = S100FileSerializer(data=request.data)
            if 'file' not in request.FILES or not serializer_class.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                file = request.FILES['file']
                logger.info("Selected file is " + str(file))           
                fileName = request.FILES['file'].name
                header = request.data.get(config.HEADER)
                metadata = request.data.get(config.METADATA)
                
                if(fileName.endswith('.h5') or fileName.endswith('.H5')):
                    length = len(fileName)
                    lastIndex=0
                    hf = h5py.File(file,'r')
                    logger.info(str(hf) + "File reads")                    
                    if(fileName.__contains__('_')):
                        try:
                            lastIndex = fileName.rindex('_')        
                            if(length >= lastIndex+4):
                                subFileName = fileName[:lastIndex]
                                logging.info(" subFileName : "+subFileName)
                                hf = h5py.File(subFileName+'_%d.h5','r', driver='family', memb_size=0)
                        except ValueError as errMessage:
                            logger.error(str(errMessage))
                            return Response({'Message': str(errMessage)},status=status.HTTP_404_NOT_FOUND)
                    else:
                        logging.info('file reading other case')  
                        hf = h5py.File(file,'r')
                    
                    firstKey = list(hf.keys())[0]
                    secondKey = list(hf[firstKey])[0]
                    thirdKey = list(hf[firstKey][secondKey])[0]
                    fourKey = list(hf[firstKey][secondKey][thirdKey])[0]
                    data_four = list(hf[firstKey][secondKey][thirdKey][fourKey])

                    pyplot.interactive(False)

                    indexValues = list(hf[firstKey][secondKey][thirdKey]['values'][:25])

                    a = np.array(indexValues, dtype=object)
                    seq2 = count(2) # we don't know in advance how many different objects we'll see
                    d = {0:0, 1:1}  # but we know that the integers are either 0 or 1
                    for o in a.flatten():  
                        if o not in d: d[o] = next(seq2)

                    # with the help of the dictionary, here it is a plottable matrix
                    b = np.array([d[x] for x in a.flatten()]).reshape(a.shape)
                    
                    imgplot = pyplot.imshow(b)
                    imgplot.set_cmap('nipy_spectral')
                    pyplot.colorbar(imgplot, orientation='vertical')
                    
                    pyplot.savefig('static/images/filenameXYZ.png') #save to the images directory
                    #return flask.jsonify({"result":"<div class='user_avatar' style='background-image:url('static/images/filenameXYZ.png');width:240px;height:240px;background-size:cover;border-radius:10px;'>"})
                    #return Response(json.dumps({"result":"<div class='user_avatar' style='background-image:url('static/images/filenameXYZ.png');width:240px;height:240px;background-size:cover;border-radius:10px;'>"}))
                    response_data = { 'url':'static/images/filenameXYZ.png'}
                    return HttpResponse(json.dumps(response_data),status=status.HTTP_200_OK)                    
        except ValueError as errMessage:            
            logger.error(str(errMessage))
            return Response({'Message': str(errMessage)},status=status.HTTP_404_NOT_FOUND)
