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
    GL_HALF_FLOAT                   = 0x140B,
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

    GL_COMPRESSED_RGBA_ASTC_4x4_KHR            = 0x93B0,
    GL_COMPRESSED_RGBA_ASTC_5x4_KHR            = 0x93B1,
    GL_COMPRESSED_RGBA_ASTC_5x5_KHR            = 0x93B2,
    GL_COMPRESSED_RGBA_ASTC_6x5_KHR            = 0x93B3,
    GL_COMPRESSED_RGBA_ASTC_6x6_KHR            = 0x93B4,
    GL_COMPRESSED_RGBA_ASTC_8x5_KHR            = 0x93B5,
    GL_COMPRESSED_RGBA_ASTC_8x6_KHR            = 0x93B6,
    GL_COMPRESSED_RGBA_ASTC_8x8_KHR            = 0x93B7,
    GL_COMPRESSED_RGBA_ASTC_10x5_KHR           = 0x93B8,
    GL_COMPRESSED_RGBA_ASTC_10x6_KHR           = 0x93B9,
    GL_COMPRESSED_RGBA_ASTC_10x8_KHR           = 0x93BA,
    GL_COMPRESSED_RGBA_ASTC_10x10_KHR          = 0x93BB,
    GL_COMPRESSED_RGBA_ASTC_12x10_KHR          = 0x93BC,
    GL_COMPRESSED_RGBA_ASTC_12x12_KHR          = 0x93BD,

    GL_COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR    = 0x93D0,
    GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR    = 0x93D1,
    GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR    = 0x93D2,
    GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR    = 0x93D3,
    GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR    = 0x93D4,
    GL_COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR    = 0x93D5,
    GL_COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR    = 0x93D6,
    GL_COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR    = 0x93D7,
    GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR   = 0x93D8,
    GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR   = 0x93D9,
    GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR   = 0x93DA,
    GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR  = 0x93DB,
    GL_COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR  = 0x93DC,
    GL_COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR  = 0x93DD,
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

PIXEL_SIZE_2 = (
    OGLEnum.GL_RGB565,
)

PIXEL_SIZE_3 = (
    OGLEnum.GL_RGB8,
)

PIXEL_SIZE_4 = (
    OGLEnum.GL_RGBA8,
)

ASTC_FORMAT_TO_BLOCK_DIMENSION = {
    OGLEnum.GL_COMPRESSED_RGBA_ASTC_4x4_KHR            : (4, 4),
    OGLEnum.GL_COMPRESSED_RGBA_ASTC_5x4_KHR            : (5, 4),
    OGLEnum.GL_COMPRESSED_RGBA_ASTC_5x5_KHR            : (5, 5),
    OGLEnum.GL_COMPRESSED_RGBA_ASTC_6x5_KHR            : (6, 5),
    OGLEnum.GL_COMPRESSED_RGBA_ASTC_6x6_KHR            : (6, 6),
    OGLEnum.GL_COMPRESSED_RGBA_ASTC_8x5_KHR            : (8, 5),
    OGLEnum.GL_COMPRESSED_RGBA_ASTC_8x6_KHR            : (8, 6),
    OGLEnum.GL_COMPRESSED_RGBA_ASTC_8x8_KHR            : (8, 8),
    OGLEnum.GL_COMPRESSED_RGBA_ASTC_10x5_KHR           : (10, 5),
    OGLEnum.GL_COMPRESSED_RGBA_ASTC_10x6_KHR           : (10, 6),
    OGLEnum.GL_COMPRESSED_RGBA_ASTC_10x8_KHR           : (10, 8),
    OGLEnum.GL_COMPRESSED_RGBA_ASTC_10x10_KHR          : (10, 10),
    OGLEnum.GL_COMPRESSED_RGBA_ASTC_12x10_KHR          : (12, 10),
    OGLEnum.GL_COMPRESSED_RGBA_ASTC_12x12_KHR          : (12, 12),

    #OGLEnum.GL_COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR    : (4, 4),
    #OGLEnum.GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR    : (5, 4),
    #OGLEnum.GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR    : (5, 5),
    #OGLEnum.GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR    : (6, 5),
    #OGLEnum.GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR    : (6, 6),
    #OGLEnum.GL_COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR    : (8, 5),
    #OGLEnum.GL_COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR    : (8, 6),
    #OGLEnum.GL_COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR    : (8, 8),
    #OGLEnum.GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR   : (10, 5),
    #OGLEnum.GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR   : (10, 6),
    #OGLEnum.GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR   : (10, 8),
    #OGLEnum.GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR  : (10, 10),
    #OGLEnum.GL_COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR  : (12, 10),
    #OGLEnum.GL_COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR  : (12, 12),
}

ASTC_FORMAT_FROM_BLOCK_DIMENSION = dict(
    (dim, enum) for enum, dim in ASTC_FORMAT_TO_BLOCK_DIMENSION.items())

def GetASTCCompressionImageSize(width, height, internalformat):
    if not IsASTCCompressionFormat(internalformat):
        return 0

    bwidth, bheight = ASTC_FORMAT_TO_BLOCK_DIMENSION[internalformat]
    return ((width + bwidth - 1) / bwidth) * ((height + bheight - 1) / bheight) * 16

def IsASTCCompressionFormat(internalformat):
    return OGLEnum.GL_COMPRESSED_RGBA_ASTC_4x4_KHR <= internalformat \
        <= OGLEnum.GL_COMPRESSED_RGBA_ASTC_12x12_KHR or \
           OGLEnum.GL_COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR <= internalformat \
        <= OGLEnum.GL_COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR

def IsCompressionFormat(internalformat):
    if internalformat in ETC_64BIT_FORMATS or \
       internalformat in ETC_128BIT_FORMATS or \
       IsASTCCompressionFormat(internalformat):
       return True
    else:
       return False

def GetSizedInternalFormat(glFormat, glType):
    if glFormat == OGLEnum.GL_RGB:
        if glType == OGLEnum.GL_UNSIGNED_BYTE:
            return OGLEnum.GL_RGB8
        elif glType == OGLEnum.GL_UNSIGNED_SHORT_5_6_5:
            return OGLEnum.GL_RGB565

    if glFormat == OGLEnum.GL_RGBA:
        if glType == OGLEnum.GL_UNSIGNED_BYTE:
            return OGLEnum.GL_RGBA8
        elif glType == OGLEnum.GL_UNSIGNED_SHORT_4_4_4_4:
            return OGLEnum.GL_RGBA4
        elif glType == OGLEnum.GL_UNSIGNED_SHORT_5_5_5_1:
            return OGLEnum.GL_RGB5_A1

    logger.error('GetSizedInternalFormat, unexpected glFormat ({0}) and glType ({1})'.format(glFormat, glType))

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
    if internalformat in PIXEL_SIZE_2: return 2
    if internalformat in PIXEL_SIZE_3: return 3
    if internalformat in PIXEL_SIZE_4: return 4
    logger.error('unexpected internal format : {0}'.format(OGLEnum.names[internalformat]))
    return 0

# return image size in bytes
def GetImageSize(width, height, internalformat):
    if internalformat in ETC_64BIT_FORMATS:
        return ((width+3)/4) * ((height+3)/4) * 8

    if internalformat in ETC_128BIT_FORMATS:
        return ((width+3)/4) * ((height+3)/4) * 16

    if IsASTCCompressionFormat(internalformat):
        return GetASTCCompressionImageSize(width, height, internalformat)

    return width * height * GetPixelSize(internalformat)
