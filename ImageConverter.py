import logging
from OGLCommon import OGLEnum

class ImageConverter(object):

    @staticmethod
    def Convert(input_image):
        logger = logging.getLogger()
        logger.error('The base ImageConverter should not be called')
        return input_image

class RGB8ToETC1(object):

    source_format = OGLEnum.GL_RGB8
    dest_format = OGLEnum.GL_ETC1_RGB8_OES

    @staticmethod
    def Convert(input_image):
        logger = logging.getLogger()
        logger.debug('Conversion from RGB8 to ETC1')
        logger.debug('Input image : {0}'.format(str(input_image)))

        logger.debug('output image : {0}'.format(str(input_image)))
        return input_image
