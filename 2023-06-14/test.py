import unittest
from unittest.mock import MagicMock, patch
from code import VideoPreview


class VideoPreviewTestCase(unittest.TestCase):
    def setUp(self):
        self.cos_client_mock = MagicMock()
        self.material_api_url = "https://example.com/materials"
        self.video_preview = VideoPreview(self.cos_client_mock, self.material_api_url)

    def test_set_image_preview_success(self):
        image_id = "123"
        preview_url = "https://example.com/preview.jpg"
        cos_url = "cos://bucket/image.jpg"
        self.video_preview._get_preview_url = MagicMock(return_value=preview_url)
        self.video_preview._save_to_cos = MagicMock(return_value=cos_url)

        result = self.video_preview.set_image_preview(image_id)

        self.assertEqual(result, cos_url)
        self.video_preview._get_preview_url.assert_called_once_with(image_id)
        self.video_preview._save_to_cos.assert_called_once_with(preview_url)

    def test_set_image_preview_error(self):
        image_id = "123"
        self.video_preview._get_preview_url = MagicMock(side_effect=ValueError("Invalid image ID"))

        with self.assertRaises(ValueError):
            self.video_preview.set_image_preview(image_id)

        self.video_preview._get_preview_url.assert_called_once_with(image_id)

    def test_get_image_preview_success(self):
        image_id = "123"
        cos_url = "cos://bucket/image.jpg"
        self.video_preview._get_cos_url = MagicMock(return_value=cos_url)

        result = self.video_preview.get_image_preview(image_id)

        self.assertEqual(result, cos_url)
        self.video_preview._get_cos_url.assert_called_once_with(image_id)

    def test_get_image_preview_invalid_id(self):
        image_id = "123"
        self.cos_client_mock.get_cos_url.side_effect = qcloud_cos.CosServiceError("NoSuchKey")

        with self.assertRaises(ValueError):
            self.video_preview.get_image_preview(image_id)

        self.video_preview._get_cos_url.assert_called_once_with(image_id)

    def test_get_image_preview_error(self):
        image_id = "123"
        self.cos_client_mock.get_cos_url.side_effect = qcloud_cos.CosServiceError("UnknownError")

        with self.assertRaises(qcloud_cos.CosServiceError):
            self.video_preview.get_image_preview(image_id)

        self.video_preview._get_cos_url.assert_called_once_with(image_id)


if __name__ == '__main__':
    unittest.main()
