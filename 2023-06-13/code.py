import logging
import requests
import datetime

from typing import Optional
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


class VideoPreview:
    def __init__(self, cos_secret_id: str, cos_secret_key: str, cos_bucket: str, cos_region: str):
        self.cos_secret_id = cos_secret_id
        self.cos_secret_key = cos_secret_key
        self.cos_bucket = cos_bucket
        self.cos_region = cos_region
        self.cos_client = self.create_cos_client()

    def create_cos_client(self) -> CosS3Client:
        config = CosConfig(Region=self.cos_region, SecretId=self.cos_secret_id, SecretKey=self.cos_secret_key)
        return CosS3Client(config)

    def fetch_preview_url(self) -> Optional[str]:
        try:
            # Make API request to fetch the video preview URL
            response = requests.get("https://api.example.com/preview-url")
            if response.status_code == 200:
                return response.json().get("url")
        except Exception as e:
            logging.error(f"Failed to fetch preview URL: {e}")
        return None

    def save_image_to_cos(self, url: str) -> Optional[str]:
        try:
            # Download the image from the URL
            response = requests.get(url)
            if response.status_code == 200:
                # Generate a unique filename based on current timestamp
                current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"preview_{current_time}.jpg"
                # Upload the image to COS
                response = self.cos_client.put_object(
                    Bucket=self.cos_bucket,
                    Body=response.content,
                    Key=filename,
                    ContentType="image/jpeg"
                )
                if response["Response"]["Error"]["Code"] == "":
                    # Set the expiration time for the image to 180 days
                    expiration_time = datetime.datetime.now() + datetime.timedelta(days=180)
                    self.cos_client.put_bucket_lifecycle_configuration(
                        Bucket=self.cos_bucket,
                        LifecycleConfiguration={
                            "Rules": [
                                {
                                    "ID": "image_expiration",
                                    "Status": "Enabled",
                                    "Expiration": {"Days": 180}
                                }
                            ]
                        }
                    )
                    return filename
        except Exception as e:
            logging.error(f"Failed to save image to COS: {e}")
        return None

    def set_image_preview(self) -> Optional[str]:
        preview_url = self.fetch_preview_url()
        if preview_url:
            return self.save_image_to_cos(preview_url)
        return None

    def get_image_preview(self, filename: str) -> Optional[str]:
        try:
            # Check if the image exists in COS and return its URL
            response = self.cos_client.head_object(Bucket=self.cos_bucket, Key=filename)
            if response["Response"]["Error"]["Code"] == "":
                return f"https://{self.cos_bucket}.cos.{self.cos_region}.myqcloud.com/{filename}"
        except Exception as e:
            logging.error(f"Failed to get image preview: {e}")
        return None
