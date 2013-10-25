import logging
logger = logging.getLogger(__name__)

from OGLCommon import OGLEnum

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
