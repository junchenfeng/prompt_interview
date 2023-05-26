# 考核目标
你的提示词工程水平是否支持写一个200行复杂度左右的代码

不论你最后是否被录取，希望这次提示词面试都能帮助你更好地理解GPT的能力

# 业务逻辑
- 从一个网络接口（例如抖音千川的素材API）中拿到一张视频的preview url
- 将图片保存在腾讯云存储桶（COS）中，过期时间为180天
- 当用户请求preview url时返回cos存储地址，如果过期重新尝试存储；如果获取失败报错

# 代码要求
- 创建一个VideoPreview的类，暴露set_image_preview/get_image_preview两个公共方法
- 必须包含必要的try catch和logging
- 尽可能符合clean code的代码风格要求：你需要学会让GPT重构
- 不限制代码语言，最好是Python。如果是Python，请使用Python3语法并增加type hint
- *可选* 在test.py里创建一个Unittest，对prompt.py的代码覆盖率越高越好

# 限制
- 使用GPT-3.5 turbo可以稳定直接生成无错误代码，但是不要求一次输出完成，允许使用多个response拼接
- 提示词在1000字以内，且必须是中文
- 提示词里直接写代码是允许的，但是越少越好

# 上交格式
- 一个prompt.txt，一个code.xyz，可以有一个test.xyz。
- 通过Pull Request提交

