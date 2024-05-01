import re

text = """
首页 注册 登录
V2EX = way to explore
V2EX 是一个关于分享和探索的地方
现在注册
已注册用户请  登录
TradingView
广告
万维广告联盟
🎁高性能云服务器ECS 99元/年起，省钱上云就现在！
广告
iX8NEGGnV2EX  ›  分享发现
感谢巨硬， Phi-3 Mini 让我八年前的破笔记本也能玩本地大模型翻译了
     iX8NEGGn · 5 天前 · 1944 次点击
用 Ollama 跑了下 4B 量化版本，翻译效果已经差不多追上谷歌机翻了，终于可以实现文档翻译自由了。
13 条回复  •  2024-04-26 16:43:52 +08:00
iX8NEGGn            1
iX8NEGGn   
OP
   5 天前   ❤️ 2
打脸了，试着翻译了几篇 PDF ，中文不太行，有的地方还多嘴，甚至有乱码。
lovestudykid            2
lovestudykid      5 天前
听说过拟合比较严重，刷榜的产物
passive         3
passive      5 天前 via Android
估计训练的人叫 Bob ，因为总会出来 Bob：提示符
iX8NEGGn            4
iX8NEGGn   
OP
   5 天前 via iPhone
@passive @lovestudykid 看到介绍说 Mini 就能媲美 Chat-GPT3.5 ，把我给激动的，14B 不得起飞噜，诶，又被骗了。
Chad0000            5
Chad0000      5 天前 via iPhone
这种新闻都是说打脸 GPT ，最终也不知道打的是谁的脸。

我铁打的 ChatGPT Plus 一直开着就挺好的
qilme           6
qilme      5 天前 via Android
论文里说了两个主要缺点，一个是只支持英文，一个是知识库偏少
haiku           7
haiku      5 天前 via Android
还是 llama8b 吧
june4           8
june4      5 天前
内存不差的话，感觉 4b 还是比 8b 之类的差不少，反正性能一样
fredweili           9
fredweili      5 天前
翻译还是得 gpt ，llama3 也不行
weilongs            10
weilongs      5 天前
op 用什么工具翻译的？ 沉浸翻译接入的 ollama 嘛？
iX8NEGGn            11
iX8NEGGn   
OP
   5 天前
@weilongs 不是，用的 memoQ ，加上自己写翻译插件（ https://v2ex.com/t/981110 ），昨晚快速对接了下 Ollama 的 API ，还没 push ，没有译后编辑需求的话，沉浸式翻译等浏览器插件更方便吧，拖入浏览器就行。
weilongs            12
weilongs      5 天前
@iX8NEGGn 哦 我尝试了沉浸式翻译，进行处理还可以。Phi 感觉不太行，我更喜欢微软另一个小模型：wizardlm2:7b
SuperMaxine         13
SuperMaxine      4 天前
目前用来翻译的本地能跑的大模型我就感觉 qwen-14b 还不错，参数量小的基本都没法看，国外的大模型比如 mixtral 、llama3-8b 之类的经常会中英混杂，翻译结果里夹生漏个一两部分不翻译。用来做中英互译任务还是得国内这些由足够中文预料进行训练的。不过就这感觉也打不过在线模型比如 kimi 之类的，和 gpt-3.5 的翻译比稍微差一点点，更打不过 gpt4 了，只能说勉强能用，通顺程度上还是不行。
万维广告联盟
🎁高性能云服务器ECS 99元/年起，省钱上云就现在！
广告
关于   ·   帮助文档   ·   博客   ·   API   ·   FAQ   ·   我们的愿景   ·   实用小工具   ·   2622 人在线   最高记录 6543   ·      Select Language
创意工作者们的社区
World is powered by solitude
VERSION: 3.9.8.5 · 23ms · UTC 13:36 · PVG 21:36 · LAX 06:36 · JFK 09:36
Developed with CodeLauncher
♥ Do have faith in what you're doing.
"""

# 使用正则表达式匹配用户评论
# 匹配模式：用户名 + 时间信息 + 评论内容
# 假设用户名由字母和数字组成，可能包含一些特殊字符，如下划线或连字符
comments = re.findall(r'(\w+|\w+[\w\s]*\w+)\s*\d+ 天前.*?(?=\n\w+|$)', text)

# 打印提取的评论
for comment in comments:
    print(comment)
