# 考核目标
你的提示词工程水平是否支持写一个200行复杂度左右的代码

不论你最后是否被录取，希望这次提示词面试都能帮助你更好地理解GPT的能力

# 业务需求
- 你有一个图片id（假设1234）和其preview url（假设https://example.com/img.png）。这个preview url有1小时的过期时间，影响了你在前端调用和展示
- 你的技术方案是将这个id对应的preview url存到腾讯云的COS桶中，当用户以image id请求preview url时返回cos存储地址用于前端展示

# 代码要求
- 创建一个VideoPreview的类，暴露set_image_preview/get_image_preview两个公共方法
- 必须包含必要的try catch和logging
- 不限制代码语言，最好是Python。如果是Python，请使用Python3语法并增加type hint
- *可选* 在test.py里创建一个Unittest，对prompt.py的代码覆盖率越高越好

# 限制
- 使用GPT-3.5 turbo可以稳定直接生成代码，但是不要求一次输出完成，允许使用多个response拼接。
 + 我应该能够用chatgpt default 3.5复现你的结果
 + 你的代码必须在逻辑上能够实现业务需求
- 提示词在1000字以内，且必须是中文
- 提示词里直接写代码是允许的，但是越少越好

# HINT
- 通过将业务需求“翻译”（拆解）为技术实现步骤，可以实现较为精准的代码控制
- *可选* 作为一个优秀的程序员，需要考虑各种异常处理的细节。这会挑战你通过prompt控制输出的能力 


# 上交格式
- 一个prompt.txt，一个code.xyz，可以有一个test.xyz。
- 通过Github的Pull Request提交

