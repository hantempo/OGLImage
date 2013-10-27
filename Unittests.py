import unittest

from OGLCommon import OGLEnum
from OGLImage import *
from OGLImageConverter import *

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

        output = RGB8ToETC1.Convert(Image2D(2, 2,
            internalformat=OGLEnum.GL_RGB8, dataSize=12))
        self.assertEqual(output.width, 2)
        self.assertEqual(output.height, 2)
        self.assertEqual(output.internalformat, OGLEnum.GL_ETC1_RGB8_OES)
        self.assertEqual(output.dataSize, 8)
        self.assertTrue(output.IsEmpty())

        raw_data = 'FFFFFF0000000F0F0FF0F0F0'.decode('hex')
        etc1_data = '7B7B7BFD111E333F'.decode('hex')
        etc1_image = RGB8ToETC1.Convert(Image2D(2, 2,
            internalformat=OGLEnum.GL_RGB8, dataSize=len(raw_data), data=raw_data))
        self.assertEqual(etc1_image.width, 2)
        self.assertEqual(etc1_image.height, 2)
        self.assertEqual(etc1_image.internalformat, OGLEnum.GL_ETC1_RGB8_OES)
        self.assertEqual(etc1_image.dataSize, len(etc1_data))
        self.assertTrue(not etc1_image.IsEmpty())
        self.assertEqual(etc1_image.data, etc1_data)

        raw_image = ETC1ToRGB8.Convert(etc1_image)
        self.assertEqual(raw_image.width, 2)
        self.assertEqual(raw_image.height, 2)
        self.assertEqual(raw_image.internalformat, OGLEnum.GL_RGB8)
        self.assertEqual(raw_image.dataSize, len(raw_data))
        self.assertTrue(not raw_image.IsEmpty())

    def test_Convert(self):
        im = Image2D(internalformat=OGLEnum.GL_RGB8)
        om = Convert(im, OGLEnum.GL_ETC1_RGB8_OES)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
