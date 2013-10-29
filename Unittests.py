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
        empty_image = Image2D(2, 2, internalformat=OGLEnum.GL_RGB8, dataSize=12)
        output = Convert(empty_image, OGLEnum.GL_ETC1_RGB8_OES)
        self.assertEqual(output.width, 2)
        self.assertEqual(output.height, 2)
        self.assertEqual(output.internalformat, OGLEnum.GL_ETC1_RGB8_OES)
        self.assertEqual(output.dataSize, 8)
        self.assertTrue(output.IsEmpty())

        raw_data = 'FFFFFF0000000F0F0FF0F0F0'.decode('hex')
        etc1_data = '7B7B7BFD111E333F'.decode('hex')
        uncom_data = 'FFFFFF000000000000FFFFFF'.decode('hex')
        etc1_image = Convert(Image2D(2, 2,
            internalformat=OGLEnum.GL_RGB8, dataSize=len(raw_data), data=raw_data),
            OGLEnum.GL_ETC1_RGB8_OES)
        self.assertEqual(etc1_image.width, 2)
        self.assertEqual(etc1_image.height, 2)
        self.assertEqual(etc1_image.internalformat, OGLEnum.GL_ETC1_RGB8_OES)
        self.assertEqual(etc1_image.dataSize, len(etc1_data))
        self.assertTrue(not etc1_image.IsEmpty())
        self.assertEqual(etc1_image.data, etc1_data)

        raw_image = Convert(etc1_image, OGLEnum.GL_RGB8)
        self.assertEqual(raw_image.width, 2)
        self.assertEqual(raw_image.height, 2)
        self.assertEqual(raw_image.internalformat, OGLEnum.GL_RGB8)
        self.assertEqual(raw_image.dataSize, len(raw_data))
        self.assertEqual(raw_image.data, uncom_data)

    def test_RGB8ToETC2(self):
        empty_image = Image2D(2, 2, internalformat=OGLEnum.GL_RGB8, dataSize=12)
        output = Convert(empty_image, OGLEnum.GL_COMPRESSED_RGB8_ETC2)
        self.assertEqual(output.width, 2)
        self.assertEqual(output.height, 2)
        self.assertEqual(output.internalformat, OGLEnum.GL_COMPRESSED_RGB8_ETC2)
        self.assertEqual(output.dataSize, 8)
        self.assertTrue(output.IsEmpty())

        raw_data = 'FFFFFF0000000F0F0FF0F0F0'.decode('hex')
        etc2_data = 'FAEE00071110000E'.decode('hex')
        uncom_data = 'EEEEEE000000101010EEEEEE'.decode('hex')
        etc2_image = Convert(Image2D(2, 2,
            internalformat=OGLEnum.GL_RGB8, dataSize=len(raw_data), data=raw_data),
            OGLEnum.GL_COMPRESSED_RGB8_ETC2)
        self.assertEqual(etc2_image.width, 2)
        self.assertEqual(etc2_image.height, 2)
        self.assertEqual(etc2_image.internalformat, OGLEnum.GL_COMPRESSED_RGB8_ETC2)
        self.assertEqual(etc2_image.dataSize, len(etc2_data))
        self.assertTrue(not etc2_image.IsEmpty())
        self.assertEqual(etc2_image.data, etc2_data)

        raw_image = Convert(etc2_image, OGLEnum.GL_RGB8)
        self.assertEqual(raw_image.width, 2)
        self.assertEqual(raw_image.height, 2)
        self.assertEqual(raw_image.internalformat, OGLEnum.GL_RGB8)
        self.assertEqual(raw_image.dataSize, len(raw_data))
        self.assertTrue(not raw_image.IsEmpty())
        self.assertEqual(raw_image.data, uncom_data)

    def test_RGBA8ToETC2_ALPHA1(self):
        empty_image = Image2D(2, 2, internalformat=OGLEnum.GL_RGBA8, dataSize=16)
        output = Convert(empty_image, OGLEnum.GL_COMPRESSED_RGB8_PUNCHTHROUGH_ALPHA1_ETC2)
        self.assertEqual(output.width, 2)
        self.assertEqual(output.height, 2)
        self.assertEqual(output.internalformat, OGLEnum.GL_COMPRESSED_RGB8_PUNCHTHROUGH_ALPHA1_ETC2)
        self.assertEqual(output.dataSize, 8)
        self.assertTrue(output.IsEmpty())

        raw_data = 'FFFFFFFF000000000F0F0F0FF0F0F0F0'.decode('hex')
        etc2_data = '0400EEE0001EEEE1'.decode('hex')
        uncom_data = 'F1F1F1FF0000000000000000F1F1F1FF'.decode('hex')
        etc2_image = Convert(Image2D(2, 2,
            internalformat=OGLEnum.GL_RGBA8, dataSize=len(raw_data), data=raw_data),
            OGLEnum.GL_COMPRESSED_RGB8_PUNCHTHROUGH_ALPHA1_ETC2)
        self.assertEqual(etc2_image.width, 2)
        self.assertEqual(etc2_image.height, 2)
        self.assertEqual(etc2_image.internalformat, OGLEnum.GL_COMPRESSED_RGB8_PUNCHTHROUGH_ALPHA1_ETC2)
        self.assertEqual(etc2_image.dataSize, len(etc2_data))
        self.assertTrue(not etc2_image.IsEmpty())
        self.assertEqual(etc2_image.data, etc2_data)

        raw_image = Convert(etc2_image, OGLEnum.GL_RGBA8)
        self.assertEqual(raw_image.width, 2)
        self.assertEqual(raw_image.height, 2)
        self.assertEqual(raw_image.internalformat, OGLEnum.GL_RGBA8)
        self.assertEqual(raw_image.dataSize, len(raw_data))
        self.assertTrue(not raw_image.IsEmpty())
        self.assertEqual(raw_image.data, uncom_data)

    def test_RGBA8ToETC2(self):
        empty_image = Image2D(2, 2, internalformat=OGLEnum.GL_RGBA8, dataSize=16)
        output = Convert(empty_image, OGLEnum.GL_COMPRESSED_RGBA8_ETC2_EAC)
        self.assertEqual(output.width, 2)
        self.assertEqual(output.height, 2)
        self.assertEqual(output.internalformat, OGLEnum.GL_COMPRESSED_RGBA8_ETC2_EAC)
        self.assertEqual(output.dataSize, 16)
        self.assertTrue(output.IsEmpty())

        raw_data = 'FFFFFFFF000000000F0F0F0FF0F0F0F0'.decode('hex')
        etc2_data = '87F2E927B6DB6DB6FAEE00071110000E'.decode('hex')
        uncom_data = 'EEEEEEFF000000001010100FEEEEEEF0'.decode('hex')
        etc2_image = Convert(Image2D(2, 2,
            internalformat=OGLEnum.GL_RGBA8, dataSize=len(raw_data), data=raw_data),
            OGLEnum.GL_COMPRESSED_RGBA8_ETC2_EAC)
        self.assertEqual(etc2_image.width, 2)
        self.assertEqual(etc2_image.height, 2)
        self.assertEqual(etc2_image.internalformat, OGLEnum.GL_COMPRESSED_RGBA8_ETC2_EAC)
        self.assertEqual(etc2_image.dataSize, len(etc2_data))
        self.assertTrue(not etc2_image.IsEmpty())
        self.assertEqual(etc2_image.data, etc2_data)

        raw_image = Convert(etc2_image, OGLEnum.GL_RGBA8)
        self.assertEqual(raw_image.width, 2)
        self.assertEqual(raw_image.height, 2)
        self.assertEqual(raw_image.internalformat, OGLEnum.GL_RGBA8)
        self.assertEqual(raw_image.dataSize, len(raw_data))
        self.assertTrue(not raw_image.IsEmpty())
        self.assertEqual(raw_image.data, uncom_data)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    unittest.main()
