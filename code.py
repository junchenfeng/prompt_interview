import logging
import requests
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

class VideoPreview:
    def __init__(self, secret_id: str, secret_key: str, region: str, bucket: str):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.region = region
        self.bucket = bucket

        # 配置日志
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)

        # 配置腾讯云存储桶
        config = CosConfig(Region=self.region, SecretId=self.secret_id, SecretKey=self.secret_key)
        self.cos_client = CosS3Client(config)

    def set_image_preview(self, image_id: str, preview_url: str) -> str:
        try:
            # 从预览URL获取图片内容
            response = requests.get(preview_url)
            response.raise_for_status()
            image_data = response.content

            # 保存图片到腾讯云存储桶
            object_key = f"{image_id}.png"
            response = self.cos_client.put_object(
                Bucket=self.bucket,
                Body=image_data,
                Key=object_key,
                ContentType='image/png'
            )
            response.raise_for_status()

            # 返回保存在COS桶中的图片地址
            return f"https://{self.bucket}.cos.{self.region}.myqcloud.com/{object_key}"
        except Exception as e:
            logging.error(f"Failed to set image preview for image_id {image_id}: {str(e)}")
            return ""

    def get_image_preview(self, image_id: str) -> str:
        try:
            # 返回保存在COS桶中的图片地址
            object_key = f"{image_id}.png"
            return f"https://{self.bucket}.cos.{self.region}.myqcloud.com/{object_key}"
        except Exception as e:
            logging.error(f"Failed to get image preview for image_id {image_id}: {str(e)}")
            return ""
