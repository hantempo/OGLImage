import logging
logger = logging.getLogger(__name__)

import networkx as nx
import numpy as np
import os, sys

from OGLCommon import OGLEnum, GetImageSize
from UtilCommon import Which, RunCommand, Delete
from OGLImage import Image2D
from OGLImageIO import SaveImage, LoadImage

ETCPACK_NAME = 'etcpack'

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

class _RGB8_RGBA8_Converter(object):
    source_format = OGLEnum.GL_RGB8
    dest_format = OGLEnum.GL_RGBA8

    @staticmethod
    def Convert(input_image):
        dst_format = _RGB8_RGBA8_Converter.dest_format
        src_format = _RGB8_RGBA8_Converter.source_format

        # for empty image
        width = input_image.width
        height = input_image.height
        dataSize = GetImageSize(width, height, dst_format)
        if input_image.IsEmpty():
            return Image2D(width=width, height=height,
                internalformat=dst_format,
                dataSize=dataSize)

        logger.debug('Convert from {0} to {1}'.format(
            OGLEnum.names[src_format],
            OGLEnum.names[dst_format]))
        logger.debug('Input image : {0}'.format(str(input_image)))

        rgb_array = np.fromstring(input_image.data, dtype='uint8')
        rgba_array = np.empty(dataSize, dtype='uint8')
        for k in range(dataSize):
            if k % 4 == 3:
                rgba_array[k] = 255
            else:
                i = k % 4 + k / 4 * 3
                rgba_array[k] = rgb_array[i]
        output_image = Image2D(width=width, height=height,
            internalformat=dst_format,
            dataSize=dataSize, data=rgba_array.tostring())

        logger.debug('Output image : {0}'.format(str(output_image)))
        return output_image

def _Image2DConverterFactory(class_name, src_format, dst_format,
    input_filename = None, output_filename = None, tool_cmd = None):

    class class_name(object):
        source_format = src_format
        dest_format = dst_format

        @staticmethod
        def Convert(input_image):
            # for empty image
            width = input_image.width
            height = input_image.height
            dataSize = GetImageSize(width, height, dst_format)
            if input_image.IsEmpty():
                return Image2D(width=width, height=height,
                    internalformat=dst_format,
                    dataSize=dataSize)

            tool_filename = tool_cmd.split()[0]
            if not Which(tool_filename):
                logger.error('Cannot find the specified tool ({0}) in the environment $PATH, return an empty image with dest format'.format(tool_filename))
                return Image2D(width=width, height=height,
                    internalformat=dst_format,
                    dataSize=dataSize)

            logger.debug('Convert from {0} to {1}'.format(
                OGLEnum.names[src_format],
                OGLEnum.names[dst_format]))
            logger.debug('Input image : {0}'.format(str(input_image)))

            SaveImage(input_filename, input_image)
            RunCommand(tool_cmd)
            output_image = LoadImage(output_filename)
            Delete(input_filename)
            Delete(output_filename)

            logger.debug('Output image : {0}'.format(str(output_image)))
            return output_image

    return class_name

# construct and register converter classes
_converters = nx.DiGraph()

RGB8ToETC1 = _Image2DConverterFactory('RGB8ToETC1',
    OGLEnum.GL_RGB8, OGLEnum.GL_ETC1_RGB8_OES,
    'temp.ppm', 'temp.ktx', ' '.join((ETCPACK_NAME, 'temp.ppm', os.curdir, '-ktx', '-c etc1')))
_RegisterConverter(_converters, RGB8ToETC1)

ETC1ToRGB8 = _Image2DConverterFactory('ETC1ToRGB8',
    OGLEnum.GL_ETC1_RGB8_OES, OGLEnum.GL_RGB8,
    'temp.ktx', 'temp.ppm', ' '.join((ETCPACK_NAME, 'temp.ktx', os.curdir, '-ktx', '-c etc1')))
_RegisterConverter(_converters, ETC1ToRGB8)

RGB8ToETC2 = _Image2DConverterFactory('RGB8ToETC2',
    OGLEnum.GL_RGB8, OGLEnum.GL_COMPRESSED_RGB8_ETC2,
    'temp.ppm', 'temp.ktx', ' '.join((ETCPACK_NAME, 'temp.ppm', os.curdir, '-ktx', '-c etc2')))
_RegisterConverter(_converters, RGB8ToETC2)

ETC2ToRGB8 = _Image2DConverterFactory('ETC2ToRGB8',
    OGLEnum.GL_COMPRESSED_RGB8_ETC2, OGLEnum.GL_RGB8,
    'temp.ktx', 'temp.ppm', ' '.join((ETCPACK_NAME, 'temp.ktx', os.curdir, '-ktx', '-c etc2')))
_RegisterConverter(_converters, ETC2ToRGB8)

RGBA8ToETC2_ALHPA1 = _Image2DConverterFactory('RGBA8ToETC2_ALHP1',
    OGLEnum.GL_RGBA8, OGLEnum.GL_COMPRESSED_RGB8_PUNCHTHROUGH_ALPHA1_ETC2,
    'temp.tga', 'temp.ktx', ' '.join((ETCPACK_NAME, 'temp.tga', os.curdir, '-ktx', '-c etc2', '-f RGBA1')))
_RegisterConverter(_converters, RGBA8ToETC2_ALHPA1)

ETC2_ALPHA1ToRGBA8 = _Image2DConverterFactory('ETC2_ALPHA1ToRGBA8',
    OGLEnum.GL_COMPRESSED_RGB8_PUNCHTHROUGH_ALPHA1_ETC2, OGLEnum.GL_RGBA8,
    'temp.ktx', 'temp.tga', ' '.join((ETCPACK_NAME, 'temp.ktx', os.curdir, '-ktx', '-c etc2', '-ext TGA')))
_RegisterConverter(_converters, ETC2_ALPHA1ToRGBA8)

RGBA8ToETC2 = _Image2DConverterFactory('RGBA8ToETC2',
    OGLEnum.GL_RGBA8, OGLEnum.GL_COMPRESSED_RGBA8_ETC2_EAC,
    'temp.tga', 'temp.ktx', ' '.join((ETCPACK_NAME, 'temp.tga', os.curdir, '-ktx', '-c etc2', '-f RGBA8')))
_RegisterConverter(_converters, RGBA8ToETC2)

ETC2ToRGBA8 = _Image2DConverterFactory('ETC2ToRGBA8',
    OGLEnum.GL_COMPRESSED_RGBA8_ETC2_EAC, OGLEnum.GL_RGBA8,
    'temp.ktx', 'temp.tga', ' '.join((ETCPACK_NAME, 'temp.ktx', os.curdir, '-ktx', '-c etc2', '-ext TGA')))
_RegisterConverter(_converters, ETC2ToRGBA8)

_RegisterConverter(_converters, _RGB8_RGBA8_Converter)

def Convert(input_image, dest_format):
    try:
        path = nx.shortest_path(_converters, input_image.internalformat, dest_format)
        for src_node, dest_node in zip(path[:-1], path[1:]):
            con = _converters[src_node][dest_node]['converter']
            input_image = con.Convert(input_image)
        return input_image
    except nx.NetworkXNoPath:
        logger.error('Cannot find conversions from {0} to {1}'.format(OGLEnum.names[input_image.internalformat], OGLEnum.names[dest_format]))
        return Image2D()
