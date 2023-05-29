import requests
 from qcloud_cos import CosConfig
 from qcloud_cos import CosS3Client 
 import logging
 
 logger = logging.getLogger(__name__)
 
 class VideoPreview:
     """视频预览图处理"""
     def __init__(self, secret_id, secret_key, region) -> None:
         """初始化参数"""
         self.secret_id = secret_id   
         self.secret_key = secret_key    
         self.region = region 
 
     def _init_cos_client(self):
         """初始化COS客户端"""
         config = CosConfig(Region=self.region, SecretId=self.secret_id, SecretKey=self.secret_key)  
         return CosS3Client(config)
 
     def set_image_preview(self, url):
         """获取最新视频预览图并上传至COS"""
         try:     
             client = self._init_cos_client()  
             # 创建存储桶
             client.create_bucket(Bucket='bucket-1250000000')  
             # 请求获取预览图流
             stream = requests.get(url)       
             # 上传预览图至COS
             client.put_object(Bucket='bucket-1250000000', Body=stream, Key='preview.jpg') 
             # 设置对象生命周期为180天
             client.put_bucket_lifecycle(Bucket='bucket-1250000000',  
                                     LifecycleConfiguration={'Rule': ['Expiration': {'Days': 180}]})
         except Exception as err:
             logger.error(f'COS error: {err}')
             
     def get_image_preview(self):
         """获取最新视频预览图URL"""
         try:
             client = self._init_cos_client()               
             # 获取存储桶中所有预览图对象
             files = client.list_objects(Bucket='bucket-1250000000', Prefix='preview_')['Contents']  
             for file in files: 
              # 检查对象最后修改时间是否在180天内 
              if datetime.now() < datetime.fromisoformat(file['LastModified']) + timedelta(days=180):
                 return client.get_presigned_url(Bucket='bucket-1250000000', Key=file['Key']) 
             # 未找到未过期预览图,调用set_image_preview方法获取最新预览图
             return self.set_image_preview()           
         except Exception as err:
             logger.error(f'COS error: {err}') 