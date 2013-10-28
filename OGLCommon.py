import logging
logger = logging.getLogger(__name__)

from math import ceil

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['names'] = reverse
    return type('Enum', (), enums)

OGLEnum = enum(
    GL_NONE                         = 0x0000,

    GL_TEXTURE_2D                   = 0x0DE1,
    GL_TEXTURE_CUBE_MAP             = 0x8513,
    GL_TEXTURE_CUBE_MAP_POSITIVE_X  = 0x8515,
    GL_TEXTURE_CUBE_MAP_NEGATIVE_X  = 0x8516,
    GL_TEXTURE_CUBE_MAP_POSITIVE_Y  = 0x8517,
    GL_TEXTURE_CUBE_MAP_NEGATIVE_Y  = 0x8518,
    GL_TEXTURE_CUBE_MAP_POSITIVE_Z  = 0x8519,
    GL_TEXTURE_CUBE_MAP_NEGATIVE_Z  = 0x851A,
    GL_TEXTURE_2D_ARRAY             = 0x8C1A,
    GL_TEXTURE_3D                   = 0x806F,

    GL_BYTE                         = 0x1400,
    GL_UNSIGNED_BYTE                = 0x1401,
    GL_SHORT                        = 0x1402,
    GL_UNSIGNED_SHORT               = 0x1403,
    GL_INT                          = 0x1404,
    GL_UNSIGNED_INT                 = 0x1405,
    GL_FLOAT                        = 0x1406,
    GL_FIXED                        = 0x140C,

    GL_DEPTH_COMPONENT              = 0x1902,
    GL_ALPHA                        = 0x1906,
    GL_RGB                          = 0x1907,
    GL_RGBA                         = 0x1908,
    GL_LUMINANCE                    = 0x1909,
    GL_LUMINANCE_ALPHA              = 0x190A,

    GL_UNSIGNED_SHORT_4_4_4_4       = 0x8033,
    GL_UNSIGNED_SHORT_5_5_5_1       = 0x8034,
    GL_UNSIGNED_SHORT_5_6_5         = 0x8363,

    GL_RGB8                         = 0x8051,
    GL_RGBA8                        = 0x8058,
    GL_RGB10_A2                     = 0x8059,
    GL_DEPTH_COMPONENT24            = 0x81A6,
    GL_RGBA4                        = 0x8056,
    GL_RGB5_A1                      = 0x8057,
    GL_RGB565                       = 0x8D62,
    GL_DEPTH_COMPONENT16            = 0x81A5,
    GL_STENCIL_INDEX8               = 0x8D48,

    GL_ETC1_RGB8_OES                = 0x8D64,
    GL_COMPRESSED_RGB8_ETC2         = 0x9274,
    GL_COMPRESSED_SRGB8_ETC2        = 0x9275,
    GL_COMPRESSED_RGB8_PUNCHTHROUGH_ALPHA1_ETC2 = 0x9276,
    GL_COMPRESSED_SRGB8_PUNCHTHROUGH_ALPHA1_ETC2 = 0x9277,
    GL_COMPRESSED_RGBA8_ETC2_EAC    = 0x9278,
    GL_COMPRESSED_SRGB8_ALPHA8_ETC2_EAC = 0x9279,
    )

ETC_64BIT_FORMATS = (
    OGLEnum.GL_ETC1_RGB8_OES,
    OGLEnum.GL_COMPRESSED_RGB8_ETC2,
    OGLEnum.GL_COMPRESSED_SRGB8_ETC2,
    OGLEnum.GL_COMPRESSED_RGB8_PUNCHTHROUGH_ALPHA1_ETC2,
    OGLEnum.GL_COMPRESSED_SRGB8_PUNCHTHROUGH_ALPHA1_ETC2,
)

ETC_128BIT_FORMATS = (
    OGLEnum.GL_COMPRESSED_RGBA8_ETC2_EAC,
    OGLEnum.GL_COMPRESSED_SRGB8_ALPHA8_ETC2_EAC,
)

PIXEL_SIZE_3 = (
    OGLEnum.GL_RGB8,
)

PIXEL_SIZE_4 = (
    OGLEnum.GL_RGBA8,
)

def IsCompressionFormat(internalformat):
    if internalformat in ETC_64BIT_FORMATS or \
       internalformat in ETC_128BIT_FORMATS:
       return True
    else:
       return False

def GetGLType(internalformat):
    mapping = {
        OGLEnum.GL_RGB8         : OGLEnum.GL_UNSIGNED_BYTE,
        OGLEnum.GL_RGBA8        : OGLEnum.GL_UNSIGNED_BYTE,
    }
    if IsCompressionFormat(internalformat):
        return 0
    else:
        try:
            return mapping[internalformat]
        except:
            logger.error('GetGLType, unexpected internalformat ({0})'.format(OGLEnum.names[internalformat]))
            return 0

def GetGLTypeSize(glType):
    mapping = {
        OGLEnum.GL_BYTE                 : 1,
        OGLEnum.GL_UNSIGNED_BYTE        : 1,
        OGLEnum.GL_SHORT                : 2,
        OGLEnum.GL_UNSIGNED_SHORT       : 2,
        OGLEnum.GL_INT                  : 4,
        OGLEnum.GL_UNSIGNED_INT         : 4,
    }
    if glType == 0: # for compression type
        return 1
    else:
        try:
            return mapping[glType]
        except:
            logger.error('GetGLTypeSize, unexpected type ({0})'.format(OGLEnum.names[glType]))
            return 0


def GetGLFormat(internalformat):
    mapping = {
        OGLEnum.GL_RGB8         : OGLEnum.GL_RGB,
        OGLEnum.GL_RGBA8        : OGLEnum.GL_RGBA,
    }
    if IsCompressionFormat(internalformat):
        return 0
    else:
        try:
            return mapping[internalformat]
        except:
            logger.error('GetGLFormat, unexpected internalformat ({0})'.format(OGLEnum.names[internalformat]))
            return 0

# return pixel size in bytes
def GetPixelSize(internalformat):
    if internalformat in PIXEL_SIZE_3:
        return 3
    if internalformat in PIXEL_SIZE_4:
        return 4
    logger.error('unexpected internal format : {0}'.format(OGLEnum.names[internalformat]))
    return 0

# return image size in bytes
def GetImageSize(width, height, internalformat):
    if internalformat in ETC_64BIT_FORMATS:
        return int(ceil(width/4.) * ceil(height/4.) * 8)

    if internalformat in ETC_128BIT_FORMATS:
        return int(ceil(width/4.) * ceil(height/4.) * 16)

    return width * height * GetPixelSize(internalformat)
