import unittest
from code import VideoPreview


class VideoPreviewTestCase(unittest.TestCase):
    def setUp(self):
        self.cos_secret_id = "YOUR_COS_SECRET_ID"
        self.cos_secret_key = "YOUR_COS_SECRET_KEY"
        self.cos_bucket = "YOUR_COS_BUCKET"
        self.cos_region = "YOUR_COS_REGION"
        self.video_preview = VideoPreview(self.cos_secret_id, self.cos_secret_key, self.cos_bucket, self.cos_region)

    def test_set_image_preview(self):
        filename = self.video_preview.set_image_preview()
        self.assertIsNotNone(filename)

    def test_get_image_preview(self):
        filename = self.video_preview.set_image_preview()
        self.assertIsNotNone(filename)

        image_url = self.video_preview.get_image_preview(filename)
        self.assertIsNotNone(image_url)
        self.assertTrue(image_url.startswith(f"https://{self.cos_bucket}.cos.{self.cos_region}.myqcloud.com/"))


if __name__ == "__main__":
    unittest.main()
