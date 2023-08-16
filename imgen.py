# encoding:utf-8

import plugins
import requests
import json
import openai
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel.chat_message import ChatMessage
from common.log import logger
from plugins import *

@plugins.register(
    name="imgen",
    desire_priority=99,
    desc="A simple image generation plugin",
    version="0.1",
    author="befantasy",
)
class imgen(Plugin):
    def __init__(self):
        super().__init__()
        try:
            conf = super().load_config()
            if not conf:
                raise Exception("config.json not found")
            self.authkey = conf["authkey"]
            self.trigger = conf["trigger"]
            self.model = conf["model"]
            self.n = conf["n"]

            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
            logger.info("[imgen] inited")
        except Exception as e:
            logger.warn("[imgen] init failed, ignore ")
            raise e
            
    def on_handle_context(self, e_context: EventContext):
        content = e_context["context"].content
        logger.debug("[imgen] on_handle_context. content: %s" % content)
        if content.startswith(self.trigger + ' '):
            drawprompt = content.split(' ', 1)[1]  # 提取绘图提示词
            #logger.info(f"[imgen]{content}")
            logger.info(f"[imgen]原始提示词: {drawprompt}")  # 记录原始提示词
            # 使用 OpenAI GPT API 进行翻译和优化
            translation = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Translate: {drawprompt}",
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.7,
            )
            
            translated_prompt = translation.choices[0].text.strip()  # 获取翻译后的提示词
            logger.info(f"[imgen]转译提示词: {translated_prompt}")  # 记录翻译优化后的提示词
           
            # 构建绘图请求的数据
            data = {
                "model": self.model,
                "prompt": translated_prompt,
                "size": "1024x1024",
                "n": self.n,
                "response_format": "url"
            }
            
            headers = {
                "Authorization": f"Bearer {self.authkey}"   # chimeragpt身份验证令牌
            }
            
            response = requests.post("https://chimeragpt.adventblocks.cc/api/v1/images/generations", json=data, headers=headers)  # 发送绘图请求
            if response.status_code == 200:
                drawprompt_url = response.json()["data"][0]["url"]  # 从响应中获取图片的 URL
                
                reply = Reply()
                reply.type = ReplyType.IMAGE_URL
                reply.content = drawprompt_url
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS  # 事件结束，进入默认处理逻辑

            else:
                logger.error("[imgen]绘图接口繁忙，请稍后再试。")
                reply = Reply()
                reply.type = ReplyType.TEXT
                reply.content = "[ERROR]绘图接口繁忙，请稍后再试。"
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS  # 事件结束，进入默认处理逻辑，一般会覆写reply

    def get_help_text(self, verbose=False, **kwargs):
        help_text = "根据提示词生成图片。使用Chimera API。"
        if not verbose:
            return help_text
        help_text = f"根据提示词生成图片\n使用方式：{self.trigger} 提示词\n---------------------------\n当前模型：{self.model}\n可用模型：kandinsky-2.2, kandinsky-2, sdxl, stable-diffusion-2.1, stable-diffusion-1.5, deepfloyd-if, material-diffusion"
        return help_text
