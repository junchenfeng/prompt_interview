import unittest
 from prompt import VideoPreview
 
 class TestVideoPreview(unittest.TestCase):
     def setUp(self):
         self.preview = VideoPreview(
             secret_id='xxx',
             secret_key='xxx', 
             region='ap-guangzhou'
         )
         
     def test_set_image_preview_success(self):
         """set_image_preview成功测试""" 
         url = 'https://example.com/image.jpg'
         result = self.preview.set_image_preview(url)
         self.assertEqual(result, None)
         
     def test_set_image_preview_fail(self):
         """set_image_preview失败测试"""    
         url = 'invalidurl'
         with self.assertRaises(Exception):
             self.preview.set_image_preview(url) 
             
     def test_get_image_preview_success(self):
         """get_image_preview成功测试"""
         url = self.preview.get_image_preview()
         self.assertTrue(url.startswith('https://bucket-1250000000.cos.ap-guangzhou.myqcloud.com'))
 
     def test_get_image_preview_fail(self):
         """get_image_preview失败测试"""    
         with self.assertRaises(Exception):
             url = self.preview.get_image_preview()
             
 if __name__ == '__main__': 
     unittest.main()