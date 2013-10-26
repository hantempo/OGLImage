import logging
logger = logging.getLogger(__name__)

import networkx as nx
from OGLCommon import OGLEnum
from UtilCommon import Which

class Image2D(object):

    def __init__(self, width=0, height=0,
        internalformat=OGLEnum.GL_NONE,
        dataSize=0, data=None):
        self.width = width
        self.height = height
        self.internalformat = internalformat
        self.dataSize = dataSize
        self.data = data

    def __repr__(self):
        return 'Image2D : dimension({0}x{1}), internalformat({2}), dataSize({3})'.format(self.width, self.height, OGLEnum.names[self.internalformat], self.dataSize)

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
        logger.debug('Conversion from RGB8 to ETC1')
        logger.debug('Input image : {0}'.format(str(input_image)))



        logger.debug('Output image : {0}'.format(str(input_image)))
        return input_image

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
