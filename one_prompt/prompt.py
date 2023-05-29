import logging
import requests
from typing import Optional
from qcloud_cos import CosConfig, CosS3Client


class VideoPreview:
    def __init__(self):
        self.config = None
        self.client = None

    def set_image_preview(
        self,
        secret_id: str,
        secret_key: str,
        region: str = 'ap-beijing',
        token: Optional[str] = '123',
        scheme: Optional[str] = 'https',
        url: Optional[str] = None,
        Key: Optional[str] = None
    ):
        try:
            self.config = CosConfig(
                Secret_id=secret_id,
                Secret_key=secret_key,
                Region=region,
                Token=token,
                Scheme=scheme
            )
            self.client = CosS3Client(self.config)
            response = self.client.create_bucket(Bucket='bucket-1250000000')
            stream = requests.get(url)
            response = self.client.put_object(
                Bucket='bucket-1250000000',
                Body=stream,
                Key=Key
            )
            logging.info(f"Image preview saved successfully: {response}")
        except Exception as e:
            logging.error(f"Failed to set image preview: {e}")

    def get_image_preview(
        self,
        ACCESS_TOKEN: str,
        advertiser_id: int,
        image_mode: str = 'VIDEO_VERTICAL',
        tags: str = '搞笑',
        sources: str = 'BP'
    ) -> Optional[str]:
        try:
            PATH = '/open_api/2/file/video/get/'
            netloc = 'ad.oceanengine.com'
            url = f"https://{netloc}{PATH}"
            headers = {'ACCESS_TOKEN': ACCESS_TOKEN}
            data = {
                'advertiser_id': advertiser_id,
                'image_mode': image_mode,
                'tags': tags,
                'sources': sources
            }
            response = requests.get(url, headers=headers, json=data)
            json_data = response.json()
            poster_url = json_data.get('poster_url')
            logging.info(f"Retrieved image preview URL: {poster_url}")
            return poster_url
        except Exception as e:
            logging.error(f"Failed to get image preview: {e}")
            return None


def main():
    logging.basicConfig(level=logging.INFO)
    video_preview = VideoPreview()

    # Step 1: Get image preview URL
    ACCESS_TOKEN = 'your_access_token'
    advertiser_id = 123456789
    poster_url = video_preview.get_image_preview(ACCESS_TOKEN, advertiser_id)

    if poster_url:
        # Step 2: Set image preview in COS
        secret_id = 'your_secret_id'
        secret_key = 'your_secret_key'
        video_preview.set_image_preview(
            secret_id=secret_id,
            secret_key=secret_key,
            url=poster_url,
            Key='preview_image.jpg'
        )


if __name__ == '__main__':
    main()
