import logging
logger = logging.getLogger(__name__)

import networkx as nx
import numpy as np
import os, sys

import OGLCommon
from OGLCommon import OGLEnum, GetImageSize
from UtilCommon import Which, RunCommand, Delete
from OGLImage import Image2D
from OGLImageIO import SaveImage, LoadImage

ETCPACK_NAME = 'etcpack'
ASTCENC_NAME = 'astcenc'

# construct and register converter classes
_converters = nx.DiGraph()

def RGB8_RGBA8(input_image):
    width = input_image.width
    height = input_image.height
    pixel_count = width * height
    dataSize = GetImageSize(width, height, OGLEnum.GL_RGBA8)
    rgb_array = np.fromstring(input_image.data, dtype='uint8').reshape((pixel_count, 3))
    a_array = np.empty((pixel_count, 1), dtype='uint8')
    a_array.fill(255)
    rgba_array = np.c_[rgb_array, a_array]
    return Image2D(width=width, height=height,
        internalformat=OGLEnum.GL_RGBA8,
        dataSize=dataSize, data=rgba_array.tostring())

def RGB8_RGB565(input_image):
    width = input_image.width
    height = input_image.height
    pixel_count = width * height
    dataSize = GetImageSize(width, height, OGLEnum.GL_RGB565)
    rgb8_array = np.fromstring(input_image.data, dtype='uint8').reshape((pixel_count, 3))
    def convertion(rgb):
        red, green, blue = rgb
        red = red * (pow(2, 5) - 1) / 0xFF
        green = green * (pow(2, 6) - 1) / 0xFF
        blue = blue * (pow(2, 5) - 1) / 0xFF
        return red << 11 | green << 5 | blue
    rgb565_array = np.array(map(convertion, rgb8_array), dtype='uint16')
    return Image2D(width=width, height=height,
        internalformat=OGLEnum.GL_RGB565,
        dataSize=dataSize, data=rgb565_array.tostring())

def _RegisterImageConverter(src_format, dst_format, convert_func):

    def _convert(input_image):
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

        output_image = convert_func(input_image)

        logger.debug('Output image : {0}'.format(str(output_image)))
        return output_image

    global _converters
    _converters.add_nodes_from([src_format, dst_format])
    _converters.add_edges_from([(src_format, dst_format,
        {'converter' : _convert})])

def _RegisterETCConverter(src_format, dst_format,
    src_file_format, dst_file_format, extra_option=''):

    TEMP_PREFIX = 'temp'
    src_filename = '.'.join((TEMP_PREFIX, src_file_format.lower()))
    dst_filename = '.'.join((TEMP_PREFIX, dst_file_format.lower()))
    tool_cmd = ' '.join((ETCPACK_NAME, src_filename, os.curdir, '-ktx', extra_option))

    def _convert(input_image):
        width = input_image.width
        height = input_image.height
        dataSize = GetImageSize(width, height, dst_format)

        tool_filename = ETCPACK_NAME
        if not Which(tool_filename):
            logger.error('Cannot find the specified tool ({0}) in the environment $PATH, return an empty image with dest format'.format(tool_filename))
            return Image2D(width=width, height=height,
                internalformat=dst_format,
                dataSize=dataSize)

        SaveImage(src_filename, input_image)
        RunCommand(tool_cmd)
        output_image = LoadImage(dst_filename)

        Delete(src_filename)
        Delete(dst_filename)

        return output_image

    _RegisterImageConverter(src_format, dst_format, _convert)

def _RegisterASTCConverter(src_format, dst_format,
    src_file_format, dst_file_format):

    TEMP_PREFIX = 'temp'
    src_filename = '.'.join((TEMP_PREFIX, src_file_format.lower()))
    dst_filename = '.'.join((TEMP_PREFIX, dst_file_format.lower()))
    is_encode = OGLCommon.IsASTCCompressionFormat(dst_format)
    if is_encode:
        (bwidth, bheight) = OGLCommon.ASTC_FORMAT_TO_BLOCK_DIMENSION[dst_format]

    # Note : During compression, if RGB channels are identical for all pixels, they will be combined into one channel
    # and after compression become alpha image instead of RGB
    # TODO : convert A to RGB if the image from decompression contains alpha
    tool_cmd = ' '.join((ASTCENC_NAME, '-cl' if is_encode else '-dl', src_filename, dst_filename,
        '{0}x{1}'.format(bwidth, bheight) if is_encode else '', '-thorough'))

    def _convert(input_image):
        width = input_image.width
        height = input_image.height
        dataSize = GetImageSize(width, height, dst_format)

        tool_filename = ASTCENC_NAME
        if not Which(tool_filename):
            logger.error('Cannot find the specified tool ({0}) in the environment $PATH, return an empty image with dest format'.format(tool_filename))
            return Image2D(width=width, height=height,
                internalformat=dst_format,
                dataSize=dataSize)

        SaveImage(src_filename, input_image)
        RunCommand(tool_cmd)
        output_image = LoadImage(dst_filename)

        #Delete(src_filename)
        #Delete(dst_filename)

        return output_image

    _RegisterImageConverter(src_format, dst_format, _convert)

_RegisterETCConverter(OGLEnum.GL_RGB8, OGLEnum.GL_ETC1_RGB8_OES,
    'PPM', 'KTX', '-c etc1')
_RegisterETCConverter(OGLEnum.GL_ETC1_RGB8_OES, OGLEnum.GL_RGB8,
    'KTX', 'PPM', '-c etc1')
_RegisterETCConverter(OGLEnum.GL_RGB8, OGLEnum.GL_COMPRESSED_RGB8_ETC2,
    'PPM', 'KTX')
_RegisterETCConverter(OGLEnum.GL_COMPRESSED_RGB8_ETC2, OGLEnum.GL_RGB8,
    'KTX', 'PPM')
_RegisterETCConverter(OGLEnum.GL_RGBA8, OGLEnum.GL_COMPRESSED_RGB8_PUNCHTHROUGH_ALPHA1_ETC2,
    'TGA', 'KTX', '-f RGBA1')
_RegisterETCConverter(OGLEnum.GL_COMPRESSED_RGB8_PUNCHTHROUGH_ALPHA1_ETC2, OGLEnum.GL_RGBA8,
    'KTX', 'TGA', '-ext TGA')
_RegisterETCConverter(OGLEnum.GL_RGBA8, OGLEnum.GL_COMPRESSED_RGBA8_ETC2_EAC,
    'TGA', 'KTX', '-f RGBA8')
_RegisterETCConverter(OGLEnum.GL_COMPRESSED_RGBA8_ETC2_EAC, OGLEnum.GL_RGBA8,
    'KTX', 'TGA', '-ext TGA')

_RegisterASTCConverter(OGLEnum.GL_RGBA8, OGLEnum.GL_COMPRESSED_RGBA_ASTC_4x4_KHR, 'KTX', 'ASTC')
_RegisterASTCConverter(OGLEnum.GL_COMPRESSED_RGBA_ASTC_4x4_KHR, OGLEnum.GL_RGBA8, 'ASTC', 'KTX')

_RegisterImageConverter(OGLEnum.GL_RGB8, OGLEnum.GL_RGBA8, RGB8_RGBA8)
_RegisterImageConverter(OGLEnum.GL_RGB8, OGLEnum.GL_RGB565, RGB8_RGB565)

def Convert(input_image, dest_format):
    try:
        path = nx.shortest_path(_converters, input_image.internalformat, dest_format)
        for src_node, dest_node in zip(path[:-1], path[1:]):
            con = _converters[src_node][dest_node]['converter']
            input_image = con(input_image)
        return input_image
    except nx.NetworkXNoPath:
        logger.error('Cannot find conversions from {0} to {1}'.format(OGLEnum.names[input_image.internalformat], OGLEnum.names[dest_format]))
        return Image2D()
