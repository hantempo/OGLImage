import unittest

from OGLCommon import OGLEnum
from Image import Image2D
from ImageConverter import *

class TestImage2D(unittest.TestCase):

    def test_initial(self):
        im = Image2D(2, 2, OGLEnum.GL_RGB8, 12, "")
        self.assertTrue(im.width == 2)
        self.assertTrue(im.height == 2)
        self.assertTrue(im.internalformat == OGLEnum.GL_RGB8)
        self.assertTrue(im.dataSize == 12)
        self.assertEqual(str(im),
            "Image2D : dimension(2x2), internalformat(GL_RGB8), dataSize(12)")

class TestImageConverter(unittest.TestCase):

    def test_RGB8ToETC1(self):
        self.assertTrue(RGB8ToETC1.source_format == OGLEnum.GL_RGB8)
        self.assertTrue(RGB8ToETC1.dest_format == OGLEnum.GL_ETC1_RGB8_OES)
        RGB8ToETC1.Convert(Image2D())

    def test_Convert(self):
        im = Image2D(internalformat=OGLEnum.GL_RGB8)
        om = Convert(im, OGLEnum.GL_ETC1_RGB8_OES)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
