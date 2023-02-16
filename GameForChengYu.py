#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from diskcache import Cache
import json
from hashlib import md5
import random
import socket
#C:\Users\Administrator\AppData\Local\Programs\Python\Python36\Scripts\pyinstaller.exe -D C:\wamp\www\python\liuchengrui\main_func.py --hidden-import tkinter --hidden-import diskcache --hidden-import json --hidden-import hashlib --hidden-import random --hidden-import socket
HOST = socket.gethostbyname(socket.gethostname())
m = md5()
m.update(HOST.encode("utf8"))
IP = m.hexdigest()
cache = Cache('./db')
cache.set('FL_NUM'+IP, 0,expire=None, read=True,tag='失败次数', retry=True)
cache.set('SUC_NUM'+IP,0,expire=None, read=True, tag='成功次数',retry=True)


class CC_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name

    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("成语猜猜乐_v1.2")           #窗口名
        #self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('400x180+10+10')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：
        self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签
        self.log_label = Label(self.init_window_name, text="残缺成语")
        self.log_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="猜对了么")
        self.result_data_label.grid(row=0, column=12)
        self.init_data_label = Label(self.init_window_name, text="输入成语")
        self.init_data_label.grid(row=12, column=0)
        #文本框

        self.log_data_Text = Label(self.init_window_name, width=10, height=2)  # 日志框
        self.log_data_Text.grid(row=1, column=0,rowspan=5, columnspan=10)
        self.result_data_Text = Text(self.init_window_name, width=30, height=10)  #处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=5)
        self.init_data_Text = Text(self.init_window_name, width=10, height=1)  # 原始数据录入框
        self.init_data_Text.grid(row=13, column=0, columnspan=10)
        self.init_static_Text = Label(self.init_window_name, width=30, height=1)  # 数据统计
        self.init_static_Text.grid(row=13, column=12,rowspan=10, columnspan=2)
        #初始化成语块
        words =self.jump_to_next()
        cache.set('CHENG_YU',str(words), expire=None, read=True, tag='当前成语', retry=True)
        self.str_trans_to_md5_button = Button(self.init_window_name, text="猜一猜", bg="lightblue", width=8,command=lambda:self.check_word_right(words))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=7, column=11)
        self.str_trans_to_next_button = Button(self.init_window_name, text="跳过", bg="lightblue", width=8,command=self.jump_to_next)  # 调用内部方法  加()为直接调用
        self.str_trans_to_next_button.grid(row=9, column=11)


    #功能函数
    def check_word_right(self,words):

        src = self.init_data_Text.get(1.0,END).strip().replace("\n","")
        chengyu = cache.get('CHENG_YU', default=False, expire_time=True, tag=True, retry=True)
        CY = eval(''.join(chengyu[0]))
        #enter = self.log_data_Text.get(1.0, END).strip().replace("\n", "").encode()
        if src and len(src)>1:

                if src==CY['word']:
                    #输出到界面
                    self.result_data_Text.delete(1.0,END)
                    self.result_data_Text.insert(1.0,get_result_msg(1,CY))
                    #计数
                    SUC_NUM = cache.get('SUC_NUM'+IP, default=False, expire_time=True, tag=True, retry=True)
                    cache.set('SUC_NUM'+IP, int(SUC_NUM[0])+1, expire=None, read=True, tag='成功次数',retry=True)
                    words  = self.jump_to_next()
                    self.log_data_Text.config(text=self.write_word_to_Text(words))
                    cache.set('CHENG_YU', str(words), expire=None, read=True, tag='当前成语', retry=True)
                else:
                    FL_NUM = cache.get('FL_NUM'+ IP, default=False, expire_time=True, tag=True, retry=True)
                    cache.set('FL_NUM'+ IP, int(FL_NUM[0]) + 1, expire=None, read=True,tag='失败次数', retry=True)
                    self.result_data_Text.delete(1.0,END)
                    self.result_data_Text.insert(1.0,get_result_msg(0,CY))
        else:
            self.result_data_Text.delete(1.0, END)
            self.write_word_to_Text(CY)
            self.result_data_Text.insert(1.0, get_result_msg(2,CY))
        self.init_static_Text.config(text=self.static_data())
    #跳到下一个成语
    def jump_to_next(self):
        words = get_word()
        self.write_word_to_Text(words)
        cache.set('CHENG_YU', str(words), expire=None, read=True, tag='当前成语', retry=True)
        return words
    #记录成功失败数
    def static_data(self):
        SUC_NUM =cache.get('SUC_NUM'+IP, default=False, expire_time=True, tag=True, retry=True)
        FL_NUM  =cache.get('FL_NUM'+IP, default=False, expire_time=True, tag=True, retry=True)
        return '成功了'+str(SUC_NUM[0])+"次.....失误了"+str(FL_NUM[0])+'次。'

    #成语动态打印
    def write_word_to_Text(self,words):
        cy = words['word']
        n = random.randint(0, 4)
        m = random.randint(1, 3)
        # 判定取出一个的情况
        yc = ''
        if len(cy[n:m]) == 1:
            yc = replace_char(cy, 'X', n, m)
            if len(yc) > 1:  # 替换成功的

                self.log_data_Text.config(text=yc)
            else:
                self.log_data_Text.config(text="".join((lambda x: (x.sort(), x)[1])(list(cy))))
        else:
            self.log_data_Text.config(text="".join((lambda x: (x.sort(), x)[1])(list(cy))))
# # 随机取出一个成语、习语
def get_word():
    path = './'
    with open(path + 'idiom.json', 'r', encoding='utf-8') as words:
        data = words.read()
    word = json.loads(data)
    item = random.choice(word)
    return item
def replace_char(string, char, n,m):
    string = list(string)
    string[n:m] = char
    return ''.join(string)

def get_result_msg(status,words):
    list  = ['您回答正确了！！','恭喜你！答对了','答对了，今晚加鸡腿','棒棒哒，可以吹牛皮了','您有答对了，帅气！','完美！继续加油！','您真是太厉害了，好崇拜你哦！','吃鸡成功，开启下一程！']
    wrong =['欧麦嘎，魔法怎么失灵了','继续努力加油哦！','吃鸡失败，晚上加班','回答错误，罚你三杯','小哥哥，你不够力呀，加油哟','错了，可能太难了，再来一把','虽然你很帅，错了我照样打你','任务失败，开黑棍啦，打黑，打黑']
    if status ==1:
        return random.choice(list)+"\n"+"出自："+"\n"+words['derivation']+"\n"+"成语释义："+"\n"+words['explanation']
    elif status ==0:
        return random.choice(wrong) + "\n"
    else:
        return  "请输入您猜测的成语！\n"
def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    CY_CODE = CC_GUI(init_window)
    # 设置根窗口默认属性
    CY_CODE.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

gui_start()


