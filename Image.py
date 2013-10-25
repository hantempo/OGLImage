

class Image2D(object):

    def __init__(self, width, height,
        internalformat, dataSize, data):
        self.width = width
        self.height = height
        self.internalformat = internalformat
        self.dataSize = dataSize
        self.data = data
