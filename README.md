<h1> Sampletools</h1>
<h2>Personal sample tools</h2>

<h3>1.M3U8下载v1.0.0</h3>

依赖Python3.10，需要额外下载tqdm包

依赖ffmpeg进行hls的解码

使用时在脚本同文件夹下新建list.txt并将对应后缀为.m3u8或.mp4的url（如果输入的url没有后缀会默认为.mp4，可能会导致其他错误）

允许最大同时下载16个url（MAX_URLALLOW），最大并行100线程（PALLOW=Semaphore(100)），对于访问失败的url允许最大重新尝试10次（trytime）。下载过程中会生成对应url的临时文件夹，下载转MP4完成后会自动删除并保存在download.py所在目录下。

<b>免责：此工具仅提供从.m3u8文件或链接转码为MP4的功能，使用前请注意当地法律法规限制。</b>
