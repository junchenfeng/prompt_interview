import requests
from typing import Optional
from qcloud_cos import CosConfig, CosS3Client
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VideoPreview:
    def __init__(self, cos_bucket: str, cos_region: str, cos_secret_id: str, cos_secret_key: str):
        """
        初始化VideoPreview类。

        :param cos_bucket: 腾讯云COS桶名称。
        :param cos_region: 腾讯云COS桶所在地区。
        :param cos_secret_id: 腾讯云COS密钥ID。
        :param cos_secret_key: 腾讯云COS密钥。
        """
        self.cos_bucket = cos_bucket
        self.cos_client = CosS3Client(CosConfig(Region=cos_region, SecretId=cos_secret_id, SecretKey=cos_secret_key))
    
    def set_image_preview(self, image_id: str, preview_url: str) -> Optional[str]:
        """
        从预览URL中获取图片，并将其保存到COS桶中。

        :param image_id: 图片ID。
        :param preview_url: 图片预览URL。
        :return: 存储在COS桶中的图片预览URL，如果保存失败则返回None。
        """
        try:
            response = requests.get(preview_url, stream=True)
            response.raise_for_status()

            self.cos_client.put_object(
                Bucket=self.cos_bucket,
                Body=response.raw,
                Key=image_id,
                ContentType='image/png'
            )
            logging.info(f"Image {image_id} saved to COS bucket")
            return f"https://{self.cos_bucket}.cos.{cos_region}.myqcloud.com/{image_id}"
        except Exception as e:
            logging.error(f"Error saving image {image_id} to COS bucket: {str(e)}")
            return None
    
    def get_image_preview(self, image_id: str) -> Optional[str]:
        """
        根据图片ID从COS桶中获取图片预览URL。

        :param image_id: 图片ID。
        :return: 存储在COS桶中的图片预览URL，如果获取失败则返回None。
        """
        try:
            self.cos_client.head_object(
                Bucket=self.cos_bucket,
                Key=image_id
            )
            return f"https://{self.cos_bucket}.cos.{cos_region}.myqcloud.com/{image_id}"
        except Exception as e:
            logging.error(f"Error getting image {image_id} from COS bucket: {str(e)}")
            return None