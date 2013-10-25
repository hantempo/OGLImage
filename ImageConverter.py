import logging
logger = logging.getLogger(__name__)

import networkx as nx
from OGLCommon import OGLEnum
from Image import Image2D

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
        logger.debug('Conversion from RGB8 to ETC1')
        logger.debug('Input image : {0}'.format(str(input_image)))

        logger.debug('output image : {0}'.format(str(input_image)))
        return input_image

converters = nx.DiGraph()
converters.add_nodes_from([
    OGLEnum.GL_RGB8,
    OGLEnum.GL_ETC1_RGB8_OES,
    ])
converters.add_edges_from([
    (OGLEnum.GL_RGB8,
     OGLEnum.GL_ETC1_RGB8_OES,
     {'converter' : RGB8ToETC1}),
    ])

def Convert(input_image, dest_format):
    global converters
    try:
        path = nx.shortest_path(converters, input_image.internalformat, dest_format)
        for src_node, dest_node in zip(path[:-1], path[1:]):
            con = converters[src_node][dest_node]['converter']
            input_image = con.Convert(input_image)
    except nx.NetworkXError:
        logger.error('Cannot find conversions from {0} to {1}'.format(OGLEnum.names[input_image.internalformat], OGLEnum.names[dest_format]))
        return Image2D()
