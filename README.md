<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot_plugin_h2e

_✨ NoneBot how2exercise ——Bot已经帮我们解决了吃什么 能不能解决我们练什么呢  ✨_

<a href="https://pypi.python.org/pypi/nonebot-plugin-note">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-note.svg" alt="pypi">
</a>

</div>


# 安装

* pip 
```
pip install nonebot-plugin-h2e
```

* nb_cli
```
nb plugin install nonebot-plugin-h2e
```

# 配置.env

```
# None
```



# 使用
```
nonebot.load_plugin('nonebot_plugin_h2e')
```


# 命令
**注：使用命令时需要加命令前缀**

* ```
  1. 合并转发形式：私聊/群聊 （可提供随机<数量>的运动方法和模糊匹配）
   
     /fitness <锻炼方式> <目标肌群> <[来<数量>种]|[<运动方法>|<关键字>]> 
     /swim    <锻炼方式> <目标肌群> <[来<数量>种]|[<运动方法>|<关键字>]> 
     /yoga    <锻炼方式> <目标肌群> <[来<数量>种]|[<运动方法>|<关键字>]> 
   
  2. 长文刷屏形式：私聊/群聊 （可提供随机<数量>的运动方法和精确匹配） 
   
     /fitnessL <锻炼方式> <目标肌群> <[来<数量>种]|[<运动方法>]> 
     /swimL    <锻炼方式> <目标肌群> <[来<数量>种]|[<运动方法>]> 
     /yogaL    <锻炼方式> <目标肌群> <[来<数量>种]|[<运动方法>]> 
   
  以上命令格式中，以< >包裹的表示一个参数，以[ ]包裹的表示一个可选项。 
   
   锻炼方式 = [有器械] | [无器械] | [无支持] 
   目标肌群 = [全身] | [背部] | [腿部] | [肩部] | [腹部] | [腰部] 
   详细说明：参见姜Bot的大脑 
  ```

  


# 其他

有bug有什么想法都可以告诉我，可先用e-mail联系：wulun0102@outlook.com



- 本项目前期与ChatGPT深度合作，是以建立一个有趣的游泳数据库为出发点，但是发现我以一人之力无法完成这庞大的设想（作者为国家一级运动员）；
- 本项目致力于高度压榨ChatGPT生成 json 文件：
  - 内容有可能不完全真实；
    - 所需的 `.json` 文件如下格式；

- ```json
    {
      "name": "俯卧撑",
      "description": "俯卧撑可以锻炼胸肌、肩膀和三头肌。需要开始时做一个高板姿势，然后弯曲肘部将身体降低，直到胸部接近地面。",
      "image": "https://example.com/pushup.jpg",
      "steps": [
        "做一个高板姿势，手掌与肩部宽度相等，双脚并拢。",
        "屈肘将身体降低，直到胸部接近地面。",
        "保持短暂的停顿，然后推回起始位置。",
        "重复以上动作。"
      ]
    }
  ```

- 在后期加入游泳动作和瑜伽动作的时候有可能逻辑会有变化，但是问题不大。

- 希望有兴趣的朋友们可以加入这个项目！！！



# 🐦 TODO list

- [ ] 完善 `/fitness 条目下 有器械、无支撑  ` 相关条目；
- [ ] 起步 `/swim 条目下 无器械、有器械、无支持` 相关条目；
- [ ] 起步 `/yoga 条目下 无器械、有器械、无支持` 相关条目；
- [ ] 等待大家的反馈；
- [ ] 增加用户组的锻炼数据存储；
- [ ] 增加用户组的锻炼计划定制；（现在只是方法，没有成为训练序列）
- [ ] 代码结构重组



## 特别鸣谢：

- 雀魂信息查询插件：https://github.com/ssttkkl/nonebot-plugin-majsoul