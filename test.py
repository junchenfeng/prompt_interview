import unittest
from unittest.mock import MagicMock, patch
from video_preview import VideoPreview

class TestVideoPreview(unittest.TestCase):
    def setUp(self):
        """在每个测试方法之前初始化VideoPreview实例。"""
        self.video_preview = VideoPreview("test_bucket", "test_region", "test_secret_id", "test_secret_key")

    @patch('requests.get')
    @patch('video_preview.CosS3Client.put_object')
    def test_set_image_preview_success(self, mock_put_object, mock_get):
        """测试set_image_preview成功保存图片到COS桶。"""
        mock_response = MagicMock()
        mock_response.raw = b"test_image_data"
        mock_response.raise_for_status.side_effect = None
        mock_get.return_value = mock_response

        result = self.video_preview.set_image_preview("test_image_id", "https://example.com/img.png")
        self.assertIsNotNone(result)
        self.assertEqual(result, "https://test_bucket.cos.test_region.myqcloud.com/test_image_id")
    
    @patch('requests.get')
    def test_set_image_preview_failure(self, mock_get):
        """测试set_image_preview在保存图片失败时返回None。"""
        mock_get.side_effect = Exception("Test exception")

        result = self.video_preview.set_image_preview("test_image_id", "https://example.com/img.png")
        self.assertIsNone(result)

    @patch('video_preview.CosS3Client.head_object')
    def test_get_image_preview_success(self, mock_head_object):
        """测试get_image_preview成功获取COS桶中的图片预览URL。"""
        mock_head_object.side_effect = None

        result = self.video_preview.get_image_preview("test_image_id")
        self.assertIsNotNone(result)
        self.assertEqual(result, "https://test_bucket.cos.test_region.myqcloud.com/test_image_id")
    
    @patch('video_preview.CosS3Client.head_object')
    def test_get_image_preview_failure(self, mock_head_object):
        """测试get_image_preview在获取COS桶中的图片预览URL失败时返回None。"""
        mock_head_object.side_effect = Exception("Test exception")

        result = self.video_preview.get_image_preview("test_image_id")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()