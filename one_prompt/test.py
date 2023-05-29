import unittest
from unittest.mock import patch
from prompt import VideoPreview


class TestVideoPreview(unittest.TestCase):
    @patch('requests.get')
    @patch('qcloud_cos.CosS3Client.create_bucket')
    @patch('qcloud_cos.CosS3Client.put_object')
    def test_set_image_preview_success(
        self,
        mock_put_object,
        mock_create_bucket,
        mock_requests_get
    ):
        video_preview = VideoPreview()
        secret_id = 'mock_secret_id'
        secret_key = 'mock_secret_key'
        url = 'mock_image_url'
        Key = 'mock_key'

        # Mock the return values
        mock_requests_get.return_value.status_code = 200
        mock_create_bucket.return_value = 'bucket_created'
        mock_put_object.return_value = 'object_created'

        video_preview.set_image_preview(secret_id, secret_key, url=url, Key=Key)

        # Check if the methods are called with the correct arguments
        mock_create_bucket.assert_called_with(Bucket='bucket-1250000000')
        mock_put_object.assert_called_with(
            Bucket='bucket-1250000000',
            Body=mock_requests_get.return_value,
            Key=Key
        )

    @patch('requests.get')
    def test_get_image_preview_success(self, mock_requests_get):
        video_preview = VideoPreview()
        ACCESS_TOKEN = 'mock_access_token'
        advertiser_id = 123
        expected_url = 'mock_poster_url'
        expected_json_response = {'poster_url': expected_url}

        # Mock the return values
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = expected_json_response

        poster_url = video_preview.get_image_preview(ACCESS_TOKEN, advertiser_id)

        # Check if the method returns the expected URL
        self.assertEqual(poster_url, expected_url)

    @patch('requests.get')
    def test_get_image_preview_failure(self, mock_requests_get):
        video_preview = VideoPreview()
        ACCESS_TOKEN = 'mock_access_token'
        advertiser_id = 123

        # Mock the return values
        mock_requests_get.return_value.status_code = 500

        poster_url = video_preview.get_image_preview(ACCESS_TOKEN, advertiser_id)

        # Check if the method returns None on failure
        self.assertIsNone(poster_url)


if __name__ == '__main__':
    unittest.main()
