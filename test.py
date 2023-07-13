import unittest
from unittest.mock import MagicMock

from video_preview import VideoPreview

class TestVideoPreview(unittest.TestCase):
    def setUp(self):
        # 创建VideoPreview类的实例
        self.video_preview = VideoPreview()

        # 模拟腾讯云COS桶的客户端
        self.video_preview.cos_client = MagicMock()

    def test_set_image_preview_success(self):
        # 模拟腾讯云COS桶的上传方法返回成功
        self.video_preview.cos_client.upload.return_value = True

        image_id = "1234"
        preview_url = "https://example.com/img.png"

        # 调用set_image_preview方法
        self.video_preview.set_image_preview(image_id, preview_url)

        # 断言日志是否记录了正确的信息
        self.assertIn(f"Image preview for ID {image_id} has been set.", self._caplog.text)

    def test_set_image_preview_failure(self):
        # 模拟腾讯云COS桶的上传方法抛出异常
        self.video_preview.cos_client.upload.side_effect = Exception("Upload failed")

        image_id = "1234"
        preview_url = "https://example.com/img.png"

        # 调用set_image_preview方法
        self.video_preview.set_image_preview(image_id, preview_url)

        # 断言日志是否记录了正确的错误信息
        self.assertIn(f"Failed to set image preview for ID {image_id}: Upload failed", self._caplog.text)

    def test_get_image_preview_success(self):
        # 模拟腾讯云COS桶的获取URL方法返回有效URL
        self.video_preview.cos_client.get_url.return_value = "https://example.com/img.png"

        image_id = "1234"

        # 调用get_image_preview方法
        preview_url = self.video_preview.get_image_preview(image_id)

        # 断言获取到了预览URL
        self.assertEqual(preview_url, "https://example.com/img.png")

    def test_get_image_preview_failure(self):
        # 模拟腾讯云COS桶的获取URL方法抛出异常
        self.video_preview.cos_client.get_url.side_effect = Exception("URL retrieval failed")

        image_id = "1234"

        # 调用get_image_preview方法
        preview_url = self.video_preview.get_image_preview(image_id)

        # 断言获取预览URL失败，返回None，并且日志中记录了正确的错误信息
        self.assertIsNone(preview_url)
        self.assertIn(f"Failed to get image preview for ID {image_id}: URL retrieval failed", self._caplog.text)

if __name__ == "__main__":
    unittest.main()
