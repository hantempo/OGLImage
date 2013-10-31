import logging
logger = logging.getLogger(__name__)

import Image, os, struct

import OGLCommon
from OGLCommon import OGLEnum, GetGLType, GetGLFormat, GetGLTypeSize
from OGLImage import Image2D

ASTC_HEAD_MAGIC = 0x5CA1AB13
ASTC_HEADER_STRUCT = struct.Struct('I' + 'B' * 12)

KTX_HEADER_STRUCT = struct.Struct('I' * 14)

def SaveImage(filepath, image):

    if image.IsEmpty():
        return

    logger.debug('Saving image as : {0}'.format(filepath))

    ext = os.path.splitext(filepath)[-1]

    if ext == '.ktx':
        SaveKTXImage(filepath, image)
    elif ext == '.astc':
        SaveASTCImage(filepath, image)
    else:
        # use Image module
        format_dict = {
            OGLEnum.GL_RGB8 : 'RGB',
            OGLEnum.GL_RGBA8 : 'RGBA',
        }
        if image.internalformat not in format_dict:
            logger.error('Unexpected internal format when saving image as {1} : {0}'.format(OGLEnum.names[image.internalformat], filepath))
            return

        try:
            Image.fromstring(
                format_dict[image.internalformat],
                (image.width, image.height),
                image.data).save(filepath)
        except IOError:
            logger.error('Failed to save image as {0}'.format(filepath))
            return

def LoadImage(filepath):

    if not os.path.exists(filepath):
        logger.error('Cannot find the specified file ({0}), return an empty image'.format(filepath))
        return Image2D()

    logger.debug('Loading image from : {0}'.format(filepath))

    ext = os.path.splitext(filepath)[-1]
    if ext == '.ktx':
        return LoadKTXImage(filepath)
    elif ext == '.astc':
        return LoadASTCImage(filepath)
    else:
        try:
            im = Image.open(filepath)
            format_dict = {
                'RGB'       : OGLEnum.GL_RGB8,
                'RGBA'      : OGLEnum.GL_RGBA8,
            }
            width, height = im.size
            data = im.tostring()
            return Image2D(width=width, height=height,
                internalformat=format_dict[im.mode],
                dataSize=len(data), data=data)
        except IOError:
            logger.error('Failed to load image from {0}, return an empty image'.format(filepath))
            return Image2D()

def SaveKTXImage(filepath, image):

    with open(filepath, 'w') as f:
        identifier = '\xabKTX 11\xbb\r\n\x1a\n'
        f.write(identifier)

        endianness = 0x04030201
        width = image.width
        height = image.height
        internalformat = image.internalformat
        glType = GetGLType(internalformat)
        glTypeSize = GetGLTypeSize(glType)
        glFormat = GetGLFormat(internalformat)
        header_data = (endianness, glType, glTypeSize, glFormat,
            internalformat, glFormat, width, height, 0,
            0, 1, 1, 0, image.dataSize)
        header = KTX_HEADER_STRUCT.pack(*header_data)
        f.write(header)

        if image.dataSize:
            f.write(image.data)

def SaveASTCImage(filepath, image):

    internalformat = image.internalformat
    width = image.width
    height = image.height
    blockDimX, blockDimY = OGLCommon.ASTC_FORMAT_TO_BLOCK_DIMENSION[internalformat]
    blockDimZ = 1
    xsize0 = width & 0xFF
    xsize1 = (width >> 8) & 0xFF
    xsize2 = (width >> 16) & 0xFF
    ysize0 = height & 0xFF
    ysize1 = (height >> 8) & 0xFF
    ysize2 = (height >> 16) & 0xFF
    zsize0, zsize1, zsize2 = 1, 0, 0

    with open(filepath, 'w') as f:
        f.write(ASTC_HEADER_STRUCT.pack(ASTC_HEAD_MAGIC,
            blockDimX, blockDimY, blockDimZ,
            xsize0, xsize1, xsize2,
            ysize0, ysize1, ysize2,
            zsize0, zsize1, zsize2))

        f.write(image.data)

def LoadKTXImage(filepath):

    if not os.path.exists(filepath):
        logger.error('Cannot find the specified file ({0}), return an empty image'.format(filepath))
        return Image2D()

    with open(filepath) as f:
        identifier = '\xabKTX 11\xbb\r\n\x1a\n'
        data = f.read(len(identifier))
        if data != identifier:
            logger.error('Invalid KTX file')
            return Image2D()

        _, glType, _, glFormat, internalformat, glBaseInternalFormat, \
        width, height, depth, _, _, _, _, dataSize = \
            KTX_HEADER_STRUCT.unpack(f.read(KTX_HEADER_STRUCT.size))
        # if internalformat is not a sized one, try to fix it
        if internalformat in (OGLEnum.GL_RGB, OGLEnum.GL_RGBA):
            internalformat = OGLCommon.GetSizedInternalFormat(glFormat, glType)

        logger.debug('KTX file info : dimension ({0}x{1}) internalformat ({2}) glType({3}) glFormat({4}) dataSize ({5})'.format(width, height,
        OGLEnum.names[internalformat],
        OGLEnum.names[glType],
        OGLEnum.names[glFormat],
        dataSize))
        data = f.read(dataSize)

        return Image2D(width=width, height=height,
            internalformat=internalformat,
            dataSize=dataSize, data=data)

def LoadASTCImage(filepath):

    if not os.path.exists(filepath):
        logger.error('Cannot find the specified file ({0}), return an empty image'.format(filepath))
        return Image2D()

    with open(filepath) as f:
        _, blockDimX, blockDimY, blockDimZ, \
            xsize0, xsize1, xsize2, \
            ysize0, ysize1, ysize2, \
            zsize0, zsize1, zsize2 = \
                ASTC_HEADER_STRUCT.unpack(f.read(ASTC_HEADER_STRUCT.size))

        internalformat = OGLCommon.ASTC_FORMAT_FROM_BLOCK_DIMENSION[(blockDimX, blockDimY)]
        width = xsize0 + xsize1 * 0xFF + xsize2 * 0xFFFF
        height = ysize0 + ysize1 * 0xFF + ysize2 * 0xFFFF
        dataSize = OGLCommon.GetImageSize(width, height, internalformat)
        data = f.read(dataSize)
        return Image2D(width=width, height=height,
            internalformat=internalformat,
            dataSize=dataSize, data=data)
