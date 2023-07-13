import unittest
from unittest.mock import patch, MagicMock
from video_preview import VideoPreview

class TestVideoPreview(unittest.TestCase):
    def setUp(self):
        self.secret_id = 'your_secret_id'
        self.secret_key = 'your_secret_key'
        self.region = 'your_region'
        self.bucket = 'your_bucket'
        self.video_preview = VideoPreview(self.secret_id, self.secret_key, self.region, self.bucket)

    def test_set_image_preview_success(self):
        image_id = '1234'
        preview_url = 'https://example.com/img.png'
        image_data = b'image_data'

        # 模拟请求预览URL返回图片内容
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.content = image_data
            mock_get.return_value = mock_response

            # 模拟保存图片到COS桶成功
            with patch('qcloud_cos.CosS3Client.put_object') as mock_put_object:
                mock_response.raise_for_status.return_value = None

                # 调用set_image_preview方法
                result = self.video_preview.set_image_preview(image_id, preview_url)

                # 验证返回的图片地址是否符合预期
                expected_url = f"https://{self.bucket}.cos.{self.region}.myqcloud.com/{image_id}.png"
                self.assertEqual(result, expected_url)

    def test_set_image_preview_failure(self):
        image_id = '1234'
        preview_url = 'https://example.com/img.png'

        # 模拟请求预览URL失败
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception('Failed to get preview URL')

            # 调用set_image_preview方法
            result = self.video_preview.set_image_preview(image_id, preview_url)

            # 验证返回的图片地址是否为空字符串
            self.assertEqual(result, '')

    def test_get_image_preview_success(self):
        image_id = '1234'

        # 调用get_image_preview方法
        result = self.video_preview.get_image_preview(image_id)

        # 验证返回的图片地址是否符合预期
        expected_url = f"https://{self.bucket}.cos.{self.region}.myqcloud.com/{image_id}.png"
        self.assertEqual(result, expected_url)

    def test_get_image_preview_failure(self):
        image_id = '1234'

        # 调用get_image_preview方法时抛出异常
        with patch('qcloud_cos.CosS3Client.put_object') as mock_put_object:
            mock_put_object.side_effect = Exception('Failed to get image preview')

            # 调用get_image_preview方法
            result = self.video_preview.get_image_preview(image_id)

            # 验证返回的图片地址是否为空字符串
            self.assertEqual(result, '')

if __name__ == '__main__':
    unittest.main()
