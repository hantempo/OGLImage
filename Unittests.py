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

class TestUncompressionConversion(unittest.TestCase):

    def test_RGB8_RGBA8(self):
        empty_image = Image2D(2, 2, internalformat=OGLEnum.GL_RGB8, dataSize=12)
        output = Convert(empty_image, OGLEnum.GL_RGBA8)
        self.assertEqual(output.width, 2)
        self.assertEqual(output.height, 2)
        self.assertEqual(output.internalformat, OGLEnum.GL_RGBA8)
        self.assertEqual(output.dataSize, 16)
        self.assertTrue(output.IsEmpty())

        rgb_data = 'FFFFFF0000000F0F0FF0F0F0'.decode('hex')
        rgba_data = 'FFFFFFFF000000FF0F0F0FFFF0F0F0FF'.decode('hex')
        rgba_image = Convert(Image2D(2, 2,
            internalformat=OGLEnum.GL_RGB8, dataSize=len(rgb_data), data=rgb_data),
            OGLEnum.GL_RGBA8)
        self.assertEqual(rgba_image.width, 2)
        self.assertEqual(rgba_image.height, 2)
        self.assertEqual(rgba_image.internalformat, OGLEnum.GL_RGBA8)
        self.assertEqual(rgba_image.dataSize, len(rgba_data))
        self.assertTrue(not rgba_image.IsEmpty())
        self.assertEqual(rgba_image.data, rgba_data)

    def test_RGB8_RGB565(self):
        empty_image = Image2D(2, 1, internalformat=OGLEnum.GL_RGB8, dataSize=6)
        output = Convert(empty_image, OGLEnum.GL_RGB565)
        self.assertEqual(output.width, 2)
        self.assertEqual(output.height, 1)
        self.assertEqual(output.internalformat, OGLEnum.GL_RGB565)
        self.assertEqual(output.dataSize, 4)
        self.assertTrue(output.IsEmpty())

        rgb8_data = 'FF0FF0000AA0'.decode('hex')
        rgb565_data = '7DF85300'.decode('hex')
        rgb565_image = Convert(Image2D(2, 1,
            internalformat=OGLEnum.GL_RGB8, dataSize=len(rgb8_data), data=rgb8_data),
            OGLEnum.GL_RGB565)
        self.assertEqual(rgb565_image.width, 2)
        self.assertEqual(rgb565_image.height, 1)
        self.assertEqual(rgb565_image.internalformat, OGLEnum.GL_RGB565)
        self.assertEqual(rgb565_image.dataSize, len(rgb565_data))
        self.assertTrue(not rgb565_image.IsEmpty())
        self.assertEqual(rgb565_image.data, rgb565_data)

class TestETCConvertion(unittest.TestCase):

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

class TestASTCConvertion(unittest.TestCase):

    def test_RGBA8ToRGBA_ASTC_4x4(self):
        empty_image = Image2D(2, 2, internalformat=OGLEnum.GL_RGBA8, dataSize=16)
        output = Convert(empty_image, OGLEnum.GL_COMPRESSED_RGBA_ASTC_4x4_KHR)
        self.assertEqual(output.width, 2)
        self.assertEqual(output.height, 2)
        self.assertEqual(output.internalformat, OGLEnum.GL_COMPRESSED_RGBA_ASTC_4x4_KHR)
        self.assertEqual(output.dataSize, 16)
        self.assertTrue(output.IsEmpty())

        raw_data = 'FF0F0FFF000000000F0F0F0FF0F0F0F0'.decode('hex')
        astc_data = '225045993CF236DCF00B01C0973A15C0'.decode('hex')
        uncom_data = 'FF1010FF000000000F0F0F0FF0F0F0F0'.decode('hex')
        astc_image = Convert(Image2D(2, 2,
            internalformat=OGLEnum.GL_RGBA8, dataSize=len(raw_data), data=raw_data),
            OGLEnum.GL_COMPRESSED_RGBA_ASTC_4x4_KHR)
        self.assertEqual(astc_image.width, 2)
        self.assertEqual(astc_image.height, 2)
        self.assertEqual(astc_image.internalformat, OGLEnum.GL_COMPRESSED_RGBA_ASTC_4x4_KHR)
        self.assertEqual(astc_image.dataSize, len(astc_data))
        self.assertTrue(not astc_image.IsEmpty())
        self.assertEqual(astc_image.data, astc_data)

        raw_image = Convert(astc_image, OGLEnum.GL_RGBA8)
        self.assertEqual(raw_image.width, 2)
        self.assertEqual(raw_image.height, 2)
        self.assertEqual(raw_image.internalformat, OGLEnum.GL_RGBA8)
        self.assertEqual(raw_image.dataSize, len(uncom_data))
        self.assertTrue(not raw_image.IsEmpty())
        self.assertEqual(raw_image.data, uncom_data)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    unittest.main()
