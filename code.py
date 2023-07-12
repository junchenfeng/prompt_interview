import os
import logging
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

class VideoPreview:
    def __init__(self, secret_id, secret_key, bucket):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.bucket = bucket

        # 配置腾讯云COS
        region = 'ap-guangzhou'  # 根据你的实际情况进行修改
        config = CosConfig(Region=region, SecretId=self.secret_id, SecretKey=self.secret_key)
        self.cos_client = CosS3Client(config)

        # 配置日志记录
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def set_image_preview(self, image_id, preview_url):
        try:
            # 将预览URL存储到腾讯云COS桶中
            object_key = f"{image_id}.jpg"  # 假设以图片ID作为对象键
            response = self.cos_client.put_object(
                Bucket=self.bucket,
                Body=preview_url,
                Key=object_key
            )
            if response['Response']['Error']['Code'] == 0:
                logging.info(f"预览URL已成功存储到腾讯云COS桶中：{object_key}")
            else:
                logging.error(f"存储预览URL到腾讯云COS桶中时出错：{response['Response']['Error']['Message']}")
        except Exception as e:
            logging.error(f"存储预览URL到腾讯云COS桶中时出现异常：{str(e)}")

    def get_image_preview(self, image_id):
        try:
            # 从腾讯云COS桶中获取与图片ID对应的预览URL
            object_key = f"{image_id}.jpg"  # 假设以图片ID作为对象键
            response = self.cos_client.get_object(
                Bucket=self.bucket,
                Key=object_key
            )
            if response['Response']['Error']['Code'] == 0:
                preview_url = response['Body'].get_raw_stream().url
                return preview_url
            else:
                logging.error(f"从腾讯云COS桶中获取预览URL时出错：{response['Response']['Error']['Message']}")
                return None
        except Exception as e:
            logging.error(f"从腾讯云COS桶中获取预览URL时出现异常：{str(e)}")
            return None
