<h1> Sampletools</h1>
<h2>Personal sample tools</h2>

<h3>1.M3U8下载v1.0.0</h3>

依赖Python3.10，需要额外下载tqdm包

依赖ffmpeg进行hls的解码

使用时在脚本同文件夹下新建list.txt并将对应后缀为.m3u8或.mp4的url（如果输入的url没有后缀会默认为.mp4，可能会导致其他错误）

允许最大同时下载16个url（MAX_URLALLOW），最大并行100线程（PALLOW=Semaphore(100)），对于访问失败的url允许最大重新尝试10次（trytime）。下载过程中会生成对应url的临时文件夹，下载转MP4完成后会自动删除并保存在download.py所在目录下。

<b>免责：此工具仅提供从.m3u8文件或链接转码为MP4的功能，使用前请注意当地法律法规限制。</b>
### 2.划词翻译
基于百度翻译API和tkinter构建了简单的划词翻译程序
按住左键选中单词即可在悬浮的小窗中显示对应的中文翻译结果，按鼠标中键隐藏窗口，按鼠标X2键（在作者设备上为前进）退出应用。查询的翻译结果会添加到剪贴板中，使用时可直接粘贴。
之后可能会加入OCR功能处理某些无法复制的文本内容。
