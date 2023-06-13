import requests
import logging
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

# 配置日志记录
logging.basicConfig(filename='app.log', level=logging.INFO)


class VideoPreview:
    def __init__(self):
        self.video_url = None

    def set_image_preview(self) -> None:
        """
        从抖音千川素材库的API接口获取视频URL，并保存在self.video_url中
        """
        try:
            # 从抖音千川素材库的API接口获取视频URL
            response = requests.get('http://example.com/api/video')
            if response.status_code == 200:
                data = response.json()
                # 假设接口返回的数据中包含视频URL字段 'video_url'
                self.video_url = data['video_url']
            else:
                raise Exception('Failed to get video URL from API')
        except Exception as e:
            logging.error(f'Error in set_image_preview: {str(e)}')

    def get_image_preview(self) -> str:
        """
        当用户请求URL时返回COS存储地址，如果过期重新尝试存储；如果获取失败则报错。
        返回COS存储地址
        """
        if not self.video_url:
            self.set_image_preview()

        # 腾讯云存储桶的配置信息
        secret_id = 'your_secret_id'
        secret_key = 'your_secret_key'
        region = 'your_region'
        bucket = 'your_bucket_name'

        try:
            # 创建 CosConfig 对象
            cos_config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)

            # 创建 CosS3Client 对象
            cos_client = CosS3Client(cos_config)

            # 将视频文件保存到腾讯云存储桶
            # 假设保存到存储桶中的文件名为 'video.mp4'
            response = cos_client.put_object_from_url(
                Bucket=bucket,
                Key='video.mp4',
                EnableMD5=False,
                FetchUrl=self.video_url
            )

            if response['Response']['Error']['Code'] == 0:
                # 返回COS存储地址
                return f'COS存储地址: {response["Response"]["Location"]}'
            else:
                raise Exception('Failed to save video to COS')
        except Exception as e:
            logging.error(f'Error in get_image_preview: {str(e)}')
            raise
