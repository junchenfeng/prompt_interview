import unittest
from code import VideoPreview


class TestVideoPreview(unittest.TestCase):
    def test_set_image_preview(self):
        preview = VideoPreview()
        preview.set_image_preview()
        self.assertIsNotNone(preview.video_url, 'Video URL should not be None')

    def test_get_image_preview(self):
        preview = VideoPreview()
        preview.set_image_preview()
        result = preview.get_image_preview()
        self.assertTrue(result.startswith('COS存储地址:'), 'Result should start with "COS存储地址:"')


if __name__ == '__main__':
    unittest.main()
