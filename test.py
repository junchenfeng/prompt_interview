import unittest
from unittest.mock import MagicMock
from video_preview import VideoPreview

class TestVideoPreview(unittest.TestCase):
    def setUp(self):
        self.secret_id = 'your_secret_id'
        self.secret_key = 'your_secret_key'
        self.bucket = 'your_bucket_name'
        self.video_preview = VideoPreview(self.secret_id, self.secret_key, self.bucket)

    def test_set_image_preview_success(self):
        # 模拟腾讯云COS客户端的put_object方法返回成功的响应
        self.video_preview.cos_client.put_object = MagicMock(return_value={
            'Response': {
                'Error': {
                    'Code': 0
                }
            }
        })

        image_id = 'image123'
        preview_url = 'https://example.com/preview.jpg'
        self.video_preview.set_image_preview(image_id, preview_url)

        # 验证put_object方法是否被调用
        self.video_preview.cos_client.put_object.assert_called_once()

    def test_set_image_preview_error(self):
        # 模拟腾讯云COS客户端的put_object方法返回错误的响应
        self.video_preview.cos_client.put_object = MagicMock(return_value={
            'Response': {
                'Error': {
                    'Code': -1,
                    'Message': 'Internal Server Error'
                }
            }
        })

        image_id = 'image123'
        preview_url = 'https://example.com/preview.jpg'
        self.video_preview.set_image_preview(image_id, preview_url)

        # 验证put_object方法是否被调用
        self.video_preview.cos_client.put_object.assert_called_once()

    def test_get_image_preview_success(self):
        # 模拟腾讯云COS客户端的get_object方法返回成功的响应
        self.video_preview.cos_client.get_object = MagicMock(return_value={
            'Response': {
                'Error': {
                    'Code': 0
                }
            },
            'Body': MagicMock(get_raw_stream=MagicMock(return_value=MagicMock(url='https://example.com/preview.jpg')))
        })

        image_id = 'image123'
        preview_url = self.video_preview.get_image_preview(image_id)

        # 验证get_object方法是否被调用
        self.video_preview.cos_client.get_object.assert_called_once()
        # 验证返回的预览URL是否正确
        self.assertEqual(preview_url, 'https://example.com/preview.jpg')

    def test_get_image_preview_error(self):
        # 模拟腾讯云COS客户端的get_object方法返回错误的响应
        self.video_preview.cos_client.get_object = MagicMock(return_value={
            'Response': {
                'Error': {
                    'Code': -1,
                    'Message': 'Internal Server Error'
                }
            }
        })

        image_id = 'image123'
        preview_url = self.video_preview.get_image_preview(image_id)

        # 验证get_object方法是否被调用
        self.video_preview.cos_client.get_object.assert_called_once()
        # 验证返回的预览URL是否为None
        self.assertIsNone(preview_url)

if __name__ == '__main__':
    unittest.main()
