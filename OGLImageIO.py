import logging
logger = logging.getLogger(__name__)

import Image, os, struct

from OGLCommon import OGLEnum
from OGLImage import Image2D

def SaveImage(filepath, image):

    if image.IsEmpty():
        return

    ext = os.path.splitext(filepath)[-1]

    if ext == '.ktx':
        logger.error('Should not here')
    else:
        # use Image module
        format_dict = {
            OGLEnum.GL_RGB8 : 'RGB',
            OGLEnum.GL_RGBA8 : 'RGBA',
        }
        Image.fromstring(
            format_dict[image.internalformat],
            (image.width, image.height),
            image.data).save(filepath)
        logger.debug('Save image as : {0}'.format(filepath))

def LoadImage(filepath):

    if not os.path.exists(filepath):
        logger.error('Cannot find the specified file, return an empty image')
        return Image2D()

    ext = os.path.splitext(filepath)[-1]
    if ext == '.ktx':
        return LoadKTXImage(filepath)
    else:
        logger.error('Should not here')

def LoadKTXImage(filepath):

    if not os.path.exists(filepath):
        logger.error('Cannot find the specified file, return an empty image')
        return Image2D()

    with open(filepath) as f:
        identifier = '\xabKTX 11\xbb\r\n\x1a\n'
        data = f.read(len(identifier))
        if data != identifier:
            logger.error('Invalid KTX file')
            return Image2D()

        header_struct = struct.Struct('I'*14)
        header = header_struct.unpack(f.read(14 * 4))
        internalformat = header[4]
        width = header[6]
        height = header[7]
        dataSize = header[-1]
        data = f.read(dataSize)
        return Image2D(width=width, height=height,
            internalformat=internalformat,
            dataSize=dataSize, data=data)
