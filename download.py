import glob
import http
import http.client
import os
import re
import time
from queue import Queue
import urllib
import urllib.request
from multiprocessing import Process,Pool
from threading import Thread,Semaphore
from tqdm import tqdm, trange


def backpack(func):
    
    def backThread(*args):
        global PALLOW
        global ThreadList
        with PALLOW:
            t = Thread(target=func,args=args)
            ThreadList.append(t)
            t.daemon=True
            t.start()
    return backThread

@backpack
def urldown(url):
    global trytime
    if trytime>=0:
        state = 0
        filename=url.split("/")[-1]
        file=open(filename,"wb")
        try:
            handle=urllib.request.urlopen(url,timeout=200)
            file.write(handle.read())
        except urllib.error.HTTPError as e:
            state = e.code
        except http.client.IncompleteRead as e:
            file.write(e.partial.decode("utf-8"))
        except http.client.RemoteDisconnected:
            trytime-=1
            return urldown(url)
        except TimeoutError:
            time.sleep(10)
            trytime-=1
            return urldown(url)
        except urllib.error.URLError:
            time.sleep(10)
            trytime-=1
            return urldown(url)
        finally:
            file.close()
            trytime=10
            return state
    else:
        trytime=10
        print("%s max try times."%url)
        time.sleep(20)
        return urldown(url)
    
class M3U8_object:
    def __init__(self,link,path):
        if not os.path.isdir(path):
            os.mkdir(path)
        os.chdir(path)
        self.link=link
        self.urls=[]
        self.Key=None
        try:
            self.decode()
        except:
            errorfile=open("error.txt","a")
            errorfile.write(link+"\n")
            errorfile.close()
            
    def decode(self):
        m3u8name=self.link.split("/")[-1]
        mu=open(m3u8name,"w")
        m3u8=bytes.decode(urllib.request.urlopen(self.link).read()).split("\n")
        for line in m3u8:
            if "#EXT-X-KEY" in line:
                if "IV" not in line:
                    pattern=re.compile(r'METHOD=(.*),URI="(.*)"')
                    try:
                        self.Method=pattern.search(line).group(1)
                        self.Key=pattern.search(line).group(2)
                        if self.Key:
                            if urldown(self.Key):
                                print("%s 下载失败。"%self.Key)
                            else:
                                line=re.sub(pattern,'METHOD=%s,URI="%s"'%(self.Method,self.Key.split("/")[-1]),line)
                    except AttributeError:
                        print(line)
                else:
                    pattern=re.compile(r'METHOD=(.*),URI="(.*)",IV=0x(.*)')
                    try:
                        self.Method=pattern.search(line).group(1)
                        self.Key=pattern.search(line).group(2)
                        self.IV=pattern.search(line).group(2)
                    except AttributeError:
                        print(line)
                    else:
                        line=re.sub(pattern,'METHOD=%s,URI="%s",IV=0x%s'%(self.Method,self.Key.split("/")[-1],self.IV),line)
                mu.write(line+"\n")
            elif "#" not in line :
                self.urls.append(line)
                mu.write(line.split("/")[-1]+"\n")
            else:
                mu.write(line+"\n")
        mu.close()
        with trange(len(self.urls)) as pbar:
            global PALLOW
            q=Queue(PALLOW)
            for url in pbar:
                time.sleep(0.1)
                pbar.set_description(self.urls[url])
                if urldown(self.urls[url]):
                    print("%s 下载失败。"%self.urls[url])
        for t in ThreadList:
            t.join()
        if os.path.isfile("%s.mp4"%self.link.split("/")[-2]):
            for f in [url.split("/")[-1] for url in self.urls]:
                os.remove(f)
        else:
            if os.system("ffmpeg -allowed_extensions ALL -i \"%s\" -c copy ..\\%s.mp4"%(m3u8name,self.link.split("/")[-2])):
                print("%s Failed."%(self.link.split("/")[-2]))
                
def processfunc(m3u8):  
    global ThreadList
    ThreadList=[]
    global trytime
    trytime=10
    global PALLOW
    PALLOW=Semaphore(100)
    M3U8_object(m3u8,m3u8.split("/")[-2].split(".")[0]+"_temp")
    
if __name__ == "__main__":
    os.chdir("D:\Project")
    urllist=[x.strip() for x in open("list.txt","r").readlines()]
    MAX_URLALLOW=16
    p=Pool(MAX_URLALLOW)
    for url in urllist:
        if ".mp4" in url:
            p.apply_async(urldown,args=(url,))
        elif ".m3u8" in url:
            p.apply_async(processfunc,args=(url,))
        else:
            p.apply_async(urldown,args=(url+".mp4",))
    p.close()
    p.join()


    
