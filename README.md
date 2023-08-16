# chatgpt-on-wechat-imgen

chatgpt-on-wechat的绘图插件。使用Chimera API，需加入ChimeraGPT的discord频道获取API key。

# 安装：
## 通过godcmd
> #auth password			

> #installp https://github.com/befantasy/imgen.git     

> #scanp      
  
#	配置：
## 申请API KEY:
https://chimeragpt.adventblocks.cc/zh

## 修改config.json
将插件目录下的config.json.template改名为config.json
```
{
  "authkey": "",	\\API KEY
  "trigger": "制图", 	\\触发词
  "model": "kandinsky-2.2", 	\\模型
  "model list": "kandinsky-2.2, sdxl, stable-diffusion-2.1, stable-diffusion-1.5, deepfloyd-if, material-diffusion, midjourney",		\\可用模型，不需修改，仅供上一行设置参考
  "n": "1"		\\暂时不要修改
}

```

重新载入配置文件，私聊向机器人发送：#reloadp imgen
