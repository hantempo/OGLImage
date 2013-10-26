import logging
logger = logging.getLogger(__name__)

import networkx as nx
import os, sys, subprocess

from OGLCommon import OGLEnum, GetImageSize
from UtilCommon import Which
from OGLImage import Image2D
from OGLImageIO import SaveImage, LoadImage

ETCPACK_NAME = 'etcpack'
ETCPACK_PATH = Which(ETCPACK_NAME)

def _RegisterConverter(converter_graph, converter_class):
    converter_graph.add_nodes_from([
        converter_class.source_format,
        converter_class.dest_format,
        ])
    converter_graph.add_edges_from([
        (converter_class.source_format,
         converter_class.dest_format,
         {'converter' : converter_class}),
        ])

class ImageConverter(object):

    @staticmethod
    def Convert(input_image):
        logger.error('The base ImageConverter should not be called')
        return input_image

class RGB8ToETC1(object):

    source_format = OGLEnum.GL_RGB8
    dest_format = OGLEnum.GL_ETC1_RGB8_OES

    @staticmethod
    def Convert(input_image):
        if not ETCPACK_PATH:
            logger.error('Cannot find the "etcpack" convertion tool in the environment $PATH')
            return input_image

        # for empty image
        width = input_image.width
        height = input_image.height
        dataSize = GetImageSize(width, height, OGLEnum.GL_ETC1_RGB8_OES)
        if input_image.IsEmpty():
            return Image2D(width=width, height=height,
                internalformat=OGLEnum.GL_ETC1_RGB8_OES,
                dataSize=dataSize)

        logger.debug('Conversion from RGB8 to ETC1')
        logger.debug('Input image : {0}'.format(str(input_image)))

        # save the input image as PPM format
        ppm_filepath = 'temp.ppm'
        ktx_filepath = 'temp.ktx'
        SaveImage(ppm_filepath, input_image)

        # call etcpack to convert as KTX format
        command = ' '.join((ETCPACK_PATH, ppm_filepath, os.curdir, '-ktx', '-c etc1'))
        logger.debug('Command : "{0}"'.format(command))
        subprocess.call(command, shell=True)

        # load the KTX format
        output_image = LoadImage(ktx_filepath)

        logger.debug('Output image : {0}'.format(str(output_image)))
        return output_image

_converters = nx.DiGraph()
_RegisterConverter(_converters, RGB8ToETC1)

def Convert(input_image, dest_format):
    try:
        path = nx.shortest_path(_converters, input_image.internalformat, dest_format)
        for src_node, dest_node in zip(path[:-1], path[1:]):
            con = _converters[src_node][dest_node]['converter']
            input_image = con.Convert(input_image)
    except nx.NetworkXError:
        logger.error('Cannot find conversions from {0} to {1}'.format(OGLEnum.names[input_image.internalformat], OGLEnum.names[dest_format]))
        return Image2D()
