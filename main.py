from tkinter import *
from pynput.mouse import Listener,Controller,Button
from pynput.keyboard import Controller as k_con,Key
from pyperclip import copy,paste
import time 
import requests
import random
import json
from hashlib import md5
import re
import math


class Translate():

    __appid = '20230219001567014'
    __appkey = 'Mzw9loC7iANB9XLT49VX'
    __url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

    def __init__(self,from_lang='en',to_lang='zh'):         
        self.from_lang = from_lang
        self.to_lang =  to_lang
    def query(self,target):
        salt = random.randint(32768, 65536)
        sign = self.make_md5(self.__appid + target + str(salt) + self.__appkey)
        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {
            'appid': self.__appid, 
            'q': target, 
            'from': self.from_lang, 
            'to': self.to_lang, 
            'salt': salt, 
            'sign': sign
            }
        # Send request
        r = requests.post(self.__url, params=payload, headers=headers)
        result = r.json()
        return result['trans_result']
        # return json.dumps(result, indent=4, ensure_ascii=False)

    def make_md5(self,s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

class MouseMonitor():
    __position=(0,0)
    __width=100
    __height=50
    __bias=5
    __old=None
    __die=False
    __show=False
    __update=time.time()
    TRANSCOLOR="white"
    def __init__(self):
        self.translate=Translate()
        self.mouse=Controller()
        self.__position=self.mouse.position
        self.keyboard=k_con()
        self.listener=Listener(on_move=self.on_move,on_click=self.on_click)
        self.listener.start()
        self.initial()
        self.window.mainloop()
        
    def initial(self):
        self.window=Tk()
        self.draw()
        self.label=Label(self.window,text="",width=self.__width-10,height=self.__height-1,justify="center")
        self.label.pack()
        self.hide()

    def draw(self): 
        size="%sx%s+%s+%s"%(self.__width,self.__height,self.mouse.position[0]+self.__bias,self.mouse.position[1]+self.__bias)
        self.window.overrideredirect(True)
        self.window.focus_force()
        self.window.wm_attributes("-topmost",1)
        self.window.geometry(size)
        self.window.update()

    def on_move(self,x,y):
        if not self.__die and self.__show:
            if time.time()-self.__update>0.1:
                try:
                    self.draw()
                except TclError:
                    self.__die=True
                   
    def on_click(self,x,y,button,state):
        print(x,y,button,state)
        if button == Button.left:
            if state:
                self.__position=(x,y)
                self.window.withdraw()
                self.__show=False
            else:
                if distance(self.__position,(x,y))>20:
                    self.copy()
                    time.sleep(0.5)
                    self.window.deiconify()
                    self.__show=True
        if state and button == Button.x2:         
            return self.quit()
        if state and button == Button.middle:
            self.hide()
    def hide(self):
        if self.__show:
            self.window.withdraw()
            self.__show=False
        else:
            self.window.deiconify()
            self.__show=True
    def copy(self):
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press("c")
            self.keyboard.release("c")
        time.sleep(0.5)
        text=paste().replace("\r\n"," ")
        text=re.sub("([^\u0030-\u0039\u0041-\u007a \(\)|\{\}’\'\":,.])"," ",text).replace("’","'")
        if text!=self.__old and len(text)>3:
            self.__old=text
            try:
                text_result=self.translate.query(text)
                result="\n".join([x["dst"] for x in text_result])
                copy(result)
            except KeyError:
                self.quit()
                print(text)
                raise KeyError("Can't translation.")
            text=text+"\nresult:"+result
            if 15*len(text)>500:
                text="\n".join([text[i:i+100]for i in range(0,len(text),100)])
            self.label.configure(text=text)
            if 15*len(text)<=15:
                self.__width=100
                self.__height=50
            elif 15*len(text)<=500:
                self.__width=15*len(text)
                self.__height=50
            else:
                self.__width=500
                self.__height=int(50*(1+(7*len(text)/500)))

            self.label.update()
        
    def quit(self):
        self.window.destroy()
        self.listener.stop()
        return False
def distance(a,b):
    sq=0
    for i in range(len(a)):
        sq+=(a[i]-b[i])**2
    return math.sqrt(sq)


if __name__== "__main__":
    MouseMonitor()